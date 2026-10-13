"""Integration check of the manuscript's bound-data/first-integral figures."""
import hashlib
import json
from pathlib import Path
import shutil

import numpy as np
import pytest

import main as j


def test_plot_campaign_checks_integrals_and_refuses_changed_reference(tmp_path):
    source = Path(j.__file__).parent/'results'/'numerical'
    numerical = tmp_path/'numerical'
    numerical.mkdir()
    for name in ('numerics.json','3-4-m3.csv','3-6-m3.csv','3-9-m3.csv'):
        shutil.copy2(source/name,numerical/name)
    result = j.write_manuscript_plots(tmp_path)
    assert result['status'] == 'passed'
    assert len(result['files']) == 4
    for name,expected in result['figure_sha256'].items():
        assert hashlib.sha256((tmp_path/'presentation'/name).read_bytes()).hexdigest()==expected
    # Independent numerical formulas for I, without the symbolic density helper.
    for case,constant in [('3.4',79/200),('3.6',-71/200),('3.9',-79/200)]:
        data = np.genfromtxt(numerical/f"{case.replace('.','-')}-m3.csv",names=True,delimiter=',')
        z,f,p,c = (data[x] for x in ('z','F_rkf45','P_rkf45','C_rkf45'))
        if case=='3.4':
            integral=c*(-z**3*p+z/p**2+.1*z*(f-z*p)**2/p)
        else:
            velocity=p+(1 if case=='3.9' else 0)
            integral=c*(p-1/p**2-.1*velocity**2/p)
        row=result['cases'][case]
        assert row['integral_constant']==pytest.approx(constant,abs=1e-15)
        assert np.max(np.abs(integral-constant))<1e-12
        assert row['max_scaled_drift']<1e-12
        assert row['max_two_state_disagreement']<1e-12
    assert json.loads((tmp_path/'presentation'/'plots.json').read_text())['status']=='passed'
    # A stale CSV must fail before generating any figure in a fresh destination.
    stale=tmp_path/'stale';shutil.copytree(numerical,stale/'numerical')
    csv_path=stale/'numerical'/'3-4-m3.csv'
    csv_path.write_bytes(csv_path.read_bytes()+b'\n')
    with pytest.raises(ValueError,match='reference_metadata_mismatch'):
        j.write_manuscript_plots(stale)
    assert not list((stale/'presentation').glob('*.pdf'))
    assert not (stale/'presentation'/'plots.json').exists()
