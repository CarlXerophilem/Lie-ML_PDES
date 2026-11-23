"""Independent reviewer receipts: no import of the reviewed implementation."""
import hashlib
import json
from pathlib import Path
import time

import sympy as s

start = time.perf_counter()
out = Path(__file__).resolve().parent
g, K = s.symbols('g K', positive=True)
m = s.symbols('m', real=True)
h, u, v, b = s.symbols('h u v b', real=True)
fields = (h, u, v, b)
jets = {f: s.symbols(f'{f}t {f}x {f}y', real=True) for f in fields}
ht, hx, hy = jets[h]
ut, ux, uy = jets[u]
vt, vx, vy = jets[v]
bt, bx, by = jets[b]
speed2 = u**2 + v**2
# On the explicitly assumed speed2>0 chart, collect one common real power.
# A first pass with separate powers hit a SymPy simplification false negative.
div = speed2**((m-1)/2)*((ux+vy) + (m-1)*(u*u*ux+u*v*(uy+vx)+v*v*vy)/speed2)
E = s.Matrix([ht+u*hx+v*hy+h*(ux+vy),
              ut+u*ux+v*uy+g*(hx+bx),
              vt+u*vx+v*vy+g*(hy+by), bt+K*div])
a, beta, c, d, e = s.symbols('a beta c d e', real=True)
weights = dict(zip(fields, (d, c, c, e)))
pr = lambda F: sum(weights[f]*f*s.diff(F,f) for f in fields) + sum(
    (weights[f]-q)*j*s.diff(F,j) for f in fields for q,j in zip((a,beta,beta),jets[f]))
alpha = a+c-beta
expected = s.Matrix([
    alpha*(u*hx+v*hy+h*(ux+vy)),
    alpha*(u*ux+v*uy)+g*(a+d-beta-c)*hx+g*(a+e-beta-c)*bx,
    alpha*(u*vx+v*vy)+g*(a+d-beta-c)*hy+g*(a+e-beta-c)*by,
    K*(a+m*c-beta-e)*div])
simp = lambda z: s.factor(s.simplify(s.expand(z)))
checks = {'general_diagonal_prolongation': [simp(pr(F)-q*F-T)
    for F,q,T in zip(E,(d-a,c-a,c-a,e-a),expected)]}
diag_solution = {beta:a+c, d:2*c, e:2*c}
remaining = simp((a+m*c-beta-e).subs(diag_solution))
checks['diagonal_remaining_condition'] = [simp(remaining-(m-3)*c)]

# At theta=0, basis differentiation gives u_y=-w/r and v_y=a/r.
# Isotropy extends this local calculation to every rotation angle.
r = s.symbols('r', positive=True)
ar,wr,hr,br,at,wt,ht0,bt0 = s.symbols('ar wr hr br at wt ht0 bt0', real=True)
aa,ww,hh = s.symbols('aa ww hh', real=True)
polar_jets = {h:hh,u:aa,v:ww,ht:ht0,hx:hr,hy:0,ut:at,ux:ar,uy:-ww/r,
              vt:wt,vx:wr,vy:aa/r,bt:bt0,bx:br,by:0}
Fspeed = (aa*aa+ww*ww)**((m-1)/2)
Fspeed_r = Fspeed*(m-1)*(aa*ar+ww*wr)/(aa*aa+ww*ww)
polar_expected = [ht0+aa*hr+hh*ar+hh*aa/r,at+aa*ar-ww*ww/r+g*(hr+br),
                  wt+aa*wr+aa*ww/r,bt0+K*(Fspeed*ar+aa*Fspeed_r+Fspeed*aa/r)]
checks['radial_equations_at_rotation_section'] = [simp(F.subs(polar_jets,simultaneous=True)-q) for F,q in zip(E,polar_expected)]

# Full seven-component commutator, including field coordinates.
t, x, y = s.symbols('t x y', real=True)
z = s.Matrix([t,x,y,h,u,v,b])
R = s.Matrix([0,-y,x,0,-v,u,0])
D = s.Matrix([0,x,y,2*h,u,v,2*b])
checks['full_rotation_scaling_commutator'] = list(D.jacobian(z)*R-R.jacobian(z)*D)

# Independent Cartesian conservative equations; the Exner residual is pore-inclusive.
H,A,W,B = [s.Function(n)(t) for n in ('H','A','W','B')]
b0 = s.symbols('b0', real=True)
r2 = x*x+y*y
depth, velx, vely, bed = H*r2,A*x-W*y,W*x+A*y,B*r2+b0
S = s.expand(velx**2+vely**2)
F = [s.diff(depth,t)+s.diff(depth*velx,x)+s.diff(depth*vely,y),
     s.diff(depth*velx,t)+s.diff(depth*velx**2+g*depth**2/2,x)+s.diff(depth*velx*vely,y)+g*depth*s.diff(bed,x),
     s.diff(depth*vely,t)+s.diff(depth*velx*vely,x)+s.diff(depth*vely**2+g*depth**2/2,y)+g*depth*s.diff(bed,y),
     s.diff(bed,t)+K*(s.diff(S*velx,x)+s.diff(S*vely,y))]
FH = s.diff(H,t)+4*A*H
FA = s.diff(A,t)+A*A-W*W+2*g*(H+B)
FW = s.diff(W,t)+2*A*W
FB = s.diff(B,t)+4*K*A*(A*A+W*W)
target = [r2*FH,velx*r2*FH+depth*(x*FA-y*FW),vely*r2*FH+depth*(y*FA+x*FW),r2*FB]
checks['conservative_cartesian_factorization'] = [simp(z-q) for z,q in zip(F,target)]
sub = {s.diff(H,t):-4*A*H,s.diff(A,t):W*W-A*A-2*g*(H+B),s.diff(W,t):-2*A*W,s.diff(B,t):-4*K*A*(A*A+W*W)}
checks['first_integrals'] = [simp(s.diff(W*W/H,t).subs(sub)),simp(s.diff(W/s.sqrt(H),t).subs(sub))]
omega = s.symbols('omega', real=True)
cstar = omega**2+s.Rational(1,4)
values = {H:cstar*(1/(2*g)-K)/t**2,A:1/(2*t),W:omega/t,B:K*cstar/t**2}
ds = {s.diff(z,t):s.diff(q,t) for z,q in values.items()}
checks['exact_family_original_conservative'] = [simp(z.subs(ds).subs(values)) for z in F]

# Derive annular integrals and boundary fluxes independently by integration.
r,ri,ro,p = s.symbols('r ri ro p', positive=True)
water_mass = s.integrate(2*s.pi*r*H*r*r,(r,ri,ro))
bed_mass = s.integrate(2*s.pi*r*(1-p)*(B*r*r+b0),(r,ri,ro))
water_flux = 2*s.pi*A*H*(ro**4-ri**4)
solid_flux = 2*s.pi*(1-p)*K*A*(A*A+W*W)*(ro**4-ri**4)
checks['annular_integrated_balances'] = [simp((s.diff(water_mass,t)+water_flux).subs(sub)),simp((s.diff(bed_mass,t)+solid_flux).subs(sub))]

pkg = out.parents[2]/'research_artifacts'/'SVE-2D-extension-20261014'
manifest = json.loads((pkg/'sources'/'source_manifest.json').read_text(encoding='utf-8'))
integrity = []
for paper in manifest['papers']:
    for version in paper.get('versions',[]):
        local = version.get('local_pdf')
        if local:
            actual = hashlib.sha256((pkg/local).read_bytes()).hexdigest()
            expected_hash = version['retrieval']['sha256']
            integrity.append({'file':local,'matches':actual==expected_hash,'sha256':actual})
saved = json.loads((pkg/'results'/'evidence.json').read_text(encoding='utf-8'))
replayed = json.loads((out/'evidence.json').read_text(encoding='utf-8'))
integrity += [{'file':'main.py','matches':hashlib.sha256((pkg/'main.py').read_bytes()).hexdigest()==saved['script_sha256']},
              {'file':'results/profiles.csv','matches':hashlib.sha256((pkg/'results'/'profiles.csv').read_bytes()).hexdigest()==saved['numerical']['sample_sha256']},
              {'file':'replay/profiles.csv','matches':replayed['numerical']['sample_sha256']==saved['numerical']['sample_sha256']}]
receipt = {'independent_of_main':True,'checks':{k:[str(z) for z in v] for k,v in checks.items()},
           'zero_count':sum(map(len,checks.values())),'integrity':integrity,
           'branch_assumptions':['u**2+v**2>0 for arbitrary real m','r>0','h>0','g,K>0'],
           'initial_run_note':'Two passes without expansion left algebraically equivalent speed powers uncombined by SymPy; both failed receipts are retained. Expansion before simplification resolves this on speed2>0 without changing any package file.',
           'all_passed':all(z==0 for values in checks.values() for z in values) and all(z['matches'] for z in integrity),
           'elapsed_seconds':time.perf_counter()-start}
(out/'independent_checks.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
assert receipt['all_passed']
