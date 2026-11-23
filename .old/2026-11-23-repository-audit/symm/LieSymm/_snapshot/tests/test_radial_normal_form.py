import sympy as sp
from radial_normal_form import normalize


def test_radial_euler_identity_without_component_sign_assumptions():
    u,v,a=sp.symbols('u v a',real=True)
    S=u*u+v*v
    residual=u*u*S**(a-1)+v*v*S**(a-1)-S**a
    assert normalize(residual,u,v)==0


def test_normalization_preserves_a_real_nonzero_obstruction():
    u,v,m=sp.symbols('u v m',real=True)
    S=u*u+v*v
    expression=(m-3)*(u*u*S**((m-3)/2)+v*v*S**((m-3)/2))
    normalized=normalize(expression,u,v)
    assert normalized!=0
    for exponent in (1,sp.Rational(3,2),3,4):
        for velocity in ((0,2),(-2,0),(-3,4)):
            assert sp.simplify((normalized-expression).subs({m:exponent,u:velocity[0],v:velocity[1]}))==0
