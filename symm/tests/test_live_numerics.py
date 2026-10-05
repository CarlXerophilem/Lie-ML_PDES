"""State continuity, batch parity, and independent physical controls."""
from io import BytesIO
import json

import numpy as np
import pytest

from symm.fluid_baselines.live_numerics import make_stepper
from symm.fluid_baselines.numerics import sve_periodic, vorticity_evolution


@pytest.mark.parametrize("model", ["ns", "oseen", "sve"])
def test_repeated_advances_match_batch_solver(model):
    if model == "sve":
        params = {"m": 3.5, "kappa": .15, "g": 1.2}
        batch = sve_periodic(n=32, end=.12, snapshots=7, **params)
    else:
        params = {"nu": .08}
        mean = (.3, -.2) if model == "oseen" else (0., 0.)
        if model == "oseen":
            params.update(a=mean[0], b=mean[1])
        batch = vorticity_evolution(n=32, nu=params["nu"], mean=mean,
                                    linear=model == "oseen", end=.12, snapshots=7)
    live = make_stepper(model, n=32, parameters=params)
    assert isinstance(live.t, float) and live.t == 0.
    assert isinstance(live.params, dict) and live.params == params
    assert live.model == model and live.kind == "interacting" and live.n == 32
    assert live.dimension == batch["dimension"]
    assert isinstance(live.state, np.ndarray)
    np.testing.assert_array_equal(live.x, batch["x"])
    if model == "sve":
        assert live.y is None and live.state.shape == (3, 32)
    else:
        np.testing.assert_array_equal(live.y, batch["y"])
        assert live.state.shape == (32, 32) and live.state.dtype == np.complex128
    for index, target in enumerate(batch["times"]):
        live.advance_to(target)
        assert live.t == float(target)
        fields = live.fields()
        assert fields.keys() == batch["fields"].keys()
        for name, field in fields.items():
            assert field.dtype == np.float64
            np.testing.assert_allclose(field, batch["fields"][name][index],
                                       rtol=0, atol=3e-14)
        diagnostic = live.diagnostics()
        assert diagnostic and all(np.isfinite(value) for value in diagnostic.values())
        assert 0 <= diagnostic["spectral_tail_ratio"] <= 1


@pytest.mark.parametrize("model", ["ns", "oseen", "sve"])
def test_zero_perturbation_clones_are_identical_and_independent(model):
    live = make_stepper(model, n=24)
    live.advance_to(.07)
    clone = live.clone()
    assert not np.shares_memory(live.state, clone.state)
    assert not np.shares_memory(live.x, clone.x)
    if live.y is not None:
        assert not np.shares_memory(live.y, clone.y)
    clone.set_parameters(live.params.copy())
    for target in (.11, .2):
        live.advance_to(target)
        clone.advance_to(target)
        np.testing.assert_array_equal(live.state, clone.state)
        assert live.diagnostics() == clone.diagnostics()
    clone.set_parameters({"g": 2.} if model == "sve" else {"nu": .2})
    assert live.params != clone.params
    original = live.state.copy()
    clone.state.flat[0] += 1
    np.testing.assert_array_equal(live.state, original)
    saved = live.state.copy()
    for field in live.fields().values():
        field[:] = 0
    np.testing.assert_array_equal(live.state, saved)


@pytest.mark.parametrize("model,updates", [
    ("ns", {"nu": .15}), ("oseen", {"nu": .15}),
    ("oseen", {"a": -.8}), ("oseen", {"b": .9}),
    ("sve", {"m": 2.5}), ("sve", {"kappa": .3}), ("sve", {"g": 2.}),
])
def test_parameter_change_preserves_state_then_changes_future(model, updates):
    control = make_stepper(model, n=24)
    control.advance_to(.08)
    perturbed = control.clone()
    before = perturbed.state.copy()
    fields_before = perturbed.fields()
    perturbed.set_parameters(updates)
    assert perturbed.t == control.t == .08
    np.testing.assert_array_equal(perturbed.state, before)
    for name, field in perturbed.fields().items():
        np.testing.assert_array_equal(field, fields_before[name])
    for key, value in updates.items():
        assert perturbed.params[key] == value
    control.advance_to(.2)
    perturbed.advance_to(.2)
    assert np.max(np.abs(control.state - perturbed.state)) > 1e-8


@pytest.mark.parametrize("model,mean", [("ns", (0., 0.)), ("oseen", (.3, -.2))])
def test_long_shear_with_piecewise_viscosity_matches_analytic_solution(model, mean):
    live = make_stepper(model, n=24, kind="shear")
    for target in (.2, .201, 1., 3.7, 20.):
        live.advance_to(target)
        integrated_nu = .01 * min(target, .2) + .2 * max(target - .2, 0.)
        decay = np.exp(-integrated_nu)
        phase = live.y[:, None] - mean[1] * target
        expected_w = np.broadcast_to(decay * np.sin(phase), (24, 24))
        expected_u = np.broadcast_to(mean[0] + decay * np.cos(phase), (24, 24))
        fields = live.fields()
        np.testing.assert_allclose(fields["vorticity"], expected_w, rtol=0, atol=2e-10)
        np.testing.assert_allclose(fields["u"], expected_u, rtol=0, atol=2e-10)
        np.testing.assert_allclose(fields["v"], mean[1], rtol=0, atol=2e-12)
        assert live.diagnostics()["spectral_tail_ratio"] < 1e-20
        if target == .2:
            before = live.state.copy()
            live.set_parameters({"nu": .2})
            np.testing.assert_array_equal(live.state, before)
    assert live.t == 20.


def test_oseen_drift_change_advects_existing_field_with_fixed_velocity_mean():
    live = make_stepper("oseen", n=32, parameters={"nu": .05})
    live.advance_to(.2)
    before = live.fields()
    live.set_parameters({"a": -.7, "b": .8})
    for name, field in live.fields().items():
        np.testing.assert_array_equal(field, before[name])
    live.advance_to(1.)
    X, Y = np.meshgrid(live.x, live.y)
    # Each Fourier mode advects by the time integral of drift and decays at nu*|k|^2.
    X = X - (.3 * .2 - .7 * .8)
    Y = Y - (-.2 * .2 + .8 * .8)
    expected = (2 * np.exp(-.1) * np.sin(X) * np.sin(Y) +
                np.exp(-.25) * (np.cos(2 * X) * np.cos(Y) + .75 * np.sin(X) * np.cos(2 * Y)))
    fields = live.fields()
    np.testing.assert_allclose(fields["vorticity"], expected, rtol=0, atol=2e-8)
    assert abs(fields["u"].mean() - .3) < 1e-14
    assert abs(fields["v"].mean() + .2) < 1e-14


def test_oseen_cfl_includes_large_advection_coefficients_at_low_viscosity():
    live = make_stepper("oseen", n=256, parameters={"nu": .0005, "a": 2., "b": 2.})
    X, Y = np.meshgrid(live.x, live.y)
    live.state[:] = np.fft.fft2(1e-4 * np.cos(84 * (X + Y)))
    live.advance_to(.1)
    expected = 1e-4 * np.exp(-.0005 * 2 * 84**2 * .1) * np.cos(84 * (X + Y - 4 * .1))
    np.testing.assert_allclose(live.fields()["vorticity"], expected, rtol=0, atol=1e-6)


@pytest.mark.parametrize("model", ["ns", "oseen"])
def test_high_viscosity_retained_modes_respect_rk_bound_and_strict_mask(model):
    live = make_stepper(model, n=48, parameters={"nu": 1.}, kind="shear")
    # The corner (15, 15) is retained; |kx|=16 is strictly excluded.
    X, Y = np.meshgrid(live.x, live.y)
    live.state[:] = np.fft.fft2(np.sin(15 * (X + Y)))
    live.advance_to(.04)
    mean = (.3, -.2) if model == "oseen" else (0., 0.)
    expected = np.exp(-450 * live.t) * np.sin(15 * (X + Y - sum(mean) * live.t))
    np.testing.assert_allclose(live.fields()["vorticity"], expected, rtol=0, atol=3e-10)
    k = np.fft.fftfreq(live.n, 1 / live.n)
    excluded = (abs(k[:, None]) >= 16) | (abs(k[None, :]) >= 16)
    assert np.count_nonzero(live.state[excluded]) == 0


def test_taylor_green_initialization_and_decay():
    live = make_stepper(n=24, kind="taylor_green", parameters={"nu": .1})
    live.advance_to(.3)
    X, Y = np.meshgrid(live.x, live.y)
    expected = 2 * np.sin(X) * np.sin(Y) * np.exp(-.2 * live.t)
    np.testing.assert_allclose(live.fields()["vorticity"], expected, rtol=0, atol=1e-11)


def test_noninteger_sve_remains_positive_and_conserves_mass_and_mean_bed():
    live = make_stepper("sve", n=32, parameters={"m": 2.5})
    means = live.state[[0, 2]].mean(axis=1)
    for target in (.1, .5, 1.):
        live.advance_to(target)
        np.testing.assert_allclose(live.state[[0, 2]].mean(axis=1), means, rtol=0, atol=2e-14)
        assert live.fields()["h"].min() > 0 and live.fields()["u"].min() > 0
        assert live.diagnostics()["mass_relative_drift"] < 2e-14
        live.set_parameters({"m": 3.7, "kappa": .2})


@pytest.mark.parametrize("component,value", [(0, 0.), (0, -1.), (1, 0.), (1, -.1), (2, np.nan)])
def test_sve_rejects_invalid_positive_power_branch_without_clipping(component, value):
    live = make_stepper("sve", n=24, parameters={"m": 2.5})
    live.state[component, 0] = value
    before = live.state.copy()
    with pytest.raises(RuntimeError):
        live.advance_to(.01)
    assert live.t == 0.
    np.testing.assert_array_equal(live.state, before)


@pytest.mark.parametrize("model", ["ns", "oseen", "sve"])
def test_tail_ratio_distinguishes_low_modes_from_unresolved_tail(model):
    live = make_stepper(model, n=24)
    assert live.diagnostics()["spectral_tail_ratio"] < 1e-20
    if model == "sve":
        live.state[0] = 1 + .03 * np.cos(10 * live.x)
        live.state[1] = .4 * live.state[0]
        live.state[2] = 0
    else:
        live.state[:] = np.fft.fft2(np.sin(6 * live.y)[:, None] * np.ones((1, 24)))
    assert live.diagnostics()["spectral_tail_ratio"] > .99
    if model == "sve":
        live.state[:] = np.array([1., .4, 0.])[:, None]
    else:
        live.state[:] = 0
    assert live.diagnostics()["spectral_tail_ratio"] == 0.


PARAMETER_BOUNDS = [
    ("ns", "nu", .0005, 1.), ("oseen", "nu", .0005, 1.),
    ("oseen", "a", -2., 2.), ("oseen", "b", -2., 2.),
    ("sve", "m", .5, 6.), ("sve", "kappa", 0., 1.), ("sve", "g", .1, 10.),
]


@pytest.mark.parametrize("model,key,lower,upper", PARAMETER_BOUNDS)
def test_parameter_bounds_are_inclusive_and_updates_are_atomic(model, key, lower, upper):
    live = make_stepper(model, n=24)
    live.advance_to(.02)
    for value in (lower, upper):
        live.set_parameters({key: value})
        assert live.params[key] == value
    params, before, time = live.params.copy(), live.state.copy(), live.t
    for value in (np.nextafter(lower, -np.inf), np.nextafter(upper, np.inf),
                  np.nan, np.inf, -np.inf, "0.1", None, True, 1j, [lower]):
        with pytest.raises(ValueError):
            live.set_parameters({key: value})
        with pytest.raises(ValueError):
            make_stepper(model, n=24, parameters={key: value})
        assert live.params == params and live.t == time
        np.testing.assert_array_equal(live.state, before)
    with pytest.raises(ValueError):
        live.set_parameters({key: lower, "unknown": 1.})
    assert live.params == params
    other = {"nu": .1, "a": .2} if model == "oseen" else {key: lower}
    if model == "oseen":
        other["b"] = np.nan
    else:
        other["unknown"] = .2
    with pytest.raises(ValueError):
        live.set_parameters(other)
    assert live.params == params


@pytest.mark.parametrize("n", [0, 16, 25, 28, 264, 64.5, 64., True, np.nan, np.inf, "64"])
def test_grid_validation(n):
    with pytest.raises(ValueError):
        make_stepper(n=n)


@pytest.mark.parametrize("n", [24, 64, 128, 256, np.int64(32)])
def test_supported_grids(n):
    live = make_stepper(n=n)
    assert live.state.shape == (n, n)


@pytest.mark.parametrize("kwargs", [
    {"model": "bad"}, {"kind": "bad"}, {"model": "sve", "kind": "shear"},
    {"parameters": {"a": .1}}, {"parameters": []}, {"parameters": {"nu": np.nan}},
    {"model": "sve", "parameters": {"nu": .1}},
])
def test_invalid_configuration(kwargs):
    with pytest.raises(ValueError):
        make_stepper(**kwargs)


@pytest.mark.parametrize("model", ["ns", "oseen", "sve"])
def test_target_validation_exact_boundary_and_noop(model):
    live = make_stepper(model, n=24)
    # A sub-tolerance interval must not silently skip the state update.
    live.advance_to(1e-15)
    assert live.t == 1e-15 and live.diagnostics()["steps"] == 1
    live.advance_to(.037123456789)
    before, time, diagnostics = live.state.copy(), live.t, live.diagnostics()
    live.advance_to(time)
    np.testing.assert_array_equal(live.state, before)
    assert live.diagnostics() == diagnostics
    for target in (time - 1e-15, -1., np.nan, np.inf, -np.inf, True, "1", None):
        with pytest.raises(ValueError):
            live.advance_to(target)
        assert live.t == time
        np.testing.assert_array_equal(live.state, before)


def test_nonfinite_fourier_state_is_rejected():
    live = make_stepper(n=24)
    live.state[0, 0] = np.nan
    with pytest.raises(RuntimeError):
        live.advance_to(.01)
    assert live.t == 0.


@pytest.mark.parametrize("model,updates", [
    ("ns", {"nu": .2}), ("oseen", {"nu": .05, "a": -.7, "b": .8}),
    ("sve", {"m": 2.7, "kappa": .3, "g": 1.2}),
])
def test_checkpoint_needs_only_public_state_and_constructor_metadata(model, updates):
    live = make_stepper(model, n=32)
    live.advance_to(.08)
    live.set_parameters(updates)
    live.advance_to(.123)
    # Same JSON metadata / full-precision NumPy storage as the hosted controller.
    meta = {key: getattr(live, key) for key in ("t", "params", "steps", "n", "model", "kind")}
    with BytesIO() as stream:
        np.savez_compressed(stream, metadata=json.dumps(meta), state=live.state)
        stream.seek(0)
        with np.load(stream, allow_pickle=False) as checkpoint:
            saved = json.loads(checkpoint["metadata"].item())
            restored = make_stepper(saved["model"], n=saved["n"], kind=saved["kind"],
                                    parameters=saved["params"])
            restored.state = checkpoint["state"].copy()
            restored.t, restored.steps = saved["t"], saved["steps"]
    assert restored.diagnostics() == live.diagnostics()
    for target in (.2, .35):
        live.advance_to(target)
        restored.advance_to(target)
        np.testing.assert_array_equal(restored.state, live.state)
        assert restored.diagnostics() == live.diagnostics()


def test_interacting_ns_energy_and_enstrophy_decay_through_time_ten():
    live = make_stepper(n=64)
    previous = live.diagnostics()
    for target in np.arange(.5, 10.01, .5):
        live.advance_to(target)
        current = live.diagnostics()
        assert all(np.isfinite(value) for value in current.values())
        assert current["kinetic_energy"] <= previous["kinetic_energy"] + 1e-12
        assert current["enstrophy"] <= previous["enstrophy"] + 1e-12
        assert current["divergence_max"] < 1e-12
        assert abs(current["vorticity_mean"]) < 1e-12
        assert 0 <= current["spectral_tail_ratio"] <= 1
        previous = current
    assert live.t == 10.
    assert live.steps >= 1000  # Explicit RK4 cap stays at .01 even late in decay.


def test_sve_stage_failure_leaves_last_accepted_state_and_clone_intact():
    saved = make_stepper("sve", n=24, parameters={"m": 2.5})
    failing = saved.clone()
    # Valid positive h/u at entry, but this steep bed reverses u in the first stage.
    failing.state[2] = 100 * np.cos(failing.x)
    before = failing.state.copy()
    with pytest.raises(RuntimeError, match="positive-velocity"):
        failing.advance_to(.01)
    np.testing.assert_array_equal(failing.state, before)
    assert failing.t == 0. and failing.steps == 0
    saved.advance_to(.01)
    assert saved.t == .01
