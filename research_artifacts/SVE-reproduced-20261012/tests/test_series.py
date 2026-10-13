import json
import csv
import hashlib

import pytest
import sympy as sp

import main as j


@pytest.mark.parametrize('case,exponent', [
    ('3.4', sp.Rational(3, 2)), ('3.5', 3),
    ('3.6', sp.Rational(3, 2)), ('3.8', 3), ('3.9', 3),
])
def test_exact_regular_series_satisfies_corrected_residual(case, exponent):
    row = j.compute_ode_series(case, exponent=exponent, order=6)
    assert row['status'] == 'regular_analytic_germ'
    assert len(row['coefficients']) == 7
    assert all(not value.atoms(sp.Float) for value in row['coefficients'])
    assert row['verification']['passed']
    assert row['verification']['through_degree'] == 3
    assert row['verification']['residual_coefficients'] == [0, 0, 0, 0]


def test_independent_polynomial_substitution_into_corrected_residual():
    row = j.compute_ode_series('3.5',order=4)
    h = sp.Symbol('h',real=True)
    polynomial = row['polynomial']
    residual = j.derive_reduction('3.5')['residual'].subs(
        {j.g:1,j.kappa:sp.Rational(1,30)})
    substituted = residual.subs({j.z:1+h,j.F:polynomial,
        j.P:sp.diff(polynomial,h),j.C:sp.diff(polynomial,h,2),
        j.H:sp.diff(polynomial,h,3)},simultaneous=True)
    assert sp.simplify(sp.series(substituted,h,0,2).removeO()) == 0


def test_quadratic_is_exact_and_nonzero_center_works():
    quadratic = j.compute_ode_series('3.8', order=6)
    h = sp.Symbol('h', real=True)
    assert sp.simplify(quadratic['polynomial']-(h+h*h/20)) == 0
    assert quadratic['coefficients'][3:] == [0, 0, 0, 0]
    shifted = j.compute_ode_series('3.4', exponent=sp.Rational(3, 2),
                                   z0=sp.Rational(6, 5), order=5)
    assert shifted['status'] == 'regular_analytic_germ'
    assert shifted['z0'] == sp.Rational(6, 5)
    assert shifted['verification']['through_degree'] == 2


@pytest.mark.parametrize('case,status', [
    ('3.1', 'outside_positive_chart'), ('3.2', 'undefined_chart'),
    ('3.3', 'no_invariant_graph'), ('3.7', 'identity_family'),
])
def test_nonregular_rows_are_typed(case, status):
    row = j.compute_ode_series(case)
    assert row['status'] == status
    assert row['polynomial'] is None


def test_parameter_and_singular_strata_are_not_divided_through():
    assert j.compute_ode_series('3.5', exponent=2)['status'] == 'incompatible_parameter'
    assert j.compute_ode_series('3.6')['alpha3'] == 0
    assert j.compute_ode_series('3.6',alpha3=1)['status'] == 'incompatible_parameter'
    assert j.compute_ode_series('3.6', alpha=0)['status'] == 'outside_positive_chart'
    assert j.compute_ode_series('3.9', alpha=0, alpha3=1)['status'] == 'identity_family'
    assert j.compute_ode_series('3.8', alpha=0)['status'] == 'undefined_chart'
    singular = j.compute_ode_series('3.6', exponent=3, g_value=sp.Rational(10,81))
    assert singular['status'] == 'normal_form_singular'
    assert singular['leading_at_initial'] == 0
    assert j.compute_ode_series('3.4', initial_jet=(2,0,sp.Rational(1,10)))['status'] == 'outside_positive_chart'


def test_small_and_non_near_rational_floats_are_not_silently_changed():
    assert j._series_rational(1e-9) == sp.Rational(1,10**9)
    value = 0.12345678912345678
    assert j._series_rational(value) == sp.Rational(str(value))
    assert j._series_rational(sp.Float('1e-9')) == sp.Rational(1,10**9)
    row = j.compute_ode_series('3.8',initial_jet=(0,1e-9,0))
    assert row['status'] == 'regular_analytic_germ'
    assert row['initial_jet'][1] == sp.Rational(1,10**9)


def test_x4_can_start_at_negative_invariant_coordinate():
    row = j.compute_ode_series('3.4',z0=-1,order=4)
    assert row['status'] == 'regular_analytic_germ'
    assert row['z0'] == -1


def test_campaign_writes_nine_statuses_and_21_ivps(tmp_path):
    report = j.run_series_campaign(tmp_path, order=4, compare_dir=None)
    assert len(report['regular_runs']) == 21
    assert all(r['status'] == 'regular_analytic_germ' for r in report['regular_runs'])
    assert len(report['nine_rows']) == 9
    assert report['nine_rows']['3.2']['status'] == 'undefined_chart'
    saved = json.loads((tmp_path/'series.json').read_text(encoding='utf-8'))
    assert saved['regular_count'] == 21
    assert (tmp_path/'series_trace.txt').exists()


def _quadratic_reference(tmp_path):
    row = j.compute_ode_series('3.8',order=4)
    path = tmp_path/'3-8-m3.csv'
    with path.open('w',newline='',encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(('z','F_rkf45','P_rkf45','C_rkf45',
                         'F_dop853','P_dop853','C_dop853'))
        for index in range(81):
            t = index*.005
            values = (t+t*t/20,1+t/10,.1)
            writer.writerow((t,*values,*values))
    record = {'case':'3.8','m':3,'g':1.,'kappa':1/30,
              'interval':[0.,.4],'initial_jet':[0.,1.,.1],
              'model':'printed scalar','status':'passed',
              'equation_sha256':j._ode_fingerprint(j.derive_reduction('3.8',alpha=1)),
              'csv_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    metadata = tmp_path/'numerics.json'
    metadata.write_text(json.dumps({'runs':[record]}),encoding='utf-8')
    return row,path,metadata,record


def test_series_reference_requires_matched_problem_and_bound_csv(tmp_path):
    row,path,metadata,record = _quadratic_reference(tmp_path)
    checked = j._series_grid_comparison(row,path)
    assert checked['status'] == 'existing_grid_nodes_only'
    assert len(checked['samples']) == 4
    assert max(max(s['abs_error_vs_dop853']) for s in checked['samples']) < 1e-14
    # Even an exactly matching quadratic curve cannot validate a different
    # model-parameter receipt; equations sharing a solution are not identical.
    record['g'] = 2.
    metadata.write_text(json.dumps({'runs':[record]}),encoding='utf-8')
    stale = j._series_grid_comparison(row,path)
    assert stale['status'] == 'reference_metadata_mismatch'
    assert stale['samples'] == []
    record['g'] = 1.
    record['equation_sha256'] = 'different-corrected-equation'
    metadata.write_text(json.dumps({'runs':[record]}),encoding='utf-8')
    assert j._series_grid_comparison(row,path)['samples'] == []


def test_series_reference_rejects_unbound_or_modified_data(tmp_path):
    row,path,metadata,record = _quadratic_reference(tmp_path)
    path.write_bytes(path.read_bytes()+b'\n')
    changed = j._series_grid_comparison(row,path)
    assert changed['status'] == 'reference_metadata_mismatch'
    assert 'csv_bytes' in changed['failed_checks']
    assert changed['samples'] == []
    metadata.unlink()
    assert j._series_grid_comparison(row,path)['status'] == 'reference_provenance_unavailable'


@pytest.mark.parametrize('bad_value', ['not-a-number', 'nan', 'inf'])
def test_series_reference_rejects_malformed_but_hash_bound_grid(tmp_path,bad_value):
    row,path,metadata,record = _quadratic_reference(tmp_path)
    with path.open(newline='',encoding='utf-8') as handle:
        rows = list(csv.reader(handle))
    rows[41][4] = bad_value
    with path.open('w',newline='',encoding='utf-8') as handle:
        csv.writer(handle).writerows(rows)
    record['csv_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    metadata.write_text(json.dumps({'runs':[record]}),encoding='utf-8')
    result = j._series_grid_comparison(row,path)
    assert result['status'] == 'reference_grid_invalid'
    assert result['samples'] == []
