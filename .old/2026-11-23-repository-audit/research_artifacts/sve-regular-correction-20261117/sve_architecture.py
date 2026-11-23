#!/usr/bin/env python3
"""Lie-reference residual neural architecture; uses the baseline's complete engine.

 python sve_architecture.py train --data data --run architecture --epochs 300
 torchrun --standalone --nproc_per_node=2 sve_architecture.py train --data data --run architecture
 python sve_architecture.py evaluate --data data --run architecture --correct --workers 4
 python sve_architecture.py predict --data data --run architecture --params=-.5,1.2,.05,.04,.03 --correct

Architecture (all variables are nondimensional):
 p=p0+kappa*x; exact reference hR=1/p, uR=-c*p,
 bR=-1/p-c^2*p^2/2+beta*c*kappa*t.
 z=(x,t,c,p0,kappa,beta,epsilon); N_theta(z)=(n_h,n_u,n_b).
 h=hR*exp(epsilon*bump(x)+t*epsilon*n_h),
 u=uR*exp(t*epsilon*n_u), b=bR+t*epsilon*n_b.
Thus initial data and the entire epsilon=0 exact reference are preserved by
construction, with positive h,u. This encodes a local perturbation-family hypothesis;
it is NOT a universal PDE solver or a Laurent representation across singularities.
The supplied reference chart has p>=0.9; singular charts are explicitly excluded.

The reference parameters are prescribed by the input target family, not learned
redundant variables. No claim of a geometric orthogonal projection is made: the
network learns a departure from the reference; non-invariance needs separate checks.
The final optional correction acts on full (h,u,b) fields via the original spatial
PDE operator, not on filtered/network residuals. Repeated Newton-Krylov iterations
solve nonlinear discrete equations, not just first-order perturbation predictions.

Shared engine includes whole-case splits, PDE automatic differentiation, AdamW,
validation/early stopping, resumable checkpoints, DDP (NCCL/Gloo), parallel refined
reference solves, an identical classical corrector and explicit failed-case reports.
Data-generation and training costs must both be included in any speedup claim.
Use WSL/Linux for CPU distributed training; do not launch several processes on one GPU.
"""
import torch
from sve_baseline import DirectField, initial_torch, reference_torch, main


class SkeletonField(DirectField):
    kind='architecture'

    def field(self,z):
        raw=self.net((z-self.center)/self.span)
        ref=reference_torch(z);init=initial_torch(z)
        z0=torch.cat((z[:,:1],torch.zeros_like(z[:,1:2]),z[:,2:]),1)
        ref0=reference_torch(z0)
        change=z[:,1:2]*z[:,6:7]*raw
        positive=ref[:,:2]*(init[:,:2]/ref0[:,:2])*torch.exp(change[:,:2])
        bed=ref[:,2:]+(init[:,2:]-ref0[:,2:])+change[:,2:]
        return torch.cat((positive,bed),1)


if __name__=='__main__':main(SkeletonField)
