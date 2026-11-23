"""Independent synthetic controls for the Stage 3 release gate.

All evidence is synthetic and isolated; no frozen Stage 1/2 artifact is edited.
The actual mathematical review is review_nonclassical.py, not this fixture.
"""
import copy
import json
from pathlib import Path

import pytest

import gatekeeper
import stage3_gate as gate


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2), encoding='utf-8')


@pytest.fixture
def synthetic(tmp_path, monkeypatch):
    root = tmp_path/'cycle'
    root.mkdir()
    batch, validation = root/'runs'/'batch', root/'runs'/'validation'
    review_path = root/'nonclassical_review.json'
    originals = json.loads((gate.HERE/'nonclassical_candidates.json').read_text(encoding='utf-8'))
    candidates = originals['candidates']
    names = ('nonclassical.py', 'nonclassical_equivalence.py', 'ml_adapter.py',
             'nonclassical_runner.py', 'stage3_gate.py', 'review_nonclassical.py',
             'NONCLASSICAL_DERIVATION.md', 'NONCLASSICAL_EQUIVALENCE.md',
             'NONCLASSICAL_REVIEW.md', 'ML_INPUTS.md', 'CONTRACT.md', 'models_2d.py', 'models.py', 'main.py')
    for name in names:
        (root/name).write_text('synthetic '+name, encoding='utf-8')
    put(root/'nonclassical_candidates.json', originals)
    put(root/'STAGE_1_GATE.json', {'synthetic': True})
    put(root/'STAGE_2_GATE.json', {'synthetic': True})
    monkeypatch.setattr(gate, 'HERE', root)
    monkeypatch.setattr(gate, 'ROOT', root)
    monkeypatch.setattr(gate, 'load_registry', lambda: (originals, {'1': {'passed': True}, '2': {'passed': True}}))
    monkeypatch.setattr(gate, 'check_gate', lambda stage: {'passed': True})
    monkeypatch.setattr(gate, 'check_hashes', lambda hashes: gatekeeper.check_hashes(hashes, root=root))
    def sources():
        return {p.name: gatekeeper.digest(p) for p in root.glob('*.py')}
    monkeypatch.setattr(gate, 'source_hashes', sources)
    # The live frozen validation inventory omits cases_2d, while the batch
    # inventory includes them. This fixture contains no such child sources.
    monkeypatch.setattr(gate, 'validation_source_hashes', sources)
    rows = []
    for candidate in candidates:
        cid = candidate['id']
        regular = cid == 'C34'
        status = 'verified_conditional_on_regular_subchart' if regular else 'failed_conditional_criterion'
        result = {'candidate': candidate, 'analysis': {'conditional_status': status},
                  'mathematical_admission': regular}
        result_path, ml_path = batch/cid/'candidate.json', batch/cid/'ml_certificate.json'
        put(result_path, result)
        ml = {'candidate_id': cid, 'conditional_status': status, 'conditional_admitted': regular,
              'global_chart_admitted': False, 'training_performed': False,
              'use': 'certified_conditional_solution_class' if regular else 'diagnostic_graph_only',
              'valid_domain_mask': ['u(t,z)!=0'] if regular else [],
              'certificate': {'conditional_evidence': {'candidate_sha256': gatekeeper.digest(result_path)},
                              'input_inverse_verified': True, 'Q_verified': True,
                              'PDE_pullback_verified': True, 'time_coefficients_reconstruct_PDE': True}}
        put(ml_path, ml)
        log = batch/f'{cid}.log'
        log.write_text('synthetic successful execution', encoding='utf-8')
        rows.append({'candidate_id': cid, 'exit_code': 0, 'process_status': 'exited',
                     'log': str(log), 'log_sha256': gatekeeper.digest(log),
                     'candidate.json_sha256': gatekeeper.digest(result_path),
                     'ml_certificate.json_sha256': gatekeeper.digest(ml_path)})
    source_map = sources()
    run = {'execution_passed': True, 'candidate_count': 64,
           'registry_sha256': gate.FROZEN_REGISTRY_SHA256, 'sources_unchanged_during_run': True,
           'source_hashes_before': source_map, 'source_hashes_after': source_map,
           'receipts': rows, 'conditional_status_counts': {
               'verified_conditional_on_regular_subchart': 1, 'failed_conditional_criterion': 63}}
    put(batch/'receipts.json', run)
    validation_rows = []
    validation.mkdir(parents=True)
    for name in ('audit', 'data-flux', 'workflow', 'engine-chart', 'active-package', 'new-cycle'):
        log = validation/f'{name}.log'
        log.write_text('synthetic successful validation', encoding='utf-8')
        validation_rows.append({'name': name, 'exit_code': 0, 'process_status': 'exited',
                                'log': str(log), 'log_sha256': gatekeeper.digest(log)})
    validation_data = {'all_protected_inputs_unchanged': True, 'sources_unchanged_during_run': True,
                       'source_hashes_before': source_map, 'source_hashes_after': source_map,
                       'receipts': validation_rows}
    put(validation/'receipts.json', validation_data)
    evidence_files = [batch/'receipts.json'] + [batch/c['id']/name for c in candidates
                       for name in ('candidate.json', 'ml_certificate.json')]
    review = {'review_status': 'accepted', 'all_checks_passed': True,
              'inputs_sha256': {name: gatekeeper.digest(root/name) for name in
                                (*names, 'nonclassical_candidates.json')},
              'evidence_sha256': {str(p.relative_to(root)): gatekeeper.digest(p) for p in evidence_files}}
    put(review_path, review)
    return {'root': root, 'batch': batch, 'validation': validation, 'review_path': review_path,
            'run': run, 'validation_data': validation_data, 'review': review}


def assess(fixture):
    return gate.assess(fixture['batch'], fixture['validation'], fixture['review_path'])


def test_synthetic_complete_evidence_accepts(synthetic):
    result = assess(synthetic)
    assert result['passed']
    assert result['new_classically_inequivalent_solution_family_claim'] is False
    assert result['complete_nonclassical_classification_claim'] is False


@pytest.mark.parametrize('attack', ['duplicate', 'timeout', 'nonzero_exit', 'missing_source', 'bad_counts'])
def test_incomplete_or_changed_execution_rejected(synthetic, attack):
    run = copy.deepcopy(synthetic['run'])
    if attack == 'duplicate':
        run['receipts'][1]['candidate_id'] = run['receipts'][0]['candidate_id']
    elif attack == 'timeout':
        run['receipts'][0]['process_status'] = 'timeout'
    elif attack == 'nonzero_exit':
        run['receipts'][0]['exit_code'] = 1
    elif attack == 'missing_source':
        run['source_hashes_before'].pop('ml_adapter.py')
        run['source_hashes_after'].pop('ml_adapter.py', None)
    else:
        run['conditional_status_counts']['failed_conditional_criterion'] = 62
    put(synthetic['batch']/'receipts.json', run)
    with pytest.raises(ValueError):
        assess(synthetic)


@pytest.mark.parametrize('attack', ['unguarded_regular', 'promoted_failure', 'training', 'wrong_candidate_hash'])
def test_ml_export_cannot_launder_a_failure(synthetic, attack):
    cid = 'C34' if attack == 'unguarded_regular' else 'C03'
    path = synthetic['batch']/cid/'ml_certificate.json'
    ml = json.loads(path.read_text(encoding='utf-8'))
    if attack == 'unguarded_regular':
        ml['valid_domain_mask'] = []
    elif attack == 'promoted_failure':
        ml['conditional_admitted'] = True
    elif attack == 'training':
        ml['training_performed'] = True
    else:
        ml['certificate']['conditional_evidence']['candidate_sha256'] = '0'*64
    put(path, ml)
    run = copy.deepcopy(synthetic['run'])
    next(row for row in run['receipts'] if row['candidate_id'] == cid)['ml_certificate.json_sha256'] = gatekeeper.digest(path)
    put(synthetic['batch']/'receipts.json', run)
    with pytest.raises(ValueError):
        assess(synthetic)


def test_validation_must_cover_every_executed_source(synthetic):
    value = copy.deepcopy(synthetic['validation_data'])
    value['source_hashes_before'].pop('ml_adapter.py')
    value['source_hashes_after'].pop('ml_adapter.py', None)
    put(synthetic['validation']/'receipts.json', value)
    with pytest.raises(ValueError):
        assess(synthetic)


@pytest.mark.parametrize('name', ['NONCLASSICAL_DERIVATION.md', 'NONCLASSICAL_EQUIVALENCE.md',
                                'review_nonclassical.py', 'NONCLASSICAL_REVIEW.md', 'ML_INPUTS.md'])
def test_review_must_bind_proof_and_reviewer_sources(synthetic, name):
    review = copy.deepcopy(synthetic['review'])
    review['inputs_sha256'].pop(name)
    put(synthetic['review_path'], review)
    with pytest.raises(ValueError):
        assess(synthetic)


def test_review_must_bind_every_ml_output(synthetic):
    review = copy.deepcopy(synthetic['review'])
    key = str((synthetic['batch']/'C63'/'ml_certificate.json').relative_to(synthetic['root']))
    review['evidence_sha256'].pop(key)
    put(synthetic['review_path'], review)
    with pytest.raises(ValueError):
        assess(synthetic)


def test_post_release_source_change_revokes_gate(synthetic):
    put(synthetic['root']/'STAGE_3_GATE.json', assess(synthetic))
    assert gate.check()['passed']
    (synthetic['root']/'ml_adapter.py').write_text('changed mathematical admission', encoding='utf-8')
    assert not gate.check()['passed']


def test_a_bare_success_flag_is_not_a_release(synthetic):
    put(synthetic['root']/'STAGE_3_GATE.json', {'passed': True})
    assert not gate.check()['passed']


def test_evidence_outside_cycle_is_rejected(synthetic):
    with pytest.raises(ValueError):
        gate.assess(synthetic['root'].parent/'other', synthetic['validation'], synthetic['review_path'])
