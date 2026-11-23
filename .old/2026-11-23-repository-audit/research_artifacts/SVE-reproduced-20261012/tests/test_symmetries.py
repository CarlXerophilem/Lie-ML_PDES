import json

import sympy as sp

import main as j
from main import build_symmetry_report, generators, split_weight_identity


def test_every_listed_generator_has_direct_off_shell_identity():
    E = j.master()
    X = generators()
    for name, factor in [('X1', 0), ('X2', 0), ('X3', 0), ('X4', -2)]:
        assert sp.simplify(j.act(E, *X[name]) - factor * E) == 0
    assert sp.simplify(j.act(E, *X['X5']) + E - split_weight_identity()) == 0
    assert sp.simplify(split_weight_identity().subs(j.m, 3)) == 0
    assert sp.simplify(split_weight_identity().subs(j.m, 4)) != 0


def test_printed_determining_system_rejects_its_own_x4():
    report = build_symmetry_report()
    witness = report['discrepancies']['printed_determining_X4_witness']
    assert witness['value'] == '6'
    assert witness['status'] == 'refuted_as_printed'
    classification = report['claims']['maximal_classification']
    assert classification['status'] == 'proved_on_declared_branch'
    assert classification['dimensions'] == {'m=1': 5, 'm=3': 5, 'm>=1,m!=1,3': 4}
    assert report['checks']['unrestricted_determining_split']['passed']
    json.dumps(report)


def test_m1_extra_vertical_boost_is_exact_and_non_generic():
    X = generators()
    assert sp.simplify(j.act(j.master(1), *X['X6'])) == 0
    assert sp.simplify(j.act(j.master(2), *X['X6'])) != 0
