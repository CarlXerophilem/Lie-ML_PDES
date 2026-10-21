import pytest
import sympy as sp
from models_2d import BRANCHES_2D,branch_model_2d,g,K,G,f
from reductions_2d import plane_wave,rotating_radial,rotation_scaling_time_ode


@pytest.mark.parametrize('name',('grass_generic_f0','slope_source_generic_f_nonzero','slope_only_f0'))
def test_plane_wave_removes_two_base_variables_with_transverse_profile(name):
    result=plane_wave(name)
    assert result['status']=='verified_ode_reduction'
    assert result['projection_rank']==2
    assert len(result['profiles'])==4
    assert result['reconstruction_residuals']==(0,0,0,0)


@pytest.mark.parametrize('name',('grass_generic_f0','slope_source_generic_f_nonzero','slope_only_f0'))
def test_single_rotation_leaves_a_radial_pde(name):
    result=rotating_radial(name)
    assert result['status']=='verified_pde_reduction',result
    assert result['projection_rank']==1
    assert len(result['reduced_independent_variables'])==2
    assert result['ode_claim'] is False
    assert result['reconstruction_residuals']==(0,0,0,0)


@pytest.mark.parametrize('name',tuple(BRANCHES_2D))
def test_time_ode_closes_only_when_actual_spatial_scaling_is_admitted(name):
    result=rotation_scaling_time_ode(name)
    cell=BRANCHES_2D[name]
    admits=(not cell['K'] or cell['m']==3) and (not cell['G'] or cell['n']==2)
    if admits:
        assert result['status']=='verified_ode_reduction',result
        assert result['projection_rank']==2
        assert result['reconstruction_residuals']==(0,0,0,0)
    else:
        assert result['status']=='generator_not_admitted'
        assert not result['generator_checks'][1]['verified']


def test_cubic_attachment_time_ode_contains_swirl_coriolis_and_slope_flux():
    result=rotation_scaling_time_ode('slope_attachment_cubic_f_nonzero')
    H,A,W,Z=result['profiles']
    t=result['reduced_independent_variables'][0]
    expected=(sp.diff(H,t)+4*A*H,
              sp.diff(A,t)+A*A-W*W-f*W+2*g*(H+Z),
              sp.diff(W,t)+2*A*W+f*A,
              sp.diff(Z,t)+4*(A*A+W*W)*(K*A-2*G*Z))
    assert all(sp.simplify(a-b)==0 for a,b in zip(result['reduced_equations'],expected))


def test_space_rotation_without_velocity_rotation_is_rejected():
    from main import JetSpace,verify_generator
    model=branch_model_2d('grass_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    t,x,y=J.x
    bad=verify_generator(J,model['equations'],(0,-y,x),(0,0,0,0))
    assert not bad['verified']


@pytest.mark.parametrize('speed',[sp.I,sp.oo,sp.nan])
def test_plane_wave_rejects_nonreal_or_nonfinite_speed(speed):
    with pytest.raises(ValueError,match='finite and real'):
        plane_wave('grass_cubic_f0',speed=speed)


def test_zero_coriolis_slope_only_time_chart_keeps_its_n2_slice():
    from models_2d import n
    result=rotation_scaling_time_ode('slope_only_f0',diffusion_exponent=2)
    assert result['status']=='verified_ode_reduction'
    assert result['parameter_specialization']=={n:2}
