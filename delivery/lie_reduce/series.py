"""Exact rational-pair series for the selected annular saddle."""
from flint import fmpq, fmpq_series

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
