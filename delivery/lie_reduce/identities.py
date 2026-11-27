"""Conservative exact identities with symbolic-parameter and power support."""
import sympy as sp


_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71)


def _witness_nonzero(expr):
    """Fast exact witness evaluation to reject non-identically-zero expressions before heavy CAS."""
    from sympy.core.function import AppliedUndef
    derivs = sorted(expr.atoms(sp.Derivative), key=lambda d: (-d.derivative_count, sp.default_sort_key(d)))
    undefs = sorted(expr.xreplace({d: 0 for d in derivs}).atoms(AppliedUndef), key=sp.default_sort_key)
    syms = sorted(expr.free_symbols, key=sp.default_sort_key)
    sub = {}
    idx = 0
    for item in (*derivs, *undefs, *syms):
        p = _PRIMES[idx % len(_PRIMES)]
        q = _PRIMES[(idx + 3) % len(_PRIMES)]
        # Use odd integer for exponent-like symbol 'm' so half-powers stay rational/algebraic
        sub[item] = sp.Integer(5) if str(item) == 'm' else sp.Rational(p + idx, q)
        idx += 1
    if not sub:
        return expr != 0, sub
    try:
        val = expr.xreplace(sub)
        if val.has(sp.zoo, sp.nan, sp.oo, -sp.oo):
            return False, None
        cval = complex(val.evalf(25))
        if abs(cval) > 1e-12:
            return True, sub
    except Exception:
        return False, None
    return False, None


def zero_record(expr):
    expr = sp.sympify(expr)
    if expr == 0 or sp.expand(expr) == 0:
        return {'status': 'proved_zero', 'method': 'identically zero after expansion', 'domain': 'everywhere'}
    if expr.has(sp.Float):
        return {'status': 'unknown', 'reason': 'floating-point input is not exact evidence'}
    is_nz, witness = _witness_nonzero(expr)
    if is_nz:
        return {'status': 'proved_not_identically_zero', 'witness': witness,
                'method': 'nonzero at exact rational witness point'}
    has_sym_pow = any(p.is_Pow and not p.exp.is_Integer for p in expr.atoms(sp.Pow))
    has_trig = bool(expr.atoms(sp.sin, sp.cos, sp.tan))
    if has_sym_pow or has_trig:
        num, _ = sp.together(sp.powsimp(sp.expand(expr))).as_numer_denom()
        num = sp.expand(sp.powsimp(sp.expand(num)))
        if has_trig and num != 0:
            num = sp.expand(sp.trigsimp(num))
        if num == 0:
            return {'status': 'proved_zero', 'method': 'exact symbolic power/trig normalization',
                    'domain': 'where the original expression is defined'}
        # Normalize composite symbolic powers (e.g. (u^2+v^2)^((m-1)/2) vs (u^2+v^2)^((m-3)/2))
        from .hidden import normalize_powers
        norm_num, _, _, _ = normalize_powers(num)
        if has_trig and norm_num != 0:
            norm_num = sp.expand(sp.trigsimp(norm_num))
        if norm_num == 0:
            return {'status': 'proved_zero', 'method': 'exact power-split numerator normalization',
                    'domain': 'where the original expression is defined'}
        return {'status': 'unknown', 'reason': 'outside rational/power-split zero form', 'expression': expr}
    try:
        numerator, denominator = sp.cancel(expr, extension=True).as_numer_denom()
    except (sp.PolynomialError, NotImplementedError):
        numerator, denominator = sp.together(expr).as_numer_denom()
    if numerator == 0:
        return {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization',
                'domain': 'where the original expression is defined'}
    variables = sorted(numerator.free_symbols, key=sp.default_sort_key)
    try:
        polynomial = sp.Poly(numerator, *(variables or [sp.Dummy('constant')]), extension=True)
        if any(c.is_algebraic is not True for c in polynomial.coeffs()):
            raise ValueError('nonalgebraic coefficients')
        return {'status': 'proved_not_identically_zero', 'numerator': polynomial.as_expr(),
                'denominator': denominator, 'method': 'nonzero polynomial over algebraic numbers'}
    except (sp.PolynomialError, ValueError, NotImplementedError):
        return {'status': 'unknown', 'reason': 'outside the supported rational/algebraic normal form',
                'expression': expr}


def require_zero(expr, stage):
    result = zero_record(expr)
    if result['status'] != 'proved_zero':
        raise ArithmeticError(f"{stage}: {result['status']}")
    return result


def nonzero_record(expr, positive=()):
    expr = sp.factor(sp.sympify(expr))
    if expr.has(sp.Float):
        return {'status': 'unknown', 'expression': expr, 'reason': 'floating-point input'}
    replacements = {v: sp.Dummy('positive', positive=True) for v in positive if isinstance(v, sp.Symbol)}
    changed = expr.xreplace(replacements)
    if changed.is_zero is True:
        return {'status': 'zero', 'expression': expr}
    if changed.is_nonzero is True:
        return {'status': 'proved_nonzero', 'expression': expr, 'method': 'exact signs and declared positive symbols'}
    if changed.func == sp.exp:
        return {'status': 'proved_nonzero', 'expression': expr, 'method': 'exponential never vanishes'}
    if changed.is_Mul and all(nonzero_record(v, positive)['status'] == 'proved_nonzero' for v in changed.args):
        return {'status': 'proved_nonzero', 'expression': expr, 'method': 'product of proved nonzero factors'}
    return {'status': 'conditional', 'expression': expr, 'required_condition': sp.Ne(expr, 0),
            'reason': 'nonvanishing not established on the whole chart'}
