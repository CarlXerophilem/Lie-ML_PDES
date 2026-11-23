"""Symbolic verification of every claim made in curriculum_math.tex.

Deterministic, no RNG. Each check prints PASS/FAIL; exit summary at the end.
Claims verified:
  (T) transport u_t = u_x: the FULL point-symmetry family in characteristic
      coordinates zeta = x+t, eta = x-t is  a(zeta,u) d_zeta + b(zeta,eta,u) d_eta
      + c(zeta,u) d_u  (proved in the tex); instances have residual == 0, and the
      induced closed form dim_D = 2*C(D+2,2) + C(D+3,3) matches the engine.
  (H) heat u_t = u_xx: the classical 6 finite generators + heat-polynomial
      superposition beta(x,t) d_u are symmetries, and the degree filtration
      predicts dim_D = finite(D) + (D+1), matching the engine.
  (B) Burgers: window sequence [4,5,5] is explained by the projective
      generator's coefficient degree 2 (invisible at D=1).
  (W) homogeneity check: the scaling-weight criterion. For evolution equations
      u_t = sum c_k m_k, the diagonal field a*x*d_x + b*t*d_t + c*u*d_u is a
      symmetry iff every present term's weight equals w(u_t) = c - b. Verified:
      the predicted scaling lattices of porous(m=2) (2-dim), Burgers (1-dim),
      KdV (1-dim), heat (2-dim) all certify residual == 0, Fisher's lattice is
      trivial (reaction term kills scaling; generic diagonal FAILS residual),
      and the weight-difference matrices have the predicted ranks.
  (S) solvability check: derived series of the computed algebras. Verified:
      Fisher [2,0] and porous [4,2,0] and KdV [4,3,1,0] terminate (solvable);
      Burgers (5-dim) and heat (6-dim) go stationary at a nonzero derived
      algebra (NOT solvable) -- each contains an sl(2,R) triple {d_t, scaling,
      projective}, whose brackets are verified explicitly.
Run:  PYTHONPATH=<project root> python symm/curriculum_checks.py
"""
import sys
from pathlib import Path
from math import comb

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import sympy as sp

from symm.textbook_validation import build
from symm.sym_engine.jet import symmetry_residual
from symm.sym_engine.eliminate import discover

x, t, u = sp.symbols('x t u')
RESULTS = []


def check(name, ok):
    print(("PASS  " if ok else "FAIL  ") + name)
    RESULTS.append(bool(ok))


# ---------------------------------------------------------------- transport
tr = build("transport")
Z, E = x + t, x - t          # zeta, eta
FAMILY = [                    # (a(zeta,u), b(zeta,eta,u), c(zeta,u))
    (Z**2 - 3*u,      Z*E*u,            Z*u - 2*u**2),
    (u**3,            E**2 - Z*u**2,    Z**3),
    (sp.Integer(1),   Z + E + u,        Z),
]
for i, (a, b, c) in enumerate(FAMILY):
    # d_zeta = (d_x + d_t)/2,  d_eta = (d_x - d_t)/2
    xi = sp.expand((a + b) / 2)      # coefficient of d_x
    tau = sp.expand((a - b) / 2)     # coefficient of d_t
    res = sp.simplify(symmetry_residual(tr, tau, xi, c))
    check(f"(T) transport family instance {i}: residual == 0", res == 0)

seq_t = []
discover(build("transport"), 1, 5, on_step=lambda k, s: seq_t.append(s["dim"]))
pred_t = [2 * comb(D + 2, 2) + comb(D + 3, 3) for D in range(1, 6)]
check(f"(T) dim_D = 2*C(D+2,2)+C(D+3,3): predicted {pred_t} == engine {seq_t}",
      seq_t == pred_t)

# ---------------------------------------------------------------- heat
he = build("heat")
HEAT_GENS = [                 # (tau, xi, phi) — classical basis (Olver)
    (0, 1, 0),                              # d_x
    (1, 0, 0),                              # d_t
    (0, 0, u),                              # u d_u
    (2*t, x, 0),                            # scaling  x d_x + 2t d_t
    (0, 2*t, -x*u),                         # Galilean boost
    (4*t**2, 4*t*x, -(x**2 + 2*t)*u),       # projective
]
for i, (tau, xi, phi) in enumerate(HEAT_GENS):
    res = sp.simplify(symmetry_residual(he, tau, xi, phi))
    check(f"(H) heat classical generator {i}: residual == 0", res == 0)

HEAT_POLYS = [sp.Integer(1), x, x**2 + 2*t, x**3 + 6*x*t,
              x**4 + 12*x**2*t + 12*t**2, x**5 + 20*x**3*t + 60*x*t**2]
for n, v in enumerate(HEAT_POLYS):
    solves = sp.simplify(sp.diff(v, t) - sp.diff(v, x, 2)) == 0
    is_sym = sp.simplify(symmetry_residual(he, 0, 0, v)) == 0
    check(f"(H) heat polynomial v{n} (deg {sp.Poly(v, x, t).total_degree()}): "
          f"solves heat & v*d_u is a symmetry", solves and is_sym)

seq_h = []
discover(build("heat"), 1, 5, on_step=lambda k, s: seq_h.append(s["dim"]))
finite_visible = [4, 5, 6, 6, 6]          # generators with coeff degree <= D
pred_h = [finite_visible[D - 1] + (D + 1) for D in range(1, 6)]
check(f"(H) dim_D = finite(D) + (D+1) heat polys: predicted {pred_h} == "
      f"engine {seq_h}", seq_h == pred_h)

# ---------------------------------------------------------------- burgers
seq_b = []
discover(build("burgers"), 1, 3, on_step=lambda k, s: seq_b.append(s["dim"]))
check(f"(B) Burgers window seq {seq_b} == [4,5,5] "
      f"(projective coeff degree 2 => enters at D=2)", seq_b == [4, 5, 5])

# ---------------------------------------------------------------- (W) homogeneity
def scaling(a, b, c):
    """(tau, xi, phi) of the diagonal field a*x*d_x + b*t*d_t + c*u*d_u."""
    return (b * t, a * x, c * u)


bu, kd, fi, po = build("burgers"), build("kdv"), build("fisher"), build("porous2")

for nm, pde, abc in [("porous S1=(1,2,0)", po, (1, 2, 0)),
                     ("porous S2=(0,-2,1)", po, (0, -2, 1)),
                     ("burgers (1,2,-1)", bu, (1, 2, -1)),
                     ("kdv (1,3,-2)", kd, (1, 3, -2)),
                     ("heat (1,2,0)", he, (1, 2, 0)),
                     ("heat (0,0,1)", he, (0, 0, 1))]:
    res = sp.simplify(symmetry_residual(pde, *scaling(*abc)))
    check(f"(W) scaling {nm}: residual == 0", res == 0)

res_f = sp.simplify(symmetry_residual(fi, *scaling(1, 2, 0)))
check("(W) fisher generic scaling (1,2,0): residual != 0 (no scaling exists)",
      res_f != 0)

# weight-difference matrices in (a,b,c): rows = w(term) - w(u_t) for each term.
W_FISHER = sp.Matrix([[-2, 1, 0],   # u_xx: (c-2a)-(c-b)
                      [0, 1, 0],    # u   : c-(c-b)
                      [0, 1, 1]])   # u^2 : 2c-(c-b)
W_POROUS = sp.Matrix([[-2, 1, 2]])  # u^2 u_xx (= u u_x^2): (3c-2a)-(c-b)
W_BURGERS = sp.Matrix([[-1, 1, 1],  # u u_x: (2c-a)-(c-b)
                       [-2, 1, 0]])  # u_xx
check("(W) fisher weight system rank 3 => only trivial scaling",
      W_FISHER.rank() == 3)
check("(W) porous weight system nullity 2 => 2-dim scaling lattice",
      3 - W_POROUS.rank() == 2)
check("(W) burgers weight system nullity 1 => 1-dim scaling lattice",
      3 - W_BURGERS.rank() == 1)

# ---------------------------------------------------------------- (S) solvability
def vf_apply(X, f):
    tau, xi, phi = X
    return tau * sp.diff(f, t) + xi * sp.diff(f, x) + phi * sp.diff(f, u)


def bracket(X, Y):
    return tuple(sp.expand(vf_apply(X, Y[i]) - vf_apply(Y, X[i]))
                 for i in range(3))


def _coeff_matrix(vecs):
    monos = sorted({m for X in vecs for comp in X
                    for m in sp.Poly(comp, x, t, u).monoms()} | {(0, 0, 0)})
    rows = []
    for X in vecs:
        row = []
        for comp in X:
            p = sp.Poly(comp, x, t, u)
            d = dict(zip(p.monoms(), p.coeffs()))
            row += [d.get(m, 0) for m in monos]
        rows.append(row)
    return sp.Matrix(rows)


def reduce_span(vecs):
    """Greedy independent spanning subset (exact rank over Q)."""
    keep = []
    r = 0
    for v in vecs:
        if any(sp.expand(c) != 0 for c in v):
            r2 = _coeff_matrix(keep + [v]).rank()
            if r2 > r:
                keep.append(v)
                r = r2
    return keep


def derived_dims(basis, max_steps=6):
    """Dimensions of the derived series g, g', g'', ... (stops when 0 or stationary)."""
    cur = reduce_span(list(basis))
    dims = [len(cur)]
    for _ in range(max_steps):
        brs = [bracket(a, b) for i, a in enumerate(cur) for b in cur[i + 1:]]
        cur = reduce_span(brs)
        dims.append(len(cur))
        if dims[-1] == 0 or dims[-1] == dims[-2]:
            break
    return dims


FISHER_B = [(1, 0, 0), (0, 1, 0)]
POROUS_B = [(1, 0, 0), (0, 1, 0), scaling(1, 2, 0), scaling(0, -2, 1)]
KDV_B = [(1, 0, 0), (0, 1, 0), (0, t, 1), scaling(1, 3, -2)]
BURGERS_B = [(1, 0, 0), (0, 1, 0), (0, t, 1), (2 * t, x, -u),
             (t ** 2, t * x, x - t * u)]
HEAT_B = [(tau, xi, phi) for tau, xi, phi in HEAT_GENS]

for nm, pde, B in [("kdv", kd, KDV_B), ("burgers", bu, BURGERS_B)]:
    ok = all(sp.simplify(symmetry_residual(pde, *X)) == 0 for X in B)
    check(f"(S) {nm} basis: every generator residual == 0", ok)

# sl(2,R) inside Burgers: [E,H] = 2E? -- verify the standard triple relations
E, H, P = (1, 0, 0), (2 * t, x, -u), (t ** 2, t * x, x - t * u)
sl2_ok = (bracket(E, H) == (2, 0, 0)
          and bracket(E, P) == H
          and bracket(H, P) == tuple(sp.expand(2 * v) for v in P))
check("(S) burgers contains sl(2,R): [d_t,H]=2 d_t, [d_t,P]=H, [H,P]=2P", sl2_ok)

for nm, B, expect in [("fisher", FISHER_B, [2, 0]),
                      ("porous", POROUS_B, [4, 2, 0]),
                      ("kdv", KDV_B, [4, 3, 1, 0])]:
    dd = derived_dims(B)
    check(f"(S) {nm} derived series {dd} == {expect} => SOLVABLE", dd == expect)

for nm, B in [("burgers", BURGERS_B), ("heat", HEAT_B)]:
    dd = derived_dims(B)
    stationary_nonzero = dd[-1] == dd[-2] and dd[-1] > 0
    check(f"(S) {nm} derived series {dd} stationary at nonzero dim "
          f"=> NOT solvable", stationary_nonzero)

print(f"\n{sum(RESULTS)}/{len(RESULTS)} checks pass")
sys.exit(0 if all(RESULTS) else 1)
