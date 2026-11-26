"""Training-visible equations and lifts. No reference solution imports."""
from dataclasses import dataclass
import math
import sympy as sp
import numpy as np
from fractions import Fraction
from functools import cached_property


@dataclass(frozen=True)
class Problem:
    id: str
    data: dict

    @property
    def X(self):return float(Fraction(self.data['half_width']))
    @property
    def initial(self):return {'N1':1.,'N2':.5}.get(self.id,0.)
    @property
    def saddle(self):return self.id.startswith('N3')
    @property
    def interval(self):return (-1.,1.) if self.saddle else (0.,1.)
    @property
    def ell(self):return float(self.data.get('slope',0))
    @property
    def b(self):return float(self.data.get('b',0))

    @cached_property
    def polynomials(self):
        return [{(i,j):float(Fraction(a))+float(Fraction(b))*math.sqrt(141) for i,j,a,b in self.data[key]}
                for key in ('psi_numerator','psi_denominator')]

    def psi(self,x,w):
        def evaluate(values):
            result=0*x
            for i in range(max(i for i,j in values),-1,-1):
                column=0*w
                for j in range(max((j for ii,j in values if ii==i),default=0),-1,-1):
                    column=column*w+values.get((i,j),0.)
                result=result*x+column
            return result
        return evaluate(self.polynomials[0])/evaluate(self.polynomials[1])

    def residual(self,s,y,dy):
        """General R(s,y,y_s;mu,data), independent of the trial representation."""
        if self.id=='N1':return 2*y*dy/self.X+1
        if self.id=='N2':
            # Clearing p^3 is valid on the recorded p>0 chart. Zero-gradient
            # spurious solutions are rejected by the independent guard checks.
            return ((10-y*y-12*y**3)*dy/self.X-20*y**3)/2.5
        return s*dy+self.b*y-self.psi(self.X*s,self.X*y)/self.X

    def rhs(self,s,y):
        if self.id=='N1':return -self.X/(2*y)
        if self.id=='N2':return self.X*20*y**3/(10-y*y-12*y**3)
        raise ValueError('Saddle uses the Briot–Bouquet operator, never N/D at rho=0')

    def physical(self,s,y,dy):
        if not self.saddle:return y,dy/self.X
        rho=self.X*s
        return 1+self.ell*rho+self.X*rho*y,self.ell+self.X*y+rho*dy

    def training_view(self):
        allowed={'id','model','generator','chart','half_width','slope','slope_exact','b','b_exact',
                 'psi_numerator','psi_denominator','prefix','guards','reference_radius','remainder_radius',
                 'parameters','lift','initial','branch'}
        assert set(self.data)<=allowed,set(self.data)-allowed
        return self


def load_problems(out):
    import json
    data=json.loads((out/'problems.json').read_text())
    return [Problem(k,v).training_view() for k,v in data.items()]
