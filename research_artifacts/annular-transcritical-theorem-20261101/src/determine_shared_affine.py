"""Determine parameter-independent shared affine point symmetries from PDEs.

Inputs: the original evolution equations, positive g,K,G,f parameter family,
and the full affine coefficient space on (t,x,y,h,u,v,B). No generator,
invariant, profile ansatz, first integral, or historical answer is imported.
The finite coefficient class is explicit: this is NOT maximal point symmetry
classification of a fixed-parameter PDE in arbitrary smooth functions.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import sympy as s

OUT=Path(__file__).resolve().parents[1]/'results'
t,x,y=s.symbols('t x y',real=True)
g,K,G,f=s.symbols('g K G f',positive=True)
parameters=(g,K,G,f)
names=('h','u','v','B')
jets={}
indices={}
for field,name in enumerate(names):
    for degree in range(5):
        for i in range(degree+1):
            j=degree-i
            symbol=s.Symbol(name if degree==0 else name+'_'+str(i)+str(j),real=True)
            jets[field,i,j]=symbol
            indices[symbol]=(field,i,j)
h,u,v,B=(jets[a,0,0] for a in range(4))
coordinates=(t,x,y,h,u,v,B)

def total(expr,axis):
    result=s.diff(expr,(x,y)[axis])
    for symbol in expr.free_symbols & indices.keys():
        a,i,j=indices[symbol]
        key=(a,i+1,j) if axis==0 else (a,i,j+1)
        if key not in jets:
            raise ValueError('Jet order insufficient: '+str(key))
        result+=s.diff(expr,symbol)*jets[key]
    return s.expand(result)

S=u*u+v*v
qx=K*S*u-G*S*jets[3,1,0]
qy=K*S*v-G*S*jets[3,0,1]
F=(
 -total(h*u,0)-total(h*v,1),
 -u*jets[1,1,0]-v*jets[1,0,1]-g*(jets[0,1,0]+jets[3,1,0])+f*v,
 -u*jets[2,1,0]-v*jets[2,0,1]-g*(jets[0,0,1]+jets[3,0,1])-f*u,
 -total(qx,0)-total(qy,1))

@lru_cache(None)
def differentiated_rhs(a,i,j):
    value=F[a]
    for _ in range(i):value=total(value,0)
    for _ in range(j):value=total(value,1)
    return value

def time_total(expr):
    result=s.diff(expr,t)
    for symbol in expr.free_symbols & indices.keys():
        result+=s.diff(expr,symbol)*differentiated_rhs(*indices[symbol])
    return s.expand(result)

unknown=s.symbols('a0:56')
affine_basis=(s.Integer(1),)+coordinates
coefficients=[sum(unknown[8*i+j]*a for j,a in enumerate(affine_basis)) for i in range(7)]
tau,xi,yi=coefficients[:3]
eta=coefficients[3:]
Q=[s.expand(eta[a]-tau*F[a]-xi*jets[a,1,0]-yi*jets[a,0,1]) for a in range(4)]

@lru_cache(None)
def differentiated_characteristic(a,i,j):
    value=Q[a]
    for _ in range(i):value=total(value,0)
    for _ in range(j):value=total(value,1)
    return value

conditions=[]
for a in range(4):
    linearized=0
    for symbol in F[a].free_symbols & indices.keys():
        linearized+=s.diff(F[a],symbol)*differentiated_characteristic(*indices[symbol])
    condition=s.expand(time_total(Q[a])-linearized)
    conditions.append(condition)
    print('determining component',names[a],'terms',len(s.Add.make_args(condition)),flush=True)

# Splitting the physical parameters is justified here ONLY because the task is
# the shared, parameter-independent coefficient class on an open positive
# parameter set. It is not a fixed-parameter completeness calculation.
split_variables=(t,x,y)+tuple(jets.values())+parameters
rows=set()
for condition in conditions:
    for coefficient in s.Poly(condition,*split_variables).coeffs():
        pieces=s.expand(coefficient).as_coefficients_dict()
        if any(term not in unknown for term in pieces):
            raise ValueError('A determining coefficient is not homogeneous linear')
        row=tuple(s.Rational(pieces.get(a,0)) for a in unknown)
        scale=s.ilcm(*[a.q for a in row])
        integers=tuple(int(scale*a) for a in row)
        divisor=math.gcd(*integers)
        integers=tuple(a//divisor for a in integers)
        first=next(a for a in integers if a)
        if first<0:integers=tuple(-a for a in integers)
        rows.add(integers)
rows=sorted(rows)
matrix=s.Matrix(rows)
rref,pivots=matrix.rref()
kernel=matrix.nullspace()
vectors=[]
for column in kernel:
    substitution=dict(zip(unknown,column))
    vector=[s.expand(a.subs(substitution,simultaneous=True)) for a in coefficients]
    assert matrix*column==s.zeros(matrix.rows,1)
    # Independent substitution into the unsplit determining expressions.
    assert all(s.expand(a.subs(substitution,simultaneous=True))==0 for a in conditions)
    vectors.append([str(a) for a in vector])

data={
 'status':'NECESSARY_AND_SUFFICIENT_IN_SHARED_PARAMETER_INDEPENDENT_AFFINE_CLASS',
 'not_a_maximal_fixed_parameter_classification':True,
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'variables':[str(a) for a in coordinates],
 'model_parameters':{'g':'>0','K':'>0','G':'>0','f':'>0'},
 'equations_Ut_equals_F':{names[a]:str(F[a]) for a in range(4)},
 'coefficient_class':'Each of the seven point coefficients is an arbitrary affine function of all seven coordinates; 56 independent constants shared over the open positive parameter family.',
 'determining_identity':'D_t(Q)-ell_F(Q)=0 on all differential consequences of U_t=F, Q=eta-tau*F-xi*Ux-zeta*Uy.',
 'maximum_spatial_jet_order':4,
 'parameter_split_reason':'Coefficients are parameter-independent and required to work on the full open positive parameter set. No fixed-parameter completeness follows.',
 'unknowns':[str(a) for a in unknown],
 'matrix_rows':rows,'rank':len(pivots),'pivot_columns':list(pivots),
 'rref':[[str(a) for a in row] for row in rref.tolist()],
 'basis':vectors,'basis_dimension':len(vectors),
 'guards_and_limits':['No parameter-dependent division in this rational linear system.',
   'Zero rows and free columns are retained by exact RREF.',
   'No original PDE residual was replaced by an unrelated symbol.',
   'Non-affine and parameter-specific extra point symmetries remain unclassified.',
   'No invariant solution class or first integral is an input.']}
with (OUT/'shared-affine-symmetries.json').open('x') as stream:json.dump(data,stream,indent=2);stream.write('\n')
with (OUT/'unsplit-determining-equations.json').open('x') as stream:
    json.dump({'variables':data['variables'],'coefficients':[str(a) for a in coefficients],
      'Q':[str(a) for a in Q],'D_tQ_minus_ell_FQ':[str(a) for a in conditions],
      'jet_coordinates':{str(a):list(b) for a,b in indices.items()}},stream,indent=2);stream.write('\n')
print(json.dumps({'rank':len(pivots),'dimension':len(vectors),'basis':vectors},indent=2))
