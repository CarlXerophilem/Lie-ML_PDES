"""Namespaced facade for the byte-pinned nonclassical implementation."""
from ._loader import load_module

_implementation = load_module('nonclassical')
__all__ = ['FIELDS', 'COORDINATES', 'P', 'R', 'UT', 'UY', 'A', 'C', 'GUARDS', 'validate_candidate', 'conditional_system', 'invariant_graph', 'compatible_families', 'analyze_candidate', 'serialize_result']
globals().update({name: getattr(_implementation, name) for name in __all__})
