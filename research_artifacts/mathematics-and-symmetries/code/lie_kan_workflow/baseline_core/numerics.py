"""Conservative Fourier collocation + DOP853 reference for smooth periodic flow.

Two-thirds filtering is applied to nonlinear flux/source outputs. No shock,
dry-bed or global smoothness guarantee is made. All four balances are coupled.
"""
import time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import resample
from .models import initial_np


def grid(n):
    x = 2*np.pi*np.arange(n)/n
    return np.meshgrid(x, x, indexing="xy")


def primitive(q):
    return np.stack([q[0], q[1]/q[0], q[2]/q[0], q[3]], axis=-1)


def hyperbolicity_probe(fields, case):
    values = fields.reshape(-1, 4)[::max(1, fields.size//128)]
    max_imag = 0.
    for h,u,v,b in values:
        r2 = u*u+v*v
        base = case.kappa*r2**((case.m-1)/2) if case.kappa else 0
        cross = case.kappa*(case.m-1)*r2**((case.m-3)/2) if case.kappa else 0
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            nx,ny = np.cos(angle),np.sin(angle); vel = u*nx+v*ny
            du = base*nx+cross*u*vel; dv = base*ny+cross*v*vel
            jac = [[vel,h*nx,h*ny,0], [case.g*nx,vel,0,case.g*nx],
                   [case.g*ny,0,vel,case.g*ny], [0,du,dv,0]]
            max_imag = max(max_imag, float(np.max(np.abs(np.linalg.eigvals(jac).imag))))
    return max_imag


def solve(case, n=24, horizon=.25, rtol=1e-9, atol=1e-11):
    tic = time.perf_counter()
    x,y = grid(n)
    u0 = initial_np(x,y,case)
    q0 = np.stack([u0[...,0],u0[...,0]*u0[...,1],u0[...,0]*u0[...,2],u0[...,3]])
    wave = np.fft.fftfreq(n, 1/n)
    kx,ky = np.meshgrid(wave,wave,indexing="xy")
    mask = (np.abs(kx)<n/3)&(np.abs(ky)<n/3)
    def derivative(field, axis):
        k = kx if axis == 1 else ky
        return np.fft.ifft2(1j*k*mask*np.fft.fft2(field)).real
    def filtered(field):
        return np.fft.ifft2(mask*np.fft.fft2(field)).real
    def rhs(t, flat):
        h,hu,hv,b = flat.reshape(4,n,n)
        if np.min(h) <= 0 or not np.isfinite(flat).all():
            raise FloatingPointError("Reference left positive finite-depth branch")
        u,v = hu/h,hv/h
        if case.kappa and np.min(u*u+v*v) < 1e-12:
            raise FloatingPointError("Active noninteger flux left nonzero-speed branch")
        bx,by = derivative(b,1),derivative(b,0)
        dh = -derivative(hu,1)-derivative(hv,0)
        dhu = -derivative(hu*u+.5*case.g*h*h,1)-derivative(hu*v,0)
        dhv = -derivative(hv*u,1)-derivative(hv*v+.5*case.g*h*h,0)
        dhu += filtered(-case.g*h*bx+case.coriolis*hv-case.drag*hu)
        dhv += filtered(-case.g*h*by-case.coriolis*hu-case.drag*hv)
        if case.kappa:
            speed = (u*u+v*v)**((case.m-1)/2)
            db = -case.kappa*(derivative(speed*u,1)+derivative(speed*v,0))
        else:
            db = np.zeros_like(b)
        return np.stack([dh,dhu,dhv,db]).ravel()
    times = np.array([0., horizon/2, horizon])
    result = solve_ivp(rhs,(0,horizon),q0.ravel(),method="DOP853",t_eval=times,
                       rtol=rtol,atol=atol)
    if not result.success:
        raise RuntimeError(result.message)
    q = result.y.T.reshape(3,4,n,n)
    fields = np.array([primitive(a) for a in q])
    elapsed = time.perf_counter()-tic
    spectrum = np.abs(np.fft.fft2(fields[-1,...,0]))**2
    high = (np.abs(kx)>=n/3)|(np.abs(ky)>=n/3)
    diag = {"n":n,"solve_seconds":elapsed,"nfev":result.nfev,"rtol":rtol,"atol":atol,
            "mass_drift":float(np.max(np.abs(q[:,0].mean((1,2))-q[0,0].mean()))),
            "bed_mean_drift":float(np.max(np.abs(q[:,3].mean((1,2))-q[0,3].mean()))),
            "min_depth":float(fields[...,0].min()),
            "min_speed":float(np.sqrt(fields[...,1]**2+fields[...,2]**2).min()),
            "high_mode_fraction":float(spectrum[high].sum()/max(spectrum.sum(),1e-30)),
            "sampled_max_eigenvalue_imag":hyperbolicity_probe(fields[-1],case),
            "scope":"smooth periodic numerical reference; sampled guards are not a theorem"}
    return times,fields,diag


def interpolate(fields,n):
    return resample(resample(fields,n,axis=1),n,axis=2).real


def ladder(case,grids,horizon,eval_n):
    records=[]; solutions=[]
    for n in grids:
        times,fields,diag=solve(case,n,horizon)
        solutions.append(interpolate(fields,eval_n));records.append(diag)
    finest=solutions[-1]
    for i,rec in enumerate(records):
        rec["max_difference_from_finest"]=float(np.max(np.abs(solutions[i]-finest)))
    # Independent temporal tolerance refinement at the finest spatial resolution.
    _,tight,check=solve(case,grids[-1],horizon,rtol=1e-11,atol=1e-13)
    tight=interpolate(tight,eval_n)
    discrepancy=float(np.max(np.abs(finest-tight)))
    return times,tight,{"ladder":records,"tight":check,"temporal_difference":discrepancy,
        "estimated_reference_uncertainty":max(discrepancy,records[-2]["max_difference_from_finest"])
            if len(records)>1 else None,
        "total_reference_seconds":sum(r["solve_seconds"] for r in records)+check["solve_seconds"]}
