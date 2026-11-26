"""Exact SymPy checks for the planar model E2, its potential formulation and its radial families.

Every check is an identity in the stated symbols; the script exits nonzero if any fails.
"""
import json
import sys
import time

import sympy as sp

t, x, y = sp.symbols('t x y', real=True)
r = sp.Symbol('r', positive=True)
g, f, K, G, m = sp.symbols('g f K G m', positive=True)
c, C1, C2, C3 = sp.symbols('c C1 C2 C3', real=True)
records = {}


def check(name, expr, note=''):
    value = sp.simplify(expr)
    ok = value.is_zero_matrix if isinstance(value, sp.MatrixBase) else value == 0
    records[name] = {'zero': bool(ok), 'note': note} if ok else {'zero': False, 'note': note, 'residue': str(value)}
    return ok


def grad(F):
    return sp.Matrix([sp.diff(F, x), sp.diff(F, y)])


def div(Vec):
    return sp.diff(Vec[0], x) + sp.diff(Vec[1], y)


def J(Vec):
    return sp.Matrix([-Vec[1], Vec[0]])


def eulerian(h, w, B):
    """Residuals of E2: mass, two momentum components, Exner."""
    speed2 = w[0]**2 + w[1]**2
    Q = speed2**((m - 1)/2)*(K*w - G*grad(B))
    mom = sp.diff(w, t) + sp.Matrix([w.dot(grad(w[0])), w.dot(grad(w[1]))]) + g*grad(h + B) + f*J(w)
    return [sp.diff(h, t) + div(h*w), mom[0], mom[1], sp.diff(B, t) + div(Q)]


def potential_formulation():
    psi, h = sp.Function('psi')(t, x, y), sp.Function('h')(t, x, y)
    rr = sp.sqrt(x**2 + y**2)
    w = grad(psi) + (C2/rr - f*rr/2)*sp.Matrix([-y/rr, x/rr])
    curl = sp.diff(w[1], x) - sp.diff(w[0], y)
    check('potential: curl w = -f', curl + f, 'zero absolute vorticity of the lifted velocity')
    Xi = sp.diff(psi, t) + (w[0]**2 + w[1]**2)/2 + g*h
    res = eulerian(h, w, -Xi/g)
    check('potential: momentum x', res[1], 'Bernoulli lift cancels advection and Coriolis')
    check('potential: momentum y', res[2])
    speed2 = w[0]**2 + w[1]**2
    exner_potential = sp.diff(Xi, t) - div(speed2**((m - 1)/2)*(g*K*w + G*grad(Xi)))
    check('potential: Exner equivalence', res[3] + exner_potential/g, 'B=-Xi/g turns Exner into the second potential equation')
    u, v = sp.Function('u')(t, x, y), sp.Function('v')(t, x, y)
    ww = sp.Matrix([u, v])
    adv = sp.Matrix([ww.dot(grad(u)), ww.dot(grad(v))])
    vort = sp.diff(v, x) - sp.diff(u, y)
    check('vector identity (w.grad)w = grad|w|^2/2 + curl(w) J w', adv - grad((u**2 + v**2)/2) - vort*J(ww))


def admitted_symmetries():
    """Linearized residual along the characteristic of R and T_c, for symbolic m,K,G,f,g,c."""
    h, u, v, B = [sp.Function(n)(t, x, y) for n in 'huvB']
    eps = sp.Symbol('epsilon')
    base = eulerian(h, sp.Matrix([u, v]), B)

    def linearized(Qh, Qu, Qv, QB):
        moved = eulerian(h + eps*Qh, sp.Matrix([u + eps*Qu, v + eps*Qv]), B + eps*QB)
        return [sp.diff(e, eps).subs(eps, 0) for e in moved]

    Dth = lambda F: -y*sp.diff(F, x) + x*sp.diff(F, y)
    lin = linearized(-Dth(h), -v - Dth(u), u - Dth(v), -Dth(B))
    expected = [-Dth(base[0]), -Dth(base[1]) - base[2], -Dth(base[2]) + base[1], -Dth(base[3])]
    ok = all(check(f'rotation R: residual {i}', sp.expand(lin[i] - expected[i])) for i in range(4))
    Dt = lambda F: sp.diff(F, t)
    lin = linearized(-Dt(h), -Dt(u), -Dt(v), c - Dt(B))
    ok &= all(check(f'drift T_c: residual {i}', sp.expand(lin[i] + Dt(base[i]))) for i in range(4))
    records['R and T_c admitted for every (m,K,G,f,g,c)'] = {'zero': bool(ok)}


def radial(V, W, H, Z, name):
    """Cartesian residuals of an invariant graph evaluated on the section y=0, x=r>0."""
    rr = sp.sqrt(x**2 + y**2)
    er, et = sp.Matrix([x/rr, y/rr]), sp.Matrix([-y/rr, x/rr])
    sub = lambda F: F.subs(r, rr)
    w = sub(V)*er + sub(W)*et
    res = eulerian(sub(H), w, sub(Z) + c*t)
    return [sp.simplify(e.subs(y, 0).subs(x, r)) for e in res]


def radial_reduction():
    H, Z = sp.Function('H')(r), sp.Function('Z')(r)
    V, W = C1/(r*H), C2/r - f*r/2
    mass, mr, mt, ex = radial(V, W, H, Z, 'saddle')
    check('radial: mass flux rHV=C1', mass)
    check('radial: azimuthal integral rW+fr^2/2=C2', mt)
    S = V**2 + W**2
    a = (m - 1)/2
    Q = C3/r - c*r/2
    PZ = (K*V - Q/S**a)/G
    ex_on = ex.subs(sp.Derivative(Z, r), PZ).doit()
    check('radial: Exner integral rQ+cr^2/2=C3 with Z\'=P_Z', ex_on)
    Dc, N = g*H - V**2, H*(S/r + f*W - g*PZ)
    check('radial: momentum = (Delta_c H\' - N)/H', mr.subs(sp.Derivative(Z, r), PZ) - (Dc*sp.diff(H, r) - N)/H)
    kap, gam = sp.symbols('kappa gamma', real=True)
    scaled = N.subs({K: kap*G, c: gam*G, C3: sp.Symbol('C3hat')*G})
    check('radial: N is G-homogeneous of degree 0 in (K,c,C3,G); parameters (m,g,f,C1,C2,K/G,c/G,C3/G)', sp.diff(scaled, G))


def anchored_crossing():
    """Anchor (r,H)=(1,1) with g=C1=C2=1 and symbolic f in (0,2) union {0}."""
    Hs = sp.Symbol('H', positive=True)
    V, W = 1/(r*Hs), 1/r - f*r/2
    S = V**2 + W**2
    a = (m - 1)/2
    S0, W0 = sp.expand(S.subs({r: 1, Hs: 1})), W.subs(r, 1)
    Pstar = S0 + f*W0
    C3a = c/2 + S0**a*(K - Pstar*G)
    PZ = (K*V - (C3a/r - c*r/2)/S**a)/G
    Dc, N = Hs - V**2, Hs*(S/r + f*W - PZ)
    at = {r: 1, Hs: 1}
    check('anchor: Delta_c=0', Dc.subs(at))
    check('anchor: N=0', N.subs(at))
    check('anchor: P_Z=S0+fW0', PZ.subs(at) - Pstar)
    Jm = sp.Matrix([[Dc.diff(r), Dc.diff(Hs)], [N.diff(r), N.diff(Hs)]]).subs(at)
    det = sp.simplify(Jm.det())
    check('anchor: (Delta_c)_H = 3', Jm[0, 1] - 3)
    check('anchor: d det/dc = 3/(G S0^a) > 0', sp.diff(det, c) - 3/(G*S0**a))
    phi = sp.simplify(det - 3*c/(G*S0**a))
    review = sp.Rational(19, 2) + 2*K/G + 3*c/(G*sp.Rational(5, 4)**a) - sp.Rational(13, 5)*(m - 1)*(K/G - sp.Rational(7, 4))
    check('anchor f=1: review determinant', sp.powsimp(sp.expand(det.subs(f, 1) - review), force=True))
    bend = (3*2**((1 - m)/2)*c + 4*G*(m + 1) + K*(4 - 2*m))/G
    check('anchor f=0: bend determinant', sp.powsimp(sp.expand(det.subs(f, 0) - bend), force=True))
    cstar0 = 2**((m + 1)/2)*(K*(m - 2) - 2*G*(m + 1))/3
    check('anchor f=0: threshold c_*', sp.simplify(bend.subs(c, cstar0)))
    check('anchor f=1, m=3, K=G=1: (77+12c)/5', det.subs({f: 1, m: 3, K: 1, G: 1}) - (77 + 12*c)/5)
    records['anchor: closed forms'] = {
        'S0': str(S0), 'P_star': str(sp.simplify(Pstar)), 'C3': str(C3a),
        'det_J': f'3*c/(G*S0**((m-1)/2)) + ({sp.simplify(phi)})',
        'det_J_bend_f0': str(bend), 'c_star_bend_f0': str(cstar0)}


def bowl():
    H, Z = sp.Function('H')(r), sp.Function('Z')(r)
    Zp = c*r**(2 - m)/(2*G*(f/2)**(m - 1))
    E = sp.Symbol('E')
    mass, mr, mt, ex = radial(sp.Integer(0), -f*r/2, H, Z, 'bowl')
    on = {sp.Derivative(Z, r): Zp}
    Hval = E - Z - f**2*r**2/(8*g)
    check('bowl: mass', mass)
    check('bowl: azimuthal momentum', mt)
    check('bowl: C2=0 for W=-fr/2', r*(-f*r/2) + f*r**2/2)
    check('bowl: radial momentum', mr.subs(sp.Derivative(H, r), sp.diff(Hval, r)).subs(on).doit())
    check('bowl: Exner with Q=-cr/2', ex.subs(on).doit())
    check('bowl: Z\'\' = (2-m) Z\'/r', sp.diff(Zp, r) - (2 - m)*Zp/r)
    rp, fp, Gp = sp.symbols('r_p f_p G_p', positive=True)
    ratio = sp.powsimp(sp.simplify((sp.diff(Zp, r)/(c*(2 - m))).subs({r: rp, f: fp, G: Gp})), force=True)
    check('bowl: Z\'\'/(c(2-m)) = 2^(m-2)(fr)^(1-m)/G > 0', sp.simplify(ratio - 2**(m - 2)*(fp*rp)**(1 - m)/Gp),
          'Z\'\'>0 when c>0 and m<2; Z\'\'=0 at m=2; Z\'\'<0 when c>0 and m>2')


def drift():
    # Positive base b = U0^m - x/2, so x = 2(U0^m - b) and d/dx = -(1/2) d/db.
    b = sp.Symbol('b', positive=True)
    U = b**(1/m)
    h, B = 1/U, 2 - 1/U - U**2/2 + t/4
    Dx = lambda F: -sp.diff(F, b)/2
    kappa = sp.Rational(1, 2)
    check('drift: mass', sp.diff(h, t) + Dx(h*U))
    check('drift: momentum', sp.diff(U, t) + U*Dx(U) + Dx(h + B))
    check('drift: Exner', sp.diff(B, t) + kappa*Dx(sp.powsimp(U**m, force=True)))
    U0, mm, xx = sp.symbols('U_0 m_p x_p', positive=True)
    check('drift: d(U0^m)/dm = U0^m log U0 >= 0 for U0>=1', sp.diff(U0**mm, mm) - U0**mm*sp.log(U0))
    check('drift: base at m=1, x=1 equals U0-1/2 >= 1/2', (U0**mm - xx/2).subs({mm: 1, xx: 1}) - (U0 - sp.Rational(1, 2)))
    check('drift: d((1/2)^(1/m))/dm = (1/2)^(1/m) log2/m^2 >= 0',
          sp.diff(sp.Rational(1, 2)**(1/mm), mm) - sp.Rational(1, 2)**(1/mm)*sp.log(2)/mm**2,
          'so U >= (1/2)^(1/m) >= 1/2 for U0>=1, m>=1, x in [0,1]')


def main():
    start = time.time()
    for step in (potential_formulation, admitted_symmetries, radial_reduction, anchored_crossing, bowl, drift):
        step()
    failed = [k for k, v in records.items() if 'zero' in v and not v['zero']]
    print(json.dumps({'checks': records, 'failed': failed, 'seconds': round(time.time() - start, 1)}, indent=1))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
