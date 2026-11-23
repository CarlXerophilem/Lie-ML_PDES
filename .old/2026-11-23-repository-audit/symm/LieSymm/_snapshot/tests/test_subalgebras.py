"""Line-orbit coverage, resonance and actual-adjoint regression checks."""
from pathlib import Path
import sys

import pytest
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from models import BRANCHES,t,x,h,u,B,n
from research_first_order import branch_generators
from research_slope import general_solution
from subalgebras import (adjoint_structure,classify_subalgebra_lines,adjoint_action,
                        canonicalize_translation_line)

COORDINATES=(t,x,h,u,B)


def basis_for(branch):
    if BRANCHES[branch]["G"]:
        return general_solution(branch,COORDINATES)["basis"]
    return tuple(branch_generators(branch,COORDINATES).values())


def classified(branch):
    options={"parameter":n,"domain":sp.Interval(0,4)} if branch=="slope_only" else {}
    return classify_subalgebra_lines(COORDINATES,basis_for(branch),**options)


@pytest.mark.parametrize("branch",tuple(BRANCHES))
def test_all_declared_algebras_have_separate_certified_line_orbit_cover(branch):
    result=classified(branch)
    assert result["status"]=="certified_line_orbit_classification",result
    assert result["maximal_point_algebra_claim"] is False
    for cell in result["strata"]:
        assert cell["coverage_status"]=="proved_exhaustive_for_connected_inner_line_orbits"
        for family in cell["families"]:
            assert family["coefficients"]!=sp.zeros(len(result["structure"]["basis"]),1)
            assert all(v==0 for v in family["normalizer"]["verification_residuals"])


def test_adjoint_sign_convention_matches_actual_cubic_generator():
    structure=adjoint_structure(COORDINATES,basis_for("slope_source_cubic"))
    D=structure["scaling_indices"][0]
    T,X,Z=structure["translation_indices"]
    eps=sp.Symbol("eps",real=True)
    left=sp.zeros(4,1);left[D]=1
    target=sp.zeros(4,1);target[T]=1;target[X]=2;target[Z]=3
    actual=adjoint_action(structure,left,target,eps)
    expected=sp.zeros(4,1)
    expected[T]=sp.exp(-eps);expected[X]=2*sp.exp(-2*eps);expected[Z]=3*sp.exp(-2*eps)
    assert actual==expected


def test_abelian_translation_algebra_retains_projective_continuous_moduli():
    cell=classified("slope_source_generic")["strata"][0]
    assert len(cell["families"])==13
    full=[f for f in cell["families"] if len(f["support"])==3]
    assert len(full)==4
    assert all(f["normalizer"]["continuous_moduli"]==2 for f in full)
    assert all(len(f["parameters"])==2 for f in full)


def test_generic_grass_central_bed_component_cannot_be_normalized_to_sign_only():
    cell=classified("grass_generic")["strata"][0]
    mixed=[f for f in cell["families"] if f["kind"]=="nonzero_A_line"]
    assert len(mixed)==3
    nonzero=[f for f in mixed if f["support"]]
    assert len(nonzero)==2
    assert all(f["normalizer"]["rank"]==0 for f in nonzero)
    assert all(len(f["parameters"])==1 for f in nonzero)
    equal_weight_pair=[f for f in cell["families"] if f["kind"]=="translation_line" and f["support"]==(0,1)]
    assert all(f["normalizer"]["continuous_moduli"]==1 for f in equal_weight_pair)


def test_symbolic_slope_resonances_include_zero_weights_and_equal_weights():
    result=classified("slope_only")
    generic=result["strata"][0]
    assert generic["excluded_resonances"]==(1,2,3,4)
    cells={next(iter(c["substitutions"].values())):c for c in result["strata"][1:]}
    assert set(cells)=={1,2,3,4}
    for exponent,expected_kernel in ((1,(1,)),(2,(0,))):
        families=[f for f in cells[exponent]["families"] if f["kind"]=="nonzero_A_line"]
        assert all(f["kernel"]==expected_kernel for f in families)
        assert len(families)==3
    for exponent,support in ((3,(1,2)),(4,(0,2))):
        families=[f for f in cells[exponent]["families"] if f["kind"]=="translation_line" and f["support"]==support]
        assert all(f["normalizer"]["continuous_moduli"]==1 for f in families)
    full=[f for f in generic["families"] if f["kind"]=="translation_line" and len(f["support"])==3]
    y=sp.Matrix(sp.symbols("yT yX yB",real=True))
    invariant=full[0]["normalizer"]["invariant_projection"]*y
    assert sp.simplify(invariant[2]-((3-n)*y[0]+(n-4)*y[1]+y[2]))==0


def test_two_scaling_directions_and_exceptional_lines_are_derived_from_weight_kernels():
    result=classified("grass_cubic")
    cell=result["strata"][0]
    mixed=[f for f in cell["families"] if f["kind"]=="nonzero_A_line"]
    assert len(mixed)==10
    generic=[f for f in mixed if f["A_direction"]["parameters"]]
    assert len(generic)==1
    assert generic[0]["kernel"]==()
    exceptions=[f for f in mixed if f["A_direction"].get("a_ratio") in (0,-1)]
    assert len(exceptions)==6
    infinity=[f for f in mixed if f["A_direction"]["label"]=="infinite A direction"]
    assert len(infinity)==3
    for f in mixed:
        if f["support"]:
            assert f["normalizer"]["continuous_moduli"]==0
    translations=[f for f in cell["families"] if f["kind"]=="translation_line"]
    assert len(translations)==13
    assert all(f["normalizer"]["continuous_moduli"]==0 for f in translations)


@pytest.mark.parametrize("branch",["grass_cubic","grass_generic","slope_attachment_cubic","slope_source_cubic"])
def test_exact_translation_orbit_witness_uses_matrix_exponential(branch):
    structure=adjoint_structure(COORDINATES,basis_for(branch))
    vector=sp.zeros(len(structure["basis"]),1)
    for index,value in zip(structure["translation_indices"],(2,-3,5)):
        vector[index]=value
    first=canonicalize_translation_line(structure,vector)
    assert first["status"]=="verified_orbit_witness",first
    scaling=sp.zeros(len(vector),1)
    for index in structure["scaling_indices"]:
        scaling[index]=sp.log(2)
    moved=-3*adjoint_action(structure,scaling,vector)
    second=canonicalize_translation_line(structure,moved)
    assert second["status"]=="verified_orbit_witness",second
    assert all(sp.simplify(a-b)==0 for a,b in zip(first["canonical_coefficients"],second["canonical_coefficients"]))


def test_translation_adjoint_eliminates_only_nonzero_eigenvalue_components():
    structure=adjoint_structure(COORDINATES,basis_for("grass_cubic"))
    v_indices,a_indices=structure["translation_indices"],structure["scaling_indices"]
    vector=sp.zeros(5,1)
    for index,value in zip(v_indices,(6,-5,8)):
        vector[index]=value
    for index,value in zip(a_indices,(1,2)):
        vector[index]=value
    eigenvalues=structure["weights"]*sp.Matrix([1,2])
    shift=sp.zeros(5,1)
    for index,lam in zip(v_indices,eigenvalues):
        shift[index]=vector[index]/lam
    matrix=sum((shift[i]*A for i,A in enumerate(structure["adjoint_matrices"])),sp.zeros(5))
    assert matrix*matrix==sp.zeros(5)
    moved=adjoint_action(structure,shift,vector)
    assert all(moved[i]==0 for i in v_indices)
    assert tuple(moved[i] for i in a_indices)==(1,2)


def test_unequal_continuous_invariants_are_not_collapsed_to_one_representative():
    structure=adjoint_structure(COORDINATES,basis_for("slope_source_cubic"))
    one=canonicalize_translation_line(structure,sp.Matrix([1,1,2,0]))
    two=canonicalize_translation_line(structure,sp.Matrix([1,1,3,0]))
    assert one["canonical_coefficients"]!=two["canonical_coefficients"]
    assert one["canonical_coefficients"]==sp.Matrix([1,1,2,0])
    assert two["canonical_coefficients"]==sp.Matrix([1,1,3,0])


def test_undeclared_parameter_and_unsupported_algebra_return_unresolved():
    missing=classify_subalgebra_lines(COORDINATES,basis_for("slope_only"))
    assert missing["status"]=="unresolved"
    not_closed=(sp.Matrix([1,0,0,0,0]),sp.Matrix([0,t,0,0,0]))
    unsupported=classify_subalgebra_lines(COORDINATES,not_closed)
    assert unsupported["status"]=="unresolved"


def test_permuted_basis_does_not_change_weight_geometry_or_line_count():
    original=basis_for("grass_cubic")
    permuted=(original[4],original[1],original[3],original[2],original[0])
    result=classify_subalgebra_lines(COORDINATES,permuted)
    assert result["status"]=="certified_line_orbit_classification"
    assert len(result["strata"][0]["families"])==23
