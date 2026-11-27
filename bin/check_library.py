#!/usr/bin/env python3
"""Small portable symbolic smoke test, after installing the package."""
import sympy as sp
from lie_reduce import JetSpace, PDESpec, ReducedODE, discover_and_enumerate, reduce_spec, timed
from lie_reduce.models import euler_spec


def main():
    spec, basis, subs = discover_and_enumerate(euler_spec())
    assert len(basis) == 4
    x1 = next(s for s in subs if s["id"] == "X1")
    result = reduce_spec(spec, x1["generators"])
    assert isinstance(result, ReducedODE)
    assert result.status == "verified", result.reason
    assert len(result.reduced_equations) == 1
    assert "m" in {str(p) for p in result.preserved_parameters}
    t, x, u = sp.symbols("t x u")
    jets = JetSpace((t, x), (u,), 2)
    heat = PDESpec("heat", jets, (jets.jet(0, 1, 0)-jets.jet(0, 0, 2),), (jets.jet(0, 1, 0),))
    assert heat.shell_certificate()["determinant_on_shell"] == 1
    assert timed(lambda: 7, 0)["value"] == 7
    print("Symbolic library smoke test passed: E1 quotient, symbolic m, custom PDE shell, explicit no-timeout.")


if __name__ == "__main__":
    main()
