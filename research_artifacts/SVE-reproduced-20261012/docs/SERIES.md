# Local series for the corrected similarity equations

## What exists

For each regular row 3.4, 3.5, 3.6, 3.8 and 3.9, the corrected printed-scalar
PDE pullback has the form

```text
E(z,F,P,C,H) = A(z,F,P,C) H + B(z,F,P,C) = 0,
P=F', C=F'', H=F'''.
```

At a jet with `g,kappa>0`, `m>=1`, original velocity `p>0`, original gradient
`q>0`, and `A!=0`, it is a normal-form ODE `F'''=-B/A`. On a sufficiently
small neighborhood of that jet the denominators stay nonzero and positive
real-power arguments stay positive. Hence the first-order vector field
`(F,P,C)'=(P,C,-B/A)` is real analytic. Locally choosing the corresponding
complex branches, the analytic IVP theorem gives a **unique convergent
analytic profile germ** for each such initial triple. This proves local
similarity-solution existence: inserting that germ into its invariant graph
solves the corrected pullback and therefore the printed scalar PDE wherever
the local reconstruction and positive chart remain valid. It supplies no
global continuation, physical-data match, or computable convergence radius.

The analytic-IVP step follows Gerald Teschl, *Ordinary Differential Equations
and Dynamical Systems* (AMS, 2012), Chapter 4, section 4.1, Theorems 4.1 and
4.2, printed pp. 113 ff. The author-hosted, AMS-permitted PDF is at
`https://www.mat.univie.ac.at/~gerald/ftp/book-ode/ode.pdf`; the checked local
copy is `build/series-sources/teschl-ode.pdf` (SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`).
The theorem asserts existence on *some* neighborhood. This package has not
computed its polydisc constants or a radius lower bound.

## Exact recurrence and audit

Set `h=z-z0` and `F_N(h)=sum(a_j*h^j, j=0..N)`, with
`a0=F0`, `a1=P0`, `a2=C0/2`. Given coefficients through `a_(n+2)`, let
`R=-B/A`. The triangular recurrence is

```text
a_(n+3) = [h^n] R(z0+h,F_(n+2),F'_(n+2),F''_(n+2))
          / ((n+3)(n+2)(n+1)),        n=0,...,N-3.
```

`compute_ode_series()` performs bounded exact SymPy power-series arithmetic
with rational inputs (and exact algebraic radicals for fractional `m`). It
then substitutes the finished polynomial into the **undivided corrected
residual**, not only the normal form, and checks coefficients `h^0` through
`h^(N-3)` are exactly zero. Thus the residual is formally `O(h^(N-2))`.
For the actual local analytic germ, Taylor's theorem gives local remainders
`F-F_N=O(h^(N+1))`, `F'-F_N'=O(h^N)`, and `F''-F_N''=O(h^(N-1))` as `h->0`.
A combined `(F,P,C)` norm is generally limited by the last exponent, not
the profile's `N+1`. None of these big-O statements supplies a *numerical*
constant or a verified radius. The finite polynomial is not itself an exact
solution unless the residual vanishes identically (as in 3.8).

Use from the package directory:

```powershell
python -B main.py --stage series --series-order 6 --trace summary
python -B -c "from main import compute_ode_series; r=compute_ode_series('3.4', exponent=3); print(r['polynomial'], r['verification'])"
```

The API returns inspectable SymPy `polynomial`, exact `coefficients`,
`recurrence`, chart values and assumptions, a typed `status`, and exact
`verification`. Degree is restricted to 3--8 for a bounded calculation.
Input decimal floats are converted to a simple fraction only when the
fraction round-trips to the identical float; otherwise their exact decimal
representation is retained. A finite `sympy.Float` is also accepted. This
avoids silently turning a tiny positive chart value into zero.

`run_series_campaign(out_dir, order=6, compare_dir=...)` writes
`series.json`, `series_trace.txt` and `series_comparison.csv`. With an
existing `numerical/` directory, comparison samples come **only** from its
saved 81-point RKF45/DOP853 CSV grid at offsets `L/2`, `L/4`, `L/8`, `L/16`;
there is no interpolation or output-grid claim about the new series solver.
The CSV keeps separate absolute errors for `F`, `F'`, `F''` and records
RKF/DOP853 disagreement plus an operational floating-resolution threshold.
These comparisons are diagnostics, not certified remainders or radius tests.
Comparison also requires a passed numerical receipt matching the model,
exponent, constants, initial jet, center and interval, with the exact
corrected-equation fingerprint and a matching CSV SHA-256. Missing, stale or
modified references receive an explicit unavailable/mismatch status and no
error values. Rerun the numerical or full campaign after editing the IVP or
equation; merely finding an old CSV with the same filename is insufficient.

## Measured finite evidence

The 2026-10-13 degree-six run completed and exactly verified all 21 regular
campaign IVPs. All 21 also found their four existing numerical grid nodes.
The nine subsection statuses are: 3.1 `outside_positive_chart` (stationary
identity family with `p=0`); 3.2 `undefined_chart` (`q=0`); 3.3
`no_invariant_graph`; 3.4, 3.5, 3.6, 3.8 and 3.9
`regular_analytic_germ`; and 3.7 `identity_family` (arbitrary analytic
`F(s)` with `alpha>0`, `F'>0`, not a unique ODE recurrence). The `alpha=0`
traveling exceptions are typed separately. X5 at `m!=3` is incompatible.

For the cubic 3.4 IVP `(z0,F0,P0,C0)=(1,2,1/2,1/10)`, the degree-six
coefficients are

```text
[2, 1/2, 1/20, -11/2370, 41037/6241000,
 -13543709/12325975000, 97895097811/43818841125000].
```

Its original corrected residual coefficients `h^0..h^3` are exactly zero.
The cubic 3.5 coefficients begin `a3=83/1100`, `a4=8309/60500` and pass
the same check. The 3.8 recurrence terminates at the exact quadratic
`F(h)=h+h^2/20` for its declared jet. Fractional `m=3/2` rows have exact
algebraic, not necessarily rational, coefficients and also pass.

At offsets `0.2,0.1,0.05,0.025`, the 3.4 cubic profile's absolute
series-vs-DOP853 errors are approximately `3.28e-9, 3.62e-11, 3.24e-13,
2.66e-15`. The last is at floating precision and is **not** an observed
order. Its `F''` errors are `2.50e-6, 1.37e-7, 5.21e-9, 1.78e-10`, as
expected to decrease more slowly. The short 3.6 and 3.9 profiles reach
roundoff in `F` quickly; they do not supply a useful profile-error slope.
The 3.8 quadratic differs from the stored numerical profiles only by
floating arithmetic. All rows and unresolved comparison flags remain in
the JSON and CSV.

## Singular and exceptional charts

`normal_form_singular` means only that dividing by `A` is invalid at the
given jet. It does **not** mean that no similarity solution exists. An exact
counterexample is the cubic X4 profile `F(z)=A*z^(1/3)` on `z>0`, with
`A^3=27*g/(1-12*g*kappa)` when `g*kappa<1/12`. For the campaign constants
`g=1`, `kappa=1/30`, `A^3=45`; the corrected residual vanishes but its
highest-derivative coefficient also vanishes along this branch. The API
does not claim existence/uniqueness from its regular normal form there.
Similarly, an identity reduction allows many profiles rather than a
three-jet-determined analytic germ, and 3.2 is undefined in the scalar PDE.

All conclusions concern the printed scalar reduction. The advectively
corrected scalar equation, full bed system, arbitrary IBVP, shocks, and
learned error are not established here.
