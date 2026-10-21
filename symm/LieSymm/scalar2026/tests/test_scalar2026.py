"""Independent controls for scalar packaging, domains and solution claims."""
import subprocess
import sys

import pytest
import sympy as sp

from symm.LieSymm.scalar2026 import (
    backend, derive_reduction, printed_pde, exact_solution_checks,
    traveling_quadrature, compute_ode_series, source_audit,
)
from symm.LieSymm.scalar2026.demo import inventory, run


def test_source_and_no_main_pollution():
    script = ('import sys,types; marker=types.ModuleType("main"); sys.modules["main"]=marker; '
              'from symm.LieSymm.scalar2026 import backend; b=backend(); '
              'assert sys.modules["main"] is marker; '
              'assert b.__name__=="symm.LieSymm.scalar2026._historical"')
    subprocess.run([sys.executable,'-c',script],check=True,timeout=30)


def test_direct_original_pde_controls():
    assert exact_solution_checks()['passed']
    t,s=sp.symbols('t s',positive=True)
    with pytest.raises(ValueError,match='phi_s=0'):
        printed_pde(t,t,s)


def test_nine_cases_keep_non_odes_separate():
    rows=inventory()
    assert [r['case'] for r in rows]==[f'3.{i}' for i in range(1,10)]
    assert derive_reduction('3.2')['status']=='undefined'
    assert derive_reduction('3.3')['status']=='no_invariant_graph'
    assert derive_reduction('3.7')['residual']==0
    assert derive_reduction('3.8')['gradient']==1
    assert sum(bool(r['numerical_exponents']) for r in rows)==5


@pytest.mark.parametrize('alpha3',[0,1])
@pytest.mark.parametrize('exponent',[1,sp.Rational(3,2),2,3,4])
def test_exact_quadrature_and_original_jet_residual(exponent,alpha3):
    q=traveling_quadrature(exponent=exponent,alpha3=alpha3)
    assert q['passed']
    b=backend();r=q['parameter'];I=q['I0'];B=q['B']
    curvature=I/B
    third=sp.diff(curvature,r)*curvature
    case='3.6' if alpha3==0 else '3.9'
    residual=derive_reduction(case,exponent=exponent)['residual']
    residual=residual.subs({b.g:1,b.kappa:sp.Rational(1,30),b.P:r,b.C:curvature,b.H:third},simultaneous=True)
    assert sp.simplify(residual)==0


def test_identity_and_singular_strata_not_divided():
    with pytest.raises(ValueError,match='identity'):
        traveling_quadrature(alpha=0)
    assert compute_ode_series('3.2')['status']=='undefined_chart'
    assert compute_ode_series('3.1')['status']=='outside_positive_chart'
    assert compute_ode_series('3.5',exponent=2)['status']=='incompatible_parameter'
    # The source power profile has zero X4 leading coefficient; use exact
    # rational amplitude A=3 by choosing g=1/2,kappa=1/12.
    result=compute_ode_series('3.4',initial_jet=(3,1,-sp.Rational(2,3)),
                              g_value=sp.Rational(1,2),kappa_value=sp.Rational(1,12))
    assert result['status']=='normal_form_singular'


def test_source_discrepancy_and_quadratic_germ():
    witnesses=source_audit()
    assert witnesses['eq24']['original_residual_at_zero']==sp.Rational(2367,5000)
    assert all(v['audit_verified'] for k,v in witnesses.items() if k!='sample')
    germ=compute_ode_series('3.8',g_value=1,kappa_value=sp.Rational(1,30))
    assert germ['verification']['passed']
    assert germ['coefficients'][3:]==[0,0,0,0]


def test_output_is_new_and_outside_library(tmp_path):
    with pytest.raises(FileExistsError):
        run(tmp_path)
    from pathlib import Path
    with pytest.raises(ValueError,match='outside'):
        run(Path(__file__).parents[1]/'generated-output')
