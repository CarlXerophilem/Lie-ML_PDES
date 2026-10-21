"""Namespaced facade for the byte-pinned subalgebras implementation."""
from ._loader import load_module

_implementation = load_module('subalgebras')
__all__ = ['adjoint_structure', 'resonance_strata', 'classify_subalgebra_lines', 'adjoint_action', 'canonicalize_translation_line']
globals().update({name: getattr(_implementation, name) for name in __all__})
