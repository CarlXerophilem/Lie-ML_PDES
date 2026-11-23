import json

import sympy as sp

from main import adjoint, bracket, build_algebra_report, orbit_invariants
from main import generators


def test_bracket_antisymmetry_and_source_table_one_errors():
    X = generators()
    assert bracket(X['X1'], X['X5']) == X['X1']
    assert bracket(X['X5'], X['X1']) == tuple(-v for v in X['X1'])
    assert bracket(X['X2'], X['X5']) == tuple(-2*v for v in X['X2'])
    assert bracket(X['X5'], X['X2']) == tuple(2*v for v in X['X2'])


def test_adjoint_uses_paper_negative_ad_convention():
    eps = sp.symbols('eps', real=True)
    assert adjoint('X1', 'X4', eps) == {'X1': -eps, 'X4': sp.Integer(1)}
    assert adjoint('X4', 'X1', eps) == {'X1': sp.exp(eps)}
    assert adjoint('X5', 'X2', eps) == {'X2': sp.exp(-2*eps)}


def test_all_jacobi_triples_and_missing_orbit_invariants():
    report = build_algebra_report()
    assert report['checks']['jacobi']['passed'] == 125
    assert report['checks']['table_2']['status'] == 'agrees'
    assert report['discrepancies']['table_1']['wrong_cells'] == ['[X5,X1]', '[X5,X2]']
    assert orbit_invariants()['generic']['translation_projective_dimension'] == 2
    assert len(orbit_invariants()['exceptional']['resonant_directions']) == 3
    assert report['checks']['m1_jacobi']['passed'] == 125
    assert report['discrepancies']['m1_missing_generator']['generator'] == 'X6=t*d_phi'
    json.dumps(report)


def test_m1_boost_algebra_is_nonabelian_in_translation_pair():
    X = generators()
    assert bracket(X['X1'], X['X6']) == X['X3']
    assert bracket(X['X4'], X['X6']) == (sp.Integer(0),)*3
