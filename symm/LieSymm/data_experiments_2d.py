"""Namespaced facade for the byte-pinned data_experiments_2d implementation."""
from ._loader import load_module

_implementation = load_module('data_experiments_2d')
__all__ = ['COORDINATES', 'uniform_rotating_flow', 'constant_slope_flow', 'initial_data_stabilizer', 'conservative_point_map', 'pushforward_generator', 'signed_coriolis_reflection']
globals().update({name: getattr(_implementation, name) for name in __all__})
