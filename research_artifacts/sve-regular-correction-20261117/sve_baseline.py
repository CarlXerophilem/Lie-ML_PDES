#!/usr/bin/env python3
"""Direct conditional neural PDE baseline and shared training/evaluation engine.

Dependencies: torch>=2.2, numpy, scipy, sympy, threadpoolctl.
Install the PyTorch wheel matching your CPU/CUDA from https://pytorch.org/get-started/.
No claim is made that any library is universally fastest. BLAS thread counts are
bounded; use one DDP process per GPU, or several Gloo processes across CPU machines.
CUDA uses TF32 when supported; mixed precision is deliberately NOT used for PDE
input derivatives. torch.compile is omitted because higher-order autograd support
and compilation overhead are workload dependent.

 python sve_baseline.py train --data data --run baseline --epochs 300
 torchrun --standalone --nproc_per_node=2 sve_baseline.py train --data data --run baseline
 # Multi-node: use torchrun --nnodes=N --node_rank=R --master_addr=HOST
 # --master_port=29500 --nproc_per_node=GPUS (shared data/run directory).
 python sve_baseline.py train --data data --run baseline --resume --epochs 600
 python sve_baseline.py evaluate --data data --run baseline --correct --workers 4
 python sve_baseline.py predict --data data --run baseline --params=-.5,1.2,.05,.04,.03

A complete trainable conditional field model, not pretrained weights. Inputs:
(x,t,c,p0,kappa,beta,epsilon); outputs: positive h,u and bed elevation b.
Both methods use the same MLP size, case splits, losses, initial constraints and
corrector. Baseline is initial-field + learned time change; the architecture adds
known reference evolution and makes its learned correction vanish at epsilon=0.
Train/val/test splits are by whole parameter case, never by points of one trajectory.
Loss: supervised fields + continuous SVE residual + reference boundary data.
All errors reported by evaluation are numerical evidence, not certified PDE bounds.
Checkpoints are trusted local pickle files: never load an untrusted checkpoint.
"""
import argparse
import concurrent.futures as cf
import hashlib
from datetime import timedelta
import json
import multiprocessing as mp
import os
from pathlib import Path
import time
import numpy as np
import torch
from torch import nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, TensorDataset, DistributedSampler, Subset
import sve_basis as basis


def reference_torch(z):
    x,t,c,p0,k,beta,eps=z.unbind(-1);p=p0+k*x
    return torch.stack((1/p,-c*p,-1/p-.5*c.square()*p.square()+beta*c*k*t),-1)


def initial_torch(z):
    zero=torch.cat((z[:,:1],torch.zeros_like(z[:,1:2]),z[:,2:]),1)
    v=reference_torch(zero);x=z[:,0]/.55
    # Clamp only auxiliary denominator; the physical fields are never clipped.
    chi=torch.where(abs(x)<1,torch.exp(1-1/(1-x.square()).clamp_min(1e-6)),0.)
    return torch.stack((v[:,0]*torch.exp(z[:,6]*chi),v[:,1],v[:,2]),-1)


class DirectField(nn.Module):
    kind='baseline'
    def __init__(self,T,width=128,depth=4):
        super().__init__();self.T=T
        low=torch.tensor([-1.,0.,*basis.BOUNDS[:,0]],dtype=torch.float32)
        high=torch.tensor([1.,T,*basis.BOUNDS[:,1]],dtype=torch.float32)
        self.register_buffer('center',(low+high)/2);self.register_buffer('span',(high-low)/2)
        layers=[nn.Linear(7,width),nn.SiLU()]
        for _ in range(depth-1):layers += [nn.Linear(width,width),nn.SiLU()]
        layers += [nn.Linear(width,3)];self.net=nn.Sequential(*layers)
        nn.init.normal_(self.net[-1].weight,std=1e-3);nn.init.zeros_(self.net[-1].bias)

    def field(self,z):
        raw=self.net((z-self.center)/self.span);v0=initial_torch(z);t=z[:,1:2]
        return torch.cat((v0[:,:2]*torch.exp(t*raw[:,:2]),v0[:,2:]+t*raw[:,2:]),1)

    def forward(self,z,physics=False):
        if physics:z=z.detach().requires_grad_(True)
        v=self.field(z)
        if not physics:return v
        derivatives=[torch.autograd.grad(v[:,j].sum(),z,create_graph=True)[0][:,:2]
                     for j in range(3)]
        (hx,ht),(ux,ut),(bx,bt)=[d.unbind(-1) for d in derivatives]
        h,u,_=v.unbind(-1)
        residual=torch.stack((ht+u*hx+h*ux,ut+u*ux+hx+bx,bt+z[:,5]*ux),-1)
        # Evaluate exact same model on the two physical boundaries.
        left=z.detach().clone();right=left.clone();left[:,0]=-1.;right[:,0]=1.
        boundary=torch.cat((self.field(left)-reference_torch(left),
                            self.field(right)-reference_torch(right)),0)
        return v,residual,boundary


def load_points(folder,ids):
    inputs=[];targets=[]
    for i in ids:
        with np.load(Path(folder)/f'case_{i:06d}.npz',allow_pickle=False) as d:
            xx,tt=np.meshgrid(d['x'],d['t']);n=xx.size
            inputs.append(np.column_stack((xx.ravel(),tt.ravel(),np.tile(d['par'],(n,1)))))
            targets.append(d['values'].reshape(-1,3))
    return TensorDataset(torch.tensor(np.concatenate(inputs),dtype=torch.float32),
                         torch.tensor(np.concatenate(targets),dtype=torch.float32))


def save_checkpoint(path,content):
    temp=path.with_suffix('.tmp');torch.save(content,temp);os.replace(temp,path)


def train(a,cls,cfg,device,rank,world):
    split=json.loads((Path(a.data)/'splits.json').read_text())
    trainset=load_points(a.data,split['train']);valset=load_points(a.data,split['val'])
    sampler=DistributedSampler(trainset,num_replicas=world,rank=rank,seed=a.seed) if world>1 else None
    # No loader processes: these datasets already reside in RAM; avoids nested pools.
    loader=DataLoader(trainset,batch_size=a.batch,shuffle=sampler is None,sampler=sampler,
                      pin_memory=device.type=='cuda',num_workers=0)
    valid=DataLoader(Subset(valset,list(range(rank,len(valset),world))),batch_size=a.batch)
    model=cls(cfg['T'],a.width,a.depth).to(device)
    optimizer=torch.optim.AdamW(model.parameters(),lr=a.lr,weight_decay=1e-6)
    start=0;best=float('inf');stale=0;elapsed=0.
    checkpoint=Path(a.run)/'last.pt'
    if a.resume:
        ck=torch.load(checkpoint,map_location=device,weights_only=False)
        if ck['kind']!=cls.kind or ck['config_id']!=cfg['config_id'] or ck['width']!=a.width or ck['depth']!=a.depth:
            raise ValueError('Checkpoint/model/data configuration mismatch')
        model.load_state_dict(ck['model']);optimizer.load_state_dict(ck['optimizer'])
        start=ck['epoch']+1;best=ck['best'];stale=ck['stale'];elapsed=ck['training_seconds']
    elif checkpoint.exists():raise FileExistsError('Use --resume or a new run directory')
    wrapped=DDP(model,device_ids=[device.index] if device.type=='cuda' else None) if world>1 else model
    begin=time.perf_counter()
    for epoch in range(start,a.epochs):
        torch.manual_seed(a.seed+epoch)
        if sampler:sampler.set_epoch(epoch)
        wrapped.train();sums=torch.zeros(2,device=device)
        for z,y in loader:
            z=z.to(device,non_blocking=True);y=y.to(device,non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            pred,residual,boundary=wrapped(z,True)
            loss=(pred-y).square().mean()+a.physics*residual.square().mean()+a.boundary*boundary.square().mean()
            finite=torch.tensor(int(torch.isfinite(loss).item()),device=device)
            if world>1:dist.all_reduce(finite,op=dist.ReduceOp.MIN)
            if not finite.item():raise FloatingPointError('Nonfinite training loss on a rank')
            loss.backward();nn.utils.clip_grad_norm_(model.parameters(),1.,error_if_nonfinite=True)
            optimizer.step();sums+=torch.stack((loss.detach()*len(z),torch.tensor(float(len(z)),device=device)))
        model.eval();val=torch.zeros(2,device=device)
        with torch.no_grad():
            for z,y in valid:
                z=z.to(device);y=y.to(device);v=model(z)
                val+=torch.stack(((v-y).square().sum(),torch.tensor(float(y.numel()),device=device)))
        if world>1:dist.all_reduce(sums);dist.all_reduce(val)
        score=(val[0]/val[1]).item()
        if not np.isfinite(score):raise FloatingPointError('Nonfinite validation error')
        improved=score<best
        best=min(best,score);stale=0 if improved else stale+1
        if rank==0:
            record=dict(epoch=epoch,train_loss=(sums[0]/sums[1]).item(),val_mse=score,
                        training_seconds=elapsed+time.perf_counter()-begin)
            with (Path(a.run)/'history.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
            ck=dict(model=model.state_dict(),optimizer=optimizer.state_dict(),epoch=epoch,best=best,
                    stale=stale,kind=cls.kind,width=a.width,depth=a.depth,T=cfg['T'],
                    config_id=cfg['config_id'],training_seconds=record['training_seconds'],
                    arguments=vars(a),torch_version=torch.__version__,world_size=world,
                    source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in Path(__file__).parent.glob('sve_*.py')})
            save_checkpoint(checkpoint,ck)
            if improved:save_checkpoint(Path(a.run)/'best.pt',ck)
            print(json.dumps(record),flush=True)
        if world>1:dist.barrier()
        if stale>=a.patience:break


def infer(model,par,x,t,device,batch=8192):
    xx,tt=np.meshgrid(x,t);z=np.column_stack((xx.ravel(),tt.ravel(),np.tile(par,(xx.size,1))))
    parts=[]
    if device.type=='cuda':torch.cuda.synchronize()
    start=time.perf_counter()
    with torch.no_grad():
        for b in range(0,len(z),batch):
            parts.append(model(torch.tensor(z[b:b+batch],dtype=torch.float32,device=device)).cpu().numpy())
    if device.type=='cuda':torch.cuda.synchronize()
    result=np.concatenate(parts).reshape(len(t),len(x),3).astype(np.float64)
    if not np.isfinite(result).all() or np.any(result[...,:2]<=0):raise ValueError('Invalid neural output')
    return result,time.perf_counter()-start


def residual_stats(model,par,x,t,device):
    xx,tt=np.meshgrid(x,t)
    z=np.column_stack((xx.ravel(),tt.ravel(),np.tile(par,(xx.size,1))))
    maxima=np.zeros(3);start=time.perf_counter()
    for j in range(0,len(z),1024):
        _,r,_=model(torch.tensor(z[j:j+1024],dtype=torch.float32,device=device),True)
        values=r.detach().abs().amax(0).cpu().numpy()
        if not np.isfinite(values).all():raise ValueError('Nonfinite PDE residual')
        maxima=np.maximum(maxima,values)
    return dict(sampled_pde_max=maxima.tolist(),residual_check_seconds=time.perf_counter()-start)


def evaluate_case(job):
    i,par,x,t,coarse,pred,seconds,do_correct,tol,out,checks=job
    report=dict(case=i,inference_seconds=seconds,status='failed',**checks)
    try:
        fine,reference_seconds=basis.solve(par,2*len(x),t)
        xx=basis.grid(2*len(x))
        fine=np.stack([np.column_stack([np.interp(x,xx,v[:,j]) for j in range(3)]) for v in fine])
        report.update(status='ok',reference_seconds=reference_seconds,
                      h_max_error=float(abs(pred[...,0]-fine[...,0]).max()),
                      field_rmse=np.sqrt(np.mean((pred-fine)**2,axis=(0,1))).tolist(),
                      reference_grid_gap=float(abs(coarse[...,0]-fine[...,0]).max()))
        outputs=dict(prediction=pred,reference=fine,x=x,t=t,par=par)
        if do_correct:
            try:
                corrected,stats=basis.correct(par,x,t,pred,tol)
                report['correction']=stats;report['corrected_h_max_error']=float(abs(corrected[...,0]-fine[...,0]).max())
                outputs['corrected']=corrected
                # Same corrector, classical warm start: isolate benefit of the learned proposal.
                classical=np.stack([basis.initial(x,par) for _ in t])
                direct,stats=basis.correct(par,x,t,classical,tol)
                report['classical_correction']=stats
                report['classical_h_max_error']=float(abs(direct[...,0]-fine[...,0]).max())
            except Exception as exc:report['correction_failure']=f'{type(exc).__name__}: {str(exc)[:200]}'
        np.savez_compressed(Path(out)/f'prediction_{i:06d}.npz',**outputs)
    except Exception as exc:report['error']=f'{type(exc).__name__}: {str(exc)[:200]}'
    return report


def evaluate(a,cls,cfg,device):
    ck=torch.load(Path(a.run)/'best.pt',map_location=device,weights_only=False)
    if ck['kind']!=cls.kind or ck['config_id']!=cfg['config_id']:raise ValueError('Incompatible checkpoint')
    model=cls(ck['T'],ck['width'],ck['depth']).to(device);model.load_state_dict(ck['model']);model.eval()
    x=basis.grid(cfg['nx']);t=np.linspace(0,cfg['T'],cfg['nt'])
    if a.command=='predict':
        par=np.array([float(v) for v in a.params.split(',')])
        if par.shape!=(5,) or np.any(par<basis.BOUNDS[:,0]) or np.any(par>basis.BOUNDS[:,1]):
            raise ValueError('Parameters outside trained family; refusing silent extrapolation')
        pred,seconds=infer(model,par,x,t,device)
        outputs=dict(prediction=pred,x=x,t=t,par=par,inference_seconds=seconds)
        if a.correct:outputs['corrected'],stats=basis.correct(par,x,t,pred,a.tol);print(json.dumps(stats))
        np.savez_compressed(Path(a.run)/'prediction.npz',**outputs);return
    split=json.loads((Path(a.data)/'splits.json').read_text());jobs=[];failures=[]
    for i in split['test']:
        with np.load(Path(a.data)/f'case_{i:06d}.npz',allow_pickle=False) as d:
            par=d['par'];coarse=d['values']
        try:
            pred,seconds=infer(model,par,x,t,device)
            checks=residual_stats(model,par,x,t,device)
            jobs.append((i,par,x,t,coarse,pred,seconds,a.correct,a.tol,a.run,checks))
        except Exception as exc:failures.append(dict(case=i,status='failed',error=str(exc)))
    with cf.ProcessPoolExecutor(max_workers=a.workers,mp_context=mp.get_context('spawn')) as pool:
        reports=list(pool.map(evaluate_case,jobs))+failures
    last=torch.load(Path(a.run)/'last.pt',map_location='cpu',weights_only=False)
    generation_seconds=0.
    for case in Path(a.data).glob('case_*.npz'):
        with np.load(case,allow_pickle=False) as d:generation_seconds+=float(d['seconds'])
    result=dict(kind=cls.kind,checkpoint_epoch=ck['epoch'],training_seconds=last['training_seconds'],
                data_generation_case_seconds_sum=generation_seconds,
                config_id=cfg['config_id'],cases=reports,
                failed_cases=sum(r['status']!='ok' for r in reports),
                correction_failures=sum('correction_failure' in r for r in reports),
                evidence='Sampled error against a refined numerical reference; not continuous certification')
    basis.atomic_json(Path(a.run)/'evaluation.json',result);print(json.dumps(result,indent=2))


def main(cls=DirectField):
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('command',choices=['train','evaluate','predict'])
    p.add_argument('--data',default='data');p.add_argument('--run',default=cls.kind)
    p.add_argument('--epochs',type=int,default=300);p.add_argument('--batch',type=int,default=1024)
    p.add_argument('--width',type=int,default=128);p.add_argument('--depth',type=int,default=4)
    p.add_argument('--lr',type=float,default=1e-3);p.add_argument('--physics',type=float,default=.1)
    p.add_argument('--boundary',type=float,default=1.);p.add_argument('--patience',type=int,default=40)
    p.add_argument('--seed',type=int,default=2026);p.add_argument('--threads',type=int,default=2)
    p.add_argument('--workers',type=int,default=4);p.add_argument('--resume',action='store_true')
    p.add_argument('--correct',action='store_true');p.add_argument('--tol',type=float,default=1e-8)
    p.add_argument('--params',default='-.5,1.2,.05,.04,.03');p.add_argument('--cpu',action='store_true')
    a=p.parse_args()
    if min(a.threads,a.workers,a.batch,a.width,a.depth,a.epochs,a.patience)<=0 or a.tol<=0 or a.lr<=0:
        raise ValueError('Counts, learning rate and tolerance must be positive')
    if a.physics<0 or a.boundary<0:raise ValueError('Loss weights must be nonnegative')
    torch.set_num_threads(a.threads);torch.manual_seed(a.seed)
    world=int(os.environ.get('WORLD_SIZE','1'));rank=int(os.environ.get('RANK','0'))
    local=int(os.environ.get('LOCAL_RANK','0'))
    device=torch.device(f'cuda:{local}' if torch.cuda.is_available() and not a.cpu else 'cpu')
    if device.type=='cuda':torch.cuda.set_device(device);torch.set_float32_matmul_precision('high')
    if world>1:
        if a.command!='train':raise ValueError('Use one launcher for evaluation; --workers parallelizes cases')
        dist.init_process_group('nccl' if device.type=='cuda' else 'gloo',timeout=timedelta(seconds=120))
    try:
        cfg=json.loads((Path(a.data)/'config.json').read_text())
        if cfg['model']!='SVE-m1-g1-well-balanced-v1':raise ValueError('Unknown governing model')
        Path(a.run).mkdir(parents=True,exist_ok=True)
        if a.command=='train':train(a,cls,cfg,device,rank,world)
        else:evaluate(a,cls,cfg,device)
    finally:
        if dist.is_initialized():dist.destroy_process_group()

if __name__=='__main__':main()
