#!/usr/bin/env python3
"""Lie reduction + analytical Taylor lift + learned remainder, m=3.

Run: python test.py --steps 1000 --lbfgs 100 --out results
Despite its requested filename, this is the proposed solver, not a pytest file.
X5 gives sigma=s*t^2. F=P2+(sigma-sigma0)^3*N(sigma) preserves the three
reduced initial data exactly. P2 is a provisional local semi-analytic choice,
not a claim that the paper's final approximation method has been settled.
The network sees one independent coordinate; it does not learn a 2D field.
"""
import argparse
import torch
from torch import nn
from base_PINN import Network,neural_arguments,setup,train,evaluate,checks,derivative
from base_LieReduct import write_equations


class ReducedField(nn.Module):
    def __init__(self,problem,width,depth):
        super().__init__();self.problem=problem;self.net=Network(1,width,depth)

    def profile(self,z):
        p=self.problem;z0=p.sigma0;d=z-z0
        # These three coefficients are the prescribed reduced IVP data.
        a=p.c*z0**(1/3);b=p.c/3*z0**(-2/3);c=-2*p.c/9*z0**(-5/3)
        normalized=2*(z-z0)/(p.sigma1-z0)-1
        return a+b*d+0.5*c*d*d+d**3*self.net(normalized)

    def forward(self,ts):
        return self.profile(ts[:,1:2]*ts[:,0:1]**2)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);neural_arguments(parser)
    args=parser.parse_args();problem=setup(args)
    if args.self_test:
        checks(problem)
        candidate=ReducedField(problem,args.width,args.depth)
        torch.nn.init.normal_(candidate.net.net[-1].weight)
        z=torch.tensor([[problem.sigma0]],requires_grad=True)
        f=candidate.profile(z);fp=derivative(f,z);fpp=derivative(fp,z)
        expected=[problem.c*problem.sigma0**(1/3),problem.c/3*problem.sigma0**(-2/3),-2*problem.c/9*problem.sigma0**(-5/3)]
        for val,ref in zip([f,fp,fpp],expected):
            torch.testing.assert_close(val,torch.full_like(val,ref))
        ts=torch.tensor([[1.05,1.08]],requires_grad=True)
        d=derivative(candidate(ts),ts)
        assert abs(float((ts[:,0]*d[:,0]-2*ts[:,1]*d[:,1]).detach()))<1e-10
        print('PASS: hard Taylor coefficients and learned-profile invariance.')
    else:
        write_equations(args.out,problem)
        model=ReducedField(problem,args.width,args.depth)
        model,metrics,history=train(model,problem,args,reduced=True)
        metrics['trial_function']='P2(sigma)+(sigma-sigma0)^3*N(sigma)'
        evaluate(model,problem,args,'LiePINN',metrics,history)
