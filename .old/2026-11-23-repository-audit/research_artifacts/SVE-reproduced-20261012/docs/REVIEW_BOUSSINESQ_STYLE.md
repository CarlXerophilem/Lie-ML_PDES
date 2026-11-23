# Fresh review: SVE replication rewrite (2026-10-14)

Scope: only `draft/main.tex` between `BEGIN/END SVE REPRODUCTION 20261012`, compared with `before/main.tex`. I read the local Boussinesq chapter extraction (printed pp. 157--159), the primary SVE PDF's case headings on PDF pp. 6--8, the source manifest, and the style/merit reports. This is an independent claim review, not a release or layout review.

## Findings, ordered by severity

1. **Minor, fix before finalizing C-TABLES:** In `draft/main.tex:2190`, case 3.9 lists the positive-chart condition `P,alpha_3-alpha P>0` but gives only the ODE for `alpha != 0`. That condition also allows `alpha=0, alpha_3>0`; the displayed undivided pullback then vanishes identically and leaves `F` arbitrary. The prose at `:2499--2503` says this, but the table's outcome column should also say `alpha=0: identity` so its same-case route is complete. For 3.6, `alpha=0` is outside its declared positive-velocity chart, so no analogous table correction is needed there.
2. **Minor wording:** `draft/main.tex:2850` introduces a reconstruction table as covering "the solved cases," but 3.7 is an identity family with arbitrary smooth `F`, not a solved ODE IVP. "The admitted graphs" or "the listed families" would preserve the section's own careful distinction. This is presentation, not a mathematical contradiction.

No incorrect new jet, current, time factor, or undivided pullback was found. No Boussinesq-specific transformation or constitutive `a,b` was imported. The new notation legend distinguishes derivative abbreviations, fixed algebra coefficients, flow parameter, and SVE model parameters.

## Claim verdicts

| Claim | Verdict | Basis / scope |
|---|---|---|
| C-STYLE | **Accepted** | The source chapter moves from determining criterion to classification table, invariant-graph table, then reduced-equation table (printed pp. 157--159). The revised SVE block follows that explanatory order while deriving its own fields and currents. The nine SVE rows are explicitly a source-selected audit, not a complete optimal system. |
| C-KEEP | **Accepted, qualified** | The paper-specific `m=1` boost, exact source-equation witnesses, first integrals, and divided-chart singular profile are substantive enough to retain a correction-focused study. The manuscript appropriately withholds literature-wide priority, full-system validity, arbitrary-data results, and numerical novelty. This verdict does not establish whether these corrections are new across the literature. |
| C-TABLES | **Qualified pending finding 1** | Cases 3.1--3.9 map from the correct source headings/generators to their own invariant graphs and undivided PDE pullbacks. Identity/undefined/no-graph and leading-coefficient failures are distinguished. Add the `alpha=0` identity directly to row 3.9 to make the table exhaustive on its stated chart. |
| C-DIRECT | **Accepted** | The direct 3.4 and 3.5 jets and current factors agree with differentiation of `phi=t F(s/t)` and `phi=F(st^2)`. Independent substitution in the expanded printed scalar `E_m` yielded zero difference from `t^-2 D(K_4 C)` for `m=3`, `-2z C_5/(t P^3)` for `m=3`, and `-alpha D(B C)` for the traveling graph at `m=3`. The 3.4 current identity itself is algebraic for general declared `m`; the sampled symbolic check does not replace a proof of every real exponent. |

## Independent checks and limits

- I used a separate, short SymPy expression for the manuscript's expanded scalar equation, populated it with the displayed 3.4, 3.5, and traveling jets, and compared against the table pullbacks. All three differences simplified to zero at `m=3` without calling package functions.
- The exact power profile `F=a z^(1/3)` gives `K_4 = z^(7/3)((12gk-1)a^3+27g)/(3a^2)` and the cubic reduced numerator has the same amplitude factor. Thus the stated amplitude condition simultaneously solves both undivided pullbacks and zeros the 3.4 leading coefficient.
- I did not rerun the full 43-test package, project audit/workflow, native `latexmk`, citation checks, or rendered-page review; those are assigned to root release validation. I did not independently verify every source counterexample or adjudicate the earlier full optimal-system classification, historical publication priority, arbitrary initial-boundary data, or the physical full bed system.

## Final verdict after one repair

I reread the revised row 3.9 and its surrounding chart/identity statements. `draft/main.tex:2190` now explicitly says `identity for alpha=0` while retaining the undivided `-alpha D(B C)` pullback and the chart `P,alpha_3-alpha P>0`; at `alpha=0` this requires `alpha_3>0` and is internally consistent. The later prose still explains its relation to case 3.7. The reconstruction introduction now says "invariant graph families," so it no longer calls arbitrary case 3.7 a solved IVP. **C-TABLES revision 2 is accepted; the two findings above are resolved.** Other claim verdicts and unjudged scope remain as stated; no full re-audit was performed.
