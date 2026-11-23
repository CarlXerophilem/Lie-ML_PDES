"""Namespaced facade for the byte-pinned models implementation."""
from ._loader import load_module

_implementation = load_module('models')
__all__ = ['t', 'x', 'h', 'u', 'B', 'g', 'K', 'G', 'm', 'n', 'BRANCHES', 'branch_model']
globals().update({name: getattr(_implementation, name) for name in __all__})
