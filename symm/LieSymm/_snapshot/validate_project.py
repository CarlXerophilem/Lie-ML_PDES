"""Required isolated validation; no repository-wide pytest collection."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from run_all import run_command, source_hashes

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    output=args.out.resolve()
    if not output.is_relative_to(HERE) or output.exists():
        parser.error('Use a NEW output directory inside this cycle')
    output.mkdir(parents=True)
    before=source_hashes()
    commands=[
        ('audit',[sys.executable,'-B','scripts/project.py','audit','--out',str(output/'audit')]),
        ('data-flux',[sys.executable,'-B','scripts/project.py','data-flux','--out',str(output/'data-flux')]),
        ('workflow',[sys.executable,'-B','scripts/project.py','workflow','--out',str(output/'workflow'),
                     '--data-report',str(output/'data-flux'/'data_flux.json')]),
        ('engine-chart',[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider','scripts/tests',
                         'symm/tests/test_chart_reduction.py','symm/tests/test_engine.py',
                         '--basetemp='+str(output/'tmp-engine')]),
        ('active-package',[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',
                           'research_artifacts/sve-progress-20261010/tests',
                           '--basetemp='+str(output/'tmp-active')]),
        ('new-cycle',[sys.executable,'-B','-m','pytest','-q','-p','no:cacheprovider',str(HERE/'tests'),
                      '--basetemp='+str(output/'tmp-new')]),
    ]
    receipts=[]
    for name,command in commands:
        receipt=run_command(command,output/f'{name}.log',timeout=240,cwd=ROOT)
        receipt['name']=name
        receipts.append(receipt)
        print(name,receipt['process_status'],receipt['exit_code'],flush=True)
    original=json.loads((HERE/'protected_inputs.json').read_text(encoding='utf-8'))
    unchanged=[]
    for item in original['files']:
        path=ROOT/item['path']
        current=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        unchanged.append({'path':item['path'],'unchanged':current==item['sha256'] and path.exists()==item['exists']})
    after=source_hashes()
    result={'receipts':receipts,'protected_inputs':unchanged,
            'source_hashes_before':before,'source_hashes_after':after,'sources_unchanged_during_run':before==after,
            'all_protected_inputs_unchanged':all(v['unchanged'] for v in unchanged),
            'all_commands_passed':all(r['exit_code']==0 for r in receipts)}
    (output/'receipts.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if (result['all_commands_passed'] and result['all_protected_inputs_unchanged']
                 and result['sources_unchanged_during_run']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
