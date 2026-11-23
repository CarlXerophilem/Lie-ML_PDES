"""Regression checks for strict evidence and chart boundaries."""
import sys
import sympy as sp
from symm.LieSymm import strict
from symm.LieSymm.core import JetSpace
from scripts import project_workflow


def test_cross_drive_evidence_link_falls_back_to_uri(monkeypatch,tmp_path):
    def different_drives(*args):
        raise ValueError('path is on a different mount')
    monkeypatch.setattr(project_workflow.os.path,'relpath',different_drives)
    value=project_workflow._evidence_href('paper name.md#section',tmp_path,tmp_path/'out')
    assert value == (tmp_path/'paper name.md').as_uri()+'#section'


def test_supported_trigonometric_generator_is_verified(monkeypatch):
    t,x,u=sp.symbols('t x u');j=JetSpace((t,x),(u,))
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=0,xi_x=0,eta_u=c_1*sin(x)},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    report=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0)),),(),{},cas_command=['fixture'])
    assert report['returned_family_verified']


def test_rank_one_in_three_coordinates_is_not_an_ode(monkeypatch):
    t,x,y,u=sp.symbols('t x y u');j=JetSpace((t,x,y),(u,))
    text='LIESYMM_RESULT_BEGIN$\n{{{},{xi_t=c_1,xi_x=0,xi_y=0,eta_u=0},{c_1}}}$\nLIESYMM_END$'
    monkeypatch.setattr(strict,'run_reduce',lambda *a,**k:dict(status='unparsed',stdout=text))
    report=strict.analyze_strict(j.x,j.u,(j.jet(0,(1,0,0)),),(),{},cas_command=['fixture'])
    chain=strict.reduce_from_analysis(report)['chains'][0]
    assert chain['category'] == 'insufficient_projection_rank'
    assert chain['projection_rank'] == 1


def test_failed_process_keeps_raw_evidence(tmp_path):
    prefix=tmp_path/'failed'
    receipt=strict.run_reduce([sys.executable,'-c','print("raw witness"); raise SystemExit(2)'],
                              'input witness',artifact_prefix=prefix)
    assert receipt['status']=='error'
    assert (tmp_path/'failed.stdout.log').read_text().strip()=='raw witness'
    assert (tmp_path/'failed.input.red').read_text()=='input witness'


def test_custom_nonzero_coriolis_is_a_real_guard():
    from scripts.run_strict_lie import model
    definition=model('custom:f_nonzero')
    assert 'f!=0' in definition['branch_conditions']['guards']
