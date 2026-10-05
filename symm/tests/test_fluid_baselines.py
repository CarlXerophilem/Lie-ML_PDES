"""Independent analytic controls and conservation checks for remote baselines."""
import numpy as np
import pytest
import sympy as sp

from symm.fluid_baselines.models import sve_scaling, fluid_translation, exact_control_residuals
from symm.fluid_baselines.numerics import sve_periodic, sve_reduced, vorticity_evolution
from symm.generic import reduce_in_chart


def test_original_sve_cubic_reduction_and_noncubic_rejection():
    problem, generator, chart, matrix = sve_scaling(3)
    result = reduce_in_chart(problem, generator, chart, symmetry_multipliers=matrix)
    assert result.certificate.status == "verified"
    H, V, C = chart.reduced_space.dependent_fields
    d = lambda i: chart.reduced_space.jet_symbol(i, (1,))
    g, kappa = problem.parameters
    expected = (d(0)+3*H*V,
                H*d(1)+V*d(0)+4*H*V**2+2*g*H*(H+C),
                d(2)+3*kappa*V**3)
    assert all(sp.expand(a-b) == 0 for a,b in zip(result.reduced_system.equations, expected))
    for m in (2, 4):
        p, gen, c, M = sve_scaling(m)
        rejected = reduce_in_chart(p, gen, c, symmetry_multipliers=M)
        assert rejected.certificate.status == "unsupported"
        assert not dict(rejected.certificate.checks)["symmetry_identity"]


@pytest.mark.parametrize("linear", [False, True])
def test_two_dimensional_fluid_translation(linear):
    problem, generator, chart, M = fluid_translation(linear)
    result = reduce_in_chart(problem, generator, chart, symmetry_multipliers=M)
    assert result.certificate.status == "verified"
    assert result.reduced_system.jet_space.p == 2
    assert result.reduced_system.equations[-1] == chart.reduced_space.jet_symbol(1, (0,1))


def test_controls_satisfy_original_equations_symbolically():
    residuals = exact_control_residuals()
    assert set(residuals) == {"sve_cubic", "taylor_green", "shear"}
    assert all(r == 0 for system in residuals.values() for r in system)


def test_sve_fv_preserves_periodic_integrals_and_positive_depth():
    run = sve_periodic(n=64, m=4, kappa=.1, end=.1, snapshots=3)
    assert run["metrics"]["mass_relative_drift"] < 1e-12
    assert run["metrics"]["bed_mean_absolute_drift"] < 1e-12
    assert np.min(run["fields"]["h"]) > .9


def test_reduced_sve_against_independent_closed_form():
    run = sve_reduced(kappa=.1, end=1.3, snapshots=5)
    t = run["times"][:,None]
    x = run["x"][None,:]
    assert np.max(np.abs(run["fields"]["h"]-x*x/(15*t*t))) < 1e-9
    assert np.max(np.abs(run["fields"]["u"]-2*x/(3*t))) < 1e-9


@pytest.mark.parametrize("kind", ["taylor_green", "shear"])
def test_fourier_ns_against_analytic_decay(kind):
    run = vorticity_evolution(n=24, nu=.1, kind=kind, end=.2, snapshots=3)
    assert run["metrics"]["exact_velocity_max_error"] < 1e-8
    assert run["metrics"]["divergence_max"] < 1e-12
    assert np.diff(run["diagnostics"]["kinetic energy"]).max() <= 1e-12


def test_oseen_matches_independent_fourier_semigroup():
    run = vorticity_evolution(n=24, nu=.05, kind="interacting", mean=(.3,-.2),
                              linear=True, end=.2, snapshots=3)
    assert run["metrics"]["exact_vorticity_max_error"] < 1e-8

