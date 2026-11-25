"""Standard-library resource and provenance records; no solver dependencies."""
from functools import lru_cache
from importlib import metadata
from pathlib import Path
import hashlib
import os
import platform
import sys


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def environment():
    cpu = Path('/proc/cpuinfo')
    model = next((line.split(':', 1)[1].strip() for line in cpu.read_text().splitlines()
                  if line.startswith('model name')), None) if cpu.exists() else platform.processor()
    memory = Path('/proc/meminfo')
    total = next((int(line.split()[1]) * 1024 for line in memory.read_text().splitlines()
                  if line.startswith('MemTotal:')), None) if memory.exists() else None
    versions = {}
    for package in ('sympy', 'numpy', 'scipy', 'torch', 'mpmath', 'python-flint'):
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    return {'python': platform.python_version(), 'executable': sys.executable,
            'platform': platform.platform(), 'cpu_model': model,
            'logical_cpu_count': os.cpu_count(),
            'cpu_affinity_count': len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else None,
            'host_memory_bytes': total, 'versions': versions,
            'memory_scope': 'host total; process peak RSS is cumulative, not per-method allocation'}
