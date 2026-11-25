#!/usr/bin/env python3
"""Unified pure-SymPy PDE manager. Numerical/ML solvers are deliberately absent."""
import argparse
import json
from pathlib import Path
import sympy as sp
from independent_verifier import verifier as _independent_verifier

ROOT=Path(__file__).resolve().parent


def _paper_text(model):
    import hashlib
    text=(ROOT/'paper_contracts'/f'{model}.json').read_text();contract=json.loads(text)
    manuscript=(ROOT.parent/'draft'/'dissertation_wku_compact.tex').read_bytes()
    if hashlib.sha256(manuscript).hexdigest()!=contract['source_sha256']:
        raise ValueError('paper transcription snapshot is stale; review it against the manuscript before verification')
    if contract['source_excerpt'] not in manuscript.decode():raise ValueError('paper excerpt differs from manuscript')
    return text


def verifier(solver_output,paper_txt_respective):
    """Public isolated two-input verifier; no solver internals enter the checker."""
    return _independent_verifier(solver_output,paper_txt_respective)


def reduction(model,exponent=2,generator=None):
    from lie_reduce.models import scalar,euler,annular
    from lie_reduce.reduce import reduce,reduce_subalgebra
    from lie_reduce.algebra import add
    from lie_reduce.run import serial
    if model=='E2':
        spec,fields,graph,_=annular();result=reduce_subalgebra(spec,fields,graph)
    else:
        spec,basis=euler(exponent) if model=='E1' else scalar(model,exponent)
        if generator=='tilted':
            c,gamma=sp.symbols('c gamma',real=True);field=add((1,basis['Y1']),(c,basis['Y3']),(gamma,basis['Y2']))
        elif generator=='bed_drift':
            alpha=sp.Symbol('alpha',real=True);field=add((1,basis['X1']),(alpha,basis['X3']))
        else:field=basis[generator or ('X4' if model=='E1' else 'Y4')]
        fields=(field,);result=reduce(spec,field)
    if result.status!='verified':return {'status':result.status,'details':serial(result)}
    graph=result.graph
    symbols=set().union(*(v.free_symbols for v in (*graph.lifts,*result.equations)))
    output={'kind':'pde_reduction','model':model,'parameter_bindings':{'m':str(exponent)} if model!='E2' else {},
            'symbols':sorted(str(v) for v in symbols),'profile_functions':[str(F.func) for F in graph.profiles],
            'generators':[[str(v) for v in X] for X in fields],
            'invariant':str(graph.invariant),'lifts':list(map(str,graph.lifts)),
            'equations':list(map(str,result.equations)),
            'weights':list(map(str,result.weights or (sp.S.One,)*len(result.equations))),
            'orbit_coordinates':{str(k):str(v) for k,v in graph.orbit_coordinates.items()},
            'conditions':serial(result.conditions),'scope':result.scope}
    text=_paper_text(model)
    return {'status':'computed','solver_output':output,'verification':verifier(output,text)}


def discover(model,exponent=2,degree=2):
    from lie_reduce.models import scalar,euler
    from lie_reduce.determining import symmetries
    from lie_reduce.run import serial
    if model=='E2':
        return {'status':'unsupported_scope','reason':'E2 uses the separately declared shared affine certificate; unrestricted polynomial planar discovery is not claimed'}
    spec,_=euler(exponent) if model=='E1' else scalar(model,exponent)
    result=symmetries(spec,degree);result.pop('matrix')
    output={'kind':'point_generators','model':model,'parameter_bindings':{'m':str(exponent)},
            'generators':[[str(v) for v in X] for X in result['basis']]}
    return {'status':'computed','discovery':serial(result),'solver_output':output,'verification':verifier(output,_paper_text(model))}


def verify_catalogue(path):
    import hashlib
    import time
    started=time.perf_counter();source=Path(path).read_bytes();catalogue=json.loads(source)
    records=[]
    for case in catalogue['runs']:
        paper=_paper_text(case['model'])
        for row in case['reductions']:
            red=row.get('value') or {}
            record={'model':case['model'],'m':case['m'],'id':row['id'],'source_status':red.get('status',row['status'])}
            if red.get('status')!='verified':
                record['verification']={'status':'not_applicable','reason':'source has no verified reduced equation to check'}
            else:
                graph=red['graph']
                output={'kind':'pde_reduction','model':case['model'],'parameter_bindings':{'m':str(case['m'])},
                    'symbols':['z','orbit','c','gamma','alpha','b','delta','epsilon'],
                    'profile_functions':[v.split('(')[0] for v in graph['profiles']],
                    'generators':[row['generator']],'invariant':graph['invariant'],'lifts':graph['lifts'],
                    'equations':red['equations'],'weights':red['weights'],
                    'orbit_coordinates':graph['orbit_coordinates'],'conditions':red['conditions']}
                record['verification']=verifier(output,paper)
            records.append(record)
        print('independent catalogue check',case['model'],case['m'],flush=True)
    return {'source_pipeline_sha256':hashlib.sha256(source).hexdigest(),'scope':'independent local pullbacks for every emitted ODE; exclusions are not reclassified',
            'records':records,'wall_seconds':time.perf_counter()-started}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--discover',action='store_true');parser.add_argument('--degree',type=int,default=2)
    parser.add_argument('--verify-catalogue',type=Path)
    parser.add_argument('--model',choices=['E1','P','M','E2']);parser.add_argument('--exponent',type=int,default=2)
    parser.add_argument('--export-tasks',action='store_true');parser.add_argument('--generator');parser.add_argument('--all-models',action='store_true')
    parser.add_argument('--out',type=Path,default=ROOT/'managed_results'/'pde.json')
    parser.add_argument('--stage-seconds',type=float,default=120)
    args=parser.parse_args()
    if args.stage_seconds<=0:parser.error('positive stage timeout required')
    if args.discover:
        if not args.model:parser.error('--discover requires --model')
        operation=lambda:discover(args.model,args.exponent,args.degree)
    elif args.verify_catalogue:
        operation=lambda:verify_catalogue(args.verify_catalogue)
    elif args.export_tasks:
        from managed_tasks import export_tasks
        operation=export_tasks
    elif args.all_models:
        cases=[('E1',2,'bed_drift'),('E1',3,'X5'),('P',3,'Y5'),('M',2,'Y4'),('M',2,'tilted'),('E2',3,None)]
        operation=lambda:[reduction(*case) for case in cases]
    elif args.model:operation=lambda:reduction(args.model,args.exponent,args.generator)
    else:parser.error('choose --model or --all-models')
    from lie_reduce.run import timed
    from managed_runtime import environment,digest
    stage=timed(operation,args.stage_seconds)
    result=stage.pop('value') if stage['status']=='completed' else {'status':stage['status'],'reason':stage['reason']}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    stage.pop('value',None)
    stage.update(environment=environment(),output_sha256=digest(args.out),
                 manager_sha256=digest(__file__),verifier_sha256=digest(ROOT/'independent_verifier.py'))
    args.out.with_suffix('.resources.json').write_text(json.dumps(stage,indent=2)+'\n')
    print(args.out)
    if stage['status']!='completed':raise SystemExit(1)


if __name__=='__main__':main()
