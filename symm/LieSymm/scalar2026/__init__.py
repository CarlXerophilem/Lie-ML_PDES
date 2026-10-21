"""Source-faithful 2026 printed scalar SVE reductions, separate from E and M.

Importing this module does not run a campaign or write historical evidence.
The historical implementation is loaded lazily after its SHA256 is checked.
"""
from .api import (
    backend, derive_reduction, compute_ode_series, printed_pde,
    exact_solution_checks, traveling_quadrature, source_audit,
)
from .catalog import solution_catalog
from .solving import solve_reduction
from .validation import verify_solution

__all__ = [
    'backend', 'derive_reduction', 'compute_ode_series', 'printed_pde',
    'exact_solution_checks', 'traveling_quadrature', 'source_audit',
    'solution_catalog', 'solve_reduction', 'verify_solution',
]
