"""CPU profile-learning benchmarks with direct unparsed symbolic-AST ODE handoff.

Every solver receives the live symbolic ODE AST (compiled directly in-memory via
SymPy AST / ``sp.lambdify`` without string parsing or manual formula edits) and its
initial trace map. Exact/reference profiles are evaluated only after fitting for
validation. Supports both linear and nonlinear reduced ODEs of order 1..3.
"""
from dataclasses import asdict, dataclass
import argparse
from math import comb, factorial
import json
import os
from time import perf_counter

os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
os.environ.setdefault('OMP_NUM_THREADS', '1')
os.environ.setdefault('MKL_NUM_THREADS', '1')

import numpy as np
from numpy.polynomial import Chebyshev, Polynomial
from scipy.integrate import solve_ivp
from scipy.linalg import lstsq
from scipy.optimize import least_squares
import sympy as sp


@dataclass(frozen=True)
class Settings:
    seed: int = 27
    width: int = 6
    chebyshev_degree: int = 15
    taylor_degree: int = 22
    train_coordinates: int = 24
    test_coordinates: int = 401
    max_nfev: int = 150


def _ast_taylor_series(rhs_expr, z_sym, jet_syms, p_sym, degree, p_val, z0_val, init_trace):
    """Automatic truncated power-series recurrence on the live SymPy AST of F^(r) = rhs."""
    order = len(jet_syms)
    coeffs = [float(init_trace[k]) / factorial(k) for k in range(order)]
    sub_p = rhs_expr.subs(p_sym, sp.Float(float(p_val))) if p_sym is not None else rhs_expr

    def _mul_poly(a, b, deg):
        out = [0.0] * (deg + 1)
        la, lb = len(a), len(b)
        for i in range(min(la, deg + 1)):
            ai = a[i]
            if ai == 0.0:
                continue
            for j in range(min(lb, deg + 1 - i)):
                out[i + j] += ai * b[j]
        return out

    def _pow_real(base_s, alpha, deg):
        b0 = base_s[0]
        if abs(b0) < 1e-15:
            raise ValueError('singular Taylor base at expansion center')
        u = [0.0] + [base_s[i] / b0 for i in range(1, deg + 1)]
        res = [1.0] + [0.0] * deg
        term = [1.0] + [0.0] * deg
        binom_c = 1.0
        for k in range(1, deg + 1):
            binom_c *= (alpha - (k - 1)) / k
            term = _mul_poly(term, u, deg)
            for idx in range(deg + 1):
                res[idx] += binom_c * term[idx]
        pref = float(b0 ** alpha)
        return [pref * v for v in res]

    def _eval_node(node, env, deg):
        if node in env:
            arr = env[node]
            return arr[:deg + 1] + [0.0] * max(0, deg + 1 - len(arr))
        if node.is_Number:
            return [float(node)] + [0.0] * deg
        if node.is_Add:
            acc = [0.0] * (deg + 1)
            for arg in node.args:
                va = _eval_node(arg, env, deg)
                for idx in range(deg + 1):
                    acc[idx] += va[idx]
            return acc
        if node.is_Mul:
            acc = [1.0] + [0.0] * deg
            for arg in node.args:
                acc = _mul_poly(acc, _eval_node(arg, env, deg), deg)
            return acc
        if node.is_Pow:
            b_s = _eval_node(node.base, env, deg)
            if node.exp.is_Integer:
                exp_i = int(node.exp)
                if exp_i >= 0:
                    acc = [1.0] + [0.0] * deg
                    for _ in range(exp_i):
                        acc = _mul_poly(acc, b_s, deg)
                    return acc
                return _pow_real(b_s, float(exp_i), deg)
            return _pow_real(b_s, float(node.exp), deg)
        if node.func == sp.exp:
            u = _eval_node(node.args[0], env, deg)
            u0 = u[0]
            du = [0.0] + u[1:deg + 1]
            res = [1.0] + [0.0] * deg
            term = [1.0] + [0.0] * deg
            for k in range(1, deg + 1):
                term = _mul_poly(term, du, deg)
                inv_f = 1.0 / factorial(k)
                for idx in range(deg + 1):
                    res[idx] += inv_f * term[idx]
            e0 = float(np.exp(u0))
            return [e0 * v for v in res]
        if node.func == sp.log:
            u = _eval_node(node.args[0], env, deg)
            if u[0] <= 0.0:
                raise ValueError('nonpositive log argument in Taylor expansion')
            du_dx = [(i + 1) * u[i + 1] for i in range(deg)] + [0.0]
            quot = _mul_poly(du_dx, _pow_real(u, -1.0, deg), deg)
            return [float(np.log(u[0]))] + [quot[i - 1] / i for i in range(1, deg + 1)]
        if node.func in (sp.sin, sp.cos):
            u = _eval_node(node.args[0], env, deg)
            u0 = u[0]
            du = [0.0] + u[1:deg + 1]
            s0, c0 = float(np.sin(u0)), float(np.cos(u0))
            res = [(s0 if node.func == sp.sin else c0)] + [0.0] * deg
            term = [1.0] + [0.0] * deg
            for k in range(1, deg + 1):
                term = _mul_poly(term, du, deg)
                cyc = (s0, c0, -s0, -c0)[k % 4] if node.func == sp.sin else (c0, -s0, -c0, s0)[k % 4]
                inv_f = cyc / factorial(k)
                for idx in range(deg + 1):
                    res[idx] += inv_f * term[idx]
            return res
        raise ValueError(f'unsupported AST node in Taylor expansion: {node}')

    for m_deg in range(max(0, degree - order + 1)):
        env = {z_sym: [float(z0_val), 1.0] + [0.0] * max(0, m_deg - 1)}
        for k_ord, j_sym in enumerate(jet_syms):
            deriv_c = []
            for idx in range(k_ord, len(coeffs)):
                fall = 1.0
                for q_f in range(k_ord):
                    fall *= (idx - q_f)
                deriv_c.append(fall * coeffs[idx])
            env[j_sym] = deriv_c + [0.0] * max(0, m_deg + 1 - len(deriv_c))
        rhs_m = _eval_node(sub_p, env, m_deg)[m_deg]
        nxt = m_deg + order
        denom = 1.0
        for q_f in range(order):
            denom *= (nxt - q_f)
        coeffs.append(rhs_m / denom)
    return coeffs[:degree + 1]


def _compile_reference_solver(rhs_expr, z_sym, jet_syms, p_sym, profile_fn, ode_expr, left_val, allow_dsolve=True):
    """Build post-fit validation reference from sp.dsolve when linear, else DOP853."""
    order = len(jet_syms)
    ic_syms = sp.symbols(f'_ic0:{order}', real=True)
    # Attempt exact closed-form dsolve only on linear ODEs (avoids SymPy nonlinear dsolve hangs)
    if allow_dsolve:
        try:
            diffeq = ode_expr
            ics = {
                (sp.diff(profile_fn, z_sym, k).subs(z_sym, sp.Rational(str(left_val)))
                 if k else profile_fn.subs(z_sym, sp.Rational(str(left_val)))): ic_syms[k]
                for k in range(order)
            }
            sol = sp.dsolve(diffeq, profile_fn, ics=ics)
            if isinstance(sol, sp.Equality) and not sol.rhs.has(sp.Integral, sp.Derivative, sp.RootSum):
                sol_expr = sol.rhs
                jet_exprs = [sp.diff(sol_expr, z_sym, k) for k in range(4)]
                args = (z_sym, *( (p_sym,) if p_sym is not None else () ), *ic_syms)
                fns = [sp.lambdify(args, je, 'numpy') for je in jet_exprs]

                def _closed_ref(z_arr, p_val, trace_vals):
                    z_np = np.asarray(z_arr, dtype=float)
                    call_args = (z_np, *( (float(p_val),) if p_sym is not None else () ), *[float(v) for v in trace_vals])
                    return tuple(np.broadcast_to(np.asarray(fn(*call_args), dtype=float), z_np.shape).copy() for fn in fns)

                return _closed_ref, 'symbolic_dsolve_ast'
        except Exception:
            pass

    # Fallback: high-order DOP853 numerical integration of the compiled normal-form AST
    args_rhs = (z_sym, *jet_syms, *( (p_sym,) if p_sym is not None else () ))
    rhs_fn = sp.lambdify(args_rhs, rhs_expr, 'numpy')
    higher_exprs = []
    cur = rhs_expr
    higher_exprs.append(cur)
    for _ in range(order, 4):
        nxt_d = sp.diff(cur, z_sym)
        for k_i in range(order - 1):
            nxt_d += jet_syms[k_i + 1] * sp.diff(cur, jet_syms[k_i])
        nxt_d += rhs_expr * sp.diff(cur, jet_syms[order - 1])
        cur = sp.cancel(nxt_d)
        higher_exprs.append(cur)
    higher_fns = [sp.lambdify(args_rhs, he, 'numpy') for he in higher_exprs]

    def _ivp_ref(z_arr, p_val, trace_vals):
        z_np = np.asarray(z_arr, dtype=float)
        z_flat = np.ravel(z_np)
        z_end = float(max(np.max(z_flat), left_val + 1e-9))

        def _vec_rhs(t_s, y_s):
            extra = (float(p_val),) if p_sym is not None else ()
            top = float(rhs_fn(t_s, *y_s, *extra))
            return [*y_s[1:], top]

        ivp = solve_ivp(
            _vec_rhs, (float(left_val), z_end), [float(v) for v in trace_vals],
            method='DOP853', t_eval=z_flat, rtol=3e-14, atol=1e-14,
        )
        if not ivp.success:
            raise ArithmeticError(f'reference DOP853 integration failed: {ivp.message}')
        jets_out = [ivp.y[k].reshape(z_np.shape) for k in range(min(order, 4))]
        extra_p = (float(p_val),) if p_sym is not None else ()
        state_cols = [ivp.y[k] for k in range(order)]
        for idx_h in range(4 - len(jets_out)):
            vals_h = np.asarray(higher_fns[idx_h](z_flat, *state_cols, *extra_p), dtype=float)
            jets_out.append(np.broadcast_to(vals_h, z_flat.shape).reshape(z_np.shape).copy())
        return tuple(jets_out[:4])

    return _ivp_ref, 'compiled_dop853_ast'


@dataclass(frozen=True)
class Case:
    name: str
    left: float
    trace_interval: tuple
    trace_order: int
    coefficients: tuple
    right_hand_side: object
    trace: object
    taylor: object
    exact: object
    fields: object
    original_residual: object
    ode_residual: object = None
    is_linear: bool = True
    training_order: int = 1
    diagnostic_order: int = 1
    symbolic_ode_expr: object = None
    handoff_mode: str = 'direct_symbolic_ast_lambdify'

    @classmethod
    def from_reduction(
        cls,
        name,
        reduction,
        *,
        left,
        trace_interval,
        trace_exprs,
        parameter_symbol,
        parameter_values=None,
        use_integrated_ode=False,
        ode_override_expr=None,
        diagnostic_expr=None,
        lift_exprs=None,
        section_values=None,
        positive_jet_guards=(),
    ):
        """Construct an ML benchmark Case directly in-memory from a live SymPy ReducedODE.

        Zero string parsing, zero manual ODE lambdas, zero manual Taylor recurrences, and
        zero manual exact-solution formulas are used.
        """
        params = dict(parameter_values or {})
        z_sym = reduction.graph.z if getattr(reduction, 'graph', None) is not None else sp.Symbol('z', real=True)
        if ode_override_expr is not None:
            raw_ode, profile_fn = ode_override_expr
        elif use_integrated_ode and reduction.integrated_ode is not None:
            raw_ode = reduction.integrated_ode
            profile_fn = reduction.target_profile or reduction.graph.profiles[0]
        else:
            raw_ode = reduction.reduced_equations[0]
            profile_fn = reduction.target_profile or reduction.graph.profiles[0]

        ode_sub = sp.together(raw_ode.subs(params).doit())
        _, den_ode = ode_sub.as_numer_denom()
        var_den = sp.Mul(*[f for f in sp.Mul.make_args(den_ode) if not f.is_Number])
        ode_clean = sp.expand(sp.cancel(ode_sub * var_den))

        deriv_orders = [d.derivative_count for d in ode_clean.atoms(sp.Derivative) if d.expr == profile_fn]
        order = int(max(deriv_orders, default=0))
        if order < 1 or order > 3:
            raise ValueError(f'{name}: expected scalar ODE of order 1..3, got order {order}')
        if len(trace_exprs) != order:
            raise ValueError(f'{name}: trace_exprs length {len(trace_exprs)} != ODE order {order}')

        J_syms = sp.symbols('_J0:4', real=True)
        jet_map = {sp.diff(profile_fn, z_sym, k) if k else profile_fn: J_syms[k] for k in range(3, -1, -1)}
        ode_j = sp.expand(ode_clean.xreplace(jet_map))

        # Solve symbolically for highest derivative J_syms[order] = rhs_normal(z, J0..J_{r-1}, p)
        sol_top = sp.solve(ode_j, J_syms[order])
        if not sol_top:
            raise ValueError(f'{name}: reduced ODE could not be solved for order-{order} jet')
        rhs_normal = sp.cancel(sol_top[0])
        # Normalize sign so leading jet has positive coefficient on principal domain when linear
        lead_c = sp.diff(ode_j, J_syms[order])
        if lead_c.is_Number and lead_c < 0:
            ode_j = -ode_j
            ode_clean = -ode_clean

        # Detect linearity in (_J0 .. _J_{order})
        active_j = J_syms[:order + 1]
        is_lin = all(
            sp.diff(ode_j, ja, jb) == 0 for ja in active_j for jb in active_j
        ) and not any(
            p_atom.base.has(*active_j) and not p_atom.exp.is_Integer for p_atom in ode_j.atoms(sp.Pow)
        )

        coeffs_tuple = ()
        rhs_callable = None
        if is_lin:
            lin_coeffs = [sp.simplify(sp.diff(ode_j, J_syms[k])) for k in range(order + 1)]
            rem_lin = sp.simplify(ode_j - sum(c_k * J_syms[k] for k, c_k in enumerate(lin_coeffs)))
            if any(c_k.has(parameter_symbol) for c_k in lin_coeffs if parameter_symbol is not None):
                is_lin = False
            else:
                compiled_c = []
                for c_k in lin_coeffs:
                    if c_k.has(z_sym):
                        fn_c = sp.lambdify(z_sym, c_k, 'numpy')
                        compiled_c.append(lambda z_v, _fn=fn_c: np.broadcast_to(np.asarray(_fn(z_v), dtype=float), np.asarray(z_v).shape))
                    else:
                        compiled_c.append(float(c_k))
                coeffs_tuple = tuple(compiled_c)
                rhs_sym = sp.simplify(-rem_lin)
                rhs_args = (z_sym, *( (parameter_symbol,) if parameter_symbol is not None else () ))
                fn_rhs = sp.lambdify(rhs_args, rhs_sym, 'numpy')
                rhs_callable = (
                    (lambda z_v, p_v, _f=fn_rhs: np.asarray(_f(z_v, p_v), dtype=float))
                    if parameter_symbol is not None
                    else (lambda z_v, _p_v, _f=fn_rhs: np.asarray(_f(z_v), dtype=float))
                )

        # General compiled ODE residual (used for nonlinear PINN/Chebyshev and verification)
        res_args = (z_sym, *J_syms, *( (parameter_symbol,) if parameter_symbol is not None else () ))
        fn_ode_res = sp.lambdify(res_args, ode_j, 'numpy')

        def _ode_res_fn(z_v, jets_v, p_v):
            z_np = np.asarray(z_v, dtype=float)
            extra = (p_v,) if parameter_symbol is not None else ()
            val = fn_ode_res(z_np, jets_v[0], jets_v[1], jets_v[2], jets_v[3], *extra)
            return np.broadcast_to(np.asarray(val, dtype=float), z_np.shape)

        # Trace callable (supports both scalar float p_v and NumPy array p_v)
        tr_syms = tuple(sp.sympify(te).subs(params) for te in trace_exprs)
        tr_fns = [
            (lambda p_in, _fn=sp.lambdify((parameter_symbol,), te, 'numpy'):
             float(_fn(p_in)) if np.ndim(p_in) == 0 else np.asarray(_fn(p_in), dtype=float))
            if (parameter_symbol is not None and te.has(parameter_symbol))
            else (lambda p_in, _v=float(te): _v if np.ndim(p_in) == 0 else np.full_like(np.asarray(p_in, dtype=float), _v))
            for te in tr_syms
        ]
        trace_fn = lambda p_v: tuple(fn(p_v) for fn in tr_fns)

        # Automatic AST Taylor callable
        taylor_fn = lambda deg_n, p_v, z0_v, tr_v: _ast_taylor_series(
            rhs_normal, z_sym, J_syms[:order], parameter_symbol, deg_n, p_v, z0_v, tr_v
        )

        # Automatic validation reference solver (post-fit only)
        ode_for_dsolve = ode_clean
        ref_solver, ref_mode = _compile_reference_solver(
            rhs_normal, z_sym, J_syms[:order], parameter_symbol, profile_fn, ode_for_dsolve, left, allow_dsolve=is_lin
        )
        exact_fn = lambda z_v, p_v: ref_solver(z_v, p_v, trace_fn(p_v))

        # Lift expressions -> physical spacetime fields
        if section_values is not None:
            sec_map = dict(section_values)
        elif getattr(reduction, 'graph', None) is not None:
            if getattr(reduction.graph, 'orbit', None) is not None:
                sec_map = {w_o: sp.S.Zero for w_o in reduction.graph.orbit[1:]}
            elif getattr(reduction.graph, 'section', None) is not None:
                sec_map = dict(reduction.graph.section)
            else:
                sec_map = {}
        else:
            sec_map = {}

        raw_lifts = lift_exprs if lift_exprs is not None else (
            reduction.reconstructed_lifts or reduction.graph.lifts
        )
        allowed_lift_syms = {z_sym, *J_syms}
        compiled_lifts = []
        for l_expr in raw_lifts:
            l_sub = sp.sympify(l_expr).subs(params).subs(sec_map, simultaneous=True).doit()
            # Map any profile(arg) and its derivatives onto profile_fn(z_sym) before jet_map replacement
            for f_atom in list(l_sub.atoms(sp.Function)):
                if f_atom.func == profile_fn.func and f_atom.args and f_atom.args[0] != z_sym:
                    l_sub = l_sub.subs(f_atom.args[0], z_sym).doit()
            l_sub = l_sub.xreplace(jet_map)
            if lift_exprs is None and (l_sub.atoms(sp.Function) - set(l_sub.atoms(sp.exp, sp.log, sp.sin, sp.cos, sp.tan, sp.tanh))
                                       or not l_sub.free_symbols.issubset(allowed_lift_syms)):
                continue
            compiled_lifts.append(sp.lambdify((z_sym, *J_syms), l_sub, 'numpy'))
        if not compiled_lifts:
            compiled_lifts.append(sp.lambdify((z_sym, *J_syms), J_syms[0], 'numpy'))

        guard_fns = [
            sp.lambdify((z_sym, *J_syms), sp.sympify(g_expr).subs(params).subs(sec_map).xreplace(jet_map), 'numpy')
            for g_expr in positive_jet_guards
        ]

        def _fields_fn(z_v, jets_v):
            z_np = np.asarray(z_v, dtype=float)
            for g_fn in guard_fns:
                g_val = np.asarray(g_fn(z_np, jets_v[0], jets_v[1], jets_v[2], jets_v[3]), dtype=float)
                if np.any(g_val <= 0.0):
                    raise ValueError(f'{name}: positivity chart guard violated')
            stacked = [
                np.broadcast_to(np.asarray(l_fn(z_np, jets_v[0], jets_v[1], jets_v[2], jets_v[3]), dtype=float), z_np.shape)
                for l_fn in compiled_lifts
            ]
            return np.stack(stacked)

        # Diagnostic residual in parent PDE balance
        if diagnostic_expr is not None:
            diag_sym = sp.sympify(diagnostic_expr).subs(params).subs(sec_map).doit()
        elif use_integrated_ode and reduction.equations:
            diag_sym = sp.sympify(reduction.equations[0]).subs(params).subs(sec_map).doit()
        else:
            diag_sym = ode_clean
        diag_j = sp.expand(diag_sym.xreplace(jet_map))
        diag_orders = [k for k in range(4) if diag_j.has(J_syms[k])]
        diag_order = int(max(diag_orders, default=order))
        fn_diag = sp.lambdify(res_args, diag_j, 'numpy')

        def _orig_res_fn(z_v, jets_v, p_v):
            z_np = np.asarray(z_v, dtype=float)
            extra = (p_v,) if parameter_symbol is not None else ()
            val = fn_diag(z_np, jets_v[0], jets_v[1], jets_v[2], jets_v[3], *extra)
            return np.broadcast_to(np.asarray(val, dtype=float), z_np.shape)

        return cls(
            name=name,
            left=float(left),
            trace_interval=(float(trace_interval[0]), float(trace_interval[1])),
            trace_order=order,
            coefficients=coeffs_tuple,
            right_hand_side=rhs_callable,
            trace=trace_fn,
            taylor=taylor_fn,
            exact=exact_fn,
            fields=_fields_fn,
            original_residual=_orig_res_fn,
            ode_residual=_ode_res_fn,
            is_linear=is_lin,
            training_order=order,
            diagnostic_order=diag_order,
            symbolic_ode_expr=ode_clean,
            handoff_mode=f'direct_symbolic_ast_lambdify ({ref_mode})',
        )


def product(left, right):
    return tuple(sum(comb(k, i) * left[i] * right[k - i] for i in range(k + 1))
                 for k in range(len(left)))


def tanh_jet(values):
    y = np.tanh(values[0])
    a = 1 - y * y
    d, dd, ddd = values[1:]
    return (y, a * d, a * (dd - 2 * y * d * d),
            a * (ddd - 6 * y * d * dd + (6 * y * y - 2) * d * d * d))


def monomial_jet(x, power):
    return tuple(np.zeros_like(x) if k > power else
                 factorial(power) / factorial(power - k) * x ** (power - k)
                 for k in range(4))


def trace_jet(case, x, p):
    values = case.trace(p)
    return tuple(sum(values[i] * monomial_jet(x, i)[k] / factorial(i)
                     for i in range(case.trace_order)) for k in range(4))


def operator(case, jets, z):
    return sum(c(z) * d if callable(c) else c * d
               for c, d in zip(case.coefficients, jets))


def eval_ode_defect(case, z, jets, p):
    if case.is_linear and case.coefficients:
        return operator(case, jets, z) - case.right_hand_side(z, p)
    return case.ode_residual(z, jets, p)


def liquid_model(case, z, p, params, width):
    x = np.ravel(z - case.left)
    p = np.broadcast_to(p, z.shape).ravel()
    lo, hi = case.trace_interval
    pscaled = (2 * p - lo - hi) / (hi - lo)
    slopes, biases, gates = params[:3 * width].reshape(3, width)
    switch = 3 * width + width * width
    influence = params[3 * width:switch].reshape(width, width)
    readout = params[switch:].reshape(2, width)
    u = (2 * x[:, None] - 1) * slopes + biases
    v = tanh_jet((u, np.broadcast_to(2 * slopes, u.shape), np.zeros_like(u), np.zeros_like(u)))
    mixed = tanh_jet(tuple(vv @ influence.T for vv in v))
    layers = tuple(vv + gg * np.tanh(gates) for vv, gg in zip(v, mixed))
    combined = tuple((layer @ readout[0] + pscaled * (layer @ readout[1])).reshape(z.shape)
                     for layer in layers)
    correction = product(monomial_jet(z - case.left, case.trace_order), combined)
    return tuple(a + b for a, b in zip(trace_jet(case, z - case.left, p.reshape(z.shape)), correction))


def fit_liquid(case, settings):
    q = (np.arange(settings.train_coordinates) + .5) / settings.train_coordinates
    lo, hi = case.trace_interval
    z, p = np.meshgrid(case.left + q, np.linspace(lo, hi, 5))
    z, p = z.ravel(), p.ravel()
    rng = np.random.default_rng(settings.seed)
    w = settings.width
    initial = rng.normal(0, .32, size=5 * w + w * w)
    initial[:w] = rng.uniform(.55, 1.5, size=w)

    def residual(weights):
        jets = liquid_model(case, z, p, weights, w)
        return eval_ode_defect(case, z, jets, p)

    fit = least_squares(residual, initial, max_nfev=settings.max_nfev,
                        gtol=1e-10, ftol=1e-10, xtol=1e-10)

    def predict(z_eval, p_eval):
        return liquid_model(case, np.asarray(z_eval), p_eval, fit.x, w)

    return predict, {
        'nfev': fit.nfev,
        'parameters': len(initial),
        'status': 'budget_exhausted' if fit.status == 0 else 'optimizer_terminated',
        'interpretation': 'fixed-budget approximation; no convergence claim',
        'optimizer_status': fit.status,
        'sample_train_rms': float(np.sqrt(np.mean(fit.fun ** 2))),
    }


def polynomial_jet(polynomial, x):
    return tuple(polynomial.deriv(k)(x) for k in range(4))


def chebyshev_profile(case, p, settings):
    n = settings.chebyshev_degree
    nodes = case.left + (1 - np.cos(np.pi * (np.arange(n + 2) + .5) / (n + 2))) / 2
    delta = nodes - case.left

    def lift(poly, x):
        return product(monomial_jet(x, case.trace_order), polynomial_jet(poly, x))

    if case.is_linear and case.coefficients:
        basis = [Chebyshev.basis(k, domain=[0, 1]) for k in range(n + 1)]
        matrix = np.column_stack([operator(case, lift(b, delta), nodes) for b in basis])
        baseline = operator(case, trace_jet(case, delta, p), nodes)
        target = np.broadcast_to(case.right_hand_side(nodes, p), nodes.shape) - baseline
        coeff, _, rank, _ = lstsq(matrix, target, lapack_driver='gelsd')
        if rank != n + 1:
            raise ArithmeticError(f'Rank {rank} in degree {n} collocation')
    else:
        tr_nodes = trace_jet(case, delta, p)

        def _nonlin_colloc(c_vec):
            poly_c = Chebyshev(c_vec, domain=[0, 1])
            jets_c = tuple(a + b for a, b in zip(tr_nodes, lift(poly_c, delta)))
            return case.ode_residual(nodes, jets_c, p)

        sol_c = least_squares(_nonlin_colloc, np.zeros(n + 1), gtol=1e-13, ftol=1e-13, xtol=1e-13, max_nfev=400)
        coeff = sol_c.x

    poly = Chebyshev(coeff, domain=[0, 1])

    def predict(z_eval):
        x = np.asarray(z_eval) - case.left
        return tuple(a + b for a, b in zip(trace_jet(case, x, p), lift(poly, x)))

    return predict


def taylor_profile(case, p, settings):
    """Use two linked series charts to keep |z-z0| <= 1/2 per chart."""
    n = settings.taylor_degree
    polys = []
    trace = case.trace(p)
    for center in (case.left, case.left + .5):
        coeff = case.taylor(n, p, center, trace)
        poly = Polynomial(coeff)
        trace = tuple(poly.deriv(k)(.5) for k in range(case.trace_order))
        polys.append(poly)

    def predict(z_eval):
        x = np.asarray(z_eval) - case.left
        return tuple(np.where(x <= .5, left_v, right_v) for left_v, right_v in zip(
            polynomial_jet(polys[0], x), polynomial_jet(polys[1], x - .5)))

    return predict


def compare(case, settings=Settings()):
    start = perf_counter()
    liquid, fit = fit_liquid(case, settings)
    fit['elapsed_seconds'] = perf_counter() - start
    lo, hi = case.trace_interval
    points = settings.test_coordinates
    z = case.left + (np.arange(points) + .5) / points
    traces = lo + (hi - lo) * (np.arange(4) + .5) / 4
    methods = ('LNN-PINN', 'Chebyshev', 'Taylor')
    logs = {k: {'errors': [], 'residuals': [], 'seconds': 0., 'trace_error': 0.} for k in methods}
    for p in traces:
        reference = case.fields(z, case.exact(z, p))
        for method in methods:
            start = perf_counter()
            if method == 'LNN-PINN':
                predict = lambda z_in, _p=p: liquid(z_in, _p)
            elif method == 'Chebyshev':
                predict = chebyshev_profile(case, p, settings)
            else:
                predict = taylor_profile(case, p, settings)
            estimated = predict(z)
            approximated = case.fields(z, estimated)
            init = predict(np.array([case.left]))
            log = logs[method]
            log['seconds'] += perf_counter() - start
            error = approximated - reference
            residual = case.original_residual(z, estimated, p)
            if not np.all(np.isfinite(error)) or not np.all(np.isfinite(residual)):
                raise ArithmeticError(f'{case.name} {method} left its valid chart')
            log['errors'].extend(error.ravel())
            log['residuals'].extend(np.atleast_1d(np.abs(residual)).ravel())
            log['trace_error'] = max(log['trace_error'], max(
                abs(float(v[0]) - desired) for v, desired in zip(init, case.trace(p))))
    metrics = {
        k: {
            'field_rms': float(np.sqrt(np.mean(np.square(v['errors'])))),
            'field_maximum': float(np.max(np.abs(v['errors']))),
            'original_residual_maximum': float(max(v['residuals'])),
            'trace_error_maximum': v['trace_error'],
            'setup_and_prediction_seconds_all_traces': v['seconds'],
        }
        for k, v in logs.items()
    }
    selection = select_method(metrics)
    res_orders = (
        {'training': case.training_order, 'diagnostic': case.diagnostic_order}
        if case.symbolic_ode_expr is not None
        else ({'training': 2, 'diagnostic': 3} if 'P at m=1' in case.name else {'training': 1, 'diagnostic': 1})
    )
    return {
        'case': case.name,
        'handoff_mode': case.handoff_mode,
        'symbolic_ode': str(case.symbolic_ode_expr) + ' = 0' if case.symbolic_ode_expr is not None else None,
        'settings': asdict(settings),
        'fit': fit,
        'method_display_name': 'adapted gated cell',
        'trace_dependence': 'affine interpolation; not nonlinear parameter learning',
        'residual_orders': res_orders,
        'test_traces': traces.tolist(),
        'metrics': metrics,
        'selection': selection,
    }


def select_method(metrics, trace_tolerance=1e-8, residual_tolerance=1e-6):
    admissible = [k for k, v in metrics.items()
                  if v['trace_error_maximum'] <= trace_tolerance and v['original_residual_maximum'] <= residual_tolerance]
    ranked = sorted(admissible, key=lambda k: (metrics[k]['original_residual_maximum'],
                                               metrics[k]['setup_and_prediction_seconds_all_traces']))
    chosen = ranked[0] if ranked else None
    return {
        'rule': 'admit trace error <= %g and sampled original residual <= %g; rank by residual, then cost'
                % (trace_tolerance, residual_tolerance),
        'admissible': ranked,
        'rejected': sorted(set(metrics) - set(admissible)),
        'selected': chosen,
        'selected_field_maximum': metrics[chosen]['field_maximum'] if chosen else None,
        'evidence_level': 'sampled residual on 401 held-out coordinates; not a continuous bound',
    }


def cli(cases):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=Settings.seed)
    parser.add_argument('--max-nfev', type=int, default=Settings.max_nfev)
    opts = parser.parse_args()
    settings = Settings(seed=opts.seed, max_nfev=opts.max_nfev)
    print(json.dumps([compare(case, settings) for case in cases], indent=2))
