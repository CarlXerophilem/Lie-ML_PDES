"""Rank-drop varieties from maximal minors, not separate parameter gcds."""
from itertools import combinations
from math import comb
import sympy as sp


def rank_locus(matrix, parameters, max_minors=2000):
    rank = matrix.rank()
    if not parameters or not rank:
        return {'generic_rank':rank,'status':'constant_rank' if not parameters else 'zero_matrix'}
    count=comb(matrix.rows,rank)*comb(matrix.cols,rank)
    if count>max_minors:
        return {'generic_rank':rank,'status':'not_computed','reason':f'{count} maximal minors exceed cap {max_minors}'}
    minors=[sp.factor(matrix.extract(i,j).det()) for i in combinations(range(matrix.rows),rank)
            for j in combinations(range(matrix.cols),rank)]
    numerators=[sp.cancel(v).as_numer_denom()[0] for v in minors if v!=0]
    denominators=[sp.cancel(v).as_numer_denom()[1] for v in matrix]
    if len(parameters)==1:
        generators=[sp.gcd_list(numerators)]
    else:
        generators=list(sp.groebner(numerators,*parameters).exprs)
    return {'generic_rank':rank,'status':'rank_drop_ideal','generators':generators,
            'excluded_denominators':sorted(set(denominators),key=sp.default_sort_key),
            'interpretation':'common zeros of all generators; denominator exclusions apply'}
