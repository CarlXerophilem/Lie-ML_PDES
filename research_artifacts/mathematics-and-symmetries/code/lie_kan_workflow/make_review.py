#!/usr/bin/env python3
"""Regenerate the review and scientific figures from measured JSON/CSV files."""
import csv
import json
import statistics as st
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
METHODS=['direct_mlp','direct_kan','series_mlp','series_kan','chain_mlp','chain_kan']


def read(path):return json.loads((ROOT/path).read_text())


def summarize(data,label):
    rows=[]
    for method in data['arguments']['methods']:
        runs=[r for r in data['runs'] if r['method']==method]
        errors=[st.mean(v['evolution_relative_l2'] for v in r['test_metrics'].values()) for r in runs]
        maxima=[max(v['max_field_evolution_error'] for v in r['test_metrics'].values()) for r in runs]
        rows.append({'family':label,'method':method,'median_aggregate_error':st.median(errors),
            'min_aggregate_error':min(errors),'max_aggregate_error':max(errors),
            'median_max_field_error':st.median(maxima),'max_field_errors_by_seed':maxima,
            'passing_seeds':sum(all(v['matched_5percent'] for v in r['test_metrics'].values()) for r in runs),
            'seed_count':len(runs),'parameters':runs[0]['parameters'],
            'training_compute_seconds':st.median(r['training_compute_seconds'] for r in runs),
            'training_wall_seconds':st.median(r['training_wall_seconds'] for r in runs),
            'inference_seconds':st.median(v['inference_seconds'] for r in runs for v in r['test_metrics'].values())})
    return rows


def table(rows):
    lines=['| Method | Aggregate error, median [range] | Max-field error, median | Passing seeds | Train compute / wall (s) | Inference (ms) |',
           '|---|---:|---:|---:|---:|---:|']
    for r in rows:
        name=r['method']
        if r['family']=='SVE per-equation gate':name+=' (per-equation gate)'
        if r['family']=='SVE sensitivity loss':name+=' (sensitivity loss)'
        lines.append(f"| {name} | {100*r['median_aggregate_error']:.3f}% [{100*r['min_aggregate_error']:.3f}, {100*r['max_aggregate_error']:.3f}] | {100*r['median_max_field_error']:.2f}% | {r['passing_seeds']}/{r['seed_count']} | {r['training_compute_seconds']:.2f} / {r['training_wall_seconds']:.2f} | {1000*r['inference_seconds']:.2f} |")
    return '\n'.join(lines)


def figure(flat,sve,gate,sensitivity):
    colors={'series_mlp':'#c76614','series_kan':'#2863ad','chain_kan':'#148374'}
    fig,ax=plt.subplots(2,2,figsize=(14,8),gridspec_kw={'width_ratios':[1,1.3]})
    for row,(label,data) in enumerate([('Flat SWE',flat),('Grass SVE',sve)]):
        for run in data['runs']:
            method=run['method']
            if method not in colors:continue
            with (ROOT/'results'/('flat_kan_pilot' if row==0 else 'sve_kan_pilot')/method/f"seed{run['seed']}"/'history.csv').open() as f:history=list(csv.DictReader(f))
            ax[row,0].semilogy([float(r['training_seconds']) for r in history],[float(r['physics_validation']) for r in history],color=colors[method],alpha=.55)
        ax[row,0].set(title=label+': proposed iterates',xlabel='Optimizer compute (s)',ylabel='Physics-validation MSE')
        datasets=[(m,[r for r in data['runs'] if r['method']==m]) for m in METHODS]
        if row==1:
            datasets += [('gate KAN',gate['runs']),('slope KAN',sensitivity['runs'])]
        for i,(m,runs) in enumerate(datasets):
            values=[100*max(v['max_field_evolution_error'] for v in r['test_metrics'].values()) for r in runs]
            ax[row,1].scatter(np.full(len(values),i)+np.linspace(-.12,.12,len(values)),values,s=32,color=colors.get(m,'#626777'),zorder=3)
            ax[row,1].plot([i-.22,i+.22],[st.median(values)]*2,color='#30343a',lw=2)
        p2=max(v['max_field_evolution_error'] for v in data['Taylor_controls']['P2'].values())*100
        ax[row,1].axhline(5,color='#af3434',ls='--',lw=1.2,label='5% target')
        ax[row,1].axhline(p2,color='#777777',ls=':',lw=1.2,label='Pure P2')
        labels=[m.replace('direct_','direct\n').replace('series_','P2 +\n').replace('chain_','chain\n') for m,_ in datasets]
        ax[row,1].set(title=label+': retained models, all seeds',xticks=range(len(datasets)),xticklabels=labels,yscale='log',ylabel='Worst held-out active-field error (%)')
        ax[row,1].legend(fontsize=8,loc='upper right')
        for a in ax[row]:a.grid(alpha=.15)
    from matplotlib.lines import Line2D
    ax[0,0].legend(handles=[Line2D([0],[0],color=c,label=m) for m,c in colors.items()],fontsize=8)
    fig.suptitle('The series helps; a smaller sampled residual does not certify prediction accuracy',fontsize=13)
    fig.tight_layout();fig.savefig(ROOT/'halfway_comparison.png',dpi=170);plt.close(fig)
    p=read('results/swe2d_analysis.json')['step_6']['picard_certificate'];r=p['iterations']
    fig,ax=plt.subplots(figsize=(6,3.5))
    ax.semilogy([v['iteration'] for v in r],[v['depth_error_at_T'] for v in r],'o-',label='Exact depth error at T')
    ax.semilogy([v['iteration'] for v in r],[v['sup_norm_error_bound_H0_1'] for v in r],'s--',label='Sup-norm geometric bound')
    ax.set(xlabel='Picard iteration k',ylabel='Absolute depth error (H0=1)',title=f"Reduced ODE control: contraction bound {p['control_kappa']:.3f}")
    ax.legend(fontsize=8);ax.grid(alpha=.15);fig.tight_layout();fig.savefig(ROOT/'picard_control.png',dpi=160);plt.close(fig)


def main():
    flat=read('results/flat_kan_pilot/results.json');sve=read('results/sve_kan_pilot/results.json')
    gate=read('results/sve_kan_component_gate/results.json');sensitivity=read('results/sve_kan_sensitivity/results.json')
    flat_rows=summarize(flat,'Flat SWE');sve_rows=summarize(sve,'Grass SVE')
    extras=summarize(gate,'SVE per-equation gate')+summarize(sensitivity,'SVE sensitivity loss')
    rows=flat_rows+sve_rows+extras
    (ROOT/'summary.json').write_text(json.dumps({'aggregation':'Per run: mean aggregate error across two test cases; max active-field error across cases. Then median across seeds. Passing requires both cases <=5% in every active field and numerical guards.',
                                               'rows':rows},indent=2))
    with (ROOT/'summary.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    a1=read('results/swe1d_analysis.json');a2=read('results/swe2d_analysis.json')
    tests=read('results/solver_checks.json');deriv=read('results/final_series_verification/verification.json')
    timing='\n'.join(f"| {key.replace('_',' ')} | {value:.4f} |" for key,value in a2['timings'].items())
    refs=[v['tight']['solve_seconds'] for d in [flat,sve] for v in d['references'].values()]
    p2_flat=max(v['max_field_evolution_error'] for v in flat['Taylor_controls']['P2'].values())
    p2_sve=max(v['max_field_evolution_error'] for v in sve['Taylor_controls']['P2'].values())
    sensitivity_rows=[]
    for directory,label in [('flat_kan_pilot','Flat f'),('sve_kan_pilot','SVE m'),('sve_kan_component_gate','SVE m: gate'),('sve_kan_sensitivity','SVE m: slope loss')]:
        d=read(f'results/{directory}/sensitivity.json')
        for m in d['runs']:
            if m['method'] not in ['series_mlp','series_kan','chain_kan']:continue
            if any(r['case']==label and r['method']==m['method'] for r in sensitivity_rows):continue
            group=[r for r in d['runs'] if r['method']==m['method']]
            sensitivity_rows.append({'case':label,'method':m['method'],
                'relative':st.median(r['parameter_derivative_relative_l2'] for r in group),
                'bed_relative':st.median(r['per_field_relative_l2']['b'] for r in group),
                'depth_absolute':st.median(r['per_field_absolute_derivative_error_rms']['h'] for r in group)})
    stable='\n'.join(f"| {r['case']} | {r['method']} | {r['relative']:.4g} | {r['bed_relative']:.4g} | {r['depth_absolute']:.3g} |" for r in sensitivity_rows)
    contraction=a2['step_6']['picard_certificate']
    report=f'''# Basic Lie analysis and series-first learning: review and measured results

The standalone ML-free analyzer completes a verified reduction/reconstruction for a compatible flat-SWE family. The learning pilot shows that a coupled quadratic time series is the strongest improvement under this short budget. Smooth KAN corrections are implemented and tested, but neither KAN architecture nor residual backtracking consistently beats the MLP controls. Parameter interpolation accuracy also does not imply accurate parameter derivatives.

## Start from the basic level

Use `python lie_analyzer.py --builtin swe2d --out results/my_analysis.json`. Only SymPy is required. The default model has depth h and two velocities u,v: one mass-conservation equation and two momentum equations. In 2D the independent variables are (t,x,y), with t>0. The accepted spatial dimensions are integers 1 and 2; the three-field 1D example retains transverse velocity. Full 2D Grass SVE adds bed b and its conservation equation as an explicitly enabled four-equation extension.

The seven steps are: declare the regular PDE chart; prolong and determine; split/solve the chosen generator ansatz; verify and compute brackets; construct flows/invariant charts; reduce; reconstruct and substitute into the original PDE. The JSON contains every stage and timings. A generic custom input can finish with an unsupported reduction or unsolved reduced PDE: exact symmetry verification does not by itself solve an arbitrary initial-boundary problem.

## Symbolic complexity and time

Let n=d+1 independent variables, m fields, r jet order, and q generator-ansatz degree. There are m*binomial(n+r,r) dependent jet coordinates, including the fields. The polynomial ansatz has K=(n+m)*binomial(n+m+q,q) unknown coefficients. With M split rows, dense numerical elimination would cost roughly O(M K^2+K^3) arithmetic operations and O(MK) storage; this is only a comparison scale. Exact symbolic expression growth, rational bit lengths, denominator branches, and simplification can dominate. No overall polynomial-runtime bound is asserted for symbolic PDE classification.

| Model | Degree | Unknown coefficients | Split matrix | Rank / nullity | Full workflow (s) |
|---|---:|---:|---:|---:|---:|
| 1D three-field SWE | 1 | {a1['step_3']['unknowns']} | {a1['step_3']['split_matrix_shape'][0]} x {a1['step_3']['split_matrix_shape'][1]} | {a1['step_3']['rank']} / {a1['step_3']['nullity']} | {a1['total_seconds']:.3f} |
| 2D three-field SWE | 1 | {a2['step_3']['unknowns']} | {a2['step_3']['split_matrix_shape'][0]} x {a2['step_3']['split_matrix_shape'][1]} | {a2['step_3']['rank']} / {a2['step_3']['nullity']} | {a2['total_seconds']:.3f} |

The 2D step costs, in seconds, are:

| Stage | Seconds |
|---|---:|
{timing}

These are observed single runs on an AMD EPYC 9V74 CPU with SymPy 1.14/Python 3.12, not portable time guarantees. Symbolic series construction took {sve['series']['seconds']:.3f} s and produced {sve['series']['operation_count']} counted operations before lambdification/CSE. Learning used CPU float64 and one thread. Degree 2 increases the 2D ansatz from 42 to 168 unknowns and is optional; its cost is not measured here.

The 1D/2D affine nullities are 7/8. Each basis vector is substituted back exactly. A quadratic projective candidate is verified separately in 2D, outside the affine search. Thus the affine kernel is not a maximal point-symmetry classification. Generic symbolic parameters, nonpolynomial powers, and constrained non-involutive charts have explicit limitations. Exceptional parameter values must be recomputed: the cubic SVE scaling candidate passes at m=3 and fails at m=3.1 with fixed parameters.

## Exact reduction, series, and a function-iteration certificate

For rho=1+a*t, a>=0, the commuting generators Tx+a*Gx and Ty+a*Gy have the required spatial rank two. Their compatible ansatz reduces SWE to H'=-2aH/rho, U'=-aU/rho, V'=-aV/rho. Reconstruction gives h=H0/rho^2, u=(a*x+U0)/rho, v=(a*y+V0)/rho, with zero original residuals. The compatible linear-velocity data are nonperiodic; this reduction cannot be imposed on the benchmark's nonuniform periodic initial data. One x-translation alone leaves a 1+1 PDE in 2D.

For the reduced linear ODE, the Volterra/Picard map acts on C([0,T];R^3) with the sup norm. A sufficient contraction bound is kappa=d*log(1+a*T)<1. At a=.5,T=.25,d=2, kappa={contraction['control_kappa']:.6f}; iteration 6 has depth error {contraction['iterations'][-1]['depth_error_at_T']:.3g} at T for H0=1. The geometric sup-norm depth bound is {contraction['iterations'][-1]['sup_norm_error_bound_H0_1']:.3g}. This certificate applies to this reduced ODE. Spatial derivatives obstruct simply assuming a C0-to-C0 Lipschitz full-PDE map. It proves neither full-PDE nor learned-chain convergence. The exact rational solution needs no neural model.

For the full smooth coupled evolution U_t=F(U;p), the half-way approximation is P2=U0+t*F(U0;p)+t^2*DF(U0;p)[F(U0;p)]/2. All water/velocity/bed coefficients are coupled. With constant initial velocity the first bed coefficient vanishes, while the second is generally nonzero. The series is local; no general convergence radius is certified. The KAN remainder uses U=P2+(t^3/T^2)*S(p)*sum(alpha_k*C_k). Each C_k composes smooth Gaussian/linear edge layers. This preserves U0 and the first two time derivatives, and respects periodicity through Fourier inputs.

Earlier correction blocks freeze. A new block is optimized against the full nonlinear residual. Backtracking uses separate physics points of training cases, tries 1,.5,.25,.125,0, and preserves the prior iterate when rejected. The default gate checks total validation loss; the optional gate checks every equation separately. A residual decrease on these sampled points is not an error estimate.

## Controlled learning pilot

Each main method used 600 Adam steps, 128 fixed collocation points per training case, six training parameter pairs, two disjoint test pairs, T=.25, and seeds 0,1,2. Flat SWE trains (f,A) with f in 0,.1,.2 and A in .02,.04; tests f=.05,.15,A=.03. Grass SVE trains m=2.9,3,3.1 with the same amplitudes; tests m=2.95,3.05,A=.03. These are finite-parameter conditional field solvers, not arbitrary-function operators. Two-stage chains split the same total step budget, and have twice the total capacity. One MLP/KAN block has 2628/2588 parameters. An MLP chain is included to isolate chaining from architecture.

Error is normalized by the *evolution* of each field, rather than its large stationary background. For each seed, aggregate errors average the two cases; the reported maximum-field error is the worst active field over both cases. Tables give medians across seeds and retain aggregate-error ranges. Passing means both cases satisfy <=5% in every active field, positive depth, and reference guards. Three seeds and two tests are a pilot, without statistical generalization guarantees.

### Flat SWE

{table(flat_rows)}

### Evolving-bed Grass SVE

{table(sve_rows)}

Pure P2 requires no learning and has worst active-field error {100*p2_flat:.2f}% for flat SWE and {100*p2_sve:.2f}% for Grass SVE. It already meets the basic flat-SWE target. The SVE bed limits its accuracy. P0/P1/P2 per-case results are retained in JSON.

### Additional diagnostic trials

{table(extras)}

The per-equation KAN gate rejects several proposed stages; seed 1 retains pure P2. None of its three seeds passes the sediment target. The optional sensitivity term penalizes a central difference of the full residual at m+epsilon and m-epsilon (epsilon=.01, weight 1); it changes coefficients and predictions together. It uses no numerical sensitivity labels. Extra residual/derivative evaluations increase cost, and this untuned weight worsens field accuracy under 600 steps. These follow-up trials were triggered by observed failures; they are diagnostic extensions rather than a prespecified superiority test. Within-stage plots show proposals, whereas accepted-stage records and final errors describe retained models.

![Learning and retained-field accuracy](halfway_comparison.png)

The unexpected result is reproducible: a single series-KAN flat run has 60.3% worst-field error, while damped chaining passes all three flat seeds. In SVE, total-loss chaining lowers sampled validation losses yet every seed misses the bed target. The matched MLP series and MLP-chain controls pass both families at this budget. The evidence supports testing a series/remainder decomposition; it does not support asserting a general KAN advantage.

## Parameter sensitivity is a separate test

Post-hoc central differences use steps .01 and .005 around f=.1 or m=3 at A=.03, with n=24 tight numerical solutions. Saved checkpoints reproduce predictions exactly (maximum replay discrepancy zero across all 42 runs). These tests never select stage weights.

| Parameter / trial | Method | Aggregate derivative relative error | Bed derivative relative error | Depth derivative absolute RMS error |
|---|---|---:|---:|---:|
{stable}

Values in this table are ratios, not percentages. For m, the reference derivative RMS is about 9.75e-9 (depth), 7.82e-8 (each velocity), and 9.62e-7 (bed). Consequently large fluid derivative ratios accompany small absolute errors, but also reveal uncontrolled parameter dependence. Accurate interpolated fields do not validate a parameter-gradient operator. The sensitivity term reduces the median bed-derivative error from 47.3% to 6.05% and aggregate derivative-error ratio from 552.5 to 39.3, while worsening field accuracy and tripling optimizer compute. It demonstrates a tradeoff rather than a validated parameter operator. Reference step differences are about 3.36e-11 in max norm for m and 4.99e-8 for f. The sensitivity-loss option is a finite-difference physics proxy; it is not a certified gradient estimator. Full per-field scales and absolute errors are included in `sensitivity.json`.

## Numerical solver review and cost comparison

Independent controls pass with maximum errors: uniform rotation/drag {tests['uniform_rotation_drag_max_error']:.3g}; lake-at-rest change {tests['lake_at_rest_max_change']:.3g}; Fourier interpolation roundtrip {tests['spectral_interpolation_roundtrip_error']:.3g}; expanded Grass divergence versus a finite difference of the vector flux {tests['expanded_Grass_vs_flux_finite_difference_max_error']:.3g}. The 12/18/24 grid ladder and independent tolerance refinement agree at roughly 1e-11 on tested cases. Mass/bed means remain near roundoff; sampled hyperbolicity and positive-depth guards pass. These are checks of a smooth periodic reference, not proofs for shocks, dry beds, or long times.

The numerical method is conservative Fourier collocation with nonlinear-output filtering and DOP853 time integration. Its rough per-RHS work is O(N^2 log N) for an N-by-N grid; storage is O(N^2). Per-case fine numerical solves took {min(refs):.3f}–{max(refs):.3f} s. Neural training times in the tables cover a six-case conditional model per seed; inference times cover a warm 16-by-16 grid at three time snapshots. They must not be presented as equivalent setup costs. The numerical solve itself is fast enough for the current target, and no end-to-end ML speedup is demonstrated. Neural inference may help repeated queries after training, but amortization and deployment throughput remain unmeasured.

The previous Lie-PINN loss identity, where the tested squared infinitesimal-dot penalty becomes residual weighting, remains a necessary cheaper control. This experiment goes beyond adding that penalty by deriving coupled series, exact compatible reduction, a reduced-ODE Picard certificate, frozen residual corrections, and parameter-sensitivity tests.

## Recommended order of work

1. Fix the PDE, positive/singular branches, parameter stratum, and data/domain.
2. Verify algebra and data-compatible group actions. Classify model strata, not samples inferred from a Taylor fit.
3. Use an exact reduction when legal; otherwise compute a coupled local series in full coordinates.
4. Check pure-series per-field accuracy and stop if it meets the target.
5. Train only the remainder, retaining MLP and pure-series controls. Record rejected corrections and compute cost.
6. Check unseen parameters, per-field conservation/error, derivative sensitivity, and longer-time/domain limits.
7. Only then enlarge to function-space operators with explicit input functions, norms, discretization tests, and appropriate convergence/regularity analysis.

The current physical coupling is water/sediment coupling. Composing network layers does not create a multilayer-fluid PDE. A true multilayer extension needs extra layer balances, interface conditions, and new classical references before learning claims.

## Source audit and reproduction

The user's `main.tex` informed exact prolongation/finite-ansatz safeguards and exceptional-parameter handling; the previous `week3_01_flatbed_swe.py` informed exact expansion checks. The uploaded NS manuscript's section 9 informed the abstract pattern of inverse/correction/residual/constraint checks only. Its specialized 3D oscillatory construction, residual-gain exponents, and claimed blowup theorem were not validated or transferred to SWE.

Inspected primary author sources: [DeepOKAN paper](https://arxiv.org/abs/2405.19143), [DeepOKAN code](https://github.com/DiabAbu/DeepOKAN), [pykan](https://github.com/KindXiaoming/pykan), [SymPy ODE Lie documentation](https://docs.sympy.org/latest/modules/solvers/ode.html), and [LPSDA](https://github.com/brandstetter-johannes/LPSDA). DeepOKAN supplies the Gaussian edge-function inspiration, while this conditional series/correction implementation is independent. LPSDA is related symmetry augmentation and is not identified as the Lie-PINN code. No verified official Lie-PINN code release was located in the inspected sources. `SOURCE_AUDIT.json` records observed commits and inspected file hashes; unlicensed author code is not redistributed.

Run `lie_analyzer.py --self-test`, `series_kan.py --verify-only`, and `solver_checks.py`. The analyzer tests exact 1D/2D reconstruction, the separately supplied projective generator, rejected near-cubic/source candidates, third-order translation checks, nonautonomous coefficients, safe expressions, and dimensional/chart boundaries. Learning verification compares symbolic a1/a2 against independent autograd (errors {deriv['symbolic_vs_autograd_a1_max']:.3g}/{deriv['symbolic_vs_autograd_a2_max']:.3g}), checks KAN first/second derivatives, finite third derivatives, and preserved time jets with a nonzero correction. The exact uniform parameter-sensitivity residual is {deriv['exact_uniform_parameter_sensitivity_residual']:.3g}.

The README gives full run commands and limitations. `requirements-tested.txt` fixes the tested environment. JSON/CSV histories, rejected/accepted weights, predictions, refinement diagnostics, checkpoints, and summary tables are included. Run `python make_review.py` to rebuild this report and figures from results. This work does not establish a maximal Lie algebra, generic-m scalar-master elimination, shock/dry-bed solution theory, full-PDE fixed-point convergence, arbitrary-function operator learning, or a universal KAN advantage.
'''
    (ROOT/'REVIEW_AND_RESULTS.md').write_text(report)
    figure(flat,sve,gate,sensitivity)
    tex='''% Insertable baseline extension; numbers from the measured pilot.
\\subsection{Series-first correction baselines}
For smooth periodic two-spatial-dimensional SWE/Grass SVE, we use the coupled
local approximation $P_2=U_0+tF(U_0;p)+\\tfrac12t^2DF(U_0;p)[F(U_0;p)]$.
Smooth Gaussian-edge KAN and matched MLP remainders preserve the first two
initial time derivatives through a $t^3$ factor. Frozen two-stage chains use
physics-only validation backtracking, including rejection. All main methods
use 600 steps, six training pairs, two disjoint test pairs, and three seeds.
\\begin{center}\\begin{tabular}{llrr}
Family & Method & Median evolution error (\\%) & Passing seeds\\\\
\\hline
'''
    for r in flat_rows+sve_rows:
        tex+=f"{r['family']} & {r['method'].replace('_', ' ')} & {100*r['median_aggregate_error']:.3f} & {r['passing_seeds']}/3\\\\\n"
    tex+='''\\end{tabular}\\end{center}
Passing requires both test cases to meet 5\\% relative evolution error in every
active field, with numerical-reference guards. Pure $P_2$ already passes the
flat-SWE target. The series decomposition helps at this budget, while KAN is
not consistently better than MLP and lower sampled residuals do not certify
prediction or parameter-gradient accuracy. Fine per-case classical solves
take roughly 0.018--0.022 s; conditional-model training costs seconds.
No end-to-end neural speedup or full-PDE fixed-point convergence is claimed.
The ML-free affine analyzer finds 7/8 verified basis generators in the declared
1D/2D ansatz and completes a compatible expansion reduction; these counts are
not maximal classifications. A separate reduced linear ODE admits a verified
local Picard contraction bound $d\\log(1+aT)<1$, which is not transferred to the
full PDE or learned correction chain.
'''
    (ROOT/'baseline_extension.tex').write_text(tex)
    print(json.dumps({'rows':len(rows),'report':'REVIEW_AND_RESULTS.md','figure':'halfway_comparison.png'}))


if __name__=='__main__':main()
