import sympy as sp
import pytest

from symm.generic import (
    CompletionCertificate,
    DifferentialBranch,
    DifferentialRanking,
    DifferentialSystem,
    GenericValidationError,
    JetSpace,
    PointGenerator,
    ReductionCertificate,
    legacy_generator_to_point,
    legacy_system,
    point_to_legacy,
)
from symm.sym_engine.jet import PDE


def test_jet_space_canonical_shape_and_names():
    x, y, t = sp.symbols("x y t")
    u, v = sp.symbols("u v")
    space = JetSpace((x, y, t), (u, v), 2)
    assert (space.p, space.q) == (3, 2)
    assert space.jet_symbol(0, (0, 0, 0)) == u
    assert space.jet_symbol(1, (1, 0, 0)) == sp.Symbol("v_x")
    assert space.jet_symbol(0, (1, 1, 0)) == sp.Symbol("u_xy")


def test_invalid_dimensions_are_rejected():
    x, u = sp.symbols("x u")
    with pytest.raises(GenericValidationError):
        JetSpace((x, x), (u,), 1)
    with pytest.raises(GenericValidationError):
        JetSpace((x,), (x,), 1)
    with pytest.raises(GenericValidationError):
        PointGenerator((1,), ())


def test_system_fingerprint_is_order_sensitive_and_stable():
    x, t, u = sp.symbols("x t u")
    space = JetSpace((x, t), (u,), 1)
    left = DifferentialSystem(space, (sp.Symbol("u_x"),), name="a")
    right = DifferentialSystem(space, (sp.Symbol("u_t"),), name="a")
    assert left.fingerprint() == left.fingerprint()
    assert left.fingerprint() != right.fingerprint()


def test_branch_and_generator_records_are_dimensioned():
    x, t, u = sp.symbols("x t u")
    generator = PointGenerator((1, 0), (0,))
    branch = DifferentialBranch(
        equations=(sp.Symbol("u_x"),),
        inequations=(sp.Symbol("a"),),
        leaders=((0, (1, 0)),),
        status="verified",
        provenance=(("source", "test"),),
    )
    assert generator.p == 2 and generator.q == 1
    assert branch.status == "verified"
    assert branch.as_dict()["leaders"] == [[0, [1, 0]]]
    assert DifferentialRanking().differentiation_compatible
    completion = CompletionCertificate(
        "system", "branch-partial", (branch,), DifferentialRanking(),
        checks=(("preserved", True),),
    )
    reduction = ReductionCertificate(
        "system", "unsupported", branch.branch_id,
        checks=(("pullback", False),), message="test",
    )
    assert completion.as_dict()["branches"][0]["branch_id"] == "branch-0"
    assert reduction.as_dict()["status"] == "unsupported"


def test_legacy_adapter_preserves_public_tuple_order():
    pde = PDE.scalar_1plus1(None, 1, "legacy", {})
    pde.Delta = pde.jet_sym(0, 1) - pde.jet_sym(1, 0)
    system = legacy_system(pde)
    assert (system.p, system.q, system.r) == (2, 1, 1)
    assert system.jet_space.independent_variables == (pde.x, pde.t)
    canonical = legacy_generator_to_point(pde, (pde.t, pde.x, pde.u))
    assert canonical.xi == (pde.x, pde.t)
    assert point_to_legacy(canonical) == (pde.t, pde.x, pde.u)
