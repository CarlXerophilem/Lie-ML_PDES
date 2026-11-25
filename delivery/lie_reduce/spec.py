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
    domain_exclusions: tuple = ()

    def shell_certificate(self):
        """A simple root is required; solve() alone would wrongly accept Delta=ut**2."""
        from .identities import require_zero, nonzero_record
        if len(self.equations)!=len(self.principal):
            raise ValueError('square principal block required; complete an overdetermined system separately')
        if any(sp.sympify(eq).has(sp.Float) for eq in self.equations):
            raise ValueError('exact PDE input required')
        solutions=sp.solve(self.equations,self.principal,dict=True,simplify=False)
        if len(solutions)!=1 or set(solutions[0])!=set(self.principal):
            raise ValueError('principal derivatives do not define a unique explicit chart')
        solution=solutions[0]
        if any(v.has(*self.principal) for v in solution.values()):
            raise ValueError('principal chart is implicit')
        for eq in self.equations:
            require_zero(eq.subs(solution,simultaneous=True),'principal substitution')
        jacobian=sp.Matrix(self.equations).jacobian(self.principal)
        determinant=sp.factor(jacobian.det().subs(solution,simultaneous=True))
        regularity=nonzero_record(determinant,self.positive)
        if regularity['status']=='zero':
            raise ValueError('singular equation presentation: principal Jacobian vanishes on shell')
        denominators=tuple(dict.fromkeys((*self.domain_exclusions,*(sp.denom(v) for v in self.equations),*(sp.denom(sp.cancel(v)) for v in solution.values()))))
        exclusions=tuple(nonzero_record(v,self.positive) for v in denominators)
        for denominator in denominators:
            if nonzero_record(denominator.subs(solution,simultaneous=True),self.positive)['status']=='zero':
                raise ValueError('principal solution lies on an excluded denominator locus')
        return {'solution':solution,'principal_jacobian':jacobian,'determinant_on_shell':determinant,
                'regularity':regularity,'denominators':denominators,'denominator_evidence':exclusions,
                'local_solvability':'not implied by algebraic solve; requires analytic Cauchy or other theorem hypotheses',
                'formal_integrability':'not computed for arbitrary systems'}

    def shell(self):
        certificate=self.shell_certificate()
        return certificate['solution'],certificate['denominators']
