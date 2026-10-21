import sympy as sp
from parent_models import scalar_models, verify_scalar_and_material


def test_scalar_closedness_and_material_reconstruction_are_separate():
    report=verify_scalar_and_material()
    assert report['all_passed']
    witness=report['P_only_counterexample']
    assert witness['P']==0
    assert witness['M']!=0
    assert report['material_constant_slope']['wrong_printed_bed_t_defect']!=0
    assert not report['point_algebra_equivalence_claim']


def test_common_scaling_of_both_scalar_models_uses_the_shared_jet_kernel():
    from main import JetSpace, verify_generator
    z=scalar_models()
    t,s,phi=(z[k] for k in ('t','s','phi'))
    w=sp.Symbol('w',real=True)
    J=JetSpace((t,s),(w,))
    for name in ('P','M'):
        expression=z[name].doit()
        mapping={d:J.jet(0,(d.variables.count(t),d.variables.count(s)))
                 for d in expression.atoms(sp.Derivative) if d.expr==phi}
        equation=expression.xreplace(mapping).subs(phi,w)
        assert verify_generator(J,(equation,),(t,s),(w,))['verified']
