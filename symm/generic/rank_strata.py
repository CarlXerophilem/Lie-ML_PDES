"""Exact finite-ansatz matrices and univariate determinantal strata."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Sequence

import sympy as sp


@dataclass(frozen=True)
class RankStrata:
    matrix: sp.Matrix
    coefficients: tuple[sp.Symbol, ...]
    parameter: sp.Symbol
    generic_rank: int
    maximal_minors: tuple[sp.Expr, ...]
    minor_gcd: sp.Expr
    exceptional_values: tuple[sp.Expr, ...]

    def nullity(self, value: sp.Expr) -> int:
        return self.matrix.cols - self.matrix.subs(self.parameter, value).rank()


def coefficient_matrix(equations: Sequence[sp.Expr], coefficients: Sequence[sp.Symbol],
                       split_variables: Sequence[sp.Symbol]) -> sp.Matrix:
    rows = []
    coefficients = tuple(coefficients)
    for expression in equations:
        polynomial = sp.Poly(sp.expand(expression), *split_variables)
        for value in polynomial.coeffs():
            row = [sp.diff(value, c) for c in coefficients]
            if sp.expand(value - sum(c*r for c, r in zip(coefficients, row))) != 0:
                raise ValueError("determining equations must be homogeneous linear in ansatz coefficients")
            if any(row) and row not in rows:
                rows.append(row)
    return sp.Matrix(rows) if rows else sp.zeros(0, len(coefficients))


def determinantal_strata(matrix: sp.Matrix, coefficients: Sequence[sp.Symbol],
                        parameter: sp.Symbol, *, max_minors: int = 100000) -> RankStrata:
    rank = matrix.rank()
    if rank == 0:
        return RankStrata(matrix, tuple(coefficients), parameter, 0, (), sp.S.One, ())
    count = comb(matrix.rows, rank)*comb(matrix.cols, rank)
    if count > max_minors:
        raise ValueError(f"exact minor enumeration needs {count} minors, budget is {max_minors}")
    minors = set()
    gcd = sp.S.Zero
    for rows in combinations(range(matrix.rows), rank):
        for cols in combinations(range(matrix.cols), rank):
            determinant = sp.factor(matrix.extract(rows, cols).det(method="domain-ge"))
            if determinant != 0:
                minors.add(determinant)
                gcd = sp.gcd(gcd, determinant)
    gcd = sp.factor(gcd)
    roots = tuple(root for root in sp.solve(gcd, parameter) if root.is_real is not False)
    return RankStrata(matrix, tuple(coefficients), parameter, rank,
                      tuple(sorted(minors, key=str)), gcd, roots)
