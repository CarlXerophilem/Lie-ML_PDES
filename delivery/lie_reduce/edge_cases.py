"""Executable presentation/fixed-locus certificates and negative controls."""
import sympy as sp
from .jets import JetSpace
from .spec import PDESpec
from .presentation import square_free_presentation
from .fixed import vertical_fixed_graphs
from .determining import symmetries


def run():
    t,x,u=sp.symbols('t x u',real=True);j=JetSpace((t,x),(u,),1)
    ut,ux=j.jet(0,1,0),j.jet(0,0,1)
    plain=PDESpec('stationary',j,(ut,),(ut,))
    squared=PDESpec('repeated presentation',j,(ut**2,),(ut,))
    try:squared.shell()
    except ValueError as exc:rejection={'status':'rejected_as_original','reason':str(exc)}
    else:raise ArithmeticError('repeated presentation incorrectly accepted')
    normalized=square_free_presentation(squared)
    result=symmetries(normalized['normalized_spec'],1)
    from .run import span_equal
    reference=symmetries(plain,1)
    if not span_equal(result['basis'],reference['basis'],(t,x,u)):
        raise ArithmeticError('regularized point kernel differs from regular reference')
    union=square_free_presentation(PDESpec('union presentation',j,(ut**2*ux**3,),(ut,)))
    if len(union['components'])!=2:raise ArithmeticError('lost a zero-set component')
    fixed={
        'scaling':vertical_fixed_graphs(plain,(0,0,u)),
        'translation':vertical_fixed_graphs(plain,(0,0,1)),
        'two_fixed_graphs':vertical_fixed_graphs(plain,(0,0,u*(u-1))),
        'positive_chart':vertical_fixed_graphs(PDESpec('positive stationary',j,(ut,),(ut,),positive=(u,)),(0,0,u)),
        'nonsymmetry':vertical_fixed_graphs(PDESpec('forced stationary',j,(ut-1,),(ut,)),(0,0,u))}
    if fixed['scaling']['branches'][0]['status']!='verified_fixed_solution':raise ArithmeticError('fixed solution lost')
    if fixed['positive_chart']['status']!='no invariant graph':raise ArithmeticError('positive chart violated')
    if fixed['nonsymmetry']['status']!='rejected':raise ArithmeticError('nonsymmetry accepted')
    return {'schema':'Definition 6.1 symbolic provenance extension','status':'passed','ML':False,'degree':1,
            'scope':'explicit rational presentations and vertical fixed-graph examples',
            'original_rejection':rejection,'regularized_equivalence':normalized,
            'regularized_basis':result['basis'],'regular_reference_span_equal':True,
            'union_of_components':union,'fixed_graphs':fixed}
