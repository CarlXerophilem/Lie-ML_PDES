"""Definition 6.1 records and per-process resource accounting."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "delivery" / "nonlinear_results"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def environment():
    versions = {}
    for name in ("numpy", "scipy", "sympy", "torch", "python-flint", "mpmath", "matplotlib"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    cpu = subprocess.check_output(["lscpu", "-J"], text=True)
    info = {v["field"].rstrip(":"): v["data"] for v in json.loads(cpu)["lscpu"]}
    return {"python": platform.python_version(), "platform": platform.platform(),
            "versions": versions, "cpu_model": info.get("Model name"),
            "logical_cpus": os.cpu_count(),
            "memory_total_kib": int(Path("/proc/meminfo").read_text().splitlines()[0].split()[1]),
            "threads": {k: os.environ.get(k) for k in
                        ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")},
            "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}


class Timer:
    def __init__(self):
        self.wall = time.perf_counter()
        self.start = resource.getrusage(resource.RUSAGE_SELF)

    def result(self):
        end = resource.getrusage(resource.RUSAGE_SELF)
        return {"wall_seconds": time.perf_counter()-self.wall,
                "user_cpu_seconds": end.ru_utime-self.start.ru_utime,
                "system_cpu_seconds": end.ru_stime-self.start.ru_stime,
                "peak_process_rss_bytes": end.ru_maxrss*1024}


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+"\n")
    tmp.replace(path)


def run_record(kind, settings):
    return {"schema_version": 2, "definition": "Dissertation Definition 6.1",
            "kind": kind, "settings": settings, "environment": environment()}
