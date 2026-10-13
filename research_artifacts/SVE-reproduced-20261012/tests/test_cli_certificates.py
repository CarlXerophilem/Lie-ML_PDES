import pytest

from main import parse_args, symbolic_certificate_summary


def valid_evidence():
    return {
        'models': {'checks': {name: True for name in (
            'mass_pullback_zero', 'momentum_pullback_zero',
            'printed_compatibility_zero', 'physical_compatibility_zero')},
            'physical_equals_printed': False,
            'discrepancies': [{'status': 'corrected_under_declared_bed_pullback'}]},
        'symmetries': {'checks': {
            **{name: {'passed': True} for name in ('X1', 'X2', 'X3', 'X4')},
            'X5': {'passed': True, 'm3_defect': '0', 'm4_defect_nonzero': True},
            'X6_m1': {'passed': True, 'm2_nonzero': True},
            'unrestricted_determining_split': {
                'passed': True,
                **{name: {'checked': True} for name in (
                    'free_y', 'free_w', 'free_a_b', 'free_a', 'free_x',
                    'm1_remaining_residual')}}},
            'discrepancies': {'printed_determining_X4_witness': {
                'status': 'refuted_as_printed'}}},
        'algebra': {'checks': {
            **{name: {'passed': 125, 'total': 125} for name in
               ('jacobi', 'm1_jacobi')},
            'antisymmetry': {'passed': 25, 'total': 25},
            'table_2': {'status': 'agrees','comparisons':{
                str(i):{'passed':True} for i in range(25)}}},
            'claims': {'source_optimal_system': {'status': 'refuted_incomplete'}}},
        'reductions':{'checks':{'passed':True},'source_witnesses':{
            f'eq{i}':{'audit_verified':True} for i in range(24,35)}},
    }


def test_all_named_certificates_pass_without_requiring_source_agreement():
    result = symbolic_certificate_summary(valid_evidence())
    assert result == {'passed': True, 'failures': []}


def test_false_symbolic_check_fails_with_named_label():
    evidence = valid_evidence()
    evidence['symmetries']['checks']['X3']['passed'] = False
    result = symbolic_certificate_summary(evidence)
    assert result['passed'] is False
    assert 'symmetries.checks.X3.passed' in result['failures']


def test_missing_required_check_fails_closed():
    evidence = valid_evidence()
    del evidence['models']['checks']['physical_compatibility_zero']
    del evidence['algebra']['checks']['table_2']
    result = symbolic_certificate_summary(evidence)
    assert result['passed'] is False
    assert 'models.checks.physical_compatibility_zero' in result['failures']
    assert 'algebra.checks.table_2.status' in result['failures']


def test_algebra_count_mismatch_fails():
    evidence = valid_evidence()
    evidence['algebra']['checks']['m1_jacobi']['passed'] = 124
    assert 'algebra.checks.m1_jacobi' in symbolic_certificate_summary(evidence)['failures']


def test_case_help_distinguishes_numerical_selector(capsys):
    with pytest.raises(SystemExit) as exc:
        parse_args(['--help'])
    assert exc.value.code == 0
    assert 'numerical exponent' in capsys.readouterr().out.lower()
