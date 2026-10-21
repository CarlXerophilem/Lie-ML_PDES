"""Namespaced facade for the byte-pinned data_experiments implementation."""
from ._loader import load_module

_implementation = load_module('data_experiments')
__all__ = ['uniform_flow', 'constant_slope_flow', 'sediment_flux_variation', 'initial_data_stabilizer', 'lake_control']
globals().update({name: getattr(_implementation, name) for name in __all__})
