"""Independent exact spot checks of the 24 November manuscript.

Run from any directory with Python and SymPy. These substitutions do not
establish completeness of symmetry classifications or analytic convergence.
"""
import json
import sympy as s


checks = {}


def zero(name, expression):
    value = s.factor(expression)
    checks[name] = {"passed": value == 0, "difference": str(value)}


t, x, z, g, kappa, beta = s.symbols("t x z g kappa beta", positive=True)
c, gamma = s.symbols("c gamma", real=True)
F = s.Function("F")(z)
p = s.diff(F, z)

# Direct material pullback of a tilted translation graph, at m=2.
A = (c**2*p - g/p**2)*s.diff(p, z)
T = -c*(gamma-c*p)*s.diff(p, z)/p
M = -c*s.diff(A, z)-s.diff(g*beta*T+(gamma-c*p)*A/p, z)
L = gamma*(g/p**3-c**2)+g*beta*c*(gamma-c*p)/p
zero("tilted_material_m2", M-s.diff(L*s.diff(p, z), z))
P = -c*s.diff(A, z)-g*beta*s.diff(T, z)
LP = c*(-c**2*p+g/p**2+g*beta*(gamma-c*p)/p)
zero("tilted_printed_m2", P-s.diff(LP*s.diff(p, z), z))

# Material chain rule applied directly to the common-scaling graph.
label = s.symbols("label", real=True)
phi = t*s.Function("F")(label/t)
Aphi = s.diff(phi,label)*s.diff(phi,t,2)-g*s.diff(phi,label,2)/s.diff(phi,label)**2
Tphi = s.diff(phi,t)*s.diff(phi,t,label)/s.diff(phi,label)
Mphi = s.diff(Aphi,t)-s.diff(g*beta*Tphi+s.diff(phi,t)*Aphi/s.diff(phi,label),label)
Lscale = F*(g/p**3-z**2)+g*beta*z*(F-z*p)/p
zero("common_scaling_material_m2", (t**2*Mphi).subs(label,t*z).doit()-s.diff(Lscale*s.diff(p,z),z))

hh, uu, qq, FF, pp, zz = s.symbols("h u q F p z")
AE = s.Matrix([[uu,hh,0],[g,uu,g],[0,qq,0]])
det = (AE-FF*s.eye(3)).det().subs({hh:1/pp,uu:FF-zz*pp,qq:beta*(FF-zz*pp)})
zero("characteristic_determinant_m2",det-pp**2*(FF*(g/pp**3-zz**2)+g*beta*zz*(FF-zz*pp)/pp))

# The explicit cubic Eulerian wave, on t,x>0 and 4*g*kappa<1.
u = 2*x/(3*t)
h = (1-4*g*kappa)*x**2/(9*g*t**2)
B = 4*kappa*x**2/(9*t**2)
zero("cubic_wave_continuity",s.diff(h,t)+s.diff(h*u,x))
zero("cubic_wave_momentum",s.diff(u,t)+u*s.diff(u,x)+g*s.diff(h+B,x))
zero("cubic_wave_exner",s.diff(B,t)+kappa*s.diff(u**3,x))

# Direct differentiation of the separate annular radial field.
r, H = s.symbols("r H",positive=True)
V = 1/(r*H)
W = 1/r-r/2
Q = (c/2-s.Rational(15,16))/r-c*r/2
speed2 = V**2+W**2
PZ = V-Q/speed2
D = H-V**2
N = H*(speed2/r+W-PZ)
point = {r:1,H:1}
zero("annular_compatible_D",D.subs(point))
zero("annular_compatible_N",N.subs(point))
zero("annular_bed_slope",PZ.subs(point)-s.Rational(7,4))
J = s.Matrix([D,N]).jacobian([r,H]).subs(point)
target = s.Matrix([[2,3],[-(33+4*c)/5,-s.Rational(11,5)]])
zero("annular_jacobian",sum((J-target).applyfunc(lambda e:e**2)))
zero("annular_determinant",J.det()-(77+12*c)/5)

# Rational majorants in the regular-series example, using |z|<=1/16,
# |F-1|,|p-1|<=1/16. These bound a complex polydisk, not sampled points.
R = a = s.Rational(1,16)
qmin = 1-a
qmax = 1+a
Ldiff = (a+3*a+3*a*a+a**3)/qmin**3+(2+a)*R**2+R*(1+a)/qmin
LF = qmin**-3+R**2+R/qmin
Lp = 3*(1+a)/qmin**4+R*(1+a)/qmin**2
checks["regular_polydisk_majorants"] = {
    "passed":bool(Ldiff<s.Rational(1,2) and LF<2 and Lp<5),
    "L_minus_one_upper":str(Ldiff),"L_F_upper":str(LF),"L_p_upper":str(Lp),
    "radius":str(min(R,a/4,s.Rational(1,56))),
}

print(json.dumps(checks,indent=2))
raise SystemExit(0 if all(row["passed"] for row in checks.values()) else 1)
