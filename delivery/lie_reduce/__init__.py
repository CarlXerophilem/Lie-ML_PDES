"""Deterministic symbolic PDE -> Lie algebra -> subalgebra combination -> ODE reducer."""
import dataclasses
try:
    import resource
except ImportError:  # Windows has no resource module.
    resource = None
import signal
import time
import sys
import threading
import sympy as sp

from .jets import JetSpace
from .spec import PDESpec


class StageTimeout(Exception):
    pass


def timed(fn, seconds):
    def interrupt(*_):
        raise StageTimeout(f'symbolic stage exceeded {seconds} seconds')

    start = time.perf_counter()
    cpu = time.process_time()
    usage = resource.getrusage(resource.RUSAGE_SELF) if resource else None
    use_timer = seconds > 0
    timer_available = (hasattr(signal, "SIGALRM") and hasattr(signal, "setitimer")
                       and threading.current_thread() is threading.main_thread())
    old = None
    try:
        if use_timer:
            if not timer_available:
                raise RuntimeError("Positive stage timeouts require a POSIX main thread; use --stage-seconds 0 to explicitly disable.")
            old = signal.signal(signal.SIGALRM, interrupt)
            signal.setitimer(signal.ITIMER_REAL, seconds)
        value = fn()
        status, reason = 'completed', None
    except Exception as exc:
        value = None
        status = 'time_limit' if isinstance(exc, StageTimeout) else 'failed'
        reason = f'{type(exc).__name__}: {exc}'
    finally:
        if old is not None:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
    end_usage = resource.getrusage(resource.RUSAGE_SELF) if resource else None
    return {
        'status': status,
        'reason': reason,
        'wall_seconds': time.perf_counter() - start,
        'cpu_seconds': time.process_time() - cpu,
        'user_cpu_seconds': end_usage.ru_utime - usage.ru_utime if usage else None,
        'system_cpu_seconds': end_usage.ru_stime - usage.ru_stime if usage else None,
        'process_peak_rss_bytes': (end_usage.ru_maxrss * (1 if sys.platform == "darwin" else 1024)) if end_usage else None,
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


# Stable entry points; implementation details live in their original modules.
__version__ = "0.1.0"
from .models import discover_and_enumerate
from .reduce import ReducedODE, reduce as reduce_spec

__all__ = ["JetSpace", "PDESpec", "ReducedODE", "discover_and_enumerate",
           "reduce_spec", "timed", "serial", "__version__"]
