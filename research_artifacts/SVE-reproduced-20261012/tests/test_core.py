import sympy as sp


def test_master_matches_direct_differentiation():
    import main as j
    phi = j.t**2 + j.s + j.s**2 / 10 + j.t*j.s / 7
    subs = {jet: sp.diff(phi,j.t,ij[0],j.s,ij[1]) for ij,jet in j.JETS.items()}
    A = sp.diff(phi,j.s)*sp.diff(phi,j.t,2)-j.g*sp.diff(phi,j.s,2)/sp.diff(phi,j.s)**2
    T = j.g*3*j.kappa*sp.diff(sp.diff(phi,j.t)**2*sp.diff(phi,j.t,j.s)/sp.diff(phi,j.s),j.s)
    expected = sp.diff(A,j.t)-T
    assert sp.cancel(j.master(3).subs(subs, simultaneous=True)-expected)==0


def test_total_derivative_refuses_truncation():
    import main as j
    import pytest
    with pytest.raises(ValueError, match='jet order'):
        j.total(j.r,0)


def test_bracket_scaling_residual_is_relative_invariant():
    import main as j
    E=j.master(3)
    assert sp.expand(j.act(E,j.t,j.s,j.u)+2*E)==0
