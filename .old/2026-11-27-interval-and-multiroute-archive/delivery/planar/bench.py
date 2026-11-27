"""Declared benchmark design for the planar E2 crossing (fixed before any training run).

Parameters nu = (m, kappa=K/G, delta=gamma_*-gamma) with gamma=c/G, so delta>0 means det J_* < 0 (saddle).
Stage A is r in [0.9, 1.1] and stage B is r in [0.5, 2]; both are radial slices transverse to <R, T_c>.
The three networks share the ansatz H = 1 + rho(ell + w_hat), w_hat = rho R(rho_hat, nu_hat), the same
training tuples, radial nodes, optimizer, iteration budget and about 1.25k trainable parameters; they
differ in architecture and loss.
"""
import time

import numpy as np
import torch

from .cands import Net, cheb_side
from .model import Anchor, cstar

torch.set_default_dtype(torch.float64)

F_BEND = 0.0
BOX = {'m': (1.5, 3.5), 'kappa': (2.0, 10.0), 'delta': (1.0, 3.0)}
NEAR_BOX = {'m': (1.5, 3.5), 'kappa': (2.0, 10.0), 'delta': (0.05, 0.25)}
REVIEW_BOX = {'m': (2.9, 3.1), 'K': (0.99, 1.01), 'G': (0.99, 1.01), 'c': (-7.05, -6.95)}
SEED_TRAIN, SEED_TEST = 27, 29
N_TRAIN, N_TEST = 48, 8
STAGES = {
    'A': {'r': (0.9, 1.1), 'sides': {1: 0.1, -1: 0.1}, 'rc': 0.0, 'rs': 0.1, 'nodes': 54, 'cheb': {1: 12, -1: 12}},
    'B': {'r': (0.5, 2.0), 'sides': {1: 1.0, -1: 0.5}, 'rc': 0.25, 'rs': 0.75, 'nodes': 96, 'cheb': {1: 28, -1: 24}},
}
ROUTES = {
    'chebyshev': 'Chebyshev collocation per tuple (classical)',
    'dop853': 'DOP853 from the Taylor germ (reference only)',
    'pinn': 'plain residual PINN: tanh MLP 4-32-32-1, raw residual Delta_c H\' - N',
    'rf': 'random-feature tanh x Chebyshev network, defect loss (AI-designed)',
    'gated': 'LNN-style gated cell, defect loss',
}
LBFGS_ITERS = 3000


def sample(box, n, seed):
    rng = np.random.default_rng(seed)
    keys = list(box)
    u = rng.random((n, len(keys)))
    return [{k: float(box[k][0] + (box[k][1] - box[k][0])*u[i, j]) for j, k in enumerate(keys)} for i in range(n)]


def nu_hat(t):
    return [(t['m'] - 2.5)/1.0, (t['kappa'] - 6.0)/4.0, (t['delta'] - 2.0)/1.0]


def tuple_model(t, f=F_BEND):
    """Float Anchor, branch data and gamma for a (m, kappa, delta) tuple."""
    gs = cstar(t['m'], t['kappa'], f)
    gamma = gs - t['delta']
    M = Anchor(t['m'], t['kappa'], gamma, f)
    det, br = M.slopes()
    return M, float(gamma), float(gs), float(det), br


def radial_nodes(stage):
    """Chebyshev nodes on the stage slice in rho, excluding |rho| < 1e-3 (the crossing is imposed exactly)."""
    st = STAGES[stage]
    lo, hi = -st['sides'][-1], st['sides'][1]
    n = st['nodes']
    k = np.arange(n)
    x = 0.5*(lo + hi) + 0.5*(hi - lo)*np.cos((2*k + 1)*np.pi/(2*n))
    return np.sort(x[np.abs(x) >= 1e-3])


# ---------------------------------------------------------------- symbolic-AST torch operator
_COMPILED_FRAK = None


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


def _get_compiled_frak():
    global _COMPILED_FRAK
    if _COMPILED_FRAK is not None:
        return _COMPILED_FRAK
    import sympy as sp
    from symbolic_new_model2026 import discover_planar_e2

    spec, _, _, red = discover_planar_e2()
    z = red.graph.z
    F0 = red.target_profile
    dF0 = sp.diff(F0, z)
    eq = red.reduced_equations[0]

    # Extract Delta_c * H' - N == 0 directly from the reduced equation (Delta_c H' - N)/H == 0
    Dc_sym = sp.cancel(F0 * sp.diff(eq, dF0))
    N_sym = sp.cancel(-F0 * sp.expand(eq - sp.diff(eq, dF0) * dF0))

    # Nondimensionalize at g = G = C1 = C2 = 1, K = kappa, c = gamma, and solve N(1, 1) == 0 for C3
    H_s, rho_s, w_s, ell_s, kap_s, gam_s = sp.symbols('H_s rho_s w_s ell_s kappa_s gamma_s', real=True)
    m_s = next(p for p in spec.parameters if str(p) == 'm')
    f_s = next(p for p in spec.parameters if str(p) == 'f')
    g_s = next(p for p in spec.parameters if str(p) == 'g')
    K_s = next(p for p in spec.parameters if str(p) == 'K')
    G_s = next(p for p in spec.parameters if str(p) == 'G')
    c_s, C1_s, C2_s, C3_s = sp.symbols('c C1 C2 C3', real=True)

    nd_sub = {g_s: 1, G_s: 1, K_s: kap_s, c_s: gam_s, C1_s: 1, C2_s: 1, F0: H_s}
    Dc_nd = sp.cancel(Dc_sym.subs(nd_sub))
    N_nd = sp.together(N_sym.subs(nd_sub))
    C3_anchor = sp.solve(N_nd.subs({z: 1, H_s: 1}), C3_s, simplify=False)[0]
    N_anchored = N_nd.subs(C3_s, C3_anchor)

    chart_sub = {z: 1 + rho_s, H_s: 1 + rho_s * (ell_s + w_s)}
    Dc_ast = Dc_nd.subs(chart_sub)
    N_ast = N_anchored.subs(chart_sub)
    _COMPILED_FRAK = (Dc_ast, N_ast, (rho_s, w_s, m_s, kap_s, gam_s, ell_s, f_s))
    return _COMPILED_FRAK


def frak_parts(rho, w, P):
    Dc_ast, N_ast, (rho_s, w_s, m_s, kap_s, gam_s, ell_s, f_s) = _get_compiled_frak()
    env = {
        rho_s: rho,
        w_s: w,
        m_s: P['m'],
        kap_s: P['kappa'],
        gam_s: P['gamma'],
        ell_s: P['ell'],
        f_s: P['f'],
    }
    return _eval_sympy_torch(Dc_ast, env), _eval_sympy_torch(N_ast, env)


# ---------------------------------------------------------------- networks
class MLP(torch.nn.Module):
    kind = 'mlp'

    def __init__(self, width=32):
        super().__init__()
        self.l1, self.l2, self.l3 = torch.nn.Linear(4, width), torch.nn.Linear(width, width), torch.nn.Linear(width, 1)

    def forward(self, rh, nu):
        x = torch.cat([rh[:, None], nu], 1)
        return self.l3(torch.tanh(self.l2(torch.tanh(self.l1(x)))))[:, 0]

    def export(self):
        return {'layers': [(l.weight.detach().numpy().copy(), l.bias.detach().numpy().copy()) for l in (self.l1, self.l2, self.l3)]}


class RF(torch.nn.Module):
    kind = 'rf'

    def __init__(self, J, hidden=14, seed=SEED_TRAIN):
        super().__init__()
        g = np.random.default_rng(seed)
        self.Wf = torch.tensor(g.normal(size=(hidden, 3)))
        self.bf = torch.tensor(g.normal(size=hidden))
        self.A = torch.nn.Parameter(torch.zeros(J, 4 + hidden))

    def forward(self, rh, nu):
        phi = torch.cat([torch.ones_like(rh)[:, None], nu, torch.tanh(nu @ self.Wf.T + self.bf)], 1)
        coef = phi @ self.A.T
        T = [torch.ones_like(rh), rh]
        for _ in range(2, self.A.shape[0]):
            T.append(2*rh*T[-1] - T[-2])
        return (torch.stack(T[:self.A.shape[0]], 1)*coef).sum(1)

    def export(self):
        return {'A': self.A.detach().numpy().copy(), 'Wf': self.Wf.numpy().copy(), 'bf': self.bf.numpy().copy()}


class Gated(torch.nn.Module):
    """v0 = tanh(A x + b), v1 = v0 + tanh(d) * tanh(W v0), R = sum_i v1_i ((1, nu) Theta)_i."""
    kind = 'gated'

    def __init__(self, width=32):
        super().__init__()
        self.inp = torch.nn.Linear(4, width)
        self.W = torch.nn.Parameter(torch.randn(width, width)/np.sqrt(width))
        self.d = torch.nn.Parameter(torch.zeros(width))
        self.Theta = torch.nn.Parameter(0.1*torch.randn(4, width)/np.sqrt(width))

    def forward(self, rh, nu):
        v0 = torch.tanh(self.inp(torch.cat([rh[:, None], nu], 1)))
        v1 = v0 + torch.tanh(self.d)*torch.tanh(v0 @ self.W.T)
        coef = torch.cat([torch.ones_like(rh)[:, None], nu], 1) @ self.Theta
        return (v1*coef).sum(1)

    def export(self):
        return {'A': self.inp.weight.detach().numpy().copy(), 'b': self.inp.bias.detach().numpy().copy(),
                'W': self.W.detach().numpy().copy(), 'd': self.d.detach().numpy().copy(),
                'Theta': self.Theta.detach().numpy().copy()}


def make_net(route, stage):
    torch.manual_seed(SEED_TRAIN)
    if route == 'pinn':
        return MLP()
    if route == 'rf':
        return RF(J=8, hidden=150) if stage == 'A' else RF(J=14, hidden=85)
    if route == 'gated':
        return Gated()
    raise ValueError(route)


def n_params(net):
    return int(sum(p.numel() for p in net.parameters()))


def batch(tuples, stage, masks=None):
    """Flattened training tensors: rho, nu_hat and operator constants per point."""
    st = STAGES[stage]
    nodes = radial_nodes(stage)
    rows = []
    for i, t in enumerate(tuples):
        keep = nodes if masks is None else nodes[masks[i]]
        for rho in keep:
            rows.append([rho] + nu_hat(t) + [t['m'], t['kappa'], t['gamma'], t['ell']])
    X = torch.tensor(np.array(rows))
    rho = X[:, 0].clone().requires_grad_(True)
    P = {'m': X[:, 4], 'kappa': X[:, 5], 'gamma': X[:, 6], 'ell': X[:, 7], 'f': F_BEND}
    return rho, X[:, 1:4], P, st


def w_and_dw(net, rho, nu, st, create_graph=True):
    rh = (rho - st['rc'])/st['rs']
    w = rho*net(rh, nu)
    dw, = torch.autograd.grad(w.sum(), rho, create_graph=create_graph)
    return w, dw


def residuals(net, rho, nu, P, st, loss):
    w, dw = w_and_dw(net, rho, nu, st)
    Dc, N = frak_parts(rho, w, P)
    if loss == 'raw':
        return Dc*(P['ell'] + w + rho*dw) - N
    return rho*dw - (N/Dc - P['ell'] - w)


def train(route, stage, tuples, masks=None, iters=LBFGS_ITERS):
    net = make_net(route, stage)
    rho, nu, P, st = batch(tuples, stage, masks)
    loss_kind = 'raw' if route == 'pinn' else 'defect'
    opt = torch.optim.LBFGS(net.parameters(), lr=1.0, max_iter=iters, max_eval=int(1.25*iters), history_size=50,
                            tolerance_grad=1e-14, tolerance_change=1e-16, line_search_fn='strong_wolfe')
    evals = [0]

    def closure():
        opt.zero_grad()
        r = residuals(net, rho, nu, P, st, loss_kind)
        L = torch.mean(r*r)
        L.backward()
        evals[0] += 1
        return L
    t0 = time.perf_counter()
    opt.step(closure)
    secs = time.perf_counter() - t0
    r = residuals(net, rho, nu, P, st, loss_kind).detach().numpy()
    d = residuals(net, rho, nu, P, st, 'defect').detach().numpy()
    return net, {'loss': loss_kind, 'final_rms_loss_residual': float(np.sqrt(np.mean(r*r))),
                 'train_max_defect': float(np.max(np.abs(d))), 'loss_evaluations': evals[0],
                 'points': int(rho.shape[0]), 'parameters': n_params(net), 'seconds': secs}


def predict(net, t, stage, rho):
    """w_hat at float rho for one tuple (torch forward pass)."""
    st = STAGES[stage]
    r = torch.tensor(np.asarray(rho, float))
    nu = torch.tensor([nu_hat(t)]*len(r))
    with torch.no_grad():
        return (r*net((r - st['rc'])/st['rs'], nu)).numpy()


def as_candidate(kind, weights, t, stage, nu=None):
    """Interval-capable candidate for the certifier; nu defaults to the point nu_hat(t)."""
    st = STAGES[stage]
    return Net(kind, weights, st['rc'], st['rs'], nu_hat(t) if nu is None else nu)


def save_weights(path, kind, weights):
    flat = {'kind': kind}
    if kind == 'mlp':
        for i, (W, b) in enumerate(weights['layers']):
            flat[f'W{i}'], flat[f'b{i}'] = W, b
    else:
        flat.update(weights)
    np.savez(path, **flat)


def load_weights(path):
    z = np.load(path, allow_pickle=False)
    kind = str(z['kind'])
    if kind == 'mlp':
        n = sum(1 for k in z.files if k.startswith('W'))
        return kind, {'layers': [(z[f'W{i}'], z[f'b{i}']) for i in range(n)]}
    return kind, {k: z[k] for k in z.files if k != 'kind'}


def chebyshev_candidate(coeffs, dom, side):
    return cheb_side(np.asarray(coeffs, float), dom, side)
