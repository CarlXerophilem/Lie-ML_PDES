"""Pure symbolic PDE specifications on complete JetSpaces, preserving all symbolic parameters.

No preset bases, no hardcoded generator labelers, no integer exponent coercion, and no manual graphs.
"""
import sympy as sp

from .algebra import canonical_basis_dict, enumerate_subalgebras
from .determining import symmetries
from .jets import JetSpace
from .spec import PDESpec


def euler_spec(exponent=None):
    t, x, h, u, bed = sp.symbols('t x h u B', real=True)
    g, K = sp.symbols('g K', positive=True)
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    jets = JetSpace((t, x), (h, u, bed), 1)
    equations = (
        jets.D(h, 0) + jets.D(h * u, 1),
        jets.D(u, 0) + u * jets.D(u, 1) + g * jets.D(h + bed, 1),
        jets.D(bed, 0) + K * jets.D(u**m, 1),
    )
    params = (g, K) + ((m,) if isinstance(m, sp.Symbol) else ())
    return PDESpec('E1', jets, tuple(map(sp.expand, equations)),
                   tuple(jets.jet(i, 1, 0) for i in range(3)),
                   params, ('h,u,g,K>0', 'm>=1'), positive=(h, u, g, K))


def scalar_spec(model, exponent=None):
    t, s, u = sp.symbols('t s phi', real=True)
    g, k = sp.symbols('g kappa', positive=True)
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    jets = JetSpace((t, s), (u,), 3)
    p, q = jets.jet(0, 1, 0), jets.jet(0, 0, 1)
    a, b, c = jets.jet(0, 2, 0), jets.jet(0, 1, 1), jets.jet(0, 0, 2)
    amplitude = q * a - g * c / q**2
    equation = jets.D(amplitude, 0) - g * jets.D(m * k * p**(m - 1) * b / q, 1)
    if model == 'M':
        equation -= jets.D(p * amplitude / q, 1)
    elif model != 'P':
        raise ValueError(model)
    params = (g, k) + ((m,) if isinstance(m, sp.Symbol) else ())
    return PDESpec(model, jets, (sp.expand(equation),), (jets.jet(0, 3, 0),),
                   params, ('phi_t>0', 'phi_s>0', 'g,kappa>0', 'm>=1'), positive=(p, q, g, k))


def planar_e2_spec(exponent=None):
    """Four Cartesian Saint-Venant-Exner balances on (t, x, y) with symbolic parameters."""
    t, x, y = sp.symbols('t x y', real=True)
    h, u, v, B = sp.symbols('h u v B', real=True)
    g, K, G = sp.symbols('g K G', positive=True)
    f = sp.Symbol('f', real=True)
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    j = JetSpace((t, x, y), (h, u, v, B), 2)
    Dt, Dx, Dy = (lambda e, i=i: j.D(e, i) for i in range(3))
    S = u**2 + v**2
    Factor = S**((m - 1) / sp.Integer(2))
    eqs = (
        Dt(h) + Dx(h * u) + Dy(h * v),
        Dt(u) + u * Dx(u) + v * Dy(u) + g * Dx(h + B) - f * v,
        Dt(v) + u * Dx(v) + v * Dy(v) + g * Dy(h + B) + f * u,
        Dt(B) + Dx(Factor * (K * u - G * Dx(B))) + Dy(Factor * (K * v - G * Dy(B))),
    )
    params = (g, K, G, f) + ((m,) if isinstance(m, sp.Symbol) else ())
    return PDESpec('E2_planar', j, tuple(map(sp.expand, eqs)),
                   tuple(j.jet(a, 1, 0, 0) for a in range(4)),
                   params, ('h>0', 'u^2+v^2>0', 'g,K,G>0'), positive=(h, g, K, G))


def polar_e2_spec(exponent=None):
    """Four polar Saint-Venant-Exner balances on (t, r, theta) with symbolic parameters."""
    t, r, theta = sp.symbols('t r theta', real=True)
    h, V, W, B = sp.symbols('h V W B', real=True)
    g, K, G = sp.symbols('g K G', positive=True)
    f = sp.Symbol('f', real=True)
    m = sp.Symbol('m', real=True) if exponent is None else sp.sympify(exponent)
    j = JetSpace((t, r, theta), (h, V, W, B), 2)
    Dt, Dr, Da = (lambda e, i=i: j.D(e, i) for i in range(3))
    S = V**2 + W**2
    Factor = S**((m - 1) / sp.Integer(2))
    eqs = (
        Dt(h) + Dr(r * h * V) / r + Da(h * W) / r,
        Dt(V) + V * Dr(V) + W * Da(V) / r - W**2 / r + g * Dr(h + B) - f * W,
        Dt(W) + V * Dr(W) + W * Da(W) / r + V * W / r + g * Da(h + B) / r + f * V,
        Dt(B) + Dr(r * Factor * (K * V - G * Dr(B))) / r + Da(Factor * (K * W - G * Da(B) / r)) / r,
    )
    params = (g, K, G, f) + ((m,) if isinstance(m, sp.Symbol) else ())
    return PDESpec('E2_polar', j, tuple(map(sp.expand, eqs)),
                   tuple(j.jet(a, 1, 0, 0) for a in range(4)),
                   params, ('r>0', 'h>0', 'V^2+W^2>0', 'g,K,G>0'), positive=(r, h, g, K, G))


def exchange_spec():
    """Five-balance rotating sediment-exchange system on (t, r, theta) with symbolic parameters."""
    t, r, theta = sp.symbols('t r theta', real=True)
    h, V, W, B, A = sp.symbols('h V W B a', real=True)
    g, K, G = sp.symbols('g K G', positive=True)
    omega, kd, ke, Da = sp.symbols('Omega k_d k_e D_a', real=True)
    j = JetSpace((t, r, theta), (h, V, W, B, A), 2)
    Dt, Dr, Da_th = (lambda e, i=i: j.D(e, i) for i in range(3))
    S = V**2 + W**2
    J_ex = kd * A - ke * B
    eqs = (
        Dt(h) + Dr(r * h * V) / r + Da_th(h * W) / r,
        Dt(V) + V * Dr(V) + W * Da_th(V) / r - W**2 / r + g * Dr(h + B) - 2 * omega * W - omega**2 * r,
        Dt(W) + V * Dr(W) + W * Da_th(W) / r + V * W / r + g * Da_th(h + B) / r + 2 * omega * V,
        Dt(B) + Dr(r * S * (K * V - G * Dr(B))) / r + Da_th(S * (K * W - G * Da_th(B) / r)) / r - J_ex,
        Dt(A) + Dr(r * (A * V - Da * h * Dr(A / h))) / r + Da_th(A * W - Da * h * Da_th(A / h) / r) / r + J_ex,
    )
    return PDESpec('E_exch', j, tuple(map(sp.expand, eqs)),
                   tuple(j.jet(k, 1, 0, 0) for k in range(5)),
                   (g, K, G, omega, kd, ke, Da), ('r>0', 'h>0', 'g,K,G>0'), positive=(r, h, g, K, G))


def discover_and_enumerate(spec, degree=1, exponent=None, max_combo_terms=2):
    """Discover point algebra on complete JetSpace and enumerate closed rank-(d-1) subalgebras."""
    found = symmetries(spec, degree=degree, exponent=exponent)
    coords = spec.jets.independent + spec.jets.dependent
    prefix = 'Y' if len(spec.jets.dependent) == 1 else 'X'
    basis = canonical_basis_dict(found['basis'], coords, prefix=prefix)
    subalgebras = enumerate_subalgebras(basis, coords, len(spec.jets.independent),
                                        max_combo_terms=max_combo_terms)
    return spec, basis, subalgebras
