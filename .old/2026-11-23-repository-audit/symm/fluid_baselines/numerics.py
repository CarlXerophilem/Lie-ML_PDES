"""Small deterministic CPU reference solvers, with explicitly limited scope.

SVE: first-order Rusanov flux, centered bed source, SSPRK3 on a periodic grid.
This is a smooth-solution baseline, not a well-balanced or shock-certified code.
NS/Oseen: periodic vorticity, strict 2/3 Fourier truncation and explicit RK4.
No machine learning is used or timed by these algorithms.
"""
from time import perf_counter

import numpy as np
from scipy.integrate import solve_ivp


def _positive_inputs(n, end, snapshots, *, start=0):
    if n < 8 or snapshots < 2 or end <= start:
        raise ValueError("require n>=8, snapshots>=2 and end>start")


def sve_periodic(n=128, m=3, kappa=.1, g=1., end=.4, snapshots=41):
    _positive_inputs(n,end,snapshots)
    if g <= 0 or kappa < 0 or m <= 0:
        raise ValueError("require g>0, kappa>=0, m>0")
    started = perf_counter()
    dx = 2*np.pi/n
    x = (np.arange(n)+.5)*dx
    # Cell averages of h, u and B; the q=h*u initialization is second-order accurate.
    h = 1+.03*np.cos(x)*np.sinc(dx/(2*np.pi))
    u = .4+.02*np.sin(x)*np.sinc(dx/(2*np.pi))
    bed = .015*np.cos(2*x)*np.sinc(dx/np.pi)
    state = np.array([h,h*u,bed])
    times = np.linspace(0,end,snapshots)
    states, steps, t = [state.copy()], 0, 0.

    def primitives(U):
        if not np.all(np.isfinite(U)) or U[0].min() <= 0:
            raise RuntimeError("SVE lost finite positive depth; run rejected")
        velocity = U[1]/U[0]
        if velocity.min() <= 0:
            raise RuntimeError("SVE left the declared positive-velocity power branch")
        return U[0],velocity,U[2]

    def speed_bound(U):
        depth,vel,_ = primitives(U)
        # Infinity norm bounds spectral radius of the primitive quasilinear matrix.
        return float(max(np.max(abs(vel)+depth),np.max(abs(vel)+2*g),
                         np.max(kappa*m*vel**(m-1))))

    def rhs(U):
        depth,vel,bed = primitives(U)
        flux = np.array([U[1],U[1]*vel+.5*g*depth**2,kappa*vel**m])
        face = .5*(flux+np.roll(flux,-1,axis=1))- .5*speed_bound(U)*(np.roll(U,-1,axis=1)-U)
        rate = -(face-np.roll(face,1,axis=1))/dx
        rate[1] -= g*depth*(np.roll(bed,-1)-np.roll(bed,1))/(2*dx)
        return rate

    for target in times[1:]:
        while t < target-1e-14:
            dt = min(.25*dx/speed_bound(state),target-t)
            a = state+dt*rhs(state)
            b = .75*state+.25*(a+dt*rhs(a))
            state = state/3+2*(b+dt*rhs(b))/3
            primitives(state)
            t += dt
            steps += 1
        states.append(state.copy())
    states = np.array(states)
    h, u, bed = states[:,0], states[:,1]/states[:,0], states[:,2]
    mass, bedmean = h.mean(axis=1),bed.mean(axis=1)
    matrices = np.zeros((len(times),n,3,3))
    matrices[:,:,0,0],matrices[:,:,0,1] = u,h
    matrices[:,:,1,0],matrices[:,:,1,1],matrices[:,:,1,2] = g,u,g
    matrices[:,:,2,1] = kappa*m*u**(m-1)
    eigenvalues = np.linalg.eigvals(matrices)
    metrics = {"mass_relative_drift":float(np.max(abs(mass-mass[0]))/mass[0]),
               "bed_mean_absolute_drift":float(np.max(abs(bedmean-bedmean[0]))),
               "minimum_depth":float(h.min()),"minimum_velocity":float(u.min()),
               "maximum_characteristic_imaginary_part":float(np.max(abs(eigenvalues.imag))),
               "steps":steps,"wall_seconds":perf_counter()-started}
    return {"dimension":1,"times":times,"x":x,"fields":{"h":h,"u":u,"bed":bed,"surface":h+bed},
            "diagnostics":{"mean depth":mass,"mean bed":bedmean,"minimum depth":h.min(axis=1)},
            "metrics":metrics}


def sve_reduced(kappa=.1, g=1., end=1.5, snapshots=41, n=128):
    _positive_inputs(n,end,snapshots,start=1)
    if g <= 0 or not 0 <= kappa < 1/(4*g):
        raise ValueError("exact control requires g>0 and 0<=4*g*kappa<1")
    started = perf_counter()
    times, x = np.linspace(1,end,snapshots),np.linspace(.5,2,n)
    exact = lambda t: np.array([(1-4*g*kappa)/(9*g*t*t),2/(3*t),4*kappa/(9*t*t)])
    def rhs(t,y):
        H,V,C = y
        return [-3*H*V,-V*V-2*g*(H+C),-3*kappa*V**3]
    sol = solve_ivp(rhs,(1,end),exact(1),t_eval=times,method="DOP853",rtol=1e-11,atol=1e-13)
    if not sol.success:
        raise RuntimeError(sol.message)
    H,V,C = sol.y
    h,u,bed = H[:,None]*x**2,V[:,None]*x,C[:,None]*x**2
    return {"dimension":1,"times":times,"x":x,"fields":{"h":h,"u":u,"bed":bed,"surface":h+bed},
            "diagnostics":{"H(t)":H,"V(t)":V,"C(t)":C},
            "metrics":{"exact_profile_max_error":float(np.max(abs(sol.y-exact(times)))),
                       "minimum_depth":float(h.min()),"nfev":sol.nfev,"wall_seconds":perf_counter()-started}}


def vorticity_evolution(n=64, nu=.05, kind="interacting", mean=(0.,0.), linear=False,
                        end=1., snapshots=41, max_dt=.01):
    _positive_inputs(n,end,snapshots)
    if nu <= 0 or max_dt <= 0 or n%2:
        raise ValueError("require positive viscosity, positive dt and an even grid")
    if kind not in ("taylor_green","shear","interacting"):
        raise ValueError("unknown initial field")
    started = perf_counter()
    x = np.arange(n)*2*np.pi/n
    X,Y = np.meshgrid(x,x,indexing="xy")
    k = np.fft.fftfreq(n,1/n)
    KX,KY = np.meshgrid(k,k,indexing="xy")
    k2 = KX**2+KY**2
    invk2 = np.zeros_like(k2)
    invk2[k2>0] = 1/k2[k2>0]
    mask = (abs(KX)<n/3)&(abs(KY)<n/3)
    if kind == "shear":
        w0 = np.sin(Y)
    else:
        w0 = 2*np.sin(X)*np.sin(Y)
        if kind == "interacting":
            w0 += np.cos(2*X)*np.cos(Y)+.75*np.sin(X)*np.cos(2*Y)
    initial = np.fft.fft2(w0)*mask
    state = initial.copy()
    times = np.linspace(0,end,snapshots)
    def real(a):
        return np.fft.ifft2(a).real
    def velocity(w):
        psi = w*invk2
        return mean[0]+real(1j*KY*psi),mean[1]-real(1j*KX*psi)
    def rhs(w):
        if linear:
            return (-nu*k2-1j*(mean[0]*KX+mean[1]*KY))*w
        u,v = velocity(w)
        advection = u*real(1j*KX*w)+v*real(1j*KY*w)
        return -np.fft.fft2(advection)*mask-nu*k2*w
    history, steps, t = [state.copy()],0,0.
    for target in times[1:]:
        while t < target-1e-14:
            u,v = velocity(state)
            dt = min(max_dt,.2*(2*np.pi/n)/max(np.max(abs(u)+abs(v)),1e-12),
                     .5/(nu*np.max(k2[mask])),target-t)
            a = rhs(state)
            b = rhs(state+dt*a/2)
            c = rhs(state+dt*b/2)
            d = rhs(state+dt*c)
            state = (state+dt*(a+2*b+2*c+d)/6)*mask
            if not np.all(np.isfinite(state)):
                raise RuntimeError("Fourier evolution became nonfinite")
            t += dt
            steps += 1
        history.append(state.copy())
    history = np.array(history)
    uv = [velocity(w) for w in history]
    u,v = np.array([a[0] for a in uv]),np.array([a[1] for a in uv])
    w = np.array([real(a) for a in history])
    energy = .5*(u*u+v*v).mean(axis=(1,2))
    enstrophy = .5*(w*w).mean(axis=(1,2))
    divergence = max(np.max(abs(real(1j*KX*np.fft.fft2(a)+1j*KY*np.fft.fft2(b)))) for a,b in uv)
    metrics = {"divergence_max":float(divergence),"energy_max_increase":float(np.diff(energy).max()),
               "enstrophy_max_increase":float(np.diff(enstrophy).max()),
               "vorticity_mean_max":float(abs(w.mean(axis=(1,2))).max()),
               "steps":steps,"wall_seconds":perf_counter()-started}
    if linear:
        exact = np.array([real(initial*np.exp((-nu*k2-1j*(mean[0]*KX+mean[1]*KY))*t)) for t in times])
        metrics["exact_vorticity_max_error"] = float(np.max(abs(w-exact)))
    elif kind in ("taylor_green","shear"):
        xe = X[None,:,:]-mean[0]*times[:,None,None]
        ye = Y[None,:,:]-mean[1]*times[:,None,None]
        decay = np.exp(-(nu if kind=="shear" else 2*nu)*times)[:,None,None]
        ue = mean[0]+decay*(np.cos(ye) if kind=="shear" else np.sin(xe)*np.cos(ye))
        ve = np.full_like(v,mean[1]) if kind=="shear" else mean[1]-decay*np.cos(xe)*np.sin(ye)
        metrics["exact_velocity_max_error"] = float(max(np.max(abs(u-ue)),np.max(abs(v-ve))))
    return {"dimension":2,"times":times,"x":x,"y":x,
            "fields":{"u":u,"v":v,"vorticity":w,"speed":np.sqrt(u*u+v*v)},
            "diagnostics":{"kinetic energy":energy,"enstrophy":enstrophy},"metrics":metrics}
