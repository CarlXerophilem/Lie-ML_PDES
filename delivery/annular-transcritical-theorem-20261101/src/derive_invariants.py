"""Derive the quotient from a selected subalgebra of computed generators.

The selection is made AFTER determining shared affine point symmetries.
Linear/quadratic invariants are solved for with unknown coefficients. None
of the target invariants or field profiles is supplied to the nullspace solve.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'results/shared-affine-symmetries.json'
data=json.loads(source.read_text())
t,x,y,h,u,v,B=s.symbols('t x y h u v B',real=True)
c=s.symbols('c',real=True)
coords=(t,x,y,h,u,v,B)
local={str(a):a for a in coords}
basis=[s.Matrix([s.sympify(a,locals=local) for a in row]) for row in data['basis']]

# Choice of subalgebra from the already computed list, not an input generator.
# These indices are pinned to the readable determining result checked below.
time,rotation,bed=basis[0],basis[3],basis[4]
assert list(time)==[1,0,0,0,0,0,0]
assert list(bed)==[0,0,0,0,0,0,1]
M=rotation.jacobian(coords)
spatial=M.extract([1,2],[1,2]); velocity=M.extract([4,5],[4,5])
assert spatial+spatial.T==s.zeros(2) and spatial.det()!=0 and velocity==spatial
assert rotation[0]==rotation[3]==rotation[6]==0
relative=time+c*bed
act=lambda X,a:s.expand(sum(X[i]*s.diff(a,q) for i,q in enumerate(coords)))
bracket=[s.simplify(act(rotation,relative[i])-act(relative,rotation[i])) for i in range(7)]
assert bracket==[0]*7
solve_ledger=[]

def polynomial_invariants(variables,degree,X):
    monomials=sorted((a for a in s.itermonomials(variables,degree)
                       if s.total_degree(a)==degree),key=s.default_sort_key)
    a=s.symbols('k0:'+str(len(monomials)))
    trial=sum(q*m for q,m in zip(a,monomials))
    equations=s.Poly(act(X,trial),*coords).coeffs()
    mat,_=s.linear_eq_to_matrix(equations,a)
    kernel=mat.nullspace()
    solve_ledger.append({'monomials':[str(q) for q in monomials],
        'matrix':[[str(q) for q in row] for row in mat.tolist()],
        'kernel':[[str(q) for q in vector] for vector in kernel],
        'parameter_dependent_pivots':False})
    assert not mat.free_symbols
    return [s.expand(sum(q*m for q,m in zip(vector,monomials)))
             for vector in kernel]

linear=polynomial_invariants(coords,1,rotation)
quadratic=polynomial_invariants((x,y,u,v),2,rotation)
base=[a for a in quadratic if a.free_symbols <= {x,y}]
assert len(base)==1
radius_squared=s.expand(base[0]/base[0].coeff(x,2))
mixed=[a for a in quadratic if s.Poly(a,u,v).total_degree()==1
       and s.Poly(a,x,y).total_degree()==1]
radial_raw=next(a for a in mixed if a.coeff(x*u)!=0)
radial_raw=s.expand(radial_raw/radial_raw.coeff(x*u))
angular_raw=next(a for a in mixed if a.coeff(x*v)!=0)
angular_raw=s.expand(angular_raw/angular_raw.coeff(x*v))
pure_velocity=next(a for a in quadratic if a.free_symbols<={u,v})
pure_velocity=s.expand(pure_velocity/pure_velocity.coeff(u,2))
assert s.expand(radius_squared*pure_velocity-radial_raw**2-angular_raw**2)==0

# Choose t before B to use the permanent unit pivot. Generic RREF of the
# reversed columns can divide by c, silently omitting c=0 in its derivation.
# Here the determining row is [1,c]; both c=0 and c!=0 are covered at once.
bt,bB=s.symbols('b_t b_B')
time_constraint=act(relative,bt*t+bB*B)
time_matrix,_=s.linear_eq_to_matrix([time_constraint],[bt,bB])
assert time_matrix[0,0]==1
time_kernel=time_matrix.nullspace()
time_bed=[s.expand(q[0]*t+q[1]*B) for q in time_kernel]
solve_ledger.append({'monomials':['t','B'],
    'matrix':[[str(q) for q in row] for row in time_matrix.tolist()],
    'kernel':[[str(q) for q in vector] for vector in time_kernel],
    'pivot':'1 in the t column; no division by c',
    'parameter_strata':'all real c, including c=0'})
assert len(time_bed)==1
bed_invariant=s.expand(time_bed[0]/time_bed[0].coeff(B))
assert h in linear and act(relative,h)==0
for invariant in [radius_squared,radial_raw,angular_raw,h,bed_invariant]:
    assert act(rotation,invariant)==0 and act(relative,invariant)==0

# Choose the positive radius and an orbit slice y=0,x=r. The exact group flow
# generates adapted coordinates; field graphs become arbitrary functions of r.
eps=s.symbols('epsilon',real=True)
r=s.symbols('r',positive=True)
H,V,W,Z=s.symbols('H V W Z',real=True)
flow=s.exp(eps*M)
forward=flow*s.Matrix([t,r,0,H,V,W,Z+c*t])
adapted=(t,r,eps,H,V,W,Z)
jac=s.trigsimp(forward.jacobian(adapted).det())
assert jac!=0
sol=s.solve([s.Eq(radial_raw,r*V),s.Eq(angular_raw,r*W)],(u,v),dict=True)[0]
sol={str(q):s.factor(a).subs(radius_squared,r*r) for q,a in sol.items()}
bed_sol=s.solve(s.Eq(bed_invariant,Z),B)[0]
profiles={H:s.Function('H')(r),V:s.Function('V')(r),W:s.Function('W')(r),Z:s.Function('Z')(r)}
forms={'h':str(H.subs(profiles)),'u':str(s.simplify(sol['u']).subs(profiles)),
       'v':str(s.simplify(sol['v']).subs(profiles)),'B':str(bed_sol.subs(profiles))}
result={
 'status':'INVARIANTS_AND_GRAPH_RECONSTRUCTION_DERIVED_FROM_DETERMINED_GENERATORS',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_result_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'selected_indices':{'time':0,'rotation':3,'bed_translation':4},
 'selection_boundary':'A useful subalgebra is chosen from returned generators; no optimal-subalgebra classification is asserted.',
 'rotation':[str(a) for a in rotation],'relative_time':[str(a) for a in relative],
 'bracket':[str(a) for a in bracket],'linear_invariants':[str(a) for a in linear],
 'invariant_solve_ledger':solve_ledger,
 'quadratic_invariants':[str(a) for a in quadratic],
 'radius_squared':str(radius_squared),'radial_numerator':str(radial_raw),
 'angular_numerator':str(angular_raw),'bed_invariant':str(bed_invariant),
 'radius_choice':'r=sqrt(radius_squared)>0',
 'adapted_coordinate_map':[str(a) for a in forward],
 'adapted_coordinate_jacobian':str(jac),
 'graph_forms':forms,
 'arbitrary_functions':['H(r)','V(r)','W(r)','Z(r)'],
 'guards':['r>0; axis is a separate orbit-rank stratum','joint base and total orbit rank both equal two'],
 'not_claimed':['preservation of arbitrary boundaries/data','maximal Lie algebra','optimal-subalgebra completeness']}
payload=json.dumps(result,indent=2)+'\n'
with (ROOT/'results/derived-invariants.json').open('x') as stream:stream.write(payload)
print(json.dumps({'graph_forms':forms,'Jacobian':str(jac)},indent=2))
