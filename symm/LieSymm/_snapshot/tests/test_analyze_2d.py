"""Independent mixed-order geometry and fail-closed certificate controls."""
import sympy as sp
import pytest
from main import JetSpace,multi_indices
from models_2d import branch_model_2d,BRANCHES_2D
from analyze_2d import MixedShell,split_free_jets
from classification_2d import integrate_sve_2d,review_gate


def test_j2_shell_keeps_bed_time_second_derivatives_free():
    model=branch_model_2d('slope_attachment_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    shell=MixedShell(J,model['equations'])
    assert len(shell.rules)==13
    all_jets={J.jet(a,index) for a in range(4) for index in multi_indices(3,2) if any(index)}
    assert len(all_jets-set(shell.rules))==23
    for index in ((2,0,0),(1,1,0),(1,0,1)):
        assert J.jet(3,index) not in shell.rules
    for equation in model['equations']:
        assert sp.simplify(shell.reduce(equation))==0
    for equation in model['equations'][:3]:
        for axis in range(3):
            assert sp.simplify(shell.reduce(J.D(equation,axis)))==0
    assert max(J.order((e,)) for e in shell.rules.values())<=2


def test_free_jet_split_includes_retained_mixed_time_jets():
    model=branch_model_2d('slope_attachment_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    shell=MixedShell(J,model['equations'])
    a,b=sp.symbols('a b')
    expression=a*J.jet(3,(1,1,0))+b*J.jet(3,(2,0,0))
    result=split_free_jets(J,expression,shell)
    assert set(result['equations'])=={a,b}


def test_unsupported_hydro_order_is_rejected():
    model=branch_model_2d('slope_attachment_cubic_f0')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    equations=list(model['equations'])
    equations[0]+=J.jet(0,(0,2,0))
    with pytest.raises(ValueError,match='Unsupported mixed orders'):
        MixedShell(J,equations)


def test_integration_cannot_relabel_changed_equation_or_guard():
    model=branch_model_2d('grass_cubic_f0')
    report={'model_id':model['branch_conditions']['model_id'],
            'coordinates':model['independent_variables'],'fields':model['dependent_fields'],
            'parameters':model['parameters'],'branch_conditions':model['branch_conditions'],
            'equations':(model['equations'][0]+1,*model['equations'][1:])}
    assert integrate_sve_2d(report)['status']=='unresolved'
    report['equations']=model['equations']
    report['branch_conditions']=dict(model['branch_conditions'],guards=['h<0'])
    assert integrate_sve_2d(report)['status']=='unresolved'


def test_review_cannot_accept_a_bare_flag(tmp_path):
    path=tmp_path/'review.json'
    path.write_text('{"all_checks_passed":true}')
    assert not review_gate(path,root=tmp_path)['passed']


@pytest.mark.parametrize('name',tuple(BRANCHES_2D))
def test_terminal_constraints_have_expected_dimension(name):
    from research_first_order_2d import general_solution as first
    from research_slope_2d import general_solution as slope
    cell=BRANCHES_2D[name]
    solved=(slope if cell['G'] else first)(name)
    dim=len(solved['free_constants'])
    if cell['G']:
        scaling=(not cell['K'] or cell['m']==3) and (cell['coriolis']=='f0' or cell['n']==2)
        expected=5+int(scaling)
    else:
        expected=5+int(cell['coriolis']=='f0')+int(not cell['K'] or cell['m']==3)
    assert dim==expected
