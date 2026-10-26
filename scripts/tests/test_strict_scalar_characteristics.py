import sympy as sp
from symm.LieSymm.core import JetSpace
from scripts.strict_scalar_source_chains import derive_affine_characteristics


def test_scaling_characteristics_and_independent_pullback():
    t,x,u=sp.symbols('t x u',real=True)
    j=JetSpace((t,x),(u,))
    result=derive_affine_characteristics(j,j.jet(0,(1,0)),(t,x,u))
    assert result['invariant'] == x/t
    assert result['Q'] == 0
    assert result['reconstruction_residual'] == 0
    assert result['category'] == 'implicit_ODE_DAE'


def test_vertical_translation_has_no_invariant_graph():
    t,x,u=sp.symbols('t x u',real=True);j=JetSpace((t,x),(u,))
    assert derive_affine_characteristics(j,j.jet(0,(1,0)),(0,0,1))['category']=='no_invariant_graph'


def test_coordinate_singularity_is_not_an_ode():
    t,x,u=sp.symbols('t x u',real=True);j=JetSpace((t,x),(u,))
    result=derive_affine_characteristics(j,j.jet(0,(1,0))/j.jet(0,(0,1))**2,(0,1,0))
    assert result['category']=='undefined_PDE_chart'


def test_zero_action_does_not_exclude_graphs():
    t,x,u=sp.symbols('t x u',real=True);j=JetSpace((t,x),(u,))
    assert derive_affine_characteristics(j,j.jet(0,(1,0)),(0,0,0))['category']=='identity_action'


def test_integrated_characteristic_denominator_is_guarded():
    t,x,u,a,b=sp.symbols('t x u a b',real=True);j=JetSpace((t,x),(u,))
    result=derive_affine_characteristics(j,j.jet(0,(1,0)),(a*t+b,0,0))
    assert sp.Ne(a,0) in result['coefficient_guards']


def test_general_exponent_translation_pullback_uses_declared_positive_chart():
    from scripts.run_strict_lie import model
    definition=model('P:general')
    j=JetSpace(definition['independent_variables'],definition['dependent_fields'])
    alpha,beta=sp.symbols('alpha beta',real=True)
    result=derive_affine_characteristics(j,definition['equations'][0],(1,alpha,beta),positive_jet_chart=True)
    assert result['reconstruction_residual']==0
