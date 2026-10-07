#!/usr/bin/env python3
"""Post-hoc parameter sensitivity and checkpoint replay; never selects weights."""
import argparse
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
import torch
import series_kan as sk
from baseline_core.models import Case
from baseline_core.numerics import solve,interpolate


def load_model(checkpoint):
    model=sk.Field(checkpoint['kind'],checkpoint['horizon'],checkpoint['series_order'])
    for _ in range(1,checkpoint['blocks']):model.blocks.append(sk.RawNet(checkpoint['kind'],zero_output=True))
    model.weights=checkpoint['weights'];model.load_state_dict(checkpoint['state_dict']);return model


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('out');args=p.parse_args()
    out=Path(args.out).resolve();data=json.loads((out/'results.json').read_text());configuration=data['arguments']
    torch.set_num_threads(1);torch.set_num_interop_threads(1);sk.COEFFICIENTS,_=sk.make_coefficients()
    family=configuration['family'];parameter='m' if family=='sve' else 'coriolis'
    center=Case('sensitivity',m=3,amplitude=.03) if family=='sve' else Case('sensitivity',coriolis=.1,kappa=0,bed_amplitude=0,amplitude=.03)
    steps=[.01,.005];reference={};diag={}
    for delta in steps:
        predictions=[]
        for sign in [-1,1]:
            case=replace(center,**{parameter:getattr(center,parameter)+sign*delta})
            times,fields,metadata=solve(case,24,configuration['horizon'],rtol=1e-11,atol=1e-13)
            predictions.append(interpolate(fields,configuration['n']));diag[f'{delta}_{sign}']=metadata
        reference[delta]=(predictions[1]-predictions[0])/(2*delta)
    active=[0,1,2]+([3] if center.kappa else [])
    reference_difference=float(np.max(abs(reference[steps[0]]-reference[steps[1]])))
    records=[];replay={}
    for run in data['runs']:
        directory=out/run['method']/f"seed{run['seed']}"
        checkpoint=torch.load(directory/'model.pt',map_location='cpu',weights_only=True);model=load_model(checkpoint)
        case=Case(**data['test_cases'][0]);saved=np.load(directory/(case.name+'.npz'))
        difference=float(np.max(abs(sk.predict(model,case,saved['times'],configuration['n'])-saved['prediction'])))
        assert difference<1e-14
        replay[f"{run['method']}_{run['seed']}"]=difference
        delta=steps[-1]
        estimates=[sk.predict(model,replace(center,**{parameter:getattr(center,parameter)+s*delta}),times,configuration['n']) for s in [-1,1]]
        sensitivity=(estimates[1]-estimates[0])/(2*delta)
        norms=np.sqrt(np.mean(reference[delta][1:]**2,axis=(0,1,2)))
        errors=np.sqrt(np.mean((sensitivity-reference[delta])[1:]**2,axis=(0,1,2)))
        per_field=errors/np.maximum(norms,1e-14)
        records.append({'method':run['method'],'seed':run['seed'],
                        'parameter_derivative_relative_l2':float(np.linalg.norm((sensitivity-reference[delta])[1:,...,active])/max(np.linalg.norm(reference[delta][1:,...,active]),1e-14)),
                        'per_field_relative_l2':dict(zip(['h','u','v','b'],map(float,per_field))),
                        'per_field_absolute_derivative_error_rms':dict(zip(['h','u','v','b'],map(float,errors))),
                        'reference_derivative_field_rms':dict(zip(['h','u','v','b'],map(float,norms)))})
    result={'status':'passed-checkpoint-replay','parameter':parameter,'center':center.metadata(),
            'finite_difference_steps':steps,'reference_difference_between_steps_max':reference_difference,
            'reference_diagnostics':diag,'runs':records,'checkpoint_replay_max':max(replay.values()),
            'scope':'post-hoc local central finite differences; weak sensitivities can have ill-conditioned relative errors; no parameter-gradient certificate'}
    (out/'sensitivity.json').write_text(json.dumps(result,indent=2));print(json.dumps({'parameter':parameter,'runs':len(records),'replay_max':max(replay.values())}))


if __name__=='__main__':main()
