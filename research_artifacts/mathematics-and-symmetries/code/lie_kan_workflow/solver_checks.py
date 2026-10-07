#!/usr/bin/env python3
"""Independent physics controls for the retained smooth spectral reference."""
import argparse
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
import torch
from baseline_core.models import Case, residual_torch
from baseline_core.numerics import solve, interpolate, ladder


def checks():
    torch.set_num_threads(1)
    # Exact spatially uniform momentum: Coriolis rotation and linear drag.
    c=Case('uniform',amplitude=0,bed_amplitude=0,kappa=0,coriolis=.2,drag=.05)
    times,fields,diag=solve(c,24,.25,rtol=1e-11,atol=1e-13)
    expected=np.zeros_like(fields);expected[...,0]=1
    expected[...,1]=(np.exp(-c.drag*times)*(c.u0*np.cos(c.coriolis*times)+c.v0*np.sin(c.coriolis*times)))[:,None,None]
    expected[...,2]=(np.exp(-c.drag*times)*(c.v0*np.cos(c.coriolis*times)-c.u0*np.sin(c.coriolis*times)))[:,None,None]
    uniform_error=float(np.max(abs(fields-expected)));assert uniform_error<1e-10
    # Lake at rest is an independent well-balanced topographic control.
    lake=Case('lake',control='lake',u0=0,v0=0,kappa=0)
    _,fields,lake_diag=solve(lake,24,.25,rtol=1e-11,atol=1e-13)
    lake_error=float(np.max(abs(fields-fields[0])));assert lake_error<1e-10
    roundtrip=float(np.max(abs(interpolate(interpolate(fields,12),24)-fields)))
    assert roundtrip<1e-12
    # Check the Grass divergence against finite differences of the vector flux,
    # independent of the expanded symbolic/autograd residual formula.
    rng=np.random.default_rng(47);x,y=rng.random((2,12))*2*np.pi
    c=Case('flux',m=3.1)
    def velocity(x,y):return .25+.02*np.sin(x)*np.cos(y),.15+.03*np.cos(x)*np.sin(y)
    def flux(x,y):
        u,v=velocity(x,y);factor=c.kappa*(u*u+v*v)**((c.m-1)/2)
        return factor*u,factor*v
    eps=1e-5
    finite=(flux(x+eps,y)[0]-flux(x-eps,y)[0])/(2*eps)+(flux(x,y+eps)[1]-flux(x,y-eps)[1])/(2*eps)
    u,v=velocity(x,y);jet=np.zeros((len(x),19));jet[:,1]=x;jet[:,2]=y;jet[:,3]=1;jet[:,4]=u;jet[:,5]=v
    jet[:,11]=.02*np.cos(x)*np.cos(y);jet[:,12]=-.02*np.sin(x)*np.sin(y)
    jet[:,14]=-.03*np.sin(x)*np.sin(y);jet[:,15]=.03*np.cos(x)*np.cos(y)
    expanded=residual_torch(torch.tensor(jet,dtype=torch.float64),c)[:,3].numpy()
    flux_error=float(np.max(abs(expanded-finite)));assert flux_error<1e-10
    _,_,ref=ladder(replace(c,amplitude=.03),[12,18,24],.25,16)
    assert ref['estimated_reference_uncertainty']<1e-8
    assert ref['tight']['mass_drift']<1e-12 and ref['tight']['bed_mean_drift']<1e-12
    assert ref['tight']['min_depth']>0 and ref['tight']['sampled_max_eigenvalue_imag']<1e-10
    return {'status':'passed','uniform_rotation_drag_max_error':uniform_error,
            'lake_at_rest_max_change':lake_error,'spectral_interpolation_roundtrip_error':roundtrip,
            'expanded_Grass_vs_flux_finite_difference_max_error':flux_error,
            'refinement':ref,'scope':'smooth periodic short-time controls; sampled hyperbolicity and refinement are not global certificates'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',default='results/solver_checks.json');args=p.parse_args()
    result=checks();out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='refinement'},indent=2))


if __name__=='__main__':main()
