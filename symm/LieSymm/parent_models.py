"""Namespaced facade for the byte-pinned parent_models implementation."""
from ._loader import load_module

_implementation = load_module('parent_models')
__all__ = ['scalar_models', 'verify_scalar_and_material']
globals().update({name: getattr(_implementation, name) for name in __all__})
