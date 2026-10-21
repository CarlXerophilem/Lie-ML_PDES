"""Integrate the declared SVE systems using their explicit necessity proofs.

The recipes are model-specific integrations of arbitrary-function determining
systems, not an affine search presented as general discovery. An unrecognized
PDE retains its raw determining equations and an unresolved integration status.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent


def integrate_sve(report):
    from models import BRANCHES, branch_model
    from main import JetSpace, verify_generator, algebra_structure
    name = report['model_id']
    if name not in BRANCHES:
        return {'status': 'unresolved', 'reason': 'No integrated necessity certificate for this input'}
    expected = branch_model(name)
    if (tuple(report['coordinates']) != expected['independent_variables']
            or tuple(report['fields']) != expected['dependent_fields']
            or tuple(report['parameters']) != expected['parameters']
            or report['branch_conditions'] != expected['branch_conditions']
            or len(report['equations']) != len(expected['equations'])
            or any(sp.expand(a-b) != 0 for a,b in zip(report['equations'],expected['equations']))):
        return {'status': 'unresolved', 'reason': 'Model/guard fingerprint differs from certificate'}
    coordinates = tuple(report['coordinates']) + tuple(report['fields'])
    if BRANCHES[name]['G']:
        from research_slope import general_solution
        cell = BRANCHES[name]
        solved = general_solution(name, coordinates=coordinates,
                                  exponent=cell['m'] if cell['K'] else cell['n'])
        proof = 'SLOPE_DERIVATION.md'
        proof_code = 'research_slope.py'
    else:
        from research_first_order import general_solution
        solved = general_solution(name, coordinates=coordinates)
        proof = 'FIRST_ORDER_DERIVATION.md'
        proof_code = 'research_first_order.py'
    coefficients = tuple(solved['coefficients'])
    constants = tuple(solved['free_constants'])
    arbitrary = tuple(report['arbitrary_generator']['xi']) + tuple(report['arbitrary_generator']['eta'])
    substitution = dict(zip(arbitrary, coefficients))
    remainders = [sp.simplify(e.subs(substitution, simultaneous=True).doit())
                  for e in report['determining_equations']]
    if any(e != 0 for e in remainders):
        return {'status': 'failed', 'reason': 'Integrated solution failed a raw determining equation',
                'remainders': remainders}
    basis = [tuple(sp.diff(e,c) for e in coefficients) for c in constants]
    space = JetSpace(report['coordinates'], report['fields'])
    checks = [verify_generator(space, report['equations'], vector[:len(space.x)],
                              vector[len(space.x):]) for vector in basis]
    if not all(check['verified'] for check in checks):
        return {'status': 'failed', 'reason': 'Independent recursive sufficiency failed', 'checks':checks}
    gate = review_gate()
    return {
        'status': ('proved_for_declared_regular_chart' if gate['passed']
                   else 'necessity_integrated_pending_review'),
        'review_gate': gate,
        'general_solution': coefficients, 'free_constants': constants,
        'basis': basis, 'dimension': len(basis), 'raw_DE_remainders': remainders,
        'candidate_checks': checks, 'necessity_proof': proof,
        'necessity_proof_sha256': hashlib.sha256((HERE/proof).read_bytes()).hexdigest(),
        'proof_verifier': proof_code,
        'proof_verifier_sha256': hashlib.sha256((HERE/proof_code).read_bytes()).hexdigest(),
        'maximality_basis': 'unrestricted necessary-equation integration plus sufficient substitution',
        'algebra': algebra_structure(coordinates,basis),
        'equivalence_completeness': 'separate_gate',
    }


def review_gate(receipt_path=None, root=HERE):
    """No inference from historical counts or a reviewer file's mere existence."""
    root=Path(root)
    path = Path(receipt_path) if receipt_path is not None else root/'classification_review.json'
    if not path.exists():
        return {'passed':False,'reason':'independent_classification_review_pending'}
    review = json.loads(path.read_text(encoding='utf-8'))
    required={'grass_generic','grass_cubic','zero_transport','slope_attachment_generic',
              'slope_attachment_cubic','slope_source_generic','slope_source_cubic','slope_only'}
    verdicts=review.get('verdicts',{})
    hashes=review.get('inputs_sha256',{})
    required_files={'main.py','classification.py','models.py','research_first_order.py','research_slope.py',
                    'FIRST_ORDER_DERIVATION.md','SLOPE_DERIVATION.md','review_classification.py',
                    'CLASSIFICATION_REVIEW.md','CONTRACT.md'}
    if not required_files.issubset(hashes):
        return {'passed':False,'reason':'missing_reviewed_input_hashes'}
    changed=[name for name,digest in hashes.items() if not (root/name).is_file()
             or hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest]
    if changed:
        return {'passed':False,'reason':'reviewed_inputs_changed','changed':changed}
    accepted=(review.get('all_checks_passed') is True and set(review.get('branches',{}))==required
              and all(v.get('passed') is True for v in review['branches'].values())
              and verdicts.get('first_order','').startswith('accepted')
              and verdicts.get('slope','').startswith('accepted')
              and verdicts.get('root_analyzer','').startswith('accepted'))
    return {'passed':accepted,'reason':'reviewed_exact_version' if accepted else 'review_not_accepted',
            'receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'scope':'eight local positive-chart Lie point algebras; not full point-equivalence groupoid'}
