#!/usr/bin/env python3
"""SVE physical basis, symbolic audit and parallel reference-data production.

Python >=3.10; numpy, scipy, sympy, threadpoolctl; torch is only needed by training.
Nondimensional model, g=1, m=1, beta=A_g/(1-porosity):
    h_t+(h*u)_x=0; u_t+u*u_x+(h+b)_x=0; b_t+beta*u_x=0.
This is the fixed Eulerian source system, NOT the incompatible printed phi PDE.
Parameters are (c,p0,kappa,beta,epsilon). x in [-1,1], t in [0,T].
Exact reference: p=p0+kappa*x, h=1/p, u=-c*p,
 b=-1/p-c*c*p*p/2+beta*c*kappa*t.
Initial h is multiplied by exp(epsilon*bump(x)); u,b are unchanged.
Exterior ghost states equal the exact reference (not periodic boundaries).
Only smooth, positive solutions in this restricted parameter family are supported.
Physical source reference: Paliathanasis et al., Mathematics 14 (2026), 433,
doi:10.3390/math14030433; the frozen Eulerian source, not its printed scalar form.

Examples:
 python sve_basis.py audit --workers 3
 # Split the symbolic identities across hosts if required:
 python sve_basis.py audit --shards 3 --shard 0 --workers 1
 python sve_basis.py generate --out data --cases 256 --nx 128 --nt 41 --workers 8
 # Distributed data shards on shared storage (run concurrently on four machines):
 python sve_basis.py generate --out data --cases 256 --shards 4 --shard 0 --workers 8
 python sve_basis.py finalize --out data

Spatial operator: Rusanov flux in (h,q=h*u,b), centered bed source; reference
residual subtraction makes this explicit reference family exactly well balanced.
This consistent reference-dependent discretization is not an entropy/shock solver.
DOP853 supplies time integration; evaluation uses a separately refined spatial grid.
The optional Newton-Krylov corrector solves the same spatial operator with implicit
trapezoidal time steps. Residual tolerance is a DISCRETE check, not a PDE certificate.
"""
import argparse
import concurrent.futures as cf
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import newton_krylov
from threadpoolctl import threadpool_limits

BOUNDS = np.array([[-.8,-.3],[1.,1.6],[-.1,.1],[.02,.08],[-.08,.08]])
G = 1.0


def atomic_json(path, value):
    path = Path(path); tmp = path.with_suffix(path.suffix + f'.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(value, indent=2, allow_nan=False)); os.replace(tmp, path)


def bump(x):
    """C-infinity compact bump supported in (-0.55,0.55), peak one."""
    z = np.asarray(x)/.55
    ans = np.zeros_like(z); mask = abs(z)<1
    ans[mask] = np.exp(1-1/(1-z[mask]**2))
    return ans


def reference(x, t, par):
    c,p0,k,beta,_ = par; p = p0+k*np.asarray(x)
    if np.any(p <= 0): raise ValueError('Reference coordinate loses invertibility')
    return np.stack([1/p, -c*p, -1/p-.5*c*c*p*p+beta*c*k*t],axis=-1)


def initial(x, par):
    v = reference(x,0.,par); v[:,0] *= np.exp(par[4]*bump(x)); return v


def conservative(v):
    return np.stack([v[...,0],v[...,0]*v[...,1],v[...,2]],axis=-1)


def primitive(U):
    if not np.isfinite(U).all() or np.min(U[...,0])<=1e-8:
        raise ValueError('Nonfinite or dry state; no clipping is allowed')
    v = np.stack([U[...,0],U[...,1]/U[...,0],U[...,2]],axis=-1)
    if np.min(v[...,1])<=0: raise ValueError('Left positive-velocity chart')
    return v


def grid(nx):
    return -1+(np.arange(nx)+.5)*(2/nx)


def raw_rhs(t, U, x, par):
    dx=x[1]-x[0]; beta=par[3]
    exterior = conservative(reference(np.array([x[0]-dx,x[-1]+dx]),t,par))
    W=np.concatenate([exterior[:1],U,exterior[1:]],axis=0)
    v=primitive(W); h,u,b=v.T
    flux=np.stack([h*u,h*u*u+.5*h*h,beta*u],axis=-1)
    # Infinity-norm row-sum bound of primitive quasilinear Jacobian
    # [[u,h,0],[1,u,1],[0,beta,0]], hence bounds full coupled wave speeds.
    speed=np.maximum.reduce([abs(u)+h,abs(u)+2,np.full_like(u,beta)])
    a=np.maximum(speed[:-1],speed[1:])
    face=.5*(flux[:-1]+flux[1:])-.5*a[:,None]*(W[1:]-W[:-1])
    rhs=-(face[1:]-face[:-1])/dx
    rhs[:,1]-=U[:,0]*(b[2:]-b[:-2])/(2*dx)
    return rhs


def rhs(t, U, x, par):
    exact=conservative(reference(x,t,par))
    ans=raw_rhs(t,U,x,par)-raw_rhs(t,exact,x,par)
    ans[:,2]+=par[3]*par[0]*par[2]
    return ans


def solve(par, nx, times, rtol=1e-8):
    x=grid(nx); y0=conservative(initial(x,par)); begin=time.perf_counter()
    speed=max(5.,abs(par[0])*(par[1]+abs(par[2]))+2.)
    with threadpool_limits(limits=1):
        sol=solve_ivp(lambda t,y:rhs(t,y.reshape(nx,3),x,par).ravel(),
                      (0.,float(times[-1])),y0.ravel(),t_eval=times,
                      method='DOP853',rtol=rtol,atol=rtol*.01,
                      max_step=.2*(2/nx)/speed)
    if not sol.success: raise RuntimeError(sol.message)
    values=primitive(sol.y.T.reshape(len(times),nx,3))
    return values, time.perf_counter()-begin


def correct(par, x, times, proposal, tol=1e-8, maxiter=40):
    """Full nonlinear discrete correction, identical for both learned models."""
    result=[initial(x,par)]; calls=0; start=time.perf_counter(); residual=0.
    for j in range(1,len(times)):
        previous=conservative(result[-1]); dt=times[j]-times[j-1]
        old_rhs=rhs(times[j-1],previous,x,par)
        def unpack(z):
            z=z.reshape(-1,3)
            return np.stack([np.exp(z[:,0]),np.exp(z[:,1]),z[:,2]],axis=-1)
        def defect(z):
            nonlocal calls
            calls+=1; v=unpack(z); U=conservative(v)
            return (U-previous-.5*dt*(old_rhs+rhs(times[j],U,x,par))).ravel()
        guess=proposal[j].copy()
        if not np.isfinite(guess).all() or np.any(guess[:,:2]<=0):
            raise ValueError('Invalid learned proposal; correction rejected')
        guess[:,:2]=np.log(guess[:,:2])
        with threadpool_limits(limits=1):
            z=newton_krylov(defect,guess.ravel(),f_tol=tol,maxiter=maxiter)
        err=float(np.max(abs(defect(z)))); residual=max(residual,err)
        if not np.isfinite(err) or err>tol: raise RuntimeError('Correction tolerance failed')
        result.append(primitive(conservative(unpack(z))))
    return np.stack(result),dict(seconds=time.perf_counter()-start,
                                rhs_calls=calls,discrete_residual=residual)


def audit_one(which):
    import sympy as s
    x,t,c,p0,k,beta=s.symbols('x t c p0 k beta',nonzero=True)
    p=p0+k*x; h=1/p; u=-c*p; b=-1/p-c*c*p*p/2+beta*c*k*t
    expressions=[s.diff(h,t)+s.diff(h*u,x),
                 s.diff(u,t)+u*s.diff(u,x)+s.diff(h+b,x),
                 s.diff(b,t)+beta*s.diff(u,x)]
    answer=s.simplify(expressions[which])
    if answer!=0: raise AssertionError(str(answer))
    return ['mass','momentum','Exner'][which]+': exact zero'


def generate_one(job):
    i,par,cfg,out=job; target=Path(out)/f'case_{i:06d}.npz'
    if target.exists():
        with np.load(target,allow_pickle=False) as d:
            if str(d['config_id'])==cfg['config_id'] and np.array_equal(d['par'],par):return i
        raise ValueError(f'Existing case has incompatible configuration: {target}')
    times=np.linspace(0,cfg['T'],cfg['nt'])
    values,seconds=solve(par,cfg['nx'],times)
    temp=target.with_suffix(f'.{os.getpid()}.tmp')
    with temp.open('wb') as f:
        np.savez_compressed(f,par=par,values=values,x=grid(cfg['nx']),t=times,
                            seconds=seconds,config_id=cfg['config_id'])
    os.replace(temp,target);return i


def finalize(out):
    out=Path(out); cfg=json.loads((out/'config.json').read_text())
    for i in range(cfg['cases']):
        p=out/f'case_{i:06d}.npz'
        if not p.exists():raise FileNotFoundError(f'Missing {p}; finish all shards first')
        with np.load(p,allow_pickle=False) as d:
            if str(d['config_id'])!=cfg['config_id']:raise ValueError('Mixed data configurations')
    ids=np.random.default_rng(cfg['seed']+1).permutation(cfg['cases'])
    a=int(.7*len(ids)); b=int(.85*len(ids))
    splits=dict(train=ids[:a].tolist(),val=ids[a:b].tolist(),test=ids[b:].tolist())
    atomic_json(out/'splits.json',splits)
    print(json.dumps({k:len(v) for k,v in splits.items()}))


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command',choices=['audit','generate','finalize'])
    p.add_argument('--out',default='data');p.add_argument('--workers',type=int,default=4)
    p.add_argument('--cases',type=int,default=256);p.add_argument('--nx',type=int,default=128)
    p.add_argument('--nt',type=int,default=41);p.add_argument('--T',type=float,default=.15)
    p.add_argument('--seed',type=int,default=2026);p.add_argument('--shards',type=int,default=1)
    p.add_argument('--shard',type=int,default=0);a=p.parse_args()
    if a.command=='finalize':finalize(a.out);return
    if a.workers<1 or a.shards<1 or not 0<=a.shard<a.shards:raise ValueError('Invalid worker/shard count')
    with cf.ProcessPoolExecutor(max_workers=a.workers,mp_context=mp.get_context('spawn')) as pool:
        audit_ids=range(a.shard,3,a.shards) if a.command=='audit' else range(3)
        print(list(pool.map(audit_one,audit_ids)))
        if a.command=='audit':return
        if a.cases<10 or a.nx<8 or a.nt<2 or a.T<=0 or not 0<=a.shard<a.shards:
            raise ValueError('Need cases>=10,nx>=8,nt>=2,T>0 and valid shard')
        out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
        cfg=dict(cases=a.cases,nx=a.nx,nt=a.nt,T=a.T,seed=a.seed,
                 model='SVE-m1-g1-well-balanced-v1',bounds=BOUNDS.tolist())
        cfg['config_id']=hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()
        path=out/'config.json'
        # Exclusive create prevents distributed shards silently changing shared config.
        try:
            with path.open('x') as f:json.dump(cfg,f,indent=2)
        except FileExistsError:
            for retry in range(50):
                try:existing=json.loads(path.read_text());break
                except json.JSONDecodeError:time.sleep(.1)
            else:raise RuntimeError('Incomplete shared config')
            if existing!=cfg:raise ValueError('Use a new output directory for a new configuration')
        pars=np.random.default_rng(a.seed).uniform(BOUNDS[:,0],BOUNDS[:,1],(a.cases,5))
        jobs=((i,pars[i],cfg,str(out)) for i in range(a.shard,a.cases,a.shards))
        for i in pool.map(generate_one,jobs,chunksize=1):print(f'case {i} saved',flush=True)
    if a.shards==1:finalize(out)

if __name__=='__main__': main()
