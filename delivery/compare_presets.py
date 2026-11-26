#!/usr/bin/env python3
"""Compare automatically reduced ODEs with the preset profiles of the three symbolic scripts.

The reducer receives only the PDE and a generator. The preset profile or the
preset pulled equation is substituted afterwards. A match means every
automatic ODE equals the preset expression up to a factor free of the profile.
"""
import json
import sympy as sp
from sympy.core.function import AppliedUndef
from lie_reduce.jets import JetSpace
from lie_reduce.spec import PDESpec
from lie_reduce.reduce import reduce


def _proportional(auto, preset):
    auto, preset = sp.simplify(auto), sp.simplify(preset)
    if preset == 0:
        return auto == 0
    ratio = sp.simplify(auto/preset)
    return not (ratio.atoms(AppliedUndef) or ratio.atoms(sp.Derivative)) and ratio != 0


def eulerian_bed_drift():
    """symbolic_sv2022: m=2 bed-drift profile, automatic d_t + b d_B reduction."""
    from lie_reduce.bed import bed_spec
    from symbolic_sv2022 import run as preset_run
    spec, _ = bed_spec(flux='K*u**2')
    b = sp.Symbol('b', real=True)
    result = reduce(spec, (1, 0, 0, 0, b))
    F0, F1, F2 = result.graph.profiles
    zz = result.graph.z
    Y = sp.Function('Y')(zz)
    g = [v for v in spec.positive if str(v) == 'g'][0]
    profile = {F0: 1/sp.sqrt(Y), F1: sp.sqrt(Y), F2: 2 - Y/2 - 1/sp.sqrt(Y)}
    residuals = [sp.simplify(e.subs(profile).doit().subs(g, 1)) for e in result.equations]
    K = [v for v in spec.positive if str(v) == 'K'][0]
    preset = preset_run()['m2_bed_drift_quotient']
    ok = residuals[0] == 0 and residuals[1] == 0 and _proportional(residuals[2], K*Y.diff(zz) + b)
    return {'source': 'symbolic_sv2022.py', 'generator': 'd_t + b d_B', 'automatic_odes': list(map(str, result.equations)),
            'preset_profile_residuals': list(map(str, residuals)), 'preset_quotient': preset, 'match': bool(ok)}


def _radial_spec(names, residuals, functions, independent, positive):
    """Replace derivatives of f(t,r) by jet symbols."""
    jets = JetSpace(independent, tuple(sp.Symbol(n, real=True) for n in names), 2)
    mapping = {}
    for a, f in enumerate(functions):
        for (k, j), v in jets.jets.items():
            if k != a:
                continue
            key = sp.diff(f, *[(x, n) for x, n in zip(independent, j) if n]) if any(j) else f
            mapping[key] = v
    order = sorted(mapping, key=lambda e: -sum(getattr(e, 'derivative_count', 0) for _ in [0]))
    equations = tuple(sp.expand(sp.together(e.doit()).xreplace({k: mapping[k] for k in order})) for e in residuals)
    equations = tuple(sp.numer(sp.together(e)) for e in equations)
    principal = tuple(jets.jet(a, 1, 0) for a in range(len(functions)))
    return PDESpec('radial', jets, equations, principal, (), (), positive=positive), jets


def annular_bed_drift():
    """symbolic_new_model2026: rotation-invariant E2, automatic d_t + c d_B on the (t,r) system."""
    import symbolic_new_model2026 as nm
    t, r = nm.t, nm.r
    functions = [sp.Function(n)(t, r) for n in ('H', 'V', 'W', 'B')]
    raw = nm.residual(*functions)
    spec, jets = _radial_spec(('h', 'V', 'W', 'B'), list(raw), functions, (t, r),
                              (r, jets_h := sp.Symbol('h', real=True), nm.g, nm.K, nm.G))
    spec = PDESpec('E2 radial', jets, spec.equations, spec.principal, (), (),
                   positive=(r, jets.dependent[0], nm.g, nm.K, nm.G))
    c = nm.Cb
    result = reduce(spec, (1, 0, 0, 0, 0, c))
    if result.status != 'verified':
        return {'source': 'symbolic_new_model2026.py', 'status': result.status, 'reason': result.reason, 'match': False}
    zz = result.graph.z
    H, Vp, Wp, Z = (sp.Function(n)(r) for n in ('H', 'V', 'W', 'Z'))
    to_r = {F.subs(zz, r): G for F, G in zip(result.graph.profiles, (H, Vp, Wp, Z))}
    auto = [e.subs(zz, r).subs(to_r).doit() for e in result.equations]
    preset = list(nm.residual(H, Vp, Wp, Z + c*t))
    equal = [_proportional(a, p) for a, p in zip(auto, preset)]
    c1, c2, c3 = sp.symbols('C1 C2 C3', real=True, nonzero=True)
    vs, ws = c1/(r*H), c2/r - nm.f*r/2
    q0 = c3/r - c*r/2
    S = vs**2 + ws**2
    pz = (nm.K*vs - q0/S)/nm.G
    D, N = nm.g*H - vs**2, H*(S/r + nm.f*ws - nm.g*pz)
    slope = [sp.simplify(e.subs({Vp: vs, Wp: ws}).doit().subs({Z.diff(r, 2): pz.diff(r), Z.diff(r): pz}))
             for e in auto]
    weight = sp.simplify(slope[1]/(D*H.diff(r) - N))
    slope_ok = slope[0] == 0 and slope[2] == 0 and not weight.atoms(sp.Derivative) and weight == r/H
    bed_ok = sp.simplify(slope[3]) == 0
    return {'source': 'symbolic_new_model2026.py', 'generator': 'd_t + c d_B on theta-invariant (t,r) chart',
            'automatic_odes': list(map(str, result.equations)), 'equal_to_preset_residuals': equal,
            'integrated_profiles_give_DH_eq_N': bool(slope_ok), 'bed_ode_closed_by_P_Z': bool(bed_ok),
            'match': bool(all(equal) and slope_ok and bed_ok)}


def exchange_swirl():
    """The exchange swirl is separable in time; test whether it is a point-symmetry invariant solution."""
    import symbolic_new_model2026 as nm
    t, r = nm.t, nm.r
    functions = [sp.Function(n)(t, r) for n in ('H', 'V', 'W', 'B', 'a')]
    raw = nm.residual(*functions[:4], functions[4])
    spec, jets = _radial_spec(('h', 'V', 'W', 'B', 'a'), list(raw), functions, (t, r), ())
    lam = nm.kd + nm.ke
    X = (0, 0, 0, 0, 0, sp.exp(-lam*t), -sp.exp(-lam*t))
    shell, _ = spec.shell()
    defects = [sp.simplify(jets.act(e, X).subs(shell, simultaneous=True)) for e in spec.equations]
    return {'source': 'symbolic_new_model2026.py (exchange swirl)',
            'candidate': 'exp(-(k_d+k_e)t)(d_B - d_a)',
            'prolonged_defects': list(map(str, defects)),
            'reading': 'the swirl shift b(t) is generated by this vertical field when the defects vanish; '
                       'a vertical field gives no quotient, so the swirl is a separable family, not a Lie ODE reduction'}


def material_scaling():
    """symbolic_sve2026: Y4 reduction of E_L against the preset T*F(s/T) pullback and first integral."""
    import reproduce_sve2026 as R
    from symbolic_sve2026 import compatible, classify, material_scaling as preset_integral
    from lie_reduce.models import scalar
    rows = []
    generic = preset_integral(classify('M')['bases']['m'][3])
    for exponent in (2, 4):
        spec, basis = scalar('M', exponent)
        result = reduce(spec, basis['Y4'])
        F0 = result.graph.profiles[0]
        zz = result.graph.z
        sym = {F0.diff(zz, 3): R.H, F0.diff(zz, 2): R.C, F0.diff(zz): R.P, F0: R.F}
        auto = result.equations[0].subs(result.graph.z, R.z).xreplace({k.subs(zz, R.z): v for k, v in sym.items()})
        T = sp.Symbol('T', positive=True)
        prof = sp.Function('profile')
        graph = T*prof(R.s/T)
        subs = {sp.diff(prof(R.z), R.z, n): v for n, v in enumerate((R.F, R.P, R.C, R.H))}
        jets = {v: sp.diff(graph, T, i, R.s, j).subs(R.s, R.z*T).doit().xreplace(subs) for (i, j), v in R.JETS.items()}
        pulled = sp.expand(T**2*compatible(exponent).xreplace(jets))
        integral = sp.sympify(generic['first_integral'], locals={'C': R.C, 'P': R.P, 'F': R.F, 'z': R.z,
                                                                 'g': R.g, 'kappa': R.kappa, 'm': R.m})
        binding = sp.sympify(generic['bindings']['V'], locals={'P': R.P, 'F': R.F, 'z': R.z})
        integral = integral.subs(sp.Symbol('V'), binding).subs(R.m, exponent)
        flux_auto = result.first_integrals[0]
        integral_ok = sp.simplify(R.profile_total(integral) - pulled) == 0
        auto_flux_ok = flux_auto['status'] == 'verified' and sp.simplify(R.profile_total(
            flux_auto['flux'].subs(zz, R.z).xreplace({k.subs(zz, R.z): v for k, v in sym.items()})) - auto) == 0
        rows.append({'m': exponent, 'automatic_ode': str(auto), 'preset_pullback': str(pulled),
                     'proportional': bool(_proportional(auto, pulled)),
                     'preset_first_integral_differentiates_to_pullback': bool(integral_ok),
                     'automatic_flux_found': bool(auto_flux_ok)})
    return {'source': 'symbolic_sve2026.py', 'generator': 'Y4 = t d_t + s d_s + phi d_phi', 'rows': rows,
            'match': all(r['proportional'] and r['preset_first_integral_differentiates_to_pullback'] for r in rows)}


def main():
    report = {}
    for name, fn in (('E1_bed_drift', eulerian_bed_drift), ('E2_annular', annular_bed_drift),
                     ('exchange_swirl', exchange_swirl), ('EL_scaling', material_scaling)):
        try:
            report[name] = fn()
        except Exception as exc:
            report[name] = {'status': 'error', 'reason': f'{type(exc).__name__}: {exc}', 'match': False}
    print(json.dumps(report, indent=2, default=str))


if __name__ == '__main__':
    main()
