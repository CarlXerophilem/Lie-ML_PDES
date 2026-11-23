# Reproduce the fixed-point defect example

The worked example uses the depth-averaged rotating exchange tank on
\(0\le t\le1\), \(1\le\sqrt{x^2+y^2}\le3/2\). Its prescribed swirl reduces
the time dependence to \(b'(t)+3b(t)=9/10\). Both methods use the same trace
\(b(0)=3/20\) and degree-ten family
\(b(t)=b(0)+\sum_{j=1}^{10} c_jt^j\).

## Run from the repository root

Verified with Python 3.12 and SymPy 1.14.0. The certificate uses rational
arithmetic and needs only SymPy. It requires no data files, accelerator,
network calls or random initialization after installation.

~~~sh
python -m pip install sympy==1.14.0
python -B delivery/semianalytic_defect.py --method fit --initial 3/20 --degree 10 --fit-nodes 17 --check-cells 128 --gamma 4 --output fit.json
python -B delivery/semianalytic_defect.py --method taylor --output taylor.json
python -B -m unittest discover -s delivery -p test_semianalytic_defect.py
~~~

Omit the output filename to write JSON to stdout. Input fractions and
decimals are parsed as exact rationals. The allowed initial offsets are
\([2/25,1/5]\). The CLI requires a positive degree, at least two more fit
nodes than the degree, at least one check cell, and \(\gamma>3\).
The specified degree determines the polynomial order. For Taylor, the
fit-node setting has no effect on the coefficients.

## From input to certificate

| Stage | Input | Output |
|---|---|---|
| Trial construction | Trace, polynomial degree, fit nodes | Exact least-squares fit of the sampled Picard defect, or the Taylor recurrence from the ODE |
| Continuous certificate | Trial, Picard integral, check cells, Bielecki weight | Check of ball membership and continuous weighted and unweighted error bounds |
| Lift | Trial, prescribed tank parameters and annulus | Five residual polynomials from direct differentiation of the Cartesian fields |
| Evaluation | Trial and closed-form offset at the check nodes | Sampled diagnostic error |

The Picard integral is a polynomial integral. For a polynomial defect \(d\),
the uniform check grid gives fill distance \(1/(2n)\) for \(n\) cells.
The extreme Bernstein coefficients of \(d'\) give an exact upper bound
for its absolute maximum. The script adds the resulting between-node
bound to the exact sampled maximum. With \(\Lambda=3/\gamma\), the
weighted ball centered at \(3/10\) has radius
\(\lvert b(0)-3/10\rvert/(1-\Lambda)\). The centre's defect and the
contraction estimate imply that the ball is invariant. The script checks
candidate membership using an unweighted upper bound for its distance
from the centre. The unweighted certificate uses the Grönwall bound
\(e^3\|d\|_\infty<21\|d\|_\infty\) for nonzero defect.

Exact fields solve the lifted equations when \(b\) solves the quotient.
A trial has bounded bed and load residuals of opposite sign. The
Cartesian substitution is performed before inserting the polynomial
trial. On the stated annulus the angular and radial dependence cancels
symbolically. The resulting residual bounds hold continuously across
the annulus and time interval.

## Read the JSON

| Key | Interpretation |
|---|---|
| input | ODE, interval, exact trace, method and all run settings |
| trial_coefficients_ascending | Rational coefficients from degree zero upward |
| trace_exact | Whether the trial meets the trace exactly |
| certificate | Contraction, ball and defect bounds, error bounds, positivity flag |
| diagnostic_sampled_oracle_error_unweighted | Sampled maximum absolute difference from the exact offset |
| cartesian_original_residuals_of_trial | Exact five residual polynomials and absolute continuous bounds |

Use the strings in the exact fields for calculations. The decimal fields
are rounded for display. The default runs give weighted error upper
bounds below \(3.59\times10^{-8}\) for defect fitting and
\(2.78\times10^{-3}\) for Taylor. These bounds refer to the given
invariant family and initial trace. The earlier gated-cell and
Chebyshev comparisons are separate experiments in the three
ml entry points and associated logs. For the printed scalar symmetry
classification and series replay, use symbolic_sve2026.py and
reproduce_sve2026.py with the locally supplied reference PDF.
