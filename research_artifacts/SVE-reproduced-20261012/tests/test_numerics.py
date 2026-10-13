from pathlib import Path

import pytest

from main import original_pde_residual, run_campaign


def test_original_coordinate_residual_and_negative_control():
    good = original_pde_residual(lambda t, s: t + s, 1.0, 1.0, m=3, h=0.02)
    bad = original_pde_residual(lambda t, s: t + s + 0.001 * t ** 3,
                                1.0, 1.0, m=3, h=0.02)
    assert abs(good['residual']) < 1e-7
    assert bad['residual'] == pytest.approx(0.006, abs=1e-7)
    assert bad['residual'] - good['residual'] > 1e-3


def test_one_case_campaign_writes_evidence(tmp_path):
    report = run_campaign(tmp_path, selected_reduction='3.4', selected_case='1')
    assert len(report['runs']) == 1
    row = report['runs'][0]
    assert row['case'] == '3.4'
    assert row['m'] == 1
    assert row['solver']['status'] == 'completed'
    assert row['solver']['scaled_disagreement'] <= 1e-7
    assert row['solver']['tight_ladder_disagreement'] <= 1e-7
    assert row['pde']['status'] == 'passed'
    assert row['pde']['acceptance_h'] == 0.003
    assert row['pde']['trajectory'] == 'DOP853 reference reconstruction'
    assert row['negative_control']['passed']
    assert row['integral']['status'] == 'passed'
    assert row['second_order']['scaled_disagreement'] <= 1e-7
    assert row['branch']['min_abs_leading'] > 0
    assert Path(row['csv']).exists()
    assert Path(row['plot']).exists()


def test_nonregular_cases_are_typed(tmp_path):
    report = run_campaign(tmp_path, selected_reduction='3.2')
    assert report['runs'] == []
    assert report['non_numerical'][0]['status'] == 'undefined'


def test_incompatible_case_is_recorded(tmp_path):
    report = run_campaign(tmp_path, selected_reduction='3.5', selected_case='1')
    assert report['runs'] == []
    assert report['non_numerical'][0]['status'] == 'incompatible_exponent'


def test_linear_case_all_exponents_and_exact_quadratic(tmp_path):
    report = run_campaign(tmp_path, selected_reduction='3.8')
    assert [row['m'] for row in report['runs']] == [1, 1.5, 2, 3, 4]
    assert all(row['status'] == 'passed' for row in report['runs'])
    assert all(row['exact_quadratic']['max_abs_error'] < 1e-10
               for row in report['runs'])
    assert all(row['solver']['ladder_distinct_history'] for row in report['runs'])
