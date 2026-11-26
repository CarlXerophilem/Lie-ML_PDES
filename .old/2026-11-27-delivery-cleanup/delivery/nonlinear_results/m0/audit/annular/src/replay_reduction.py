"""Replay the invariant-class reduction using previously DERIVED graph forms.

This stage reads the graph returned by this package's determining/invariant
chain. It is NOT an unrestricted Lie discovery or a complete-classification
certificate. No historical answer is imported. Generic radial flux components
retain their defined constitutive meaning; no PDE residual is replaced by a
free placeholder. The separate Cartesian checker does not import this stage.
"""
from pathlib import Path
import json
import hashlib
import sympy as s

OUT = Path(__file__).resolve().parents[1] / 'results/derived-reduction.json'
t, r, theta = s.symbols('t r theta', real=True)
g, K, G = s.symbols('g K G', positive=True)
f, c, C1, C2, C3 = s.symbols('f c C1 C2 C3', real=True)
H, V, W, Z, Q, T = [s.Function(n)(r) for n in ['H','V','W','Z','Q','T']]
co, si = s.cos(theta), s.sin(theta)

def dx(a): return co*s.diff(a,r)-si*s.diff(a,theta)/r
def dy(a): return si*s.diff(a,r)+co*s.diff(a,theta)/r
def clean(a): return s.factor(s.trigsimp(s.expand(a)))
def zero(a):
    v=clean(a)
    assert v == 0, str(v)

# Original differential operators evaluated on the invariant fields. Q,T are
# the radial/angular components of q(H, V er + W etheta, Z' er), respectively.
invariant_file=Path(__file__).resolve().parents[1]/'results/derived-invariants.json'
invariant_data=json.loads(invariant_file.read_text())
assert invariant_data['status']=='INVARIANTS_AND_GRAPH_RECONSTRUCTION_DERIVED_FROM_DETERMINED_GENERATORS'
xs,ys=s.symbols('x y',real=True)
parse={'r':r,'t':t,'x':xs,'y':ys,'c':c}
parse.update({n:s.Function(n) for n in ['H','V','W','Z']})
forms={k:s.sympify(a,locals=parse).subs({xs:r*co,ys:r*si})
       for k,a in invariant_data['graph_forms'].items()}
assert s.simplify(forms['h']-H)==0
u,v,b=forms['u'],forms['v'],forms['B']
# Pull back the original Cartesian closure before introducing defined flux
# components. Q and T are auxiliary components, never free PDE residuals.
speed_squared=clean(u*u+v*v)
qx_original=K*speed_squared*u-G*speed_squared*dx(b)
qy_original=K*speed_squared*v-G*speed_squared*dy(b)
radial_closure=clean(co*qx_original+si*qy_original)
tangential_closure=clean(-si*qx_original+co*qy_original)
qx, qy = Q*co-T*si, Q*si+T*co
mass = s.diff(H,t)+dx(H*u)+dy(H*v)
mx = s.diff(u,t)+u*dx(u)+v*dy(u)+g*dx(H+b)-f*v
my = s.diff(v,t)+u*dx(v)+v*dy(v)+g*dy(H+b)+f*u
bed = s.diff(b,t)+dx(qx)+dy(qy)
radial=clean(co*mx+si*my)
angular=clean(-si*mx+co*my)
mass,bed=clean(mass),clean(bed)
original_bed=s.diff(b,t)+dx(qx_original)+dy(qy_original)
zero(original_bed-bed.subs({Q:radial_closure,T:tangential_closure}).doit())
pulled = dict(mass=mass, radial_momentum=radial,
              tangential_momentum=angular, Exner=bed)

# Currents are obtained from the original mass/bed flux and polar Jacobian.
mass_current=clean(r*(H*u*co+H*v*si))
bed_current=clean(r*(qx*co+qy*si))
zero(r*mass-s.diff(mass_current,r))
bed_forcing=clean(r*bed-s.diff(bed_current,r))
I1=mass_current
I3=clean(bed_current+s.integrate(bed_forcing,r))

# Integrating factor is derived from the actual tangential equation, dividing
# only on the declared V != 0 chart. Constants from primitives remain free C2.
theta_normal=clean(angular/V)
leading=s.expand(theta_normal).coeff(s.diff(W,r))
assert leading == 1
rest=clean(theta_normal-s.diff(W,r))
a=clean(s.diff(rest,W)); forcing=clean(rest-a*W)
mu=clean(s.exp(s.integrate(a,r)))
I2=clean(mu*W+s.integrate(mu*forcing,r))
zero(s.diff(I2,r)-mu*theta_normal)

V_sol=s.solve(s.Eq(I1,C1),V)[0]
W_sol=s.solve(s.Eq(I2,C2),W)[0]
Q_sol=s.solve(s.Eq(I3,C3),Q)[0]
red=clean(radial.subs({V:V_sol,W:W_sol}).doit())
hh, dh, pp=s.symbols('H dH P', real=True)
red=red.subs({s.diff(H,r):dh,s.diff(Z,r):pp,H:hh})
D=clean(hh*s.diff(red,dh))
N=clean(-hh*red.subs(dh,0))
zero(hh*red-(D*dh-N))

vv,ww,qq=s.symbols('V W Q',real=True)
law=radial_closure.subs({s.diff(Z,r):pp,V:vv,W:ww})
slope=s.solve(s.Eq(law,qq),pp)[0]
V_value=V_sol.subs(H,hh); W_value=W_sol; Q_value=Q_sol
P=s.factor(slope.subs({vv:V_value,ww:W_value,qq:Q_value}))
N_cubic=s.factor(N.subs(pp,P))
rank=s.Matrix([I1,I2,I3]).jacobian([H,W,Q]).det()

# Critical projection condition is symbolic, for every positive g,H,r.
critical_relation={C1**2:g*r**2*hh**3}
zero((s.diff(D,hh)-3*g).subs(critical_relation))
zero((s.diff(D,r)-2*g*hh/r).subs(critical_relation))

# Supplied dimensionless parameter slice; solve for the missing compatible C3.
slice_parameters={g:1,K:1,G:1,f:1,C1:1,C2:1}
point={r:1,hh:1}
Ds=D.subs(slice_parameters)
Ns=N_cubic.subs(slice_parameters)
C3_family=s.solve(s.Eq(Ns.subs(point),0),C3)[0]
Ns=s.factor(Ns.subs(C3,C3_family))
J=s.Matrix([Ds,Ns]).jacobian([r,hh]).subs(point).applyfunc(s.factor)
det=s.factor(J.det())
saddle=s.solve_univariate_inequality(det<0,c)
z=s.symbols('s',real=True)
slopes=s.factor(J[0,1]*z**2+(J[0,0]-J[1,1])*z-J[1,0])
example_slopes=s.solve(slopes.subs(c,-7),z)
example_eigenvalues=[s.simplify(J[0,0]+J[0,1]*a) for a in example_slopes]
zero(Ds.subs(point)); zero(Ns.subs(point))
q_p= s.diff(law,pp).subs({vv:V_value,ww:W_value}).subs(slice_parameters).subs(point)

# A failure of critical compatibility and two theorem-domain negative cases.
flat_N=N.subs(pp,0).subs(slice_parameters).subs(point)
negative = {
    'flat_bed_N_at_same_water_state':str(flat_N),
    'c_zero_slope_discriminant':str(s.discriminant(slopes,z).subs(c,0)),
    'zero_eigenvalue_parameter':str(s.solve(s.Eq(det,0),c)[0]),
    'V_zero_angular_equation':str(angular.subs(V,0)),
    'G_zero_slope_pivot':str(s.diff(law,pp).subs(G,0)),
}
assert flat_N != 0
assert s.discriminant(slopes,z).subs(c,0)<0

data = {
 'status':'EXACT_REDUCTION_DERIVED_FROM_CURRENT_DETERMINING_AND_INVARIANT_CHAIN',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'sympy_version':s.__version__,
 'inputs':{'model':'h_t+div(hw)=0; w_t+(w.grad)w+g grad(h+B)+f Jw=0; B_t+div(q)=0',
  'class':'h=H(r), w=V(r)er+W(r)etheta, B=Z(r)+ct',
  'flux_semantics':'(Q,T) are the polar components of a rotation-equivariant q(h,w,gradB)',
  'unrestricted_complete_discovery':False,'reads_current_derived_graph':True,
  'historical_answers_read':False,
  'derived_graph_sha256':hashlib.sha256(invariant_file.read_bytes()).hexdigest(),
  'derived_graph_input':str(invariant_file)},
 'polar_pullback':{k:str(v) for k,v in pulled.items()},
 'flux_pullback':{'radial':str(radial_closure),
   'tangential':str(tangential_closure),
   'original_Exner_equals_defined_component_form':'0'},
 'integrating_factor':str(mu),'angular_linear_coefficient':str(a),
 'integrals':[str(I1),str(I2),str(I3)], 'independence_determinant':str(rank),
 'solved_balances':{'V':str(V_sol),'W':str(W_sol),'Q':str(Q_sol)},
 'undivided':{'D':str(D),'N_before_closure':str(N),'P_cubic':str(P),'N_cubic':str(N_cubic)},
 'critical_projection':{'D_H':'3*g','D_r':'2*g*H/r'},
 'family':{'fixed':'g=K=G=f=C1=C2=1; r*=H*=1','C3':str(C3_family),
  'Jacobian':[[str(a) for a in row] for row in J.tolist()],
  'determinant':str(det),'trace':str(s.trace(J)), 'saddle_condition':str(saddle),
  'slope_polynomial':str(slopes),'c_minus_7_slopes':[str(a) for a in example_slopes],
  'c_minus_7_eigenvalues':[str(a) for a in example_eigenvalues],
  'slope_pivot_at_point':str(q_p)},
 'negative_cases':negative,
 'guards':['r>0','H>0','C1!=0 (equivalently V!=0 here)',
   'selected local constitutive root with q_P!=0','D!=0 only for explicit normal form',
   'D=N=0 and det(J)<0 for the selected critical theorem'],
 'remaining_nonsymbolic_obligations':['proof via stable manifolds and converse germ argument',
   'independent Cartesian reconstruction','literature priority','physical applicability']
}
with OUT.open('x') as stream:json.dump(data,stream,indent=2);stream.write('\n')
print(json.dumps({'output':str(OUT),'status':data['status'],'saddle_condition':str(saddle)}))
