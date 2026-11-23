"""Record serial validation without hiding failed historical checks."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if (out / 'commands.json').exists():
        parser.error('Select a new output directory; earlier receipts are immutable')
    python = [sys.executable, '-B', '-X', 'utf8']
    pytest = ['-m', 'pytest', '-q', '-p', 'no:cacheprovider']
    active = ['symm/LieSymm/tests', 'symm/LieSymm/scalar2026/tests',
              'scripts/tests', 'symm/tests/test_engine.py',
              'symm/tests/test_chart_reduction.py',
              'research_artifacts/sve-progress-20261010/tests']
    active += [p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'symm/tests').glob('test_generic_*.py'))]
    jobs = [
        ('active-regression', pytest + ['--basetemp', str(out/'pytest-active')] + active),
        ('historical-regression', pytest + ['--basetemp', str(out/'pytest-historical'), 'symm/LieSymm/_snapshot/tests']),
        ('integrity', ['-m', 'symm.LieSymm', '--check-integrity']),
        ('audit', ['scripts/project.py', 'audit', '--out', str(out/'audit')]),
        ('data-flux', ['scripts/project.py', 'data-flux', '--out', str(out/'data-flux')]),
        ('workflow', ['scripts/project.py', 'workflow', '--out', str(out/'workflow'),
                      '--data-report', str(out/'data-flux/data_flux.json')]),
        ('dissertation-identities', ['scripts/verify_dissertation_interfaces.py', '--out', str(out/'dissertation-identities.json')]),
    ]
    rows = []
    env = {**os.environ, 'PYTHONUTF8': '1', 'PYTHONHASHSEED': '0'}
    for name, command in jobs:
        started = time.monotonic()
        with (out/(name+'.log')).open('wb') as stream:
            result = subprocess.run(python+command, cwd=ROOT, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=1800)
        rows.append({'name': name, 'command': python+command, 'returncode': result.returncode,
                     'elapsed_seconds': time.monotonic()-started,
                     'log_sha256': hashlib.sha256((out/(name+'.log')).read_bytes()).hexdigest()})
        (out/'commands.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
        print(name, result.returncode, flush=True)
    return int(any(row['returncode'] for row in rows))


if __name__ == '__main__':
    raise SystemExit(main())
