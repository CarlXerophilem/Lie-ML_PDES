"""Independently revalidate the remote generic result without another CAS run."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import model,atomic_json
from scripts.summarize_strict_lie import audit_algebra
from symm.LieSymm import strict
from symm.LieSymm.core import json_ready


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'build/final-20261027/remote')
    p.add_argument('--out',type=Path,default=ROOT/'research_artifacts/sve-final-20261027/data')
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    original=json.loads((a.source/'campaign/direct-generic.json').read_text())
    definition=model('E1:grass_generic')
    initial=strict.analyze_strict(**definition,cas_mode='crack')
    if hashlib.sha256(initial['cas_script'].encode()).hexdigest()!=original['input_sha256']:
        raise ValueError('Exact direct-CRACK input fingerprint mismatch')
    captured={**original,'status':'unparsed','execution_kind':'historical_output_revalidation'}
    with patch.object(strict,'run_reduce',return_value=captured):
        report=strict.analyze_strict(**definition,cas_mode='crack',cas_command=['recorded-output-only'])
    report['translation_reduction']=strict.reduce_from_analysis(report)
    report['algebra']=audit_algebra(definition,original['stdout'],report['independent_checks'],cas_mode='crack')
    report['revalidation']={'original_receipt_sha256':hashlib.sha256((a.source/'campaign/direct-generic.json').read_bytes()).hexdigest(),
        'strict_source_sha256':hashlib.sha256(Path(strict.__file__).read_bytes()).hexdigest(),
        'execution_kind':'historical_output_revalidation'}
    atomic_json(a.out/'remote-generic-verified.json',json_ready(report))
    summary=json.loads((a.source/'campaign/summary.json').read_text())
    summary['initial_charged_seconds']=summary['charged_seconds']
    for row in summary['jobs']:
        row['original_status']=row['status']
        if row['name']=='direct-generic':
            row['status']=report['cas']['status']
            row['returned_family_verified']=report['returned_family_verified']
            row['algebra_dimension']=report['algebra'][0]['dimension']
            row['domain_note']='Assignment denominators exclude m=1,2; no completeness proof'
        elif row['name']=='fixed-positive':
            row['diagnosis']='Exit 0 without terminal frame; abrupt output end, underlying cause not established'
        elif row['name'].startswith('official-'):
            row['diagnosis']='Distribution sample completed; not a target determining-system certificate'
    extra=json.loads((a.source/'exceptional-retry/summary.json').read_text())
    summary['jobs']+=extra['jobs'];summary['charged_seconds']=extra['charged_seconds']
    summary['remaining_seconds']=7200-summary['charged_seconds']
    summary['serial_gate_violation']={'job':'direct-classify','original_status':'cleanup-failed',
        'controller_continued':True,'fixed_runner_stops':True,
        'later_process_check_sha256':hashlib.sha256((a.source/'process-check.txt').read_bytes()).hexdigest(),
        'explanation':'Later absence of processes does not prove no overlap at the original transition'}
    summary['exceptional_diagnostics']={
        'm1':'One residual differential equation remains; not a closed general solution',
        'm2':'Returned expressions contain unevaluated int/noint and derivative dependencies; parser refuses unsupported expressions'}
    summary['strict_pass']=False
    atomic_json(a.out/'remote-summary.json',summary)
    print(json.dumps({k:summary[k] for k in ['charged_seconds','remaining_seconds','strict_pass']}))
    print('Generic family verified:',report['returned_family_verified'],'algebra dimension:',report['algebra'][0]['dimension'])


if __name__=='__main__':main()
