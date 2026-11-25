"""Run immutable P/M proof sources and compare their complete JSON certificate."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def verify():
    root=Path(__file__).with_name('frozen')
    manifest=json.loads((root/'manifest.json').read_text())
    for name,digest in manifest['sha256'].items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            raise ArithmeticError('frozen certificate source changed: '+name)
    result=subprocess.run([sys.executable,'-B',str(root/'frozen_PM.py')],capture_output=True,text=True,timeout=30,check=True)
    if json.loads(result.stdout)!=json.loads((root/'PM.json').read_text()):
        raise ArithmeticError('frozen P/M output differs from recorded certificate')
    return {'status':'passed','sha256':manifest['sha256'],'scope':'original smooth positive-chart proof; preserved verbatim'}


if __name__=='__main__': print(json.dumps(verify(),indent=2))
