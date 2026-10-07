"""SVE fixed-flat-bed boundary case: finite volumes + exact Lie similarity.

Run: python solve_sve.py
Equations: Paliathanasis, Leon & Leach (2026), Mathematics 14, 433, (1)-(4).
This is beta=0, B=0, not a simulation of mobile-bed sediment transport.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'
G, H0, XMIN, XMAX, TEND = 9.81, 1., -40., 60., 8.
C0 = np.sqrt(G * H0)
DRY = 1e-12

def exact(x, t):
    x = np.asarray(x)
    if t <= 0:
        return np.where(x < 0, H0, 0.), np.zeros_like(x)
    z = x / t
    fan = (z > -C0) & (z < 2*C0)
    h = np.where(z <= -C0, H0, np.where(fan, (2*C0-z)**2/(9*G), 0.))
    # Velocity is undefined in vacuum; zero is only an array convention.
    u = np.where(fan, 2*(C0+z)/3, 0.)
    return h, u

def exact_cell_depth(edges, t):
    if t <= 0:
        return H0 * np.maximum(0, np.minimum(edges[1:], 0)-edges[:-1]) / np.diff(edges)
    a, b = -C0*t, 2*C0*t
    def primitive(x):
        z = np.clip(x, a, b)
        return H0*(np.minimum(x,a)-a) + ((2*C0*t-a)**3-(2*C0*t-z)**3)/(27*G*t*t)
    return np.diff(primitive(edges))/np.diff(edges)

def velocity(q):
    return np.divide(q[1], q[0], out=np.zeros_like(q[0]), where=q[0]>DRY)

def flux(q):
    u = velocity(q)
    return np.array([q[1], q[1]*u + .5*G*q[0]**2])

def solve(n=1200, times=None):
    times = np.linspace(0, TEND, 161) if times is None else np.asarray(times)
    edges = np.linspace(XMIN, XMAX, n+1)
    x = (edges[1:]+edges[:-1])/2
    dx = edges[1]-edges[0]
    q = np.array([exact_cell_depth(edges, 0), np.zeros(n)])
    snapshots, t = [], 0.
    mass0 = float(np.sum(q[0])*dx)
    max_mass_drift = 0.
    min_depth = float(q[0].min())
    steps = 0
    for target in times:
        while t < target-1e-13:
            # Constant reservoirs: left (h0,0), right (0,0).
            ext = np.concatenate((np.array([[H0],[0.]]), q, np.zeros((2,1))), axis=1)
            speed = np.abs(velocity(ext)) + np.sqrt(G*ext[0])
            dt = min(.45*dx/speed.max(), target-t)
            a = np.maximum(speed[:-1], speed[1:])
            f = .5*(flux(ext[:,:-1])+flux(ext[:,1:]))-.5*a*(ext[:,1:]-ext[:,:-1])
            q -= dt/dx*(f[:,1:]-f[:,:-1])
            if q[0].min() < -1e-13:
                raise RuntimeError('Negative water depth')
            q[0] = np.maximum(q[0],0.)
            q[1,q[0]<=DRY] = 0.
            t += dt
            steps += 1
            min_depth = min(min_depth,float(q[0].min()))
            max_mass_drift = max(max_mass_drift,abs(float(q[0].sum()*dx)-mass0)/mass0)
        snapshots.append(q.copy())
    snapshots = np.asarray(snapshots)
    h = snapshots[:,0,:]
    u = np.divide(snapshots[:,1,:],h,out=np.zeros_like(h),where=h>DRY)
    reference = exact_cell_depth(edges,times[-1])
    return dict(x=x, edges=edges, t=times, h=h, u=u, q=snapshots[:,1,:],
                B=np.zeros_like(h),
                metrics=dict(n=n, dx=dx, steps=steps, min_depth_m=min_depth,
                relative_mass_drift=max_mass_drift,
                normalized_L1_depth=float(np.sum(abs(h[-1]-reference))*dx/mass0),
                mean_absolute_depth_error_m=float(np.mean(abs(h[-1]-reference)))))

def symbolic_check():
    x,t,g,c=sp.symbols('x t g c', positive=True)
    h=(2*c-x/t)**2/(9*g)
    u=sp.Rational(2,3)*(c+x/t)
    residuals=[sp.diff(h,t)+sp.diff(h*u,x),
               sp.diff(h*u,t)+sp.diff(h*u*u+g*h*h/2,x)]
    result = [str(sp.simplify(r)) for r in residuals]
    assert result==['0','0']
    r=sp.symbols('r',positive=True)  # r=-s in the wet region
    phi=2*c*t-3*(g*r)**sp.Rational(1,3)*t**sp.Rational(2,3)
    phi_s=-sp.diff(phi,r)
    lagrange=sp.simplify(sp.diff(phi,t,2)-g*sp.diff(phi,r,2)/phi_s**3)
    assert lagrange==0
    return dict(fan_continuity=result[0],fan_momentum=result[1],
                lagrange_equation_5=str(lagrange),
                exner='0 (beta=0, B=0)',
                scope='Smooth fan only; wet/dry interfaces checked by continuous h and hu limits.')

def main():
    OUT.mkdir(exist_ok=True)
    data=solve()
    np.savez_compressed(OUT/'solution.npz',**{k:v for k,v in data.items() if k!='metrics'})
    convergence=[]
    for n in [600,1200,2400]:
        d=solve(n,times=[0,TEND])
        convergence.append(d['metrics'])
    assert all(convergence[i+1]['normalized_L1_depth']<convergence[i]['normalized_L1_depth'] for i in range(2))
    checks=dict(parameters=dict(g=G,h0=H0,beta=0,B=0,m='irrelevant when beta=0',
                    domain=[XMIN,XMAX],T=TEND,cfl=.45,dry_tolerance=DRY),
                symbolic=symbolic_check(),production=data['metrics'],convergence=convergence,
                exact_front_m=2*C0*TEND,exact_fan_head_m=-C0*TEND,
                note='Convergence uses only initial/final output times; production hits 161 frame times.')
    (OUT/'verification.json').write_text(json.dumps(checks,indent=2))
    print(json.dumps(checks,indent=2))

if __name__=='__main__':
    main()
