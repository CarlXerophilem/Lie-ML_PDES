#!/usr/bin/env python3
"""Repeated measured costs of exact candidate verification, not full classification."""
import argparse
import json
from pathlib import Path
import numpy as np
from models import suite
from symbolic import audit


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repeats',type=int,default=5)
    p.add_argument('--out',default='results/symbolic_repeated.json')
    args=p.parse_args()
    if args.repeats<2:p.error('at least two repeats required')
    records={}
    for name,case in suite().items():
        trials=[audit(case) for _ in range(args.repeats)]
        timings={key:{'median':float(np.median([r[key] for r in trials])),
                      'min':float(min(r[key] for r in trials)),'max':float(max(r[key] for r in trials))}
                 for key in ['total_seconds','build_seconds','scaling_seconds']}
        generators={g:{'median':float(np.median([next(a['verify_seconds'] for a in r['generators'] if a['generator']==g) for r in trials]))}
                    for g in [r['generator'] for r in trials[0]['generators']]}
        records[name]={'repeats':args.repeats,'seconds':timings,'generators':generators,'audit':trials[0],
                       'cache_note':'in-process repeats use SymPy caches; first trial and all trials retained','trials':trials}
        print(name,timings['total_seconds'],flush=True)
    destination=Path(args.out);destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(records,indent=2))


if __name__=='__main__':main()
