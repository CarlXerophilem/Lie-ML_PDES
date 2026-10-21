"""Namespaced facade for the byte-pinned algebra_2d implementation."""
from ._loader import load_module

_implementation = load_module('algebra_2d')
__all__ = ['COORDINATES', 'bracket', 'constant_coordinates', 'adjoint_action', 'representative_subalgebras']
globals().update({name: getattr(_implementation, name) for name in __all__})
