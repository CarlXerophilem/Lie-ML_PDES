#!/usr/bin/env python3
"""Run verification, single-PDE controls, or a conditional SVE benchmark."""
import argparse
import csv
import json
import platform
import time
from pathlib import Path
import numpy as np
import scipy
import sympy
import torch
from models import suite, conditional_family
from symbolic import audit_suite
from numerics import ladder
from pinns import train_run


def parse():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--task',choices=['verify','suite','family'],default='verify')
    p.add_argument('--cases',nargs='+',default=['flat','sve_m3','sve_m3.1'])
    p.add_argument('--architectures',nargs='+',choices=['mlp','modified','deeponet'],default=['mlp'])
    p.add_argument('--methods',nargs='+',choices=['vanilla','lie','reweighted','cosine','conservation'],default=['vanilla','lie','reweighted'])
    p.add_argument('--seeds',type=int,nargs='+',default=[0,1,2])
    p.add_argument('--steps',type=int,default=400)
    p.add_argument('--collocation',type=int,default=128)
    p.add_argument('--width',type=int,default=32)
    p.add_argument('--lr',type=float,default=.001)
    p.add_argument('--horizon',type=float,default=.25)
    p.add_argument('--grids',type=int,nargs='+',default=[12,18,24])
    p.add_argument('--eval-grid',type=int,default=16)
    p.add_argument('--threads',type=int,default=1)
    p.add_argument('--sym-weight',type=float,default=1.)
    p.add_argument('--generators',nargs='+',choices=['D','V','J','Tt','Tx','Ty'],default=None)
    p.add_argument('--accuracy',type=float,default=.05,help='maximum relative evolution error over active fields')
    p.add_argument('--out',default='results/pilot')
    args=p.parse_args()
    if args.steps<1 or args.collocation<8 or args.horizon<=0 or args.width<4:
        p.error('positive steps/horizon, collocation>=8 and width>=4 required')
    if args.grids!=sorted(set(args.grids)) or min(args.grids)<8 or args.eval_grid<8:
        p.error('distinct increasing grids >=8, eval-grid>=8 required')
    if args.sym_weight<0 or args.accuracy<=0:
        p.error('nonnegative symmetry weight and positive accuracy required')
    return args


def flatten(records):
    rows=[]
    for run in records:
        for name,score in run['test_metrics'].items():
            rows.append({**{k:run[k] for k in ['architecture','method','seed','status','parameters','train_seconds',
                                             'training_wall_seconds','total_seconds']},'case':name,
                         **{k:v for k,v in score.items() if not isinstance(v,dict)}})
    return rows


def main():
    args=parse();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True)
    torch.set_num_threads(args.threads);torch.set_num_interop_threads(args.threads)
    from verify import run as verify
    check=verify();(out/'verification.json').write_text(json.dumps(check,indent=2))
    print('Verification passed.',flush=True)
    if args.task=='verify':
        return
    start=time.perf_counter()
    if args.task=='family':
        train,test=conditional_family();groups=[('family',train,test)];cases=train+test
    else:
        catalog=suite();selected=list(catalog.values()) if args.cases==['all'] else [catalog[n] for n in args.cases]
        groups=[(c.name,[c],[c]) for c in selected];cases=selected
    audits=audit_suite(cases,out)
    references={};diagnostics={};reference_start=time.perf_counter()
    for case in cases:
        times,reference,diag=ladder(case,args.grids,args.horizon,args.eval_grid)
        references[case.name]=(times,reference,diag);diagnostics[case.name]=diag
    (out/'numerical_references.json').write_text(json.dumps(diagnostics,indent=2))
    reference_wall=time.perf_counter()-reference_start
    environment={'python':platform.python_version(),'platform':platform.platform(),'processor':platform.processor(),
                 'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,'torch':torch.__version__,
                 'torch_threads':torch.get_num_threads(),'device':'CPU','dtype':'float64'}
    payload={'arguments':vars(args),'environment':environment,'cases':[c.metadata() for c in cases],
             'reference_wall_seconds':reference_wall,'runs':[],'protocol':{
             'fixed_paired_collocation':True,'parameter_matched_architectures':True,
             'checkpoint':'final fixed step; test diagnostics never select checkpoint or loss weight',
             'accuracy':'max per-active-field relative evolution L2 <= accuracy; reference uncertainty separately guarded',
             'scope':'smooth periodic 2+1 SWE/Grass-SVE adaptation, not reproduction of paper Heat/Burgers tables'}}
    for name,train,test in groups:
        for architecture in args.architectures:
            for seed in args.seeds:
                for method in args.methods:
                    directory=out/name/architecture/f'seed{seed}'/method
                    record=train_run(train,test,references,audits,architecture,method,seed,args,directory)
                    record['group']=name;payload['runs'].append(record)
                    payload['wall_seconds']=time.perf_counter()-start
                    (out/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=False))
                    scores=list(record['test_metrics'].values())
                    print(f'{name} {architecture} seed={seed} {method}: {record["train_seconds"]:.2f}s, '
                          f'evolution errors={[round(s["evolution_relative_l2"],4) for s in scores]}',flush=True)
    rows=flatten(payload['runs'])
    with (out/'metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    from visualize import render
    render(out)
    print(f'Results: {out}',flush=True)


if __name__=='__main__':
    main()
