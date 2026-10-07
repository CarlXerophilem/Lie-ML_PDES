#!/usr/bin/env python3
"""Build a measured research note and an insertable LaTeX baseline section."""
import json
from pathlib import Path
import numpy as np


def main():
    root=Path(__file__).resolve().parent
    family=json.loads((root/'results/family_pilot/results.json').read_text())
    fs=json.loads((root/'results/family_pilot/summary.json').read_text())
    ss=json.loads((root/'results/suite_pilot/summary.json').read_text())
    symbols=json.loads((root/'results/symbolic_repeated.json').read_text())
    numerics=json.loads((root/'results/suite_pilot/numerical_references.json').read_text())
    def row(arch,method):return next(r for r in fs if r['architecture']==arch and r['method']==method)
    plain,lie,weighted,modified,conservation=[row(a,m) for a,m in [('mlp','vanilla'),('mlp','lie'),('mlp','reweighted'),
                                                               ('modified','vanilla'),('mlp','conservation')]]
    classical=np.array([v['ladder'][-1]['solve_seconds'] for v in numerics.values()])
    reduction=100*(1-weighted['train_seconds_median']/lie['train_seconds_median'])
    paired=[]
    for run in family['runs']:
        if run['method']!='lie':continue
        counterpart=next(r for r in family['runs'] if r['architecture']==run['architecture'] and r['seed']==run['seed'] and r['method']=='reweighted')
        for name,s in run['test_metrics'].items():
            paired.append(abs(s['evolution_relative_l2']-counterpart['test_metrics'][name]['evolution_relative_l2']))
    grads=[r['gradient_diagnostics']['gradient_cosine'] for r in family['runs'] if r['method']=='conservation']
    lines=['# SWE/SVE Lie-PINN baseline: measured pilot','',
           'Start with the flat-bed single-PDE experiment in README.md. The main experiment has two spatial coordinates plus time, four coupled fields, a smooth periodic domain, and a short horizon T=0.25. A separate 1+1 scalar control verifies the exceptional subgroup in the supplied manuscript.','',
           '**What was executed:** 63 single-case runs (7 cases × 3 seeds × 3 losses) and 45 conditional-family runs (3 architectures × 3 seeds × 5 losses). Each uses 600 Adam steps and 128 paired collocation points per training case. The family trains six parameter/initial-amplitude pairs and tests two unseen pairs plus one translated structural check. No test-based checkpoint selection was used.','',
           '## Symbolic cost and scope','',
           '| Case | PDE operation count | Scaling nullity | Audit seconds: median [min, max] |',
           '|---|---:|---:|---:|']
    for name,r in symbols.items():
        t=r['seconds']['total_seconds'];a=r['audit']
        lines.append(f"| {name} | {a['equation_ops']} | {a['scaling_ansatz']['nullity']} | {t['median']:.4f} [{t['min']:.4f}, {t['max']:.4f}] |")
    lines+=['','The audit uses a 19-coordinate first-order jet, a 4×19 residual Jacobian, seven supplied candidate generators, and a five-coefficient scaling ansatz. Repeated in-process timings retain cache effects and the first trial. This does not time or prove a maximal Lie classification.','',
            'Cubic active Grass transport has the additional V scaling; nearby noncubic cases reject it. Fixed Coriolis/drag breaks D. Continuous bulk rotations/scalings do not act globally on the fixed square torus; they enter only as local residual identities.','',
            '## Conditional neural comparison','',
            '| Architecture | Loss | Parameters | Evolution L2: seed median [min,max] | Maximum field error: median | Training compute: median s |',
            '|---|---|---:|---:|---:|---:|']
    for r in fs:
        lines.append(f"| {r['architecture']} | {r['method']} | {r['parameters']} | {r['error_median']:.4f} [{r['error_min']:.4f}, {r['error_max']:.4f}] | {r['max_field_error_median']:.4f} | {r['train_seconds_median']:.3f} |")
    lines+=['','Aggregate evolution errors average the two genuinely unseen test cases. Maximum field errors also inspect bed evolution. Seed ranges are not confidence intervals.','',
            f"The MLP Lie-loss median is {lie['error_median']:.4f}, versus {plain['error_median']:.4f} for vanilla. Its exact algebraic weighting reaches the same result: maximum paired evolution-error difference {max(paired):.3g}. The weighting uses {weighted['train_seconds_median']:.3f} s versus {lie['train_seconds_median']:.3f} s for explicit prolongation, a measured {reduction:.1f}% reduction in optimizer compute in this pilot.",
            '',f"The modified MLP has aggregate median error {modified['error_median']:.4f} versus {plain['error_median']:.4f} for the plain MLP, but its median maximum field error is {modified['max_field_error_median']:.4f} versus {plain['max_field_error_median']:.4f}. Architecture rankings therefore depend on the field/metric and seed. The paper's worse-modified-MLP result is not asserted as universal or reproduced in this different PDE experiment.",
            '',f"The MLP conservation variant has aggregate median error {conservation['error_median']:.4f}. Final training-batch PDE/extra-gradient cosines over all conservation runs range from {min(grads):.3f} to {max(grads):.3f}. All are positive at this sampled final checkpoint, so these diagnostics do not support gradient conflict as the explanation. Weight, quadrature, capacity, and sampling ablations are required before judging conservation penalties generally.",
            '', '![Learning curves](results/family_pilot/figures/learning_process.png)',
            '![Optimization snapshots](results/family_pilot/figures/training.gif)','',
            'The family pilot’s first panel logs last-update PDE losses from cycling training cases; it is not a fixed-case loss trajectory. Held-out evolution errors use the same diagnostic case throughout. Future runs additionally log PDE residuals at fixed independent points. GIF frames show training progress at fixed final physical time.','',
            '## Single-case baselines','',
            '| Case | Loss | Evolution L2 median | Maximum field error median | Matched seeds / 3 |',
            '|---|---|---:|---:|---:|']
    for r in ss:lines.append(f"| {r['group']} | {r['method']} | {r['error_median']:.4f} | {r['max_field_error_median']:.4f} | {r['matched_runs']}/3 |")
    lines+=['','## Classical comparison and limits','',
            f"Finest-grid classical solve times range from {classical.min():.4f} to {classical.max():.4f} s for the seven cases. Grid/tolerance construction is logged separately. Reference uncertainty estimates range from {min(v['estimated_reference_uncertainty'] for v in numerics.values()):.3g} to {max(v['estimated_reference_uncertainty'] for v in numerics.values()):.3g} in maximum absolute field difference.",
            '', 'None of the 45 conditional runs passes the preset 5% maximum per-field evolution-error target. Thus this pilot establishes **no matched-accuracy neural speedup or finite amortization break-even**. Neural grid inference is cheap, but numerical trajectories are also cached for repeated field queries. The possible amortization target is many new parameter/initial-data solves, after independent accuracy validation.','',
            'The supported advantages are exact hard initial conditions/periodicity, exact translation-family canonicalization, parameter-conditioned interpolation, and a verified cheaper implementation of a redundant Lie loss. Better accuracy than classical solving is not demonstrated.','',
            '## Next experiments beyond Lie classification','',
            '1. Run fixed-step collocation-count and loss-weight ablations with independent validation/test families; preserve every seed and failure.',
            '2. Improve sediment-dynamics accuracy with coupled equation balancing, residual-adaptive points, and gradient diagnostics.',
            '3. Extend the initial-condition family before claiming operator generalization; include a separate extrapolation test.',
            '4. Use a sourced energy-compatible/slope-aware SVE closure before introducing energy constraints.',
            '5. Add a well-balanced finite-volume reference and weak/conservative neural residual before studying shocks or dry beds.',
            '6. Compare conditional/equivariant architectures and inverse-parameter identification with the Lie-PINN baseline retained.',
            '', 'All statements apply to the recorded CPU pilot and declared regular model branch. The scalar printed-master control remains mathematically distinct from the 2+1 Grass system. Sources and exact commands are in README.md.']
    (root/'RESEARCH_REPORT.md').write_text('\n'.join(lines)+'\n')
    tex=r'''% Insert after the existing baseline section; requires amsmath.
% Add the three bibitems from baseline_references.tex to your bibliography.
\subsection{Smooth two-spatial-coordinate SWE/SVE Lie--PINN baseline}
We compare actual neural PDE solvers on a dimensionless smooth periodic
$(2+1)$-dimensional problem with fields $(h,u,v,b)$, not a two-coordinate
space--time reduction. The Grass vector flux is
$\boldsymbol q_b=\kappa(u^2+v^2)^{(m-1)/2}(u,v)$.
Seven cases progress from fixed flat bed through fixed topography and
isotropic Coriolis/linear drag to active transport at $m=2.9,3,3.1,4$.
The coupled conservative reference uses filtered Fourier collocation and
DOP853, with spatial and temporal refinement and physical-branch diagnostics.
This is a short-time smooth baseline, not a shock or dry-bed experiment.

The method adapts the jet-gradient/prolongation penalty of
\cite{akhound2023liepinn}, using a nonnegative squared-dot loss and a separate
squared-cosine variant. The PDE loss is retained. Supplied one-parameter
subgroups are checked infinitesimally and through finite jet actions. For
accepted candidates,
\[
 \operatorname{pr}^{(1)}X\Delta=M_X\Delta,
 \qquad M_D=-I,\quad M_V=\operatorname{diag}(2,1,1,2).
\]
The rotation multiplier mixes momentum residuals; autonomous translations
give zero. Thus the squared-dot Lie objective is an equation weighting in
this implementation. A matched algebraic weighting control tests the same
loss and parameter gradients. Cubic transport admits $V$ while nearby
noncubic cases reject it. These are candidate-verification results within a
finite scaling ansatz, not a maximal classification. Bulk dilation/rotation
identities do not justify global transformations of a fixed square torus or
invariant reductions of incompatible initial data.

We use matched-size plain MLP, modified MLP \cite{wang2021gradient}, and
branch/trunk architectures, identical hard initial conditions and periodic
coordinate features, paired points/initializations, and three seeds. A
conditional model trains six exponent/amplitude pairs and tests two unseen
pairs; a translated case separately checks exact phase canonicalization.
The final checkpoint is fixed in advance. Reference snapshots are diagnostics,
not supervised future data or test-based selectors. A conservation variant
constrains periodic water mass and bed mean; no unsupported Grass-SVE energy
law is imposed \cite{fernandez2017sve}.

The pilot executes 63 single-case and 45 conditional runs, each with 600 Adam
steps and 128 points per training case. Conditional plain-MLP median relative
evolution errors are VANILLA_ERROR for vanilla and LIE_ERROR for Lie loss.
The weighting control matches the latter and reduces median optimizer compute
from LIE_TIME~s to WEIGHT_TIME~s. Parameter-gradient equality is checked
independently. The modified MLP improves the aggregate median but worsens the
maximum-field median in this pilot; the architecture result in Appendix C of
\cite{akhound2023liepinn} is therefore treated as a hypothesis rather than a
universal ranking. Conservation penalties can also increase prediction error.

Finest-grid classical solve times are CLASS_MIN--CLASS_MAX~s. None of the
conditional runs meets the preset 5\% relative evolution-error target for
every active field, so no matched-accuracy neural speedup or finite
amortization claim follows. Whole-field errors can hide inaccurate bed
dynamics and are reported alongside evolution and per-field errors.
Symbolic build/audit, reference construction, training, monitoring, wall
time, and inference are logged separately. The 19-coordinate jet and $4\times19$
Jacobian define a bounded symbolic workload; exact simplification cost is
expression dependent and does not establish complexity of maximal Lie
classification. The manuscript's scalar $(1+1)$ master equation retains its
own cubic $X_5$ control and is not identified with this Grass system.

Training histories, field/error plots, an optimization GIF, checkpoints,
per-seed metrics, repeated symbolic timings, and scripts for sample/weight
ablations are supplied. Further experiments should target sediment accuracy,
gradient balance, broader initial-data families, a sourced energy-compatible
closure, and conservative weak formulations before shocks.
'''
    replacements={'VANILLA_ERROR':f"{plain['error_median']:.4f}",'LIE_ERROR':f"{lie['error_median']:.4f}",
                  'LIE_TIME':f"{lie['train_seconds_median']:.3f}",'WEIGHT_TIME':f"{weighted['train_seconds_median']:.3f}",
                  'CLASS_MIN':f"{classical.min():.4f}",'CLASS_MAX':f"{classical.max():.4f}"}
    for key,value in replacements.items():tex=tex.replace(key,value)
    (root/'baseline_section.tex').write_text(tex)
    print('Generated RESEARCH_REPORT.md and baseline_section.tex.')


if __name__=='__main__':main()
