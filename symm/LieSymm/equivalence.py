"""Namespaced facade for the byte-pinned equivalence implementation."""
from ._loader import load_module

_implementation = load_module('equivalence')
__all__ = ['parameter_map', 'effective_exponents', 'normal_form', 'equivalence_status', 'verify_maps']
globals().update({name: getattr(_implementation, name) for name in __all__})
