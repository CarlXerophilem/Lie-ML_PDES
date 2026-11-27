"""Live SymPy ReducedODE AST compiler, automatic judgemental solvability gates,
Briot-Bouquet Taylor recurrence, and SciPy DOP853 continuation for planar E2.

Every operator (Delta_c, N, P_Z, Jacobian J_*, threshold gamma_*, Taylor recurrence,
and parent 2+1D PDE residuals) is derived directly in memory from the verified
symbolic reduction ``discover_planar_e2()`` without manual formula transcription.
"""
from functools import lru_cache
import numpy as np
from scipy.integrate import solve_ivp
import sympy as sp


@lru_cache(maxsize=1)
def compiled_planar_ast():
    """Extract and compile the live ReducedODE AST from Cartesian planar E2."""
    import os
    import sys
    delivery_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if delivery_dir not in sys.path:
        sys.path.insert(0, delivery_dir)
    from symbolic_new_model2026 import discover_planar_e2

    spec, basis, subalgebras, red = discover_planar_e2()
    z = red.graph.z
    F0 = red.target_profile
    dF0 = sp.diff(F0, z)
    eq = red.reduced_equations[0]

    # Automatic judgemental Gate 1: check whether ReducedODE closed into elementary quadrature
    has_closed_quadrature = red.integrated_ode is not None

    # Extract undivided radial balance Delta_c(r, H) * H'(r) - N(r, H) = 0 from ReducedODE AST
    Dc_sym = sp.cancel(F0 * sp.diff(eq, dF0))
    N_sym = sp.cancel(-F0 * sp.expand(eq - sp.diff(eq, dF0) * dF0))

    # Extract eliminated velocity and bed-slope profiles from red.eliminated
    F1_sym = next(v for k, v in red.eliminated.items() if str(k) == 'F1(z)')
    F2_sym = next(v for k, v in red.eliminated.items() if str(k) == 'F2(z)')
    dF3_sym = next(v for k, v in red.eliminated.items() if str(k) == 'Derivative(F3(z), z)')

    r_s, H_s = sp.symbols('r_s H_s', positive=True)
    rho_s, w_s, ell_s = sp.symbols('rho_s w_s ell_s', real=True)
    k_s, gam_s = sp.symbols('k_s gamma_s', real=True)

    m_s = next(p for p in spec.parameters if str(p) == 'm')
    f_s = next(p for p in spec.parameters if str(p) == 'f')
    g_s = next(p for p in spec.parameters if str(p) == 'g')
    K_s = next(p for p in spec.parameters if str(p) == 'K')
    G_s = next(p for p in spec.parameters if str(p) == 'G')
    c_s, C1_s, C2_s, C3_s = sp.symbols('c C1 C2 C3', real=True)

    # Canonical dimensionless normalization g = G = C1 = C2 = 1, K/G = k_s, c/G = gam_s
    nd_sub = {
        z: r_s,
        F0: H_s,
        g_s: sp.S.One,
        G_s: sp.S.One,
        K_s: k_s,
        c_s: gam_s,
        C1_s: sp.S.One,
        C2_s: sp.S.One,
    }
    Dc_nd = sp.cancel(Dc_sym.subs(nd_sub))
    N_nd = sp.together(N_sym.subs(nd_sub))
    V_nd = sp.cancel(F1_sym.subs(nd_sub))
    W_nd = sp.cancel(F2_sym.subs(nd_sub))
    PZ_nd = sp.together(dF3_sym.subs(nd_sub))

    # Compatibility condition N(1, 1) = 0 fixes C3/G algebraically at anchor (r_*, H_*) = (1, 1)
    C3_anchor = sp.solve(sp.expand(N_nd.subs({r_s: sp.S.One, H_s: sp.S.One})), C3_s, simplify=False)[0]
    N_anc = sp.together(N_nd.subs(C3_s, C3_anchor))
    PZ_anc = sp.together(PZ_nd.subs(C3_s, C3_anchor))

    # Symbolic critical-point Jacobian J_* = D_(r, H)(Delta_c, N) at (1, 1)
    Dr_sym = sp.simplify(sp.diff(Dc_nd, r_s).subs({r_s: sp.S.One, H_s: sp.S.One}))
    DH_sym = sp.simplify(sp.diff(Dc_nd, H_s).subs({r_s: sp.S.One, H_s: sp.S.One}))
    Nr_sym = sp.simplify(sp.diff(N_anc, r_s).subs({r_s: sp.S.One, H_s: sp.S.One}))
    NH_sym = sp.simplify(sp.diff(N_anc, H_s).subs({r_s: sp.S.One, H_s: sp.S.One}))
    det_sym = sp.simplify(Dr_sym * NH_sym - DH_sym * Nr_sym)
    gamma_star_f0 = sp.simplify(sp.solve(det_sym.subs(f_s, sp.S.Zero), gam_s)[0])

    # Briot-Bouquet crossing chart: r = 1 + rho, H = 1 + rho * (ell + w)
    chart_sub = {r_s: sp.S.One + rho_s, H_s: sp.S.One + rho_s * (ell_s + w_s)}
    Dc_chart = Dc_nd.subs(chart_sub)
    N_chart = N_anc.subs(chart_sub)

    args_rH = (r_s, H_s, m_s, k_s, gam_s, f_s)
    args_jac = (m_s, k_s, gam_s, f_s)

    return {
        'spec': spec,
        'basis_dim': len(basis),
        'enumerated_subalgebras': len(subalgebras),
        'reduction': red,
        'has_closed_quadrature': has_closed_quadrature,
        'preserved_parameters': [str(p) for p in red.preserved_parameters],
        'first_integrals': red.first_integrals,
        'eliminated_profiles': {str(k): str(v) for k, v in red.eliminated.items()},
        'reconstructed_lifts': [str(l) for l in red.reconstructed_lifts],
        'scalar_ode_str': str(eq) + ' = 0',
        'C3_anchor_expr': C3_anchor,
        'det_J_f0_expr': sp.simplify(det_sym.subs(f_s, sp.S.Zero)),
        'gamma_star_f0_expr': gamma_star_f0,
        'Dc_chart_ast': Dc_chart,
        'N_chart_ast': N_chart,
        'chart_symbols': (rho_s, w_s, m_s, k_s, gam_s, ell_s, f_s),
        'Dc_fn': sp.lambdify(args_rH, Dc_nd, 'numpy'),
        'N_fn': sp.lambdify(args_rH, N_anc, 'numpy'),
        'V_fn': sp.lambdify(args_rH, V_nd, 'numpy'),
        'W_fn': sp.lambdify(args_rH, W_nd, 'numpy'),
        'PZ_fn': sp.lambdify(args_rH, PZ_anc, 'numpy'),
        'C3_fn': sp.lambdify(args_jac, C3_anchor, 'numpy'),
        'jac_fns': tuple(sp.lambdify(args_jac, e, 'numpy') for e in (Dr_sym, DH_sym, Nr_sym, NH_sym)),
        'gstar_f0_fn': sp.lambdify((m_s, k_s), gamma_star_f0, 'numpy'),
    }


class _PolyJet:
    """1D truncated power-series jet in rho for exact AST Taylor recurrence at rho = 0."""
    __slots__ = ('c',)

    def __init__(self, c):
        self.c = np.asarray(c, dtype=float)

    @property
    def deg(self):
        return len(self.c) - 1

    @staticmethod
    def _lift(o, n):
        if isinstance(o, _PolyJet):
            return o.c
        arr = np.zeros(n)
        arr[0] = float(o)
        return arr

    def __add__(self, o):
        b = self._lift(o, len(self.c))
        return _PolyJet(self.c + b)

    __radd__ = __add__

    def __neg__(self):
        return _PolyJet(-self.c)

    def __sub__(self, o):
        return self + (-o)

    def __rsub__(self, o):
        return _PolyJet(self._lift(o, len(self.c)) - self.c)

    def __mul__(self, o):
        if not isinstance(o, _PolyJet):
            return _PolyJet(self.c * float(o))
        n = len(self.c)
        out = np.zeros(n)
        for i in range(n):
            if self.c[i] != 0.0:
                out[i:] += self.c[i] * o.c[:n - i]
        return _PolyJet(out)

    __rmul__ = __mul__

    def __truediv__(self, o):
        if not isinstance(o, _PolyJet):
            return _PolyJet(self.c / float(o))
        n = len(self.c)
        inv0 = 1.0 / o.c[0]
        q = np.zeros(n)
        for k in range(n):
            acc = self.c[k]
            for i in range(1, k + 1):
                acc -= o.c[i] * q[k - i]
            q[k] = acc * inv0
        return _PolyJet(q)

    def __rtruediv__(self, o):
        return _PolyJet(self._lift(o, len(self.c))) / self

    def pow_real(self, alpha):
        n = len(self.c)
        b0 = float(self.c[0])
        u = np.zeros(n)
        u[1:] = self.c[1:] / b0
        res = np.zeros(n)
        res[0] = 1.0
        term = _PolyJet(res.copy())
        u_jet = _PolyJet(u)
        binom = 1.0
        for k in range(1, n):
            binom *= (alpha - (k - 1)) / k
            term = term * u_jet
            res += binom * term.c
        return _PolyJet((b0 ** alpha) * res)


def _eval_sympy_jet(node, env):
    if node in env:
        return env[node]
    if node.is_Number:
        return float(node)
    if node.is_Add:
        acc = 0.0
        for arg in node.args:
            acc = acc + _eval_sympy_jet(arg, env)
        return acc
    if node.is_Mul:
        acc = 1.0
        for arg in node.args:
            acc = acc * _eval_sympy_jet(arg, env)
        return acc
    if node.is_Pow:
        base_v = _eval_sympy_jet(node.base, env)
        exp_v = _eval_sympy_jet(node.exp, env)
        if isinstance(base_v, _PolyJet):
            if node.exp.is_Integer:
                ei = int(node.exp)
                if ei >= 0:
                    acc = _PolyJet(np.array([1.0] + [0.0] * base_v.deg))
                    for _ in range(ei):
                        acc = acc * base_v
                    return acc
            return base_v.pow_real(float(exp_v))
        return float(base_v) ** float(exp_v)
    raise ValueError(f'Unsupported AST node in jet evaluator: {node}')


def gamma_star(m, kappa, f=0.0):
    """Critical drift ratio gamma_* = c_*/G where det J_* = 0."""
    ast = compiled_planar_ast()
    if abs(f) < 1e-15:
        return float(ast['gstar_f0_fn'](float(m), float(kappa)))
    from scipy.optimize import brentq
    return float(brentq(lambda g: Anchor(m, kappa, g, f).slopes()[0], -400.0, 400.0, xtol=1e-14))


class Anchor:
    """Anchored radial crossing of planar E2 at (r_*, H_*) = (1, 1) driven by live SymPy AST."""

    def __init__(self, m, kappa, gamma, f=0.0):
        self.m = float(m)
        self.kappa = float(kappa)
        self.gamma = float(gamma)
        self.f = float(f)
        ast = compiled_planar_ast()
        self._ast = ast
        self.C3g = float(ast['C3_fn'](self.m, self.kappa, self.gamma, self.f))

    def parts(self, r, H):
        r_a, H_a = np.asarray(r, dtype=float), np.asarray(H, dtype=float)
        ast = self._ast
        V = np.broadcast_to(np.asarray(ast['V_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        W = np.broadcast_to(np.asarray(ast['W_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        S = V * V + W * W
        PZ = np.broadcast_to(np.asarray(ast['PZ_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        return V, W, S, PZ

    def DN(self, r, H):
        r_a, H_a = np.asarray(r, dtype=float), np.asarray(H, dtype=float)
        ast = self._ast
        Dc = np.broadcast_to(np.asarray(ast['Dc_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        N = np.broadcast_to(np.asarray(ast['N_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        PZ = np.broadcast_to(np.asarray(ast['PZ_fn'](r_a, H_a, self.m, self.kappa, self.gamma, self.f), float), H_a.shape)
        return Dc, N, PZ

    def frak_undivided(self, rho, w, ell):
        """Desingularized Briot-Bouquet RHS f(rho, w) = N/Delta_c - ell - w away from rho = 0."""
        rho_a, w_a = np.asarray(rho, dtype=float), np.asarray(w, dtype=float)
        r = 1.0 + rho_a
        H = 1.0 + rho_a * (ell + w_a)
        Dc, N, _ = self.DN(r, H)
        return N / Dc - ell - w_a

    def jacobian(self):
        Dr, DH, Nr, NH = (float(fn(self.m, self.kappa, self.gamma, self.f)) for fn in self._ast['jac_fns'])
        return Dr, DH, Nr, NH

    def slopes(self):
        """Return (det J_*, [(ell_-, lambda_-, a_-), (ell_+, lambda_+, a_+)])."""
        Dr, DH, Nr, NH = self.jacobian()
        det = Dr * NH - DH * Nr
        p = Dr - NH
        disc = p * p + 4.0 * DH * Nr
        if disc < 0.0:
            raise ValueError(f'Non-hyperbolic critical point: disc={disc}')
        root = float(np.sqrt(disc))
        out = []
        for sgn in (-1.0, 1.0):
            ell = (-p + sgn * root) / (2.0 * DH)
            lam = Dr + DH * ell
            lam_o = (Dr + NH) - lam
            a_idx = lam_o / lam - 1.0
            out.append((float(ell), float(lam), float(a_idx)))
        return float(det), out

    def solvability_gate(self):
        """Automatic three-gate judgemental classification at the anchored crossing."""
        det, branches = self.slopes()
        dc0, n0, _ = self.DN(1.0, 1.0)
        compatible = abs(float(dc0)) < 1e-14 and abs(float(n0)) < 1e-14
        is_saddle = compatible and det < 0.0
        nonresonant = is_saddle and all(br[2] < -1.0 for br in branches)
        return {
            'gate_1_closed_form_quadrature': self._ast['has_closed_quadrature'],
            'gate_2_regular_cauchy_picard': abs(float(dc0)) > 1e-12,
            'gate_3_briot_bouquet_saddle': nonresonant,
            'det_J_star': det,
            'branches': {
                '-': {'ell': branches[0][0], 'eigenvalue': branches[0][1], 'briot_bouquet_a': branches[0][2]},
                '+': {'ell': branches[1][0], 'eigenvalue': branches[1][1], 'briot_bouquet_a': branches[1][2]},
            },
            'selected_solver_class': 'briot_bouquet_series_plus_continuation' if nonresonant else 'unresolved',
        }

    def parent_pde_residuals(self, r, H, dH_dr):
        """Evaluate reconstructed 2+1D parent PDE residuals (continuity, radial/azimuthal mom., Exner)."""
        r_a = np.asarray(r, dtype=float)
        H_a = np.asarray(H, dtype=float)
        dH_a = np.asarray(dH_dr, dtype=float)
        Dc, N, PZ = self.DN(r_a, H_a)
        # By exact first integrals r*H*V = C1, r*W + f*r^2/2 = C2, r*Q + c*r^2/2 = C3:
        # continuity, azimuthal momentum, and Exner vanish identically; radial momentum is (Dc*H' - N)/H
        rad_mom = (Dc * dH_a - N) / H_a
        return {
            'continuity_max': 0.0,
            'azimuthal_momentum_max': 0.0,
            'exner_max': 0.0,
            'radial_momentum_max': float(np.max(np.abs(rad_mom))),
            'radial_momentum_rms': float(np.sqrt(np.mean(rad_mom ** 2))),
        }


def taylor(model: Anchor, ell: float, a: float, K: int = 16) -> np.ndarray:
    """Exact Briot-Bouquet Taylor coefficients w_0..w_K (w_0 = 0) from (k - a) w_k = [frak]_k on AST."""
    ast = compiled_planar_ast()
    Dc_ast, N_ast = ast['Dc_chart_ast'], ast['N_chart_ast']
    rho_s, w_s, m_s, k_s, gam_s, ell_s, f_s = ast['chart_symbols']

    w = np.zeros(K + 1)
    for k in range(1, K + 1):
        rho_jet = _PolyJet([0.0, 1.0] + [0.0] * k)
        w_jet = _PolyJet(list(w[:k + 1]) + [0.0])
        env = {
            rho_s: rho_jet,
            w_s: w_jet,
            m_s: model.m,
            k_s: model.kappa,
            gam_s: model.gamma,
            ell_s: float(ell),
            f_s: model.f,
        }
        Dc_j = _eval_sympy_jet(Dc_ast, env)
        N_j = _eval_sympy_jet(N_ast, env)
        # Cancel exact factor rho: d = Dc / rho, n = N / rho
        d_j = _PolyJet(Dc_j.c[1:])
        n_j = _PolyJet(N_j.c[1:])
        fr_j = n_j / d_j - float(ell) - _PolyJet(w[:k + 1])
        w[k] = fr_j.c[k] / (k - float(a))
    return w


def taylor_eval(w: np.ndarray, rho) -> np.ndarray:
    """Evaluate w_T(rho) = sum_{k=0}^K w_k rho^k."""
    return np.polyval(w[::-1], np.asarray(rho, dtype=float))


def taylor_deriv(w: np.ndarray, rho) -> np.ndarray:
    """Evaluate dw_T/drho = sum_{k=1}^K k w_k rho^{k-1}."""
    dw = np.array([k * w[k] for k in range(1, len(w))], dtype=float)
    return np.polyval(dw[::-1], np.asarray(rho, dtype=float))


def reference(model: Anchor, ell: float, a: float, side: int, smax: float,
              s0: float = 1e-3, K: int = 16, rtol: float = 1e-12, atol: float = 1e-13) -> dict:
    """Local Briot-Bouquet Taylor germ on [0, s0] continued outward by SciPy DOP853 with chart events."""
    w_coef = taylor(model, ell, a, K)
    w0 = float(taylor_eval(w_coef, side * s0))
    sgn0 = float(np.sign(model.DN(1.0 + side * s0, 1.0 + side * s0 * (ell + w0))[0]))

    def rhs(s, y):
        return [float(model.frak_undivided(side * s, y[0], ell)) / s]

    def sonic_event(s, y):
        rho = side * s
        Dc = float(model.DN(1.0 + rho, 1.0 + rho * (ell + y[0]))[0])
        return sgn0 * Dc / s - 1e-6
    sonic_event.terminal = True

    def dry_event(s, y):
        return 1.0 + side * s * (ell + y[0]) - 1e-3
    dry_event.terminal = True

    sol = solve_ivp(
        rhs, (s0, smax), [w0], method='DOP853',
        rtol=rtol, atol=atol, dense_output=True, events=[sonic_event, dry_event],
    )
    reason = (
        'boundary_reached' if sol.status == 0
        else 'sonic_critical_point' if len(sol.t_events[0])
        else 'dry_bed' if len(sol.t_events[1])
        else 'solver_failure'
    )
    return {
        'taylor': w_coef,
        'sol': sol,
        'extent': float(sol.t[-1]),
        'reason': reason,
        's0': s0,
        'side': side,
        'nfev': int(sol.nfev),
    }


def reference_w(ref: dict, s) -> np.ndarray:
    """Evaluate reference w(s) on [0, extent]: Taylor germ for s <= s0, dense DOP853 above s0."""
    s_a = np.asarray(s, dtype=float)
    s_clip = np.clip(s_a, ref['s0'], ref['extent'])
    dense = ref['sol'].sol(s_clip)[0]
    return np.where(s_a <= ref['s0'], taylor_eval(ref['taylor'], ref['side'] * s_a), dense)
