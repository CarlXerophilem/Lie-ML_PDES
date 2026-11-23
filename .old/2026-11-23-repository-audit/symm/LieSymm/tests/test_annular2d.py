"""Independent signs, chart guards, and negative controls for full E."""

import importlib
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
import sympy as sp


def api():
    name = "symm.LieSymm.annular2d"
    assert importlib.util.find_spec(name) is not None, "annular full-E case is not implemented"
    return importlib.import_module(name)


@pytest.fixture(scope="module")
def case():
    return api().build_case()


@pytest.fixture(scope="module")
def exact():
    return api().certify_case()


def test_registry_and_generic_model_have_identical_cartesian_equations(case):
    assert case.registry_residuals == (0, 0, 0, 0)
    h, u, v, bed = case.system.jet_space.dependent_fields
    j = case.system.jet_space.jet_symbol
    g, K, G, f, c = case.parameters
    assert sp.expand(case.system.equations[1] - (
        j(1, (1, 0, 0)) + u*j(1, (0, 1, 0)) + v*j(1, (0, 0, 1))
        + g*(j(0, (0, 1, 0)) + j(3, (0, 1, 0))) - f*v)) == 0
    assert sp.expand(sp.diff(case.system.equations[3], j(3, (0, 2, 0)))+G*(u*u+v*v)) == 0


def test_all_six_generators_have_covariant_certificates(exact):
    assert exact["status"] == "verified-local-subalgebra-and-reduction"
    assert set(exact["symmetries"]) == {"T", "X", "Y", "A", "J", "D"}
    assert all(record["verified"] for record in exact["symmetries"].values())
    assert all(record["two_prolongation_forms_agree"] for record in exact["symmetries"].values())
    assert exact["symmetries"]["J"]["raw_off_shell_zero"] is False
    assert exact["maximal_classification_claim"] is False


def test_actual_rotation_prolongation_mixes_velocity_and_spatial_jets(case, exact):
    j = case.system.jet_space.jet_symbol
    coefficients = exact["symmetries"]["J"]["prolongation"]
    assert coefficients[(0, (0, 1, 0))] == -j(0, (0, 0, 1))
    assert coefficients[(1, (0, 1, 0))] == -j(2, (0, 1, 0))-j(1, (0, 0, 1))
    assert coefficients[(3, (0, 2, 0))] == -2*j(3, (0, 1, 1))
    assert coefficients[(3, (0, 1, 1))] == j(3, (0, 2, 0))-j(3, (0, 0, 2))


def test_brackets_and_adjoint_use_the_actual_sign_convention(exact):
    algebra = exact["algebra"]
    assert algebra["closure_status"] == "closed"
    assert algebra["structure_constants"][4][1] == (0, 0, -1, 0, 0, 0)
    assert algebra["structure_constants"][4][2] == (0, 1, 0, 0, 0, 0)
    assert algebra["structure_constants"][5][3] == (0, 0, 0, -2, 0, 0)
    eps = algebra["adjoint_parameter"]
    adjoint = algebra["adjoints"]["J"]
    assert sp.simplify(adjoint[1, 1]-sp.cos(eps)) == 0
    assert sp.simplify(adjoint[2, 1]+sp.sin(eps)) == 0


def test_spatial_only_rotation_is_rejected_by_original_momentum(case):
    a = api()
    from symm.generic import PointGenerator, prolonged_system
    t, x, y = case.system.jet_space.independent_variables
    wrong = PointGenerator((0, -y, x), (0, 0, 0, 0))
    lhs = prolonged_system(case.system, wrong)
    residuals = sp.Matrix(lhs)-case.multipliers["J"]*sp.Matrix(case.system.equations)
    assert any(sp.expand(value) != 0 for value in residuals)
    assert a.certify_generator(case, wrong, case.multipliers["J"])["verified"] is False


def test_two_stage_library_reduction_matches_independent_radial_odes(exact):
    reduction = exact["reduction"]
    assert reduction["time_certificate"].status == "verified"
    assert reduction["rotation_certificate"].status == "verified"
    assert reduction["projection_rank"] == 2
    assert reduction["commutator"] == (0, 0, 0, 0, 0, 0, 0)
    r, H, V, W, Z, g, K, G, f, c = reduction["symbols"]
    Hp, Vp, Wp, Zp, Zpp = reduction["derivatives"]
    wanted = (
        V*Hp + H*Vp + H*V/r,
        V*Vp-W**2/r-f*W+g*(Hp+Zp),
        V*(Wp+W/r+f),
        c+(V**2+W**2)*(K*V-G*Zp)/r
        +2*(V*Vp+W*Wp)*(K*V-G*Zp)+(V**2+W**2)*(K*Vp-G*Zpp),
    )
    assert all(sp.simplify(a-b) == 0 for a, b in zip(reduction["equations"], wanted))
    assert reduction["cartesian_pullback_residuals"] == (0, 0, 0, 0)
    assert all(value == 0 for value in reduction["invariant_surface_residuals"])


def test_bed_evolution_sign_error_is_visible_in_cartesian_pullback(exact):
    reduction = exact["reduction"]
    c = reduction["symbols"][-1]
    assert sp.simplify(reduction["opposite_bed_sign_residual"]+2*c) == 0
    assert reduction["opposite_bed_sign_residual"] != 0


def test_three_first_integrals_are_functionally_independent_on_recorded_chart(exact):
    reduction = exact["reduction"]
    r,H,V,W,Z,g,K,G,f,c = reduction["symbols"]
    assert reduction["first_integral_residuals"] == (0,0,0)
    assert sp.factor(reduction["first_integral_independence_determinant"]+r**3*G*V*(V**2+W**2)) == 0


def test_constant_zero_coriolis_is_a_supported_separate_case():
    a = api()
    case = a.build_case(coriolis=0)
    assert case.registry_residuals == (0, 0, 0, 0)
    assert a.certify_generator(case, case.generators["J"], case.multipliers["J"])["verified"]


@pytest.mark.parametrize("replacement", [
    {"r": 0}, {"H": 0}, {"V": 0}, {"G": 0}, {"g": -1},
    {"H": 4}, {"c": 0}, {"W": float("nan")},
])
def test_singular_or_out_of_chart_profile_data_are_rejected(replacement):
    data = dict(r=1, H=1, V=2, W=.3, Z=0, P=.9, g=1, K=.05, G=.1, f=.2, c=.02)
    data.update(replacement)
    with pytest.raises(ValueError):
        api().profile_rhs(data["r"], [data[k] for k in ("H", "V", "W", "Z", "P")],
                          **{k: data[k] for k in ("g", "K", "G", "f", "c")})


def test_regular_profile_rhs_obeys_original_undivided_radial_equations():
    a = api()
    r, H, V, W, Z, P = 1., 1., 2., .3, 0., .9
    g, K, G, f, c = 1., .05, .1, .2, .02
    Hp, Vp, Wp, Zp, Pp = a.profile_rhs(r, (H,V,W,Z,P), g=g,K=K,G=G,f=f,c=c)
    S = V*V+W*W
    residuals = (
        V*Hp+H*Vp+H*V/r,
        V*Vp-W*W/r-f*W+g*(Hp+P),
        V*(Wp+W/r+f),
        c+S*(K*V-G*P)/r+2*(V*Vp+W*Wp)*(K*V-G*P)+S*(K*Vp-G*Pp),
        Zp-P,
    )
    assert np.max(np.abs(residuals)) < 1e-13


def test_numerical_profile_has_guarded_cross_solver_and_cartesian_checks():
    report = api().solve_profile()
    assert report["status"] == "verified-sampled-numerical-profile"
    assert report["cross_solver_max_abs_error"] < 1e-8
    assert report["minimum_H"] > 0
    assert report["minimum_V"] > 0
    assert report["minimum_abs_characteristic_pivot"] > 0
    assert max(report["first_integral_max_drifts"].values()) < 1e-9
    assert report["cartesian_finite_difference_checks"][-1]["max_abs_residual"] < 1e-6
    assert report["continuous_error_bound_claim"] is False


def test_profile_plot_writes_nonblank_png_and_pdf_from_actual_samples(tmp_path):
    a = api()
    assert hasattr(a,"write_profile_plot"), "numerical-profile plot writer is not implemented"
    paths = a.write_profile_plot(a.solve_profile(),tmp_path)
    from PIL import Image
    with Image.open(paths[0]) as image:
        assert image.width >= 1000 and image.height >= 500
        assert np.asarray(image.convert("RGB")).std() > 20
    assert paths[1].read_bytes().startswith(b"%PDF-")


def test_cli_writes_complete_source_and_receipt_hash_manifest(tmp_path):
    root = Path(__file__).resolve().parents[3]
    result = subprocess.run([sys.executable,"-B","-X","utf8","-m","symm.LieSymm.annular2d",
                             "--out",str(tmp_path)],cwd=root,
                            env=dict(os.environ,MPLBACKEND="Agg"),capture_output=True,text=True,timeout=90)
    assert result.returncode == 0, result.stdout+result.stderr
    manifest = json.loads((tmp_path/"manifest.json").read_text(encoding="utf-8"))
    for relative,digest in manifest["source_sha256"].items():
        assert hashlib.sha256((root/relative).read_bytes()).hexdigest() == digest
    for relative,digest in manifest["receipts_sha256"].items():
        assert hashlib.sha256((tmp_path/relative).read_bytes()).hexdigest() == digest
