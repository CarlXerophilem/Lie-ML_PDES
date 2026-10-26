import sys

import pytest
import sympy as sp

from symm.LieSymm.strict import analyze_strict, reduce_from_analysis, run_reduce, liepde_script
from symm.LieSymm.core import JetSpace


def heat():
    t, x, u = sp.symbols('t x u')
    j = JetSpace((t, x), (u,))
    return dict(independent_variables=j.x, dependent_fields=j.u,
                equations=(j.jet(0, (1, 0))-j.jet(0, (0, 2)),),
                parameters=(), branch_conditions={'model_id': 'forged_known_model'})


def test_unrestricted_and_no_registry(monkeypatch):
    from symm.LieSymm._loader import load_module
    def forbidden(*args, **kwargs):
        raise AssertionError('registry integration called')
    monkeypatch.setattr(load_module('classification'), 'integrate_sve', forbidden)
    report = analyze_strict(**heat())
    assert report['classification_status'] != 'complete'
    assert report['determining_equations']
    assert report['remaining_equations']
    assert report['arbitrary_generator']['xi'][0].args == (*report['coordinates'], *report['fields'])
    assert report['prolongation_agreement']
    assert report['cas']['status'] == 'not_run'
    assert reduce_from_analysis(report)['status'] == 'blocked'


def test_script_uses_general_point_mode():
    script = liepde_script(**heat())
    assert '{"point"}' in script
    assert 'df(u,t)' in script
    assert 'df(u,x,2)' in script
    assert 'xi_' not in script


def test_runtime_never_certifies_exit_zero():
    r = run_reduce([sys.executable, '-c', 'print("LIESYMM_END")'], '', timeout=60)
    assert r['returncode'] == 0
    assert r['status'] == 'unparsed'
    assert not r['verified']


def test_missing_runtime_and_bad_budget():
    assert run_reduce(['no-such-reduce-runtime'], '', timeout=60)['status'] == 'backend-unavailable'
    with pytest.raises(ValueError):
        run_reduce([sys.executable], '', timeout=0)


def test_prepopulated_profile_not_accepted():
    with pytest.raises(TypeError):
        reduce_from_analysis({}, profile=['made-up'])


def test_parse_partial_and_reject_injection():
    from symm.LieSymm.strict import parse_liepde_output
    text = 'LIESYMM_RESULT_BEGIN$\n{{{df(c_4,t)}, {xi_t=c_1,xi_x=0,eta_u=c_4},{c_1,c_4}}}$\nLIESYMM_END$'
    parsed = parse_liepde_output(text)
    assert parsed['branches'][0]['remaining']
    assert not parsed['solved']
    with pytest.raises(ValueError):
        parse_liepde_output(text.replace('c_1,xi_x', '__import__("os"),xi_x'))
    with pytest.raises(ValueError):
        parse_liepde_output('LIESYMM_END')


def test_parse_finite_algebra():
    from symm.LieSymm.strict import parse_liepde_output
    text = 'LIESYMM_RESULT_BEGIN$\n{{{}, {xi_t=c_1,xi_x=c_2,eta_u=0},{c_1,c_2}}}$\nLIESYMM_END$'
    result = parse_liepde_output(text)
    assert result['solved']
    assert len(result['branches']) == 1


def test_diffusion_names_and_mixed_order_shell():
    from symm.LieSymm.models import branch_model
    from symm.LieSymm.strict import StrictMixedShell
    model = branch_model('slope_attachment_cubic')
    script = liepde_script(**model)
    assert 'lsvar' in script  # gravity g and diffusion G must stay distinct
    j = JetSpace(model['independent_variables'], model['dependent_fields'])
    shell = StrictMixedShell(j, model['equations'])
    assert j.jet(2, (1, 1)) not in shell.rules
    assert j.jet(0, (1, 1)) in shell.rules


def test_parameters_and_nonzero_conditions_reach_cas():
    from symm.LieSymm.models import branch_model
    script = liepde_script(**branch_model('grass_generic'))
    assert '{"point"},{g,k,m},{g,k,(-3+m)}' in script


def test_exceptional_parameter_is_applied_before_verification(monkeypatch):
    import symm.LieSymm.strict as strict
    model = heat()
    t,x = model['independent_variables']; u, = model['dependent_fields']
    m = sp.Symbol('m')
    j = JetSpace((t,x),(u,))
    model.update(parameters=(m,), equations=(j.jet(0,(1,0))-m*j.jet(0,(0,1)),))
    output = 'LIESYMM_RESULT_BEGIN$\n{{{},{m=0,xi_t=0,xi_x=0,eta_u=c_1*x},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=output))
    report = strict.analyze_strict(**model,cas_command=['fixture'])
    assert report['returned_family_verified']
    assert report['independent_checks'][0]['parameter_substitutions'] == {m:0}
    model['branch_conditions']['guards'] = ['m!=0']
    rejected = strict.analyze_strict(**model,cas_command=['fixture'])
    assert not rejected['returned_family_verified']
    assert rejected['independent_checks'][0]['status'] == 'excluded-by-input-guards'


def test_mixed_shell_invariant_under_equation_row_permutation():
    from symm.LieSymm.strict import StrictMixedShell
    t,x,u,v = sp.symbols('t x u v')
    j = JetSpace((t,x),(u,v))
    equations = (j.jet(0,(1,0))-j.jet(1,(0,2)),j.jet(1,(1,0))-j.jet(0,(0,1)))
    assert StrictMixedShell(j,equations).rules == StrictMixedShell(j,equations[::-1]).rules


def test_guard_substitution_precedes_symbol_assumptions():
    from symm.LieSymm.strict import _branch_guards
    g=sp.Symbol('g',positive=True)
    assert _branch_guards(['g>0'],(g,),{g:0})[0]['status'] == 'false'


def test_reserved_symbols_are_escaped():
    from symm.LieSymm.strict import _reduce_names
    df,sine=sp.symbols('df sin')
    names=_reduce_names((df,sine))
    assert names[df] != 'df' and names[sine] != 'sin'


def test_duplicate_assignment_rejected():
    from symm.LieSymm.strict import parse_liepde_output
    with pytest.raises(ValueError):
        parse_liepde_output('LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=0,xi_t=1},{}}}$\nLIESYMM_END$')


def test_characteristics_derived_from_returned_translation(monkeypatch):
    import symm.LieSymm.strict as strict
    output='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=output))
    report=strict.analyze_strict(**heat(),cas_command=['fixture'])
    result=strict.reduce_from_analysis(report)
    assert result['status'] == 'partial'
    assert result['chains'][0]['projection_rank'] == 1
    assert result['chains'][0]['Q_zero']
    assert result['chains'][0]['category'] == 'implicit_ODE_DAE'
    assert result['chains'][0]['reconstruction_identity_verified']
    assert strict.reduce_from_analysis(report,data_case={'unparsed':'data'})['status'] == 'blocked'
    nonlinear=heat()
    t,x=nonlinear['independent_variables'];u,=nonlinear['dependent_fields']
    j=JetSpace((t,x),(u,))
    nonlinear['equations']=(j.jet(0,(1,0))-u*j.jet(0,(0,1)),)
    nonlinear_report=strict.analyze_strict(**nonlinear,cas_command=['fixture'])
    assert strict.reduce_from_analysis(nonlinear_report)['chains'][0]['reconstruction_identity_verified']


def test_reduction_eliminates_original_coordinate_coefficients(monkeypatch):
    import symm.LieSymm.strict as strict
    definition=heat();t,x=definition['independent_variables'];u,=definition['dependent_fields']
    j=JetSpace((t,x),(u,))
    definition['equations']=(j.jet(0,(1,0))-t*u,)
    output='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=0,xi_x=c_1,eta_u=0},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=output))
    report=strict.analyze_strict(**definition,cas_command=['fixture'])
    chain=strict.reduce_from_analysis(report)['chains'][0]
    assert not any(e.has(t,x) for e in chain['reduced_equations'])
    assert chain['reconstruction_identity_verified']


def test_positive_radial_power_identity_without_forced_global_powers():
    from symm.LieSymm.strict import _chart_simplify
    u,v,n=sp.symbols('u v n',real=True)
    radius=u*u+v*v
    expression=u*u*radius**(n/2)+v*v*radius**(n/2)-radius**(n/2+1)
    assert _chart_simplify(expression,[radius]) == 0


def test_crack_branch_inequalities_are_retained():
    from symm.LieSymm.strict import parse_crack_output
    output='STRICT_CRACK_BRANCH_BEGIN$\n{{},{xi_t=c_1},{c_1,m},{m-1}}$\nSTRICT_CRACK_BRANCH_END$'
    result=parse_crack_output(output)
    assert result['branches'][0]['nonzero_conditions'] == [sp.Symbol('m')-1]
