"""Fresh-review identities, independent of the authors' prolongation helpers.

This checks proof steps and compares the root analyzer to a separate explicit
mixed-order prolongation. Necessity is adjudicated in CLASSIFICATION_REVIEW.md;
finite symbolic checks alone are not the maximality argument.
Writes only classification_review.json. Run with python -B.
"""
from pathlib import Path
import hashlib
import json
import time
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REVIEWED_INPUTS = ['CONTRACT.md', 'FIRST_ORDER_DERIVATION.md', 'SLOPE_DERIVATION.md',
                  'research_first_order.py', 'research_slope.py', 'models.py', 'main.py',
                  'classification.py', 'review_classification.py', 'CLASSIFICATION_REVIEW.md',
                  'reductions.py', 'tests/test_reductions.py', 'tests/test_engine.py',
                  'equivalence.py', 'EQUIVALENCE.md']
# Capture before importing author modules. Reject any edit during this review;
# end-only hashes could otherwise attest a version never executed by this run.
INPUT_SNAPSHOT = {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in REVIEWED_INPUTS}

import sympy as s

import main
import models
import research_first_order
import research_slope
import classification
import reductions
import equivalence

t, x, h, u, B = models.t, models.x, models.h, models.u, models.B
g, K, G, m, n = models.g, models.K, models.G, models.m, models.n
w = (h, u, B)
coords = (t, x, *w)
# Explicit ambient jet coordinates, independently constructed, through J3.
js = {(i, a, b): (w[i] if a+b == 0 else
      s.Symbol(f'{w[i]}__{a}_{b}', real=True))
      for i in range(3) for a in range(4) for b in range(4-a)}
rev = {v: k for k, v in js.items()}
yt = tuple(js[i, 1, 0] for i in range(3))
yx = tuple(js[i, 0, 1] for i in range(3))
p, q, r = yx
v, Btx = js[2, 0, 2], js[2, 1, 1]


def total(expr, axis):
    expr = s.sympify(expr)
    out = s.diff(expr, (t, x)[axis])
    for z in expr.free_symbols & rev.keys():
        i, a, b = rev[z]
        out += s.diff(expr, z)*js[i, a+(axis == 0), b+(axis == 1)]
    return s.expand(out)


def direct(C, D, field):
    """Explicit first/second recursive prolongation, on the mixed J2 shell."""
    tau, xi, *eta = map(s.sympify, field)
    et = [total(e, 0)-a*total(tau, 0)-b*total(xi, 0)
          for e, a, b in zip(eta, yt, yx)]
    ex = [total(e, 1)-a*total(tau, 1)-b*total(xi, 1)
          for e, a, b in zip(eta, yt, yx)]
    exx = total(ex[2], 1)-Btx*total(tau, 1)-v*total(xi, 1)
    H, U, Z = eta
    residual = [et[0]+U*p+u*ex[0]+H*q+h*ex[1],
                et[1]+U*q+u*ex[1]+g*(ex[0]+ex[2]),
                et[2]+s.diff(C, u)*U*q+C*ex[1]-s.diff(D, u)*U*v-D*exx
                -s.diff(D, u, 2)*U*q*r-s.diff(D, u)*(ex[1]*r+q*ex[2])]
    f = (-u*p-h*q, -u*q-g*(p+r), D*v+s.diff(D, u)*q*r-C*q)
    return tuple(s.expand(e.subs(dict(zip(yt, f)), simultaneous=True))
                 for e in residual), f


def gate_controls():
    """Read-only in-memory filesystem tests of acceptance and stale rejection."""
    contents = {'snapshot/'+f: (HERE/f).read_bytes() for f in REVIEWED_INPUTS}
    receipt = {
        'all_checks_passed': True,
        'branches': {name: {'passed': True} for name in models.BRANCHES},
        'verdicts': dict.fromkeys(('first_order', 'slope', 'root_analyzer'), 'accepted'),
        'inputs_sha256': dict(INPUT_SNAPSHOT),
    }

    class MemoryPath:
        def __init__(self, value):
            self.value = value.value if isinstance(value, MemoryPath) else str(value)
        def __truediv__(self, value):
            return MemoryPath(self.value+'/'+str(value))
        def exists(self):
            return self.value in contents
        def is_file(self):
            return self.exists()
        def read_bytes(self):
            return contents[self.value]
        def read_text(self, encoding='utf-8'):
            return self.read_bytes().decode(encoding)

    def evaluate(record=receipt):
        contents['snapshot/review.json'] = json.dumps(record).encode()
        with patch.object(classification, 'Path', MemoryPath):
            return classification.review_gate('snapshot/review.json', root='snapshot')

    outcomes = {}
    accepted = evaluate()
    assert accepted['passed'] is True
    outcomes['current_exact_snapshot_accepted'] = True
    original = contents['snapshot/main.py']
    contents['snapshot/main.py'] = original+b'\n# stale source control\n'
    stale = evaluate()
    assert stale['passed'] is False and stale['reason'] == 'reviewed_inputs_changed'
    contents['snapshot/main.py'] = original
    outcomes['changed_source_rejected'] = True
    missing = json.loads(json.dumps(receipt))
    del missing['inputs_sha256']['models.py']
    assert evaluate(missing)['passed'] is False
    outcomes['missing_required_hash_rejected'] = True
    partial = json.loads(json.dumps(receipt))
    del partial['branches']['zero_transport']
    assert evaluate(partial)['passed'] is False
    outcomes['missing_branch_rejected'] = True
    failed = json.loads(json.dumps(receipt))
    failed['branches']['slope_only']['passed'] = False
    assert evaluate(failed)['passed'] is False
    outcomes['failed_branch_rejected'] = True
    rejected = json.loads(json.dumps(receipt))
    rejected['verdicts']['slope'] = 'rejected'
    assert evaluate(rejected)['passed'] is False
    outcomes['rejected_verdict_rejected'] = True
    annotated = dict(receipt, independent_note='Receipt metadata may change without a hash fixed point')
    changed_receipt = evaluate(annotated)
    assert changed_receipt['passed'] is True
    assert changed_receipt['receipt_sha256'] != accepted['receipt_sha256']
    assert 'classification_review.json' not in receipt['inputs_sha256']
    outcomes['receipt_not_its_own_hashed_input'] = True
    return outcomes


def check_adjoint(check, name, integration):
    """Independent affine flow pullbacks realize exp(epsilon ad_X)."""
    basis = [s.Matrix(v) for v in integration['basis']]
    epsilon = s.Symbol('epsilon', real=True)
    algebra = integration['algebra']
    for i, X in enumerate(basis):
        weights = [s.diff(X[j], coord) for j, coord in enumerate(coords)]
        offsets = [s.simplify(X[j]-weights[j]*coord) for j, coord in enumerate(coords)]
        assert all(not z.has(*coords) for z in weights+offsets)
        flow = []
        for coord, weight, offset in zip(coords, weights, offsets):
            # In these bases a component is a translation or a pure dilation;
            # no division by symbolic n-2, n-1, etc. is required.
            assert weight == 0 or offset == 0
            flow.append(coord+epsilon*offset if weight == 0 else coord*s.exp(epsilon*weight))
        inverse_derivative = s.diag(*(s.exp(-epsilon*z) for z in weights))
        errors = []
        for j, Y in enumerate(basis):
            pullback = inverse_derivative*Y.subs(dict(zip(coords, flow)), simultaneous=True)
            represented = sum((basis[k]*algebra['adjoint_flows'][i][k, j]
                               for k in range(len(basis))), s.zeros(5, 1))
            errors.extend(pullback-represented)
        check(f'{name} finite adjoint equals flow pullback for basis {i}', errors)


def check_reductions(check):
    """Direct original-PDE differentiation, independent of chain/graph helpers."""
    records = {}

    def basis_for(name):
        if models.BRANCHES[name]['G']:
            return research_slope.general_solution(name, coords)['basis']
        return tuple(research_first_order.branch_generators(name, coords).values())

    selected = [('grass_generic', 'common', None), ('grass_cubic', 'common', None),
                ('grass_cubic', 'relative', None), ('grass_cubic', 'spatial', None),
                ('zero_transport', 'spatial', None), ('slope_attachment_cubic', 'last', None),
                ('slope_source_cubic', 'last', None)]
    selected += [('slope_only', 'last', exponent) for exponent in range(5)]
    cases = [(name, 'travel', None) for name in models.BRANCHES]+selected
    for name, kind, exponent in cases:
        model, basis = models.branch_model(name), basis_for(name)
        substitutions = {} if exponent is None else {n: s.Integer(exponent)}
        if kind == 'travel':
            reduction = reductions.traveling_reduction(model, basis)
        else:
            if kind == 'last':
                chosen = basis[-1]
            else:
                named = research_first_order.branch_generators(name, coords)
                chosen = named['common_base_scaling']
                if kind == 'relative':
                    chosen = named['relative_scaling']
                if kind == 'spatial':
                    chosen -= named['relative_scaling']
            reduction = reductions.scaling_reduction(model, basis, chosen, substitutions=substitutions)
        label = f'{name}/{kind}/n={exponent}'
        assert reduction['status'] == 'verified_reduction', (label, reduction)
        # Fresh coordinates carry only the chart positivity justified by the
        # returned guard; replace before differentiating the original PDE.
        chart = reduction.get('selected_chart', 'translation')
        tp = s.Symbol('review_t', **({'positive': True} if chart == 'time' else {'real': True}))
        xp = s.Symbol('review_x', **({'positive': True} if chart == 'space' else {'real': True}))
        coordinate_map = {t: tp, x: xp}
        gh, gu, gb = [e.subs(coordinate_map, simultaneous=True) for e in reduction['graph']]
        cell = models.BRANCHES[name]
        flux = K*gu**cell['m'] if cell['K'] else s.S.Zero
        if cell['G']:
            flux -= G*gu**s.sympify(cell['n']).subs(substitutions)*s.diff(gb, xp)
        original = [s.diff(gh, tp)+gu*s.diff(gh, xp)+gh*s.diff(gu, xp),
                    s.diff(gu, tp)+gu*s.diff(gu, xp)+g*(s.diff(gh, xp)+s.diff(gb, xp)),
                    s.diff(gb, tp)+s.diff(flux, xp)]
        invariant = reduction['base_invariant'].subs(coordinate_map, simultaneous=True)
        z = reduction['profile_coordinate']
        pulled = [(factor*eq.subs(z, invariant)).subs(coordinate_map, simultaneous=True)
                  for factor, eq in zip(reduction['row_factors'], reduction['reduced_equations'])]
        check(f'independent original-PDE pullback {label}', [a-b for a, b in zip(original, pulled)])
        assert reduction['leading_system']['leading_matrix_inverted'] is False
        assert reduction['leading_system']['singular_locus_discarded'] is False
        records[label] = {'passed': True, 'chart': reduction.get('selected_chart', 'translation'),
                          'orders': reduction['leading_system']['orders']}
        print(f'PASS independent pullback {label}', flush=True)
    return records


def check_reflection(check):
    """Signed |u|-law reflection, not real noninteger powers of negative u."""
    speed = s.Symbol('review_speed', positive=True)
    ht, ut, Bt = yt
    for sign in (-1, 1):
        velocity = sign*speed
        # Derive Dx flux by the ordinary chain rule, with Dx|u|=sign*u_x.
        flux = K*sign*speed**m-G*speed**n*r
        dx_flux = s.diff(flux, speed)*sign*q+s.diff(flux, r)*v
        old = (ht+velocity*p+h*q, ut+velocity*q+g*(p+r), Bt+dx_flux)
        new_flux = K*(-sign)*speed**m-G*speed**n*(-r)
        # x'=-x, u'=-u: u'_x'=u_x and B'_xx'=B_xx.
        new_dx_flux = s.diff(new_flux, speed)*(-sign)*q
        # The derivative above retains original r=-B'_x', so Dr/Dx'=-B_xx.
        new_dx_flux += s.diff(new_flux, r)*(-v)
        new = (ht+(-velocity)*(-p)+h*q,
               -ut+(-velocity)*q+g*(-p-r), Bt+new_dx_flux)
        check(f'signed reflection off-shell identities speed sign {sign}',
              (new[0]-old[0], new[1]+old[1], new[2]-old[2]))
    reflection = s.Matrix((t, -x, h, -u, B))
    check('reflection Jacobian and involution',
          [reflection.jacobian(coords).det()-1,
           *(reflection.subs(dict(zip(coords, reflection)), simultaneous=True)-s.Matrix(coords))])
    supplied = equivalence.verify_maps()
    assert supplied['all_passed'] is True
    assert supplied['status']['full_local_point_equivalence'] == 'unresolved'
    return {'independent_signed_reflection': True, 'author_map_checks_passed': supplied['check_count'],
            'negative_chart_classification_transport': 'accepted for signed absolute-value flux only',
            'full_equivalence_groupoid': 'not established'}


def run():
    start = time.perf_counter()
    checks, branch_receipts = [], {}

    def check(name, expr):
        values = list(expr) if isinstance(expr, (s.MatrixBase, list, tuple)) else [expr]
        defects = [s.simplify(s.expand(e)) for e in values]
        if any(z != 0 for z in defects):
            raise AssertionError((name, [str(z) for z in defects if z != 0]))
        checks.append(name)

    def arb(name, args=coords):
        return s.Function(name)(*args)

    # First-order projectability and trace eliminations, without author helpers.
    z, zp = s.symbols('z zp', real=True)
    a, b, c = s.symbols('a b c', real=True)
    HH, UU, ZZ = s.symbols('HH UU ZZ', real=True)
    A = s.Matrix([[u, h, 0], [g, u, g], [0, z, 0]])
    J = s.Matrix(3, 3, lambda i, j: s.Symbol(f'J{i}{j}'))
    M = A*J-J*A+s.Matrix([[UU, HH, 0], [0, UU, 0], [0, zp*UU, 0]])
    M += a*A+b*A*A-c*s.eye(3)
    solved = s.solve([s.trace(M), s.trace(A*M)], [HH, UU], dict=True)[0]
    Us = s.Rational(3, 2)*c-a*u-b*(u*u+g*(h+z))
    Hs = (-2*a*h+a*(m-3)*z+b*g*(m-1)*z*(h+z)/u-4*b*h*u
          +b*(m-2)*z*u-s.Rational(3, 2)*c*(m-1)*z/u-c*u/g)
    check('trace solve U', solved[UU]-Us)
    check('trace solve H', solved[HH].subs(zp, (m-1)*z/u)-Hs)
    det_condition = s.trace(A.adjugate()*M).subs(solved).subs(zp, (m-1)*z/u)
    check('h coefficient of determinant', s.diff(det_condition, h)-g*(b*g*m*z+c))
    check('m=1 endpoint remainder', det_condition.subs({m: 1, c: -b*g*z})
          -g*z*(-4*a*u+3*b*g*z)/2)
    check('positive transport exceptional factor', det_condition.subs({b: 0, c: 0})
          -a*g*z*u*(m-3))
    check('K=0 determinant', det_condition.subs(z, 0)+c*(u*u-g*h))
    A0 = A.subs(z, 0)
    e0 = s.Matrix([-2*a*h-4*b*h*u, -a*u-b*(u*u+g*h), arb('Z0')])
    M0 = A0*e0.jacobian(w)-e0.jacobian(w)*A0
    M0 += sum((e0[i]*A0.diff(ww) for i, ww in enumerate(w)), s.zeros(3))
    M0 += a*A0+b*A0*A0
    check('K=0 actual matrix removes tau_x', M0[0, 0]-3*g*h*b)
    check('symmetrizer', s.diag(g/h, 1, g/z)*A-(s.diag(g/h, 1, g/z)*A).T)
    lam = s.Symbol('lambda')
    check('K=0 discriminant', s.discriminant(A0.charpoly(lam).as_expr(), lam)
          -4*g*h*(u*u-g*h)**2)
    l = s.symbols('l0:3')
    rr, ss = s.symbols('r0:3'), s.symbols('s0:3')
    L, P = s.diag(*l), s.Matrix(yx)
    R, S = s.Matrix([rr]), s.Matrix([ss])
    Q = L*L*P*(R*P)[0]-L*P*(R*L*P)[0]+P*(S*L*P)[0]-L*P*(S*P)[0]
    for i in range(3):
        for j in range(3):
            if i != j:
                check(f'quadratic eigenbasis {i},{j}', s.expand(Q[i]).coeff(P[i]*P[j])
                      -(l[i]-l[j])*(l[i]*rr[j]-ss[j]))

    # Independently reconstruct every loadbearing slope projectability step.
    C, D = m*K*u**(m-1), G*u**n
    tau, xi, H, U, Z = [arb(k) for k in ('tau', 'xi', 'H', 'U', 'Z')]
    first_raw, _ = direct(C, s.S.Zero, (tau, xi, H, U, Z))
    Af = s.Matrix([[u, h, 0], [g, u, g], [0, C, 0]])
    ef, P = s.Matrix([H, U, Z]), s.Matrix(yx)
    R, S = s.Matrix([[s.diff(tau, ww) for ww in w]]), s.Matrix([[s.diff(xi, ww) for ww in w]])
    Mf = Af*ef.jacobian(w)-ef.jacobian(w)*Af
    Mf += sum((ef[i]*Af.diff(ww) for i, ww in enumerate(w)), s.zeros(3))
    Mf += (s.diff(tau, t)-s.diff(xi, x))*Af+s.diff(tau, x)*Af*Af-s.diff(xi, t)*s.eye(3)
    Qf = Af*Af*P*(R*P)[0]-Af*P*(R*Af*P)[0]+P*(S*Af*P)[0]-Af*P*(S*P)[0]
    check('unrestricted first-order C plus M p plus Q identity',
          s.Matrix(first_raw)-ef.diff(t)-Af*ef.diff(x)-Mf*P-Qf)
    raw, f = direct(C, D, (tau, xi, H, U, Z))
    first_rules = dict(zip(yt, f))
    mixed_rules = {js[i, 1, 1]: total(f[i], 1) for i in range(2)}
    time_rules = {js[i, 2, 0]: total(f[i], 0).subs(first_rules, simultaneous=True)
                  .subs(mixed_rules, simultaneous=True) for i in range(2)}
    chart = {**first_rules, **mixed_rules, **time_rules}
    for i in range(2):
        for axis in range(2):
            check(f'mixed J2 shell F{i+1} derivative {axis}',
                  total(yt[i]-f[i], axis).subs(chart, simultaneous=True))
    check('slope B_tx projectability', s.diff(raw[2], Btx)-2*D*total(tau, 1))
    tau = arb('tau', (t,))
    raw, _ = direct(C, D, (tau, xi, H, U, Z))
    for i, ww in enumerate((h, u)):
        check(f'slope {ww}_xx projectability', s.diff(raw[2], js[i, 0, 2])
              +D*(s.diff(Z, ww)-r*s.diff(xi, ww)))
    xi, Z = arb('xi', (t, x, B)), arb('Z', (t, x, B))
    raw, _ = direct(C, D, (tau, xi, H, U, Z))
    check('slope xi_B projectability', s.diff(raw[2], v)
          -D*(2*s.diff(xi, x)-s.diff(tau, t)+2*r*s.diff(xi, B))+s.diff(D, u)*U)
    xi = arb('xi', (t, x))
    raw, _ = direct(C, D, (tau, xi, H, U, Z))
    check('slope H_B', s.diff(raw[0], v)-D*s.diff(H, B))
    check('slope U_B', s.diff(raw[1], v)-D*s.diff(U, B))
    H, U = arb('H', (t, x, h, u)), arb('U', (t, x, h, u))
    raw, _ = direct(C, D, (tau, xi, H, U, Z))
    check('slope H_u', s.diff(raw[0], r)+g*s.diff(H, u))
    H = arb('H', (t, x, h))
    raw, _ = direct(C, D, (tau, xi, H, U, Z))
    diffbase = s.diff(tau, t)-s.diff(xi, x)
    water = ((h*s.diff(U, h)+U-s.diff(xi, t)+u*diffbase)*p
             +(H-h*s.diff(H, h)+h*s.diff(U, u)+h*diffbase)*q
             +s.diff(H, t)+u*s.diff(H, x)+h*s.diff(U, x))
    momentum = (g*(-s.diff(U, u)+s.diff(H, h)+diffbase)*p
                +(-h*s.diff(U, h)+U-s.diff(xi, t)+u*diffbase)*q
                +g*(-s.diff(U, u)+s.diff(Z, B)+diffbase)*r
                +s.diff(U, t)+u*s.diff(U, x)+g*(s.diff(H, x)+s.diff(Z, x)))
    check('slope seven hydro DEs reconstruct both residuals',
          (raw[0]-water, raw[1]-momentum))
    T, Lc, t0 = s.symbols('T L t0', real=True)
    d = Lc-T
    Rt, St = arb('R', (t,)), arb('S', (t,))
    hydro = (T*t+t0, Lc*x+Rt, 2*d*h, d*u+s.diff(Rt, t),
             2*d*B-s.diff(Rt, t, 2)*x/g+St)
    raw, _ = direct(C, D, hydro)
    check('slope integrated hydro residuals', raw[:2])
    bed = (D*(T+(2-n)*d-n*s.diff(Rt, t)/u)*v
           +s.diff(D, u)*(T+(2-n)*d-(n-1)*s.diff(Rt, t)/u)*q*r
           +(C*((m-3)*d+(m-1)*s.diff(Rt, t)/u)+s.diff(D, u)*s.diff(Rt, t, 2)/g)*q
           -s.diff(Rt, t)*r-s.diff(Rt, t, 3)*x/g+s.diff(St, t))
    check('slope complete remaining bed identity', raw[2]-bed)
    check('slope plain r removes frame function', s.Poly(s.expand(bed), p, q, r, v)
          .coeff_monomial(r)+s.diff(Rt, t))

    # Root raw DEs must equal the direct mixed-order result after the single
    # J3 lift B_tx = Dx(f3). Its leading B_xxx coefficient is D != 0.
    for name, cell in models.BRANCHES.items():
        branch_start = time.perf_counter()
        print(f'RUN {name}', flush=True)
        model = models.branch_model(name)
        report = main.analyze(**model)
        field = (*report['arbitrary_generator']['xi'], *report['arbitrary_generator']['eta'])
        Cb = cell['m']*K*u**(cell['m']-1) if cell['K'] else s.S.Zero
        Db = G*u**cell['n'] if cell['G'] else s.S.Zero
        direct_raw, fb = direct(Cb, Db, field)
        lifted = [s.expand(e.subs(Btx, total(fb[2], 1))) for e in direct_raw]
        check(f'{name} independent raw residual equality',
              [a-b for a, b in zip(lifted, report['on_shell_equations'])])
        for j, split in enumerate(report['determining_splits']):
            reconstructed = sum(term['coefficient']*s.prod(z**k for z, k in
                                zip(split['jets'], term['powers'])) for term in split['terms'])
            check(f'{name} exact split reconstruction row {j}',
                  reconstructed/split['denominator']-report['on_shell_equations'][j])
            assert split['status'] == 'complete_jet_split'
        if cell['G']:
            check(f'{name} J3 lift leading coefficient', s.diff(total(fb[2], 1), js[2, 0, 3])-Db)
            solution = research_slope.general_solution(name, coords)['coefficients']
        else:
            solution = research_first_order.general_solution(name, coords)['coefficients']
        substituted = {a: b for a, b in zip(field, solution)}
        check(f'{name} integrated solution in every root DE',
              [e.xreplace(substituted).doit() for e in report['determining_equations']])
        integration = report.get('integration', {})
        assert 'general_solution' in integration, (name, integration)
        dimensions = {'grass_generic': 4, 'grass_cubic': 5, 'zero_transport': 5,
                      'slope_attachment_generic': 3, 'slope_attachment_cubic': 4,
                      'slope_source_generic': 3, 'slope_source_cubic': 4, 'slope_only': 4}
        assert integration['dimension'] == dimensions[name], (name, integration['dimension'])
        check(f'{name} root integrated solution equals independent branch result',
              [a-b for a, b in zip(integration['general_solution'], solution)])
        check_adjoint(check, name, integration)
        accepted, _ = direct(Cb, Db, solution)
        check(f'{name} independent final sufficiency', accepted)
        branch_receipts[name] = {
            'raw_determining_equations': len(report['determining_equations']),
            'integrated_solution': [str(z) for z in solution],
            'root_report_classification_status': report['classification_status'],
            'shell_divisors': [str(z) for z in report['normal_form_divisors']],
            'elapsed_seconds': time.perf_counter()-branch_start,
            'passed': True,
        }
        print(f"PASS {name}: {len(report['determining_equations'])} raw DEs", flush=True)

    print('RUN independent reductions, review gate, and signed reflection', flush=True)
    reduction_receipts = check_reductions(check)
    gate_receipts = gate_controls()
    reflection_receipts = check_reflection(check)
    live_hashes = {f: hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in REVIEWED_INPUTS}
    changed = [f for f in REVIEWED_INPUTS if live_hashes[f] != INPUT_SNAPSHOT[f]]
    assert not changed, ('Inputs changed while reviewed; rerun stable version', changed)
    result = {
        'reviewer_role': 'fresh independent mathematical reviewer; not an author',
        'verdicts': {
            'first_order': 'accepted on the declared positive open chart',
            'slope': 'accepted on the declared positive open chart',
            'root_analyzer': 'accepted for unrestricted DE construction in the eight declared cells; qualified as a classifier',
            'reductions': 'accepted for the declared translation and homogeneous diagonal charts',
            'review_gate': 'accepted for exact-version freshness without a receipt self-hash dependency',
            'adjoints': 'accepted as exp(epsilon ad_X), realized by flow pullback',
            'negative_speed_reflection': 'accepted for the signed absolute-value flux only',
        },
        'check_count': len(checks), 'checks': checks, 'all_checks_passed': True,
        'branches': branch_receipts,
        'reduction_cases': reduction_receipts,
        'review_gate_controls': gate_receipts,
        'reflection_review': reflection_receipts,
        'elapsed_seconds': time.perf_counter()-start,
        'inputs_sha256': INPUT_SNAPSHOT,
        'input_snapshot_unchanged_through_execution': True,
        'proof_review': 'CLASSIFICATION_REVIEW.md contains the necessity and coverage adjudication',
        'prior_attempts': [
            {'status': 'failed', 'reason': 'Root classification adapter passed n instead of m to positive-K solver; author repaired'},
            {'status': 'timed_out', 'timeout_seconds': 28,
             'completed_branches': ['grass_generic', 'grass_cubic', 'slope_attachment_generic', 'slope_attachment_cubic'],
             'interpretation': 'Resource limit only; not an obstruction or mathematical failure'},
        ],
        'limitations': ['Finite checks are not the necessity proof',
                        'Model-specific necessity certificates do not supply a universal PDE integration algorithm',
                        'No full point-equivalence groupoid adjudication',
                        'Negative-speed transfer applies only to the signed absolute-value flux',
                        'No 2D, zero-speed or zero-depth classification',
                        'No global PDE existence, shock, or arbitrary-data theorem'],
    }
    (HERE/'classification_review.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    live_gate = classification.review_gate()
    assert live_gate['passed'] is True, live_gate
    print(json.dumps({'checks': len(checks), 'elapsed_seconds': result['elapsed_seconds'],
                      'passed': True}, indent=2))


if __name__ == '__main__':
    run()
