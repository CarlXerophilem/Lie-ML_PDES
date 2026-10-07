"""Independent physics, symbolic, autograd, and boundary sanity checks."""
from dataclasses import replace
import numpy as np
import sympy as sp
import torch
from models import suite, initial_torch, residual_torch, subgroup_coeff_torch,finite_action,multiplier
from symbolic import audit, build, coefficients
from numerics import solve, initial_np, grid
from pinns import PINN, jet, identity_check, lie_dots


def run():
    cases=suite();records={}
    for name in ('flat','rotation_drag','sve_m3','sve_m3.1','sve_m4'):
        case=cases[name];record=audit(case)
        expected={'flat':['D','V','J'],'rotation_drag':['V','J'],
                  'sve_m3':['D','V','J'],'sve_m3.1':['D','J'],'sve_m4':['D','J']}[name]
        assert record['useful_generators']==expected,(name,record['useful_generators'])
        assert not next(r for r in record['generators'] if r['generator']=='Gx')['verified']
        identity=identity_check(case,expected)
        assert identity['loss_difference']<1e-12 and identity['max_parameter_gradient_difference']<1e-11
        if name=='flat':assert record['Galilean_Gx_valid_on_flat_bed_restriction'] is True
        testjet=torch.rand(9,19,dtype=torch.float64)+.3
        original=residual_torch(testjet,case)
        finite_errors={}
        for generator in expected:
            transformed=residual_torch(finite_action(testjet,generator,.17),case)
            covariance=original@torch.matrix_exp(testjet.new_tensor(multiplier(generator))*.17).T
            finite_errors[generator]=float((transformed-covariance).abs().max())
            assert finite_errors[generator]<1e-12
        records[name]={**identity,'finite_subgroup_covariance_max':finite_errors}
    case=cases['sve_m3.1']
    torch.manual_seed(1)
    values=torch.rand(5,19,dtype=torch.float64)+.2;values.requires_grad_()
    z,f,d,e=build(case);symbols=(*z,*f,*(a for row in d for a in row))
    eq_numpy=sp.lambdify(symbols,list(e),'numpy')(*values.detach().numpy().T)
    difference=np.max(np.abs(np.array(eq_numpy).T-residual_torch(values,case).detach().numpy()))
    assert difference<1e-12
    for name in ('D','V','J','Tx'):
        fun=sp.lambdify(symbols,list(coefficients(z,f,d,name)),'numpy')
        entries=fun(*values.detach().numpy().T)
        numeric=np.array([np.broadcast_to(item,(5,)) for item in entries]).T
        assert np.max(np.abs(numeric-subgroup_coeff_torch(values,name).detach().numpy()))<1e-12
    assert lie_dots(residual_torch(values,case),values,['Tx','Ty','Tt']).abs().max()<1e-14
    # The intentionally invalid near-cubic V generator must have a nonzero defect.
    bad=next(r for r in audit(case)['generators'] if r['generator']=='V')
    assert not bad['verified'] and any(a!='0' for a in bad['defect'])
    boundaries={}
    for arch in ('mlp','modified','deeponet'):
        model=PINN(arch,.25)
        p=torch.rand(12,3,dtype=torch.float64)*torch.tensor([.25,6.28,6.28])
        p[:,0]=0
        ic_error=float((model(p,case)-initial_torch(p,case)).abs().max().detach())
        p[:,0]=.13;px=p.clone();px[:,1]+=2*np.pi;py=p.clone();py[:,2]+=2*np.pi
        bc_error=max(float((model(px,case)-model(p,case)).abs().max().detach()),
                     float((model(py,case)-model(p,case)).abs().max().detach()))
        # Translate both input and initial data: this family uses exact canonicalization.
        translated=replace(case,phase_x=.37,phase_y=.51)
        shifted=p+p.new_tensor([0,.37,.51]);translation_error=float((model(shifted,translated)-model(p,case)).abs().max().detach())
        assert ic_error==0 and bc_error<1e-12 and translation_error<1e-12
        boundaries[arch]={'ic_max':ic_error,'periodic_max':bc_error,'translation_family_max':translation_error}
    lake=replace(cases['topography'],name='lake',u0=0,v0=0,control='lake')
    times,fields,diag=solve(lake,18,.25)
    lake_error=float(np.max(np.abs(fields-fields[0])))
    assert lake_error<1e-10
    constant=replace(cases['sve_m3'],name='constant',amplitude=0,bed_amplitude=0)
    _,fields,_=solve(constant,18,.25)
    constant_error=float(np.max(np.abs(fields-fields[0])))
    assert constant_error<1e-12
    # Exact spatially uniform Coriolis/drag solution independently checks source signs.
    rotation=replace(cases['rotation_drag'],name='uniform_rotation',amplitude=0,bed_amplitude=0)
    times,fields,_=solve(rotation,18,.25)
    u=np.exp(-rotation.drag*times)*(rotation.u0*np.cos(rotation.coriolis*times)+rotation.v0*np.sin(rotation.coriolis*times))
    v=np.exp(-rotation.drag*times)*(-rotation.u0*np.sin(rotation.coriolis*times)+rotation.v0*np.cos(rotation.coriolis*times))
    source_error=max(float(np.max(np.abs(fields[...,1]-u[:,None,None]))),
                     float(np.max(np.abs(fields[...,2]-v[:,None,None]))))
    assert source_error<1e-10
    return {'status':'passed','paired_loss_gradient_identities':records,'torch_sympy_equation_max':float(difference),
            'boundary_checks':boundaries,'lake_at_rest_max':lake_error,'constant_flow_max':constant_error,
            'uniform_rotation_drag_max':source_error,'invalid_near_cubic_scaling_rejected':True,
            'translation_lie_loss_is_zero':True}
