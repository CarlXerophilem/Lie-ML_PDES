"""2D integration adapter: unrestricted proof first, basis extraction second."""
from pathlib import Path
import hashlib
import json
import sympy as sp
from radial_normal_form import normalize

HERE=Path(__file__).resolve().parent


def review_gate(receipt_path=None,root=HERE):
    from models_2d import BRANCHES_2D
    root=Path(root)
    path=Path(receipt_path) if receipt_path is not None else root/'classification_2d_review.json'
    if not path.exists():
        return {'passed':False,'reason':'independent_2d_classification_review_pending'}
    review=json.loads(path.read_text(encoding='utf-8'))
    hashes=review.get('inputs_sha256',{})
    required={'main.py','models.py','CONTRACT.md','models_2d.py','analyze_2d.py','classification_2d.py','radial_normal_form.py',
              'research_first_order_2d.py','research_slope_2d.py',
              'FIRST_ORDER_2D_DERIVATION.md','SLOPE_2D_DERIVATION.md',
              'review_classification_2d.py','CLASSIFICATION_2D_REVIEW.md'}
    if not required.issubset(hashes):
        return {'passed':False,'reason':'missing_reviewed_input_hashes'}
    changed=[name for name,digest in hashes.items() if not (root/name).is_file()
             or hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest]
    if changed:
        return {'passed':False,'reason':'reviewed_inputs_changed','changed':changed}
    branches=review.get('branches',{})
    verdicts=review.get('verdicts',{})
    accepted=(review.get('all_checks_passed') is True and set(branches)==set(BRANCHES_2D)
              and all(row.get('passed') is True for row in branches.values())
              and all(verdicts.get(key,'').startswith('accepted') for key in ('first_order','slope','root_analyzer')))
    return {'passed':accepted,'reason':'reviewed_exact_version' if accepted else 'review_not_accepted',
            'receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'scope':'all 17 declared 2D local smooth point algebras on h>0, u^2+v^2>0'}


def integrate_sve_2d(report):
    from models_2d import BRANCHES_2D,branch_model_2d
    from main import JetSpace,verify_generator,algebra_structure
    name=report['model_id'].removeprefix('2d__')
    if name not in BRANCHES_2D:
        return {'status':'unresolved','reason':'No unrestricted necessity certificate for this input'}
    expected=branch_model_2d(name)
    if (tuple(report['coordinates'])!=expected['independent_variables']
            or tuple(report['fields'])!=expected['dependent_fields']
            or tuple(report['parameters'])!=expected['parameters']
            or report['branch_conditions']!=expected['branch_conditions']
            or len(report['equations'])!=len(expected['equations'])
            or any(sp.expand(a-b)!=0 for a,b in zip(report['equations'],expected['equations']))):
        return {'status':'unresolved','reason':'Model/guard fingerprint differs from certificate'}
    if BRANCHES_2D[name]['G']:
        from research_slope_2d import general_solution
        proof='SLOPE_2D_DERIVATION.md'
        proof_code='research_slope_2d.py'
    else:
        from research_first_order_2d import general_solution
        proof='FIRST_ORDER_2D_DERIVATION.md'
        proof_code='research_first_order_2d.py'
    coordinates=tuple(report['coordinates'])+tuple(report['fields'])
    solved=general_solution(name,coordinates=coordinates)
    coefficients=tuple(solved['coefficients'])
    constants=tuple(solved['free_constants'])
    arbitrary=tuple(report['arbitrary_generator']['xi'])+tuple(report['arbitrary_generator']['eta'])
    substitution=dict(zip(arbitrary,coefficients))
    derivative_substitution={derivative:sp.diff(substitution[derivative.expr],*derivative.variables)
        for equation in report['determining_equations'] for derivative in equation.atoms(sp.Derivative)
        if derivative.expr in substitution}
    substitution.update(derivative_substitution)
    u,v=report['fields'][1:3]
    remainders=[normalize(e.xreplace(substitution),u,v) for e in report['determining_equations']]
    if any(e!=0 for e in remainders):
        return {'status':'failed','reason':'General solution failed raw determining equations','remainders':remainders}
    basis=[tuple(sp.diff(e,c) for e in coefficients) for c in constants]
    J=JetSpace(report['coordinates'],report['fields'])
    checks=[verify_generator(J,report['equations'],q[:3],q[3:]) for q in basis]
    for check in checks:
        check['before_radial_normalization']=check['residuals']
        check['residuals']=[normalize(value,u,v) for value in check['residuals']]
        check['verified']=all(value==0 for value in check['residuals'])
        check['normalization_domain']='u**2+v**2>0; exact integer shifts of one real-power base'
    if not all(check['verified'] for check in checks):
        return {'status':'failed','reason':'Independent recursive sufficiency failed','checks':checks}
    gate=review_gate()
    return {'status':'proved_for_declared_regular_chart' if gate['passed'] else 'necessity_integrated_pending_review',
            'review_gate':gate,'general_solution':coefficients,'free_constants':constants,
            'constant_equations':solved.get('constant_equations',solved.get('constraints',())),
            'basis':basis,'dimension':len(basis),'raw_DE_remainders':remainders,
            'candidate_checks':checks,'necessity_proof':proof,
            'necessity_proof_sha256':hashlib.sha256((HERE/proof).read_bytes()).hexdigest(),
            'proof_verifier':proof_code,'proof_verifier_sha256':hashlib.sha256((HERE/proof_code).read_bytes()).hexdigest(),
            'maximality_basis':'unrestricted necessary-equation integration and sufficient substitution',
            'algebra':algebra_structure(coordinates,basis),'equivalence_completeness':'separate_unresolved_question'}
