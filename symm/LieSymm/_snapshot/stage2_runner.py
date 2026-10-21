"""Sequential 2D branch execution, authorized only by the current 1D gate."""
from pathlib import Path
import hashlib
import json
import sys
from models_2d import BRANCHES_2D
from run_all import run_command

HERE=Path(__file__).resolve().parent


def source_hashes():
    paths=list(HERE.glob('*.py'))+list((HERE/'cases').glob('*.py'))
    paths+=list((HERE/'cases_2d').glob('*.py'))+list((HERE/'tests').glob('*.py'))
    return {str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}


def run(output):
    from gatekeeper import check_gate
    preceding=check_gate(1)
    if not preceding['passed']:
        raise ValueError(preceding)
    output=Path(output).resolve()
    if not output.is_relative_to(HERE) or output==HERE or output.exists():
        raise ValueError('Use a NEW output directory inside this cycle')
    output.mkdir(parents=True)
    before=source_hashes()
    receipts=[]
    for name in BRANCHES_2D:
        script=HERE/'cases_2d'/f'{name}.py'
        command=[sys.executable,'-B',str(script),'--out',str(output/name),'--trace','full']
        receipt=run_command(command,output/f'{name}.log',timeout=240)
        receipt.update(branch=name,child_sha256=hashlib.sha256(script.read_bytes()).hexdigest())
        derivation=output/name/'derivation.json'
        receipt['derivation_sha256']=hashlib.sha256(derivation.read_bytes()).hexdigest() if derivation.is_file() else None
        receipts.append(receipt)
        print(name,receipt['process_status'],receipt['exit_code'],flush=True)
    after=source_hashes()
    result={'stage':'2','execution_passed':all(r['exit_code']==0 for r in receipts) and before==after,
            'source_hashes_before':before,'source_hashes_after':after,'sources_unchanged_during_run':before==after,
            'preceding_gate':preceding,'receipts':receipts,
            'classification_gate':'requires independent necessity review and fresh project validation'}
    (output/'receipts.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if result['execution_passed'] else 1
