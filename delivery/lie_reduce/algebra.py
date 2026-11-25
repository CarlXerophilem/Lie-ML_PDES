"""Appendix B catalogue is input; algebra membership and brackets are computed."""
import sympy as sp
from itertools import combinations, product


def bracket(X,Y,coordinates):
    X,Y=sp.Matrix(X),sp.Matrix(Y)
    return tuple(Y.jacobian(coordinates)*X-X.jacobian(coordinates)*Y)


def add(*weighted):
    return tuple(sp.expand(sum(c*X[i] for c,X in weighted)) for i in range(len(weighted[0][1])))


def catalogue(spec,basis,exponent):
    scalar=spec.name in ('P','M'); pre='Y' if scalar else 'X'
    T,S,Z=(basis[pre+str(i)] for i in ((1,3,2) if scalar else (1,2,3)))
    D=basis[pre+'4']; c,delta,b=sp.symbols('c delta b',real=True)
    out=[]
    def row(label,X,conditions=()): out.append({'id':label,'generator':X,'parameter_conditions':conditions})
    if spec.name=='P' and exponent==1:
        G=basis['Y6'];row('B.linear.D+deltaG',add((1,D),(delta,G)));row('B.linear.G',G)
        for e in (-1,1):
            row(f'B.linear.G+{e}T+cS',add((1,G),(e,T),(c,S)))
            row(f'B.linear.G+{e}S',add((1,G),(e,S)))
        row('B.linear.T+cS',add((1,T),(c,S)));row('B.linear.S+deltaZ',add((1,S),(delta,Z)));row('B.linear.Z',Z)
    elif exponent!=3:
        row('B.generic.scaling',D if scalar else add((1,D),(delta,Z)))
        for e in ((delta,) if scalar else (-1,0,1)):
            row(f'B.generic.T+cS+{e}Z',add((1,T),(c,S),(e,Z)))
            row(f'B.generic.S+{e}Z',add((1,S),(e,Z)))
        row('B.generic.Z',Z)
    else:
        C=basis[pre+'5']
        row('B.cubic.D+bC',add((1,D),(b,C)),('b avoids exceptional zero weights handled below',))
        row('B.cubic.C',C)
        special=[(-1,T),(sp.Rational(1,2),S)] if scalar else [(-1,T),(0,Z)]
        for v,A in special:
            for e in (-1,0,1): row(f'B.cubic.D+{v}C+{e}A',add((1,D),(v,C),(e,A)))
        for e in (-1,0,1):row(f'B.cubic.C+{e}A',add((1,C),(e,Z if scalar else S)))
        for size in (1,2,3):
            for support in combinations(range(3),size):
                for signs in product((-1,1),repeat=size-1):
                    co=(1,)+signs
                    if scalar and size==3:
                        if signs[-1]!=1:continue
                        co=(1,signs[0],delta)
                    row('B.cubic.translation.'+str((support,co)),add(*[(v,(T,S,Z)[i]) for v,i in zip(co,support)]),
                        ('delta != 0',) if scalar and size==3 else ())
    return out


def weights(spec,basis):
    scalar=spec.name in ('P','M');pre='Y' if scalar else 'X'
    coords=spec.jets.independent+spec.jets.dependent
    return {f'[{left},{right}]':bracket(X,Y,coords) for left,X in basis.items()
            for right,Y in basis.items() if left<right}


def coordinates_in_basis(X,basis,coordinates):
    constants=sp.symbols('c:'+str(len(basis)))
    residual=add((1,X),*[(-c,Y) for c,Y in zip(constants,basis)])
    rows=[v for e in residual for v in sp.Poly(e,*coordinates).coeffs()]
    solutions=sp.solve(rows,constants,dict=True)
    if len(solutions)!=1 or set(solutions[0])!=set(constants):
        raise ValueError('generator not uniquely represented in supplied basis')
    return tuple(solutions[0][c] for c in constants)


def adjoint_matrix(X,basis,coordinates,epsilon):
    ad=sp.Matrix.hstack(*(sp.Matrix(coordinates_in_basis(bracket(X,Y,coordinates),basis,coordinates)) for Y in basis))
    return (epsilon*ad).exp()
