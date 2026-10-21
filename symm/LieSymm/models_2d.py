"""Namespaced facade for the byte-pinned models_2d implementation."""
from ._loader import load_module

_implementation = load_module('models_2d')
__all__ = ['t', 'x', 'y', 'h', 'u', 'v', 'B', 'g', 'K', 'G', 'm', 'n', 'f', 'BRANCHES_2D', 'branch_model_2d', 'recover_one_dimension']
globals().update({name: getattr(_implementation, name) for name in __all__})
