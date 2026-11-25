"""Immutable b9842d6 numerical and table regression; timing is observational."""
import json
from pathlib import Path
import sys
import numpy as np
import sympy as sp
from .record import ROOT, save, run_record, Timer
from .audit import command


def run(out):
    out=Path(out);timer=Timer()
    frozen=json.loads(Path(__file__).with_name('frozen_baseline.json').read_text())
    report=run_record('legacy_regression',{'baseline':frozen['commit'],'rtol':frozen['rtol'],'atol':frozen['atol']})
    rows=[];commands=[]
    for name in ('ml_sv2022','ml_sve2026','ml_new_model2026'):
        commands.append(command([sys.executable,'-B',f'delivery/{name}.py'],out/f'{name}.json'))
        rows.extend(json.loads((out/f'{name}.json').read_text()))
    checks=[]
    for actual,expected in zip(rows,frozen['rows'],strict=True):
        assert actual['settings']==expected['settings']
        assert actual['test_traces']==expected['test_traces']
        assert actual['fit']['nfev']==150
        for method,metrics in expected['metrics'].items():
            for name,value in metrics.items():
                if 'seconds' in name: continue
                observed=actual['metrics'][method][name]
                ok=bool(np.isclose(observed,value,rtol=frozen['rtol'],atol=frozen['atol']))
                checks.append({'case':actual['case'],'method':method,'metric':name,'expected':value,'observed':observed,'passed':ok})
    from semianalytic_defect import run as tank
    tank_rows=[]
    for method in ('fit','taylor'):
        row=tank(method,sp.Rational(3,20),10,17,128,sp.Integer(4))
        save(out/f'tank_{method}.json',row)
        # The immutable source is replayed in a separate module for exact comparison.
        import subprocess,types
        old=types.ModuleType('frozen_tank')
        exec(subprocess.check_output(['git','show','b9842d6:delivery/semianalytic_defect.py'],cwd=ROOT,text=True),old.__dict__)
        assert row==old.run(method,sp.Rational(3,20),10,17,128,sp.Integer(4))
        tank_rows.append({'method':method,'exact_record_equal':True})
    manuscript=(ROOT/'draft/dissertation_wku_compact.tex').read_text()
    # Blocks may move to an appendix, but their literal numerical content is frozen.
    for label,block in frozen['tables'].items():
        assert block in manuscript,label
    report.update(status='passed' if all(c['passed'] for c in checks) else 'failed',
                  checks=checks,tank=tank_rows,frozen_table_blocks_equal=True,commands=commands,resources=timer.result())
    save(out/'REGRESSION.json',report)
    if report['status']!='passed': raise AssertionError('Legacy regression failed; original values remain frozen')
    return report
