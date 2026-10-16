"""Run project-required checks into this inspection's isolated build directory."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"

checks = [
    ("audit", ["scripts/project.py", "audit", "--out", str(HERE / "validation/audit")]),
    ("data-flux", ["scripts/project.py", "data-flux", "--out", str(HERE / "validation/data-flux")]),
    ("workflow", ["scripts/project.py", "workflow", "--out", str(HERE / "validation/workflow"),
                  "--data-report", str(HERE / "validation/data-flux/data_flux.json")]),
    ("parameter-controls", ["draft/proposal_support/verify_parameter_effects.py"]),
    ("project-regressions", ["-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
        "--basetemp="+str(HERE / "validation/pytest-tmp"), "scripts/tests",
        "symm/tests/test_chart_reduction.py", "symm/tests/test_engine.py",
        "research_artifacts/sve-progress-20261010/tests"]),
]
receipts = []
(HERE / "validation").mkdir(exist_ok=True)
for name, args in checks:
    start = time.perf_counter()
    command = [sys.executable, *args]
    try:
        result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8",
                                errors="replace", stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=240)
        exit_code, output = result.returncode, result.stdout
    except subprocess.TimeoutExpired as exc:
        exit_code = "timeout"
        output = str(exc.stdout or "") + "\nTIMEOUT after 240 seconds\n"
    (HERE / "validation" / (name+".log")).write_text(output, encoding="utf-8")
    record = {"name":name, "command":command, "cwd":str(ROOT), "exit_code":exit_code,
              "elapsed_seconds":round(time.perf_counter()-start,3), "log":"validation/"+name+".log"}
    receipts.append(record)
    (HERE / "validation/receipts.json").write_text(json.dumps(receipts,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(record), flush=True)
