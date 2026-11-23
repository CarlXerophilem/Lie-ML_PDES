import sympy as sp
import pytest
from main import (JetSpace, EvolutionShell, arbitrary_generator, characteristic,
                  prolongation_coefficients, split_free_jets, generalized_power_terms,
                  analyze, verify_generator)
from models import branch_model, BRANCHES, m, n, K


def test_characteristic_and_recursive_prolongation_agree_for_arbitrary_coefficients():
    t,x,w = sp.symbols('t x w')
    J = JetSpace((t,x),(w,))
    xi,eta = arbitrary_generator(J)
    first = prolongation_coefficients(J,xi,eta,2,'characteristic')
    second = prolongation_coefficients(J,xi,eta,2,'recursive')
    assert all(sp.expand(first[k]-second[k]) == 0 for k in first)


def test_jet_limit_is_not_silent_truncation():
    t,x,w = sp.symbols('t x w')
    J = JetSpace((t,x),(w,),1)
    with pytest.raises(ValueError,match='Jet order exhausted'):
        J.D(J.jet(0,(0,1)),1)


def test_mixed_order_shell_includes_differential_consequences():
    model = branch_model('slope_attachment_cubic')
    J = JetSpace(model['independent_variables'],model['dependent_fields'])
    shell = EvolutionShell(J,model['equations'])
    for equation in model['equations']:
        assert sp.simplify(shell.reduce(equation)) == 0
        for axis in (0,1):
            assert sp.simplify(shell.reduce(J.D(equation,axis))) == 0
    assert any('__1_1' in key for key in shell.rules_used)


def test_parameters_are_not_split_as_free_jet_coordinates():
    t,x,w,a,b = sp.symbols('t x w a b')
    J = JetSpace((t,x),(w,))
    shell = EvolutionShell(J,(J.jet(0,(1,0)),))
    split = split_free_jets(J,(m*a+b)*J.jet(0,(0,1)),shell)
    assert split['equations'] == [m*a+b]
    assert sp.solve(split['equations'],b) == {b:-a*m}


def test_real_power_relations_and_collisions_are_preserved():
    p = sp.Symbol('p',positive=True)
    terms,collisions = generalized_power_terms(p**m+p**3,p)
    assert set(terms) == {m,sp.Integer(3)}
    assert any(sp.solve(c,m) == [3] for c in collisions)
    assert generalized_power_terms(p**m-p*p**(m-1),p)[0] == {}


@pytest.mark.parametrize('branch,dimension',[
    ('grass_generic',4),('grass_cubic',5),('zero_transport',5),
    ('slope_attachment_generic',3),('slope_attachment_cubic',4),
    ('slope_source_generic',3),('slope_source_cubic',4),('slope_only',4)])
def test_every_declared_cell_solves_all_unrestricted_determining_equations(branch,dimension):
    report = analyze(**branch_model(branch))
    integrated = report['integration']
    assert integrated['status'] in {'necessity_integrated_pending_review','proved_for_declared_regular_chart'}
    assert integrated['dimension'] == dimension
    assert all(r == 0 for r in integrated['raw_DE_remainders'])
    assert all(c['verified'] for c in integrated['candidate_checks'])
    assert integrated['algebra']['status'] == 'verified_bracket_closure'
    assert integrated['algebra']['optimal_system_status'] == 'not_proved'


def test_model_identity_cannot_import_an_unrelated_maximality_certificate():
    model = branch_model('grass_cubic')
    model['equations'] = (*model['equations'][:2],model['equations'][2]+1)
    report = analyze(**model)
    assert report['classification_status'] == 'unresolved'
    assert 'fingerprint' in report['integration']['reason']


def test_slope_source_cubic_has_mixed_scaling_but_rejects_spatial_only():
    model = branch_model('slope_source_cubic')
    J = JetSpace(model['independent_variables'],model['dependent_fields'])
    t,x = J.x;h,u,B=J.u
    assert verify_generator(J,model['equations'],(t,2*x),(2*h,u,2*B))['verified']
    assert not verify_generator(J,model['equations'],(0,x),(2*h,u,2*B))['verified']


def test_zero_transport_does_not_turn_full_bed_into_a_flat_prescribed_bed():
    model = branch_model('zero_transport')
    J=JetSpace(model['independent_variables'],model['dependent_fields'])
    t,x=J.x;h,u,B=J.u
    result=verify_generator(J,model['equations'],(0,t),(0,1,0))
    assert not result['verified']
    assert result['residuals'][2] == -J.jet(2,(0,1))


def test_historical_parent_defects_and_fixed_kernel():
    from audit_parents import audit
    result=audit()
    assert not result['syntax']['style_template']['parseable']
    assert result['mixed_shell_witness'] == '-6'
    assert result['repaired_cubic_verified']
    assert result['printed_wrong_generator_rejected']


def test_review_gate_rejects_a_bare_success_flag(tmp_path):
    import json
    from classification import review_gate
    receipt=tmp_path/'review.json'
    receipt.write_text(json.dumps({'all_checks_passed':True,'passed':True}))
    assert not review_gate(receipt,root=tmp_path)['passed']
