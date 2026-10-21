"""Independent regression checks for graph, chart and equation reductions."""
from pathlib import Path
import sys

import pytest
import sympy as sp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import JetSpace, graph_check
from models import BRANCHES, branch_model, t, x, h, u, B, g, K, G, m, n
from reductions import (traveling_reduction,scaling_reduction,constant_slope_graph,
                        initial_data_stabilizer,basis_combination)
from research_first_order import branch_generators
from research_slope import general_solution


COORDINATES = (t,x,h,u,B)


def solved_basis(branch):
    if BRANCHES[branch]["G"]:
        return general_solution(branch,COORDINATES)["basis"]
    return tuple(branch_generators(branch,COORDINATES).values())


@pytest.mark.parametrize("branch",tuple(BRANCHES))
def test_traveling_every_declared_branch_has_chain_chart_and_reconstruction(branch):
    result = traveling_reduction(branch_model(branch),solved_basis(branch))
    assert result["status"] == "verified_reduction", result
    assert result["chart_jacobian"] == 1
    assert all(v==0 for v in result["characteristic_residuals"])
    assert all(v==0 for v in result["reconstruction_residuals"])
    assert all(v==0 for v in result["chain_residuals"])
    assert result["leading_system"]["leading_matrix_inverted"] is False
    z = result["profile_coordinate"]
    H,U,Z = result["profiles"]
    c = result["generator"][1]
    # Independent conservation checks: mass and momentum are total derivatives
    # of traveling fluxes. The module never receives these formulas.
    expected_mass = sp.diff(H*(U-c),z)
    expected_momentum = sp.diff((U-c)**2/2+g*(H+Z),z)
    assert sp.simplify(result["reduced_equations"][0]-expected_mass)==0
    assert sp.simplify(result["reduced_equations"][1]-expected_momentum)==0
    cell = BRANCHES[branch]
    flux = K*U**cell["m"] if cell["K"] else sp.S.Zero
    if cell["G"]:
        flux -= G*U**cell["n"]*sp.diff(Z,z)
    expected_bed = sp.diff(flux-c*Z,z)
    assert sp.simplify(result["reduced_equations"][2]-expected_bed)==0


def test_traveling_extracts_actual_linear_combination_without_basis_order_assumption():
    basis = solved_basis("grass_cubic")
    changed = (basis[0]+2*basis[1],basis[0]-basis[1],*reversed(basis[2:]))
    result = traveling_reduction(branch_model("grass_cubic"),changed,speed=sp.Rational(2,3))
    assert result["status"] == "verified_reduction"
    assert result["basis_membership"]["weights"][:2] == (sp.Rational(5,9),sp.Rational(4,9))


def test_missing_translation_is_not_silently_added():
    basis = (sp.Matrix((0,1,0,0,0)),sp.Matrix((0,0,0,0,1)))
    result = traveling_reduction(branch_model("slope_only"),basis)
    assert result["status"] == "unresolved"
    assert "outside" in result["reason"]


@pytest.mark.parametrize("branch,selector,expected_chart",[
    ("grass_generic","common","time"),
    ("grass_cubic","common","time"),
    ("grass_cubic","spatial_amplitude","space"),
    ("grass_cubic","relative","time"),
    ("zero_transport","spatial_amplitude","space"),
    ("slope_attachment_cubic","last","space"),
    ("slope_source_cubic","last","time"),
])
def test_selected_diagonal_scalings_from_solved_basis(branch,selector,expected_chart):
    basis = solved_basis(branch)
    if selector == "last":
        selected = basis[-1]
    else:
        named = branch_generators(branch,COORDINATES)
        selected = named["common_base_scaling"]
        if selector == "spatial_amplitude":
            selected -= named["relative_scaling"]
        elif selector == "relative":
            selected = named["relative_scaling"]
    result = scaling_reduction(branch_model(branch),basis,selected)
    assert result["status"] == "verified_reduction", result
    assert result["selected_chart"] == expected_chart
    assert all(v==0 for v in result["invariant_residuals"])
    assert all(v==0 for v in result["reconstruction_residuals"])
    assert all(v==0 for v in result["characteristic_residuals"])
    assert result["chart_jacobian"] != 0


def test_symbolic_slope_exponent_requires_n2_chart_split():
    basis = solved_basis("slope_only")
    pending = scaling_reduction(branch_model("slope_only"),basis,basis[-1])
    assert pending["status"] == "unresolved"
    assert pending["required_split"] == (sp.Eq(n-2,0),sp.Ne(n-2,0))
    at_two = scaling_reduction(branch_model("slope_only"),basis,basis[-1],substitutions={n:2})
    assert at_two["status"] == "verified_reduction",at_two
    assert at_two["selected_chart"] == "space"
    assert sp.Gt(x,0) in at_two["chart_guards"]


def test_symbolic_n_time_chart_records_guard_and_exact_identities():
    basis = solved_basis("slope_only")
    result = scaling_reduction(branch_model("slope_only"),basis,basis[-1],chart="time")
    assert result["status"] == "verified_reduction",result
    assert sp.Ne(n-2,0,evaluate=False) in result["chart_guards"]
    assert sp.Gt(t,0) in result["chart_guards"]
    assert all(v==0 for v in result["reconstruction_residuals"])


def test_singular_chart_and_nonhomogeneous_fields_remain_unresolved():
    basis = solved_basis("slope_attachment_cubic")
    singular = scaling_reduction(branch_model("slope_attachment_cubic"),basis,basis[-1],chart="time")
    assert singular["status"] == "unresolved"
    shifted = basis[-1]+basis[0]
    unsupported = scaling_reduction(branch_model("slope_attachment_cubic"),basis,shifted)
    assert unsupported["status"] == "unresolved"
    assert "without additive" in unsupported["reason"]


def test_wrong_cubic_spatial_scaling_fails_for_n3_even_if_supplied_as_candidate_basis():
    fake = sp.Matrix((0,x,2*h,u,2*B))
    # Presence in an untrusted candidate list never replaces the PDE check.
    result = scaling_reduction(branch_model("slope_source_cubic"),(fake,),fake)
    assert result["status"] == "unresolved"


def test_reconstruction_against_direct_graph_differentiation_and_broken_ode():
    model = branch_model("slope_source_cubic")
    basis = solved_basis("slope_source_cubic")
    result = scaling_reduction(model,basis,basis[-1])
    assert result["status"] == "verified_reduction"
    direct = graph_check(JetSpace((t,x),(h,u,B)),model["equations"],result["graph"])
    z = result["profile_coordinate"]
    for original,weight,reduced in zip(direct["equation_residuals"],result["row_factors"],result["reduced_equations"]):
        assert sp.simplify(original-weight*reduced.subs(z,result["base_invariant"])) == 0
    broken = result["reduced_equations"][0]+1
    assert sp.simplify(direct["equation_residuals"][0]-result["row_factors"][0]*broken.subs(z,result["base_invariant"])) != 0


def test_singular_leading_matrices_are_preserved():
    stationary = traveling_reduction(branch_model("zero_transport"),solved_basis("zero_transport"),speed=0)
    assert stationary["status"] == "verified_reduction"
    assert stationary["leading_system"]["determinant"] == 0
    slope = traveling_reduction(branch_model("slope_source_cubic"),solved_basis("slope_source_cubic"))
    H,U,_ = slope["profiles"]
    c = slope["generator"][1]
    determinant = slope["leading_system"]["determinant"]
    assert sp.simplify(determinant+G*U**3*((U-c)**2-g*H))==0
    assert slope["leading_system"]["singular_locus_discarded"] is False


@pytest.mark.parametrize("branch",tuple(BRANCHES))
def test_constructed_constant_slope_solution_all_branches(branch):
    result = constant_slope_graph(branch_model(branch))
    assert result["status"] == "verified_exact_graph",result
    assert result["check"]["equation_residuals"] == [0,0,0]
    assert any(condition.has(t) for condition in result["guards"])


def test_fixed_uniform_initial_graph_stabilizer_does_not_keep_time_or_bed_translation():
    h0,u0 = sp.symbols("h0 u0",positive=True)
    b0 = sp.Symbol("b0",real=True)
    result = initial_data_stabilizer(branch_model("zero_transport"),solved_basis("zero_transport"),(h0,u0,b0))
    assert result["status"] == "verified_initial_graph_stabilizer",result
    solved = result["coefficient_solution"]
    assert solved[0] == solved[2] == solved[4] == 0
    assert solved[1] != 0 and solved[3] != 0
    assert result["verification_residuals"] == (0,0,0,0)
