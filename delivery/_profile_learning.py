"""Small CPU benchmarks on verified invariant charts.

Every solver gets only the ODE and its traces. Exact profiles are evaluated
after fitting. The liquid block is a feature-space residual cell, with no
claim of a recurrent physical-time model.
"""
from dataclasses import dataclass, asdict
import argparse
from math import comb, factorial
import json
from time import perf_counter

import numpy as np
from numpy.polynomial import Chebyshev, Polynomial
from scipy.linalg import lstsq
from scipy.optimize import least_squares


@dataclass(frozen=True)
class Settings:
    seed: int = 27
    width: int = 6
    chebyshev_degree: int = 15
    taylor_degree: int = 22
    train_coordinates: int = 24
    test_coordinates: int = 401
    max_nfev: int = 150


@dataclass(frozen=True)
class Case:
    name: str
    left: float
    trace_interval: tuple
    trace_order: int
    coefficients: tuple
    right_hand_side: object
    trace: object
    taylor: object
    exact: object
    fields: object
    original_residual: object


def product(left, right):
    return tuple(sum(comb(k,i)*left[i]*right[k-i] for i in range(k+1))
                 for k in range(len(left)))


def tanh_jet(values):
    y=np.tanh(values[0])
    a=1-y*y
    d, dd, ddd=values[1:]
    return (y,a*d,a*(dd-2*y*d*d),
            a*(ddd-6*y*d*dd+(6*y*y-2)*d*d*d))


def monomial_jet(x,power):
    return tuple(np.zeros_like(x) if k>power else
                 factorial(power)/factorial(power-k)*x**(power-k)
                 for k in range(4))


def trace_jet(case,x,p):
    values=case.trace(p)
    return tuple(sum(values[i]*monomial_jet(x,i)[k]/factorial(i)
                     for i in range(case.trace_order)) for k in range(4))


def operator(case, jets, z):
    return sum(c(z)*d if callable(c) else c*d
               for c,d in zip(case.coefficients,jets))


def liquid_model(case,z,p,params,width):
    # The affine readout exactly matches all four tasks' affine dependence on
    # trace data. This tests interpolation in the trace, not nonlinear transfer.
    x=np.ravel(z-case.left)
    p=np.broadcast_to(p,z.shape).ravel()
    lo,hi=case.trace_interval
    pscaled=(2*p-lo-hi)/(hi-lo)
    slopes,biases,gates = params[:3*width].reshape(3,width)
    switch=3*width+width*width
    influence=params[3*width:switch].reshape(width,width)
    readout=params[switch:].reshape(2,width)
    u=(2*x[:,None]-1)*slopes+biases
    v=tanh_jet((u,np.broadcast_to(2*slopes,u.shape),np.zeros_like(u),np.zeros_like(u)))
    mixed=tanh_jet(tuple(vv@influence.T for vv in v))
    layers=tuple(vv+gg*np.tanh(gates) for vv,gg in zip(v,mixed))
    combined=tuple((layer@readout[0]+pscaled*(layer@readout[1])).reshape(z.shape)
                   for layer in layers)
    correction=product(monomial_jet(z-case.left,case.trace_order),combined)
    return tuple(a+b for a,b in zip(trace_jet(case,z-case.left,p.reshape(z.shape)),correction))


def fit_liquid(case,settings):
    q=(np.arange(settings.train_coordinates)+.5)/settings.train_coordinates
    lo,hi=case.trace_interval
    z,p=np.meshgrid(case.left+q,np.linspace(lo,hi,5))
    z,p=z.ravel(),p.ravel()
    rng=np.random.default_rng(settings.seed)
    w=settings.width
    initial=rng.normal(0,.32,size=5*w+w*w)
    initial[:w]=rng.uniform(.55,1.5,size=w)
    def residual(weights):
        jets=liquid_model(case,z,p,weights,w)
        return operator(case,jets,z)-case.right_hand_side(z,p)
    fit=least_squares(residual,initial,max_nfev=settings.max_nfev,
                      gtol=1e-10,ftol=1e-10,xtol=1e-10)
    def predict(z,p):
        return liquid_model(case,np.asarray(z),p,fit.x,w)
    return predict, {"nfev":fit.nfev,"parameters":len(initial),
                     "status":"budget_exhausted" if fit.status == 0 else "optimizer_terminated",
                     "interpretation":"fixed-budget approximation; no convergence claim",
                     "optimizer_status":fit.status,
                     "sample_train_rms":float(np.sqrt(np.mean(fit.fun**2)))}


def polynomial_jet(polynomial,x):
    return tuple(polynomial.deriv(k)(x) for k in range(4))


def chebyshev_profile(case,p,settings):
    n=settings.chebyshev_degree
    nodes=case.left+(1-np.cos(np.pi*(np.arange(n+2)+.5)/(n+2)))/2
    delta=nodes-case.left
    def lift(poly,x):
        return product(monomial_jet(x,case.trace_order),polynomial_jet(poly,x))
    basis=[Chebyshev.basis(k,domain=[0,1]) for k in range(n+1)]
    matrix=np.column_stack([operator(case,lift(b,delta),nodes) for b in basis])
    baseline=operator(case,trace_jet(case,delta,p),nodes)
    target=np.broadcast_to(case.right_hand_side(nodes,p),nodes.shape)-baseline
    coeff,_,rank,_=lstsq(matrix,target,lapack_driver="gelsd")
    if rank != n+1:
        raise ArithmeticError(f"Rank {rank} in degree {n} collocation")
    poly=Chebyshev(coeff,domain=[0,1])
    def predict(z):
        x=np.asarray(z)-case.left
        return tuple(a+b for a,b in zip(trace_jet(case,x,p),lift(poly,x)))
    return predict


def taylor_profile(case,p,settings):
    """Use two linked series charts to keep |z-z0| <= 1/2 per chart."""
    n=settings.taylor_degree
    polys=[]
    trace=case.trace(p)
    for center in (case.left,case.left+.5):
        coeff=case.taylor(n,p,center,trace)
        poly=Polynomial(coeff)
        trace=tuple(poly.deriv(k)(.5) for k in range(case.trace_order))
        polys.append(poly)
    def predict(z):
        x=np.asarray(z)-case.left
        return tuple(np.where(x<=.5,left,right) for left,right in zip(
            polynomial_jet(polys[0],x),polynomial_jet(polys[1],x-.5)))
    return predict


def compare(case,settings=Settings()):
    start=perf_counter()
    liquid,fit=fit_liquid(case,settings)
    fit["elapsed_seconds"]=perf_counter()-start
    lo,hi=case.trace_interval
    points=settings.test_coordinates
    z=case.left+(np.arange(points)+.5)/points
    traces=lo+(hi-lo)*(np.arange(4)+.5)/4
    methods=("LNN-PINN","Chebyshev","Taylor")
    logs={k:{"errors":[],"residuals":[],"seconds":0.,"trace_error":0.} for k in methods}
    for p in traces:
        reference=case.fields(z,case.exact(z,p))
        for method in methods:
            start=perf_counter()
            if method=="LNN-PINN":
                predict=lambda z:liquid(z,p)
            elif method=="Chebyshev":
                predict=chebyshev_profile(case,p,settings)
            else:
                predict=taylor_profile(case,p,settings)
            estimated=predict(z)
            approximated=case.fields(z,estimated)
            init=predict(np.array([case.left]))
            log=logs[method]
            log["seconds"]+=perf_counter()-start
            error=approximated-reference
            residual=case.original_residual(z,estimated,p)
            if not np.all(np.isfinite(error)) or not np.all(np.isfinite(residual)):
                raise ArithmeticError(f"{case.name} {method} left its valid chart")
            log["errors"].extend(error.ravel())
            log["residuals"].extend(np.atleast_1d(np.abs(residual)).ravel())
            log["trace_error"]=max(log["trace_error"],max(
                abs(float(v[0])-desired) for v,desired in zip(init,case.trace(p))))
    metrics={k:{"field_rms":float(np.sqrt(np.mean(np.square(v["errors"])))),
                "field_maximum":float(np.max(np.abs(v["errors"]))),
                "original_residual_maximum":float(max(v["residuals"])),
                "trace_error_maximum":v["trace_error"],
                "setup_and_prediction_seconds_all_traces":v["seconds"]}
             for k,v in logs.items()}
    # Keep historical metric keys for regression. The displayed method name is
    # adapted gated cell, not the original LNN-PINN architecture.
    return {"case":case.name,"settings":asdict(settings),"fit":fit,
            "method_display_name":"adapted gated cell",
            "trace_dependence":"affine interpolation; not nonlinear parameter learning",
            "residual_orders":{"training":2,"diagnostic":3} if "P at m=1" in case.name
                              else {"training":1,"diagnostic":1},
            "test_traces":traces.tolist(),"metrics":metrics}


def cli(cases):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed",type=int,default=Settings.seed)
    parser.add_argument("--max-nfev",type=int,default=Settings.max_nfev)
    opts=parser.parse_args()
    settings=Settings(seed=opts.seed,max_nfev=opts.max_nfev)
    print(json.dumps([compare(case,settings) for case in cases],indent=2))
