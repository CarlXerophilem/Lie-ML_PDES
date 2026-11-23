"""LieSymm: equation-first local analysis with explicit certificate boundaries.

Legacy symm APIs remain at their existing paths. This subpackage neither
replaces them nor imports the optional scalar2026 plotting/demo dependencies.
"""
from .core import *
from .core import __all__ as _core_exports
from .models import branch_model, BRANCHES
from .models_2d import branch_model_2d, BRANCHES_2D
from .reductions import traveling_reduction, scaling_reduction

__version__ = "0.1.0"
__all__ = [*_core_exports, "branch_model", "BRANCHES", "branch_model_2d", "BRANCHES_2D",
           "traveling_reduction", "scaling_reduction"]
