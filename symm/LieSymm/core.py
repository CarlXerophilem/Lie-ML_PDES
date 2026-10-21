"""General jets, determining equations, recursive checks, and graph algebra."""
from ._loader import load_module

_core = load_module("main")
__all__ = ["JetSpace", "EvolutionShell", "multi_indices", "arbitrary_generator",
           "characteristic", "prolongation_coefficients", "point_action", "split_free_jets",
           "generalized_power_terms", "verify_generator", "lie_bracket", "algebra_structure",
           "graph_check", "json_ready", "print_derivation"]
globals().update({name: getattr(_core, name) for name in __all__})


def analyze(independent_variables, dependent_fields, equations, parameters,
            branch_conditions, data_case=None):
    """Derive determining equations; classify only exact supported fingerprints.

    Three coordinates use the frozen 2D dispatcher and its Stage 1 gate.
    The normal-form backend can reject singular/unsupported equations explicitly.
    """
    from .provenance import provenance_summary
    result = load_module("general_sve").analyze(
        independent_variables, dependent_fields, equations, parameters,
        branch_conditions, data_case)
    result["library_provenance"] = provenance_summary()
    return result


__all__.append("analyze")
