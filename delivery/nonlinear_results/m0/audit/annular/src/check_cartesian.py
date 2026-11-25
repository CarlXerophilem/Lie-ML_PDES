"""Independent Cartesian differentiation of the original coupled PDE.

This file does not import the polar derivation or its output. All derivative
substitutions below are defined jets of H(r) and Z(r), with Z'=P(r,H) and
Z''=P_r+P_H H'. No residual is represented by an independent placeholder.
"""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parents[1]/'results/cartesian.json'
t,x,y=s.symbols('t x y',real=True)
r,h=s.symbols('r H',positive=True)
dh=s.symbols('dH',real=True)
g,K,G=s.symbols('g K G',positive=True)
f,c,C1,C2,C3=s.symbols('f c C1 C2 C3',real=True)

def zero(expr):
    v=s.factor(s.simplify(expr))
    assert v == 0,str(v)
    return str(v)

# First check the full Cartesian angular-current identity with arbitrary bed.
h0=s.Function('h')(t,x,y); u0=s.Function('u')(t,x,y)
v0=s.Function('v')(t,x,y); B0=s.Function('B')(t,x,y)
M=s.diff(h0,t)+s.diff(h0*u0,x)+s.diff(h0*v0,y)
Eu=s.diff(u0,t)+u0*s.diff(u0,x)+v0*s.diff(u0,y)+g*s.diff(h0+B0,x)-f*v0
Ev=s.diff(v0,t)+u0*s.diff(v0,x)+v0*s.diff(v0,y)+g*s.diff(h0+B0,y)+f*u0
ell=x*v0-y*u0+f*(x*x+y*y)/2
angular_flux_x=h0*u0*ell-g*h0**2*y/2
angular_flux_y=h0*v0*ell+g*h0**2*x/2
angular_balance=s.diff(h0*ell,t)+s.diff(angular_flux_x,x)+s.diff(angular_flux_y,y)
torque=g*h0*(x*s.diff(B0,y)-y*s.diff(B0,x))
current_identity=zero(angular_balance-(ell*M+h0*(x*Ev-y*Eu)-torque))

# Actual Cartesian fields, before any coordinate or derivative substitution.
R=s.sqrt(x*x+y*y)
HF=s.Function('H'); ZF=s.Function('Z')
H=HF(R); Z=ZF(R)
V=C1/(R*H); W=C2/R-f*R/2
u=V*x/R-W*y/R; v=V*y/R+W*x/R; B=Z+c*t
speed=s.factor(u*u+v*v)
qx=K*speed*u-G*speed*s.diff(B,x)
qy=K*speed*v-G*speed*s.diff(B,y)
mass=s.diff(H,t)+s.diff(H*u,x)+s.diff(H*v,y)
mx=s.diff(u,t)+u*s.diff(u,x)+v*s.diff(u,y)+g*s.diff(H+B,x)-f*v
my=s.diff(v,t)+u*s.diff(v,x)+v*s.diff(v,y)+g*s.diff(H+B,y)+f*u
bed=s.diff(B,t)+s.diff(qx,x)+s.diff(qy,y)

# The slope is independently obtained by solving the declared constitutive law.
vr=C1/(r*h); wr=C2/r-f*r/2; qr=C3/r-c*r/2
p=s.symbols('P',real=True)
P=s.solve(s.Eq((vr*vr+wr*wr)*(K*vr-G*p),qr),p)[0]
Pprime=s.diff(P,r)+s.diff(P,h)*dh
D=g*h-vr**2
N=h*((vr**2+wr**2)/r+f*wr-g*P)
eval_r=lambda a:a.subs(r,R)

def jets(expr,p0=P,p1=Pprime):
    replacements={}
    for atom in expr.atoms(s.Subs):
        assert atom.point==(R,),str(atom)
        derivative=atom.expr
        assert isinstance(derivative,s.Derivative)
        name=derivative.expr.func.__name__
        order=sum(n for _,n in derivative.variable_count)
        if name=='H' and order==1: value=dh
        elif name=='Z' and order==1:value=eval_r(p0)
        elif name=='Z' and order==2:value=eval_r(p1)
        else:raise AssertionError('Unhandled derivative '+str(atom))
        replacements[atom]=value
    answer=expr.xreplace(replacements).xreplace({H:h})
    assert not answer.has(s.Subs,s.Derivative)
    return s.factor(answer)

res={}
res['mass']=zero(jets(mass))
res['momentum_x_identity']=zero(jets(mx)-x/R*eval_r((D*dh-N)/h))
res['momentum_y_identity']=zero(jets(my)-y/R*eval_r((D*dh-N)/h))
res['Exner']=zero(jets(bed))
res['radial_flux_identity']=zero(jets(qx*x/R+qy*y/R)-eval_r(qr))

# Fault injection: changing bed slope must change momentum, not be erased by a
# substituted residual. The additional slope is constant, so p1 is unchanged.
eps=s.symbols('epsilon',real=True)
res['bed_slope_fault_x_detected']=zero(jets(mx,P+eps,Pprime)-jets(mx)-g*eps*x/R)
res['bed_slope_fault_y_detected']=zero(jets(my,P+eps,Pprime)-jets(my)-g*eps*y/R)

critical={x:1,y:0,h:1,g:1,K:1,G:1,f:1,C1:1,C2:1,C3:-s.Rational(71,16),c:-7}
flat_radial=s.factor(jets(mx,s.Integer(0),s.Integer(0)).subs(critical))
assert flat_radial==-s.Rational(7,4)

data={'status':'EXACT_CARTESIAN_RECONSTRUCTION_IDENTITIES_VERIFIED',
 'sympy_version':s.__version__,'polar_derivation_imported':False,
 'original_current_identity':current_identity,
 'angular_current':{'density':str(h0*ell),'flux_x':str(angular_flux_x),'flux_y':str(angular_flux_y),
   'on_solution_source':str(-torque)},
 'checks':res,'flat_bed_radial_residual_at_critical_water_state':str(flat_radial),
 'logical_consequence':'Any C1 H satisfying DHprime=N with Zprime=P reconstructs the full PDE, including D=0; Z is C2.',
 'not_established_by_this_script':['existence of H','stable-manifold theorem','numerical enclosure','novelty','arbitrary-IBVP well-posedness']}
with OUT.open('x') as stream:json.dump(data,stream,indent=2);stream.write('\n')
print(json.dumps({'output':str(OUT),'status':data['status'],'checks':len(res)+1}))
