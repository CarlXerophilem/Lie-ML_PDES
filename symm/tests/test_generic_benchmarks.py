import sympy as sp

from symm.generic import (
    JetSpace,
    PointGenerator,
    benchmark_registry,
    navier_stokes_2d,
    orbit_rank,
    parameter_branches,
    validate_registry,
)
from symm.generic.jets import multi_index_count


def test_registry_covers_required_shapes():
    reports = validate_registry()
    assert all(report["shape_ok"] for report in reports)
    assert all(report["status"] == "verified" for report in reports)
    assert any(report["shape"][2] != report["shape"][1] for report in reports)


def test_navier_stokes_structural_gate_and_known_residuals():
    case = navier_stokes_2d()
    assert (case.system.p, case.system.q, case.system.r) == (3, 3, 3)
    assert 3 * multi_index_count(3, 2) == 30
    report = next(item for item in validate_registry() if item["name"] == case.name)
    assert report["known_generator_residuals_ok"]
    assert all(value == 0 for values in report["known_generator_residuals"].values() for value in values)


def test_parameter_and_rank_drop_metadata_remain_visible():
    regular, singular = parameter_branches()
    assert regular.system.inequations == (sp.Symbol("a"),)
    assert singular.system.assumptions == (sp.Eq(sp.Symbol("a"), 0),)
    rank_case = next(item for item in benchmark_registry() if item.name == "rank-dropping-rotation")
    generator = rank_case.known_generators[0][1]
    assert orbit_rank(rank_case.system.jet_space, (generator,)) == 1
    origin = PointGenerator(tuple(value.subs({sp.Symbol("x"): 0, sp.Symbol("y"): 0})
                                 for value in generator.xi), generator.phi)
    assert orbit_rank(rank_case.system.jet_space, (origin,)) == 0
    assert rank_case.rank_guards == (sp.Symbol("x")**2 + sp.Symbol("y")**2,)
