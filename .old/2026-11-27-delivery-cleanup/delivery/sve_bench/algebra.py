"""Exact Q(sqrt(141)) series and outward-rounded coefficient majorants."""
from flint import fmpq, fmpq_series, arb
import sympy as sp

ROOT141=sp.sqrt(141)


class Series:
    """Two rational FLINT series, representing a+b sqrt(141)."""
    def __init__(self,a,b=None,order=64):
        self.order=order
        self.a=a if isinstance(a,fmpq_series) else fmpq_series(a if isinstance(a,list) else [a],prec=order)
        self.b=b if isinstance(b,fmpq_series) else fmpq_series(b if isinstance(b,list) else [b or 0],prec=order)

    def cast(self,x): return x if isinstance(x,Series) else Series(x,order=self.order)
    def __add__(self,x):
        x=self.cast(x);return Series(self.a+x.a,self.b+x.b,order=self.order)
    __radd__=__add__
    def __neg__(self): return Series(-self.a,-self.b,order=self.order)
    def __sub__(self,x): return self+-self.cast(x)
    def __rsub__(self,x): return self.cast(x)+-self
    def __mul__(self,x):
        x=self.cast(x);return Series(self.a*x.a+141*self.b*x.b,self.a*x.b+self.b*x.a,order=self.order)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.cast(x);den=x.a*x.a-141*x.b*x.b
        return Series((self.a*x.a-141*self.b*x.b)/den,(self.b*x.a-self.a*x.b)/den,order=self.order)
    def __rtruediv__(self,x): return self.cast(x)/self
    def __pow__(self,n):
        if n<0:return 1/(self**(-n))
        result=Series(1,order=self.order)
        for _ in range(n):result=result*self
        return result
    def diff(self):
        return Series([i*self.a[i] for i in range(1,self.order)],
                      [i*self.b[i] for i in range(1,self.order)],order=self.order)
    def coefficient(self,i):return self.a[i],self.b[i]
    def pairs(self,n):return [[str(self.a[i]),str(self.b[i])] for i in range(n)]


def annular(r,h):
    v=1/(r*h);w=1/r-r/2;q=-71/(16*r)+7*r/2
    speed=v*v+w*w;pz=v-q/speed
    return h-v*v,h*(speed/r+w-pz),pz


def pair(expr):
    expr=sp.expand(sp.radsimp(expr))
    b=expr.coeff(ROOT141);a=sp.expand(expr-b*ROOT141)
    assert a.is_Rational and b.is_Rational,(a,b)
    return [str(a),str(b)]


def ball_pair(value):return arb(value[0])+arb(value[1])*arb(141).sqrt()


def polynomial_record(expr,x,w):
    poly=sp.Poly(expr,x,w,extension=ROOT141)
    return [[i,j,*pair(c)] for (i,j),c in poly.terms()]


def majorant(poly,R,W,dx=0,dw=0):
    total=arb(0)
    for i,j,a,b in poly:
        if i<dx or j<dw:continue
        weight=1
        for q in range(dx):weight*=i-q
        for q in range(dw):weight*=j-q
        total+=abs(ball_pair((a,b)))*weight*R**(i-dx)*W**(j-dw)
    return total


def lower_denominator(poly,R,W):
    constant=next(ball_pair((a,b)) for i,j,a,b in poly if i==j==0)
    rest=[row for row in poly if row[:2]!=[0,0]]
    return abs(constant)-majorant(rest,R,W)


def interval_polynomial(poly,x,w):
    # Nested Horner form avoids a dependency-heavy sum of powers.
    values={(i,j):ball_pair((a,b)) for i,j,a,b in poly}
    result=arb(0)
    max_i=max(i for i,j in values)
    for i in range(max_i,-1,-1):
        column=arb(0)
        max_j=max((j for ii,j in values if ii==i),default=0)
        for j in range(max_j,-1,-1):column=column*w+values.get((i,j),arb(0))
        result=result*x+column
    return result


def outward(value):
    return {'enclosure':str(value),'lower':str(value.lower()),'upper':str(value.upper())}
