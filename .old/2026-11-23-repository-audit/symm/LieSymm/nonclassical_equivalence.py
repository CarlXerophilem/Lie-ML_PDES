"""Namespaced facade for the byte-pinned nonclassical_equivalence implementation."""
from ._loader import load_module

_implementation = load_module('nonclassical_equivalence')
__all__ = ['COORDINATES', 'FIELDS', 'FROZEN_REGISTRY_SHA256', 'CLASSICAL', 'NONCLASSICAL', 'solution_family_containment', 'classical_distribution_equivalence', 'special_solution_collapse_control', 'evaluate_frozen_registry']
globals().update({name: getattr(_implementation, name) for name in __all__})
