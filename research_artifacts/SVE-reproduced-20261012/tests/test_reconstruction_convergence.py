import ast
from pathlib import Path

import numpy as np
import pytest
from scipy.interpolate import BPoly

import main as demo


@pytest.mark.parametrize('case', ['3.4', '3.5', '3.6', '3.8', '3.9'])
def test_reconstruction_matches_independent_polynomial_chain_rule(case):
    # F is a nonconstant polynomial so phi, velocity and reciprocal gradient
    # can be evaluated independently of the numerical ODE implementation.
    def F(z): return 2 + 0.5*z + 0.1*z*z
    def P(z): return 0.5 + 0.2*z
    knots = np.array([0., 2.])
    curve = BPoly.from_derivatives(knots, [[F(z), P(z), .2] for z in knots],
                                   extrapolate=False)
    tt, ss = .9, .7
    fields, valid = demo.reconstruct_profile_fields(case, curve, (0, 2),
                                                    np.array([tt]), np.array([ss]))
    def position(t, s):
        if case == '3.4': return t*F(s/t)
        if case == '3.5': return F(s*t*t)
        if case == '3.6': return F(s+t)
        if case == '3.9': return t+F(s+t)
        return s+F(t)
    h = 1e-5
    velocity = (position(tt+h,ss)-position(tt-h,ss))/(2*h)
    gradient = (position(tt,ss+h)-position(tt,ss-h))/(2*h)
    assert valid[0,0]
    assert fields['phi'][0,0] == pytest.approx(position(tt,ss), abs=1e-12)
    assert fields['u'][0,0] == pytest.approx(velocity, rel=1e-8)
    assert fields['h'][0,0] == pytest.approx(1/gradient, rel=1e-8)


def test_reconstruction_masks_extrapolation_and_nonpositive_chart():
    curve = BPoly.from_derivatives([1., 1.1], [[2., .5, .1], [2.0505, .51, .1]],
                                   extrapolate=False)
    fields, valid = demo.reconstruct_profile_fields('3.6', curve, (1,1.1),
                                                    np.array([0.]), np.array([.9,1.05,1.2]))
    assert valid.tolist() == [[False, True, False]]
    assert all(np.isnan(values[0,[0,2]]).all() for values in fields.values())
    negative = BPoly.from_derivatives([0., 2.], [[2.,-.5,0.],[1.,-.5,0.]],
                                      extrapolate=False)
    _, valid = demo.reconstruct_profile_fields('3.6', negative, (0,2),
                                               np.array([0.]), np.array([1.]))
    assert not valid.any()


def test_exact_nonpolynomial_order_control():
    control = demo._conv_exp_control()
    orders = [r['pairwise_order'] for r in control['fixed'] if r.get('pairwise_order') is not None]
    assert 4.8 < orders[-1] < 5.15


def test_unresolved_error_is_never_used_to_infer_order():
    rows = [{'h':.2,'error':1e-10,'resolved':True},
            {'h':.1,'error':0.,'resolved':False}]
    demo._conv_order(rows, 'h')
    assert rows[-1]['pairwise_order'] is None


def test_quadratic_reference_uses_time_since_initial_point(monkeypatch):
    import time
    monkeypatch.setitem(demo.NUMERICAL_CASE_SETTINGS, '3.8',
                        ((.2, .6), (0., 1., .1)))
    row = demo._conv_one('3.8', 3, time.monotonic()+10)
    assert row['status'] == 'completed'
    assert row['reference']['endpoint'] == pytest.approx([.408, 1.04, .1])
    assert max(x['error'] for x in row['fixed']) < 1e-12


def test_main_has_no_local_implementation_dependency_or_source_exec():
    tree = ast.parse(Path(demo.__file__).read_text(encoding='utf-8'))
    assert not any(isinstance(n, ast.ImportFrom) and
                   (n.level or (n.module or '').startswith('sve_reproduce'))
                   for n in ast.walk(tree))
    assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                   and n.func.id in ('exec', 'eval') for n in ast.walk(tree))
