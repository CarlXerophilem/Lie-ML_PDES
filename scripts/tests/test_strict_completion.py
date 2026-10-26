"""Acceptance regressions for portable strict evidence."""
import sys
import sympy as sp
from symm.LieSymm import strict
from symm.LieSymm.core import JetSpace
from scripts import run_strict_lie as runner


def test_linux_launcher_never_uses_wsl(tmp_path):
    command=runner.cas_command(tmp_path,60,tmp_path/'process.pid',platform='linux',memory_bytes=8_000_000_000)
    assert 'wsl' not in command
    assert str(tmp_path/'cas/runtime/usr/lib/reduce/cslbuild/csl/reduce') in command
    assert '--as=8000000000' in command


def test_full_input_hash_includes_guards():
    d=runner.model('P:3');a=strict.input_fingerprint(**d)
    d['branch_conditions']['guards'].append('phi_t>1')
    assert strict.input_fingerprint(**d)!=a


def test_fixed_and_jet_guards_have_declared_values():
    d=runner.model('E2:slope_only_n2_f_nonzero')
    assert d['branch_conditions']['fixed_parameters']['n']==2
    j=JetSpace(('t','x'),('u',))
    env=strict.guard_environment(j,(),{'fixed_parameters':{'f':0}})
    rows=strict._branch_guards(['u_t>0','f=0'],env,{})
    assert [r['status'] for r in rows]==['conditional','true']


def test_branches_match_by_family_not_output_position():
    x,m,c,d=sp.symbols('x m c d');xi=sp.Symbol('xi_x')
    a={'remaining':[],'assignments':{xi:c*x},'free':[c,m]}
    b={'remaining':[],'assignments':{xi:c*x,m:1},'free':[c]}
    traces=[{**b,'nonzero_conditions':[]},{'remaining':[],'assignments':{xi:2*d*x},'free':[d,m],'nonzero_conditions':[m-1]}]
    r=strict.match_branch_conditions([a,b],traces,(xi,),(m,),(x,))
    assert r['matched'] and [v['trace_index'] for v in r['matches']]==[1,0]
    assert r['matches'][0]['nonzero_conditions']==[m-1]
    assert r['parameter_coverage']=='unverified'


def test_ambiguous_branch_correspondence_is_blocked():
    x,c=sp.symbols('x c');xi=sp.Symbol('xi_x')
    a={'remaining':[],'assignments':{xi:c*x},'free':[c]}
    assert not strict.match_branch_conditions([a],[{**a,'nonzero_conditions':[]},{**a,'nonzero_conditions':[]}],(xi,),(),(x,))['matched']


def test_small_remaining_budget_preserves_timeout_receipt(tmp_path):
    r=strict.run_reduce([sys.executable,'-c','import time; time.sleep(2)'],'',timeout=.15,artifact_prefix=tmp_path/'limited')
    assert r['status']=='timeout'
    assert (tmp_path/'limited.stdout.log').exists()


def test_backend_timeout_exit_is_not_generic_crash():
    r=strict.run_reduce([sys.executable,'-c','raise SystemExit(124)'],'')
    assert r['status']=='timeout'


def test_invalid_guard_does_not_become_strict_acceptance(monkeypatch):
    t,x,u=sp.symbols('t x u');j=JetSpace((t,x),(u,))
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    r=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0)),),(),{'guards':['missing>0']},cas_command=['fixture'])
    assert r['guard_status']=='unparsed'
    assert r['classification_status']=='incomplete'


def test_direct_crack_preserves_arbitrary_dependencies():
    t,x,u=sp.symbols('t x u');j=JetSpace((t,x),(u,))
    report=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0)),),(),{})
    code=strict.crack_script(report)
    assert 'depend xi_t,t,x,u$' in code
    assert 'strictresult:=crack(' in code
    assert '{xi_t,xi_x,eta_u}' in code


def test_reduction_keeps_fixed_and_terminal_guards(monkeypatch):
    t,x,u,m=sp.symbols('t x u m');j=JetSpace((t,x),(u,))
    text=('STRICT_CRACK_BRANCH_BEGIN$\n{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1,m},{m-1}}$\n'
          'STRICT_CRACK_BRANCH_END$\nLIESYMM_RESULT_BEGIN$\n'
          '{{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1,m}}}$\nLIESYMM_END$')
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    report=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0)),),(m,),
                                {'guards':['f=0'],'fixed_parameters':{'f':0}},cas_command=['fixture'])
    chain=strict.reduce_from_analysis(report)['chains'][0]
    assert all(g['status']!='unparsed' for g in chain['guard_checks'])
    assert any(g.get('origin')=='CRACK_terminal_branch' and g['condition']==sp.Ne(m,1)
               for g in chain['guard_checks'])


def test_reduction_does_not_accept_unparsed_chart(monkeypatch):
    t,x,u=sp.symbols('t x u');j=JetSpace((t,x),(u,))
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    report=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0)),),(),{'guards':['missing>0']},cas_command=['fixture'])
    assert strict.reduce_from_analysis(report)['chains'][0]['category']=='unparsed_chart_guards'


def test_power_translation_pullback_uses_declared_chart(monkeypatch):
    d=runner.model('E1:slope_attachment_generic')
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_x=0,eta_h=0,eta_u=0,eta_b=0},{c_1,m}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    r=strict.analyze_strict(**d,cas_command=['fixture'])
    chain=strict.reduce_from_analysis(r)['chains'][0]
    assert chain['reconstruction_identity_verified']
    assert chain['reconstruction_residuals']==[0,0,0]


def test_positive_chart_simplification_preserves_derivative_defect():
    x=sp.Symbol('x');f=sp.Function('F')(x)
    assert strict._chart_simplify(sp.diff(f,x),[f])==sp.diff(f,x)


def test_direct_crack_terminal_format_keeps_inequations():
    from scripts.run_strict_remote_campaign import parse_terminal_result
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1},{c_1,m},{m-1}}}$\nLIESYMM_END$'
    result=parse_terminal_result('direct-generic',text)
    assert result['solved']
    assert result['branches'][0]['nonzero_conditions']==[sp.Symbol('m')-1]
    assert result['inequalities']=='returned_by_crack'
