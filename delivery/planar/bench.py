"""Irreducible planar E2 ODE surrogate layer: symbolic-parameter LNN-PINN only.

Active symbolic parameter space:
    nu = (m, k = K/G, delta = gamma_*(m, k) - c/G) in [1.5, 3.5] x [2, 10] x [1, 3],
where det J_*(nu) = -3 * 2^((1-m)/2) * delta < 0 guarantees two analytic crossing germs.

Radial domain:
    r in [0.85, 2.0] (s_in = 0.15, s_out = 1.0), where every parameter tuple in the box
    stays strictly inside the smooth physical chart (H > 0, S > 0, Delta_c != 0 away from r = 1).
    LNN-PINN trains 100% physics-only from the live SymPy ReducedODE AST with zero DOP853
    labels and zero DOP853 domain-masking oracle.
"""
import time
import numpy as np
import torch

from .model import Anchor, compiled_planar_ast, gamma_star

torch.set_default_dtype(torch.float64)

F_BEND = 0.0
BOX = {'m': (1.5, 3.5), 'kappa': (2.0, 10.0), 'delta': (1.0, 3.0)}
SEED_TRAIN, SEED_TEST = 27, 29
N_TRAIN, N_TEST = 48, 8

ANNULUS = {
    'r': (0.85, 2.0),
    'sides': {1: 1.0, -1: 0.15},
    'rc': 0.425,
    'rs': 0.575,
    'nodes': 84,
    'cheb': {1: 28, -1: 16},
}
NEAR_WINDOW = (0.9, 1.1)
INWARD_SONIC_PROBE_SMAX = 0.5  # probes down toward r = 0.5 to illustrate physical sonic stop Delta_c -> 0
LBFGS_ITERS = 3000


def sample(box, n, seed):
    rng = np.random.default_rng(seed)
    keys = list(box)
    u = rng.random((n, len(keys)))
    return [{k: float(box[k][0] + (box[k][1] - box[k][0]) * u[i, j]) for j, k in enumerate(keys)} for i in range(n)]


def nu_hat(t):
    """Affine normalization of nu = (m, k, delta) onto [-1, 1]^3."""
    return [(t['m'] - 2.5) / 1.0, (t['kappa'] - 6.0) / 4.0, (t['delta'] - 2.0) / 1.0]


def tuple_model(t, f=F_BEND):
    """Build Anchor, exact threshold gamma_*, and Briot-Bouquet branch data for tuple t."""
    gs = gamma_star(t['m'], t['kappa'], f)
    gamma = gs - t['delta']
    M = Anchor(t['m'], t['kappa'], gamma, f)
    det, br = M.slopes()
    return M, float(gamma), float(gs), float(det), br


def radial_nodes():
    """Chebyshev collocation nodes in rho = r - 1 on [-0.15, 1.0], excluding |rho| < 1e-3."""
    lo, hi = -ANNULUS['sides'][-1], ANNULUS['sides'][1]
    n = ANNULUS['nodes']
    k = np.arange(n)
    x = 0.5 * (lo + hi) + 0.5 * (hi - lo) * np.cos((2.0 * k + 1.0) * np.pi / (2.0 * n))
    return np.sort(x[np.abs(x) >= 1e-3])


def _eval_sympy_torch(node, env):
    if node in env:
        return env[node]
    if node.is_Number:
        return float(node)
    if node.is_Add:
        acc = 0.0
        for arg in node.args:
            acc = acc + _eval_sympy_torch(arg, env)
        return acc
    if node.is_Mul:
        acc = 1.0
        for arg in node.args:
            acc = acc * _eval_sympy_torch(arg, env)
        return acc
    if node.is_Pow:
        base_v = _eval_sympy_torch(node.base, env)
        if node.exp.is_Integer:
            return base_v ** int(node.exp)
        return base_v ** _eval_sympy_torch(node.exp, env)
    raise ValueError(f'Unsupported SymPy AST node in torch operator: {node}')


def frak_parts_torch(rho, w, P):
    """Evaluate (Delta_c, N) in PyTorch directly on the live SymPy ReducedODE AST."""
    ast = compiled_planar_ast()
    Dc_ast, N_ast = ast['Dc_chart_ast'], ast['N_chart_ast']
    rho_s, w_s, m_s, k_s, gam_s, ell_s, f_s = ast['chart_symbols']
    env = {
        rho_s: rho,
        w_s: w,
        m_s: P['m'],
        k_s: P['kappa'],
        gam_s: P['gamma'],
        ell_s: P['ell'],
        f_s: P['f'],
    }
    return _eval_sympy_torch(Dc_ast, env), _eval_sympy_torch(N_ast, env)


class LNNPINN(torch.nn.Module):
    """Gated liquid residual block (Tao, Wang & Liu 2026) learning the crossing-exact remainder:
        v_0 = tanh(A x + b),   v_1 = v_0 + tanh(d) * tanh(W v_0),
        R_theta(rho_hat, nu_hat) = sum_i v_{1,i} ((1, nu_hat) Theta)_i,
        H_theta(r; nu) = 1 + ell_+(nu) * rho + rho^2 * R_theta(rho_hat, nu_hat).
    """

    def __init__(self, in_dim=4, width=32):
        super().__init__()
        self.inp = torch.nn.Linear(in_dim, width)
        self.W = torch.nn.Parameter(torch.randn(width, width) / np.sqrt(width))
        self.d = torch.nn.Parameter(torch.zeros(width))
        self.Theta = torch.nn.Parameter(0.005 * torch.randn(in_dim, width) / np.sqrt(width))

    def forward(self, rh, nu):
        x = torch.cat([rh[:, None], nu], dim=1)
        v0 = torch.tanh(self.inp(x))
        v1 = v0 + torch.tanh(self.d) * torch.tanh(v0 @ self.W.T)
        coef = torch.cat([torch.ones_like(rh)[:, None], nu], dim=1) @ self.Theta
        return (v1 * coef).sum(dim=1)

    def export(self):
        return {
            'A': self.inp.weight.detach().numpy().copy(),
            'b': self.inp.bias.detach().numpy().copy(),
            'W': self.W.detach().numpy().copy(),
            'd': self.d.detach().numpy().copy(),
            'Theta': self.Theta.detach().numpy().copy(),
        }


def n_params(net):
    return int(sum(p.numel() for p in net.parameters()))


def build_training_batch(tuples):
    """Pure physics-only collocation grid on r in [0.85, 2.0] x 48 tuples (zero DOP853 oracle)."""
    nodes = radial_nodes()
    rows = []
    for t in tuples:
        nh = nu_hat(t)
        for rho in nodes:
            rows.append([rho, nh[0], nh[1], nh[2], t['m'], t['kappa'], t['gamma'], t['ell']])
    X = torch.tensor(np.array(rows, dtype=float))
    rho = X[:, 0].clone().requires_grad_(True)
    nu = X[:, 1:4]
    P = {'m': X[:, 4], 'kappa': X[:, 5], 'gamma': X[:, 6], 'ell': X[:, 7], 'f': F_BEND}
    return rho, nu, P


def w_and_dw(net, rho, nu, create_graph=True):
    rh = (rho - ANNULUS['rc']) / ANNULUS['rs']
    w = rho * net(rh, nu)
    dw, = torch.autograd.grad(w.sum(), rho, create_graph=create_graph)
    return w, dw


def desingularized_defect(net, rho, nu, P, create_graph=True):
    w, dw = w_and_dw(net, rho, nu, create_graph=create_graph)
    Dc, N = frak_parts_torch(rho, w, P)
    return rho * dw - (N / Dc - P['ell'] - w)


def train_lnn_pinn(tuples, adam_iters=400, iters=LBFGS_ITERS, seed=SEED_TRAIN):
    torch.manual_seed(seed)
    net = LNNPINN(in_dim=4, width=32)
    rho, nu, P = build_training_batch(tuples)
    t0 = time.perf_counter()

    # Stage 1: Adam warm-up smoothly enters the physical chart basin (H > 0, Delta_c != 0)
    adam = torch.optim.Adam(net.parameters(), lr=3e-3)
    for _ in range(adam_iters):
        adam.zero_grad()
        res_a = desingularized_defect(net, rho, nu, P, create_graph=True)
        loss_a = torch.mean(res_a * res_a)
        loss_a.backward()
        adam.step()
    warmup_rms = float(torch.sqrt(loss_a).item())

    # Stage 2: L-BFGS refinement with domain-positivity line-search guard
    opt = torch.optim.LBFGS(
        net.parameters(), lr=1.0, max_iter=iters, max_eval=int(1.25 * iters),
        history_size=60, tolerance_grad=1e-14, tolerance_change=1e-16,
        line_search_fn='strong_wolfe',
    )
    evals = [0]

    def closure():
        opt.zero_grad()
        w, dw = w_and_dw(net, rho, nu, create_graph=True)
        H = 1.0 + rho * (P['ell'] + w)
        if bool((H <= 1e-4).any()):
            return torch.tensor(1e10, dtype=torch.float64)
        Dc, N = frak_parts_torch(rho, w, P)
        res = rho * dw - (N / Dc - P['ell'] - w)
        loss = torch.mean(res * res)
        if not torch.isfinite(loss):
            return torch.tensor(1e10, dtype=torch.float64)
        loss.backward()
        evals[0] += 1
        return loss

    opt.step(closure)
    secs = time.perf_counter() - t0
    res_np = desingularized_defect(net, rho, nu, P, create_graph=False).detach().numpy()
    return net, {
        'model': 'LNN-PINN (width-32 gated liquid residual block, crossing-exact Briot-Bouquet prefix)',
        'optimizer': f'Adam ({adam_iters} steps, lr=3e-3) + L-BFGS (strong_wolfe, max_iter={iters})',
        'loss': 'desingularized Briot-Bouquet defect: rho * dw/drho - (N/Delta_c - ell_+ - w)',
        'domain_oracle_used': False,
        'profile_labels_used': False,
        'parameters': n_params(net),
        'collocation_points': int(rho.shape[0]),
        'n_train_tuples': len(tuples),
        'nodes_per_tuple': int(rho.shape[0] // len(tuples)),
        'adam_warmup_rms_defect': warmup_rms,
        'lbfgs_loss_evaluations': int(evals[0]),
        'train_rms_defect': float(np.sqrt(np.mean(res_np * res_np))),
        'train_max_defect': float(np.max(np.abs(res_np))),
        'seconds': float(secs),
    }


def predict_profile_and_jet(net, t, rho):
    """Evaluate H_theta(r; nu), dH_theta/dr, w_theta(rho), dw_theta/drho, and ||dH_theta/dnu||."""
    rho_t = torch.tensor(np.asarray(rho, dtype=float), requires_grad=True)
    nu_t = torch.tensor([nu_hat(t)] * len(rho_t), dtype=torch.float64, requires_grad=True)
    rh = (rho_t - ANNULUS['rc']) / ANNULUS['rs']
    R_val = net(rh, nu_t)
    w_t = rho_t * R_val
    dw_t, = torch.autograd.grad(w_t.sum(), rho_t, create_graph=False, retain_graph=True)
    dR_dnu, = torch.autograd.grad(R_val.sum(), nu_t, create_graph=False)

    rho_np = rho_t.detach().numpy()
    w_np = w_t.detach().numpy()
    dw_np = dw_t.detach().numpy()
    ell = float(t['ell'])
    H_np = 1.0 + rho_np * (ell + w_np)
    dH_np = ell + w_np + rho_np * dw_np
    P = {'m': t['m'], 'kappa': t['kappa'], 'gamma': t['gamma'], 'ell': ell, 'f': F_BEND}
    with torch.no_grad():
        Dc, N = frak_parts_torch(rho_t.detach(), w_t.detach(), P)
        defect_np = (rho_t.detach() * dw_t.detach() - (N / Dc - ell - w_t.detach())).numpy()
    return {
        'w': w_np,
        'dw': dw_np,
        'H': H_np,
        'dH_dr': dH_np,
        'defect': defect_np,
        'param_grad_norm_mean': float(torch.linalg.vector_norm(dR_dnu, dim=1).mean().item()),
    }
