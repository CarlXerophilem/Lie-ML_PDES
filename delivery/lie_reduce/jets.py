from itertools import product
import sympy as sp


class JetSpace:
    """Symmetric multi-index jets, with vector dependent variables from the outset."""
    def __init__(self, independent, dependent, order):
        self.independent, self.dependent = tuple(independent), tuple(dependent)
        self.order = order
        self.zero = (0,) * len(independent)
        self.indices = sorted((j for j in product(range(order+1), repeat=len(independent))
                               if sum(j) <= order), key=lambda j: (sum(j), tuple(-v for v in j)))
        self.jets = {(a,j): (u if not any(j) else sp.Symbol(
            str(u)+'_'+'_'.join(map(str,j)), real=True))
            for a,u in enumerate(dependent) for j in self.indices}

    def jet(self, a, *j):
        return self.jets[a,tuple(j)]

    def D(self, expression, axis):
        expression = sp.sympify(expression)
        result = sp.diff(expression, self.independent[axis])
        for (a,j),v in self.jets.items():
            derivative = sp.diff(expression,v)
            if derivative == 0:
                continue
            nxt = tuple(n+int(k==axis) for k,n in enumerate(j))
            if (a,nxt) not in self.jets:
                raise ValueError('total derivative exceeds allocated jet order')
            result += derivative*self.jets[a,nxt]
        return sp.expand(result)

    def prolong(self, field):
        n = len(self.independent)
        xi, eta = tuple(field[:n]), tuple(field[n:])
        if len(eta) != len(self.dependent):
            raise ValueError('generator has wrong vector dimension')
        dxi = [[self.D(v,i) for v in xi] for i in range(n)]
        result = {}
        for a,e in enumerate(eta):
            result[a,self.zero] = sp.sympify(e)
            for j in self.indices[1:]:
                i = next(k for k,v in enumerate(j) if v)
                prev = tuple(v-int(k==i) for k,v in enumerate(j))
                result[a,j] = sp.expand(self.D(result[a,prev],i)-sum(
                    self.jets[a,tuple(v+int(k==l) for k,v in enumerate(prev))]*dxi[i][l]
                    for l in range(n)))
        return result

    def act(self, expression, field):
        coefficients = self.prolong(field)
        return sp.expand(sum(v*sp.diff(expression,x) for v,x in zip(field,self.independent))+
                         sum(coefficients[key]*sp.diff(expression,v) for key,v in self.jets.items()))

    def pullback(self, graphs):
        return {v: sp.diff(graphs[a], *[(x,k) for x,k in zip(self.independent,j) if k])
                if any(j) else graphs[a] for (a,j),v in self.jets.items()}
