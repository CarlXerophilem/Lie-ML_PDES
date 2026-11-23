"""Release gate for the finite conditional search and checked ML input export."""
from collections import Counter
import json
from pathlib import Path

from gatekeeper import check_gate,digest,check_hashes
from nonclassical_runner import load_registry,FROZEN_REGISTRY_SHA256
from stage2_runner import source_hashes
from run_all import source_hashes as validation_source_hashes

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
STATUSES={'verified_conditional_on_declared_chart',
          'verified_conditional_on_regular_subchart','failed_conditional_criterion'}


def _inside(path):
    path=Path(path).resolve()
    if not path.is_relative_to(HERE):
        raise ValueError('Stage 3 evidence must belong to this cycle')
    return path


def _read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def assess(branch_run,validation_run,review_path):
    registry,gates=load_registry()
    branch_run,validation_run,review_path=map(_inside,(branch_run,validation_run,review_path))
    run=_read(branch_run/'receipts.json')
    validation=_read(validation_run/'receipts.json')
    review=_read(review_path)
    if (not run.get('execution_passed') or run.get('candidate_count')!=64
            or run.get('registry_sha256')!=FROZEN_REGISTRY_SHA256
            or not run.get('sources_unchanged_during_run')
            or run.get('source_hashes_before')!=run.get('source_hashes_after')
            or not run.get('source_hashes_after') or check_hashes(run['source_hashes_after'])
            or set(run['source_hashes_after'])!=set(source_hashes())):
        raise ValueError('Missing current, stable, complete candidate execution')
    expected={row['id']:row for row in registry['candidates']}
    if (len(run.get('receipts',[]))!=64 or
            {row['candidate_id'] for row in run['receipts']}!=set(expected)):
        raise ValueError('Missing or duplicate frozen candidate')
    evidence=[HERE/'STAGE_1_GATE.json',HERE/'STAGE_2_GATE.json',HERE/'nonclassical_candidates.json',
              branch_run/'receipts.json',validation_run/'receipts.json',review_path]
    counts=Counter()
    for row in run['receipts']:
        cid=row['candidate_id']
        log=_inside(row['log'])
        result_path=branch_run/cid/'candidate.json'
        ml_path=branch_run/cid/'ml_certificate.json'
        if (row['exit_code']!=0 or row['process_status']!='exited'
                or log!=(branch_run/f'{cid}.log') or digest(log)!=row['log_sha256']
                or digest(result_path)!=row['candidate.json_sha256']
                or digest(ml_path)!=row['ml_certificate.json_sha256']):
            raise ValueError('Failed or changed candidate execution '+cid)
        result,ml=_read(result_path),_read(ml_path)
        status=result['analysis']['conditional_status']
        admitted=status!='failed_conditional_criterion'
        if (result['candidate']!=expected[cid] or status not in STATUSES
                or result['mathematical_admission'] is not admitted
                or ml['candidate_id']!=cid or ml['conditional_status']!=status
                or ml['conditional_admitted'] is not admitted
                or ml['global_chart_admitted'] is not (status=='verified_conditional_on_declared_chart')
                or ml['training_performed'] is not False
                or ml['certificate']['conditional_evidence']['candidate_sha256']!=digest(result_path)
                or any(ml['certificate'].get(k) is not True for k in (
                    'input_inverse_verified','Q_verified','PDE_pullback_verified','time_coefficients_reconstruct_PDE'))
                or (status=='verified_conditional_on_regular_subchart' and 'u(t,z)!=0' not in ml['valid_domain_mask'])
                or (not admitted and ml['use']!='diagnostic_graph_only')):
            raise ValueError('Inconsistent mathematical/ML admission '+cid)
        counts[status]+=1
        evidence.extend((log,result_path,ml_path))
    if dict(counts)!=run.get('conditional_status_counts'):
        raise ValueError('Candidate summary counts do not match actual results')
    if (not validation.get('all_protected_inputs_unchanged')
            or not validation.get('sources_unchanged_during_run')
            or validation.get('source_hashes_before')!=validation.get('source_hashes_after')
            or not validation.get('source_hashes_after') or check_hashes(validation['source_hashes_after'])
            or set(validation['source_hashes_after'])!=set(validation_source_hashes())):
        raise ValueError('Missing current validation or protected input drift')
    rows=validation.get('receipts',[])
    if (len(rows)!=6 or {row['name'] for row in rows}!=
            {'audit','data-flux','workflow','engine-chart','active-package','new-cycle'}):
        raise ValueError('Required validation is incomplete')
    qualifications=[]
    for row in rows:
        log=_inside(row['log'])
        if (row['process_status']!='exited' or log!=validation_run/f"{row['name']}.log"
                or digest(log)!=row['log_sha256']):
            raise ValueError('Invalid validation log or subprocess')
        evidence.append(log)
        if row['exit_code']==0:
            continue
        if row['name']!='audit':
            raise ValueError('Validation failed: '+row['name'])
        path=validation_run/'audit'/'audit.json'
        baseline=ROOT/'build/sve-systematic-20261020/validation/audit/audit.json'
        issues,previous=_read(path)['issues'],_read(baseline)['issues']
        if sorted(issues)!=sorted(previous):
            raise ValueError('Changed audit issue set')
        evidence.append(path)
        qualifications.append({'project_audit':'failed_unchanged_preexisting_issue_set',
                               'issue_count':len(issues),'baseline_sha256':digest(baseline)})
    hashes=review.get('inputs_sha256',{})
    required={'nonclassical.py','nonclassical_equivalence.py','ml_adapter.py',
              'nonclassical_runner.py','stage3_gate.py','nonclassical_candidates.json',
              'review_nonclassical.py','NONCLASSICAL_REVIEW.md','NONCLASSICAL_DERIVATION.md',
              'NONCLASSICAL_EQUIVALENCE.md','ML_INPUTS.md'}
    if (review.get('review_status')!='accepted' or review.get('all_checks_passed') is not True
            or not required.issubset(hashes) or check_hashes(hashes)):
        raise ValueError('Independent Stage 3 review is missing or stale')
    reviewed_evidence=review.get('evidence_sha256',{})
    expected_review={str((branch_run/'receipts.json').relative_to(HERE))}
    expected_review.update(str((branch_run/cid/name).relative_to(HERE)) for cid in expected
                           for name in ('candidate.json','ml_certificate.json'))
    if not expected_review.issubset(reviewed_evidence) or check_hashes(reviewed_evidence):
        raise ValueError('Independent review must bind all released candidate and ML outputs')
    evidence.extend(_inside(HERE/name) for name in (*hashes,*reviewed_evidence))
    return {'stage':3,'passed':True,'scope':'64 frozen affine distributions; exact input/reconstruction export',
            'prior_gates':gates,'conditional_status_counts':dict(counts),
            'inputs_sha256':source_hashes(),
            'evidence_sha256':{str(path.relative_to(HERE)):digest(path) for path in evidence},
            'qualifications':qualifications,'training_performed':False,
            'complete_nonclassical_classification_claim':False,
            'new_classically_inequivalent_solution_family_claim':False,
            'subalgebra_optimality_2d':'not proved; separate from completed maximal point algebra'}


def create(branch_run,validation_run,review_path):
    path=HERE/'STAGE_3_GATE.json'
    if path.exists():
        raise ValueError('Preserve the existing stage gate; use a reviewed revision')
    result=assess(branch_run,validation_run,review_path)
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


def check():
    path=HERE/'STAGE_3_GATE.json'
    if not path.is_file():
        return {'passed':False,'reason':'release_gate_missing'}
    gate=_read(path)
    preceding={str(s):check_gate(s) for s in (1,2)}
    if not all(row['passed'] for row in preceding.values()):
        return {'passed':False,'reason':'prior_gate_no_longer_current'}
    if not gate.get('passed') or not gate.get('inputs_sha256') or not gate.get('evidence_sha256'):
        return {'passed':False,'reason':'missing_reviewed_evidence'}
    changed=check_hashes(gate['inputs_sha256'])+check_hashes(gate['evidence_sha256'])
    return {'passed':not changed,'reason':'reviewed_exact_version' if not changed else 'source_or_evidence_changed',
            'changed':changed,'gate_sha256':digest(path),'qualifications':gate.get('qualifications',[])}
