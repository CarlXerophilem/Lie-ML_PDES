"""Bounded follow-up of the poles actually returned by the generic CRACK run."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import psutil
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import model,cas_command,cleanup_linux,require_cleanup,atomic_json
from scripts.summarize_strict_lie import audit_algebra
from symm.LieSymm import strict
from symm.LieSymm.core import json_ready


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-root',type=Path,required=True)
    args=parser.parse_args();root=args.runtime_root.resolve();out=root/'exceptional-retry'
    out.mkdir(exist_ok=False)
    previous=json.loads((root/'campaign/summary.json').read_text())
    spent=previous['charged_seconds'];rows=[]
    active=[p.info for p in psutil.process_iter(['pid','name','status'])
            if p.info['name'] in ('reduce','redcsl') and p.info['status']!=psutil.STATUS_ZOMBIE]
    atomic_json(out/'process-preflight.json',{'live_cas':active,'previous_cleanup_failure_preserved':True})
    if active:raise RuntimeError('Existing CAS process; refusing overlapping solve')
    for exponent in (1,2):
        definition=model('E1:grass_generic')
        m=next(p for p in definition['parameters'] if str(p)=='m')
        definition['branch_conditions']['substitutions']={m:sp.Integer(exponent)}
        definition['branch_conditions']['fixed_parameters']['m']=sp.Integer(exponent)
        definition['branch_conditions']['model_id']=f'E1:grass_generic:m{exponent}'
        limit=min(300,7200-spent-1)
        if limit<=0:break
        pid=out/f'm{exponent}.pid';prefix=out/f'm{exponent}'
        atomic_json(out/'running.json',{'exponent':exponent,'budget_before':spent,'limit':limit})
        report=None
        try:
            report=strict.analyze_strict(**definition,cas_mode='crack',
                cas_command=cas_command(root,limit,pid,memory_bytes=8_000_000_000),
                timeout=limit,memory_bytes=8_000_000_000,cas_log_prefix=prefix)
        finally:
            cleanup=cleanup_linux(pid)
            atomic_json(out/f'm{exponent}-cleanup.json',cleanup)
        report['linux_cleanup']=cleanup
        atomic_json(out/f'm{exponent}.json',json_ready(report))
        require_cleanup(cleanup)
        report['translation_reduction']=strict.reduce_from_analysis(report)
        if report.get('cas_solution'):
            report['algebra']=audit_algebra(definition,report['cas']['stdout'],report['independent_checks'],cas_mode='crack')
        atomic_json(out/f'm{exponent}.json',json_ready(report))
        (out/'running.json').unlink()
        spent+=report['cas']['elapsed_seconds']
        row={'name':f'direct-m{exponent}','status':report['cas']['status'],
             'elapsed_seconds':report['cas']['elapsed_seconds'],'linux_cleanup':cleanup,
             'returned_family_verified':report.get('returned_family_verified',False),
             'input_sha256':report['cas']['input_sha256']}
        rows.append(row)
        atomic_json(out/'summary.json',{'budget_seconds':7200,'charged_seconds':spent,'jobs':rows,'strict_pass':False})
        print(json.dumps(row),flush=True)


if __name__=='__main__':main()
