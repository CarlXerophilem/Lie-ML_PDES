"""Conservative exact identities. Unknown is never a proof of nonzero."""
import sympy as sp


def zero_record(expr):
    expr=sp.sympify(expr)
    if expr.has(sp.Float):
        return {'status':'unknown','reason':'floating-point input is not exact evidence'}
    numerator,denominator=sp.cancel(expr,extension=True).as_numer_denom()
    if numerator==0:
        return {'status':'proved_zero','method':'exact rational/algebraic numerator normalization',
                'domain':'where the original expression is defined'}
    variables=sorted(numerator.free_symbols,key=sp.default_sort_key)
    try:
        polynomial=sp.Poly(numerator,*(variables or [sp.Dummy('constant')]),extension=True)
        if any(c.is_algebraic is not True for c in polynomial.coeffs()):
            raise ValueError('nonalgebraic coefficients')
        return {'status':'proved_not_identically_zero','numerator':polynomial.as_expr(),
                'denominator':denominator,'method':'nonzero polynomial over algebraic numbers'}
    except (sp.PolynomialError,ValueError,NotImplementedError):
        return {'status':'unknown','reason':'outside the supported rational/algebraic normal form',
                'expression':expr}


def require_zero(expr,stage):
    result=zero_record(expr)
    if result['status']!='proved_zero':
        raise ArithmeticError(f"{stage}: {result['status']}")
    return result


def nonzero_record(expr,positive=()):
    expr=sp.factor(sp.sympify(expr))
    if expr.has(sp.Float):return {'status':'unknown','expression':expr,'reason':'floating-point input'}
    replacements={v:sp.Dummy('positive',positive=True) for v in positive if isinstance(v,sp.Symbol)}
    changed=expr.xreplace(replacements)
    if changed.is_zero is True:return {'status':'zero','expression':expr}
    if changed.is_nonzero is True:
        return {'status':'proved_nonzero','expression':expr,'method':'exact signs and declared positive symbols'}
    # Products of real exponentials never vanish. Recursion retains other factors.
    if changed.func==sp.exp:return {'status':'proved_nonzero','expression':expr,'method':'exponential never vanishes'}
    if changed.is_Mul and all(nonzero_record(v)['status']=='proved_nonzero' for v in changed.args):
        return {'status':'proved_nonzero','expression':expr,'method':'product of proved nonzero factors'}
    return {'status':'conditional','expression':expr,'required_condition':sp.Ne(expr,0),
            'reason':'nonvanishing not established on the whole chart'}
