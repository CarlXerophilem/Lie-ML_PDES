"""Namespaced facade for the byte-pinned ml_adapter implementation."""
from ._loader import load_module

_implementation = load_module('ml_adapter')
__all__ = ['FIELDS', 'T', 'RHO', 'Z', 'F', 'P', 'g', 'K', 'validate_candidate', 'graph_certificate', 'build_certificate', 'encode', 'decode', 'encode_certificate']
globals().update({name: getattr(_implementation, name) for name in __all__})
