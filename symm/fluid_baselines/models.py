"""Original Eulerian balances, supplied reductions, and independent exact controls.

Coordinates always use multi-indices: the generic jet suffixes are positional.
Fixed nondimensional parameters are not transformed by the supplied generators.
"""
import sympy as sp

from symm.generic import DifferentialSystem, JetSpace, PDEProblem, PointGenerator, ReductionChart


def sve_scaling(m=3):
    """Grass-flux SVE (h, velocity, bed), not the printed scalar master PDE."""
    t, x = sp.symbols("t x", real=True)
    h, u, B = sp.symbols("h u B", real=True)
    g, kappa = sp.symbols("g kappa", positive=True)
    m = sp.sympify(m)
    if not m.is_number or m.is_real is not True:
        raise ValueError("supply a fixed real numeric exponent")
    space = JetSpace((t,x), (h,u,B), 1)
    dt = lambda i: space.jet_symbol(i, (1,0))
    dx = lambda i: space.jet_symbol(i, (0,1))
    equations = (dt(0)+u*dx(0)+h*dx(1),
                 h*dt(1)+u*dt(0)+u**2*dx(0)+2*h*u*dx(1)+g*h*dx(0)+g*h*dx(2),
                 dt(2)+kappa*m*u**(m-1)*dx(1))
    problem = PDEProblem(DifferentialSystem(space, equations, (h,), name=f"Eulerian-SVE-m{m}"),
                         parameters=(g,kappa), domain=(h>0,u>0,x>0))
    generator = PointGenerator((0,x), (2*h,u,2*B))
    z, rho = sp.symbols("z rho", real=True)
    H, V, C = sp.symbols("H V C", real=True)
    chart = ReductionChart(JetSpace((z,), (H,V,C), 1), (t,), rho, x,
                           (z,rho), (x**2*H,x*V,x**2*C), (x**2,x**3,x**2))
    return problem, generator, chart, sp.diag(2,3,2)


def fluid_translation(linear=False):
    """2D incompressible Navier--Stokes or constant-drift Oseen; reduce by d/dx."""
    t,x,y = sp.symbols("t x y", real=True)
    u,v,p = sp.symbols("u v p", real=True)
    nu = sp.Symbol("nu", positive=True)
    a,b = sp.symbols("a b", real=True)
    space = JetSpace((t,x,y), (u,v,p), 2)
    j = space.jet_symbol
    advx, advy = (a,b) if linear else (u,v)
    lap = lambda f: j(f,(0,2,0))+j(f,(0,0,2))
    equations = (j(0,(1,0,0))+advx*j(0,(0,1,0))+advy*j(0,(0,0,1))+j(2,(0,1,0))-nu*lap(0),
                 j(1,(1,0,0))+advx*j(1,(0,1,0))+advy*j(1,(0,0,1))+j(2,(0,0,1))-nu*lap(1),
                 j(0,(0,1,0))+j(1,(0,0,1)))
    problem = PDEProblem(DifferentialSystem(space,equations,name="Oseen-2D" if linear else "NS-2D"),
                         parameters=(nu,a,b) if linear else (nu,))
    gen = PointGenerator((0,1,0), (0,0,0))
    tau,z,rho = sp.symbols("tau z rho", real=True)
    U,V,P = sp.symbols("U V P", real=True)
    chart = ReductionChart(JetSpace((tau,z),(U,V,P),2), (t,y), rho, x,
                           (tau,rho,z), (U,V,P), (1,1,1))
    return problem,gen,chart,sp.zeros(3)


def exact_control_residuals():
    """Differentiate closed forms directly in original physical coordinates."""
    t,x,y,g,k,nu,A = sp.symbols("t x y g k nu A", positive=True)
    h = x**2*(1-4*g*k)/(9*g*t**2)
    u = 2*x/(3*t)
    B = 4*k*x**2/(9*t**2)
    sve = (sp.diff(h,t)+sp.diff(h*u,x),
           sp.diff(h*u,t)+sp.diff(h*u**2+g*h**2/2,x)+g*h*sp.diff(B,x),
           sp.diff(B,t)+k*sp.diff(u**3,x))

    def ns(u,v,p):
        lap = lambda f: sp.diff(f,x,2)+sp.diff(f,y,2)
        return (sp.diff(u,t)+u*sp.diff(u,x)+v*sp.diff(u,y)+sp.diff(p,x)-nu*lap(u),
                sp.diff(v,t)+u*sp.diff(v,x)+v*sp.diff(v,y)+sp.diff(p,y)-nu*lap(v),
                sp.diff(u,x)+sp.diff(v,y))

    decay = A*sp.exp(-2*nu*t)
    tg = ns(decay*sp.sin(x)*sp.cos(y), -decay*sp.cos(x)*sp.sin(y),
            decay**2*(sp.cos(2*x)+sp.cos(2*y))/4)
    shear = ns(A*sp.exp(-nu*t)*sp.cos(y),sp.S.Zero,sp.S.Zero)
    return {name: tuple(sp.trigsimp(sp.simplify(e)) for e in values)
            for name,values in (("sve_cubic",sve),("taylor_green",tg),("shear",shear))}
