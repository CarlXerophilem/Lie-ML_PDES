import pytest
import sympy as sp
from models_2d import BRANCHES_2D,branch_model_2d,recover_one_dimension,f


@pytest.mark.parametrize('name',tuple(BRANCHES_2D))
def test_one_dimensional_restriction_has_exact_coriolis_boundary(name):
    from models import u
    result=recover_one_dimension(name)
    assert result['one_dimensional_residuals']==(0,0,0)
    if name.endswith('_f0'):
        assert result['recovered']
    else:
        assert not result['recovered']
        assert sp.simplify(result['transverse_residual']-f*u)==0


def test_slope_order_and_mixed_derivatives_are_generated_from_flux():
    from main import JetSpace
    from models_2d import G,u,v
    model=branch_model_2d('slope_attachment_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    bed=model['dependent_fields'][-1]
    assert J.order(model['equations'])==2
    for index in ((0,2,0),(0,0,2)):
        assert sp.simplify(sp.diff(model['equations'][-1],J.jet(bed,index))+G*(u*u+v*v))==0
