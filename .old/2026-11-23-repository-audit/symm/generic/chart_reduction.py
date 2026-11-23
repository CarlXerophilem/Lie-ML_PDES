"""Exact local reduction in a supplied projectable one-generator chart.

The verified scope is the PDE pullback on recorded regularity conditions.
No characteristic integration, maximal symmetry classification, differential
completion, nonempty-branch proof or IBVP existence theorem is claimed.
"""

from dataclasses import dataclass

import sympy as sp

from .core import JetSpace, PointGenerator, ReducedSystem, ReductionCertificate, ReductionMap, fingerprint
from .jets import characteristic, iter_multi_indices, jet_coordinates, prolonged_action, prolonged_system
from .problem import DataCondition, PDEProblem


@dataclass(frozen=True)
class ReductionChart:
    reduced_space: JetSpace
    invariants: tuple[sp.Expr, ...]
    orbit_variable: sp.Symbol
    orbit_coordinate: sp.Expr
    inverse_coordinates: tuple[sp.Expr, ...]
    field_reconstruction: tuple[sp.Expr, ...]
    equation_factors: tuple[sp.Expr, ...]

    def __post_init__(self):
        for name in ("invariants", "inverse_coordinates", "field_reconstruction", "equation_factors"):
            object.__setattr__(self, name, tuple(map(sp.sympify, getattr(self, name))))
        object.__setattr__(self, "orbit_coordinate", sp.sympify(self.orbit_coordinate))

    def as_dict(self):
        return {"reduced_space": self.reduced_space.as_dict(),
                "orbit_variable": sp.srepr(self.orbit_variable),
                "orbit_coordinate": sp.srepr(self.orbit_coordinate),
                **{name: list(map(sp.srepr, getattr(self, name))) for name in
                   ("invariants", "inverse_coordinates", "field_reconstruction", "equation_factors")}}


@dataclass(frozen=True)
class ChartReductionOutcome:
    reduced_system: ReducedSystem | None
    certificate: ReductionCertificate
    pulled_domain: tuple[sp.Basic, ...] = ()
    pulled_inequations: tuple[sp.Expr, ...] = ()
    pulled_data: tuple[DataCondition, ...] = ()
    regularity_conditions: tuple[sp.Basic, ...] = ()
    data_status: str = "not-checked"
    data_checks: tuple[tuple[str, bool], ...] = ()
    data_invariance_residuals: tuple[sp.Expr, ...] = ()

    def as_dict(self):
        return {"reduced_system": self.reduced_system.as_dict() if self.reduced_system else None,
                "certificate": self.certificate.as_dict(),
                "pulled_domain": list(map(sp.srepr, self.pulled_domain)),
                "pulled_inequations": list(map(sp.srepr, self.pulled_inequations)),
                "pulled_data": [item.as_dict() for item in self.pulled_data],
                "regularity_conditions": list(map(sp.srepr, self.regularity_conditions)),
                "data_status": self.data_status,
                "data_checks": list(self.data_checks),
                "data_invariance_residuals": list(map(sp.srepr, self.data_invariance_residuals))}


class _Unsupported(ValueError):
    pass


def reduce_in_chart(problem: PDEProblem, generator: PointGenerator, chart: ReductionChart,
                    *, symmetry_multipliers=None) -> ChartReductionOutcome:
    """Verify and reduce using `pr(X) Delta = M Delta` and a supplied chart.

`M` defaults to zero and must have r by r entries depending on base coordinates
and fixed parameters. Reconstruction is affine in q fresh profile coordinates.
Source-coordinate residual factors are nonzero functions of x and parameters.
All pulled domain/data constraints remain available, including orbit-dependent
ones. Callers must retain them when using the reduced equations.
"""
    system = problem.system
    space, target = system.jet_space, chart.reduced_space
    source_id = system.fingerprint()
    configuration_id = fingerprint({"problem": problem.as_dict(), "chart": chart.as_dict(),
                                    "generator": generator.as_dict(),
                                    "symmetry_multipliers": symmetry_multipliers.tolist()
                                    if isinstance(symmetry_multipliers, sp.MatrixBase)
                                    else symmetry_multipliers})
    checks = []
    residuals = []

    def check(name, condition):
        condition = bool(condition)
        checks.append((name, condition))
        if not condition:
            raise _Unsupported(name)

    def zero(expression):
        return sp.simplify(expression) == 0

    try:
        check("dimensions", space.p >= 2 and target.p == space.p-1 and target.q == space.q
              and target.max_order == space.max_order and space.max_order >= 1
              and generator.p == space.p and generator.q == space.q
              and len(chart.invariants) == target.p and len(chart.inverse_coordinates) == space.p
              and len(chart.field_reconstruction) == space.q and len(chart.equation_factors) == system.r)
        x, z, rho = space.independent_variables, target.independent_variables, chart.orbit_variable
        source_jets, reduced_jets = jet_coordinates(space), jet_coordinates(target)
        params = set(problem.parameters)
        source_symbols = set(x) | set(source_jets.values())
        target_symbols = set(z) | set(reduced_jets.values()) | {rho}
        check("fresh_chart_symbols", isinstance(rho, sp.Symbol)
              and len(target_symbols) == len(z)+len(reduced_jets)+1
              and not target_symbols & (source_symbols | params))
        base_allowed = set(x) | params
        point_allowed = base_allowed | set(space.dependent_fields)
        check("point_generator", all(not c.free_symbols-point_allowed for c in generator.xi+generator.phi))
        check("projectable_generator", all(not c.free_symbols-base_allowed for c in generator.xi))
        check("chart_dependencies", all(not e.free_symbols-base_allowed for e in
              (*chart.invariants, chart.orbit_coordinate, *chart.equation_factors))
              and all(not e.free_symbols-set(z)-{rho}-params for e in chart.inverse_coordinates)
              and all(not e.free_symbols-base_allowed-set(target.dependent_fields)
                      for e in chart.field_reconstruction))
        directional = lambda e: sp.simplify(sum(c*sp.diff(e,v) for c,v in zip(generator.xi,x)))
        check("invariants", all(zero(directional(e)) for e in chart.invariants))
        speed = directional(chart.orbit_coordinate)
        jacobian = sp.Matrix((*chart.invariants,chart.orbit_coordinate)).jacobian(x).det()
        check("base_rank", not zero(jacobian) and not zero(speed))
        inverse = dict(zip(x,chart.inverse_coordinates))
        forward = dict(zip((*z,rho),(*chart.invariants,chart.orbit_coordinate)))
        check("inverse_chart", all(zero(e.subs(inverse, simultaneous=True)-v)
              for e,v in zip((*chart.invariants,chart.orbit_coordinate),(*z,rho)))
              and all(zero(e.subs(forward, simultaneous=True)-v) for e,v in zip(chart.inverse_coordinates,x)))
        fields = target.dependent_fields
        fiber_jacobian = sp.Matrix(chart.field_reconstruction).jacobian(fields).det()
        check("affine_fiber", all(zero(sp.diff(e,u,v)) for e in chart.field_reconstruction
                                   for u in fields for v in fields))
        check("fiber_rank", not zero(fiber_jacobian))

        matrix = sp.zeros(system.r) if symmetry_multipliers is None else sp.Matrix(symmetry_multipliers)
        check("multiplier_dimensions", matrix.shape == (system.r,system.r))
        check("multiplier_dependencies", all(not c.free_symbols-base_allowed for c in matrix))
        symmetry_residuals = tuple(sp.simplify(lhs-rhs) for lhs,rhs in zip(
            prolonged_system(system,generator),matrix*sp.Matrix(system.equations)))
        residuals.extend(symmetry_residuals)
        check("symmetry_identity", all(zero(e) for e in symmetry_residuals))

        # Chain rule before changing the base coordinates. Profile jet symbols
        # are independent placeholders; their x derivatives use D_i I^j.
        invariant_jacobian = sp.Matrix(chart.invariants).jacobian(x)

        def lifted_derivative(expression, i):
            value = sp.diff(expression,x[i])
            for (field,index),symbol in reduced_jets.items():
                coefficient = sp.diff(expression,symbol)
                if coefficient == 0:
                    continue
                for j in range(target.p):
                    weight = invariant_jacobian[j,i]
                    if weight == 0:
                        continue
                    shifted = tuple(n+(k==j) for k,n in enumerate(index))
                    if (field,shifted) not in reduced_jets:
                        raise _Unsupported("jet_order_budget")
                    value += coefficient*weight*reduced_jets[(field,shifted)]
            return sp.expand(value)

        rules = dict(zip(space.dependent_fields,chart.field_reconstruction))
        for index in iter_multi_indices(space.p,space.max_order,1):
            i = next(i for i,n in enumerate(index) if n)
            previous = tuple(n-(k==i) for k,n in enumerate(index))
            for field in range(space.q):
                rules[source_jets[(field,index)]] = lifted_derivative(rules[source_jets[(field,previous)]],i)
        surface = characteristic(space,generator)
        graph_residuals = tuple(sp.simplify(e.xreplace(rules)) for e in surface)
        residuals.extend(graph_residuals)
        check("invariant_surface", all(zero(e) for e in graph_residuals))

        def pull(expression):
            return sp.simplify(expression.xreplace(rules).subs(inverse,simultaneous=True))

        factors = tuple(pull(e) for e in chart.equation_factors)
        check("nonzero_factors", all(not zero(e) for e in factors))
        pulled_equations = tuple(pull(e) for e in system.equations)
        equations = tuple(sp.factor(e/f) for e,f in zip(pulled_equations,factors))
        check("orbit_independent_equations", all(not e.has(rho) for e in equations))
        identities = tuple(sp.simplify(e-f*r) for e,f,r in zip(pulled_equations,factors,equations))
        residuals.extend(identities)
        check("pullback_identity", all(zero(e) for e in identities))

        domains = tuple(pull(e) for e in (*problem.domain,*system.assumptions))
        inequations = tuple(pull(e) for e in system.inequations)
        from .boundary import normalize_zero_condition, restrict_to_constraints
        data_units = []
        data_list = []
        for source_data in problem.data:
            normalized_surface, units = normalize_zero_condition(pull(source_data.surface))
            data_units.extend(units)
            normalized_residuals = []
            for expression in source_data.residuals:
                normalized, units = normalize_zero_condition(pull(expression))
                normalized_residuals.append(normalized)
                data_units.extend(units)
            data_list.append(DataCondition(source_data.name, normalized_surface,
                                           tuple(normalized_residuals)))
        data = tuple(data_list)
        data_checks = []
        data_invariance_residuals = []
        for source_data, pulled_data in zip(problem.data, data):
            surface_action = sp.simplify(prolonged_action(space, source_data.surface, generator))
            residual_actions = tuple(sp.simplify(prolonged_action(space, expression, generator))
                                     for expression in source_data.residuals)
            data_invariance_residuals.extend((surface_action, *residual_actions))
            boundary_test = restrict_to_constraints(surface_action, (source_data.surface,))
            data_tests = tuple(restrict_to_constraints(expression,
                               (source_data.surface, *source_data.residuals))
                               for expression in residual_actions)
            data_units.extend(pull(e) for e in boundary_test.denominator_guards)
            data_units.extend(pull(e) for test in data_tests for e in test.denominator_guards)
            data_checks.append((f"{source_data.name}.surface_invariant", boundary_test.verified))
            data_checks.append((f"{source_data.name}.residuals_invariant",
                                all(test.verified for test in data_tests)))
            data_checks.append((f"{source_data.name}.quotient_data",
                                not pulled_data.surface.has(rho)
                                and all(not expression.has(rho)
                                        for expression in pulled_data.residuals)))
        # Keep every denominator even if the final expression cancels it.
        raw_guards = [*problem.denominator_guards,jacobian,speed,fiber_jacobian,*chart.equation_factors]
        expressions = (*chart.invariants,chart.orbit_coordinate,*chart.field_reconstruction,
                       *generator.xi,*generator.phi,*matrix,*rules.values())
        raw_guards += [sp.denom(sp.together(e)) for e in expressions]
        mapped_guards = [pull(e) for e in raw_guards] + data_units
        mapped_guards += [sp.denom(sp.together(e)) for e in
                          (*chart.inverse_coordinates,*equations,*mapped_guards)]
        mapped_guards = tuple(dict.fromkeys(e for e in mapped_guards if e not in (sp.S.One,-sp.S.One)))
        check("guard_preservation", all(not zero(e) for e in (*inequations,*mapped_guards))
              and all(e is not sp.S.false for e in domains))
        conditions = tuple(sp.Ne(e,0,evaluate=False) for e in mapped_guards)

        reduction_map = ReductionMap(source_id,generator,z,fields,surface,
            tuple((key,pull(key)) for key in source_jets.values()),
            reconstruction_rules=tuple(zip(space.dependent_fields,chart.field_reconstruction)),
            rank_guards=(pull(jacobian),pull(speed),pull(fiber_jacobian)),
            denominator_guards=mapped_guards)
        reduced = ReducedSystem(target,equations,
            tuple(e for e in (*inequations,*mapped_guards) if not e.has(rho)),
            tuple(e for e in domains if not e.has(rho)),reduction_map)
        certificate = ReductionCertificate(source_id,"verified","branch-0",tuple(checks),
            residuals=tuple(residuals),covered_guards=(*inequations,*mapped_guards),
            uncovered_branches=("zeros of recorded chart and denominator guards",),
            message="exact local invariant PDE pullback on recorded smooth regular chart; no IBVP or completion claim",
            configuration_fingerprint=configuration_id)
        data_status = ("data-compatible" if data and all(value for _, value in data_checks)
                       else "pulled-back-only" if data else "not-supplied")
        return ChartReductionOutcome(reduced,certificate,domains,inequations,data,conditions,
                                     data_status,tuple(data_checks),tuple(data_invariance_residuals))
    except (_Unsupported, ValueError, TypeError, sp.PolynomialError) as exc:
        if not checks or checks[-1][1]:
            checks.append(("symbolic_operation",False))
        certificate = ReductionCertificate(source_id,"unsupported","branch-0",tuple(checks),
            residuals=tuple(residuals),message=f"supplied reduction not verified: {exc}",
            configuration_fingerprint=configuration_id)
        return ChartReductionOutcome(None,certificate)
