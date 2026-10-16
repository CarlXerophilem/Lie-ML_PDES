"""Scientific regression tests with independent physical/negative controls."""
import importlib.util
from pathlib import Path

import pytest
import sympy as s

spec=importlib.util.spec_from_file_location('sve2d_extension',Path(__file__).parents[1]/'main.py')
calc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


@pytest.fixture(scope='module')
def reports():
    return dict(symmetry=calc.symmetry_checks(),radial=calc.radial_checks(),cubic=calc.cubic_checks())


@pytest.mark.parametrize('group',['symmetry','radial','cubic'])
def test_exact_certificates(reports,group):
    for name,values in reports[group]['exact_checks'].items():
        assert values and all(v==0 for v in values),name


@pytest.mark.parametrize('name,expected',[
    ('galilean_boost',-1),('rotation_without_velocity',-1),('noncubic_scaling_m2',-2)])
def test_candidate_negative_controls(reports,name,expected):
    assert reports['symmetry']['negative_controls'][name]==expected


def test_planar_restriction_recovers_cubic_1d():
    model=calc.jet_model(3)
    t,x,y=model['base']
    h,u,v,b=model['fields']
    J=model['jets']
    restrictions={v:0,**{j:0 for (f,z),j in J.items() if f==v or z==y}}
    expected=[J[h,t]+u*J[h,x]+h*J[u,x],
              J[u,t]+u*J[u,x]+model['g']*(J[h,x]+J[b,x]),0,
              J[b,t]+3*model['K']*u*u*J[u,x]]
    assert calc.zero_list(model['E'].subs(restrictions)-s.Matrix(expected))==[0]*4


def test_lake_at_rest_over_nonflat_static_bed():
    model=calc.jet_model(3)
    t,x,y=model['base']
    h,u,v,b=model['fields']
    J=model['jets']
    constraints={j:0 for j in J.values()}
    constraints.update({u:0,v:0,J[b,x]:2,J[b,y]:3,J[h,x]:-2,J[h,y]:-3})
    assert calc.zero_list(model['E'].subs(constraints))==[0]*4


def test_2d_geometry_is_not_1d(reports):
    assert reports['radial']['missing_geometry_witness']==1
    assert reports['cubic']['missing_factor_witness']==1


def test_pure_swirl_stationary_exact_family():
    # A=0, W=1, H=1/4, B=1/4, g=1: centrifugal and free-surface forces balance.
    model=calc.jet_model(3)
    t,x,y=model['base']
    h,u,v,b=model['fields']
    fields={h:(x*x+y*y)/4,u:-y,v:x,b:(x*x+y*y)/4}
    jets={j:s.diff(fields[f],z) for (f,z),j in model['jets'].items()}
    substituted=model['E'].subs(jets,simultaneous=True).subs(fields,simultaneous=True)
    assert calc.zero_list(substituted.subs(model['g'],1))==[0]*4
