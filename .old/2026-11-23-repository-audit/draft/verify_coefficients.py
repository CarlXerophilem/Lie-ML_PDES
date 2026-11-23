"""Independent exact coefficient checks. Requires SymPy. No numerical experiments."""
import json
from pathlib import Path
import sympy as s

r,H,c,z,a,b=s.symbols('r H c z a b')
V=1/(r*H)
W=1/r-r/2
Q=(c/2-s.Rational(15,16))/r-c*r/2
P=V-Q/(V**2+W**2)
D=H-V**2
N=H*((V**2+W**2)/r+W-P)
A=s.simplify(s.Matrix([D,N]).jacobian([r,H]).subs({r:1,H:1}))
assert A==s.Matrix([[2,3],[-(33+4*c)/5,-s.Rational(11,5)]])
assert s.simplify(A.det()-(77+12*c)/5)==0
Hpoly=1+a*z+b*z**2
expr=D.subs({r:1+z,H:Hpoly})*s.diff(Hpoly,z)-N.subs(c,-7).subs({r:1+z,H:Hpoly})
num,den=s.fraction(s.cancel(expr))
p=s.Poly(num,z)
a2=(150*a**3+184*a**2+642*a+1155)/(10*(45*a+31))
remainders=[]
for j in range(3):
    numerator=s.fraction(s.cancel(p.nth(j).subs(b,a2)))[0]
    remainder=s.rem(numerator,15*a*a+21*a+5,a)
    assert remainder==0,(j,remainder)
    remainders.append(str(remainder))
report={'critical_jacobian':str(A),'determinant':str(s.factor(A.det())),
        'original_undivided_numerator_remainders_orders_0_1_2':remainders,
        'a2':str(a2),
        'scope':'Exact symbolic checks only; convergence is proved in the manuscript, no numerical radius claimed.'}
Path(__file__).with_name('symbolic_checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
