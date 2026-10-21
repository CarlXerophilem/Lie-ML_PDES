"""Namespaced facade for the byte-pinned reductions_2d implementation."""
from ._loader import load_module

_implementation = load_module('reductions_2d')
__all__ = ['plane_wave', 'rotating_radial', 'rotation_scaling_time_ode']
globals().update({name: getattr(_implementation, name) for name in __all__})
