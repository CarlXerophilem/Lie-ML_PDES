import sympy as sp

import main as j
from main import derive_reduction, build_reduction_report


def test_all_rows_have_contract_keys_and_types():
    keys = {'id', 'status', 'coordinate', 'ansatz', 'residual', 'leading',
            'rhs', 'velocity', 'gradient', 'ode_order', 'steps', 'guards',
            'source_equations'}
    for case in [f'3.{n}' for n in range(1, 10)] + ['table3-mixed']:
        row = derive_reduction(case)
        assert set(row) == keys
        assert isinstance(row['steps'], list)


def test_time_and_space_translation_are_not_interchangeable():
    assert derive_reduction('3.1')['status'] == 'identity'
    assert derive_reduction('3.2')['status'] == 'undefined'
    assert derive_reduction('3.3')['status'] == 'no_invariant_graph'
    linear = derive_reduction('3.8', alpha=1)
    assert linear['coordinate'] == j.t
    assert sp.simplify(linear['residual'] - j.H) == 0
    assert sp.simplify(linear['leading'] - 1) == 0
    assert sp.simplify(linear['rhs']) == 0


def test_traveling_pullback_and_parameters():
    row = derive_reduction('3.9', exponent=3, alpha=-1, alpha3=1)
    assert next(step['expression'] for step in row['steps']
                if step['label'] == 'phi') == row['ansatz']
    assert sp.simplify(row['velocity'] - (1+j.P)) == 0
    assert sp.simplify(row['gradient'] - j.P) == 0
    assert sp.simplify(row['residual'].subs({j.C: 0, j.H: 0})) == 0
    assert sp.simplify(row['residual'].subs({j.g: 1, j.kappa: sp.Rational(1,30),
        j.z: 1, j.F: 2, j.P: sp.Rational(1,2), j.C: sp.Rational(1,10),
        j.H: 0})) != 0


def test_scaling_rows_are_regular_at_reference_jet():
    for case in ('3.4', '3.5', 'table3-mixed'):
        row = derive_reduction(case)
        assert row['status'] == 'regular_ode'
        assert row['ode_order'] == 3
        assert sp.simplify(sp.diff(row['residual'], j.H)-row['leading']) == 0
        value = row['leading'].subs({j.g: 1, j.kappa: sp.Rational(1,30),
            j.z: 1, j.F: 2, j.P: sp.Rational(1,2), j.C: sp.Rational(1,10)})
        assert value != 0


def test_resonant_mixed_row_is_typed():
    row = derive_reduction('table3-mixed', mix_alpha=-1)
    assert row['coordinate'] == j.t
    assert row['status'] == 'regular_ode'
    assert 's' in str(row['ansatz'])


def test_scaling_invariants_and_endpoint_parameters():
    for case, A, B in [('3.4',1,-1),('3.5',0,2),
                       ('table3-mixed',sp.Rational(4,5),-sp.Rational(2,5))]:
        row = derive_reduction(case)
        T, S, U = j.t, -B*j.s, A*j.u
        assert sp.simplify(T*sp.diff(row['coordinate'],j.t)+
                           S*sp.diff(row['coordinate'],j.s)) == 0
        # Treat F as a function of z: Q=eta-tau*phi_t-xi*phi_s.
        profile = sp.Function('profile')(row['coordinate'])
        graph = row['ansatz'].subs(j.F, profile)
        Q = U.subs(j.u,graph)-T*sp.diff(graph,j.t)-S*sp.diff(graph,j.s)
        assert sp.simplify(Q) == 0
    assert derive_reduction('3.6',alpha=0)['status'] == 'identity'
    assert derive_reduction('3.9',alpha=0)['status'] == 'identity'
    assert sp.simplify(derive_reduction('table3-mixed',exponent=2,mix_alpha=0)['residual']-
                       derive_reduction('3.4',exponent=2)['residual']) == 0


def test_report_is_jsonable_and_has_nine_cases():
    import json
    report = build_reduction_report()
    assert len(report['cases']) == 9
    json.dumps(report)


def test_printed_cubic_power_law_is_exact_but_x4_singular():
    from main import cubic_power_law_audit
    audit = cubic_power_law_audit()
    condition = audit['condition_printed']
    assert sp.factor(audit['x4_residual']/condition).has(j.z)
    assert sp.simplify(audit['x4_leading']/condition -
                       j.z**sp.Rational(7,3)/(3*sp.Symbol('A',positive=True)**2)) == 0
    assert sp.simplify(audit['x5_residual']/condition) != 0


def test_traveling_integral_is_exact_and_linearizes():
    from main import traveling_first_integral
    for case, a3 in [('3.6',0), ('3.9',1)]:
        data = traveling_first_integral(3,-1,a3)
        assert sp.simplify(derive_reduction(case)['residual']-
                           data['dI']) == 0


def test_common_scaling_integral_is_exact_for_symbolic_exponent():
    from main import common_scaling_first_integral
    data = common_scaling_first_integral(j.m)
    assert sp.simplify(data['dI']-derive_reduction('3.4',exponent=j.m)['residual']) == 0


def test_wrong_38_graph_is_a_positive_branch_counterexample():
    from main import translated_ansatz_witnesses
    w = translated_ansatz_witnesses()['3.8_wrong_graph_counterexample']
    assert w['original_PDE'] == 0
    assert w['F_sss'] == 1
    assert w['phi_s'] > 0 or sp.ask(sp.Q.positive(w['phi_s']))


def test_printed_25_27_29_31_33_have_exact_rational_witnesses():
    from main import printed_equation_witnesses
    w = printed_equation_witnesses()
    for eq in ('eq24','eq25','eq28','eq29','eq33'):
        assert w[eq]['original_residual_at_zero'] != 0
    assert w['eq26']['correct_mu_equation_at_zero'] != 0
    assert w['eq27']['printed_Mprime_at_sample'] != w['eq27']['correct_Mprime_at_sample']
    assert w['eq30']['printed_Mprime_over_M_at_sample'] != w['eq30']['correct_Mprime_over_M_at_sample']
    assert w['eq31']['d_of_correct_integral_dP_at_sample'] != 0
    assert w['eq34']['original_residual_at_implied_jet'] != 0
    assert set(f'eq{i}' for i in range(24,35)) <= set(w)
    assert all(w[f'eq{i}']['status'] in {'verified','qualified','refuted_as_printed','unresolved'}
               for i in range(24,35))
