"""Task 1: symbolic checks for smooth (2+1) shallow water on a flat bed.

Requires SymPy. Assume h > 0. No boundary-value problem is asserted here.
The expansion control is regular for t >= 0 and a, H0 > 0.
"""
import sympy as sp

t = sp.symbols("t", nonnegative=True)
x, y = sp.symbols("x y", real=True)
g, H0, a = sp.symbols("g H0 a", positive=True)
h, u, v = [sp.Function(name)(t, x, y) for name in ("h", "u", "v")]
D = sp.diff

mass = D(h, t) + D(h*u, x) + D(h*v, y)
mx = D(u, t) + u*D(u, x) + v*D(u, y) + g*D(h, x)
my = D(v, t) + u*D(v, x) + v*D(v, y) + g*D(h, y)
cx = D(h*u, t) + D(h*u**2 + g*h**2/2, x) + D(h*u*v, y)
cy = D(h*v, t) + D(h*u*v, x) + D(h*v**2 + g*h**2/2, y)

assert sp.simplify(cx - h*mx - u*mass) == 0
assert sp.simplify(cy - h*my - v*mass) == 0
print("PASS: conservative/primitive identities (equivalent when h > 0)")

rho = 1 + a*t
controls = {
    "rest": {h: H0, u: 0, v: 0},
    "2D expansion": {h: H0/rho**2, u: a*x/rho, v: a*y/rho},
}
for name, solution in controls.items():
    residual = [sp.simplify(eq.subs(solution).doit()) for eq in (mass, cx, cy)]
    assert all(value == 0 for value in residual), (name, residual)
    print(f"PASS: {name}; conservative residuals = {residual}")
