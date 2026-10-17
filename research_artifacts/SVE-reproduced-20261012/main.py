"""Symbolic derivation and audit of Equations (24)-(31)
in Paliathanasis, Symmetry 2022, 14, 1679 (Eulerian 1D SVE model).
"""
import sympy as sp

t, x = sp.symbols('t x', real=True)
u, h, B = sp.symbols('u h B', real=True)
u_t, u_x, h_t, h_x, B_t, B_x = sp.symbols('u_t u_x h_t h_x B_t B_x', real=True)
g, zeta, m = sp.symbols('g zeta m', positive=True)

# 1. Eulerian SVE System (Equations 1-4, with zeta_bar := m * zeta * A_g)
eq1 = h_t + u * h_x + h * u_x
eq2 = (u * h_t + h * u_t) + (u**2 * h_x + 2 * h * u * u_x + g * h * h_x) + g * h * B_x
eq3 = B_t + zeta * u**(m - 1) * u_x

COORDS = (t, x, u, h, B)
JETS_T = {u: u_t, h: h_t, B: B_t}
JETS_X = {u: u_x, h: h_x, B: B_x}

def total_t(expr):
    return (sp.diff(expr, t)
            + sum(sp.diff(expr, f) * JETS_T[f] for f in (u, h, B)))

def total_x(expr):
    return (sp.diff(expr, x)
            + sum(sp.diff(expr, f) * JETS_X[f] for f in (u, h, B)))

def prolong_and_act(vec, exprs):
    """Apply first prolongation of vec = (xi_t, xi_x, eta_u, eta_h, eta_B)."""
    xi_t, xi_x, eta_u, eta_h, eta_B = vec
    etas = {u: eta_u, h: eta_h, B: eta_B}
    Dt_xi_t, Dx_xi_t = total_t(xi_t), total_x(xi_t)
    Dt_xi_x, Dx_xi_x = total_t(xi_x), total_x(xi_x)
    prol = {}
    for f in (u, h, B):
        prol[JETS_T[f]] = total_t(etas[f]) - JETS_T[f] * Dt_xi_t - JETS_X[f] * Dt_xi_x
        prol[JETS_X[f]] = total_x(etas[f]) - JETS_T[f] * Dx_xi_t - JETS_X[f] * Dx_xi_x
    subs_on_shell = {
        h_t: sp.solve(eq1, h_t)[0],
        u_t: sp.solve(eq2.subs(h_t, sp.solve(eq1, h_t)[0]), u_t)[0],
        B_t: sp.solve(eq3, B_t)[0],
    }
    residuals = []
    for eq in exprs:
        act_eq = (sum(v * sp.diff(eq, c) for v, c in zip(vec, COORDS))
                  + sum(prol[jet] * sp.diff(eq, jet) for jet in prol))
        residuals.append(sp.simplify(act_eq.subs(subs_on_shell)))
    return residuals

# ==============================================================================
# Equations (24) and (25): Proposition 1 Lie Point Symmetries
# ==============================================================================
X1 = (sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0))
X2 = (sp.Integer(0), sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0))
X3 = (t, x, sp.Integer(0), sp.Integer(0), sp.Integer(0))
X4 = (sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(0), sp.Integer(1))

# Printed Eq (25) vs Corrected Eq (25) (matching Section 4.10)
X5_printed = (t, sp.Integer(0), -2 * u, -h, -2 * B)
X5_correct = (t, sp.Integer(0), -u, -2 * h, -2 * B)

print("=== EQUATION (24): Generic Symmetries X1..X4 ===")
for name, gen in [('X1', X1), ('X2', X2), ('X3', X3), ('X4', X4)]:
    res = prolong_and_act(gen, (eq1, eq2, eq3))
    print(f"  {name} = {gen} -> on-shell residuals: {res}")

print("\n=== EQUATION (25): m = 3 Scaling Symmetry X5 ===")
eqs_m3 = (eq1, eq2, eq3.subs(m, 3))
print("  Printed X5 (t, 0, -2u, -h, -2B) residuals at m=3 :",
      prolong_and_act(X5_printed, eqs_m3))
print("  Corrected X5 (t, 0, -u, -2h, -2B) residuals at m=3:",
      prolong_and_act(X5_correct, eqs_m3))

# ==============================================================================
# Equations (26)-(29): Commutators, Adjoint Action, and Invariants
# ==============================================================================
BASIS = {'X1': X1, 'X2': X2, 'X3': X3, 'X4': X4, 'X5': X5_correct}
NAMES = ('X1', 'X2', 'X3', 'X4', 'X5')

def lie_bracket(V, W):
    return tuple(sp.simplify(sum(V[k] * sp.diff(W[i], COORDS[k])
                                 - W[k] * sp.diff(V[i], COORDS[k])
                                 for k in range(5))) for i in range(5))

def decompose(V):
    c = sp.symbols('c1:6')
    eqs = [sum(c[j] * BASIS[NAMES[j]][i] for j in range(5)) - V[i] for i in range(5)]
    polys = [coeff for e in eqs for coeff in sp.Poly(e, *COORDS).coeffs()]
    sol = sp.solve(polys, c, dict=True)[0]
    return {NAMES[j]: sol.get(c[j], sp.Integer(0)) for j in range(5)
            if sol.get(c[j], 0) != 0}

print("\n=== TABLE 1 & EQUATIONS (26)-(27): Commutators and Adjoint Table ===")
struct_const = {}
for i, A in enumerate(NAMES):
    for j, B_name in enumerate(NAMES):
        decomp = decompose(lie_bracket(BASIS[A], BASIS[B_name]))
        struct_const[(i, j)] = decomp
        if decomp:
            print(f"  [{A}, {B_name}] = {decomp}")

a_vars = sp.symbols('a1:6', real=True)
phi = sp.Function('phi')(*a_vars)
print("\n=== EQUATIONS (28)-(29): Adjoint Invariant System Delta_A(phi) = 0 ===")
for i, A in enumerate(NAMES):
    delta_A = sp.Integer(0)
    for j, B_name in enumerate(NAMES):
        for C_name, val in struct_const[(i, j)].items():
            k = NAMES.index(C_name)
            delta_A += val * a_vars[j] * sp.diff(phi, a_vars[k])
    print(f"  A = {A}: {sp.Eq(sp.simplify(delta_A), 0)}")

# ==============================================================================
# Equations (30)-(33): Invariant Surface Condition and X1 Reduction
# ==============================================================================
print("\n=== EQUATIONS (30)-(33): Reduction under X1 = d_t ===")
U_x = sp.Function('u')(x)
H_x = sp.Function('h')(x)
B_fn = sp.Function('B')(x)
red31 = sp.Eq(sp.diff(U_x * H_x, x), 0)
red32 = sp.Eq(sp.diff(H_x * U_x**2 + sp.Rational(1, 2) * g * H_x**2, x)
              + g * H_x * sp.diff(B_fn, x), 0)
red33 = sp.Eq(zeta * U_x**(m - 1) * sp.diff(U_x, x), 0)
print("  Eq (31):", red31)
print("  Eq (32):", red32)
print("  Eq (33):", red33)