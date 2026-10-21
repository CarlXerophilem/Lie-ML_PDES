"""Namespaced facade for the byte-pinned reductions implementation."""
from ._loader import load_module

_implementation = load_module('reductions')
__all__ = ['basis_combination', 'traveling_reduction', 'scaling_reduction', 'constant_slope_graph', 'initial_data_stabilizer']
globals().update({name: getattr(_implementation, name) for name in __all__})
