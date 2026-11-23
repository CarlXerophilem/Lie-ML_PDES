"""Independent line-orbit and release-control review; writes only its receipt.

Completeness/nonredundancy arguments are in SUBALGEBRA_REVIEW.md. Finite
checks validate identities and branch bookkeeping, not the abstract theorem.
The stage-gate fixtures use an in-memory filesystem and never create a live gate.
"""
from pathlib import Path
from itertools import combinations, product
from unittest.mock import patch
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
INPUTS = ['subalgebras.py', 'SUBALGEBRAS.md', 'tests/test_subalgebras.py',
          'main.py', 'models.py', 'research_first_order.py', 'research_slope.py',
          'gatekeeper.py', 'run_all.py', 'validate_project.py', 'case_support.py',
          'classification.py', 'SUBALGEBRA_REVIEW.md', 'review_subalgebras.py']
BEFORE = {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in INPUTS}

import sympy as s
import models
import research_first_order
import research_slope
import subalgebras
import gatekeeper
import classification
import run_all

coords = (models.t, models.x, models.h, models.u, models.B)
n = models.n


def basis_for(branch):
    if models.BRANCHES[branch]['G']:
        return research_slope.general_solution(branch, coords)['basis']
    return tuple(research_first_order.branch_generators(branch, coords).values())


def release_controls():
    """Execute real gatekeeper functions against isolated memory-only receipts."""
    source_names = set(INPUTS) | {'data_experiments.py', 'parent_models.py', 'review_data_parent.py'}
    source_names |= {f'cases/{name}.py' for name in models.BRANCHES}
    base = {'cycle/'+f: (HERE/f).read_bytes() for f in source_names}
    hashes = {f: hashlib.sha256(base['cycle/'+f]).hexdigest() for f in source_names}
    sha = lambda value: hashlib.sha256(value).hexdigest()
    dump = lambda value: json.dumps(value).encode()
    data_scope = ['constructed exact flows', 'specified initial-data stabilizers',
                  'P/M separation', 'mass-coordinate signs and guards']
    data = {'review_status': 'accepted', 'all_checks_passed': True, 'scope': data_scope,
            'reviewed_sha256': {f: hashes[f] for f in
                               ('data_experiments.py', 'parent_models.py', 'review_data_parent.py')}}
    base['cycle/review_data_parent_results.json'] = dump(data)
    base['cycle/classification_review.json'] = dump({'all_checks_passed': True, 'inputs_sha256': hashes})
    branches = []
    for name in models.BRANCHES:
        log = f'cycle/run/{name}.log'
        base[log] = ('completed '+name).encode()
        branches.append({'branch': name, 'exit_code': 0, 'process_status': 'exited',
                         'log': log, 'log_sha256': sha(base[log]),
                         'child_sha256': hashes[f'cases/{name}.py']})
        base[f'cycle/run/{name}/derivation.json'] = dump({
            'model_id': name, 'classification_status': 'proved_for_declared_regular_chart',
            'generator_verification': 'verified', 'traveling_reduction': {'status': 'verified_reduction'}})
    base['cycle/run/receipts.json'] = dump({
        'execution_passed': True, 'sources_unchanged_during_run': True,
        'source_hashes_before': hashes, 'source_hashes_after': hashes, 'receipts': branches})
    validations = []
    for name in ('audit', 'data-flux', 'workflow', 'engine-chart', 'active-package', 'new-cycle'):
        log = f'cycle/validation/{name}.log'
        base[log] = ('completed '+name).encode()
        validations.append({'name': name, 'exit_code': 0, 'process_status': 'exited',
                            'log': log, 'log_sha256': sha(base[log])})
    base['cycle/validation/receipts.json'] = dump({
        'all_protected_inputs_unchanged': True, 'sources_unchanged_during_run': True,
        'source_hashes_before': hashes, 'source_hashes_after': hashes, 'receipts': validations})
    contents = {}

    class MemoryPath:
        def __init__(self, value):
            self.value = value.value if isinstance(value, MemoryPath) else str(value).replace('\\', '/')
        def __str__(self):
            return self.value
        def __hash__(self):
            return hash(self.value)
        def __eq__(self, other):
            return self.value == str(other)
        def __truediv__(self, other):
            return MemoryPath(self.value+'/'+str(other))
        def resolve(self):
            return self
        def is_relative_to(self, root):
            return self.value == str(root) or self.value.startswith(str(root)+'/')
        def relative_to(self, root):
            if not self.is_relative_to(root):
                raise ValueError('outside virtual cycle')
            return MemoryPath(self.value[len(str(root))+1:])
        def is_file(self):
            return self.value in contents
        def exists(self):
            return self.is_file()
        def read_bytes(self):
            return contents[self.value]
        def read_text(self, encoding='utf-8'):
            return self.read_bytes().decode(encoding)
        def write_text(self, value, encoding='utf-8'):
            contents[self.value] = value.encode(encoding)
            return len(value)

    def edit(path, mutate):
        obj = json.loads(contents[path])
        mutate(obj)
        contents[path] = dump(obj)

    controls = {}
    additional = ['cycle/review_data_parent_results.json']

    def create():
        return gatekeeper.create_stage1('cycle/run', 'cycle/validation', additional)

    def reject(name, mutate):
        contents.clear(); contents.update(base)
        mutate()
        try:
            create()
        except ValueError:
            controls[name] = True
        else:
            raise AssertionError('Invalid release fixture accepted: '+name)

    with patch.object(gatekeeper, 'Path', MemoryPath), \
         patch.object(gatekeeper, 'HERE', MemoryPath('cycle')), \
         patch.object(gatekeeper, 'ROOT', MemoryPath('workspace')), \
         patch.object(classification, 'review_gate', lambda: {'passed': True, 'reason': 'review fixture'}):
        contents.update(base)
        result = create()
        assert result['passed'] and gatekeeper.check_gate(1)['passed']
        assert 'tracked separately' in result['subalgebra_optimality']
        controls['valid_complete_receipts_pass_without_claiming_subalgebra_optimality'] = True
        contents['cycle/run/grass_generic.log'] += b' changed after release'
        assert gatekeeper.check_gate(1)['passed'] is False
        controls['post_release_changed_evidence_rejected'] = True
        reject('child_nonzero_exit_rejected', lambda: edit('cycle/run/receipts.json',
               lambda obj: obj['receipts'][0].update(exit_code=1)))
        reject('child_timeout_even_with_zero_exit_rejected', lambda: edit('cycle/run/receipts.json',
               lambda obj: obj['receipts'][0].update(process_status='timeout')))
        reject('modified_child_log_rejected', lambda: contents.update({
               'cycle/run/grass_generic.log': b'changed since subprocess'}))
        reject('modified_child_source_rejected', lambda: contents.update({
               'cycle/cases/grass_generic.py': b'changed after subprocess'}))
        reject('wrong_derivation_model_rejected', lambda: edit('cycle/run/grass_generic/derivation.json',
               lambda obj: obj.update(model_id='zero_transport')))
        reject('duplicate_child_receipt_rejected', lambda: edit('cycle/run/receipts.json',
               lambda obj: obj['receipts'].append(obj['receipts'][0])))
        reject('source_snapshot_drift_rejected', lambda: edit('cycle/run/receipts.json',
               lambda obj: obj['source_hashes_after'].update({'main.py': 'bad'})))
        reject('protected_input_failure_rejected', lambda: edit('cycle/validation/receipts.json',
               lambda obj: obj.update(all_protected_inputs_unchanged=False)))
        reject('changed_validation_log_rejected', lambda: contents.update({
               'cycle/validation/new-cycle.log': b'changed after tests'}))
        reject('non_audit_validation_failure_rejected', lambda: edit('cycle/validation/receipts.json',
               lambda obj: obj['receipts'][-1].update(exit_code=1)))
        reject('missing_data_review_scope_rejected', lambda: edit('cycle/review_data_parent_results.json',
               lambda obj: obj.update(scope=[])))
        additional[:] = ['cycle/classification_review.json']
        reject('classification_receipt_cannot_replace_data_review', lambda: None)
        additional[:] = ['cycle/review_data_parent_results.json']
        contents.clear(); contents.update(base)
        create()
        contents['cycle/main.py'] += b' changed after stage gate'
        assert gatekeeper.check_gate(1)['passed'] is False
        controls['post_release_changed_source_rejected'] = True
        contents.clear(); contents.update(base)
        contents['cycle/STAGE_1_GATE.json'] = dump({'passed': True})
        assert gatekeeper.check_gate(1)['passed'] is False
        controls['bare_stage_success_flag_rejected'] = True
        contents.clear(); contents.update(base)
        edit('cycle/validation/receipts.json', lambda obj: obj['receipts'][0].update(exit_code=1))
        issues = ['retained old missing archive link']
        contents['cycle/validation/audit/audit.json'] = dump({'issues': issues})
        contents['workspace/build/sve-systematic-20261020/validation/audit/audit.json'] = dump({'issues': issues})
        qualified = create()
        assert qualified['qualifications'][0]['project_audit'] == 'failed_unchanged_preexisting_issue_set'
        controls['unchanged_audit_failure_retained_as_failure_qualification'] = True
    return controls


def run():
    started = time.perf_counter()
    checks, records = [], {}

    def check(name, values):
        values = list(values) if isinstance(values, (s.MatrixBase, list, tuple)) else [values]
        residuals = [s.simplify(s.expand(v)) for v in values]
        assert all(v == 0 for v in residuals), (name, residuals)
        checks.append(name)

    for branch in models.BRANCHES:
        basis = [s.Matrix(v) for v in basis_for(branch)]
        kwargs = {'parameter': n, 'domain': s.Interval(0, 4)} if branch == 'slope_only' else {}
        result = subalgebras.classify_subalgebra_lines(coords, basis, **kwargs)
        assert result['status'] == 'certified_line_orbit_classification'
        structure = result['structure']
        vi, ai = structure['translation_indices'], structure['scaling_indices']
        for i, left in enumerate(basis):
            defects = []
            for j, right in enumerate(basis):
                direct = s.Matrix([sum(left[k]*s.diff(right[l], q)-right[k]*s.diff(left[l], q)
                                       for k, q in enumerate(coords)) for l in range(5)])
                represented = sum((basis[k]*structure['adjoint_matrices'][i][k, j]
                                   for k in range(len(basis))), s.zeros(5, 1))
                defects.extend(direct-represented)
            check(f'{branch} actual vector-field brackets for basis {i}', defects)
        cells = []
        for cellno, cell in enumerate(result['strata']):
            W = cell['weights']
            excluded = set(cell.get('excluded_resonances', ()))
            seen = set()
            translation_groups = {}
            direction_groups = {}
            for familyno, family in enumerate(cell['families']):
                label = f'{branch} cell{cellno} family{familyno}'
                support = family['support']
                if family['kind'] == 'translation_line':
                    key = ('V', support, family['signs'])
                    translation_groups.setdefault(support, []).append(family)
                    M = s.ones(len(support), 1).row_join(W.extract(support, range(W.cols)))
                else:
                    direction = tuple(family['A_direction']['direction'])
                    key = ('A', direction, support, family['signs'])
                    direction_groups.setdefault(direction, []).append(family)
                    eigen = W*s.Matrix(direction)
                    kernel = tuple(i for i, value in enumerate(eigen) if s.factor(value) == 0)
                    assert family['kernel'] == kernel and set(support).issubset(kernel)
                    M = W.extract(support, range(W.cols))
                assert key not in seen, (label, 'duplicate family key')
                seen.add(key)
                certificate = family['normalizer']
                free = certificate['remaining_rows']
                # Independently construct the annihilator of the orbit directions.
                # It gives all linear invariants, without using the exported Pi.
                null = M.T.nullspace()
                N = s.Matrix.vstack(*(vec.T for vec in null)) if null else s.zeros(0, len(support))
                assert len(free) == N.rows == len(family['parameters'])-(len(family.get('A_direction', {}).get('parameters', ())))
                check(label+' independent invariant annihilator', N*M)
                check(label+' canonical projection preserves every quotient invariant', N*certificate['invariant_projection']-N)
                if N.rows:
                    invariant_minor = s.factor(N.extract(range(N.rows), free).det())
                    assert invariant_minor != 0
                    if invariant_minor.has(n):
                        roots = s.solveset(s.fraction(invariant_minor)[0], n, domain=s.Interval(0, 4))
                        assert isinstance(roots, s.FiniteSet) or roots == s.EmptySet
                        assert set(roots).issubset(excluded)
                # The normalization move itself lies in the actual orbit tangent image.
                check(label+' orbit-to-slice identity',
                      certificate['invariant_projection']-s.eye(len(support))-M*certificate['theta_map'])
            expected_supports = {sup for size in range(1, len(vi)+1) for sup in combinations(range(len(vi)), size)}
            assert set(translation_groups) == expected_supports
            for support, families in translation_groups.items():
                assert {f['signs'] for f in families} == {(1,)+tail for tail in product((-1, 1), repeat=len(support)-1)}
            for direction, families in direction_groups.items():
                a = s.Matrix(direction)
                eigen = W*a
                kernel = families[0]['kernel']
                expected = {(support, signs) for size in range(len(kernel)+1)
                            for support in combinations(kernel, size)
                            for signs in product((-1, 1), repeat=size)}
                assert {(f['support'], f['signs']) for f in families} == expected
                vv = s.symbols('v0:'+str(len(vi)), real=True)
                vector, shift = s.zeros(len(basis), 1), s.zeros(len(basis), 1)
                for j, index in enumerate(ai):
                    vector[index] = a[j]
                for j, index in enumerate(vi):
                    vector[index] = vv[j]
                    if j not in kernel:
                        shift[index] = vv[j]/eigen[j]
                ad = sum((shift[i]*structure['adjoint_matrices'][i].subs(cell['substitutions'])
                          for i in range(len(basis))), s.zeros(len(basis)))
                check(f'{branch} cell{cellno} direction{direction} nilpotent translation ad', ad*ad)
                expected_vector = vector.copy()
                for j, index in enumerate(vi):
                    if j not in kernel:
                        expected_vector[index] = 0
                check(f'{branch} cell{cellno} direction{direction} actual ad elimination',
                      (s.eye(len(basis))+ad)*vector-expected_vector)
            cells.append({'label': cell['label'], 'families': len(cell['families']),
                          'translation_families': sum(len(v) for v in translation_groups.values()),
                          'A_directions': len(direction_groups), 'passed': True})
        if branch == 'slope_only':
            W = structure['weights']
            roots = set()
            for row in W:
                roots.update(s.solve(row, n))
            for i, j in combinations(range(3), 2):
                roots.update(s.solve(W[i, 0]-W[j, 0], n))
            assert roots == {s.Integer(1), s.Integer(2), s.Integer(3), s.Integer(4)}
            assert set(result['strata'][0]['excluded_resonances']) == roots
            assert {c['substitutions'][n] for c in result['strata'][1:]} == roots
            assert all(s.simplify(guard.subs(n, 0)) is s.true for guard in result['strata'][0]['guards'])
            checks.append('slope resonances exhaust zero-weight and equal-weight mechanisms; n0 is generic')
        if len(ai) == 2:
            finite = {f['A_direction'].get('a_ratio') for f in result['strata'][0]['families']
                      if f['kind'] == 'nonzero_A_line' and 'a_ratio' in f['A_direction']}
            assert finite == {s.Integer(-1), s.Integer(0)}
            assert cells[0]['A_directions'] == 4 and cells[0]['families'] == 23
            checks.append(branch+' complete projective A charts including infinity')
        records[branch] = {'passed': True, 'weights': str(structure['weights']), 'strata': cells}
        print(f'PASS {branch}: {sum(c["families"] for c in cells)} representative families', flush=True)

    print('RUN in-memory release gate rejection controls', flush=True)
    gates = release_controls()
    hashes = {name.replace('\\', '/'): value for name, value in run_all.source_hashes().items()}
    assert all(f in hashes for f in ('gatekeeper.py', 'run_all.py', 'subalgebras.py',
                                     'case_support.py', 'review_subalgebras.py', 'tests/test_subalgebras.py'))
    checks.append('runner snapshots release, mathematical, child, test and reviewer Python sources')
    after = {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in INPUTS}
    assert after == BEFORE, 'Reviewed sources changed during execution'
    receipt = {
        'review_status': 'accepted', 'all_checks_passed': True,
        'verdicts': {'one_dimensional_subalgebras': 'accepted exhaustive and nonredundant for connected inner adjoint plus line rescaling',
                     'release_controls': 'accepted for produced receipts on frozen source snapshots'},
        'check_count': len(checks), 'checks': checks, 'branches': records,
        'release_gate_controls': gates, 'input_snapshot_unchanged_through_execution': True,
        'prior_attempts': [{'status': 'reviewer_assertion_failed',
                            'reason': 'Windows hash-path separators differed from the reviewer assertion; normalized and rerun'}],
        'inputs_sha256': BEFORE, 'elapsed_seconds': time.perf_counter()-started,
        'limitations': ['No disconnected or outer equivalence classification', 'No higher-dimensional subalgebras',
                        'No automatic usefulness, data compatibility, or regularity for every representative',
                        'No live stage gate created by this review; virtual fixtures only',
                        'Full child and project validation executions belong to root release'],
    }
    (HERE/'subalgebra_review.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'checks': len(checks), 'gate_controls': len(gates),
                      'elapsed_seconds': receipt['elapsed_seconds'], 'passed': True}, indent=2))


if __name__ == '__main__':
    run()
