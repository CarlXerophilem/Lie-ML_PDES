"""Deterministic symbolic PDE -> Lie algebra -> subalgebra combination -> ODE reducer."""
import dataclasses
import resource
import signal
import time
import sympy as sp

from .jets import JetSpace
from .spec import PDESpec


class StageTimeout(Exception):
    pass


def timed(fn, seconds):
    def interrupt(*_):
        raise StageTimeout(f'symbolic stage exceeded {seconds} seconds')

    old = signal.signal(signal.SIGALRM, interrupt)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    start = time.perf_counter()
    cpu = time.process_time()
    usage = resource.getrusage(resource.RUSAGE_SELF)
    try:
        value = fn()
        status, reason = 'completed', None
    except Exception as exc:
        value = None
        status = 'time_limit' if isinstance(exc, StageTimeout) else 'failed'
        reason = f'{type(exc).__name__}: {exc}'
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old)
    return {
        'status': status,
        'reason': reason,
        'wall_seconds': time.perf_counter() - start,
        'cpu_seconds': time.process_time() - cpu,
        'user_cpu_seconds': resource.getrusage(resource.RUSAGE_SELF).ru_utime - usage.ru_utime,
        'system_cpu_seconds': resource.getrusage(resource.RUSAGE_SELF).ru_stime - usage.ru_stime,
        'process_peak_rss_bytes': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
        'value': value,
    }


def serial(value):
    if isinstance(value, JetSpace):
        return {
            'independent': serial(value.independent),
            'dependent': serial(value.dependent),
            'order': value.order,
            'jet_symbols': serial(value.jets),
        }
    if dataclasses.is_dataclass(value):
        return serial(dataclasses.asdict(value))
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(v) for v in value]
    if isinstance(value, sp.MatrixBase):
        return serial(value.tolist())
    if isinstance(value, sp.Basic):
        return str(value)
    return value
