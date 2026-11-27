"""Reproducible runner for Chapter 4: Irreducible Planar E2 ODE Continuation and LNN-PINN.

Executes the unified SymPy-AST pipeline on the declared physical parameter box
    m in [1.5, 3.5],  k = K/G in [2, 10],  delta = gamma_*(m, k) - c/G in [1, 3]
over the globally smooth physical annulus r in [0.85, 2.0] (48 train tuples seed 27,
8 held-out test tuples seed 29), recording:
  1. Automatic judgemental gate verification on the live SymPy ReducedODE AST.
  2. Local Briot-Bouquet Taylor series (K = 16): accuracy near r = 1 vs blow-up at r = 2.
  3. Per-tuple classical continuation: Taylor + SciPy DOP853 (plus inward sonic-point event
     probe below r = 0.85) and 1D Chebyshev spectral collocation.
  4. Multi-parameter physics-only grey-box surrogate: LNN-PINN (width-32 gated liquid block)
     conditioned on (m, k, delta) with zero DOP853 labels and zero domain-masking oracle.
  5. Appendix controls: exact f > 0 convex-bed bowl and non-power-law C^2 flux bed drift.
"""
import json
import os
import platform
import subprocess
import sys
import time
import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid
import sympy
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from planar import bench as B
from planar.classical import collocate, eval_cheb_side
from planar.model import (
    Anchor,
    compiled_planar_ast,
    reference,
    reference_w,
    taylor,
    taylor_deriv,
    taylor_eval,
)

OUT = os.path.join(HERE, 'logs', 'planar_ml')


def git_rev():
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=HERE, text=True).strip()
    except Exception:
        return 'unknown'


def prepare_tuples(raw_tuples):
    enriched = []
    for idx, raw in enumerate(raw_tuples):
        M, gamma, gs, det, br = B.tuple_model(raw, B.F_BEND)
        ell_m, lam_m, a_m = br[0]
        ell_p, lam_p, a_p = br[1]
        gate = M.solvability_gate()
        assert gate['gate_3_briot_bouquet_saddle'], f'Tuple {idx} failed Briot-Bouquet gate!'
        enriched.append({
            'index': idx,
            **raw,
            'gamma': gamma,
            'gamma_star': gs,
            'det_J': det,
            'ell_minus': ell_m,
            'lam_minus': lam_m,
            'a_minus': a_m,
            'ell': ell_p,
            'lam': lam_p,
            'a': a_p,
            'model': M,
            'gate': gate,
        })
    return enriched


def verify_smooth_annulus(tuples):
    """Confirm via DOP853 event detection that 100% of tuples traverse r in [0.85, 2.0] smoothly,
    and probe inward down to r = 0.50 to document where true second sonic points occur."""
    annulus_ok = 0
    inward_sonic_hits = []
    for t in tuples:
        M = t['model']
        r_out = reference(M, t['ell'], t['a'], +1, B.ANNULUS['sides'][1])
        r_in = reference(M, t['ell'], t['a'], -1, B.ANNULUS['sides'][-1])
        if r_out['reason'] == 'boundary_reached' and r_in['reason'] == 'boundary_reached':
            annulus_ok += 1
        probe = reference(M, t['ell'], t['a'], -1, B.INWARD_SONIC_PROBE_SMAX)
        if probe['reason'] != 'boundary_reached':
            inward_sonic_hits.append({
                'index': t['index'],
                'm': t['m'],
                'kappa': t['kappa'],
                'delta': t['delta'],
                'r_stop': float(1.0 - probe['extent']),
                'reason': probe['reason'],
            })
    return {
        'total_tuples': len(tuples),
        'smooth_on_0p85_to_2p0': annulus_ok,
        'inward_probe_to_0p50_stops': len(inward_sonic_hits),
        'min_smooth_r_across_all_tuples': float(
            min([1.0 - h['r_stop'] for h in []] + [h['r_stop'] for h in inward_sonic_hits] + [0.5])
        ) if inward_sonic_hits else 0.5,
        'stops_detail': inward_sonic_hits,
    }


def integrate_bed(M: Anchor, r_grid: np.ndarray, H_grid: np.ndarray) -> np.ndarray:
    """Integrate Z'(r) = P_Z(r, H(r)) from Z(1) = 0 on a sorted radial grid containing r = 1."""
    _, _, PZ = M.DN(r_grid, H_grid)
    Z_raw = cumulative_trapezoid(PZ, r_grid, initial=0.0)
    z_at_1 = float(np.interp(1.0, r_grid, Z_raw))
    return Z_raw - z_at_1


def bowl_control():
    """Exact rotating moving-bed convex-bowl check (f > 0, V = 0, W = -fr/2, c > 0) for Appendix A."""
    f, g, G, c, E = 1.0, 1.0, 1.0, 0.1, 2.6
    r = np.linspace(0.6, 1.8, 241)
    worst = 0.0
    for m in (1.0, 1.5, 2.0, 3.0):
        Zp = c * (r ** (2.0 - m)) / (2.0 * G * ((0.5 * f) ** (m - 1.0)))
        Z = (c / (2.0 * G * ((0.5 * f) ** (m - 1.0)))) * (
            np.log(r) if m == 3.0 else (r ** (3.0 - m) - 1.0) / (3.0 - m)
        )
        H = E - Z - (f * f * r * r) / (8.0 * g)
        Hp = -Zp - (f * f * r) / (4.0 * g)
        W = -0.5 * f * r
        radial_mom = -(W * W) / r - f * W + g * (Hp + Zp)
        Q_r = (np.abs(W) ** (m - 1.0)) * (-G * Zp)
        exner_int = r * Q_r + 0.5 * c * r * r
        worst = max(worst, float(np.max(np.abs(radial_mom))), float(np.max(np.abs(exner_int))))
    return {'f': f, 'g': g, 'G': G, 'c': c, 'E': E, 'm_tested': [1.0, 1.5, 2.0, 3.0], 'max_residual_and_quadrature_diff': worst}


def analytical_bounds_control(t0):
    """Verify the explicit analytical contraction & Cauchy/Laurent tail bounds of Chapter 4."""
    # 1. Laurent contraction on |xi| <= 1/4, ||v||_inf <= 1/4:
    #    ||T_L v|| <= (1/24)*(16/15)^2 * 3 + (1/4)*((1/16)*(16/15) + (1/4)*(16/15)^3/12) * (3/4)
    y_min = 15.0 / 16.0
    t_norm_bound = 3.0 * (1.0 / (24.0 * y_min**2)) + 0.75 * 0.25 * (
        (0.25**2) / y_min + 0.25 / (12.0 * y_min**3)
    )
    # 2. Local Briot-Bouquet Cauchy tail check at held-out tuple 0 on |rho| <= 0.05:
    M = t0['model']
    ell, a = t0['ell'], t0['a']
    b = -a  # b = 1 - lambda_o / lambda > 1
    w_c = taylor(M, ell, a, K=16)
    ref_out = reference(M, ell, a, +1, 0.10)
    rho_small = np.linspace(1e-3, 0.05, 50)
    H_true = 1.0 + rho_small * (ell + reference_w(ref_out, rho_small))
    H_tay8 = 1.0 + rho_small * (ell + taylor_eval(w_c[:9], rho_small))
    actual_tail8 = float(np.max(np.abs(H_true - H_tay8)))
    # Empirical geometric majorant on |rho| <= R_loc = 0.25 from |w_k| R_loc^k
    R_loc = 0.25
    R_w = float(np.max([abs(w_c[k]) * (R_loc ** k) for k in range(1, 17)]))
    theta = 0.05 / R_loc
    cauchy_bound8 = float(R_w * R_loc * (theta ** 9) / (1.0 - theta))
    return {
        'regular_Y4_certified_radius': 1.0 / 64.0,
        'laurent_T_norm_upper_bound': float(t_norm_bound),
        'briot_bouquet_b_tuple0': float(b),
        'tuple0_K8_actual_err_on_0p05': actual_tail8,
        'tuple0_K8_cauchy_majorant_on_0p05': cauchy_bound8,
        'majorant_holds': bool(actual_tail8 <= cauchy_bound8),
    }


def flux_drift_control():
    """Verify Proposition 2.7 (closed-form drift wave) for non-power-law C^2 flux Q(u) = u^3 + 0.5*u*exp(-u/4)."""
    g, q0, alpha, U0 = 1.0, 1.2, 0.25, 1.1
    u = np.linspace(0.55, 1.1, 300)
    Q = lambda v: v**3 + 0.5 * v * np.exp(-0.25 * v)
    dQ = lambda v: 3.0 * v**2 + (0.5 - 0.125 * v) * np.exp(-0.25 * v)
    xi = (Q(U0) - Q(u)) / alpha
    H = q0 / u
    Z = (0.5 * U0**2 + g * (q0 / U0)) - (0.5 * u**2 + g * H)
    # Check Exner residual: alpha + d/dxi Q(U(xi)) = alpha + Q'(U) * U'(xi) = 0
    U_xi = -alpha / dQ(u)
    exner_res = alpha + dQ(u) * U_xi
    H_xi = -(q0 / (u * u)) * U_xi
    Z_xi = -(u + g * (-q0 / (u * u))) * U_xi
    mom_res = u * U_xi + g * (H_xi + Z_xi)
    return {
        'flux_law': 'Q(u) = u^3 + 0.5 * u * exp(-u/4)',
        'max_exner_residual': float(np.max(np.abs(exner_res))),
        'max_momentum_residual': float(np.max(np.abs(mom_res))),
        'min_dQ_du': float(np.min(dQ(u))),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    t_start = time.perf_counter()

    ast = compiled_planar_ast()
    train_tuples = prepare_tuples(B.sample(B.BOX, B.N_TRAIN, B.SEED_TRAIN))
    test_tuples = prepare_tuples(B.sample(B.BOX, B.N_TEST, B.SEED_TEST))

    # 1. Verify smooth annulus on both train & test sets + inward sonic probe
    train_domain = verify_smooth_annulus(train_tuples)
    test_domain = verify_smooth_annulus(test_tuples)
    assert train_domain['smooth_on_0p85_to_2p0'] == B.N_TRAIN
    assert test_domain['smooth_on_0p85_to_2p0'] == B.N_TEST

    # 2. Train joint 4D physics-only LNN-PINN surrogate on the 48 training tuples
    net, train_log = B.train_lnn_pinn(train_tuples, iters=B.LBFGS_ITERS, seed=B.SEED_TRAIN)
    np.savez(os.path.join(OUT, 'weights_lnn_pinn.npz'), **net.export())

    # 3. Evaluate all 3 solver classes on the 8 held-out test tuples
    s_near = np.linspace(1e-3, 0.10, 100)
    s_in = np.linspace(1e-3, B.ANNULUS['sides'][-1], 120)
    s_out = np.linspace(1e-3, B.ANNULUS['sides'][1], 240)
    rho_eval = np.concatenate([-s_in[::-1], s_out])
    r_eval = 1.0 + rho_eval

    test_records = []
    grids_payload = {}

    for t in test_tuples:
        M = t['model']
        ell, a = t['ell'], t['a']

        # Method 1: Local Briot-Bouquet Taylor series (K = 16)
        t0 = time.perf_counter()
        w_tay_coef = taylor(M, ell, a, K=16)
        tay_secs = time.perf_counter() - t0

        # Method 2a: Taylor (s0 = 1e-3) + SciPy DOP853 per-tuple continuation
        t0 = time.perf_counter()
        ref_in = reference(M, ell, a, -1, B.ANNULUS['sides'][-1])
        ref_out = reference(M, ell, a, +1, B.ANNULUS['sides'][1])
        dop_secs = time.perf_counter() - t0

        w_dop = np.concatenate([
            reference_w(ref_in, s_in[::-1]),
            reference_w(ref_out, s_out),
        ])
        H_dop = 1.0 + rho_eval * (ell + w_dop)
        Z_dop = integrate_bed(M, r_eval, H_dop)

        # Near-window [0.9, 1.1] Taylor evaluation vs DOP853
        rho_near = np.concatenate([-s_near[::-1], s_near])
        r_near = 1.0 + rho_near
        w_dop_near = np.concatenate([
            reference_w(ref_in, s_near[::-1]),
            reference_w(ref_out, s_near),
        ])
        H_dop_near = 1.0 + rho_near * (ell + w_dop_near)
        Z_dop_near = integrate_bed(M, r_near, H_dop_near)
        w_tay_near = taylor_eval(w_tay_coef, rho_near)
        dw_tay_near = taylor_deriv(w_tay_coef, rho_near)
        H_tay_near = 1.0 + rho_near * (ell + w_tay_near)
        Z_tay_near = integrate_bed(M, r_near, H_tay_near)
        dH_tay_near = ell + w_tay_near + rho_near * dw_tay_near
        tay_near_pde = M.parent_pde_residuals(r_near, H_tay_near, dH_tay_near)

        # Global [0.85, 2.0] Taylor evaluation (demonstrating divergence outside |r - 1| < R <= 1)
        w_tay_glob = taylor_eval(w_tay_coef, rho_eval)
        H_tay_glob = 1.0 + rho_eval * (ell + w_tay_glob)

        # Method 2b: 1D Chebyshev spectral collocation per-tuple
        cheb_in = collocate(M, ell, -1, B.ANNULUS['sides'][-1], B.ANNULUS['cheb'][-1])
        cheb_out = collocate(M, ell, +1, B.ANNULUS['sides'][1], B.ANNULUS['cheb'][1])
        w_ci, dw_ci = eval_cheb_side(cheb_in['coeffs'], B.ANNULUS['sides'][-1], -1, -s_in[::-1])
        w_co, dw_co = eval_cheb_side(cheb_out['coeffs'], B.ANNULUS['sides'][1], +1, s_out)
        w_cheb = np.concatenate([w_ci, w_co])
        dw_cheb = np.concatenate([dw_ci, dw_co])
        H_cheb = 1.0 + rho_eval * (ell + w_cheb)
        Z_cheb = integrate_bed(M, r_eval, H_cheb)
        dH_cheb = ell + w_cheb + rho_eval * dw_cheb
        cheb_pde = M.parent_pde_residuals(r_eval, H_cheb, dH_cheb)
        cheb_defect = rho_eval * dw_cheb - M.frak_undivided(rho_eval, w_cheb, ell)

        # Method 3: Zero-shot evaluation of the 4D parametric LNN-PINN surrogate
        t0 = time.perf_counter()
        pred = B.predict_profile_and_jet(net, t, rho_eval)
        lnn_query_secs = time.perf_counter() - t0
        H_lnn = pred['H']
        Z_lnn = integrate_bed(M, r_eval, H_lnn)
        lnn_pde = M.parent_pde_residuals(r_eval, H_lnn, pred['dH_dr'])

        # Inward sonic boundary probe down toward r = 0.50 + second crossing branch ell_-
        probe_in = reference(M, ell, a, -1, B.INWARD_SONIC_PROBE_SMAX)
        ref_minus_in = reference(M, t['ell_minus'], t['a_minus'], -1, 0.15)
        ref_minus_out = reference(M, t['ell_minus'], t['a_minus'], +1, 0.15)

        rec = {
            'index': t['index'],
            'parameters': {
                'm': t['m'],
                'kappa': t['kappa'],
                'delta': t['delta'],
                'gamma': t['gamma'],
                'gamma_star': t['gamma_star'],
            },
            'crossing': {
                'det_J': t['det_J'],
                'ell_plus': ell,
                'a_plus': a,
                'ell_minus': t['ell_minus'],
                'a_minus': t['a_minus'],
            },
            'taylor_K16': {
                'near_0p9_1p1_max_H_err': float(np.max(np.abs(H_tay_near - H_dop_near))),
                'near_0p9_1p1_max_bed_Z_err': float(np.max(np.abs(Z_tay_near - Z_dop_near))),
                'near_0p9_1p1_max_pde_res': tay_near_pde['radial_momentum_max'],
                'global_0p85_2p0_max_H_err': float(np.max(np.abs(H_tay_glob - H_dop))),
                'H_at_r2': float(H_tay_glob[-1]),
                'seconds': tay_secs,
            },
            'dop853': {
                'inward_reason': ref_in['reason'],
                'outward_reason': ref_out['reason'],
                'nfev_total': ref_in['nfev'] + ref_out['nfev'],
                'seconds': dop_secs,
                'inward_probe_to_0p5_r_stop': float(1.0 - probe_in['extent']),
                'inward_probe_to_0p5_reason': probe_in['reason'],
            },
            'chebyshev_1d': {
                'N_in': cheb_in['N'],
                'N_out': cheb_out['N'],
                'converged': bool(cheb_in['success'] and cheb_out['success']),
                'max_H_diff_vs_dop853': float(np.max(np.abs(H_cheb - H_dop))),
                'max_bed_Z_diff_vs_dop853': float(np.max(np.abs(Z_cheb - Z_dop))),
                'max_defect': float(np.max(np.abs(cheb_defect))),
                'max_pde_res': cheb_pde['radial_momentum_max'],
                'nfev_total': cheb_in['nfev'] + cheb_out['nfev'],
                'seconds': cheb_in['seconds'] + cheb_out['seconds'],
            },
            'lnn_pinn_surrogate': {
                'max_H_err_vs_dop853': float(np.max(np.abs(H_lnn - H_dop))),
                'rms_H_err_vs_dop853': float(np.sqrt(np.mean((H_lnn - H_dop) ** 2))),
                'max_H_err_vs_chebyshev': float(np.max(np.abs(H_lnn - H_cheb))),
                'max_bed_Z_err_vs_dop853': float(np.max(np.abs(Z_lnn - Z_dop))),
                'max_defect': float(np.max(np.abs(pred['defect']))),
                'rms_defect': float(np.sqrt(np.mean(pred['defect'] ** 2))),
                'max_pde_res': lnn_pde['radial_momentum_max'],
                'rms_pde_res': lnn_pde['radial_momentum_rms'],
                'param_grad_norm_mean': pred['param_grad_norm_mean'],
                'query_seconds': lnn_query_secs,
            },
        }
        test_records.append(rec)

        # Save dense plotting curves for representative tuples (tuple 0 for global profile, tuple 1 for sonic stop)
        if t['index'] in (0, 1):
            s_p = np.linspace(1e-3, probe_in['extent'], 160)
            w_p = reference_w(probe_in, s_p)
            r_p = 1.0 - s_p
            H_p = 1.0 - s_p * (ell + w_p)
            Dc_p, _, _ = M.DN(r_p, H_p)

            s_m = np.linspace(1e-3, 0.15, 80)
            r_m = np.concatenate([1.0 - s_m[::-1], [1.0], 1.0 + s_m])
            H_m = np.concatenate([
                1.0 - s_m[::-1] * (t['ell_minus'] + reference_w(ref_minus_in, s_m[::-1])),
                [1.0],
                1.0 + s_m * (t['ell_minus'] + reference_w(ref_minus_out, s_m)),
            ])
            s_out1 = np.linspace(1e-3, 0.35, 90)
            r_out1 = 1.0 + s_out1
            H_out1 = 1.0 + s_out1 * (ell + reference_w(ref_out, s_out1))
            r_p_full = np.concatenate([r_p[::-1], [1.0], r_out1])
            H_p_full = np.concatenate([H_p[::-1], [1.0], H_out1])
            Dc_out1, _, _ = M.DN(r_out1, H_out1)
            Dc_p_full = np.concatenate([Dc_p[::-1], [0.0], Dc_out1])
            grids_payload[str(t['index'])] = {
                'r': r_eval.tolist(),
                'H_dop': H_dop.tolist(),
                'Z_dop': Z_dop.tolist(),
                'eta_dop': (H_dop + Z_dop).tolist(),
                'H_cheb': H_cheb.tolist(),
                'Z_cheb': Z_cheb.tolist(),
                'H_lnn': H_lnn.tolist(),
                'Z_lnn': Z_lnn.tolist(),
                'H_tay_plot': np.where(np.abs(H_tay_glob) <= 14.0, H_tay_glob, np.nan).tolist(),
                'inward_probe_r': r_p_full.tolist(),
                'inward_probe_H': H_p_full.tolist(),
                'inward_probe_Dc': Dc_p_full.tolist(),
                'branch_minus_r': r_m.tolist(),
                'branch_minus_H': H_m.tolist(),
            }

    # Aggregate summary metrics across the 8 held-out test tuples
    tay_near_errs = [r['taylor_K16']['near_0p9_1p1_max_H_err'] for r in test_records]
    tay_near_Z_errs = [r['taylor_K16']['near_0p9_1p1_max_bed_Z_err'] for r in test_records]
    tay_glob_errs = [r['taylor_K16']['global_0p85_2p0_max_H_err'] for r in test_records]
    cheb_diffs = [r['chebyshev_1d']['max_H_diff_vs_dop853'] for r in test_records]
    cheb_Z_diffs = [r['chebyshev_1d']['max_bed_Z_diff_vs_dop853'] for r in test_records]
    cheb_pdes = [r['chebyshev_1d']['max_pde_res'] for r in test_records]
    cheb_secs = [r['chebyshev_1d']['seconds'] for r in test_records]
    dop_secs_all = [r['dop853']['seconds'] for r in test_records]
    lnn_errs = [r['lnn_pinn_surrogate']['max_H_err_vs_dop853'] for r in test_records]
    lnn_rms_errs = [r['lnn_pinn_surrogate']['rms_H_err_vs_dop853'] for r in test_records]
    lnn_Z_errs = [r['lnn_pinn_surrogate']['max_bed_Z_err_vs_dop853'] for r in test_records]
    lnn_defects = [r['lnn_pinn_surrogate']['max_defect'] for r in test_records]
    lnn_pdes = [r['lnn_pinn_surrogate']['max_pde_res'] for r in test_records]
    lnn_qsecs = [r['lnn_pinn_surrogate']['query_seconds'] for r in test_records]

    # Dimensionality scaling comparison (Chebyshev tensor product vs LNN-PINN)
    N_r_tot = B.ANNULUS['cheb'][1] + B.ANNULUS['cheb'][-1]  # 44 radial spectral modes
    M_param = 8  # 8 Chebyshev nodes per preserved symbolic parameter
    scaling = {
        'N_r_modes': N_r_tot,
        'M_per_parameter': M_param,
        'p3_active_box': {
            'tensor_chebyshev_dof': int(N_r_tot * (M_param ** 3)),
            'lnn_pinn_params': B.n_params(B.LNNPINN(in_dim=4, width=32)),
        },
        'p6_unnormalized_f0': {
            'tensor_chebyshev_dof': int(N_r_tot * (M_param ** 6)),
            'lnn_pinn_params': B.n_params(B.LNNPINN(in_dim=7, width=32)),
        },
        'p9_full_preserved_symbols': {
            'tensor_chebyshev_dof': int(N_r_tot * (M_param ** 9)),
            'lnn_pinn_params': B.n_params(B.LNNPINN(in_dim=10, width=32)),
        },
    }

    summary = {
        'git_commit': git_rev(),
        'environment': {
            'python': platform.python_version(),
            'sympy': sympy.__version__,
            'numpy': np.__version__,
            'scipy': scipy.__version__,
            'torch': torch.__version__,
        },
        'reduced_ode_ast': {
            'discovered_lie_dim': ast['basis_dim'],
            'enumerated_rank2_subalgebras': ast['enumerated_subalgebras'],
            'preserved_parameters': ast['preserved_parameters'],
            'preserved_parameter_count': len(ast['preserved_parameters']),
            'first_integrals_count': len(ast['first_integrals']),
            'eliminated_profiles': ast['eliminated_profiles'],
            'gate_1_closed_form_quadrature': ast['has_closed_quadrature'],
            'det_J_f0_symbolic': str(ast['det_J_f0_expr']),
            'gamma_star_f0_symbolic': str(ast['gamma_star_f0_expr']),
        },
        'design': {
            'box': B.BOX,
            'f': B.F_BEND,
            'annulus_r': list(B.ANNULUS['r']),
            'near_window_r': list(B.NEAR_WINDOW),
            'n_train': B.N_TRAIN,
            'n_test': B.N_TEST,
            'seed_train': B.SEED_TRAIN,
            'seed_test': B.SEED_TEST,
        },
        'domain_verification': {
            'train': train_domain,
            'test': test_domain,
        },
        'summary_held_out': {
            'taylor_K16_near_median_H_err': float(np.median(tay_near_errs)),
            'taylor_K16_near_max_H_err': float(np.max(tay_near_errs)),
            'taylor_K16_near_median_bed_Z_err': float(np.median(tay_near_Z_errs)),
            'taylor_K16_global_median_H_err': float(np.median(tay_glob_errs)),
            'taylor_K16_global_max_H_err': float(np.max(tay_glob_errs)),
            'dop853_full_annulus_count': f'{B.N_TEST}/{B.N_TEST}',
            'dop853_mean_seconds_per_tuple': float(np.mean(dop_secs_all)),
            'chebyshev_converged_count': f"{sum(r['chebyshev_1d']['converged'] for r in test_records)}/{B.N_TEST}",
            'chebyshev_max_H_diff_vs_dop853': float(np.max(cheb_diffs)),
            'chebyshev_median_H_diff_vs_dop853': float(np.median(cheb_diffs)),
            'chebyshev_max_bed_Z_diff_vs_dop853': float(np.max(cheb_Z_diffs)),
            'chebyshev_median_bed_Z_diff_vs_dop853': float(np.median(cheb_Z_diffs)),
            'chebyshev_max_pde_res': float(np.max(cheb_pdes)),
            'chebyshev_mean_seconds_per_tuple': float(np.mean(cheb_secs)),
            'lnn_pinn_median_max_H_err': float(np.median(lnn_errs)),
            'lnn_pinn_worst_max_H_err': float(np.max(lnn_errs)),
            'lnn_pinn_median_rms_H_err': float(np.median(lnn_rms_errs)),
            'lnn_pinn_median_bed_Z_err': float(np.median(lnn_Z_errs)),
            'lnn_pinn_worst_bed_Z_err': float(np.max(lnn_Z_errs)),
            'lnn_pinn_median_max_defect': float(np.median(lnn_defects)),
            'lnn_pinn_worst_max_defect': float(np.max(lnn_defects)),
            'lnn_pinn_median_max_pde_res': float(np.median(lnn_pdes)),
            'lnn_pinn_worst_max_pde_res': float(np.max(lnn_pdes)),
            'lnn_pinn_mean_query_seconds_per_tuple': float(np.mean(lnn_qsecs)),
        },
        'lnn_pinn_training': train_log,
        'parameter_dimension_scaling': scaling,
        'held_out_tuples': test_records,
        'appendix_controls': {
            'convex_bowl_f_pos': bowl_control(),
            'general_c2_flux_drift': flux_drift_control(),
            'analytical_tail_bounds': analytical_bounds_control(test_tuples[0]),
        },
        'total_wall_seconds': float(time.perf_counter() - t_start),
    }

    with open(os.path.join(OUT, 'planar_ode_results.json'), 'w') as fh:
        json.dump(summary, fh, indent=2)
    with open(os.path.join(OUT, 'planar_ode_grids.json'), 'w') as fh:
        json.dump(grids_payload, fh)

    print(json.dumps({
        'commit': summary['git_commit'][:7],
        'smooth_annulus_train': f"{train_domain['smooth_on_0p85_to_2p0']}/{B.N_TRAIN}",
        'smooth_annulus_test': f"{test_domain['smooth_on_0p85_to_2p0']}/{B.N_TEST}",
        'taylor_near_max_err': summary['summary_held_out']['taylor_K16_near_max_H_err'],
        'taylor_global_max_err': summary['summary_held_out']['taylor_K16_global_max_H_err'],
        'chebyshev_vs_dop853_max': summary['summary_held_out']['chebyshev_max_H_diff_vs_dop853'],
        'lnn_pinn_median_max_H_err': summary['summary_held_out']['lnn_pinn_median_max_H_err'],
        'lnn_pinn_worst_max_H_err': summary['summary_held_out']['lnn_pinn_worst_max_H_err'],
        'lnn_pinn_worst_pde_res': summary['summary_held_out']['lnn_pinn_worst_max_pde_res'],
        'train_seconds': train_log['seconds'],
        'wall_seconds': summary['total_wall_seconds'],
    }, indent=2))


if __name__ == '__main__':
    main()
