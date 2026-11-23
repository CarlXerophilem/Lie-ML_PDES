"""Final exact pullbacks for the rotating exchange tank and separate cubic E2."""
import json
import sympy as s

t, th = s.symbols("t theta", real=True)
r, g, K, G = s.symbols("r g K G", positive=True)
omega, f, kd, ke, Cb, Da = s.symbols("Omega f k_d k_e c D_a", real=True)
ct, st = s.cos(th), s.sin(th)
er, ea = s.Matrix([ct,st]), s.Matrix([-st,ct])


def clean(expr):
    return s.factor(s.trigsimp(s.expand(expr)))


def grad(a):
    return er*a.diff(r)+ea*a.diff(th)/r


def div(w):
    return clean(sum(grad(w[i])[i] for i in range(2)))


def residual(H,V,W,B,A=None):
    velocity=V*er+W*ea
    speed=clean(velocity.dot(velocity))
    flux=speed*(K*velocity-G*grad(B))
    exchange=A is not None
    spin=2*omega if exchange else f
    mom=velocity.diff(t)+s.Matrix([velocity.dot(grad(c)) for c in velocity])
    mom+=g*grad(H+B)+spin*s.Matrix([-velocity[1],velocity[0]])
    if exchange:
        mom-=omega**2*r*er
    result=s.Matrix([H.diff(t)+div(H*velocity),clean(mom.dot(er)),
                     clean(mom.dot(ea)),B.diff(t)+div(flux)])
    if exchange:
        J=kd*A-ke*B
        result[3]-=J
        result=result.col_join(s.Matrix([A.diff(t)+div(A*velocity-Da*H*grad(A/H))+J]))
    return result.applyfunc(clean)


def run():
    H,V,W,B,A = (s.Function(n)(t,r) for n in ("H","V","W","B","a"))
    E=residual(H,V,W,B,A)
    Q=(V**2+W**2)*(K*V-G*B.diff(r))
    J=kd*A-ke*B
    expected=s.Matrix([H.diff(t)+(r*H*V).diff(r)/r,
        V.diff(t)+V*V.diff(r)-W**2/r+g*(H+B).diff(r)-2*omega*W-omega**2*r,
        W.diff(t)+V*W.diff(r)+V*W/r+2*omega*V,
        B.diff(t)+(r*Q).diff(r)/r-J,
        A.diff(t)+(r*(A*V-Da*H*(A/H).diff(r))).diff(r)/r+J])
    assert (E-expected).applyfunc(s.simplify) == s.zeros(5,1)
    c1,c2,c3=s.symbols("C1 C2 C3",real=True,nonzero=True)
    h,v,w,z=[s.Function(n)(r) for n in ("H","V","W","Z")]
    e2_rotation=residual(H,V,W,B)
    e2=residual(h,v,w,z+Cb*t)
    e2_expected=e2_rotation.subs({H:h,V:v,W:w,B:z+Cb*t}).doit()
    assert (e2-e2_expected).applyfunc(s.simplify)==s.zeros(4,1)
    vs=c1/(r*h)
    ws=c2/r-f*r/2
    q0=c3/r-Cb*r/2
    S=vs**2+ws**2
    pz=(K*vs-q0/S)/G
    D=g*h-vs**2
    N=h*(S/r+f*ws-g*pz)
    reduced=e2.subs({v:vs,w:ws}).doit().subs(
        {z.diff(r,2):pz.diff(r),z.diff(r):pz})
    assert (reduced-s.Matrix([0,(D*h.diff(r)-N)/h,0,0])).applyfunc(s.factor)==s.zeros(4,1)
    p=s.Symbol("p", real=True)
    b=s.Rational(3,10)+(p-s.Rational(3,10))*s.exp(-3*t)
    bed=s.Rational(1,10)/r**2
    controls={H:1+s.Rational(25,72)*r**2-bed,V:0,W:r/2,
              B:bed+b,A:bed/2+s.Rational(9,20)-b}
    pars={g:1,K:1,G:1,omega:s.Rational(1,3),kd:2,ke:1,Da:0}
    check=E.xreplace(controls).subs(pars).doit().applyfunc(s.simplify)
    assert check==s.zeros(5,1)
    assert s.simplify((r*Q).xreplace(controls).subs(pars).doit())==s.Rational(1,20)
    return {
        "tank_rotation_generator":"-y*dx+x*dy-v*du+u*dv",
        "rank_1_rotation_quotient_variables":["t","r"],
        "rank_1_exchange_residuals": list(map(str,expected)),
        "swirl_b":str(b),"swirl_residuals":list(map(str,check)),
        "swirl_r_Qr":"1/20",
        "wholly_separate_E2_rotation_residuals":list(map(str,e2_rotation)),
        "E2_rotation_plus_bed_drift_residuals":list(map(str,e2)),
        "E2_slope_equation":"D*dH/dr=N; dZ/dr=P_Z",
        "E2_profiles":{"V":str(vs),"W":str(ws),"D":str(D),"N":str(N),"P_Z":str(pz)},
        "scope":"Exact quotients and selected branch tests. No maximal planar point-symmetry classification."
    }


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
