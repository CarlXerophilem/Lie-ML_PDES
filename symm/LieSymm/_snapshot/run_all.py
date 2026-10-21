"""Run each 1D child separately; preserve exit status, timing and source hashes."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from models import BRANCHES

HERE=Path(__file__).resolve().parent


def source_hashes():
    paths=list(HERE.glob('*.py'))+list((HERE/'cases').glob('*.py'))+list((HERE/'tests').glob('*.py'))
    return {str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def run_command(command, log_path, timeout=180, cwd=None):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    timer=time.perf_counter()
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',
               PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
    with open(log_path,'wb') as stream:
        try:
            result=subprocess.run(command,cwd=cwd or HERE,stdout=stream,stderr=subprocess.STDOUT,
                                  env=env,timeout=timeout,check=False)
            exit_code=result.returncode
            status='exited'
        except subprocess.TimeoutExpired:
            exit_code=None
            status='timeout'
    return {'command':command,'cwd':str(cwd or HERE),'started_utc':start,
            'elapsed_seconds':time.perf_counter()-timer,'timeout_seconds':timeout,
            'exit_code':exit_code,'process_status':status,'log':str(log_path),
            'log_sha256':hashlib.sha256(Path(log_path).read_bytes()).hexdigest(),
            'cpu_lease':'cpu-symbolic','heavy_concurrency':1,'python_hash_seed':0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--stage',choices=['1','2','nonclassical'],default='1')
    args=parser.parse_args()
    if args.stage != '1':
        from gatekeeper import check_gate
        gate=check_gate(1 if args.stage=='2' else 2)
        if not gate['passed']:
            parser.error('Preceding complete-classification review gate has not passed')
        import importlib
        module_name='stage2_runner' if args.stage=='2' else 'nonclassical_runner'
        try:
            runner=importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name!=module_name:
                raise
            parser.error('The reviewed preceding stage passed, but this downstream runner is not implemented')
        return runner.run(args.out)
    output=args.out.resolve()
    if not output.is_relative_to(HERE) or output == HERE or output.exists():
        parser.error('Choose a NEW output directory inside this cycle')
    output.mkdir(parents=True)
    before=source_hashes()
    receipts=[]
    for name in BRANCHES:
        script=HERE/'cases'/f'{name}.py'
        command=[sys.executable,'-B',str(script),'--out',str(output/name),'--trace','full']
        receipt=run_command(command,output/f'{name}.log')
        receipt['branch']=name
        receipt['child_sha256']=hashlib.sha256(script.read_bytes()).hexdigest()
        receipts.append(receipt)
        print(name,receipt['process_status'],receipt['exit_code'],flush=True)
    after=source_hashes()
    result={'stage':'1','execution_passed':all(r['exit_code']==0 for r in receipts) and before==after,
            'source_hashes_before':before,'source_hashes_after':after,'sources_unchanged_during_run':before==after,
            'classification_gate':'requires independent necessity review and validation receipt',
            'receipts':receipts,
            'sources':after}
    (output/'receipts.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['execution_passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
