#!/usr/bin/env python3
"""Unified ODE candidate manager; verification is an external two-input boundary."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse
import fcntl
import json
from pathlib import Path
import resource
import time
import sys
import sympy as sp
from ode_methods.task import Task

ROOT=Path(__file__).resolve().parent
METHODS=('taylor','chebyshev','pinn','lnn','prefix')


def training_task(data):
    allowed={'id','operator','residual','initial','interval','physical_scale','b','slope','residual_numerator','residual_denominator'}
    return Task({k:v for k,v in data.items() if k in allowed})


def budgeted_fit(task,method,args,prefix,out):
    from ode_methods.neural import fit
    lock_path=out/'training_budget.lock';ledger_path=out/'training_budget.json'
    with lock_path.open('w') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        if ledger_path.exists():ledger=json.loads(ledger_path.read_text())
        else:
            # Keep a conservative reserved allowance for pre-manager legacy/pilot
            # work. This ledger applies to managed runs, not undocumented history.
            ledger={'limit_cpu_seconds':7200,'reserved_prior_cpu_seconds':120,'runs':[]}
        used=ledger['reserved_prior_cpu_seconds']+sum(r['cpu_seconds'] for r in ledger['runs'])
        available=ledger['limit_cpu_seconds']-used
        if available<=0:return {'status':'not_run','termination':'global_cpu_budget'}
        start=time.process_time()
        try:return fit(task,method,args.steps,min(args.cpu_seconds,available),args.seed,prefix)
        finally:
            ledger['runs'].append({'task':task.data['id'],'method':method,'seed':args.seed,'cpu_seconds':time.process_time()-start})
            ledger_path.write_text(json.dumps(ledger,indent=2)+'\n')


def solve(data,method,args,out):
    from ode_methods.classical import taylor,chebyshev,analytic
    contract=data['paper_contract']
    for key in ('residual','residual_numerator','residual_denominator'):
        if key in data and data[key]!=contract.get(key):raise ValueError('training equation differs from independent verification contract: '+key)
    if data['initial']!=contract['trace_value']:raise ValueError('training trace differs from verification contract')
    task=training_task(data);start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_SELF)
    if method=='taylor':candidate=taylor(task,args.degree)
    elif method=='chebyshev':candidate=chebyshev(task,args.degree)
    elif method=='analytic':candidate=analytic(task)
    else:
        prefix=taylor(task,3)['coefficients'] if method=='prefix' else None
        candidate=budgeted_fit(task,method,args,prefix,out)
    after=resource.getrusage(resource.RUSAGE_SELF)
    cost={'wall_seconds':time.perf_counter()-start,'user_cpu_seconds':after.ru_utime-before.ru_utime,
          'system_cpu_seconds':after.ru_stime-before.ru_stime,'process_peak_rss_bytes':after.ru_maxrss*1024}
    # Import only AFTER candidate construction. No verifier/reference callback is
    # passed to any optimizer; the checker imports no ODE-method modules.
    from lie_pde_reducer import verifier
    from managed_runtime import environment,digest
    verification_start=time.perf_counter()
    verification=verifier(candidate,json.dumps(data['paper_contract'])) if 'representation' in candidate else {'status':'not_applicable','reason':candidate.get('reason',candidate['status'])}
    return {'schema':'Definition 6.1 method record','task':data['id'],'method':method,
            'environment':environment(),'manager_sha256':digest(__file__),
            'settings':{'seed':args.seed,'degree':args.degree,'max_steps':args.steps,'max_training_cpu_seconds':args.cpu_seconds,
                        'device':'CPU','dtype':'exact symbolic' if method in ('taylor','analytic') else 'float64',
                        'training_used':method in ('pinn','lnn','prefix'),'threads':1,'run_class':'pilot' if args.steps<8000 else 'budgeted_run'},
            'candidate':candidate,'verification':verification,'cost':cost,'verification_wall_seconds':time.perf_counter()-verification_start,
            'training_input_fields':sorted(task.data),'continuous_neural_certificate':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tasks',type=Path,default=ROOT/'managed_results'/'tasks.json')
    parser.add_argument('--task',default='N1');parser.add_argument('--all-tasks',action='store_true')
    parser.add_argument('--method',choices=(*METHODS,'analytic','all'),default='all')
    parser.add_argument('--degree',type=int,default=10);parser.add_argument('--steps',type=int,default=8000)
    parser.add_argument('--cpu-seconds',type=float,default=150);parser.add_argument('--seed',type=int,default=27)
    parser.add_argument('--out',type=Path,default=ROOT/'managed_results'/'ode')
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    if args.degree<2 or args.steps<1 or args.cpu_seconds<=0:parser.error('positive budgets and degree>=2 required')
    payload=json.loads(args.tasks.read_text())
    if payload['schema']!='verified-ode-tasks-v1':parser.error('verified task export required')
    tasks=[v for v in payload['tasks'] if args.all_tasks or v['id']==args.task]
    if not tasks:parser.error('unknown task')
    methods=METHODS if args.method=='all' else (args.method,)
    run_dir=args.out/str(time.time_ns());run_dir.mkdir();summary=[]
    # Freeze the precise task inputs beside candidates for later independent replay.
    (run_dir/'TASKS.json').write_text(json.dumps(payload,indent=2)+'\n')
    for data in tasks:
        for method in methods:
            print(data['id'],method,'started',flush=True)
            try:
                from lie_reduce.run import timed
                stage=timed(lambda:solve(data,method,args,args.out),max(60,2*args.cpu_seconds))
                record=stage['value'] if stage['status']=='completed' else {'task':data['id'],'method':method,'status':stage['status'],'reason':stage['reason']}
            except Exception as exc:record={'task':data['id'],'method':method,'status':'failed','reason':f'{type(exc).__name__}: {exc}'}
            (run_dir/(data['id']+'_'+method+'.json')).write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
            summary.append({k:record.get(k) for k in ('task','method','status','reason','settings','cost','verification_wall_seconds')})
            summary[-1]['termination']=record.get('candidate',{}).get('termination',record.get('candidate',{}).get('status'))
            summary[-1]['verification']=record.get('verification',{}).get('status')
            print(summary[-1],flush=True)
    (run_dir/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(run_dir)


if __name__=='__main__':main()
