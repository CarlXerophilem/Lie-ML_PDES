"""Exact same-base real-power normalization on u^2+v^2>0.

This preserves exponent multiplication relations; it never regards shifted
powers as independent variables or splits equations by parameter powers.
Only integer exponent shifts are moved into coefficients before restoring
the defining polynomial of the positive squared speed.
"""
import sympy as sp


def normalize(expression,u,v):
    expression=sp.sympify(expression)
    reduced=sp.simplify(sp.factor_terms(sp.expand(expression)))
    if reduced==0:
        return reduced
    base=u*u+v*v
    radius=sp.Dummy('positive_squared_speed',positive=True)
    expanded=sp.expand(reduced.xreplace({base:radius}))
    grouped={}
    for term in sp.Add.make_args(expanded):
        exponent,coefficient=sp.S.Zero,sp.S.One
        for factor in sp.Mul.make_args(sp.factor_terms(term)):
            if factor==radius:
                exponent+=1
            elif isinstance(factor,sp.Pow) and factor.base==radius:
                exponent+=factor.exp
            else:
                coefficient*=factor
        constant,variable=sp.expand(exponent).as_coeff_Add()
        integer=sp.floor(constant)
        if integer.is_Integer:
            key=sp.simplify(variable+constant-integer)
            coefficient*=radius**integer
        else:
            key=sp.simplify(exponent)
        grouped[key]=grouped.get(key,sp.S.Zero)+coefficient
    return sp.factor_terms(sum(sp.simplify(coefficient.subs(radius,base))*base**exponent
                               for exponent,coefficient in grouped.items()))
