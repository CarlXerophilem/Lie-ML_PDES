"""Finite jets and point prolongation; no generator ansatz is imposed."""
import sympy as sp

t, s, u = sp.symbols('t s u')
p, q = sp.symbols('p q', positive=True)
a, b, c = sp.symbols('a b c')
r, w, x, y = sp.symbols('r w x y')
JETS = {(0,0):u, (1,0):p, (0,1):q, (2,0):a, (1,1):b,
        (0,2):c, (3,0):r, (2,1):w, (1,2):x, (0,3):y}
g, kappa = sp.symbols('g kappa', positive=True)
m = sp.symbols('m', real=True)

def total(expr, axis):
    result = sp.diff(expr, (t,s)[axis])
    for ij, jet in JETS.items():
        nxt = (ij[0] + (axis == 0), ij[1] + (axis == 1))
        if nxt in JETS:
            result += JETS[nxt] * sp.diff(expr, jet)
    return sp.expand(result)

def prolongation(tau, xi, eta):
    coeff = {(0,0):eta}
    dtau = [total(tau,i) for i in (0,1)]
    dxi = [total(xi,i) for i in (0,1)]
    for n in range(1,4):
        for i in range(n,-1,-1):
            j=n-i
            axis=0 if i else 1
            prev=(i-1,j) if i else (i,j-1)
            coeff[(i,j)] = sp.expand(total(coeff[prev],axis)
                -JETS[(prev[0]+1,prev[1])]*dtau[axis]
                -JETS[(prev[0],prev[1]+1)]*dxi[axis])
    return coeff

def act(expr, tau, xi, eta):
    coeff=prolongation(tau,xi,eta)
    out=tau*sp.diff(expr,t)+xi*sp.diff(expr,s)
    out += sum(coeff[ij]*sp.diff(expr,jet) for ij,jet in JETS.items())
    return sp.expand(out)

def model_residual(exponent=m, physical=False):
    A=q*a-g*c/q**2
    T=g*exponent*kappa*total(p**(exponent-1)*b/q,1)
    E=total(A,0)-T
    if physical:
        E-=total(p*A/q,1)
    return sp.expand(E)
