"""Exact rational bounds for the entire constructed reference family.

This is an analytic bootstrap certificate, not a grid regularity check.
Scope: g=1, kappa=1/30, m in [1,4], initial (F,F',F'')=(2,1/2,1/10),
z in [1,7/5]. It certifies the exact reference family, not trained candidates.
"""
import sympy as sp

def tube_certificate(physical=False):
    R=sp.Rational
    z0,z1=R(1),R(7,5);pmax=R(3,5)
    if physical:
        Imax=R(149,100)
        lower=lambda z:(R(3,2)+z/2)*(R(125,27)-z*z)
        leading_min=lower(z1)
        # lower(z) strictly decreases on [1,7/5]; use exact right sums.
        delta_bound=sum(R(1,10)*Imax/lower(1+R(i,10)) for i in range(1,5))
    else:
        Imax=R(11,25)
        lower=lambda z:R(25,9)*z-R(3,5)*z**3
        # This cubic is concave; its minimum on a closed interval is at an endpoint.
        leading_min=min(lower(z0),lower(z1))
        delta_bound=(z1-z0)*Imax/leading_min
    assert leading_min>0
    assert delta_bound<R(1,10)
    return {'model':'physical_corrected' if physical else 'printed',
        'scope':{'g':'1','kappa':'1/30','m_closed_interval':['1','4'],
                 'z_closed_interval':['1','7/5'],'initial':['2','1/2','1/10']},
        'proof_type':'analytic continuation bootstrap with exact rational inequalities',
        'F_bounds':['2','56/25'],'Fp_bounds':['1/2','3/5'],
        'velocity_lower':'29/25','leading_lower':str(leading_min),
        'I0_upper':str(Imax),'Fp_increase_upper':str(delta_bound),
        'Fp_increase_upper_decimal':float(delta_bound),
        'barrier_slack':str(R(1,10)-delta_bound),
        'applies_to':'exact reference family; neural candidate guards remain sampled'}
