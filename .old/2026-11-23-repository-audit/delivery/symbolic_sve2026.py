"""Final SymPy expressions for P and M on their common positive chart."""
import json

from reproduce_sve2026 import (act, bracket, derive_reduction, generators, master,
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
    return boost_defect


def regular_common_chart():
    """Direct pullbacks at t=1, s=z using phi=t*F(s/t); m is symbolic."""
    T = sp.Symbol("T", positive=True)
    profile = sp.Function("profile")
    graph = T*profile(s/T)
    jets = {v:sp.diff(graph,T,i,s,j).subs({T:1,s:z}, simultaneous=True).doit()
            for (i,j),v in JETS.items()}
    jets = {key: val.xreplace({sp.diff(profile(z),z,n):v
                              for n,v in enumerate((F,P,C,H))})
            for key,val in jets.items()}
    rp = sp.factor(master().xreplace(jets))
    rm = sp.factor(compatible().xreplace(jets))
    vel = sp.Symbol("velocity", positive=True)
    difference = rp-derive_reduction("3.4",exponent=m)["residual"]
    assert sp.factor(sp.expand(difference.subs(F,vel+z*P))) == 0
    correction = sp.factor(rm-rp)
    expected = (F-z*P)*(g/P**3-z**2)*C
    assert sp.factor(correction-(expected.diff(z)+P*expected.diff(F)
                                  +C*expected.diff(P)+H*expected.diff(C))) == 0
    spot = {z:1,F:2,P:1,C:sp.Rational(1,10),g:1,kappa:sp.Rational(1,30)}
    checks = {}
    for exponent in (1,2,3):
        lp, lm = [sp.simplify(e.diff(H).subs(spot).subs(m,exponent)) for e in (rp,rm)]
        assert lp != 0 and lm != 0
        exact_h = sp.simplify(-rp.subs(H,0).subs(spot).subs(m,exponent)/lp)
        assert sp.simplify(rp.subs(spot).subs({m:exponent,H:exact_h})) == 0
        defect = sp.simplify(rm.subs(spot).subs({m:exponent,H:exact_h}))
        assert defect != 0
        checks[str(exponent)] = {"P_leading":str(lp),"M_leading":str(lm),
                                 "M_on_P_jet":str(defect)}
    return {"P":str(rp), "M":str(rm), "M_minus_P":str(correction), "checks":checks}


def singular_common_chart_certificate():
    """Differentiate the implicit critical equations before imposing L=0."""
    F0, pp, zz, bb = sp.symbols("F p z beta",positive=True)
    V = F0-zz*pp
    p_equation = g-zz**2*pp**3+g*bb*pp*V**(m-1)
    m_equation = F0*(g-zz**2*pp**3)+g*bb*zz*pp**2*V**(m-1)
    derivatives = {}
    for model, E, value, expected in (
        ("P",p_equation,(g+g*bb*pp*V**(m-1))/pp**3,
         -3*g/pp-2*g*bb*V**(m-1)-g*bb*(m-1)*zz*pp*V**(m-2)),
        ("M",m_equation,(g+g*bb*zz*pp**2*V**(m-1)/F0)/pp**3,
         -3*F0*g/pp-g*bb*zz*pp*V**(m-1)-g*bb*(m-1)*zz**2*pp**2*V**(m-2))
    ):
        # Only replace the cubic-term factor, keeping z in V and transport.
        if model == "P":
            remainder = E.diff(pp)+3*zz**2*pp**2
            restricted = remainder-3*pp**2*value
        else:
            remainder = E.diff(pp)+3*F0*zz**2*pp**2
            restricted = remainder-3*F0*pp**2*value
        difference = (restricted-expected).subs(F0,sp.Symbol("V",positive=True)+zz*pp)
        assert sp.factor(sp.expand(difference)) == 0
        derivatives[model] = str(expected)
    return {"scope":"z,p,V,g,beta>0 and m>=1",
            "p_derivatives_at_L_zero":derivatives,
            "analytic_germs":"If L=0 at the centre, I_0 must vanish. Affine F and the analytic first-order root branch L=0 exhaust the local analytic germs through that jet."}


def run():
    assert _determining_split()["passed"]
    defect = m_symbol_certificate()
    basis = generators()
    def select(names):
        return {k:list(map(str,basis[k])) for k in names.split()}
    return {
        "scope": "Unrestricted smooth point symmetries for real m>=1 on p=phi_t>0, q=phi_s>0; g,kappa>0",
        "coordinates": ["t","s","phi"],
        "P_m1": select("X1 X2 X3 X4 X6"),
        "M_m1_and_both_generic": select("X1 X2 X3 X4"),
        "both_m3": select("X1 X2 X3 X4 X5"),
        "M_m1_boost_defect": str(defect),
        "connected_optimal_lines": orbit_invariants(),
        "common_scaling": regular_common_chart(),
        "singular_common_scaling":singular_common_chart_certificate()
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
