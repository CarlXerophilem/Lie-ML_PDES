# Task 5 brief — Reduction: invariants and the residual-zero reduced ODE

This is your requirements. Use the exact code, signatures, and test cases below verbatim.
Tasks 1-4 are complete (do NOT modify them). Work strictly TEST-FIRST.

## Global Constraints
- No new dependencies beyond `sympy 1.14`, `numpy 2.3`, `scipy 1.17`, `pytest`. Pure stdlib otherwise.
- Determinism: no randomness.
- Scope: scalar PDEs `(x,t,u)`, order `k<=3`, point symmetries.
- Not a git repo. Final step = tests green. Run from project root `D:\MATHs\math 4890 LieML`.

## Interfaces you CONSUME
- `symm/sym_engine/jet.py`: `PDE` with `.x, .t, .u, .order, .Delta, .jet` (dict `(a,b)->Symbol`).

## Interfaces you PRODUCE (later tasks rely on these EXACT names)
In a NEW file `symm/sym_engine/reduce.py`:
- `@dataclass Reduction` with fields `gen, z, U, ansatz, ode, residual`.
- `reduce_by(pde, gen) -> Reduction | None`. Handles two generator families:
  the TRANSLATION family (`tau, xi` constant, `phi=0`) → travelling wave `z = x - c t`, `u = U(z)`;
  and the SCALING family (`tau=a t, xi=b x, phi=e u`) → self-similar `u = t^(e/a) U(z)`, `z = x t^(-b/a)`.
  Returns `None` for any other generator. `residual` is `0` (sympy Integer) when the reduction is valid
  (the substituted PDE collapses to a function of `z` only).

## Files
- Create: `symm/sym_engine/reduce.py`
- Test: `symm/tests/test_reduce.py`

## Step 1 — write the failing test (`symm/tests/test_reduce.py`)

```python
# symm/tests/test_reduce.py
import sympy as sp
from symm.sym_engine.jet import PDE
from symm.sym_engine.reduce import reduce_by

def _burgers():
    nu = sp.Symbol('nu', positive=True)
    pde = PDE.scalar_1plus1(Delta=None, order=2, name="burgers", params={nu: 0.1})
    ux = pde.jet_sym(1, 0); ut = pde.jet_sym(0, 1); uxx = pde.jet_sym(2, 0)
    pde.Delta = ut + pde.u * ux - nu * uxx
    pde._init_onshell()
    return pde, nu

def test_travelling_wave_reduction_residual_zero():
    pde, nu = _burgers()
    c = sp.Symbol('c')
    gen = (sp.Integer(1), c, sp.Integer(0))   # d_t + c d_x
    red = reduce_by(pde, gen)
    assert red is not None
    assert sp.simplify(red.residual) == 0
    z = red.z
    U = red.U
    expected = nu * U(z).diff(z, 2) - (U(z) - c) * U(z).diff(z)
    assert sp.simplify(red.ode - expected) == 0 or sp.simplify(red.ode + expected) == 0

def test_steady_reduction_from_dt():
    pde, nu = _burgers()
    gen = (sp.Integer(1), sp.Integer(0), sp.Integer(0))   # d_t  -> c=0, z=x, u=U(x)
    red = reduce_by(pde, gen)
    assert red is not None
    assert sp.simplify(red.residual) == 0

def test_dx_alone_returns_none():
    pde, nu = _burgers()
    gen = (sp.Integer(0), sp.Integer(1), sp.Integer(0))   # d_x : tau=0, not a handled family
    assert reduce_by(pde, gen) is None
```

## Step 2 — run to verify it fails
`python -m pytest symm/tests/test_reduce.py -q` → FAIL (module missing).

## Step 3 — minimal implementation (`symm/sym_engine/reduce.py`)

```python
# symm/sym_engine/reduce.py
import sympy as sp
from dataclasses import dataclass


@dataclass
class Reduction:
    gen: tuple
    z: sp.Symbol
    U: sp.Function
    ansatz: sp.Expr
    ode: sp.Expr
    residual: sp.Expr


def _is_const(e, vars_):
    return all(sp.diff(e, v) == 0 for v in vars_)


def reduce_by(pde, gen):
    x, t, u = pde.x, pde.t, pde.u
    tau, xi, phi = map(sp.sympify, gen)
    z = sp.Symbol('z', real=True)
    U = sp.Function('U')

    # --- translation family: tau, xi constant, phi == 0  -> travelling/standing wave ---
    if _is_const(tau, (x, t, u)) and _is_const(xi, (x, t, u)) and phi == 0 and tau != 0:
        c = sp.simplify(xi / tau)               # wave speed; z = x - c t, u = U(z)
        subs = {u: U(z)}
        # d^a_x d^b_t U(x - c t) = (-c)^b * U^{(a+b)}(z)
        for (a, b), s in pde.jet.items():
            if 1 <= a + b <= pde.order:
                subs[s] = (-c)**b * sp.diff(U(z), z, a + b)
        E = sp.expand(pde.Delta.subs(subs))
        remaining = [v for v in (x, t) if E.has(v)]
        residual = sp.simplify(E) if remaining else sp.Integer(0)
        return Reduction(gen=gen, z=z, U=U, ansatz=U(z), ode=sp.simplify(E), residual=residual)

    # --- scaling family: tau = a t, xi = b x, phi = e u ---
    if tau != 0:
        a = sp.simplify(tau / t)
        if a != 0 and sp.simplify(tau - a * t) == 0:
            b = sp.simplify(xi / x) if xi != 0 else sp.Integer(0)
            e = sp.simplify(phi / u) if phi != 0 else sp.Integer(0)
            if sp.simplify(xi - b * x) == 0 and sp.simplify(phi - e * u) == 0:
                beta = sp.simplify(b / a)
                alpha = sp.simplify(e / a)
                u_of = t**alpha * U(x * t**(-beta))     # u = t^alpha U(z), z = x t^-beta
                subs = {u: u_of}
                for (aa, bb), s in pde.jet.items():
                    if 1 <= aa + bb <= pde.order:
                        d = u_of
                        for _ in range(aa):
                            d = sp.diff(d, x)
                        for _ in range(bb):
                            d = sp.diff(d, t)
                        subs[s] = d
                E = sp.expand(pde.Delta.subs(subs))
                # invert z = x t^-beta  (x = z t^beta) and factor the lowest power of t
                Ez = sp.powsimp(sp.expand(E.subs(x, z * t**beta)), force=True)
                Ez = sp.simplify(Ez)
                tpow = sp.simplify(sp.gcd(Ez, t))  # best-effort common t factor
                cand = sp.simplify(Ez / tpow) if tpow != 0 else Ez
                remaining = [v for v in (x, t) if cand.has(v)]
                residual = sp.Integer(0) if not remaining else sp.simplify(cand)
                return Reduction(gen=gen, z=z, U=U, ansatz=u_of, ode=cand, residual=residual)

    return None
```

## Step 4 — run to verify it passes
`python -m pytest symm/tests/test_reduce.py -q` → the three tests must PASS.

NOTES:
- The TRANSLATION branch is the critical path and must be exactly right (the test verifies residual 0
  and the Burgers reduced ODE up to overall sign). Get those two translation tests + the `None` test green.
- The SCALING branch is BEST-EFFORT (it is not exercised by this task's tests). If you find the scaling
  reduction does not cleanly give residual 0 for some PDE later, that is acceptable for v1 — it reports a
  nonzero residual honestly. Do NOT spend effort perfecting it here; do NOT change the three test
  assertions. If `sp.gcd(Ez, t)` misbehaves, you may replace the `tpow`/`cand` lines with `cand = Ez`
  (the residual will then just be reported honestly) — but the three tests above must still pass.

## Step 5 — final check
`python -m pytest symm/tests -q` — ALL tests (Tasks 1-5) green.

## Report contract
Write full report to `D:\MATHs\math 4890 LieML\.sdd\task-5-report.md`. Return ONLY: status, files
created, one-line test summary, concerns (note explicitly whether you touched the scaling branch).
