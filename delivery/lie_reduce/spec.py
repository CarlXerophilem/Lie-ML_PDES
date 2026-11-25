from dataclasses import dataclass
import sympy as sp
from .jets import JetSpace


@dataclass(frozen=True)
class PDESpec:
    name: str
    jets: JetSpace
    equations: tuple
    principal: tuple
    parameters: tuple = ()
    conditions: tuple = ()
    positive: tuple = ()

    def shell(self):
        """Unique explicit principal chart; no positivity inferred from a sign."""
        solutions = sp.solve(self.equations, self.principal, dict=True, simplify=False)
        if len(solutions) != 1 or set(solutions[0]) != set(self.principal):
            raise ValueError('principal derivatives do not define a unique explicit chart')
        solution = solutions[0]
        if any(v.has(*self.principal) for v in solution.values()):
            raise ValueError('principal chart is implicit')
        return solution, tuple(sp.denom(sp.cancel(v)) for v in solution.values())
