# Computed Lie reductions (no ML)

Generated from PDE pullbacks. `verified` means symbolic local identity, not certified numerical data or global chart admissibility.
Finite polynomial discovery: degree 2 at m=1,2,3,4. All-real-m smooth claims belong to the separately frozen proofs.

## P, m=1

Discovery: completed.

### B.linear.D+deltaG

Generator: `['t', 's', 'delta*t + phi']`

Status: **verified**.

Graph: `['t*(delta*log(t) + F0(s/t))']`

```text
-(delta*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + delta*Derivative(F0(z), z)**4 - g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-delta*z*Derivative(F0(z), z) - (-g*kappa*z*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', 't != 0', 'local flow chart; logarithm arguments positive when used', 'delta*log(t) + delta - s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.linear.G

Generator: `['0', '0', 't']`

Status: **no invariant graph**.

polynomial base constraint cannot hold on an open base patch; parameter specializations must be checked separately

### B.linear.G+-1T+cS

Generator: `['-1', 'c', 't']`

Status: **verified**.

Graph: `['-t**2/2 + F0(c*t + s)']`

```text
c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2 - Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': 'c*(c**2*Derivative(F0(z), z)**4 - g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3 - c*Derivative(F0(z), z)', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '-1 != 0', 'local flow chart; logarithm arguments positive when used', 'c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, c*t + s) - t > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.linear.G+-1S

Generator: `['0', '-1', 't']`

Status: **verified**.

Graph: `['-s*t + F0(t)']`

```text
-z*Derivative(F0(z), (z, 3)) - Derivative(F0(z), (z, 2)) = 0
```

First integral: `{'status': 'verified', 'flux': '-z*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '-1 != 0', 'local flow chart; logarithm arguments positive when used', '-s + Derivative(F0(t), t) > 0', '-t > 0', 'g > 0', 'kappa > 0']`

### B.linear.G+1T+cS

Generator: `['1', 'c', 't']`

Status: **verified**.

Graph: `['t**2/2 + F0(-c*t + s)']`

```text
-c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2 + Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(c**2*Derivative(F0(z), z)**4 - g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3 - c*Derivative(F0(z), z)', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + t > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.linear.G+1S

Generator: `['0', '1', 't']`

Status: **verified**.

Graph: `['s*t + F0(t)']`

```text
z*Derivative(F0(z), (z, 3)) + Derivative(F0(z), (z, 2)) = 0
```

First integral: `{'status': 'verified', 'flux': 'z*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 's + Derivative(F0(t), t) > 0', 't > 0', 'g > 0', 'kappa > 0']`

### B.linear.T+cS

Generator: `['1', 'c', '0']`

Status: **verified**.

Graph: `['F0(-c*t + s)']`

```text
-c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(c**2*Derivative(F0(z), z)**4 - g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.linear.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.linear.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(-g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(-g*kappa*z*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(c**2*Derivative(F0(z), z)**4 - g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## P, m=2

Discovery: completed.

### B.generic.scaling

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(2*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 2*g*kappa*z*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 2*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 2*g*kappa*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(2*g*kappa*z**2*Derivative(F0(z), z)**3 - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+deltaZ

Generator: `['1', 'c', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(-c*t + s)']`

```text
-c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 2*c*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 2*delta*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 2*delta*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(c**2*Derivative(F0(z), z)**4 + 2*c*g*kappa*Derivative(F0(z), z)**3 - 2*delta*g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + delta > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(2*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 2*g*kappa*z*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 2*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 2*g*kappa*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(2*g*kappa*z**2*Derivative(F0(z), z)**3 - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-c*(c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 2*c*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 2*g*gamma*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 2*g*gamma*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(c**2*Derivative(F0(z), z)**4 + 2*c*g*kappa*Derivative(F0(z), z)**3 - 2*g*gamma*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## P, m=3

Discovery: completed.

### B.cubic.D+bC

Generator: `['b*t + t', '-2*b*s + s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp((2*b - 1)*log(t)/(b + 1)))*exp(log(t)/(b + 1))']`

```text
-(24*b**3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 24*b**3*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 120*b**3*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 48*b**3*g*kappa*z*Derivative(F0(z), z)**5 + 2*b**3*g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 4*b**3*g*z*Derivative(F0(z), (z, 2))**2 - 8*b**3*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 8*b**3*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 24*b**3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*b**3*z*Derivative(F0(z), z)**5 - 36*b**2*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 36*b**2*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 24*b**2*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 132*b**2*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 72*b**2*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 24*b**2*g*kappa*z*Derivative(F0(z), z)**5 + 24*b**2*g*kappa*F0(z)*Derivative(F0(z), z)**4 + 3*b**2*g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 6*b**2*g*z*Derivative(F0(z), (z, 2))**2 - b**2*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + 12*b**2*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*b**2*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 36*b**2*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 2*b**2*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 8*b**2*z*Derivative(F0(z), z)**5 + 18*b*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 18*b*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 24*b*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 42*b*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 6*b*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 6*b*g*kappa*z*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 48*b*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 6*b*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 2*b*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) - 6*b*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 6*b*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 18*b*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - b*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 3*b*z*Derivative(F0(z), z)**5 - b*F0(z)*Derivative(F0(z), z)**4 - 3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 3*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 3*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 6*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 3*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/((b + 1)**3*Derivative(F0(z), z)**3) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-4*b*(b - 1)*(2*b - 1)*(v1 + v2*z)/(b + 1)**3', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*b**3*v1 - 8*b**3*v2*z + 12*b**2*v1 + 12*b**2*v2*z - 4*b*v1 - 4*b*v2*z', 'denominator': 'b**3 + 3*b**2 + 3*b + 1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't*(b + 1) != 0', 'local flow chart; logarithm arguments positive when used', '(s*(2*b - 1)*exp(2*b*log(t)/(b + 1))*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp((2*b - 1)*log(t)/(b + 1))) + F0(s*exp((2*b - 1)*log(t)/(b + 1)))*exp(log(t)/(b + 1)))/(t*(b + 1)) > 0', 'exp(2*b*log(t)/(b + 1))*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp((2*b - 1)*log(t)/(b + 1))) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*z*(12*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 24*g*kappa*Derivative(F0(z), z)**5 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - 4*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 12*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*Derivative(F0(z), z)**5)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+-1A

Generator: `['-1', '3*s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp(3*t))*exp(-t)']`

```text
-(81*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 81*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 54*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 297*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 126*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 72*g*kappa*z*Derivative(F0(z), z)**5 + 9*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**4 + 3*g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 6*g*z*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) - 27*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 27*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 81*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 3*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 15*z*Derivative(F0(z), z)**5 - F0(z)*Derivative(F0(z), z)**4)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-24*v1 - 24*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-24*v1 - 24*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '-1 != 0', 'local flow chart; logarithm arguments positive when used', '(3*s*exp(3*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(3*t)) - F0(s*exp(3*t)))*exp(-t) > 0', 'exp(2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(3*t)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+0A

Generator: `['0', '3*s', 'phi']`

Status: **verified**.

Graph: `['s**(1/3)*F0(t)']`

```text
-(6*g*kappa*F0(z)*Derivative(F0(z), z)**3 + 6*g*Derivative(F0(z), z) - F0(z)**3*Derivative(F0(z), (z, 3)) - F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)))/(3*F0(z)**2) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '4*g*kappa*v1*(3*v0*v2 - v1**2)/v0**2', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '12*g*kappa*v0*v1*v2 - 4*g*kappa*v1**3', 'denominator': 'v0**2', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*s != 0', 'local flow chart; logarithm arguments positive when used', 's**(1/3)*Derivative(F0(t), t) > 0', 'F0(t)/(3*s**(2/3)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+1A

Generator: `['1', '3*s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp(-3*t))*exp(t)']`

```text
(81*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 81*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 54*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 297*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 126*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 72*g*kappa*z*Derivative(F0(z), z)**5 + 9*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**4 + 3*g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 6*g*z*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) - 27*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 27*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 81*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 3*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 15*z*Derivative(F0(z), z)**5 - F0(z)*Derivative(F0(z), z)**4)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '24*v1 + 24*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '24*v1 + 24*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-3*s*exp(-2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(-3*t)) + F0(s*exp(-3*t))*exp(t) > 0', 'exp(-2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(-3*t)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+-1A

Generator: `['3*t/2', '-1', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s + 2*log(t)/3)']`

```text
-2*(12*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 12*g*kappa*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 24*g*kappa*F0(z)*Derivative(F0(z), z)**4 + 48*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 24*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 24*g*kappa*Derivative(F0(z), z)**5 + 48*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 12*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 9*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + 9*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 18*g*Derivative(F0(z), (z, 2))**2 - 2*F0(z)*Derivative(F0(z), z)**4 + 2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 4*Derivative(F0(z), z)**5 - 4*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/(27*Derivative(F0(z), z)**3) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '8*v2/27', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '8*v2', 'denominator': '27', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*(F0(s + 2*log(t)/3) + Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + 2*log(t)/3))/(3*t**(1/3)) > 0', 't**(2/3)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + 2*log(t)/3) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+0A

Generator: `['3*t/2', '0', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s)']`

```text
2*(-24*g*kappa*F0(z)*Derivative(F0(z), z)**3 + 9*g*Derivative(F0(z), (z, 2)) + 2*F0(z)*Derivative(F0(z), z)**3)/(27*Derivative(F0(z), z)**2) = 0
```

First integral: `{'status': 'verified', 'flux': '-2*g/(3*Derivative(F0(z), z)) + (-8*g*kappa/9 + 2/27)*F0(z)**2', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*F0(s)/(3*t**(1/3)) > 0', 't**(2/3)*Derivative(F0(s), s) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+1A

Generator: `['3*t/2', '1', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s - 2*log(t)/3)']`

```text
2*(12*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 12*g*kappa*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 24*g*kappa*F0(z)*Derivative(F0(z), z)**4 + 48*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 24*g*kappa*Derivative(F0(z), z)**5 - 48*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 12*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 9*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + 9*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 18*g*Derivative(F0(z), (z, 2))**2 + 2*F0(z)*Derivative(F0(z), z)**4 + 2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 4*Derivative(F0(z), z)**5 - 4*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/(27*Derivative(F0(z), z)**3) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v2/27', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v2', 'denominator': '27', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*(F0(s - 2*log(t)/3) - Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - 2*log(t)/3))/(3*t**(1/3)) > 0', 't**(2/3)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - 2*log(t)/3) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+-1A

Generator: `['t', '-2*s', '-1']`

Status: **verified**.

Graph: `['F0(s*t**2) - log(t)']`

```text
-2*(12*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 12*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 24*g*kappa*z*Derivative(F0(z), z)**5 - 36*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 3*g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*g*kappa*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 12*g*kappa*Derivative(F0(z), z)**4 + 3*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*z*Derivative(F0(z), (z, 2))**2 - 4*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 12*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*z*Derivative(F0(z), z)**5 - z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) - 1/t > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+0A

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*z*(12*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 24*g*kappa*Derivative(F0(z), z)**5 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - 4*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 12*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*Derivative(F0(z), z)**5)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+1A

Generator: `['t', '-2*s', '1']`

Status: **verified**.

Graph: `['F0(s*t**2) + log(t)']`

```text
-2*(12*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 12*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 24*g*kappa*z*Derivative(F0(z), z)**5 + 36*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 3*g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*g*kappa*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 12*g*kappa*Derivative(F0(z), z)**4 + 3*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*z*Derivative(F0(z), (z, 2))**2 - 4*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 12*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*z*Derivative(F0(z), z)**5 + z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) + 1/t > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0,), (1,))

Generator: `['1', '0', '0']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['F0(s)']`

### B.cubic.translation.((1,), (1,))

Generator: `['0', '1', '0']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['F0(t)']`

### B.cubic.translation.((2,), (1,))

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### B.cubic.translation.((0, 1), (1, -1))

Generator: `['1', '-1', '0']`

Status: **verified**.

Graph: `['F0(s + t)']`

```text
-(3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(3*g*kappa*Derivative(F0(z), z)**4 + g*Derivative(F0(z), z) - Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1), (1, 1))

Generator: `['1', '1', '0']`

Status: **verified**.

Graph: `['F0(s - t)']`

```text
(3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*g*kappa*Derivative(F0(z), z)**4 + g*Derivative(F0(z), z) - Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 2), (1, -1))

Generator: `['1', '0', '-1']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['-t + F0(s)']`

### B.cubic.translation.((0, 2), (1, 1))

Generator: `['1', '0', '1']`

Status: **verified**.

Graph: `['t + F0(s)']`

```text
0 = 0
```

First integral: `{'status': 'not_found', 'reason': 'no derivative'}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '1 > 0', 'Derivative(F0(s), s) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((1, 2), (1, -1))

Generator: `['0', '1', '-1']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['-s + F0(t)']`

### B.cubic.translation.((1, 2), (1, 1))

Generator: `['0', '1', '1']`

Status: **verified**.

Graph: `['s + F0(t)']`

```text
Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', '1 > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, -1, delta))

Generator: `['1', '-1', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(s + t)']`

```text
-(3*delta**2*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*delta**2*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 6*delta*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(3*delta**2*g*kappa*Derivative(F0(z), z)**2 + 6*delta*g*kappa*Derivative(F0(z), z)**3 + 3*g*kappa*Derivative(F0(z), z)**4 + g*Derivative(F0(z), z) - Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'delta + Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, 1, delta))

Generator: `['1', '1', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(s - t)']`

```text
(3*delta**2*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*delta**2*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 6*delta*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*delta**2*g*kappa*Derivative(F0(z), z)**2 - 6*delta*g*kappa*Derivative(F0(z), z)**3 + 3*g*kappa*Derivative(F0(z), z)**4 + g*Derivative(F0(z), z) - Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'delta - Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.cubic

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*z*(12*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 24*g*kappa*Derivative(F0(z), z)**5 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2 - 4*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 12*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*Derivative(F0(z), z)**5)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
(3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 3*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - 6*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 3*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*z*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) - z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*g*kappa*z**3*Derivative(F0(z), z)**4 - 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**3 + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2 + g*z*Derivative(F0(z), z) - z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
c*(3*c**2*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*c**2*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 - 6*c*g*gamma*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 3*g*gamma**2*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) - 3*g*gamma**2*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': 'c*(3*c**2*g*kappa*Derivative(F0(z), z)**4 - c**2*Derivative(F0(z), z)**4 - 6*c*g*gamma*kappa*Derivative(F0(z), z)**3 + 3*g*gamma**2*kappa*Derivative(F0(z), z)**2 + g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## P, m=4

Discovery: completed.

### B.generic.scaling

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(4*g*kappa*z**4*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 8*g*kappa*z**4*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 4*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 12*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 4*g*kappa*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*g*kappa*z**4*Derivative(F0(z), z)**5 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4 + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**3 - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+deltaZ

Generator: `['1', 'c', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(-c*t + s)']`

```text
-c*(4*c**3*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 8*c**3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 12*c**2*delta*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*c**2*delta*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 12*c*delta**2*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 4*delta**3*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 4*delta**3*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(4*c**3*g*kappa*Derivative(F0(z), z)**5 - 12*c**2*delta*g*kappa*Derivative(F0(z), z)**4 + c**2*Derivative(F0(z), z)**4 + 12*c*delta**2*g*kappa*Derivative(F0(z), z)**3 - 4*delta**3*g*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + delta > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(4*g*kappa*z**4*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 8*g*kappa*z**4*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 4*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 + 12*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 4*g*kappa*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*z*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*z*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)) + z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 3*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*g*kappa*z**4*Derivative(F0(z), z)**5 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4 + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**3 - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2 - g*z*Derivative(F0(z), z) + z**3*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-c*(4*c**3*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 8*c**3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 12*c**2*g*gamma*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*c**2*g*gamma*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + c**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2))**2 + 12*c*g*gamma**2*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 4*g*gamma**3*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 3)) + 4*g*gamma**3*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 2*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**3 = 0
```

First integral: `{'status': 'verified', 'flux': '-c*(4*c**3*g*kappa*Derivative(F0(z), z)**5 - 12*c**2*g*gamma*kappa*Derivative(F0(z), z)**4 + c**2*Derivative(F0(z), z)**4 + 12*c*g*gamma**2*kappa*Derivative(F0(z), z)**3 - 4*g*gamma**3*kappa*Derivative(F0(z), z)**2 - g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## M, m=1

Discovery: completed.

### B.generic.scaling

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(-g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(-g*kappa*z*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+deltaZ

Generator: `['1', 'c', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(-c*t + s)']`

```text
-(c**2*delta*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - c*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + c*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - delta*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*delta*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(c**2*delta*Derivative(F0(z), z)**4 - c*g*kappa*Derivative(F0(z), z)**3 - delta*g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + delta > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(-g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(-g*kappa*z*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-(c**2*gamma*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - c*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + c*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - g*gamma*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*gamma*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(c**2*gamma*Derivative(F0(z), z)**4 - c*g*kappa*Derivative(F0(z), z)**3 - g*gamma*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## M, m=2

Discovery: completed.

### B.generic.scaling

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(2*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 2*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(2*g*kappa*z**2*Derivative(F0(z), z)**4 - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+deltaZ

Generator: `['1', 'c', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(-c*t + s)']`

```text
-(c**2*delta*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 2*c**2*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 2*c*delta*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 2*c*delta*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - delta*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*delta*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(c**2*delta*Derivative(F0(z), z)**4 + 2*c**2*g*kappa*Derivative(F0(z), z)**4 - 2*c*delta*g*kappa*Derivative(F0(z), z)**3 - delta*g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + delta > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(2*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 2*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 2*g*kappa*F0(z)*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(2*g*kappa*z**2*Derivative(F0(z), z)**4 - 2*g*kappa*z*F0(z)*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-(2*c**2*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*gamma*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 2*c*g*gamma*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 2*c*g*gamma*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - g*gamma*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*gamma*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(2*c**2*g*kappa*Derivative(F0(z), z)**4 + c**2*gamma*Derivative(F0(z), z)**4 - 2*c*g*gamma*kappa*Derivative(F0(z), z)**3 - g*gamma*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## M, m=3

Discovery: completed.

### B.cubic.D+bC

Generator: `['b*t + t', '-2*b*s + s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp((2*b - 1)*log(t)/(b + 1)))*exp(log(t)/(b + 1))']`

```text
-(24*b**3*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 24*b**3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 120*b**3*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 48*b**3*g*kappa*z*Derivative(F0(z), z)**6 - 2*b**3*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + 8*b**3*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 4*b**3*z*Derivative(F0(z), z)**6 - 36*b**2*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 36*b**2*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 24*b**2*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 132*b**2*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 72*b**2*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 24*b**2*g*kappa*z*Derivative(F0(z), z)**6 + 24*b**2*g*kappa*F0(z)*Derivative(F0(z), z)**5 - b**2*g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*b**2*g*F0(z)*Derivative(F0(z), (z, 2))**2 - 5*b**2*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + 4*b**2*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*b**2*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 10*b**2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 18*b*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 18*b*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 24*b*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 42*b*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 6*b*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 6*b*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 48*b*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 6*b*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 2*b*g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 6*b*g*F0(z)*Derivative(F0(z), (z, 2))**2 - 4*b*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 4*b*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 2*b*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 9*b*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - b*z*Derivative(F0(z), z)**6 - 3*b*F0(z)*Derivative(F0(z), z)**5 - 3*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 3*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 6*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 3*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/((b + 1)**3*Derivative(F0(z), z)**4) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-4*b*(b - 1)*(2*b - 1)*(v1 + v2*z)/(b + 1)**3', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*b**3*v1 - 8*b**3*v2*z + 12*b**2*v1 + 12*b**2*v2*z - 4*b*v1 - 4*b*v2*z', 'denominator': 'b**3 + 3*b**2 + 3*b + 1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't*(b + 1) != 0', 'local flow chart; logarithm arguments positive when used', '(s*(2*b - 1)*exp(2*b*log(t)/(b + 1))*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp((2*b - 1)*log(t)/(b + 1))) + F0(s*exp((2*b - 1)*log(t)/(b + 1)))*exp(log(t)/(b + 1)))/(t*(b + 1)) > 0', 'exp(2*b*log(t)/(b + 1))*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp((2*b - 1)*log(t)/(b + 1))) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*(12*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 24*g*kappa*z*Derivative(F0(z), z)**4 - g*Derivative(F0(z), (z, 2)) + 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 2*z*Derivative(F0(z), z)**4)/Derivative(F0(z), z)**2 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+-1A

Generator: `['-1', '3*s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp(3*t))*exp(-t)']`

```text
-(81*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 81*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 54*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 297*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 126*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 72*g*kappa*z*Derivative(F0(z), z)**6 + 9*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**5 + g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 9*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 9*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 21*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 3*z*Derivative(F0(z), z)**6 - 3*F0(z)*Derivative(F0(z), z)**5)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-24*v1 - 24*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-24*v1 - 24*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '-1 != 0', 'local flow chart; logarithm arguments positive when used', '(3*s*exp(3*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(3*t)) - F0(s*exp(3*t)))*exp(-t) > 0', 'exp(2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(3*t)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+0A

Generator: `['0', '3*s', 'phi']`

Status: **verified**.

Graph: `['s**(1/3)*F0(t)']`

```text
-(6*g*kappa*F0(z)*Derivative(F0(z), z)**3 + 18*g*Derivative(F0(z), z) - F0(z)**3*Derivative(F0(z), (z, 3)) + F0(z)**2*Derivative(F0(z), z)*Derivative(F0(z), (z, 2)))/(3*F0(z)**2) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '4*g*kappa*v1*(3*v0*v2 - v1**2)/v0**2', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '12*g*kappa*v0*v1*v2 - 4*g*kappa*v1**3', 'denominator': 'v0**2', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*s != 0', 'local flow chart; logarithm arguments positive when used', 's**(1/3)*Derivative(F0(t), t) > 0', 'F0(t)/(3*s**(2/3)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+1A

Generator: `['1', '3*s', 'phi']`

Status: **verified**.

Graph: `['F0(s*exp(-3*t))*exp(t)']`

```text
(81*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 81*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 54*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 297*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 9*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 126*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 72*g*kappa*z*Derivative(F0(z), z)**6 + 9*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**5 + g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 9*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 9*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 21*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 3*z*Derivative(F0(z), z)**6 - 3*F0(z)*Derivative(F0(z), z)**5)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '24*v1 + 24*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '24*v1 + 24*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-3*s*exp(-2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(-3*t)) + F0(s*exp(-3*t))*exp(t) > 0', 'exp(-2*t)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*exp(-3*t)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+-1A

Generator: `['3*t/2', '-1', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s + 2*log(t)/3)']`

```text
-2*(12*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 12*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 24*g*kappa*F0(z)*Derivative(F0(z), z)**5 + 48*g*kappa*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 24*g*kappa*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 24*g*kappa*Derivative(F0(z), z)**6 + 48*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 12*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 12*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 9*g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 27*g*F0(z)*Derivative(F0(z), (z, 2))**2 - 18*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 6*F0(z)*Derivative(F0(z), z)**5 + 2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 4*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 4*Derivative(F0(z), z)**6 + 8*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)))/(27*Derivative(F0(z), z)**4) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '8*v2/27', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '8*v2', 'denominator': '27', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*(F0(s + 2*log(t)/3) + Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + 2*log(t)/3))/(3*t**(1/3)) > 0', 't**(2/3)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + 2*log(t)/3) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+0A

Generator: `['3*t/2', '0', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s)']`

```text
-2*(8*g*kappa*F0(z)*Derivative(F0(z), z)**5 - 3*g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 9*g*F0(z)*Derivative(F0(z), (z, 2))**2 - 6*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - 2*F0(z)*Derivative(F0(z), z)**5)/(9*Derivative(F0(z), z)**4) = 0
```

First integral: `{'status': 'verified', 'flux': '2*g*F0(z)*Derivative(F0(z), (z, 2))/(3*Derivative(F0(z), z)**3) - 2*g/(3*Derivative(F0(z), z)) + (-8*g*kappa/9 + 2/9)*F0(z)**2', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*F0(s)/(3*t**(1/3)) > 0', 't**(2/3)*Derivative(F0(s), s) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+1/2C+1A

Generator: `['3*t/2', '1', 'phi']`

Status: **verified**.

Graph: `['t**(2/3)*F0(s - 2*log(t)/3)']`

```text
2*(12*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 12*g*kappa*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 24*g*kappa*F0(z)*Derivative(F0(z), z)**5 + 48*g*kappa*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 24*g*kappa*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 24*g*kappa*Derivative(F0(z), z)**6 - 48*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 12*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 12*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 9*g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 27*g*F0(z)*Derivative(F0(z), (z, 2))**2 + 18*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + 6*F0(z)*Derivative(F0(z), z)**5 + 2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 4*Derivative(F0(z), z)**6 - 8*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)))/(27*Derivative(F0(z), z)**4) = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v2/27', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v2', 'denominator': '27', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '3*t/2 != 0', 'local flow chart; logarithm arguments positive when used', '2*(F0(s - 2*log(t)/3) - Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - 2*log(t)/3))/(3*t**(1/3)) > 0', 't**(2/3)*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - 2*log(t)/3) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+-1A

Generator: `['t', '-2*s', '-1']`

Status: **verified**.

Graph: `['F0(s*t**2) - log(t)']`

```text
-(24*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 24*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 120*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 24*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 48*g*kappa*z*Derivative(F0(z), z)**6 - 72*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 6*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 6*g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 24*g*kappa*Derivative(F0(z), z)**5 + 6*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 2*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*g*Derivative(F0(z), (z, 2))**2 + 8*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 4*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 4*z*Derivative(F0(z), z)**6 - 10*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) - 1/t > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+0A

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*(12*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 24*g*kappa*z*Derivative(F0(z), z)**4 - g*Derivative(F0(z), (z, 2)) + 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 2*z*Derivative(F0(z), z)**4)/Derivative(F0(z), z)**2 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+1A

Generator: `['t', '-2*s', '1']`

Status: **verified**.

Graph: `['F0(s*t**2) + log(t)']`

```text
-(24*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 24*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 120*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 24*g*kappa*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 48*g*kappa*z*Derivative(F0(z), z)**6 + 72*g*kappa*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 6*g*kappa*z*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 6*g*kappa*z*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 24*g*kappa*Derivative(F0(z), z)**5 + 6*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - 2*g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*Derivative(F0(z), (z, 2))**2 + 8*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 4*z**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 4*z*Derivative(F0(z), z)**6 + 10*z*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) + 1/t > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0,), (1,))

Generator: `['1', '0', '0']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['F0(s)']`

### B.cubic.translation.((1,), (1,))

Generator: `['0', '1', '0']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['F0(t)']`

### B.cubic.translation.((2,), (1,))

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### B.cubic.translation.((0, 1), (1, -1))

Generator: `['1', '-1', '0']`

Status: **verified**.

Graph: `['F0(s + t)']`

```text
-3*g*kappa*(Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + Derivative(F0(z), (z, 2))**2) = 0
```

First integral: `{'status': 'verified', 'flux': '-3*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1), (1, 1))

Generator: `['1', '1', '0']`

Status: **verified**.

Graph: `['F0(s - t)']`

```text
3*g*kappa*(Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + Derivative(F0(z), (z, 2))**2) = 0
```

First integral: `{'status': 'verified', 'flux': '3*g*kappa*Derivative(F0(z), z)*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 2), (1, -1))

Generator: `['1', '0', '-1']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['-t + F0(s)']`

### B.cubic.translation.((0, 2), (1, 1))

Generator: `['1', '0', '1']`

Status: **verified**.

Graph: `['t + F0(s)']`

```text
-g*(-Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': 'g*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**3', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '1 > 0', 'Derivative(F0(s), s) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((1, 2), (1, -1))

Generator: `['0', '1', '-1']`

Status: **chart-incompatible**.

a declared strictly positive quantity is identically nonpositive on this graph

Graph: `['-s + F0(t)']`

### B.cubic.translation.((1, 2), (1, 1))

Generator: `['0', '1', '1']`

Status: **verified**.

Graph: `['s + F0(t)']`

```text
Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', '1 > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, -1, delta))

Generator: `['1', '-1', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(s + t)']`

```text
-(3*delta**2*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 3*delta**2*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 6*delta*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - delta*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*delta*g*Derivative(F0(z), (z, 2))**2 + delta*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(3*delta**2*g*kappa*Derivative(F0(z), z)**3 + 6*delta*g*kappa*Derivative(F0(z), z)**4 - delta*g*Derivative(F0(z), z) + delta*Derivative(F0(z), z)**4 + 3*g*kappa*Derivative(F0(z), z)**5)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'delta + Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s + t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, 1, delta))

Generator: `['1', '1', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(s - t)']`

```text
(3*delta**2*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 3*delta**2*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 6*delta*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + delta*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*delta*g*Derivative(F0(z), (z, 2))**2 - delta*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*delta**2*g*kappa*Derivative(F0(z), z)**3 - 6*delta*g*kappa*Derivative(F0(z), z)**4 + delta*g*Derivative(F0(z), z) - delta*Derivative(F0(z), z)**4 + 3*g*kappa*Derivative(F0(z), z)**5)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'delta - Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s - t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.cubic

Generator: `['t', '-2*s', '0']`

Status: **verified**.

Graph: `['F0(s*t**2)']`

```text
-2*(12*g*kappa*z**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 12*g*kappa*z**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 60*g*kappa*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 24*g*kappa*z*Derivative(F0(z), z)**4 - g*Derivative(F0(z), (z, 2)) + 4*z**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + 2*z*Derivative(F0(z), z)**4)/Derivative(F0(z), z)**2 = 0
```

First integral: `{'status': 'not_total_derivative', 'euler_operator': '-8*v1 - 8*v2*z', 'evidence': {'status': 'proved_not_identically_zero', 'numerator': '-8*v1 - 8*v2*z', 'denominator': '1', 'method': 'nonzero polynomial over algebraic numbers'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '2*s*t*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 't**2*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s*t**2) > 0', 'g > 0', 'kappa > 0']`

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
(3*g*kappa*z**3*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 3*g*kappa*z**3*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*g*kappa*z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - 6*g*kappa*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) + 3*g*kappa*F0(z)**2*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) + g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 + g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) - z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*g*kappa*z**3*Derivative(F0(z), z)**5 - 6*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**4 + 3*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**3 + g*F0(z)*Derivative(F0(z), z) - z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
(3*c**3*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) + 3*c**3*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 - 6*c**2*g*gamma*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - c**2*gamma*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + 3*c*g*gamma**2*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) - 3*c*g*gamma**2*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + g*gamma*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) - 3*g*gamma*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '(3*c**3*g*kappa*Derivative(F0(z), z)**5 - 6*c**2*g*gamma*kappa*Derivative(F0(z), z)**4 - c**2*gamma*Derivative(F0(z), z)**4 + 3*c*g*gamma**2*kappa*Derivative(F0(z), z)**3 + g*gamma*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## M, m=4

Discovery: completed.

### B.generic.scaling

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(4*g*kappa*z**4*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 3)) + 8*g*kappa*z**4*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2))**2 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 4*g*kappa*z**3*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 2)) + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 12*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*g*kappa*F0(z)**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*g*kappa*z**4*Derivative(F0(z), z)**6 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**5 + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**4 - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+deltaZ

Generator: `['1', 'c', 'delta']`

Status: **verified**.

Graph: `['delta*t + F0(-c*t + s)']`

```text
-(4*c**4*g*kappa*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 3)) + 8*c**4*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2))**2 - 12*c**3*delta*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 12*c**3*delta*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 12*c**2*delta**2*g*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*delta*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*c*delta**3*g*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 4*c*delta**3*g*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - delta*g*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*delta*g*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*c**4*g*kappa*Derivative(F0(z), z)**6 - 12*c**3*delta*g*kappa*Derivative(F0(z), z)**5 + 12*c**2*delta**2*g*kappa*Derivative(F0(z), z)**4 + c**2*delta*Derivative(F0(z), z)**4 - 4*c*delta**3*g*kappa*Derivative(F0(z), z)**3 - delta*g*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + delta > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+deltaZ

Generator: `['0', '1', 'delta']`

Status: **verified**.

Graph: `['delta*s + F0(t)']`

```text
delta*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'delta*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'delta > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.Y4

Generator: `['t', 's', 'phi']`

Status: **verified**.

Graph: `['t*F0(s/t)']`

```text
-(4*g*kappa*z**4*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 3)) + 8*g*kappa*z**4*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2))**2 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 4*g*kappa*z**3*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 2)) + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 12*g*kappa*z**2*F0(z)*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 + 12*g*kappa*z*F0(z)**2*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)) - 4*g*kappa*F0(z)**3*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 2)) - g*F0(z)*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*F0(z)*Derivative(F0(z), (z, 2))**2 - g*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2)) + z**2*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + z**2*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2)) + 2*z*F0(z)*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2)))/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*g*kappa*z**4*Derivative(F0(z), z)**6 - 12*g*kappa*z**3*F0(z)*Derivative(F0(z), z)**5 + 12*g*kappa*z**2*F0(z)**2*Derivative(F0(z), z)**4 - 4*g*kappa*z*F0(z)**3*Derivative(F0(z), z)**3 - g*F0(z)*Derivative(F0(z), z) + z**2*F0(z)*Derivative(F0(z), z)**4)*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', 't != 0', 'local flow chart; logarithm arguments positive when used', '-s*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t)/t + F0(s/t) > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, s/t) > 0', 'g > 0', 'kappa > 0']`

### table3.2.tilted

Generator: `['1', 'c', 'gamma']`

Status: **verified**.

Graph: `['gamma*t + F0(-c*t + s)']`

```text
-(4*c**4*g*kappa*Derivative(F0(z), z)**6*Derivative(F0(z), (z, 3)) + 8*c**4*g*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 2))**2 - 12*c**3*g*gamma*kappa*Derivative(F0(z), z)**5*Derivative(F0(z), (z, 3)) - 12*c**3*g*gamma*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 2))**2 + 12*c**2*g*gamma**2*kappa*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) + c**2*gamma*Derivative(F0(z), z)**4*Derivative(F0(z), (z, 3)) - 4*c*g*gamma**3*kappa*Derivative(F0(z), z)**3*Derivative(F0(z), (z, 3)) + 4*c*g*gamma**3*kappa*Derivative(F0(z), z)**2*Derivative(F0(z), (z, 2))**2 - g*gamma*Derivative(F0(z), z)*Derivative(F0(z), (z, 3)) + 3*g*gamma*Derivative(F0(z), (z, 2))**2)/Derivative(F0(z), z)**4 = 0
```

First integral: `{'status': 'verified', 'flux': '-(4*c**4*g*kappa*Derivative(F0(z), z)**6 - 12*c**3*g*gamma*kappa*Derivative(F0(z), z)**5 + 12*c**2*g*gamma**2*kappa*Derivative(F0(z), z)**4 + c**2*gamma*Derivative(F0(z), z)**4 - 4*c*g*gamma**3*kappa*Derivative(F0(z), z)**3 - g*gamma*Derivative(F0(z), z))*Derivative(F0(z), (z, 2))/Derivative(F0(z), z)**4', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', '-c*Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) + gamma > 0', 'Subs(Derivative(F0(_xi_1), _xi_1), _xi_1, -c*t + s) > 0', 'g > 0', 'kappa > 0']`

### table3.2.spatial

Generator: `['0', '1', 'gamma']`

Status: **verified**.

Graph: `['gamma*s + F0(t)']`

```text
gamma*Derivative(F0(z), (z, 3)) = 0
```

First integral: `{'status': 'verified', 'flux': 'gamma*Derivative(F0(z), (z, 2))', 'identity_remainder': 0, 'constant': 'I0', 'euler_evidence': {'status': 'proved_zero', 'method': 'exact rational/algebraic numerator normalization', 'domain': 'where the original expression is defined'}}`

Conditions: `['phi_t>0', 'phi_s>0', 'g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'Derivative(F0(t), t) > 0', 'gamma > 0', 'g > 0', 'kappa > 0']`

### table3.2.vertical

Generator: `['0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

## E1, m=1

Discovery: completed.

### B.generic.scaling

Generator: `['t', 'x', '0', '0', 'delta']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'delta*log(t) + F2(x/t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
delta + kappa*Derivative(F1(z), z) - z*Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+-1Z

Generator: `['1', 'c', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', '-t + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + kappa*Derivative(F1(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+-1Z

Generator: `['0', '1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', '-x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
-g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+0Z

Generator: `['1', 'c', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 'F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + kappa*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+0Z

Generator: `['0', '1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+1Z

Generator: `['1', 'c', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 't + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + kappa*Derivative(F1(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+1Z

Generator: `['0', '1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.bed_drift

Generator: `['1', '0', '0', '0', 'alpha']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 'alpha*t + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
alpha + kappa*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=1', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

## E1, m=2

Discovery: completed.

### B.generic.scaling

Generator: `['t', 'x', '0', '0', 'delta']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'delta*log(t) + F2(x/t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
delta + 2*kappa*F1(z)*Derivative(F1(z), z) - z*Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+-1Z

Generator: `['1', 'c', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', '-t + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 2*kappa*F1(z)*Derivative(F1(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+-1Z

Generator: `['0', '1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', '-x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
-g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+0Z

Generator: `['1', 'c', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 'F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 2*kappa*F1(z)*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+0Z

Generator: `['0', '1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+1Z

Generator: `['1', 'c', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 't + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 2*kappa*F1(z)*Derivative(F1(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+1Z

Generator: `['0', '1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.bed_drift

Generator: `['1', '0', '0', '0', 'alpha']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 'alpha*t + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
alpha + 2*kappa*F1(z)*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=2', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

## E1, m=3

Discovery: completed.

### B.cubic.D+bC

Generator: `['b*t + t', 'x', '-2*b*h', '-b*u', '-2*B*b']`

Status: **verified**.

Graph: `['F0(x*exp(-log(t)/(b + 1)))*exp(-2*b*log(t)/(b + 1))', 'F1(x*exp(-log(t)/(b + 1)))*exp(-b*log(t)/(b + 1))', 'F2(x*exp(-log(t)/(b + 1)))*exp(-2*b*log(t)/(b + 1))']`

```text
-(-b*F0(z)*Derivative(F1(z), z) + 2*b*F0(z) - b*F1(z)*Derivative(F0(z), z) + z*Derivative(F0(z), z) - F0(z)*Derivative(F1(z), z) - F1(z)*Derivative(F0(z), z))/(b + 1) = 0
```

```text
-(-b*g*Derivative(F0(z), z) - b*g*Derivative(F2(z), z) - b*F1(z)*Derivative(F1(z), z) + b*F1(z) - g*Derivative(F0(z), z) - g*Derivative(F2(z), z) + z*Derivative(F1(z), z) - F1(z)*Derivative(F1(z), z))/(b + 1) = 0
```

```text
-(-3*b*kappa*F1(z)**2*Derivative(F1(z), z) + 2*b*F2(z) - 3*kappa*F1(z)**2*Derivative(F1(z), z) + z*Derivative(F2(z), z))/(b + 1) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't*(b + 1) != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x*exp(-log(t)/(b + 1)))*exp(-2*b*log(t)/(b + 1)) > 0', 'F1(x*exp(-log(t)/(b + 1)))*exp(-b*log(t)/(b + 1)) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C

Generator: `['t', '0', '-2*h', '-u', '-2*B']`

Status: **verified**.

Graph: `['F0(x)/t**2', 'F1(x)/t', 'F2(x)/t**2']`

```text
F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 2*F2(z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x)/t**2 > 0', 'F1(x)/t > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+-1A

Generator: `['-1', 'x', '2*h', 'u', '2*B']`

Status: **verified**.

Graph: `['F0(x*exp(t))*exp(-2*t)', 'F1(x*exp(t))*exp(-t)', 'F2(x*exp(t))*exp(-2*t)']`

```text
z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) + z*Derivative(F2(z), z) - 2*F2(z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '-1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x*exp(t))*exp(-2*t) > 0', 'F1(x*exp(t))*exp(-t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+0A

Generator: `['0', 'x', '2*h', 'u', '2*B']`

Status: **verified**.

Graph: `['x**2*F0(t)', 'x*F1(t)', 'x**2*F2(t)']`

```text
3*F0(z)*F1(z) + Derivative(F0(z), z) = 0
```

```text
2*g*F0(z) + 2*g*F2(z) + F1(z)**2 + Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**3 + Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 'x != 0', 'local flow chart; logarithm arguments positive when used', 'x**2*F0(t) > 0', 'x*F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+-1C+1A

Generator: `['1', 'x', '2*h', 'u', '2*B']`

Status: **verified**.

Graph: `['F0(x*exp(-t))*exp(2*t)', 'F1(x*exp(-t))*exp(t)', 'F2(x*exp(-t))*exp(2*t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + 2*F0(z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) + F1(z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - z*Derivative(F2(z), z) + 2*F2(z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x*exp(-t))*exp(2*t) > 0', 'F1(x*exp(-t))*exp(t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+0C+-1A

Generator: `['t', 'x', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'F2(x/t) - log(t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - z*Derivative(F2(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+0C+0A

Generator: `['t', 'x', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'F2(x/t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - z*Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.D+0C+1A

Generator: `['t', 'x', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'F2(x/t) + log(t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - z*Derivative(F2(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+-1A

Generator: `['t', '-1', '-2*h', '-u', '-2*B']`

Status: **verified**.

Graph: `['F0(x + log(t))/t**2', 'F1(x + log(t))/t', 'F2(x + log(t))/t**2']`

```text
F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) + Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) + Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 2*F2(z) + Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x + log(t))/t**2 > 0', 'F1(x + log(t))/t > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+0A

Generator: `['t', '0', '-2*h', '-u', '-2*B']`

Status: **verified**.

Graph: `['F0(x)/t**2', 'F1(x)/t', 'F2(x)/t**2']`

```text
F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 2*F2(z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x)/t**2 > 0', 'F1(x)/t > 0', 'g > 0', 'kappa > 0']`

### B.cubic.C+1A

Generator: `['t', '1', '-2*h', '-u', '-2*B']`

Status: **verified**.

Graph: `['F0(x - log(t))/t**2', 'F1(x - log(t))/t', 'F2(x - log(t))/t**2']`

```text
F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) - Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) - Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 2*F2(z) - Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x - log(t))/t**2 > 0', 'F1(x - log(t))/t > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0,), (1,))

Generator: `['1', '0', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 'F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((1,), (1,))

Generator: `['0', '1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((2,), (1,))

Generator: `['0', '0', '0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### B.cubic.translation.((0, 1), (1, -1))

Generator: `['1', '-1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(t + x)', 'F1(t + x)', 'F2(t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) + Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) + Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) + Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t + x) > 0', 'F1(t + x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1), (1, 1))

Generator: `['1', '1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(-t + x)', 'F1(-t + x)', 'F2(-t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) - Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-t + x) > 0', 'F1(-t + x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 2), (1, -1))

Generator: `['1', '0', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', '-t + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 2), (1, 1))

Generator: `['1', '0', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 't + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((1, 2), (1, -1))

Generator: `['0', '1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', '-x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
-g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((1, 2), (1, 1))

Generator: `['0', '1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, -1, -1))

Generator: `['1', '-1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(t + x)', 'F1(t + x)', '-t + F2(t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) + Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) + Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) + Derivative(F2(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t + x) > 0', 'F1(t + x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, -1, 1))

Generator: `['1', '-1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(t + x)', 'F1(t + x)', 't + F2(t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) + Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) + Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) + Derivative(F2(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t + x) > 0', 'F1(t + x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, 1, -1))

Generator: `['1', '1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(-t + x)', 'F1(-t + x)', '-t + F2(-t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) - Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - Derivative(F2(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-t + x) > 0', 'F1(-t + x) > 0', 'g > 0', 'kappa > 0']`

### B.cubic.translation.((0, 1, 2), (1, 1, 1))

Generator: `['1', '1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(-t + x)', 'F1(-t + x)', 't + F2(-t + x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) - Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - Derivative(F1(z), z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - Derivative(F2(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-t + x) > 0', 'F1(-t + x) > 0', 'g > 0', 'kappa > 0']`

### table3.2.cubic

Generator: `['t', '0', '-2*h', '-u', '-2*B']`

Status: **verified**.

Graph: `['F0(x)/t**2', 'F1(x)/t', 'F2(x)/t**2']`

```text
F0(z)*Derivative(F1(z), z) - 2*F0(z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) - F1(z) = 0
```

```text
3*kappa*F1(z)**2*Derivative(F1(z), z) - 2*F2(z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x)/t**2 > 0', 'F1(x)/t > 0', 'g > 0', 'kappa > 0']`

### table3.2.bed_drift

Generator: `['1', '0', '0', '0', 'alpha']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 'alpha*t + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
alpha + 3*kappa*F1(z)**2*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=3', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

## E1, m=4

Discovery: completed.

### B.generic.scaling

Generator: `['t', 'x', '0', '0', 'delta']`

Status: **verified**.

Graph: `['F0(x/t)', 'F1(x/t)', 'delta*log(t) + F2(x/t)']`

```text
-z*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) - z*Derivative(F1(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
delta + 4*kappa*F1(z)**3*Derivative(F1(z), z) - z*Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', 't != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x/t) > 0', 'F1(x/t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+-1Z

Generator: `['1', 'c', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', '-t + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 4*kappa*F1(z)**3*Derivative(F1(z), z) - 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+-1Z

Generator: `['0', '1', '0', '0', '-1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', '-x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
-g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+0Z

Generator: `['1', 'c', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 'F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 4*kappa*F1(z)**3*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+0Z

Generator: `['0', '1', '0', '0', '0']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.T+cS+1Z

Generator: `['1', 'c', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(-c*t + x)', 'F1(-c*t + x)', 't + F2(-c*t + x)']`

```text
-c*Derivative(F0(z), z) + F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
-c*Derivative(F1(z), z) + g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
-c*Derivative(F2(z), z) + 4*kappa*F1(z)**3*Derivative(F1(z), z) + 1 = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(-c*t + x) > 0', 'F1(-c*t + x) > 0', 'g > 0', 'kappa > 0']`

### B.generic.S+1Z

Generator: `['0', '1', '0', '0', '1']`

Status: **verified**.

Graph: `['F0(t)', 'F1(t)', 'x + F2(t)']`

```text
Derivative(F0(z), z) = 0
```

```text
g + Derivative(F1(z), z) = 0
```

```text
Derivative(F2(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(t) > 0', 'F1(t) > 0', 'g > 0', 'kappa > 0']`

### B.generic.Z

Generator: `['0', '0', '0', '0', '1']`

Status: **no invariant graph**.

fixed-locus constraint cannot vanish on declared chart

### table3.2.bed_drift

Generator: `['1', '0', '0', '0', 'alpha']`

Status: **verified**.

Graph: `['F0(x)', 'F1(x)', 'alpha*t + F2(x)']`

```text
F0(z)*Derivative(F1(z), z) + F1(z)*Derivative(F0(z), z) = 0
```

```text
g*Derivative(F0(z), z) + g*Derivative(F2(z), z) + F1(z)*Derivative(F1(z), z) = 0
```

```text
alpha + 4*kappa*F1(z)**3*Derivative(F1(z), z) = 0
```

Conditions: `['h,u,g,kappa>0', 'm=4', '1 != 0', 'local flow chart; logarithm arguments positive when used', 'F0(x) > 0', 'F1(x) > 0', 'g > 0', 'kappa > 0']`

## Annular E2 manual rank-two section

```text
{'status': 'completed', 'reason': None, 'wall_seconds': 0.3465600280323997, 'cpu_seconds': 0.3465435310000018, 'user_cpu_seconds': 0.3465440000000015, 'system_cpu_seconds': 0.0, 'process_peak_rss_bytes': 101920768, 'value': {'reduction': {'model': 'E2', 'status': 'verified', 'reason': '', 'graph': {'z': 'z', 'invariant': 'r', 'profiles': ['H(z)', 'V(z)', 'W(z)', 'Z(z)'], 'lifts': ['H(r)', 'V(r)', 'W(r)', 'c*t + Z(r)'], 'section': {'t': 0, 'theta': 0, 'r': 'z'}, 'conditions': [], 'orbit_coordinates': {}}, 'equations': ['(z*H(z)*Derivative(V(z), z) + z*V(z)*Derivative(H(z), z) + H(z)*V(z))/z', '-(f*z*W(z) - g*z*Derivative(H(z), z) - g*z*Derivative(Z(z), z) - z*V(z)*Derivative(V(z), z) + W(z)**2)/z', '(f*z + z*Derivative(W(z), z) + W(z))*V(z)/z', '(-G*z*V(z)**2*Derivative(Z(z), (z, 2)) - 2*G*z*V(z)*Derivative(V(z), z)*Derivative(Z(z), z) - G*z*W(z)**2*Derivative(Z(z), (z, 2)) - 2*G*z*W(z)*Derivative(W(z), z)*Derivative(Z(z), z) - G*V(z)**2*Derivative(Z(z), z) - G*W(z)**2*Derivative(Z(z), z) + 3*K*z*V(z)**2*Derivative(V(z), z) + 2*K*z*V(z)*W(z)*Derivative(W(z), z) + K*z*W(z)**2*Derivative(V(z), z) + K*V(z)**3 + K*V(z)*W(z)**2 + c*z)/z'], 'weights': [], 'first_integrals': [], 'leading_coefficients': [], 'conditions': ['r>0', 'h>0', 'g,K,G>0'], 'checks': {'base_orbit_rank': 2, 'point_orbit_rank': 2, 'on_shell': True, 'invariant_surface': True, 'pullback': True}, 'scope': 'manual two-dimensional subalgebra; two-dimensional optimal system not computed', 'degree': None}, 'first_integrals': ['z*H(z)*V(z)', 'f*z**2/2 + z*W(z)', 'c*z**2/2 + z*(-G*Derivative(Z(z), z) + K*V(z))*(V(z)**2 + W(z)**2)'], 'flux_identity_remainders': ['0', '0', '0'], 'V': 'C1/(z*H(z))', 'W': 'C2/z - f*z/2', 'P_Z': '(C1*K/(z*H(z)) - (C3/z - c*z/2)/(C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2))/G', 'D': '-C1**2/(z**2*H(z)**2) + g*H(z)', 'N': '(f*(C2/z - f*z/2) + (C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2)/z - g*(C1*K/(z*H(z)) - (C3/z - c*z/2)/(C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2))/G)*H(z)', 'undivided_ode': '(-C1**2/(z**2*H(z)**2) + g*H(z))*Derivative(H(z), z) - (f*(C2/z - f*z/2) + (C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2)/z - g*(C1*K/(z*H(z)) - (C3/z - c*z/2)/(C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2))/G)*H(z)', 'additional_conditions': ['V != 0 for angular integration', 'H>0', 'r>0', 'V**2+W**2>0'], 'singularity_candidates': {'leading_zero': 'Eq(-C1**2/(z**2*H(z)**2) + g*H(z), 0)', 'compatible_critical': ['Eq(-C1**2/(z**2*H(z)**2) + g*H(z), 0)', 'Eq((f*(C2/z - f*z/2) + (C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2)/z - g*(C1*K/(z*H(z)) - (C3/z - c*z/2)/(C1**2/(z**2*H(z)**2) + (C2/z - f*z/2)**2))/G)*H(z), 0)'], 'classification': 'saddle requires an additional desingularized Jacobian check'}, 'task_status': 'critical N3 requires separate BB normal form; regular N/D export forbidden at D=0'}}
```
