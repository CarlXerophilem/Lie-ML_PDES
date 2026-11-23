"""Exact-version stage gates: a bare passed flag cannot authorize later work."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_hashes(hashes, root=None):
    root=HERE if root is None else Path(root)
    return [name for name,value in hashes.items()
            if not (root/name).is_file() or digest(root/name)!=value]


def check_gate(stage):
    if stage not in (1,2):
        return {'passed':False,'reason':'unknown_classification_stage'}
    path=HERE/f'STAGE_{stage}_GATE.json'
    if not path.is_file():
        return {'passed':False,'reason':'preceding_classification_gate_missing'}
    gate=json.loads(path.read_text(encoding='utf-8'))
    if gate.get('passed') is not True or not gate.get('inputs_sha256') or not gate.get('evidence_sha256'):
        return {'passed':False,'reason':'missing_positive_gate_and_hashed_evidence'}
    changed=check_hashes(gate['inputs_sha256'])+check_hashes(gate['evidence_sha256'])
    if changed:
        return {'passed':False,'reason':'stage_sources_or_evidence_changed','changed':changed}
    if stage==1:
        from classification import review_gate
        current=review_gate()
        if not current['passed']:
            return {'passed':False,'reason':'independent_classification_review_not_current','review':current}
    else:
        try:
            from classification_2d import review_gate as review_gate_2d
        except ImportError:
            return {'passed':False,'reason':'independent_2d_review_not_implemented'}
        current=review_gate_2d()
        if not current['passed']:
            return {'passed':False,'reason':'independent_2d_review_not_current','review':current}
    return {'passed':True,'reason':'reviewed_and_executed_exact_version',
            'gate_sha256':digest(path),'qualifications':gate.get('qualifications',[])}


def create_stage1(branch_run, validation_run, additional_review_receipts):
    """Bind a reviewed classification to all child executions and fresh tests.

    Repository documentary audit failures are retained verbatim, and can be
    qualified only if their exact issue set matches the earlier frozen cycle.
    This does not relabel a failed project-wide audit as passing.
    """
    from classification import review_gate
    from models import BRANCHES
    review=review_gate()
    if not review['passed']:
        raise ValueError(review)
    branch_run,validation_run=Path(branch_run).resolve(),Path(validation_run).resolve()
    for path in (branch_run,validation_run):
        if not path.resolve().is_relative_to(HERE):
            raise ValueError('Stage receipts must belong to this cycle')
    run=json.loads((branch_run/'receipts.json').read_text(encoding='utf-8'))
    validation=json.loads((validation_run/'receipts.json').read_text(encoding='utf-8'))
    if (not run['execution_passed'] or not run['sources_unchanged_during_run']
            or run['source_hashes_before']!=run['source_hashes_after']):
        raise ValueError('All branch children must run on stable sources')
    if {r['branch'] for r in run['receipts']}!=set(BRANCHES):
        raise ValueError('Missing declared branch execution')
    if len(run['receipts'])!=len(BRANCHES):
        raise ValueError('Duplicate or extra branch execution')
    evidence=[HERE/'classification_review.json',branch_run/'receipts.json',validation_run/'receipts.json']
    for receipt in run['receipts']:
        name=receipt['branch']
        log=Path(receipt['log'])
        if (receipt['exit_code']!=0 or receipt['process_status']!='exited'
                or log.resolve()!=(branch_run/f'{name}.log').resolve()
                or digest(log)!=receipt['log_sha256']
                or digest(HERE/'cases'/f'{name}.py')!=receipt['child_sha256']):
            raise ValueError(f'Unverified child process/log/source for {name}')
        evidence.append(log)
    for name in BRANCHES:
        path=branch_run/name/'derivation.json'
        result=json.loads(path.read_text(encoding='utf-8'))
        if (result['model_id']!=name
                or result['classification_status']!='proved_for_declared_regular_chart'
                or result['generator_verification']!='verified'
                or result['traveling_reduction']['status']!='verified_reduction'):
            raise ValueError(f'Incomplete branch {name}')
        evidence.append(path)
    if (not validation['all_protected_inputs_unchanged'] or not validation['sources_unchanged_during_run']
            or validation['source_hashes_before']!=validation['source_hashes_after']):
        raise ValueError('Protected evidence or live test sources changed')
    required={'audit','data-flux','workflow','engine-chart','active-package','new-cycle'}
    if {r['name'] for r in validation['receipts']}!=required:
        raise ValueError('Missing required validation command')
    qualifications=[]
    for receipt in validation['receipts']:
        log=Path(receipt['log'])
        if digest(log)!=receipt['log_sha256']:
            raise ValueError('Validation log changed')
        evidence.append(log)
        if receipt['exit_code']==0:
            continue
        if receipt['name']!='audit':
            raise ValueError(f"Validation failed: {receipt['name']}")
        current=validation_run/'audit'/'audit.json'
        baseline=ROOT/'build/sve-systematic-20261020/validation/audit/audit.json'
        issues=json.loads(current.read_text(encoding='utf-8'))['issues']
        old=json.loads(baseline.read_text(encoding='utf-8'))['issues']
        if sorted(issues)!=sorted(old):
            raise ValueError('Project audit failure changed; requires explicit review')
        evidence.append(current)
        qualifications.append({'project_audit':'failed_unchanged_preexisting_issue_set',
            'issue_count':len(issues),'baseline':str(baseline),'baseline_sha256':digest(baseline),
            'interpretation':'documentary/archive/link audit remains failed; mathematical classification and tests are separate'})
    for receipt_path in additional_review_receipts:
        receipt_path=Path(receipt_path).resolve()
        receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
        hashes=receipt.get('inputs_sha256',receipt.get('reviewed_sha256'))
        if not receipt.get('all_checks_passed') or not hashes:
            raise ValueError('Additional independent review is incomplete')
        if check_hashes(hashes):
            raise ValueError('Additional review is stale')
        evidence.append(receipt_path)
    data_path=HERE/'review_data_parent_results.json'
    if data_path not in [Path(p).resolve() for p in additional_review_receipts]:
        raise ValueError('Data/parent independent review is required')
    data=json.loads(data_path.read_text(encoding='utf-8'))
    if (data.get('review_status')!='accepted'
            or not {'constructed exact flows','specified initial-data stabilizers','P/M separation',
                    'mass-coordinate signs and guards'}.issubset(data.get('scope',[]))
            or not {'data_experiments.py','parent_models.py','review_data_parent.py'}.issubset(
                data.get('reviewed_sha256',{}))):
        raise ValueError('Required data/parent review scope is not accepted')
    for snapshot in (run['source_hashes_before'],validation['source_hashes_before']):
        if check_hashes(snapshot):
            raise ValueError('Source changed after branch or validation execution')
    result={'stage':1,'passed':True,'classification_scope':'all declared 1D local smooth point algebras on h>0, |u|>0',
        'classification_receipt':review,'branches':list(BRANCHES),
        'inputs_sha256':validation['source_hashes_before'],
        'evidence_sha256':{str(p.relative_to(HERE)):digest(p) for p in evidence},
        'qualifications':qualifications,
        'separate_unresolved_questions':['full point-equivalence groupoid','global solutions and arbitrary data'],
        'subalgebra_optimality':'tracked separately; not inferred from point-algebra maximality'}
    path=HERE/'STAGE_1_GATE.json'
    if path.exists():
        raise ValueError('Preserve existing stage gate; do not overwrite without a new revision')
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
