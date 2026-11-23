"""Separate certificates for the scalar source and material equations."""
import json

from reproduce_sve2026 import (act, generators, master,
                               orbit_invariants, prolongation, total, u, t, s,
                               p, q, a, b, c, r, w, x, y, g, kappa, m, JETS, z, F, P, C, H,
                               _determining_split, sp)


def compatible(exponent=m):
    return sp.expand(master(exponent) - total(p*(q*a-g*c/q**2)/q, 1))


def m_symbol_certificate():
    """Use free third jets on the slice with all second jets zero."""
    tau, xi, eta = (sp.Function(name)(t,s,u) for name in ("tau", "xi", "eta"))
    residual = compatible()
    zero2 = dict.fromkeys((a,b,c), sp.S.Zero)
    principal = residual.xreplace(zero2)
    graph = {r: -principal.xreplace({r:sp.S.Zero})/q}
    pro = prolongation(tau,xi,eta)
    variation = sum(residual.diff(jet).xreplace(zero2) *
                    pro[ij].xreplace(zero2)
                    for ij,jet in JETS.items()).xreplace(graph)
    dw = sp.expand(q**4*variation.diff(w))
    by_q = sp.Poly(dw, q)
    tx, sx, ex = [v.diff(t) for v in (tau,xi,eta)]
    tu, su = tau.diff(u), xi.diff(u)
    ts, es = tau.diff(s), eta.diff(s)
    k = g*kappa*m*p**(m-1)
    expected = (-2*(sx+p*su)*q**5 + (2*k*tu-ex)*q**4
                +(p*es+2*k*ts+2*g*tu)*q**3+2*g*ts*q**2)
    assert sp.simplify(dw-expected) == 0
    assert by_q.coeff_monomial(q**2) == 2*g*ts
    # The q^5 and q^2 terms vanish for all p,q, then q^3 forces tau_u=eta_s=0.
    # The remaining q^4 term forces eta_t=0.
    constraints = dict.fromkeys((sx,su,ts,tu,es,ex), sp.S.Zero)
    dx = sp.expand(q**4*variation.diff(x)).xreplace(constraints)
    weight = g*(3*eta.diff(u)-xi.diff(s)-2*tx)*q**2
    weight += k*(3-m)*(eta.diff(u)-tx)*q**3
    assert sp.simplify(dx-weight) == 0
    # Principal constraints imply affine generators. Test the full residual.
    for name in ("X1","X2","X3","X4","X5"):
        e = residual.subs(m,3) if name == "X5" else residual
        lam = {"X4":-2,"X5":-1}.get(name,0)
        assert sp.simplify(act(e,*generators()[name])-lam*e) == 0
    boost_defect = sp.simplify(act(residual.subs(m,1),*generators()["X6"]))
    assert boost_defect == -total((q*a-g*c/q**2)/q,1)


def material_scaling():
    """Verify the undivided first integral from the original material jets."""
    T = sp.Symbol("T", positive=True)
    profile = sp.Function("profile")
    graph = T*profile(s/T)
    substitutions = {sp.diff(profile(z), z, n): value
                     for n, value in enumerate((F, P, C, H))}
    jets = {v: sp.diff(graph,T,i,s,j).subs({T:1,s:z}, simultaneous=True).doit()
                   .xreplace(substitutions) for (i,j),v in JETS.items()}
    velocity = F-z*P
    leading = F*(g/P**3-z*z)+g*kappa*m*z*velocity**(m-1)/P
    flux = leading*C
    expected = flux.diff(z)+P*flux.diff(F)+C*flux.diff(P)+H*flux.diff(C)
    diff = (compatible().xreplace(jets)-expected)
    v = sp.Symbol("velocity", positive=True)
    assert sp.factor(sp.expand(diff.subs(F,v+z*P))) == 0
    return {"leading":str(leading), "first_integral":str(flux)}


def run():
    assert _determining_split()["passed"]
    m_symbol_certificate()
    basis = generators()
    def select(names):
        return {k:list(map(str,basis[k])) for k in names.split()}
    return {
        "scope": "Unrestricted smooth point symmetries for real m>=1 on p=phi_t>0, q=phi_s>0; g,kappa>0",
        "coordinates": ["t","s","phi"],
        "P_m1": select("X1 X2 X3 X4 X6"),
        "M_m1_and_both_generic": select("X1 X2 X3 X4"),
        "both_m3": select("X1 X2 X3 X4 X5"),
        "connected_optimal_lines": orbit_invariants(),
        "material_scaling": material_scaling()
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
