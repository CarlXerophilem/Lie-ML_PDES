"""Post-CAS source comparison using characteristic integration, not stored graphs.

The source selects nine subgroups only after the arbitrary-coefficient CAS solve.
This helper handles diagonal affine actions discovered in that solve. It does
not impose an affine ansatz on unknown symmetry coefficients.
"""
from pathlib import Path
import hashlib
import argparse
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import sympy as sp
from symm.LieSymm.core import JetSpace,verify_generator,json_ready,multi_indices
from symm.LieSymm.strict import parse_liepde_output,_reduce_names,liepde_script,_chart_simplify
from scripts.run_strict_lie import model,atomic_json
from scripts.summarize_strict_lie import coefficient_matrix
from scripts.revalidate_strict_receipts import revalidate_receipt


def derive_affine_characteristics(space,equation,generator,*,positive_jet_chart=False):
    """Integrate dx/ds=Ax+b and du/ds=Cu+d; accept no supplied invariant/profile."""
    if len(space.x)!=2 or len(space.u)!=1:
        raise ValueError('This post-solve characteristic chart is scalar 1+1 only')
    xi=tuple(map(sp.sympify,generator[:2]));eta=sp.sympify(generator[2]);u=space.u[0]
    check=verify_generator(space,(equation,),xi,(eta,))
    if not check['verified']:
        return dict(category='generator_not_admitted',residuals=check['residuals'])
    if all(v==0 for v in xi):
        if eta==0:
            return dict(category='identity_action',invariant_surface_equation=sp.S.Zero)
        return dict(category='no_invariant_graph' if eta.is_zero is False or eta.is_number else 'vertical_constraint',
                    invariant_surface_equation=eta)
    affine=[]
    for coordinate,coefficient in zip(space.x,xi):
        a=sp.diff(coefficient,coordinate);b=sp.simplify(coefficient-a*coordinate)
        if a.has(*space.x,u) or b.has(*space.x,u):
            raise ValueError('Action is not diagonal affine; characteristic solver unavailable')
        affine.append((a,b))
    c=sp.diff(eta,u);d=sp.simplify(eta-c*u)
    if c.has(*space.x,u) or d.has(*space.x,u):
        raise ValueError('Field action is not affine in its own field')
    pivot=next(i for i,v in enumerate(xi) if v != 0)
    other=1-pivot;p=space.x[pivot];x=space.x[other]
    tau=sp.integrate(1/xi[pivot],p)
    if tau.has(sp.Integral,sp.Piecewise):
        return dict(category='unresolved_characteristic_integral',integral=tau)
    a,b=affine[other]
    invariant=sp.simplify((x+b/a)*sp.exp(-a*tau) if a != 0 else x-b*tau)
    r=sp.Symbol('strict_orbit',positive=True)
    z=sp.Symbol('strict_invariant',real=True)
    tau_r=tau.subs(p,r)
    profile=sp.Function('strict_profile')(z)
    # General solution of the linear field characteristic equation.
    field_chart=sp.simplify(sp.exp(c*tau_r)*profile-d/c if c != 0 else profile+d*tau_r)
    graph=sp.simplify(field_chart.subs({r:p,z:invariant},simultaneous=True))
    q=sp.simplify(eta.subs(u,graph)-sum(v*sp.diff(graph,xv) for v,xv in zip(xi,space.x)))
    inverse_other=sp.solve(sp.Eq(invariant.subs(p,r),z),x)
    if len(inverse_other)!=1:
        return dict(category='unresolved_inverse_chart',invariant=invariant)
    inverse={p:r,x:inverse_other[0]}
    jacobian=sp.factor(sp.Matrix((p,invariant)).jacobian(space.x).det())
    dz=[sp.simplify(sp.diff(invariant,xv).subs(inverse,simultaneous=True)) for xv in space.x]
    def coordinate_derivative(value,axis):
        return sp.simplify((sp.diff(value,r) if axis==pivot else 0)+dz[axis]*sp.diff(value,z))
    order=space.order((equation,))
    coordinate_jets={(0,0):field_chart}
    for index in multi_indices(2,order):
        if not any(index):continue
        axis=next(i for i,n in enumerate(index) if n)
        previous=tuple(n-int(i==axis) for i,n in enumerate(index))
        coordinate_jets[index]=coordinate_derivative(coordinate_jets[previous],axis)
    rules={space.jet(0,index):value for index,value in coordinate_jets.items()}
    denominator=sp.simplify(sp.denom(sp.together(equation)).subs(inverse,simultaneous=True).xreplace(rules))
    basic=dict(generator=generator,characteristic_time=tau,invariant=invariant,field_characteristic=(c,d),
               graph=graph,profile=profile,Q=q,inverse_coordinates=inverse,coordinate_jacobian=jacobian,
               coordinate_guards=[sp.Ne(xi[pivot],0),sp.Ne(jacobian,0)],
               orbit_chart_guard=sp.Gt(p,0),
               coefficient_guards=([sp.Ne(a,0)] if a != 0 else [])+([sp.Ne(c,0)] if c != 0 else [])
                                  +([sp.Ne(affine[pivot][0],0)] if affine[pivot][0] != 0 else [])
                                  +[sp.Ne(sp.denom(sp.together(tau)),0)],
               real_log_guards=[sp.Gt(log.args[0],0) for log in tau.atoms(sp.log)])
    if denominator==0:
        return {**basic,'category':'undefined_PDE_chart','PDE_denominator':denominator}
    pullback=sp.factor(equation.subs(inverse,simultaneous=True).xreplace(rules))
    direct={space.jet(0,index):(sp.diff(graph,*sum(([v]*n for v,n in zip(space.x,index)),[])) if any(index) else graph)
            for index in multi_indices(2,order)}
    independent=sp.simplify(equation.xreplace(direct).subs(inverse,simultaneous=True).doit())
    difference=sp.simplify(independent-pullback)
    if pullback==0:
        reduced,multiplier,category=sp.S.Zero,sp.S.One,'identity_family'
    else:
        reduced,multiplier=pullback.as_independent(r,as_Add=False)
        category='implicit_ODE_DAE' if not multiplier.has(z) else 'unresolved_orbit_dependence'
    velocity=coordinate_jets.get((1,0),coordinate_derivative(field_chart,0))
    gradient=coordinate_jets.get((0,1),coordinate_derivative(field_chart,1))
    if positive_jet_chart and velocity != 0 and gradient != 0:
        difference=_chart_simplify(difference,[velocity,gradient])
    return {**basic,'category':category,'PDE_denominator':denominator,'undivided_pullback':pullback,
            'reduced_equation':reduced,'orbit_multiplier':multiplier,
            'multiplier_guard':sp.Ne(multiplier,0),'reconstruction_residual':difference,
            'velocity':velocity,'gradient':gradient,'positive_velocity_guard':sp.Gt(velocity,0),
            'positive_gradient_guard':sp.Gt(gradient,0),
            'positive_jet_chart_used_for_powers':positive_jet_chart,
            'positive_chart_excluded':velocity==0 or gradient==0,
            'verified_identity':q==0 and difference==0}


def select_source_branch(definition, receipt):
    report=revalidate_receipt(definition,receipt)
    eligible=[(i,b) for i,b in enumerate(report['cas_solution']['branches'])
              if not any(p in b['assignments'] for p in definition['parameters'])
              and report['independent_checks'][i].get('verified')]
    if len(eligible)!=1:raise ValueError('Unique checked unspecialized source branch required')
    index,branch=eligible[0]
    return report,index,branch


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stratum',choices=('general','1','3'),default='3')
    parser.add_argument('--source',type=Path,default=ROOT/'build/final-20261027/revalidated-reviewed')
    parser.add_argument('--out',type=Path,default=ROOT/'build/final-20261027/selected-reviewed')
    args=parser.parse_args()
    out=args.out;out.mkdir(parents=True,exist_ok=True)
    receipt_path=args.source/f'P--{args.stratum}-60.json'
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    definition=model('P:'+args.stratum);j=JetSpace(definition['independent_variables'],definition['dependent_fields'])
    report,branch_index,solved=select_source_branch(definition,receipt)
    names=_reduce_names((*j.x,*j.u,*definition['parameters']))
    keys=[sp.Symbol('xi_'+names[x]) for x in j.x]+[sp.Symbol('eta_'+names[j.u[0]])]
    free=[c for c in solved['free'] if c not in definition['parameters']]
    basis=[tuple(sp.diff(solved['assignments'][k],c) for k in keys) for c in free]
    # Post-solve comparison selectors only. No catalogue graph/reduction API is used.
    from symm.LieSymm.scalar2026 import catalog
    mapping={catalog.t:j.x[0],catalog.s:j.x[1],catalog.PHI:j.u[0]}
    rows=[]
    for selector in catalog.representatives()[:9]:
        vector=tuple(sp.sympify(v).subs(mapping) for v in selector['generator'])
        matrix=coefficient_matrix([*basis,vector],(*j.x,*j.u))
        try:
            weights,arbitrary=matrix[:,:-1].gauss_jordan_solve(matrix[:,-1])
        except ValueError:
            rows.append(dict(source_subsection=selector['id'],category='source_generator_not_in_returned_span'))
            continue
        weights=weights.subs({v:0 for v in arbitrary})
        membership=[sp.simplify(v-sum(weights[k]*basis[k][a] for k in range(len(basis)))) for a,v in enumerate(vector)]
        if any(v!=0 for v in membership):raise ValueError('Source subgroup is outside solved CAS span')
        row=derive_affine_characteristics(j,definition['equations'][0],vector,positive_jet_chart=True)
        row.update(source_subsection=selector['id'],cas_combination_weights=list(weights),membership_residual=membership,
                   inherited_branch_guards=report['independent_checks'][branch_index]['guard_checks'],
                   membership_denominators=[sp.denom(sp.factor(w)) for w in weights])
        rows.append(row)
    suffix='' if args.stratum=='3' else '-'+args.stratum
    atomic_json(out/('scalar-nine-characteristic-chains'+suffix+'.json'),json_ready(dict(status='partial',exponent=args.stratum,
        scope='Nine source-selected subgroup chains after CAS solve; not exhaustive strata or all subalgebras',
        source_receipt_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
        input_sha256=report['input_sha256'],selected_branch_index=branch_index,
        inherited_branch_guards=report['independent_checks'][branch_index]['guard_checks'],
        execution_kind='historical_output_revalidation',
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=rows)))
    print([(row['source_subsection'],row['category']) for row in rows])


if __name__=='__main__':main()
