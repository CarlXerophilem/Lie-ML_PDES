"""Reproducible nine-subsection printed-SVE demo in (s,t,phi) coordinates.

Run: python -m symm.LieSymm.scalar2026.demo --out build/NEW-DIRECTORY
The output directory must not exist. No pure PINN, source rewriting or E/M
model substitution is performed. Numerical examples use constructed data.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import time

from .api import (
    backend, derive_reduction, compute_ode_series, exact_solution_checks,
    traveling_quadrature, source_audit, SOURCE_SHA256,
)


def write_json(path, value):
    path.write_text(json.dumps(backend().jsonable(value), indent=2, ensure_ascii=False,
                              allow_nan=False), encoding='utf-8')


def inventory():
    """One row per subsection; numbered intermediate equations are mapped too."""
    b = backend()
    details = {
        '3.1': ('identity_outside_positive_velocity_chart', 'Arbitrary F(s); m=3 zero-velocity control.', 'none'),
        '3.2': ('undefined_pde_chart', 'phi_s=0. No divided-PDE solution can be asserted.', 'none'),
        '3.3': ('no_invariant_graph', 'Q=1 cannot vanish.', 'none'),
        '3.4': ('first_integral_series_numerical_and_exact_subfamilies',
                "L F''=I0 lowers order 3 to 2; affine profiles and the cubic power profile are exact. General closed form unresolved.", '(24)'),
        '3.5': ('series_numerical_and_exact_power_subfamily',
                'm=3 only. Exact power profile; derivative/scaling reductions give a first-order rational equation. General closed form unresolved.', '(25),(26),(27)'),
        '3.6': ('regular_exact_parametric_quadrature',
                "B(F')F''=I0; exact parametric quadrature for I0!=0, affine family for I0=0. B=0 requires a separate chart.", '(28),(29),(30),(31)'),
        '3.7': ('identity_family', 'phi=a*t+F(s), a>0, F_prime>0; arbitrary smooth profile.', 'none'),
        '3.8': ('complete_quadratic_family_on_declared_graph',
                'phi=a*s+c0+c1*t+c2*t^2/2; a>0, c1+c2*t>0.', '(32)'),
        '3.9': ('regular_exact_parametric_quadrature',
                "B(F')F''=I0 with nonzero translation in phi. Retain I0, not only the printed special constant.", '(33),(34)'),
    }
    rows = []
    for case, (status, solution, equations) in details.items():
        r = derive_reduction(case)
        rows.append(dict(case=case, source_equations=equations, status=status,
                         solution=solution, coordinate=r['coordinate'], ansatz=r['ansatz'],
                         residual=r['residual'], leading=r['leading'], guards=r['guards'],
                         numerical_exponents=([3] if case=='3.5' else list(b.EXPONENTS))
                         if case in b.CASES else [], model='P'))
    return rows


def _plots(out, numerics, series):
    """Scientific exports: no interpolation outside the solved profile patch."""
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import BPoly

    b = backend()
    plots = out/'plots'
    plots.mkdir()
    figures = []
    fig = plt.figure(figsize=(14,9), layout='constrained')
    profile_fig, axes = plt.subplots(2,3,figsize=(13,8),layout='constrained')
    cubic = [r for r in numerics['runs'] if float(r['m'])==3 and r['status']=='passed']
    for index, row in enumerate(cubic):
        case = row['case']
        data = np.loadtxt(row['csv'],delimiter=',',skiprows=1)
        z_grid, jets = data[:,0], data[:,4:7]
        interp = BPoly.from_derivatives(z_grid,jets,extrapolate=False)
        low, high = row['interval']
        zz = np.linspace(low,high,60)
        if case=='3.8':
            ss,tt = np.meshgrid(np.linspace(0,1,45),zz)
            profile_coord = tt
        else:
            profile_coord,tt = np.meshgrid(zz,np.linspace(.8,1.2,45))
            ss = profile_coord*tt if case=='3.4' else (
                profile_coord/tt**2 if case=='3.5' else profile_coord-tt)
        ff,pp = interp(profile_coord),interp.derivative()(profile_coord)
        if case=='3.4':
            phi,vel,grad = tt*ff,ff-profile_coord*pp,pp
        elif case=='3.5':
            phi,vel,grad = ff,2*profile_coord*pp/tt,tt**2*pp
        elif case=='3.8':
            phi,vel,grad = ss+ff,pp,np.ones_like(pp)
        else:
            phi,vel,grad = ff+(tt if case=='3.9' else 0),pp+(1 if case=='3.9' else 0),pp
        valid = ((profile_coord>=low)&(profile_coord<=high)&(vel>0)&(grad>0)
                 &np.isfinite(phi)&np.isfinite(vel)&np.isfinite(grad))
        phi = np.where(valid,phi,np.nan)
        np.savez_compressed(plots/f"surface-{case}.npz",s=ss,t=tt,phi=phi,
                            velocity=vel,gradient=grad,valid=valid,
                            profile_coordinate=profile_coord)
        ax=fig.add_subplot(2,3,index+1,projection='3d')
        ax.plot_surface(ss,tt,phi,cmap='viridis',linewidth=0,antialiased=True)
        ax.set(xlabel=r'$s$',ylabel=r'$t$',zlabel=r'$\phi$',
               title=f'{case} | corrected pullback | m=3')
        ax.view_init(elev=25,azim=-60)
        a=axes.flat[index]
        a.plot(z_grid,jets[:,0],label='DOP853',color='#145c70',lw=2)
        a.plot(z_grid,data[:,1],ls='--',label='RKF45',color='#bf633e')
        germ=next(r for r in series if r['case']==case and float(r['m'])==3)
        coefs=np.array([float(c) for c in germ['coefficients']])
        taylor=np.polynomial.polynomial.polyval(z_grid-float(germ['z0']),coefs)
        a.plot(z_grid,taylor,ls=':',label='degree-6 Taylor',color='#8a5295')
        a.set(xlabel='z (t for 3.8)',ylabel='F',title=f'{case} | same initial jet')
        a.grid(alpha=.2)
        if index==0:a.legend(frameon=False,fontsize=8)
    # One exact surface is invariant under both cubic scaling generators.
    ss,tt=np.meshgrid(np.linspace(.2,1.5,60),np.linspace(.3,1.5,45))
    phi=45**(1/3)*ss**(1/3)*tt**(2/3)
    ax=fig.add_subplot(2,3,6,projection='3d')
    ax.plot_surface(ss,tt,phi,cmap='cividis',linewidth=0)
    ax.set(xlabel=r'$s$',ylabel=r'$t$',zlabel=r'$\phi$',
           title=r'Exact: $\phi=45^{1/3}s^{1/3}t^{2/3}$')
    ax.view_init(elev=25,azim=-60)
    np.savez_compressed(plots/'surface-power.npz',s=ss,t=tt,phi=phi,valid=np.ones_like(phi,dtype=bool))
    axes.flat[5].axis('off')
    axes.flat[5].text(.03,.85,'Printed scalar model P\ng=1, kappa=1/30\n\n'
                    'Curves: constructed local IVPs.\nTaylor: local truncation, not an exact solution.\n'
                    'Surfaces: solved profile interval only.\nNo Eulerian bed equivalence asserted.',
                    transform=axes.flat[5].transAxes,va='top',fontsize=11)
    fig.suptitle('One spatial dimension + time: reconstructed position maps',fontsize=16)
    for stem,current in [('s-t-phi-surfaces',fig),('profile-solutions',profile_fig)]:
        current.savefig(plots/f'{stem}.png',dpi=160,bbox_inches='tight',pad_inches=.2)
        current.savefig(plots/f'{stem}.pdf',bbox_inches='tight',pad_inches=.2)
        plt.close(current)
        figures.append(f'plots/{stem}.png')
    return figures


def run(out):
    out=Path(out).resolve()
    library=Path(__file__).resolve().parents[1]
    if out==library or out.is_relative_to(library):
        raise ValueError('Outputs must be outside the library and its frozen evidence')
    if out.exists():
        raise FileExistsError('Use a NEW output directory; evidence is never overwritten')
    out.mkdir(parents=True)
    start=time.perf_counter()
    b=backend()
    print('1. Original printed PDE, independent graph pullbacks and exact controls',flush=True)
    exact=exact_solution_checks()
    pullbacks=b.verify_reduction_pullbacks()
    quadratures={case:traveling_quadrature(alpha3=0 if case=='3.6' else 1)
                 for case in ('3.6','3.9')}
    symbolic=dict(exact=exact,pullbacks=pullbacks,quadratures=quadratures,
                  source_witnesses=source_audit(),power=b.cubic_power_law_audit())
    write_json(out/'symbolic.json',symbolic)
    rows=inventory()
    write_json(out/'inventory.json',rows)
    if not exact['passed'] or not pullbacks['passed'] or not all(q['passed'] for q in quadratures.values()):
        raise RuntimeError('Symbolic gate failed; no numerical campaign launched')
    print('2. All five valid ODE families: classic RKF45, DOP853, original-PDE finite differences',flush=True)
    numerics=b.run_campaign(out/'numerics')
    print('3. Exact local degree-six series for each regular IVP',flush=True)
    series=[]
    for numerical in numerics['runs']:
        case=numerical['case'];exponent=b.sp.Rational(str(numerical['m']))
        germ=compute_ode_series(case,exponent=exponent,order=6,
                               g_value=1,kappa_value=b.sp.Rational(1,30))
        series.append(germ)
    write_json(out/'series.json',series)
    print('4. Reconstruct (s,t,phi) surfaces on solved patches',flush=True)
    figures=_plots(out,numerics,series)
    source_verified=all(v.get('audit_verified',False) for k,v in symbolic['source_witnesses'].items() if k!='sample')
    passed=(numerics['all_passed'] and all(s['status']=='regular_analytic_germ' and
             s['verification']['passed'] for s in series) and source_verified)
    report=dict(model='P',all_checks_passed=passed,source_agreement=False,
                source_sha256=SOURCE_SHA256,source_doi='10.3390/math14030433',
                subsections=len(rows),regular_ivps=len(numerics['runs']),
                passed_ivps=sum(r['status']=='passed' for r in numerics['runs']),
                series=len(series),figures=figures,elapsed_seconds=time.perf_counter()-start,
                limitations=['Constructed IVPs; not source experimental data.',
                'Numerical residuals are sampled diagnostics, not continuous error bounds.',
                'General closed forms for 3.4/3.5 and singular continuation remain unresolved.',
                'No physical equivalence of E, P and M is inferred.',
                'Coverage is nine paper subsections; not every Lie reduction or every PDE solution.'])
    write_json(out/'report.json',report)
    _write_readme(out,rows,report,numerics,quadratures)
    manifest={str(p.relative_to(out)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in out.rglob('*') if p.is_file()}
    write_json(out/'MANIFEST.json',dict(outputs=manifest,source_sha256=SOURCE_SHA256,
              wrapper_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in Path(__file__).parent.glob('*.py')}))
    return report


def _write_readme(out,rows,report,numerics,quadratures):
    lines=['# 2026 printed scalar SVE: verified solution demo','',
           'The source is DOI 10.3390/math14030433, v3. P is the printed scalar model.',
           'Several printed formulas fail exact checks. This demo solves pullbacks derived from equation (7).',
           '',f"Checks passed: **{report['all_checks_passed']}**. {report['passed_ivps']}/{report['regular_ivps']} local IVPs passed.",
           '', '| Subsection | Source equations | Processing result | Solution scope |',
           '|---|---|---|---|']
    lines += [f"| {r['case']} | {r['source_equations']} | {r['status']} | {r['solution']} |" for r in rows]
    lines += ['', '## Exact traveling profiles', '',
              'Let r=F_prime, Y_prime=B and W_prime=r*B. For I0 != 0:',
              '```text','z=z0+(Y(r)-Y(p0))/I0','F=F0+(W(r)-W(p0))/I0','```',
              'Require B(r)!=0, r>0 and the declared positive velocity. The I0=0 affine branch is retained.', '']
    for case,q in quadratures.items():
        lines += [f"{case}, cubic demo: `B={q['B']}`, `Y={q['Y']}`, `W={q['W']}`.",'']
    lines += ['## Reading the pictures','',
              '`s` labels material particles, `t` is time, and `phi` is particle position.',
              'A profile F(z) generates a surface, e.g. z=s/t and phi=t F(z).',
              'It is one spatial dimension plus time. phi is not the water depth.',
              'Velocity phi_t and depth 1/phi_s are kinematic outputs; an Eulerian bed solution needs a separate proof.','']
    lines += [f'![{Path(p).stem}]({p})' for p in report['figures']]
    lines += ['', '## Numerical receipts','',
              '| Case | m | Result | original PDE residual at h=.003 |', '|---|---|---|---|']
    lines += [f"| {r['case']} | {r['m']} | {r['status']} | {r.get('pde',{}).get('acceptance_max_abs_residual','not evaluated')} |" for r in numerics['runs']]
    lines += ['', 'Numerical parameters: g=1, kappa=1/30, m in {1,1.5,2,3,4}; 3.5 only m=3.',
              'Initial jets and solved intervals are in numerics/numerics.json. All profiles use constructed data.',
              'Exact series recurrences and zero coefficient tests are in series.json. Truncations are not exact solutions.',
              'Source witnesses, exact graphs, first-integral identities and direct pullbacks are in symbolic.json.','']
    lines += [f'- {s}' for s in report['limitations']]
    (out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    table=''.join('<tr><td>'+html.escape(r['case'])+'</td><td>'+html.escape(r['source_equations'])+
                  '</td><td>'+html.escape(r['solution'])+'</td></tr>' for r in rows)
    images=''.join(f'<figure><img src="{p}"><figcaption>{html.escape(Path(p).stem)}</figcaption></figure>' for p in report['figures'])
    (out/'index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
        '<title>2026 SVE solutions in s, t, phi</title><style>body{font:17px/1.6 system-ui;max-width:1180px;'
        'margin:40px auto;padding:0 24px;color:#192f38;background:#fafbf9}h1{line-height:1.15}'
        'img{width:100%;height:auto}figure{margin:30px 0}td,th{padding:12px;text-align:left;border-bottom:1px solid #ccd5d1}'
        'table{border-collapse:collapse}a{color:#12657a}</style><h1>2026 SVE: profiles become surfaces</h1>'
        '<p>Printed scalar model P · material coordinate s · time t · particle position phi.</p>'
        '<p>Exact examples and corrected PDE pullbacks are verified. Printed formulas with counterexamples are retained separately. '
        'These surfaces do not certify the coupled Eulerian bed system.</p>'
        f'<p>{report["passed_ivps"]}/{report["regular_ivps"]} constructed local IVPs passed sampled checks. '
        '<a href="README.md">Detailed scope</a> · <a href="report.json">Receipt</a> · <a href="symbolic.json">Exact certificates</a></p>'
        +images+'<h2>All nine source subsections</h2><table><tr><th>Case</th><th>Equations</th><th>Solution status</th></tr>'
        +table+'</table><p>General closed forms for 3.4/3.5 and continuation through singular charts remain open.</p></html>',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    report=run(args.out)
    print(json.dumps(report,indent=2))
    return 0 if report['all_checks_passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
