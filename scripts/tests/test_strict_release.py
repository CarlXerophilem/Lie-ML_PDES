"""Independent-review regressions: evidence conditions and serial isolation."""
import hashlib
import sys
import pytest
import sympy as sp
from scripts.run_strict_lie import model
from symm.LieSymm.strict import input_fingerprint, liepde_script


def receipt():
    definition=model('P:general')
    row='{{},{xi_t=c_1,xi_s=c_2,eta_phi=0},{c_1,c_2,m},{m-1}}'
    text=('STRICT_CRACK_BRANCH_BEGIN$\n'+row+'$\nSTRICT_CRACK_BRANCH_END$\n'
          'LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_s=c_2,eta_phi=0},{c_1,c_2,m}}}$\nLIESYMM_END$')
    return definition,{'input_sha256':input_fingerprint(**definition),
                       'cas':{'input_sha256':hashlib.sha256(liepde_script(**definition).encode()).hexdigest(),
                              'status':'returned-solved','stdout':text}}


def test_replay_rejects_different_full_mathematical_input():
    from scripts.revalidate_strict_receipts import revalidate_receipt
    definition,original=receipt()
    definition['branch_conditions']['guards'].append('m>1')
    with pytest.raises(ValueError,match='fingerprint'):
        revalidate_receipt(definition,original)


def test_traveling_supplement_inherits_terminal_conditions():
    from scripts.strict_traveling_from_cas import traveling_chains_from_receipt
    definition,original=receipt()
    rows=traveling_chains_from_receipt(definition,original)
    chain=rows[0]['reduction']['chains'][0]
    assert any(g.get('origin')=='CRACK_terminal_branch' and g['status']=='conditional'
               for g in chain['guard_checks'])
    assert rows[0]['input_sha256']==original['input_sha256']


def test_scalar_source_selection_retains_branch_conditions():
    from scripts.strict_scalar_source_chains import select_source_branch
    definition,original=receipt()
    report,index,branch=select_source_branch(definition,original)
    assert index==0
    assert branch['assignments']
    assert any(g.get('origin')=='CRACK_terminal_branch'
               for g in report['independent_checks'][index]['guard_checks'])


def test_serial_runner_stops_after_failed_cleanup(monkeypatch,tmp_path):
    from scripts import run_strict_lie as runner
    calls=[]
    monkeypatch.setattr(sys,'argv',['runner','--out',str(tmp_path)])
    monkeypatch.setattr(runner,'cases',lambda:['P:1','P:3'])
    monkeypatch.setattr(runner,'cleanup_linux',lambda p:dict(status='cleanup-failed'))
    def run(*a,**k):calls.append(a);return dict(status='timeout')
    monkeypatch.setattr(runner,'run_reduce',run)
    with pytest.raises(RuntimeError,match='cleanup'):
        runner.main()
    assert len(calls)==1
    assert (tmp_path/'P--1-worker-60.json').exists()


def test_remote_campaign_keeps_marker_and_stops_after_failed_cleanup(monkeypatch,tmp_path):
    from scripts import run_strict_remote_campaign as runner
    (tmp_path/'baseline.exit').write_text('124')
    (tmp_path/'baseline.resources').write_text('Elapsed (wall clock) time (h:mm:ss or m:ss): 0:01\nMaximum resident set size (kbytes): 1\n')
    for name in ['red','stdout','stderr']:(tmp_path/('baseline.'+name)).write_text('')
    package=tmp_path/'runtime/usr/share/reduce/packages/crack';package.mkdir(parents=True)
    for name in ['liepde','applysym']:(package/(name+'.tst')).write_text('')
    inputs=tmp_path/'inputs';inputs.mkdir()
    for name in ['direct-classify','fixed-positive','direct-generic']:(inputs/(name+'.red')).write_text('')
    monkeypatch.setattr(sys,'argv',['runner','--out',str(tmp_path)])
    monkeypatch.setattr(runner,'cas_command',lambda *a,**k:['fixture'])
    monkeypatch.setattr(runner,'cleanup_linux',lambda p:dict(status='cleanup-failed'))
    calls=[]
    def run(*a,**k):calls.append(a);return dict(status='unparsed',stdout='',stderr='',elapsed_seconds=.1)
    monkeypatch.setattr(runner,'run_reduce',run)
    with pytest.raises(RuntimeError,match='cleanup'):
        runner.main()
    assert len(calls)==1
    assert (tmp_path/'campaign/official-liepde.running.json').exists()
    assert (tmp_path/'campaign/official-liepde.json').exists()


def test_direct_crack_family_preserves_assignment_denominators(monkeypatch):
    from symm.LieSymm import strict
    definition=model('E1:grass_generic')
    row='{{},{xi_t=c_1,xi_x=c_2,eta_h=0,eta_u=0,eta_b=c_3/(m-2)},{c_1,c_2,c_3},{}}'
    stdout=('STRICT_CRACK_BRANCH_BEGIN$\n'+row+'$\nSTRICT_CRACK_BRANCH_END$\n'
            'LIESYMM_RESULT_BEGIN$\n{'+row+'}$\nLIESYMM_END$')
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=stdout))
    report=strict.analyze_strict(**definition,cas_command=['fixture'],cas_mode='crack')
    checks=report['independent_checks'][0]
    assert checks['verified']
    guards=[g for g in checks['guard_checks'] if g.get('origin')=='CAS_assignment_denominator']
    assert guards and any(g['condition'].subs({definition['parameters'][-1]:2})==sp.false for g in guards)
    chain=strict.reduce_from_analysis(report)['chains'][0]
    assert any(g.get('origin')=='CAS_assignment_denominator' for g in chain['guard_checks'])
