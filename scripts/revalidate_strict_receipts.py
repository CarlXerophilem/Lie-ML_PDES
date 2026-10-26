"""Recheck recorded CAS outputs; never label replay as a fresh solve."""
import argparse,hashlib,json,sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import cases,model,atomic_json
from symm.LieSymm import strict
from symm.LieSymm.core import json_ready


def revalidate_receipt(definition, original, *, require_input_fingerprint=True):
    """Replay vendor output only after checking its mathematical input.

    Historical receipts without the newer full fingerprint may be migrated by
    the serial revalidation CLI. Supplementary reducers require the full hash.
    This does not perform or claim a fresh CAS solve.
    """
    expected=strict.input_fingerprint(**definition)
    recorded=original.get('input_sha256')
    if (require_input_fingerprint or recorded is not None) and recorded!=expected:
        raise ValueError('Full mathematical input fingerprint mismatch')
    mode=original.get('cas_mode','liepde')
    script=(strict.analyze_strict(**definition,cas_mode=mode)['cas_script'] if mode=='crack'
            else strict.liepde_script(**definition))
    if hashlib.sha256(script.encode()).hexdigest()!=original['cas']['input_sha256']:
        raise ValueError('CAS input mismatch')
    if original['cas']['status'] not in ('returned-solved','returned-partial','unparsed'):
        raise ValueError('No completed CAS output to revalidate')
    captured={**original['cas'],'status':'unparsed','execution_kind':'historical_output_revalidation'}
    with patch.object(strict,'run_reduce',return_value=captured):
        report=strict.analyze_strict(**definition,cas_command=['recorded-output-only'],cas_mode=mode)
    if require_input_fingerprint and not report.get('branch_correspondence',{}).get('matched'):
        raise ValueError('Matched terminal branch conditions are required')
    return report


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=ROOT/'build/sve-strict-lie-20261026');parser.add_argument('--out',type=Path,default=ROOT/'build/final-20261027/revalidated');args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    summary=[]
    for key in cases():
        source=args.source/(key.replace(':','--')+'-60.json')
        if not source.exists():continue
        old=json.loads(source.read_text());definition=model(key)
        report=revalidate_receipt(definition,old,require_input_fingerprint=False)
        report['revalidation']={'original_receipt_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'strict_source_sha256':hashlib.sha256(Path(strict.__file__).read_bytes()).hexdigest(),'execution_kind':'historical_output_revalidation'}
        report['translation_reduction']=strict.reduce_from_analysis(report)
        report['transfer_diagnostics']=old.get('transfer_diagnostics')
        atomic_json(args.out/source.name,json_ready(report))
        row={'case':key,'branch_match':report.get('branch_correspondence',{}).get('matched',False),'guard_status':report.get('guard_status'),'verified_families':sum(c.get('verified',False) for c in report.get('independent_checks',[])),'strict_pass':False};summary.append(row);print(row,flush=True)
        atomic_json(args.out/'summary.json',summary)

if __name__=='__main__':main()
