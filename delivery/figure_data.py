"""Export LaTeX macros (numbers.tex) and pgfplots .dat tables from planar_ode_results.json."""
import json
import math
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, 'logs', 'planar_ml')
FIGS = os.path.join(HERE, '..', 'draft', 'figures', 'planar')


def sci_tex(x, digits=2):
    x = float(x)
    if x == 0.0:
        return '0'
    exp = int(math.floor(math.log10(abs(x))))
    mant = x / (10.0 ** exp)
    if round(abs(mant), digits) >= 10.0:
        mant /= 10.0
        exp += 1
    if -2 <= exp <= 1:
        return f'{x:.{max(0, digits - exp)}f}'
    return f'{mant:.{digits}f}\\times 10^{{{exp}}}'


def write_table(path, cols, rows):
    with open(path, 'w') as fh:
        fh.write(' '.join(cols) + '\n')
        for row in rows:
            fh.write(' '.join('nan' if v is None or (isinstance(v, float) and np.isnan(v)) else f'{float(v):.8e}' for v in row) + '\n')


def main():
    os.makedirs(FIGS, exist_ok=True)
    with open(os.path.join(LOGS, 'planar_ode_results.json')) as fh:
        res = json.load(fh)
    with open(os.path.join(LOGS, 'planar_ode_grids.json')) as fh:
        grids = json.load(fh)

    # 1. annulus_solvers.dat (held-out tuple 0 across r in [0.85, 2.0])
    g0 = grids['0']
    rows_solvers = [
        (r, hd, hc, hl, ht, zd, zc, zl, eta)
        for r, hd, hc, hl, ht, zd, zc, zl, eta in zip(
            g0['r'], g0['H_dop'], g0['H_cheb'], g0['H_lnn'],
            g0['H_tay_plot'], g0['Z_dop'], g0['Z_cheb'], g0['Z_lnn'], g0['eta_dop'],
        )
    ]
    write_table(
        os.path.join(FIGS, 'annulus_solvers.dat'),
        ['r', 'H_dop', 'H_cheb', 'H_lnn', 'H_tay', 'Z_dop', 'Z_cheb', 'Z_lnn', 'eta_dop'],
        rows_solvers,
    )

    # 2. annulus_sonic.dat (held-out tuple 1 inward sonic probe down to r_stop + branch_minus)
    g1 = grids['1']
    rows_sonic = [
        (r, h, dc)
        for r, h, dc in zip(g1['inward_probe_r'], g1['inward_probe_H'], g1['inward_probe_Dc'])
    ]
    write_table(
        os.path.join(FIGS, 'annulus_sonic.dat'),
        ['r', 'H_plus', 'Dc'],
        rows_sonic,
    )
    rows_minus = [(r, h) for r, h in zip(g1['branch_minus_r'], g1['branch_minus_H'])]
    write_table(
        os.path.join(FIGS, 'annulus_branch_minus.dat'),
        ['r', 'H_minus'],
        rows_minus,
    )

    # 3. annulus_errors.dat (all 8 held-out test tuples sorted by saddle margin delta)
    held = sorted(res['held_out_tuples'], key=lambda rec: rec['parameters']['delta'])
    rows_err = []
    for idx_sorted, rec in enumerate(held, start=1):
        p = rec['parameters']
        rows_err.append((
            idx_sorted,
            rec['index'],
            p['m'],
            p['kappa'],
            p['delta'],
            rec['taylor_K16']['near_0p9_1p1_max_H_err'],
            rec['taylor_K16']['global_0p85_2p0_max_H_err'],
            rec['chebyshev_1d']['max_H_diff_vs_dop853'],
            rec['chebyshev_1d']['max_pde_res'],
            rec['lnn_pinn_surrogate']['max_H_err_vs_dop853'],
            rec['lnn_pinn_surrogate']['max_defect'],
            rec['lnn_pinn_surrogate']['max_pde_res'],
            rec['lnn_pinn_surrogate']['max_bed_Z_err_vs_dop853'],
        ))
    write_table(
        os.path.join(FIGS, 'annulus_errors.dat'),
        [
            'rank', 'tuple_id', 'm', 'kappa', 'delta',
            'tay_near_err', 'tay_glob_err',
            'cheb_H_diff', 'cheb_pde_res',
            'lnn_H_err', 'lnn_defect', 'lnn_pde_res', 'lnn_Z_err',
        ],
        rows_err,
    )

    # 4. LaTeX macros in draft/figures/planar/numbers.tex
    S = res['summary_held_out']
    T = res['lnn_pinn_training']
    D = res['domain_verification']
    SC = res['parameter_dimension_scaling']
    t0_p = res['held_out_tuples'][0]['parameters']
    t1_sonic = res['held_out_tuples'][1]['dop853']['inward_probe_to_0p5_r_stop']
    all_stops = D['train']['stops_detail'] + D['test']['stops_detail']
    max_r_stop = max(h['r_stop'] for h in all_stops) if all_stops else 0.5

    macros = {
        'NumGitCommitShort': res['git_commit'][:7],
        'NumPreservedParams': str(res['reduced_ode_ast']['preserved_parameter_count']),
        'NumTrainTuples': str(res['design']['n_train']),
        'NumTestTuples': str(res['design']['n_test']),
        'NumTotalTuples': str(res['design']['n_train'] + res['design']['n_test']),
        'NumNodesPerTuple': str(T['nodes_per_tuple']),
        'NumCollocTotal': f"{T['collocation_points']:,}",
        'NumLNNParams': f"{T['parameters']:,}",
        'NumLNNTrainSec': f"{T['seconds']:.1f}",
        'NumLNNTrainRMS': sci_tex(T['train_rms_defect'], 2),
        'NumLNNTrainMax': sci_tex(T['train_max_defect'], 2),
        'NumTayNearMed': sci_tex(S['taylor_K16_near_median_H_err'], 2),
        'NumTayNearMax': sci_tex(S['taylor_K16_near_max_H_err'], 2),
        'NumTayNearZMed': sci_tex(S['taylor_K16_near_median_bed_Z_err'], 2),
        'NumTayGlobMed': sci_tex(S['taylor_K16_global_median_H_err'], 2),
        'NumTayGlobMax': sci_tex(S['taylor_K16_global_max_H_err'], 2),
        'NumDOPFull': S['dop853_full_annulus_count'],
        'NumDOPMs': f"{1e3 * S['dop853_mean_seconds_per_tuple']:.1f}",
        'NumChebFull': S['chebyshev_converged_count'],
        'NumChebDiffMax': sci_tex(S['chebyshev_max_H_diff_vs_dop853'], 2),
        'NumChebDiffMed': sci_tex(S['chebyshev_median_H_diff_vs_dop853'], 2),
        'NumChebZMax': sci_tex(S['chebyshev_max_bed_Z_diff_vs_dop853'], 2),
        'NumChebZMed': sci_tex(S['chebyshev_median_bed_Z_diff_vs_dop853'], 2),
        'NumChebPDEMax': sci_tex(S['chebyshev_max_pde_res'], 2),
        'NumChebMs': f"{1e3 * S['chebyshev_mean_seconds_per_tuple']:.1f}",
        'NumLNNHMed': sci_tex(S['lnn_pinn_median_max_H_err'], 2),
        'NumLNNHWorst': sci_tex(S['lnn_pinn_worst_max_H_err'], 2),
        'NumLNNHRMSMed': sci_tex(S['lnn_pinn_median_rms_H_err'], 2),
        'NumLNNZMed': sci_tex(S['lnn_pinn_median_bed_Z_err'], 2),
        'NumLNNZWorst': sci_tex(S['lnn_pinn_worst_bed_Z_err'], 2),
        'NumLNNDefMed': sci_tex(S['lnn_pinn_median_max_defect'], 2),
        'NumLNNDefWorst': sci_tex(S['lnn_pinn_worst_max_defect'], 2),
        'NumLNNPDEMed': sci_tex(S['lnn_pinn_median_max_pde_res'], 2),
        'NumLNNPDEWorst': sci_tex(S['lnn_pinn_worst_max_pde_res'], 2),
        'NumLNNQueryMs': f"{1e3 * S['lnn_pinn_mean_query_seconds_per_tuple']:.2f}",
        'NumSonicStopsTotal': str(len(all_stops)),
        'NumMaxSonicStopR': f'{max_r_stop:.2f}',
        'NumTupleOneSonicR': f'{t1_sonic:.3f}',
        'NumTupleZeroM': f"{t0_p['m']:.2f}",
        'NumTupleZeroK': f"{t0_p['kappa']:.2f}",
        'NumTupleZeroD': f"{t0_p['delta']:.2f}",
        'NumChebDOFpThree': f"{SC['p3_active_box']['tensor_chebyshev_dof']:,}",
        'NumChebDOFpNine': sci_tex(SC['p9_full_preserved_symbols']['tensor_chebyshev_dof'], 2),
        'NumLNNpNine': f"{SC['p9_full_preserved_symbols']['lnn_pinn_params']:,}",
        'NumBowlMaxRes': sci_tex(res['appendix_controls']['convex_bowl_f_pos']['max_residual_and_quadrature_diff'], 1),
        'NumFluxDriftRes': sci_tex(res['appendix_controls']['general_c2_flux_drift']['max_momentum_residual'], 1),
        'NumTayEightErr': sci_tex(res['appendix_controls']['analytical_tail_bounds']['tuple0_K8_actual_err_on_0p05'], 2),
        'NumTayEightBound': sci_tex(res['appendix_controls']['analytical_tail_bounds']['tuple0_K8_cauchy_majorant_on_0p05'], 2),
    }
    with open(os.path.join(FIGS, 'numbers.tex'), 'w') as fh:
        fh.write('% Auto-generated by delivery/figure_data.py from planar_ode_results.json; do not hand-edit.\n')
        for name, val in sorted(macros.items()):
            fh.write(f'\\providecommand{{\\{name}}}{{{val}}}\n')

    print('Wrote numbers.tex and annulus_*.dat tables to', FIGS)


if __name__ == '__main__':
    main()
