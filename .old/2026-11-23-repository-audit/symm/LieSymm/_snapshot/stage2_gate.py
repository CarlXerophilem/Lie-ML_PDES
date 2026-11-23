"""Bind 2D maximality review to stable execution and required validation."""
from pathlib import Path
import json
from gatekeeper import HERE,ROOT,digest,check_hashes,check_gate


def create_stage2(branch_run,validation_run,additional_review_receipts=()):
    from classification_2d import review_gate
    from models_2d import BRANCHES_2D
    from stage2_runner import source_hashes as stage2_source_hashes
    from run_all import source_hashes as validation_source_hashes
    preceding=check_gate(1)
    current=review_gate()
    if not preceding['passed'] or not current['passed']:
        raise ValueError({'preceding':preceding,'classification':current})
    branch_run,validation_run=Path(branch_run).resolve(),Path(validation_run).resolve()
    if not all(path.is_relative_to(HERE) for path in (branch_run,validation_run)):
        raise ValueError('Execution evidence must belong to this cycle')
    run=json.loads((branch_run/'receipts.json').read_text(encoding='utf-8'))
    validation=json.loads((validation_run/'receipts.json').read_text(encoding='utf-8'))
    if (not run['execution_passed'] or not run['sources_unchanged_during_run']
            or not run['source_hashes_after']
            or set(run['source_hashes_after'])!=set(stage2_source_hashes())
            or run['source_hashes_before']!=run['source_hashes_after']
            or check_hashes(run['source_hashes_after'])):
        raise ValueError('Missing stable and current branch execution')
    if ({row['branch'] for row in run['receipts']}!=set(BRANCHES_2D)
            or len(run['receipts'])!=len(BRANCHES_2D)):
        raise ValueError('Missing or duplicate declared 2D branch')
    evidence=[HERE/'STAGE_1_GATE.json',HERE/'classification_2d_review.json',
              branch_run/'receipts.json',validation_run/'receipts.json']
    for row in run['receipts']:
        name=row['branch']
        log=Path(row['log'])
        path=branch_run/name/'derivation.json'
        result=json.loads(path.read_text(encoding='utf-8'))
        if (row['exit_code']!=0 or row['process_status']!='exited'
                or log.resolve()!=(branch_run/f'{name}.log').resolve()
                or digest(log)!=row['log_sha256']
                or digest(path)!=row.get('derivation_sha256')
                or digest(HERE/'cases_2d'/f'{name}.py')!=row['child_sha256']
                or result['model_id']!='2d__'+name
                or result['classification_status']!='proved_for_declared_regular_chart'
                or result['generator_verification']!='verified'
                or result['reduction_status']!='verified_specified_reductions'
                or result['data_status']!='verified_specified_data_controls'):
            raise ValueError('Incomplete execution: '+name)
        evidence.extend((log,path))
    if (not validation['all_protected_inputs_unchanged']
            or not validation['sources_unchanged_during_run']
            or not validation['source_hashes_after']
            or set(validation['source_hashes_after'])!=set(validation_source_hashes())
            or validation['source_hashes_before']!=validation['source_hashes_after']
            or check_hashes(validation['source_hashes_after'])):
        raise ValueError('Validation changed protected/live sources')
    if ({row['name'] for row in validation['receipts']}!=
            {'audit','data-flux','workflow','engine-chart','active-package','new-cycle'}
            or len(validation['receipts'])!=6):
        raise ValueError('Required validation command missing or duplicated')
    qualifications=[]
    for row in validation['receipts']:
        log=Path(row['log'])
        if (row['process_status']!='exited'
                or log.resolve()!=(validation_run/f"{row['name']}.log").resolve()
                or digest(log)!=row['log_sha256']):
            raise ValueError('Validation process or canonical log is invalid')
        evidence.append(log)
        if row['exit_code']==0:
            continue
        if row['name']!='audit':
            raise ValueError('Validation failed: '+row['name'])
        path=validation_run/'audit'/'audit.json'
        baseline=ROOT/'build/sve-systematic-20261020/validation/audit/audit.json'
        issues=json.loads(path.read_text(encoding='utf-8'))['issues']
        previous=json.loads(baseline.read_text(encoding='utf-8'))['issues']
        if sorted(issues)!=sorted(previous):
            raise ValueError('Changed project audit issue set requires review')
        evidence.append(path)
        qualifications.append({'project_audit':'failed_unchanged_preexisting_issue_set',
                               'issue_count':len(issues),'baseline':str(baseline),
                               'baseline_sha256':digest(baseline)})
    required_reviews={HERE/'data_2d_review.json':'data_experiments_2d.py',
                      HERE/'algebra_2d_review.json':'algebra_2d.py'}
    if not set(required_reviews).issubset({Path(path).resolve() for path in additional_review_receipts}):
        raise ValueError('Independent data and algebra reviews are required')
    for path in additional_review_receipts:
        path=Path(path).resolve()
        if not path.is_relative_to(HERE):
            raise ValueError('Review must belong to this cycle')
        receipt=json.loads(path.read_text(encoding='utf-8'))
        hashes=receipt.get('inputs_sha256',receipt.get('reviewed_sha256',{}))
        if (receipt.get('all_checks_passed') is not True or not hashes or check_hashes(hashes)
                or receipt.get('review_status')!='accepted'
                or (path in required_reviews and required_reviews[path] not in hashes)):
            raise ValueError('Incomplete or stale additional review')
        evidence.append(path)
        # check_gate(2) must remain sensitive to reviewed prose and other
        # non-Python dependencies after this creation-time validation.
        for name in hashes:
            dependency=(HERE/name).resolve()
            if not dependency.is_relative_to(HERE):
                raise ValueError('Reviewed dependency is outside this cycle')
            evidence.append(dependency)
    result={'stage':2,'passed':True,'classification_scope':'all 17 declared 2D local smooth point algebras; h>0, u^2+v^2>0',
            'classification_receipt':current,'branches':list(BRANCHES_2D),
            'inputs_sha256':run['source_hashes_after'],
            'evidence_sha256':{str(path.relative_to(HERE)):digest(path) for path in evidence},
            'qualifications':qualifications,
            'subalgebra_optimality':'not proved; verified representatives and actual adjoints are separate',
            'separate_unresolved_questions':['complete point-equivalence groupoid',
                                             'optimal classification of 2D-model subalgebras',
                                             'global solutions and arbitrary data']}
    path=HERE/'STAGE_2_GATE.json'
    if path.exists():
        raise ValueError('Preserve existing stage gate; create a reviewed revision instead')
    path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result
