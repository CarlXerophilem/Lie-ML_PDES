"""General-symm: equation -> arbitrary X -> Q -> determining equations.

This readable parent deliberately separates deriving necessary equations,
integrating their general solution, checking generators, and classifying
subalgebras. A successful prolongation is never a maximality certificate.
Run ``python main.py --help``. Historical scripts are read-only inputs.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
import itertools
import json
from pathlib import Path
import time

import sympy as sp

HERE = Path(__file__).resolve().parent


# 0. Dynamic multi-field jet space. Coordinates do not depend on a global PDE.
def multi_indices(dimensions, order):
    for degree in range(order + 1):
        for index in itertools.product(range(degree + 1), repeat=dimensions):
            if sum(index) == degree:
                yield index


class JetSpace:
    def __init__(self, independent_variables, dependent_fields, max_order=6):
        self.x = tuple(independent_variables)
        self.u = tuple(dependent_fields)
        self.max_order = max_order
        if not self.x or not self.u or len(set(self.x + self.u)) != len(self.x + self.u):
            raise ValueError('Coordinates must be nonempty and disjoint')
        self.coordinates = {
            (a, index): (field if not any(index) else
                         sp.Symbol(f'{field}__' + '_'.join(map(str, index)), real=True))
            for a, field in enumerate(self.u)
            for index in multi_indices(len(self.x), max_order)
        }
        self.reverse = {symbol: key for key, symbol in self.coordinates.items()}

    def jet(self, field, index):
        if not isinstance(field, int):
            field = self.u.index(field)
        if sum(index) > self.max_order:
            raise ValueError('Jet order exhausted; no derivative may be silently dropped')
        return self.coordinates[(field, tuple(index))]

    def unit(self, axis):
        return tuple(int(i == axis) for i in range(len(self.x)))

    def D(self, expression, axis):
        expression = sp.sympify(expression)
        result = sp.diff(expression, self.x[axis])
        for symbol in expression.free_symbols & self.reverse.keys():
            a, index = self.reverse[symbol]
            shifted = list(index)
            shifted[axis] += 1
            result += sp.diff(expression, symbol) * self.jet(a, shifted)
        return sp.expand(result)

    def D_multi(self, expression, index):
        for axis, count in enumerate(index):
            for _ in range(count):
                expression = self.D(expression, axis)
        return expression

    def order(self, expressions):
        symbols = set().union(*(sp.sympify(e).free_symbols for e in expressions))
        return max((sum(self.reverse[s][1]) for s in symbols & self.reverse.keys()), default=0)


# 1. Arbitrary point coefficients, characteristic Q and point prolongation.
def arbitrary_generator(space):
    args = space.x + space.u
    return (tuple(sp.Function(f'xi_{x}')(*args) for x in space.x),
            tuple(sp.Function(f'eta_{u}')(*args) for u in space.u))


def characteristic(space, xi, eta):
    return tuple(eta[a] - sum(xi[i] * space.jet(a, space.unit(i))
                             for i in range(len(space.x))) for a in range(len(space.u)))


def prolongation_coefficients(space, xi, eta, order, method='characteristic'):
    xi, eta = tuple(map(sp.sympify, xi)), tuple(map(sp.sympify, eta))
    zero = (0,) * len(space.x)
    coefficients = {(a, zero): eta[a] for a in range(len(space.u))}
    Q = characteristic(space, xi, eta)
    for index in multi_indices(len(space.x), order):
        if not any(index):
            continue
        axis = next(i for i, count in enumerate(index) if count)
        previous = list(index)
        previous[axis] -= 1
        previous = tuple(previous)
        for a in range(len(space.u)):
            if method == 'characteristic':
                value = space.D_multi(Q[a], index)
                for j in range(len(space.x)):
                    shifted = tuple(v + int(i == j) for i, v in enumerate(index))
                    value += xi[j] * space.jet(a, shifted)
            elif method == 'recursive':
                value = space.D(coefficients[(a, previous)], axis)
                for j in range(len(space.x)):
                    shifted = tuple(v + int(i == j) for i, v in enumerate(previous))
                    value -= space.jet(a, shifted) * space.D(xi[j], axis)
            else:
                raise ValueError('Unknown prolongation method')
            value = sp.expand(value)
            if space.order((value,)) > order:
                raise ValueError('Uncancelled higher jet in point prolongation')
            coefficients[(a, index)] = value
    return coefficients


def point_action(space, equation, xi, eta, order=None, method='characteristic', coefficients=None):
    order = space.order((equation,)) if order is None else order
    coefficients = coefficients or prolongation_coefficients(space, xi, eta, order, method)
    result = sum(xi[i] * sp.diff(equation, x) for i, x in enumerate(space.x))
    for key, symbol in space.coordinates.items():
        if sum(key[1]) <= order and equation.has(symbol):
            result += coefficients[key] * sp.diff(equation, symbol)
    return sp.expand(result)


# 2. One specialized model supplies both equations and their differential shell.
class EvolutionShell:
    def __init__(self, space, equations):
        self.space = space
        self.equations = tuple(equations)
        self.divisors = []
        self.rules_used = {}
        if len(equations) != len(space.u):
            raise ValueError('This normal-form backend needs one equation per field')
        leader_order = 1
        if len(space.u) == 1:
            pure = [index[0] for (a, index), symbol in space.coordinates.items()
                    if index[0] and not any(index[1:]) and equations[0].has(symbol)]
            if pure:
                leader_order = max(pure)
        self.leader_order = leader_order
        leaders = [space.jet(a, (leader_order,) + (0,) * (len(space.x) - 1))
                   for a in range(len(space.u))]
        matrix, rhs = sp.linear_eq_to_matrix(equations, leaders)
        determinant = sp.factor(matrix.det())
        if determinant == 0:
            raise ValueError('Singular time-leading matrix: branch analysis required')
        self.divisors.append(determinant)
        self.rhs = tuple(sp.simplify(v) for v in matrix.inv() * rhs)
        if any(v.has(*leaders) for v in self.rhs):
            raise ValueError('Unresolved time-leading jets')

    @lru_cache(maxsize=None)
    def replacement(self, a, index):
        diff = (index[0] - self.leader_order,) + index[1:]
        if diff[0] < 0:
            return self.space.jet(a, index)
        expression = self.space.D_multi(self.rhs[a], diff)
        expression = self.reduce(expression)
        self.rules_used[str(self.space.jet(a, index))] = expression
        return expression

    def reduce(self, expression):
        principal = [(self.space.reverse[s], s) for s in expression.free_symbols
                     if s in self.space.reverse and self.space.reverse[s][1][0] >= self.leader_order]
        replacements = {s: self.replacement(a, index) for (a, index), s in principal}
        return sp.expand(expression.xreplace(replacements))


# 3. Split free jets, not model parameters or dependent powers of the same jet.
def split_free_jets(space, expression, shell):
    numerator, denominator = sp.fraction(sp.together(expression))
    jets = sorted((s for s in numerator.free_symbols if s in space.reverse
                   and any(space.reverse[s][1])
                   and space.reverse[s][1][0] < shell.leader_order), key=str)
    try:
        polynomial = sp.Poly(sp.expand(numerator), *jets) if jets else None
        terms = polynomial.terms() if polynomial is not None else [((), numerator)]
        equations = []
        term_records = []
        for powers, coefficient in terms:
            coefficient = sp.factor(coefficient)
            if coefficient == 0:
                continue
            term_records.append({'powers': powers, 'coefficient': coefficient})
            if coefficient not in equations:
                equations.append(coefficient)
        return {'status': 'complete_jet_split', 'equations': equations,
                'jets': jets, 'terms': term_records, 'denominator': denominator}
    except sp.PolynomialError:
        # Preserve the identity. A generalized-power splitter must prove its
        # exponent independence and resonance branches before it may replace it.
        return {'status': 'unresolved_nonpolynomial_jet_identity',
                'equations': [numerator], 'jets': jets, 'terms': [],
                'denominator': denominator}


def generalized_power_terms(expression, variable):
    """Collect actual exponents; never introduce independent power placeholders.

    Returns possible exponent collisions as obligations. Coefficients must be
    independent of `variable`; symbolic parameters are not split as free jets.
    The caller must declare variable>0 before using real-power independence.
    """
    terms = {}
    for term in sp.Add.make_args(sp.expand(expression)):
        powers = term.as_powers_dict()
        exponent = sp.simplify(powers.get(variable, 0))
        coefficient = sp.cancel(term / variable ** exponent)
        if coefficient.has(variable):
            raise ValueError('Expression is not a finite generalized power sum')
        terms[exponent] = sp.simplify(terms.get(exponent, 0) + coefficient)
    terms = {e: c for e, c in terms.items() if c != 0}
    collisions = []
    for left, right in itertools.combinations(terms, 2):
        difference = sp.factor(left - right)
        if difference.free_symbols:
            collisions.append(sp.Eq(difference, 0))
    return terms, collisions


# 4. Public analysis entrypoint. Integration certificates are an explicit stage.
def analyze(independent_variables, dependent_fields, equations, parameters,
            branch_conditions, data_case=None):
    started = time.perf_counter()
    space = JetSpace(independent_variables, dependent_fields)
    substitutions = branch_conditions.get('substitutions', {})
    specialized = tuple(sp.expand(sp.sympify(e).subs(substitutions, simultaneous=True)) for e in equations)
    order = space.order(specialized)
    xi, eta = arbitrary_generator(space)
    report = {
        'model_id': branch_conditions.get('model_id', 'user_system'),
        'coordinates': space.x, 'fields': space.u, 'parameters': parameters,
        'branch_conditions': branch_conditions, 'equations': specialized,
        'order': order, 'arbitrary_generator': {'xi': xi, 'eta': eta},
        'characteristic': characteristic(space, xi, eta),
        'classification_status': 'unresolved', 'generator_verification': 'not_run',
        'subalgebra_classification': 'not_run', 'data_case': data_case,
        'data_status': 'not_run', 'reduction_status': 'not_run',
    }
    shell = EvolutionShell(space, specialized)
    coefficients = prolongation_coefficients(space, xi, eta, order)
    actions = [point_action(space, e, xi, eta, order, coefficients=coefficients) for e in specialized]
    restricted = [shell.reduce(e) for e in actions]
    splits = [split_free_jets(space, e, shell) for e in restricted]
    report.update({
        'prolonged_equations': actions, 'on_shell_equations': restricted,
        'determining_splits': splits,
        'determining_equations': list(dict.fromkeys(e for split in splits for e in split['equations'])),
        'normal_form_rhs': shell.rhs, 'normal_form_divisors': shell.divisors,
        'differential_consequences': shell.rules_used,
        'elapsed_seconds': time.perf_counter() - started,
    })
    from classification import integrate_sve
    report['integration'] = integrate_sve(report)
    report['classification_status'] = report['integration']['status']
    if 'candidate_checks' in report['integration']:
        report['generator_verification'] = 'verified'
        report['subalgebra_classification'] = 'bracket_verified_optimal_system_not_proved'
    report['elapsed_seconds'] = time.perf_counter() - started
    return report


# 5. Independent candidate verification by the recursive prolongation formula.
def verify_generator(space, equations, xi, eta):
    equations = tuple(map(sp.sympify, equations))
    shell = EvolutionShell(space, equations)
    order = space.order(equations)
    coefficients = prolongation_coefficients(space, xi, eta, order, 'recursive')
    residuals = [sp.simplify(shell.reduce(point_action(space, e, xi, eta, order,
                 method='recursive', coefficients=coefficients))) for e in equations]
    return {'verified': all(e == 0 for e in residuals), 'residuals': residuals,
            'divisors': shell.divisors, 'method': 'recursive_point_prolongation'}


# 6. Algebra and graph geometry. No basis ordering or optimal-system guesswork.
def lie_bracket(coordinates, left, right):
    return tuple(sp.simplify(sum(left[j] * sp.diff(right[i], x)
                 - right[j] * sp.diff(left[i], x) for j, x in enumerate(coordinates)))
                 for i in range(len(coordinates)))


def algebra_structure(coordinates, basis):
    constants = sp.symbols(f'c0:{len(basis)}')
    structure = {}
    for i, left in enumerate(basis):
        for j, right in enumerate(basis):
            if j <= i:
                continue
            bracket = lie_bracket(coordinates, left, right)
            identities = [sum(constants[k] * basis[k][a] for k in range(len(basis))) - value
                          for a, value in enumerate(bracket)]
            equations = []
            for identity in identities:
                try:
                    equations.extend(sp.Poly(identity, *coordinates).coeffs())
                except sp.PolynomialError:
                    return {'status': 'unresolved_functional_basis_decomposition'}
            solutions = sp.solve(equations, constants, dict=True)
            if not solutions or any(c not in solutions[0] for c in constants):
                return {'status': 'unresolved_or_dependent_basis', 'pair': (i, j)}
            structure[f'{i},{j}'] = [solutions[0][c] for c in constants]
    epsilon = sp.Symbol('epsilon', real=True)
    matrices = []
    for i in range(len(basis)):
        matrix = sp.zeros(len(basis))
        for j in range(len(basis)):
            if i == j:
                continue
            values = structure[f'{min(i,j)},{max(i,j)}']
            for k,value in enumerate(values):
                matrix[k,j] = value if i < j else -value
        matrices.append(matrix)
    return {'status': 'verified_bracket_closure', 'structure_constants': structure,
            'adjoint_matrices': matrices,
            'adjoint_flows': [sp.exp(epsilon*matrix) for matrix in matrices],
            'adjoint_convention': 'ad_X(Y)=[X,Y]; Ad(exp(epsilon X))=exp(epsilon ad_X)',
            'one_dimensional_subalgebra_candidates': basis,
            'optimal_system_status': 'not_proved'}


def graph_check(space, equations, graph, xi=None, eta=None):
    substitution = {space.jet(a, index): (sp.diff(graph[a], *sum(
                    ([x] * count for x, count in zip(space.x, index)), [])) if any(index) else graph[a])
                    for a in range(len(space.u))
                    for index in multi_indices(len(space.x), space.order(equations))}
    residuals = [sp.simplify(e.xreplace(substitution)) for e in equations]
    Q = [] if xi is None else [sp.simplify(e.xreplace(substitution))
                               for e in characteristic(space, xi, eta)]
    return {'equation_residuals': residuals, 'characteristic_residuals': Q,
            'is_solution': all(e == 0 for e in residuals),
            'is_invariant': None if xi is None else all(e == 0 for e in Q)}


# 7. Serialization and a readable stage-by-stage CLI.
def json_ready(value):
    if isinstance(value, sp.MatrixBase):
        return [[json_ready(entry) for entry in row] for row in value.tolist()]
    if isinstance(value, sp.Basic):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(v) for v in value]
    return value


def print_derivation(report):
    stages = [('1. Specialized PDE and branch', report['equations']),
              ('2. Jet coordinates and total derivatives', [
                  f"Independent variables: {report['coordinates']}; fields: {report['fields']}",
                  f"PDE order: {report['order']}; field__j0_j1_... denotes the indicated partial derivative",
                  'D_i = partial_i + sum_(a,J) u^a_(J+e_i) partial_(u^a_J)',
                  f"Time-leading divisors: {report['normal_form_divisors']}"]),
              ('3. Arbitrary point generator and characteristic Q',
               [report['arbitrary_generator'], report['characteristic']]),
              ('4a. Prolonged equations before using the PDE', report['prolonged_equations']),
              ('4b. Differential consequences used', report['differential_consequences']),
              ('4c. Equation-manifold restriction', report['on_shell_equations']),
              ('5. Necessary determining equations', report['determining_equations'])]
    for title, expressions in stages:
        print('\n' + title)
        for expression in (expressions if isinstance(expressions, (tuple, list)) else [expressions]):
            print(' ', expression)
    print('\n6. General-solution status:', report['classification_status'])
    print(' Branch:', report['branch_conditions'])
    integration = report.get('integration', {})
    if 'general_solution' in integration:
        print(' General solution:', integration['general_solution'])
        print(' Free constants:', integration['free_constants'])
        print('\n7. Basis obtained by differentiating the general solution')
        for vector in integration['basis']:
            print(' ', vector)
        print('\n8. Algebra:', integration['algebra'])


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--branch', default='grass_generic')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--trace', choices=['full', 'summary'], default='full')
    args = parser.parse_args()
    from models import branch_model
    model = branch_model(args.branch)
    report = analyze(**model)
    if args.trace == 'full':
        print_derivation(report)
    else:
        print(args.branch, len(report['determining_equations']), 'determining equations')
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'derivation.json').write_text(json.dumps(json_ready(report), indent=2), encoding='utf-8')


if __name__ == '__main__':
    cli()
