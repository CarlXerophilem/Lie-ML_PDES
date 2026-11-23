"""Perturbation controls distinguish computation from replayed success labels."""
import json
from pathlib import Path

import numpy as np
import pytest
import sympy as sp

import main as j


def test_live_graph_and_integral_identities_cover_nine_cases():
    checks=j.verify_reduction_pullbacks()
    assert checks['passed']
    assert len(checks['direct_graph_checks'])==25
    assert {row['case'] for row in checks['direct_graph_checks']}=={f'3.{i}' for i in range(1,10)}
    x4=next(r for r in checks['direct_graph_checks'] if r['case']=='3.4')
    assert x4['pullback_multiplier']==sp.Symbol('T',positive=True)**-2
    assert set(checks['first_integral_checks'])=={'3.4','3.6','3.9'}


def test_changed_master_is_detected_by_independent_pullback(monkeypatch):
    original=j.master
    monkeypatch.setattr(j,'master',lambda exponent=j.m:original(exponent)+j.q)
    checks=j.verify_reduction_pullbacks()
    assert not checks['passed']
    assert any(not row['passed'] for row in checks['direct_graph_checks'] if row['case']=='3.4')
    # The previously printed literal zero for this counterexample must change.
    wrong_graph=j.translated_ansatz_witnesses()['3.8_wrong_graph_counterexample']
    assert wrong_graph['original_PDE']==1+j.s**2/2


def test_table_agreement_is_computed_and_detects_altered_action(monkeypatch):
    original=j.adjoint
    def broken(actor,target,epsilon,stratum='m3'):
        result=dict(original(actor,target,epsilon,stratum))
        if actor=='X1' and target=='X4' and stratum=='m3':
            result['X1']=epsilon
        return result
    monkeypatch.setattr(j,'adjoint',broken)
    table=j.build_algebra_report()['checks']['table_2']
    assert table['status']=='disagrees'
    assert not table['comparisons']['Ad(X1)X4']['passed']


def test_numerical_and_series_solutions_respond_to_new_initial_data():
    # A new IVP, absent from the saved campaign, has an exact quadratic control.
    initial=(3.,2.,.4)
    solve=j.solve_ivp_rkf45(lambda t,y:np.array([y[1],y[2],0.]),
                          (0.,.3),initial,t_eval=np.array([0.,.3]))
    assert solve.status=='completed' and solve.nfev>0
    assert np.allclose(solve.y[:,-1],[3.618,2.12,.4],rtol=0,atol=2e-14)
    row=j.compute_ode_series('3.8',initial_jet=(3,2,sp.Rational(2,5)))
    h=sp.Symbol('h',real=True)
    assert sp.expand(row['polynomial']-(3+2*h+h**2/5))==0


def test_removed_viewer_cli_and_stale_report_cannot_claim_fresh_work(tmp_path):
    with pytest.raises(SystemExit):j.parse_args(['--stage','html'])
    with pytest.raises(SystemExit):j.parse_args(['--html-out','out.html'])
    source=Path(j.__file__).read_text(encoding='utf-8')
    assert '<!doctype html>' not in source.lower()
    assert not hasattr(j,'write_solutions_html')
    (tmp_path/'evidence.json').write_text(json.dumps({'run':{'symbolic_passed':True}}))
    (tmp_path/'code_manifest.json').write_text(json.dumps({'main.py':'stale'}))
    with pytest.raises(SystemExit,match='different or unrecorded code'):
        j.main(['--stage','report','--out',str(tmp_path)])
