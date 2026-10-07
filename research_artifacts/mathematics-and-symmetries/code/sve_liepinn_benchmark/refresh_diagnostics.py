#!/usr/bin/env python3
"""Add final-checkpoint diagnostics without retraining or changing measured times."""
import argparse
import csv
import json
import numpy as np
import torch
from models import Case,equation_scales
from pinns import PINN,gradient_diagnostics
from visualize import relocate_directories,render
from benchmark import flatten


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('out');args=p.parse_args()
    from pathlib import Path
    out=Path(args.out).resolve();payload=json.loads((out/'results.json').read_text())
    reference_diagnostics=json.loads((out/'numerical_references.json').read_text())
    audits=json.loads((out/'symbolic.json').read_text());configuration=payload['arguments']
    torch.set_num_threads(configuration['threads']);torch.set_num_interop_threads(configuration['threads'])
    relocate_directories(payload['runs'],out)
    for run in payload['runs']:
        if 'gradient_diagnostics' not in run:
            checkpoint=torch.load(Path(run['directory'])/'model.pt',map_location='cpu',weights_only=True)
            model=PINN(checkpoint['architecture'],checkpoint['horizon'],checkpoint['width'])
            model.load_state_dict(checkpoint['state_dict'])
            case=Case(**checkpoint['train_cases'][0]);rng=np.random.default_rng(run['seed']+1123)
            points=torch.tensor(rng.random((configuration['collocation'],3))*[configuration['horizon'],2*np.pi,2*np.pi],dtype=torch.float64)
            generators=configuration['generators'] if configuration['generators'] is not None else audits[case.name]['useful_generators']
            run['gradient_diagnostics']=gradient_diagnostics(model,points,case,run['method'],generators,configuration['sym_weight'])
        for name,scores in run['test_metrics'].items():
            case=next(Case(**c) for c in payload['cases'] if c['name']==name)
            data=np.load(Path(run['directory'])/(name+'.npz'));ref=data['reference']
            active=[0,1,2]+([3] if case.kappa else [])
            scale=max(float(np.sqrt(np.mean((ref[1:]-ref[0])**2,axis=(0,1,2)))[active].min()),1e-14)
            diag=reference_diagnostics[name];uncertainty=diag['estimated_reference_uncertainty']
            good=uncertainty is not None and uncertainty/scale<configuration['accuracy']/10 and diag['tight']['sampled_max_eigenvalue_imag']<1e-10
            good=good and diag['tight']['min_depth']>0
            branch=scores['min_depth']>0 and (not case.kappa or scores['min_speed']>1e-6)
            scores['reference_accuracy_guard_passed']=bool(good);scores['sampled_physical_branch_passed']=bool(branch)
            scores['matched_accuracy']=bool(run['status']=='ok' and good and branch and scores['max_active_field_evolution_error']<=configuration['accuracy'])
            if not scores['matched_accuracy']:
                scores['new_parameter_query_break_even']=None;scores['break_even_reason']='accuracy threshold not reached'
    payload['postprocess_note']='Final-checkpoint gradient/physical/reference diagnostics added without retraining or modifying original timings.'
    (out/'results.json').write_text(json.dumps(payload,indent=2,allow_nan=False))
    rows=flatten(payload['runs'])
    with (out/'metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    render(out)
    print('Diagnostic refresh completed.',flush=True)


if __name__=='__main__':main()
