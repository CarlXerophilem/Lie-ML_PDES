"""Stage 2 equation registry: isotropic flux, evolving bed, constant Coriolis.

No maximality is supplied by this file. All continuous cells need a new
unrestricted determining-system integration and independent review.
"""
import sympy as sp
from main import JetSpace
from models import BRANCHES as ONE_DIMENSIONAL_CELLS, g, K, G, m, n

t,x,y=sp.symbols('t x y',real=True)
h=sp.Symbol('h',positive=True)
u,v,B=sp.symbols('u v B',real=True)
f=sp.Symbol('f',real=True,nonzero=True)

BRANCHES_2D={
    f'{name}_{rotation}':dict(cell,base_cell=name,coriolis=rotation,
                              guards=list(cell['guards']))
    for name,cell in ONE_DIMENSIONAL_CELLS.items()
    for rotation in ('f0','f_nonzero')
}
_slope_rotating=BRANCHES_2D.pop('slope_only_f_nonzero')
BRANCHES_2D['slope_only_generic_f_nonzero']=dict(_slope_rotating,
    guards=_slope_rotating['guards']+['n!=2'])
BRANCHES_2D['slope_only_n2_f_nonzero']=dict(_slope_rotating,n=sp.Integer(2),
    guards=_slope_rotating['guards']+['n=2'])


def branch_model_2d(name):
    cell=BRANCHES_2D[name]
    J=JetSpace((t,x,y),(h,u,v,B))
    speed_squared=u*u+v*v
    fv=sp.S.Zero if cell['coriolis']=='f0' else f
    velocity=(u,v)
    flux=[]
    for i,w in enumerate(velocity,1):
        transport=K*speed_squared**((sp.sympify(cell['m'])-1)/2)*w if cell['K'] else sp.S.Zero
        diffusion=G*speed_squared**(sp.sympify(cell['n'])/2)*J.jet(B,J.unit(i)) if cell['G'] else sp.S.Zero
        flux.append(transport-diffusion)
    mass=J.jet(h,(1,0,0))+J.D(h*u,1)+J.D(h*v,2)
    momentum=[]
    for a,w in enumerate(velocity,1):
        coriolis=-fv*v if a==1 else fv*u
        momentum.append(J.jet(w,(1,0,0))+u*J.D(w,1)+v*J.D(w,2)+g*J.D(h+B,a)+coriolis)
    bed=J.jet(B,(1,0,0))+J.D(flux[0],1)+J.D(flux[1],2)
    equations=(mass,*momentum,bed)
    parameters=(g,)+((K,) if cell['K'] else ())+((G,) if cell['G'] else ())
    parameters+=tuple(sorted(set().union(*(e.free_symbols for e in equations)) & {m,n,f},key=str))
    return dict(independent_variables=(t,x,y),dependent_fields=(h,u,v,B),
        equations=equations,parameters=parameters,
        branch_conditions={'model_id':'2d__'+name,
            'guards':['h>0','u**2+v**2>0','g>0', 'f=0' if fv==0 else 'f!=0']+cell['guards'],
            'substitutions':{},'registry_status':'awaiting_2d_necessity_integration_and_review'},
        data_case=None)


def recover_one_dimension(name):
    """At f=0, y-independent graphs with v=0 must reproduce the 1D PDE.

    At f!=0 the transverse equation retains f*u; that is a negative control,
    not a dimension-reduction equivalence.
    """
    from models import branch_model
    model=branch_model_2d(name)
    target=branch_model(BRANCHES_2D[name]['base_cell'])
    if name=='slope_only_n2_f_nonzero':
        target['equations']=tuple(e.subs(n,2) for e in target['equations'])
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    J1=JetSpace(target['independent_variables'],target['dependent_fields'])
    mapping={t:J1.x[0],x:J1.x[1],h:J1.u[0],u:J1.u[1],v:sp.S.Zero,B:J1.u[2]}
    for symbol,(a,index) in J.reverse.items():
        if not any(index):
            continue
        if a==2 or index[2]:
            mapping[symbol]=sp.S.Zero
        else:
            field_index={0:0,1:1,3:2}[a]
            mapping[symbol]=J1.jet(field_index,index[:2])
    reduced=tuple(sp.simplify(e.xreplace(mapping)) for e in model['equations'])
    differences=tuple(sp.simplify(reduced[a]-target['equations'][b])
                      for a,b in ((0,0),(1,1),(3,2)))
    return {'one_dimensional_residuals':differences,'transverse_residual':reduced[2],
            'recovered':all(value==0 for value in differences) and reduced[2]==0,
            'scope':'f=0, v=0, all y derivatives zero, positive-u representative chart'}
