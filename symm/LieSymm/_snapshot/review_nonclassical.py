"""Independent Stage 3 review, using direct first prolongation of raw PDEs.

The reference calculation below does not import the conditional solver,
its elimination formulas, equivalence adapter, or the ML graph constructor.
Production interfaces are compared separately after the reference is built.
"""
from __future__ import annotations

import hashlib
import argparse
import json
import math
from functools import lru_cache
from pathlib import Path
import time

import sympy as sp

HERE = Path(__file__).resolve().parent
FROZEN = '2409ee048ab8ed66bdf4d0840a34a95b6ea380fdb72c2aedc29ce84382b3b764'
t, x, y = sp.symbols('t x y', real=True)
h, u, v, B = sp.symbols('h u v B', real=True)
g, K = sp.symbols('g K', positive=True)
FIELDS = (h, u, v, B)
PT = sp.Matrix(sp.symbols('ht ut vt Bt', real=True))
PX = sp.Matrix(sp.symbols('hx ux vx Bx', real=True))
PY = sp.Matrix(sp.symbols('hy uy vy By', real=True))
REGULAR_IDS = {'C00', 'C01', 'C02', 'C28', 'C31', 'C34', 'C37',
               'C45', 'C46', 'C47', 'C48', 'C49', 'C50'}
FULL_IDS = REGULAR_IDS - {'C34', 'C37'}


def clean(value):
    return sp.factor(sp.cancel(value))


def serial(value):
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, sp.MatrixBase)):
        return [serial(v) for v in value]
    if isinstance(value, sp.Basic):
        return str(value)
    return value


def raw_pde():
    """Original two-dimensional cubic Grass equations, no solver templates."""
    ht, ut, vt, Bt = PT
    hx, ux, vx, Bx = PX
    hy, uy, vy, By = PY
    return sp.Matrix([
        ht + u*hx + h*ux + v*hy + h*vy,
        ut + u*ux + v*uy + g*(hx+Bx),
        vt + u*vx + v*vy + g*(hy+By),
        Bt + K*((3*u*u+v*v)*ux + 2*u*v*vx
                + 2*u*v*uy + (u*u+3*v*v)*vy),
    ])


def reference(candidate):
    """Differentiate every raw equation as a function on first-jet space."""
    a = tuple(map(sp.Integer, candidate['a']))
    b = tuple(map(sp.Integer, candidate['b']))
    c = sp.Integer(candidate['c'])
    eta = sp.Matrix([ai*field+bi for ai, bi, field in zip(a, b, FIELDS)])
    equations = raw_pde()
    prolonged = equations.jacobian(FIELDS)*eta
    for jets in (PT, PX, PY):
        prolonged += equations.jacobian(jets)*sp.diag(*a)*jets
    q_subs = dict(zip(PT, eta-c*PX)) | dict(zip(PY, (0,)*4))
    joint = equations.subs(q_subs, simultaneous=True).applyfunc(sp.expand)
    omega = prolonged.subs(q_subs, simultaneous=True).applyfunc(sp.expand)
    leading = joint.jacobian(PX)
    return {'eta': eta, 'joint': joint, 'prolonged': omega, 'leading': leading,
            'determinant': clean(leading.det())}


@lru_cache(maxsize=3)
def independent_adjugate(c):
    zero = {'c': c, 'a': [0]*4, 'b': [0]*4}
    matrix = reference(zero)['leading']
    return matrix.adjugate()


def independent_uniform_obstruction(item, c):
    """A directly prolonged field coefficient with fixed sign for every g,K>0."""
    omega = item['prolonged']
    numerators = (omega.subs(dict(zip(PX, (0,)*4)))*item['determinant']
                  -omega.jacobian(PX)*independent_adjugate(c)*item['eta']).applyfunc(sp.expand)
    for row, expression in enumerate(numerators):
        for powers, coefficient in sp.Poly(expression, *FIELDS).as_dict().items():
            parameter_coefficients = list(sp.Poly(coefficient, g, K).as_dict().values())
            if (parameter_coefficients and
                    (all(value > 0 for value in parameter_coefficients)
                     or all(value < 0 for value in parameter_coefficients))):
                return {'row': row, 'field_powers': powers, 'coefficient': coefficient,
                        'parameter_coefficients': parameter_coefficients,
                        'nonzero_for_every_positive_g_K': True}
    return None


def independent_math(candidates):
    checks = []
    rows = []
    def check(name, passed, evidence=None):
        checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})

    # An independently selected regular point works for all three frozen c's.
    point = {g: 1, K: 1, h: 2, u: 2, v: 1, B: 3}
    for candidate in candidates:
        item = reference(candidate)
        ident = candidate['id']
        leading = item['leading'].subs(point)
        eta = item['eta'].subs(point)
        p = -leading.inv()*eta
        witness = point | dict(zip(PX, p))
        joint = item['joint'].subs(witness, simultaneous=True)
        omega = item['prolonged'].subs(witness, simultaneous=True)
        check(ident+'_consistent_rational_joint_jet', all(e == 0 for e in joint),
              {'point': point, 'p': p, 'determinant': leading.det()})
        if ident not in REGULAR_IDS:
            check(ident+'_direct_prolongation_counterexample', any(e != 0 for e in omega), omega)
            uniform = independent_uniform_obstruction(item, candidate['c'])
            check(ident+'_every_positive_parameter_pair', uniform is not None, uniform)
            rows.append({'id': ident, 'reference_status': 'fails_regular_joint_manifold',
                         'counterexample': {'point': point, 'p': p, 'prolonged': omega},
                         'uniform_parameter_obstruction': uniform})
            continue
        # Positive controls are identities, not mere zeroes at this point.
        if ident in {'C28', 'C31'}:
            beta = candidate['b'][0]
            remainder = (K*(3*u*u+v*v)*item['prolonged'][0]
                         -beta*(item['joint'][3]-2*K*v*item['joint'][2]))
            check(ident+'_global_nonvanishing_pivot_identity', sp.expand(remainder) == 0,
                  {'remainder': sp.expand(remainder), 'pivot': K*(3*u*u+v*v),
                   'strictly_positive_from_guards': True})
            check(ident+'_remaining_prolongation_components',
                  all(e == 0 for e in item['prolonged'][1:]), list(item['prolonged'][1:]))
            at_singular = item['joint'].subs({u: 0})
            # E_B = K v^2 u_x gives u_x=0 since speed!=0; E_h then equals beta.
            check(ident+'_singular_stratum_inconsistent',
                  at_singular[0].subs(PX[1], 0) == beta and beta != 0,
                  {'singular_mass_after_bed_constraint': at_singular[0].subs(PX[1], 0)})
            rows.append({'id': ident, 'reference_status': 'passes_all_consistent_joint_jets',
                         'singular_u0_status': 'empty_joint_stratum'})
        elif ident in {'C34', 'C37'}:
            p_symbolic = -item['leading'].inv()*item['eta']
            on_regular = item['prolonged'].subs(dict(zip(PX, p_symbolic)), simultaneous=True)
            check(ident+'_regular_identity', all(clean(e) == 0 for e in on_regular),
                  {'remainders': [clean(e) for e in on_regular], 'required_guard': 'u!=0'})
            beta = candidate['b'][1]
            singular = {g: 1, K: 1, h: 2, u: 0, v: 1, B: 3,
                        PX[0]: 1, PX[1]: 0, PX[2]: 0, PX[3]: -beta-1}
            sjoint = item['joint'].subs(singular, simultaneous=True)
            somega = item['prolonged'].subs(singular, simultaneous=True)
            check(ident+'_characteristic_negative_control',
                  all(e == 0 for e in sjoint) and any(e != 0 for e in somega),
                  {'point_and_jets': singular, 'joint': sjoint, 'prolonged': somega})
            rows.append({'id': ident, 'reference_status': 'regular_only_characteristic_failure',
                         'singular_counterexample': {'point_and_jets': singular,
                                                    'joint': sjoint, 'prolonged': somega}})
        else:
            check(ident+'_global_prolongation_identity', all(e == 0 for e in item['prolonged']),
                  item['prolonged'])
            rows.append({'id': ident, 'reference_status': 'passes_all_consistent_joint_jets',
                         'singular_status': 'same_zero_identity'})
    check('frozen_count_64_unique', len(candidates) == len({c['id'] for c in candidates}) == 64)
    check('independent_partition', len(REGULAR_IDS) == 13 and len(FULL_IDS) == 11)
    return {'checks': checks, 'candidates': rows}


def independent_solution_containment():
    """The accepted conditional families do not establish new solution classes."""
    beta = sp.Symbol('beta', real=True, nonzero=True)
    u0 = sp.Symbol('u0', real=True, nonzero=True)
    H0, V0, B0, U0 = sp.symbols('H0 V0 B0 U0', real=True)
    families = {
        'depth_shift': ((H0+beta*(t-x/u0), u0, V0, B0+beta*x/u0),
                        (1, u0, 0, 0, 0, 0, beta)),
        'velocity_shift': ((H0, U0+beta*t, V0, B0-beta*x/g),
                           (0, 1, 0, 0, 0, 0, -beta/g)),
    }
    rows = {}
    for name, (graph, vector) in families.items():
        sub = dict(zip(FIELDS, graph))
        for coordinate, jets in ((t, PT), (x, PX), (y, PY)):
            sub.update({jet: sp.diff(field, coordinate) for jet, field in zip(jets, graph)})
        residual = raw_pde().subs(sub, simultaneous=True).applyfunc(clean)
        characteristic = [clean(vector[i+3]-sum(vector[j]*sp.diff(graph[i], coordinate)
                           for j, coordinate in enumerate((t, x, y)))) for i in range(4)]
        rows[name] = {'graph': graph, 'classical_generator': vector,
                      'original_PDE_residuals': residual, 'classical_Q_residuals': characteristic,
                      'passed': all(e == 0 for e in (*residual, *characteristic))}
    return rows


def independent_distribution_intersection(candidate):
    """All classical tangent fields, not just membership of the proposed basis.

    A classical basis related by an invertible function-valued 2x2 matrix
    would supply two independent classical fields tangent to this same
    distribution. Polynomial splitting finds the entire tangent intersection.
    """
    constants = sp.symbols('T0 X0 Y0 Z0 rot at bx', real=True)
    T0, X0, Y0, Z0, rot, at, bx = constants
    classical = sp.Matrix([T0+at*t, X0+bx*x-rot*y, Y0+bx*y+rot*x,
                           2*(bx-at)*h, (bx-at)*u-rot*v,
                           (bx-at)*v+rot*u, Z0+2*(bx-at)*B])
    eta = sp.Matrix([ai*field+bi for ai, bi, field in
                     zip(candidate['a'], candidate['b'], FIELDS)])
    equations = [classical[1]-candidate['c']*classical[0]]
    equations += [classical[i+3]-classical[0]*eta[i] for i in range(4)]
    coefficients = [coefficient for equation in equations
                    for coefficient in sp.Poly(equation, t, x, y, *FIELDS).coeffs()]
    matrix, rhs = sp.linear_eq_to_matrix(coefficients, constants)
    assert all(e == 0 for e in rhs)
    kernel = matrix.nullspace()
    vectors = [classical.subs(dict(zip(constants, column)), simultaneous=True) for column in kernel]
    rank = sp.Matrix.hstack(*vectors).rank() if vectors else 0
    return {'tangent_classical_generators': vectors, 'intersection_rank': rank,
            'basis_change_invariant': True,
            'distribution_is_classically_generated': rank == 2}


def independent_export_check(candidate, certificate):
    """Differentiate the actual exponential graph before comparing its export."""
    rho = sp.Symbol('rho', positive=True)
    profile = sp.symbols('H U V Zb', real=True)
    slope = sp.symbols('H_z U_z V_z Zb_z', real=True)
    graph = []
    for ai, bi, fi in zip(candidate['a'], candidate['b'], profile):
        if ai:
            graph.append((fi+sp.Rational(bi, ai))*sp.exp(ai*t)-sp.Rational(bi, ai))
        else:
            graph.append(fi+bi*t)
    sub = dict(zip(FIELDS, graph))
    for index, field in enumerate(graph):
        dx = sum(sp.diff(field, fi)*pi for fi, pi in zip(profile, slope))
        sub[PX[index]] = dx
        sub[PT[index]] = sp.diff(field, t)-candidate['c']*dx
        sub[PY[index]] = 0
    original = raw_pde().subs(sub, simultaneous=True)
    exponent_map = {sp.exp(k*t): rho**k for k in range(-10, 11) if k}
    original = [sp.expand(e).subs(exponent_map, simultaneous=True) for e in original]
    lookup = {str(symbol): symbol for symbol in (g, K, t, rho, *profile, *slope)} | {'T': t}
    exported = [sp.sympify(e, locals=lookup) for e in certificate['pullback_PDE']]
    differences = [clean(a-b) for a, b in zip(original, exported)]
    reconstructed = [sum(sp.sympify(row['coefficient_must_vanish'], locals=lookup)
                          *rho**row['exp_rate']*t**row['time_power'] for row in equation)
                     for equation in certificate['profile_equations']]
    reconstruction_errors = [clean(a-b) for a, b in zip(original, reconstructed)]
    return {'original_PDE_pullback_remainders': differences,
            'time_coefficient_reconstruction_remainders': reconstruction_errors,
            'passed': all(e == 0 for e in (*differences, *reconstruction_errors))}


def reference_review():
    started = time.perf_counter()
    registry_path = HERE/'nonclassical_candidates.json'
    candidates = json.loads(registry_path.read_text(encoding='utf-8'))['candidates']
    result = independent_math(candidates)
    checks = result['checks']
    checks.append({'name': 'frozen_registry_hash', 'passed': hashlib.sha256(registry_path.read_bytes()).hexdigest() == FROZEN})
    families = independent_solution_containment()
    checks.extend({'name': name+'_classical_solution_containment', 'passed': row['passed'], 'evidence': row}
                  for name, row in families.items())
    intersections = {candidate['id']: independent_distribution_intersection(candidate) for candidate in candidates}
    checks.append({'name': 'independent_classical_distribution_partition',
                   'passed': sum(row['distribution_is_classically_generated'] for row in intersections.values()) == 9,
                   'evidence': intersections})
    return {**result, 'review_status': 'reference_only', 'all_checks_passed': all(row['passed'] for row in checks),
            'distribution_intersections': intersections, 'elapsed_seconds': time.perf_counter()-started}


def review(batch_path=None):
    started = time.perf_counter()
    import ml_adapter
    from gatekeeper import check_gate, check_hashes
    from nonclassical_runner import load_registry
    from stage2_runner import source_hashes

    batch = Path(batch_path or HERE/'runs'/'stage3-candidates-final').resolve()
    if not batch.is_relative_to(HERE):
        raise ValueError('Review batch must belong to this cycle')
    source_before = source_hashes()
    registry, gates = load_registry()
    run_path = batch/'receipts.json'
    run = json.loads(run_path.read_text(encoding='utf-8'))
    result = reference_review()
    checks = result['checks']
    def check(name, passed, evidence=None):
        checks.append({'name': name, 'passed': bool(passed), 'evidence': evidence})
    def zero(name, entries):
        values = [clean(value) for value in entries]
        check(name, all(value == 0 for value in values), values)
    def rejects(name, thunk):
        try:
            thunk()
        except ValueError:
            check(name, True)
        else:
            check(name, False, 'Expected ValueError was not raised')

    check('prior_classification_gates_current', all(row['passed'] for row in gates.values()), gates)
    check('batch_execution_current_complete', run.get('execution_passed') is True
          and run.get('candidate_count') == 64 and run.get('registry_sha256') == FROZEN
          and run.get('sources_unchanged_during_run') is True
          and run.get('source_hashes_before') == run.get('source_hashes_after') == source_before)
    process_rows = run.get('receipts', [])
    check('batch_unique_frozen_ids', len(process_rows) == 64
          and {row['candidate_id'] for row in process_rows} == {row['id'] for row in registry['candidates']})
    by_id = {row['candidate_id']: row for row in process_rows}
    lookup = {str(symbol): symbol for symbol in (t, x, y, *FIELDS, g, K)}
    for suffix, jets in (('t', PT), ('x', PX), ('y', PY)):
        lookup.update({f'{field}_{suffix}': jet for field, jet in zip(FIELDS, jets)})
    def parsed_matrix(data):
        return sp.Matrix([[sp.sympify(value, locals=lookup) for value in row] for row in data])

    expected_counts = {'verified_conditional_on_declared_chart': 11,
                       'verified_conditional_on_regular_subchart': 2,
                       'failed_conditional_criterion': 51}
    check('independent_status_counts_match_batch', run.get('conditional_status_counts') == expected_counts)
    evidence_paths = [run_path]
    export_rows = []
    for candidate in registry['candidates']:
        ident = candidate['id']
        reference_item = reference(candidate)
        record_path = batch/ident/'candidate.json'
        ml_path = batch/ident/'ml_certificate.json'
        log_path = batch/f'{ident}.log'
        evidence_paths.extend((record_path, ml_path, log_path))
        record = json.loads(record_path.read_text(encoding='utf-8'))
        certificate = json.loads(ml_path.read_text(encoding='utf-8'))
        process = by_id[ident]
        check(ident+'_bounded_successful_process', process.get('exit_code') == 0
              and process.get('process_status') == 'exited'
              and process.get('timeout_seconds') == 120
              and process.get('heavy_concurrency') == 1
              and process.get('cpu_lease') == 'cpu-symbolic'
              and Path(process['log']).resolve() == log_path
              and process.get('log_sha256') == hashlib.sha256(log_path.read_bytes()).hexdigest()
              and process.get('candidate.json_sha256') == hashlib.sha256(record_path.read_bytes()).hexdigest()
              and process.get('ml_certificate.json_sha256') == hashlib.sha256(ml_path.read_bytes()).hexdigest())
        check(ident+'_exact_frozen_candidate', record.get('candidate') == candidate
              and record.get('registry_sha256') == FROZEN)
        analysis = record['analysis']
        expected_status = ('verified_conditional_on_declared_chart' if ident in FULL_IDS else
                           'verified_conditional_on_regular_subchart' if ident in REGULAR_IDS else
                           'failed_conditional_criterion')
        check(ident+'_independently_derived_status', analysis['conditional_status'] == expected_status
              and record['mathematical_admission'] is (ident in REGULAR_IDS)
              and analysis['global_chart_admitted'] is (ident in FULL_IDS))
        system = analysis['joint_system']
        zero(ident+'_original_2D_equations_match', parsed_matrix(system['original_PDE'])-raw_pde())
        zero(ident+'_joint_PDE_Q_match', parsed_matrix(system['joint_first_order_equations'])-reference_item['joint'])
        zero(ident+'_direct_first_prolongation_match', parsed_matrix(system['prolonged_PDE_on_Q'])-reference_item['prolonged'])
        zero(ident+'_characteristic_determinant_match', [sp.sympify(system['determinant'], locals=lookup)-reference_item['determinant']])
        zero(ident+'_involutivity', parsed_matrix(system['involutivity_residual']))
        check(ident+'_projected_rank_two', analysis['distribution']['projection_rank'] == 2
              and sp.sympify(analysis['distribution']['projection_minor_t_y']) != 0)
        expected_singular = ('no_compatible_jets' if ident in {'C28', 'C31'} else
                             'failed_on_compatible_jets' if ident in {'C34', 'C37'} else
                             'all_compatible_jets_verified' if ident in FULL_IDS else
                             'not_resolved_for_rejected_candidate')
        check(ident+'_singular_scope_preserved', analysis['singular_status'] == expected_singular
              and analysis['singular_analysis']['implicit_DAE']['discarded'] is False)
        check(ident+'_graph_does_not_prove_conditional_invariance',
              analysis['invariant_graph']['conditional_invariance_inferred_from_graph'] is False)

        equivalence = record['classical_equivalence']
        intersection = result['distribution_intersections'][ident]
        check(ident+'_independent_classical_distribution_rank',
              equivalence['classical_equivalent'] is intersection['distribution_is_classically_generated']
              and equivalence['evaluated_classical_rank'] == intersection['intersection_rank']
              and equivalence['novel_solution_family_claim'] is False)
        if ident in {'C28', 'C31', 'C34', 'C37'}:
            contained = equivalence['solution_family_containment']
            check(ident+'_solution_family_is_classical',
                  contained['classical_solution_family_containment'] is True
                  and contained['full_local_candidate_solution_family_on_stated_chart'] is True
                  and contained['distribution_equality_on_these_graphs'] is False
                  and contained['novel_solution_family_claim'] is False)

        exported = independent_export_check(candidate, certificate)
        check(ident+'_independent_original_PDE_export', exported['passed'], exported)
        check(ident+'_ML_status_and_candidate_binding',
              certificate['candidate_id'] == ident
              and certificate['affine_coefficients'] == {key: candidate[key] for key in ('a', 'b', 'c')}
              and certificate['conditional_status'] == expected_status
              and certificate['conditional_admitted'] is (ident in REGULAR_IDS)
              and certificate['global_chart_admitted'] is (ident in FULL_IDS)
              and certificate['training_performed'] is False
              and certificate['learned_error_bound'] is False
              and certificate['independent_review'] == 'required_before_release'
              and certificate['certificate']['conditional_evidence']['candidate_sha256']
                  == hashlib.sha256(record_path.read_bytes()).hexdigest())
        values = (2.0, 3.0, 4.0, 5.0)
        current = ml_adapter.decode(candidate, 1/7, values)
        encoded = ml_adapter.encode(candidate, 1/7, 2/7, 3/7, current)
        check(ident+'_numeric_inverse_control', encoded['valid_domain'] is True
              and all(math.isclose(left, right, rel_tol=1e-12, abs_tol=1e-12)
                      for left, right in zip(values, encoded['profiles'])))
        if ident not in REGULAR_IDS:
            check(ident+'_failure_export_is_diagnostic', certificate['use'] == 'diagnostic_graph_only')
            rejects(ident+'_diagnostic_encode_rejected',
                    lambda: ml_adapter.encode_certificate(certificate, 0, 0, 0, (2, 3, 4, 5)))
        else:
            check(ident+'_admitted_certificate_encode',
                  ml_adapter.encode_certificate(certificate, 0, 0, 0, (2, 3, 4, 5))['valid_domain'] is True)
        if ident in {'C34', 'C37'}:
            check(ident+'_regular_chart_mask_enforced', 'u(t,z)!=0' in certificate['valid_domain_mask']
                  and ml_adapter.encode_certificate(certificate, 0, 0, 0, (2, 0, 1, 5))['valid_domain'] is False)
        export_rows.append({'candidate_id': ident, 'status': expected_status,
                            'independent_export_passed': exported['passed']})

    control = registry['candidates'][0]
    kwargs = {'equivalence_status': 'control', 'conditional_evidence': {'control': True}}
    rejects('ML_rejects_failed_status_promoted_to_success', lambda: ml_adapter.build_certificate(
        control, conditional_admitted=True, conditional_status='failed_conditional_criterion', **kwargs))
    rejects('ML_rejects_unknown_status', lambda: ml_adapter.build_certificate(
        control, conditional_admitted=False, conditional_status='unresolved', **kwargs))
    rejects('ML_rejects_missing_evidence', lambda: ml_adapter.build_certificate(
        control, conditional_admitted=True, conditional_status='verified_conditional_on_declared_chart',
        equivalence_status='control', conditional_evidence=None))
    for label, values, gravity, transport in (
        ('dry', (0, 1, 1, 0), 1, 1), ('zero_speed', (2, 0, 0, 0), 1, 1),
        ('bad_g', (2, 1, 1, 0), 0, 1), ('bad_K', (2, 1, 1, 0), 1, 0),
        ('nonfinite', (2, math.nan, 1, 0), 1, 1)):
        check('ML_domain_control_'+label,
              ml_adapter.encode(control, 0, 0, 0, values, gravity, transport)['valid_domain'] is False)

    required_sources = ('CONTRACT.md', 'models.py', 'models_2d.py', 'main.py',
        'nonclassical.py', 'NONCLASSICAL_DERIVATION.md', 'nonclassical_equivalence.py',
        'NONCLASSICAL_EQUIVALENCE.md', 'ml_adapter.py', 'ML_INPUTS.md',
        'nonclassical_runner.py', 'nonclassical_candidates.json', 'stage3_gate.py',
        'release.py', 'review_nonclassical.py', 'NONCLASSICAL_REVIEW.md',
        'tests/test_stage3_gate.py', 'tests/test_nonclassical.py',
        'tests/test_nonclassical_equivalence.py', 'tests/test_ml_adapter.py')
    inputs = {name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in required_sources}
    evidence_paths.extend((HERE/'STAGE_1_GATE.json', HERE/'STAGE_2_GATE.json'))
    evidence = {str(path.relative_to(HERE)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in evidence_paths}
    check('sources_unchanged_through_review', source_before == source_hashes())
    check('bound_inputs_current', not check_hashes(inputs) and not check_hashes(evidence))
    check('prior_gates_still_current', all(check_gate(stage)['passed'] for stage in (1, 2)))
    passed = all(row['passed'] for row in checks)
    return {**result, 'review_status': 'accepted' if passed else 'rejected',
            'all_checks_passed': passed, 'checks': checks, 'export_checks': export_rows,
            'inputs_sha256': inputs, 'evidence_sha256': evidence,
            'verdicts': {'conditional_criterion': 'accepted' if passed else 'rejected',
                         'classical_distribution_and_solution_distinction': 'accepted' if passed else 'rejected',
                         'ML_reconstruction_and_fail_closed_release': 'accepted' if passed else 'rejected'},
            'finite_candidate_count': 64, 'conditional_status_counts': expected_counts,
            'new_classically_inequivalent_solution_family_claim': False,
            'unrestricted_nonclassical_classification_claim': False,
            'training_performed': False, 'project_validation_required_separately': True,
            'elapsed_seconds': time.perf_counter()-started}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reference-only', action='store_true')
    parser.add_argument('--batch', type=Path, default=HERE/'runs'/'stage3-candidates-final')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = reference_review() if args.reference_only else review(args.batch)
    output = args.out or (HERE/'runs'/'stage3-review-preflight'/'reference.json' if args.reference_only
                          else HERE/'nonclassical_review.json')
    output = output.resolve()
    if not output.is_relative_to(HERE):
        raise ValueError('Review output must belong to this cycle')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(serial(result), indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'passed': result['all_checks_passed'], 'checks': len(result['checks']),
                      'elapsed_seconds': result['elapsed_seconds'],
                      'failures': [row['name'] for row in result['checks'] if not row['passed']]}))
    raise SystemExit(0 if result['all_checks_passed'] else 1)
