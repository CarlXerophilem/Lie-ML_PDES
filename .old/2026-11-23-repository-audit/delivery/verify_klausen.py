"""Re-evaluate trusted NPZ outputs from a local run of the pinned original LieSolver.

Uses explicit brick maps and independent PDE references; imports no upstream
solver or plotting code. Object arrays are read only from locally generated
trusted checkpoints. Do not pass an NPZ from an untrusted source.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad


def evaluate(model, equation, x, t):
    def sine(k,shift):
        decay=np.exp(-k*k*t) if equation=="heat" else np.cos(k*t)
        return decay*np.sin(k*x-shift)

    def transformed(xx,tt,shift,k,curvature,final_shift):
        xx=xx-final_shift
        denom=1+4*curvature*tt
        xx=xx/denom
        tt=tt/denom
        factor=np.exp(-curvature*(x-final_shift)**2/denom)/np.sqrt(denom)
        return factor*np.exp(-k*k*tt)*np.sin(k*xx-shift)

    with np.load(model,allow_pickle=True) as data:
        families=list(data["families_str"])
        expected=["exp(-t)*sin(x)"," 1","exp(-t)*sin(x)"] if equation=="heat" else [
            "sin(x)*cos(t)","exp(-(t + x)**2) + exp(-(-t + x)**2)"]
        if len(families)!=len(expected) or not all(f.endswith(e) for f,e in zip(families,expected)):
            raise ValueError(f"Unexpected original families: {families}")
        result=np.zeros_like(x)
        for i,theta,weight in zip(data["family_idx"],data["theta"],data["a"]):
            if i==0:
                value=sine(theta[1],theta[0])
            elif equation=="wave":
                shift,k=theta
                kx=k*x-shift
                value=np.exp(-(kx+k*t)**2)+np.exp(-(kx-k*t)**2)
            elif i==1:
                curvature,shift=theta
                denom=1+4*curvature*t
                value=np.exp(-curvature*(x-shift)**2/denom)/np.sqrt(denom)
            else:
                value=transformed(x,t,*theta)
            result+=weight*value
        return result, float(data["mse"]), len(data["a"])


def reference(equation,x,t):
    if equation=="wave":
        def extension(z):
            s=np.mod(z,2)
            return np.where(s<1,1,-1)*np.exp(-50*(np.minimum(s,2-s)-.5)**2)
        return (extension(x-t)+extension(x+t))/2
    modes=np.pi*np.arange(1,65)
    coeff=np.array([2*quad(lambda y:(y*y+y**3-y**5+y**7-2*y)*np.sin(k*y),
                            0,1,epsabs=1e-12)[0] for k in modes])
    return 2*x+sum(b*np.exp(-k*k*t)*np.sin(k*x) for b,k in zip(coeff,modes))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("equation",choices=("heat","wave"))
    parser.add_argument("model",type=Path)
    opts=parser.parse_args()
    x=np.linspace(.001,.999,201)
    end=.1 if opts.equation=="heat" else 1.
    t=np.linspace(end/10,end,171)
    x,t=np.meshgrid(x,t)
    candidate,mse,count=evaluate(opts.model,opts.equation,x,t)
    truth=reference(opts.equation,x,t)
    relative=np.linalg.norm(candidate-truth)/np.linalg.norm(truth)
    if not relative<.02:
        raise AssertionError(f"Unexpected reference-grid error {relative}")
    print(json.dumps({"equation":opts.equation,"bricks":count,"upstream_mse":mse,
                      "upstream_cutoff_met":mse<=9e-7,
                      "independent_relative_L2":relative,"independent_grid":list(x.shape),
                      "wave_corner_IC_jump":float(np.exp(-12.5)) if opts.equation=="wave" else None,
                      "time_min":float(t.min()),"time_max":float(t.max())},indent=2))


if __name__=="__main__":
    main()
