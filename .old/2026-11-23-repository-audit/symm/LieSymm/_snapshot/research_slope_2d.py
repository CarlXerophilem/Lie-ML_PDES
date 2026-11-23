"""Independent unrestricted 2D SVE slope-family determining calculation.

The exact coefficient identities support the necessity proof in
SLOPE_2D_DERIVATION.md. No finite generator ansatz supplies maximality.
This module deliberately does not import the parent's prolongation engine.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import time

import sympy as s

t,x,y=s.symbols("t x y",real=True)
h=s.Symbol("h",positive=True)
u,v,B=s.symbols("u v B",real=True)
g,G=s.symbols("g G",positive=True)
K=s.Symbol("K",nonnegative=True)
m,n=s.symbols("m n",real=True)
f=s.Symbol("f",real=True,nonzero=True)
xs=(t,x,y)
fields=(h,u,v,B)
coordinates=xs+fields
velocity=s.Matrix([u,v])
position=s.Matrix([x,y])
J=s.Matrix([[0,-1],[1,0]])
speed2=u*u+v*v
radial_D=G*speed2**(n/2)
radial_F=K*speed2**((m-1)/2)*velocity
abstract_D=s.Function("D")(u,v)
abstract_F=s.Matrix([s.Function("F1")(u,v),s.Function("F2")(u,v)])

# 1. Explicit independent J2 implementation, including first-order consequences.
first={(a,i):s.Symbol(f"{field}_{xs[i]}") for a,field in enumerate(fields) for i in range(3)}
second={(a,i,j):s.Symbol(f"{field}_{xs[i]}{xs[j]}")
        for a,field in enumerate(fields) for i in range(3) for j in range(i,3)}


def jet(a,i,j=None):
    return first[a,i] if j is None else second[a,min(i,j),max(i,j)]


def total(expr,axis):
    expr=s.sympify(expr)
    value=s.diff(expr,xs[axis])
    for a,field in enumerate(fields):
        value += jet(a,axis)*s.diff(expr,field)
    for (a,i),symbol in first.items():
        value += jet(a,i,axis)*s.diff(expr,symbol)
    return s.expand(value)


def div(vector):
    return total(vector[0],1)+total(vector[1],2)


def model_data(radial=False):
    D,F=(radial_D,radial_F) if radial else (abstract_D,abstract_F)
    gradB=s.Matrix([jet(3,1),jet(3,2)])
    source=div(F)
    diffusion=div(D*gradB)
    rhs=(
        -u*jet(0,1)-v*jet(0,2)-h*(jet(1,1)+jet(2,2)),
        -u*jet(1,1)-v*jet(1,2)-g*(jet(0,1)+jet(3,1))+f*v,
        -u*jet(2,1)-v*jet(2,2)-g*(jet(0,2)+jet(3,2))-f*u,
        -source+diffusion,
    )
    return D,F,source,diffusion,rhs


def clean(expr):
    expanded=s.expand(expr)
    if expanded==0:
        return s.S.Zero
    reduced=s.simplify(s.factor_terms(expanded))
    if reduced==0 or not any(power.base==speed2 for power in reduced.atoms(s.Pow)):
        return reduced
    # The chart gives R2=u**2+v**2>0. Keep related radial powers related:
    # S**(m/2-1/2) and S**(m/2+1/2) differ by exactly one power of S.
    # Group only integer exponent shifts, then impose S=u**2+v**2 on
    # their rational coefficients. No exponent independence is presumed.
    radial=s.Dummy("R2",positive=True)
    value=s.expand(s.powdenest(reduced.xreplace({speed2:radial}),force=True))
    grouped={}
    for term in s.Add.make_args(value):
        exponent,coefficient=s.S.Zero,s.S.One
        for factor in s.Mul.make_args(s.factor_terms(term)):
            if factor==radial:
                exponent+=1
            elif isinstance(factor,s.Pow) and factor.base==radial:
                exponent+=factor.exp
            else:
                coefficient*=factor
        constant,variable=s.expand(exponent).as_coeff_Add()
        integer=s.floor(constant)
        if integer.is_Integer:
            key=s.simplify(variable+constant-integer)
            coefficient*=radial**integer
        else:
            key=s.simplify(exponent)
        grouped[key]=grouped.get(key,0)+coefficient
    return s.factor_terms(sum(s.simplify(coefficient.subs(radial,speed2))*speed2**exponent
                             for exponent,coefficient in grouped.items()))


def residuals(generator,radial=False):
    tau,xi,zeta,a,b,c,d=map(s.sympify,generator)
    base=(tau,xi,zeta)
    etas=(a,b,c,d)
    D,F,source,diffusion,rhs=model_data(radial)
    prolong={}
    for alpha,e in enumerate(etas):
        for i in range(3):
            prolong[alpha,i]=total(e,i)-sum(jet(alpha,j)*total(base[j],i) for j in range(3))
    bed_second=[]
    for i in (1,2):
        bed_second.append(total(prolong[3,i],i)-sum(jet(3,j,i)*total(base[j],i) for j in range(3)))
    water=(prolong[0,0]+b*jet(0,1)+c*jet(0,2)+u*prolong[0,1]+v*prolong[0,2]
           +a*(jet(1,1)+jet(2,2))+h*(prolong[1,1]+prolong[2,2]))
    momentum=[]
    for alpha,e in ((1,b),(2,c)):
        cor=-f*c if alpha==1 else f*b
        momentum.append(prolong[alpha,0]+b*jet(alpha,1)+c*jet(alpha,2)
                        +u*prolong[alpha,1]+v*prolong[alpha,2]
                        +g*(prolong[0,alpha]+prolong[3,alpha])+cor)
    bed=prolong[3,0]
    vel_eta=(b,c)
    for i in range(2):
        for j in range(2):
            bed += s.diff(F[i],velocity[j])*prolong[j+1,i+1]
            for k in range(2):
                bed += s.diff(F[i],velocity[j],velocity[k])*vel_eta[k]*jet(j+1,i+1)
            bed -= s.diff(D,velocity[j])*(prolong[j+1,i+1]*jet(3,i+1)+jet(j+1,i+1)*prolong[3,i+1])
            for k in range(2):
                bed -= s.diff(D,velocity[j],velocity[k])*vel_eta[k]*jet(j+1,i+1)*jet(3,i+1)
        bed -= sum(s.diff(D,velocity[k])*vel_eta[k] for k in range(2))*jet(3,i+1,i+1)
        bed -= D*bed_second[i]
    subs={jet(a,0):rhs[a] for a in range(4)}
    return tuple(s.expand(expr.subs(subs,simultaneous=True)) for expr in (water,*momentum,bed))


def fn(name,args=coordinates):
    return s.Function(name)(*args)


def _checker():
    checks=[]
    def check(name,actual,expected=0):
        delta=clean(actual-expected)
        if delta!=0:
            raise AssertionError(name+": "+str(delta))
        checks.append(name)
    return checks,check


# 2. Principal jets force projectability before the hydrodynamic equations.
def check_principal():
    checks,check=_checker()
    D,F,source,diffusion,rhs=model_data()
    gen=[fn(name) for name in ("tau","xi","zeta","a","b","c","d")]
    raw=residuals(gen)
    for axis in (1,2):
        check("arbitrary B_t"+str(axis)+" coefficient",s.diff(raw[3],jet(3,0,axis)),2*D*total(gen[0],axis))
    gen[0]=fn("tau",(t,))
    raw=residuals(gen)
    for alpha in range(3):
        coefficient=-D*(s.diff(gen[6],fields[alpha])-jet(3,1)*s.diff(gen[1],fields[alpha])
                         -jet(3,2)*s.diff(gen[2],fields[alpha]))
        check("fluid spatial Hessian "+str(alpha),s.diff(raw[3],jet(alpha,1,1)),coefficient)
    gen[1],gen[2],gen[6]=[fn(name,(t,x,y,B)) for name in ("xi","zeta","d")]
    raw=residuals(gen)
    etaD=s.diff(D,u)*gen[4]+s.diff(D,v)*gen[5]
    check("B_xx coefficient",s.diff(raw[3],jet(3,1,1)),
          D*(2*s.diff(gen[1],x)-s.diff(gen[0],t)+2*jet(3,1)*s.diff(gen[1],B))-etaD)
    check("B_yy coefficient",s.diff(raw[3],jet(3,2,2)),
          D*(2*s.diff(gen[2],y)-s.diff(gen[0],t)+2*jet(3,2)*s.diff(gen[2],B))-etaD)
    check("B_xy coefficient",s.diff(raw[3],jet(3,1,2)),
          2*D*(s.diff(gen[1],y)+s.diff(gen[2],x)+jet(3,2)*s.diff(gen[1],B)+jet(3,1)*s.diff(gen[2],B)))
    gen[1],gen[2]=fn("xi",(t,x,y)),fn("zeta",(t,x,y))
    raw=residuals(gen)
    for alpha in range(3):
        check("hydro Laplacian coefficient "+str(alpha),s.diff(raw[alpha],jet(3,1,1)),D*s.diff(gen[alpha+3],B))
    gen[3],gen[4],gen[5]=[fn(name,(t,x,y,h,u,v)) for name in ("a","b","c")]
    raw=residuals(gen)
    check("mass B_x gives a_u",s.diff(raw[0],jet(3,1)),-g*s.diff(gen[3],u))
    check("mass B_y gives a_v",s.diff(raw[0],jet(3,2)),-g*s.diff(gen[3],v))
    # All J2 consequences of the three first-order rows are retained.
    rules={jet(a,0):rhs[a] for a in range(4)}
    for a in range(3):
        for axis in (1,2):
            rules[jet(a,0,axis)]=total(rhs[a],axis)
    for a in range(3):
        rules[jet(a,0,0)]=total(rhs[a],0).subs(rules,simultaneous=True)
    for a in range(3):
        row=jet(a,0)-rhs[a]
        for axis in range(3):
            check("mixed-order consequence "+str(a)+"/"+str(axis),total(row,axis).subs(rules,simultaneous=True))
    return checks


# 3. Reconstruct the complete hydro determining equations, then integrate them.
def check_hydro():
    checks,check=_checker()
    tau=fn("tau",(t,))
    spatial=s.Matrix([fn("xi",(t,x,y)),fn("zeta",(t,x,y))])
    a=fn("a",(t,x,y,h))
    b=s.Matrix([fn("b",(t,x,y,h,u,v)),fn("c",(t,x,y,h,u,v))])
    d=fn("d",(t,x,y,B))
    raw=residuals((tau,*spatial,a,*b,d))
    A=spatial.jacobian((x,y))
    Bw=b.jacobian((u,v))
    V=b-spatial.diff(t)+(s.diff(tau,t)*s.eye(2)-A)*velocity
    grad_h=s.Matrix([jet(0,1),jet(0,2)])
    grad_B=s.Matrix([jet(3,1),jet(3,2)])
    P=s.Matrix(2,2,lambda j,i:jet(j+1,i+1))
    mass=s.diff(a,t)+sum(velocity[i]*s.diff(a,xs[i+1])+h*s.diff(b[i],xs[i+1]) for i in range(2))
    mass += ((V+h*b.diff(h)).dot(grad_h))
    for i in range(2):
        for j in range(2):
            coefficient=h*(Bw[i,j]-A[i,j])
            if i==j:
                coefficient+=a-h*s.diff(a,h)+h*s.diff(tau,t)
            mass+=coefficient*P[j,i]
    check("complete mass determining polynomial",raw[0],mass)
    constant=b.diff(t)+sum((velocity[i]*b.diff(xs[i+1]) for i in range(2)),s.zeros(2,1))
    constant+=g*s.Matrix([s.diff(a+d,x),s.diff(a+d,y)])
    constant+=f*(J*b-Bw*J*velocity+s.diff(tau,t)*J*velocity)
    momentum=constant+g*((s.diff(a,h)+s.diff(tau,t))*s.eye(2)-Bw-A.T)*grad_h
    momentum+=g*((s.diff(d,B)+s.diff(tau,t))*s.eye(2)-Bw-A.T)*grad_B
    momentum+=P*V-h*b.diff(h)*s.trace(P)
    for i in range(2):
        check("complete momentum determining polynomial "+str(i),raw[i+1],momentum[i])

    # Exact integration, with arbitrary time functions retained until bed constraints.
    k,omega0=s.symbols("k omega0",real=True)
    shift=s.Matrix([fn("p",(t,)),fn("q",(t,))])
    sigma=s.diff(tau,t)/2+k
    omega=omega0-f*tau/2
    alpha=sigma-s.diff(tau,t)
    A=sigma*s.eye(2)+omega*J
    spatial=A*position+shift
    b=spatial.diff(t)+(A-s.diff(tau,t)*s.eye(2))*velocity
    psi=-(s.diff(tau,t,3)+f*f*s.diff(tau,t))*(x*x+y*y)/(4*g)
    psi-=((shift.diff(t,2)+f*J*shift.diff(t)).dot(position))/g
    psi+=fn("S",(t,))
    integrated=(tau,*spatial,2*alpha*h,*b,2*alpha*B+psi)
    integrated_raw=residuals(integrated)
    for i in range(3):
        check("integrated arbitrary-time hydro identity "+str(i),integrated_raw[i])
    return checks


# 4. A divergence identity integrates the remaining bed equation without n division.
def check_bed():
    checks,check=_checker()
    D,F,source,diffusion,rhs=model_data()
    tau=fn("tau",(t,));sigma=fn("sigma",(t,));omega=fn("omega",(t,))
    shift=s.Matrix([fn("p",(t,)),fn("q",(t,))])
    A=sigma*s.eye(2)+omega*J
    spatial=A*position+shift
    alpha=sigma-s.diff(tau,t)
    chi=2*alpha
    b=spatial.diff(t)+(A-s.diff(tau,t)*s.eye(2))*velocity
    psi=fn("psi",(t,x,y))
    raw=residuals((tau,*spatial,chi*h,*b,chi*B+psi))
    gradB=s.Matrix([jet(3,1),jet(3,2)])
    gradpsi=s.Matrix([s.diff(psi,x),s.diff(psi,y)])
    etaD=s.diff(D,u)*b[0]+s.diff(D,v)*b[1]
    expected=(chi-s.diff(tau,t))*rhs[3]+s.diff(chi,t)*B+s.diff(psi,t)-spatial.diff(t).dot(gradB)
    expected+=div(F.jacobian((u,v))*b-A*F)
    expected-=div(((etaD+chi*D)*s.eye(2)-D*(A+A.T))*gradB+D*gradpsi)
    check("complete bed divergence transformation",raw[3],expected)

    # The radial covariance identities justify the compact m,n form for all
    # real exponents on speed_squared>0, not a finite exponent sample.
    aa,ww=s.symbols("alpha omega",real=True)
    M=aa*s.eye(2)+ww*J
    covariant=radial_F.jacobian((u,v))*M*velocity-(m*aa*s.eye(2)+ww*J)*radial_F
    for i in range(2):
        check("radial vector covariance "+str(i),covariant[i])
    check("radial scalar homogeneity",s.diff(radial_D,u)*(M*velocity)[0]+s.diff(radial_D,v)*(M*velocity)[1],n*aa*radial_D)
    check("radial transport nonzero parallel contraction",(velocity.T*radial_F.jacobian((u,v))*velocity)[0],m*K*speed2**((m+1)/2))
    return checks


# 5. Solve the surviving constant equations on each explicit parameter branch.
def general_solution(branch,coordinates=None,exponent=None):
    selected=globals()["coordinates"] if coordinates is None else tuple(coordinates)
    if len(selected)!=7:
        raise ValueError("coordinates must be (t,x,y,h,u,v,B)")
    tt,xx,yy,hh,uu,vv,BB=selected
    coriolis=0 if branch.endswith("_f0") else f
    base=branch[:-3] if branch.endswith("_f0") else branch[:-10] if branch.endswith("_f_nonzero") else None
    if base is None:
        raise ValueError("branch must declare f0 or f_nonzero")
    guards=["G>0","h>0","u**2+v**2>0","g>0","f=0" if coriolis==0 else "f!=0"]
    if base in ("slope_attachment_generic","slope_source_generic"):
        mm=m if exponent is None else s.sympify(exponent)
        if mm.is_number and (mm==3 or not 1<=mm<=4):
            raise ValueError("generic transport branch requires 1<=m<=4,m!=3")
        nn=mm-1 if base=="slope_attachment_generic" else mm
        source_factor=K*mm*(mm-3)
        guards += ["K>0","1<=m<=4","m!=3"]
    elif base in ("slope_attachment_cubic","slope_source_cubic"):
        if exponent is not None and s.sympify(exponent)!=3:
            raise ValueError("cubic branch requires m=3")
        mm=s.Integer(3)
        nn=s.Integer(2 if base=="slope_attachment_cubic" else 3)
        source_factor=s.S.Zero
        guards += ["K>0","m=3"]
    elif base in ("slope_only","slope_only_generic","slope_only_n2"):
        mm=None
        nn=s.Integer(2) if base=="slope_only_n2" else n if exponent is None else s.sympify(exponent)
        if nn.is_number and not 0<=nn<=4:
            raise ValueError("slope-only exponent must lie in [0,4]")
        if base=="slope_only_n2" and exponent is not None and s.sympify(exponent)!=2:
            raise ValueError("n2 branch requires n=2")
        if base=="slope_only_generic" and nn==2:
            raise ValueError("generic rotating slope-only branch excludes n=2")
        if base=="slope_only" and coriolis!=0 and not nn.is_number:
            raise ValueError("rotating slope-only family must split n=2 from n!=2")
        source_factor=s.S.Zero
        guards += ["K=0","0<=n<=4"]
        if base=="slope_only_generic":guards += ["n!=2"]
        if base=="slope_only_n2":guards += ["n=2"]
    else:
        raise ValueError("not a positive-diffusion 2D branch: "+branch)
    t0,x0,y0,b0,omega0,T,d=s.symbols("t0 x0 y0 b0 omega0 T d",real=True)
    equations=(T+(2-nn)*d,source_factor*d,coriolis*T)
    solved=tuple(s.linsolve(equations,(T,d)))[0]
    Ts,ds=solved
    coefficients=s.Matrix([T*tt+t0,(T+d)*xx-omega0*yy+x0,
                           omega0*xx+(T+d)*yy+y0,2*d*hh,
                           d*uu-omega0*vv,omega0*uu+d*vv,b0+2*d*BB])
    coefficients=coefficients.subs({T:Ts,d:ds},simultaneous=True)
    constants=tuple(z for z in (t0,x0,y0,b0,omega0,d) if coefficients.has(z))
    return {"coefficients":coefficients,"free_constants":constants,
            "basis":tuple(coefficients.diff(z) for z in constants),"constant_equations":equations,
            "constant_solution":solved,"guards":guards,"branch":branch,"m":mm,"n":nn,
            "review_status":"pending_fresh_review"}


def check_final():
    checks,check=_checker()
    translations=((1,0,0,0,0,0,0),(0,1,0,0,0,0,0),(0,0,1,0,0,0,0),(0,0,0,0,0,0,1))
    rotation=(0,-y,x,0,-v,u,0)
    for label,gen in [("translation "+str(i),q) for i,q in enumerate(translations)]+[("joint rotation",rotation)]:
        for row,value in enumerate(residuals(gen,radial=True)):
            check(label+" row "+str(row),value)
    dilation=((n-2)*t,(n-1)*x,(n-1)*y,2*h,u,v,2*B)
    raw=residuals(dilation,radial=True)
    source=model_data(radial=True)[2]
    expected=(0,-f*(n-2)*v,f*(n-2)*u,(m-3)*source)
    for row in range(4):
        check("exact dilation obstruction row "+str(row),raw[row],expected[row])
    branches=[f"{law}_{flow}" for law in ("slope_attachment_generic","slope_attachment_cubic",
              "slope_source_generic","slope_source_cubic") for flow in ("f0","f_nonzero")]
    branches += ["slope_only_f0","slope_only_generic_f_nonzero","slope_only_n2_f_nonzero"]
    solutions={}
    for branch in branches:
        sol=general_solution(branch)
        T,d=s.symbols("T d",real=True)
        for row,eq in enumerate(sol["constant_equations"]):
            check("constant solve "+branch+"/"+str(row),eq.subs({T:sol["constant_solution"][0],d:sol["constant_solution"][1]},simultaneous=True))
        solutions[branch]={"coefficients":[str(z) for z in sol["coefficients"]],
                           "free_constants":[str(z) for z in sol["free_constants"]],
                           "dimension":len(sol["free_constants"]),"guards":sol["guards"],
                           "constant_equations":[str(z) for z in sol["constant_equations"]]}
    controls={
        "spatial_rotation_without_velocity_rotation":[str(clean(q)) for q in residuals((0,-y,x,0,0,0,0),radial=True)[:3]],
        "rotating_m3_n3_dilation":[str(clean(q.subs({m:3,n:3}))) for q in raw],
        "time_dependent_bed_gauge":[str(clean(q)) for q in residuals((0,0,0,0,0,0,t),radial=True)],
    }
    for label,values in controls.items():
        if all(q=="0" for q in values):
            raise AssertionError("broken hypothesis was accepted: "+label)
    return checks,solutions,controls


def run(phase="all",timeout_seconds=60):
    started=time.perf_counter()
    receipt={"status":"exact_phase_checks_passed; unrestricted_classification_pending_fresh_review",
             "phase":phase,"declared_process_timeout_seconds":timeout_seconds,"checks":[]}
    phases={"principal":check_principal,"hydro":check_hydro,"bed":check_bed}
    for name,action in phases.items():
        if phase in (name,"all"):
            receipt["checks"]+=action()
    if phase in ("final","all"):
        checks,solutions,controls=check_final()
        receipt["checks"]+=checks
        receipt["branch_solutions"]=solutions
        receipt["broken_hypothesis_controls"]=controls
    receipt.update({"check_count":len(receipt["checks"]),"elapsed_seconds":time.perf_counter()-started,
                    "scope":"2D full evolving-bed SVE; h>0,u**2+v**2>0,g>0,G>0; constant f",
                    "division_guards":["G*(u**2+v**2)**(n/2)>0","h>0","g>0","u**2+v**2>0"],
                    "no_division_by":["u","v","n","n-2","m-3","K","f"],
                    "surviving_constant_equations":["T+(2-n)*d=0","m*K*(m-3)*d=0","f*T=0"],
                    "maximality_review":"pending_fresh_review"})
    Path(__file__).with_name("slope_2d_results.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:receipt[k] for k in ("status","phase","check_count","elapsed_seconds")},indent=2))
    return receipt


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase",choices=("all","principal","hydro","bed","final"),default="all")
    parser.add_argument("--timeout-seconds",type=int,default=60,
                        help="receipt metadata; the caller must enforce this limit with subprocess.run(timeout=...)")
    args=parser.parse_args()
    run(args.phase,args.timeout_seconds)
