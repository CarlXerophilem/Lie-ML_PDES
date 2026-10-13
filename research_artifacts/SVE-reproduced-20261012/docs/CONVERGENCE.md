# Endpoint convergence of the constructed regular IVPs

This experiment tests the **printed scalar** SVE profile ODEs, not physical
data, arbitrary PDE initial/boundary data, or a continuous error bound. Run
from this package directory:

```powershell
python -B main.py --stage convergence
```

The script calls `run_convergence(out_dir)` and writes
`results/convergence/convergence.json`, `.csv`, and `.png`. The JSON retains
the endpoint vector, step/RHS counts, failures, comparator settings, and
resolved/unresolved decisions for every run. It does not replace the original
81-point numerical campaign. The original 21 initial jets and intervals are
unchanged: 3.4 on `[1,1.4]`, 3.5/3.6/3.9 on `[1,1.1]`, and 3.8 on `[0,.4]`.

## Protocol

The fixed-step ladder takes exactly `N=1,2,4,8,16,32,64` steps with the
classic six-stage Fehlberg **fifth-order accepted state**. There is no error
controller. Each endpoint is compared componentwise with a tight SciPy
`DOP853` solution at the same endpoint, scaled by `max(1,|reference|)`.
Two DOP853 policies, `(rtol,atol,max_step)=(1e-12,1e-14,L/8)` and
`(1e-13,1e-15,L/16)`, supply a reference-disagreement diagnostic; the
tighter policy supplies the comparison value. Neither reference has an
output grid. For 3.8, the exact quadratic replaces DOP853.

The adaptive sweep uses the same Fehlberg implementation with `rtol` from
`1e-3` through `1e-10`, `atol=rtol/100`, `first_step=L/2`, and the same
nonrestrictive `max_step=L` at every tolerance. There is **no `t_eval`**.
Its step counts, rejections and function evaluations are saved. Holding the
step policy fixed isolates tolerance changes from a changing maximum step;
it does not force the method to choose different steps on a short/easy IVP.

To avoid calling floating-point noise an order, a fixed-step endpoint error
is *resolved* only if it exceeds `10*max(32*epsilon_machine,
10*DOP853_pair_disagreement)`. The maximum comparator disagreement in this
run was `1.89e-15`; thus the resolved-error thresholds range from
`7.11e-14` to `1.89e-13`. Pairwise order `log2(E_N/E_2N)` is reported only
when **both** errors exceed that threshold. This is an operational resolution
screen, not a rigorous upper bound on either solver's error.

## Measured results (2026-10-12, Python 3.14.2)

All 21 established IVPs completed both sweeps. Of 147 fixed-step endpoint
errors, 55 exceeded the resolution threshold and 92 did not. There are 39
resolved adjacent-step order estimates. For the five 3.4 exponent rows,
the resolved late-ladder orders approach five: the last resolved order is
between `4.97` and `4.98`. The cubic 3.5 row's last resolved order is
`4.93`. These are empirical global endpoint orders on these smooth local
IVPs, not an error certificate for the original PDE.

The short 3.6 and 3.9 traveling-wave intervals each give only one resolved
adjacent pair, around `4.95`--`4.97`; further halving reaches the floor.
That supports consistency with fifth order but does **not** establish an
asymptotic range for those rows. The five 3.8 rows have the exact quadratic
`F(t)=F0+P0*t+C0*t^2/2`; their fixed-step differences are roundoff-level
and no nontrivial convergence order can be inferred.

The separate exact non-polynomial control `y'=y`, `y(0)=1` on `[0,2]`
has fixed-step orders `4.44, 4.72, 4.86, 4.93, 4.96` for successive
halvings. This tests the code's fifth-order behavior without relying on a
numerical reference. It does not by itself establish the SVE model's order.

On 3.4 and 3.5, adaptive endpoint error decreases from about `1e-7` to
`1e-11` as tolerance tightens and accepted steps rise from 2 to 12 and
11, respectively. The first four tolerance settings use identical two-step
histories, so their error is identical: a genuine coarse-tolerance plateau.
The 3.6 and 3.9 rows remain two-step histories throughout this chosen sweep;
their errors do not change with tolerance. The 3.8 adaptive endpoints equal
the exact quadratic to floating precision (zero in the reported scaled
metric). A tolerance sweep cannot demonstrate convergence where the step
history does not change.

Every positive-branch guard is checked at solver stages and fixed-step
endpoints. Only local, sampled regularity is established. The figure omits
zero adaptive errors from its log axis; the CSV and JSON retain them. Source
equation errors, branch singularities, and behavior outside these intervals
are not resolved by this experiment.
