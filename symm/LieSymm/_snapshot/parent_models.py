"""Separate scalar and material controls, never inputs to full-system classification.

Printed P: Paliathanasis, Leon and Leach (2026), DOI 10.3390/math14030433,
page 2, equations (5)--(7). M is the independently derived compatibility
equation retaining material bed transport. Neither name implies a point
equivalence with the three-field Eulerian system.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def scalar_models():
    t,s = sp.symbols('t s', real=True)
    g,K = sp.symbols('g K', positive=True)
    m = sp.Symbol('m', real=True)
    phi = sp.Function('phi')(t,s)
    bed = sp.Function('bed')(t,s)
    q,v = sp.diff(phi,s),sp.diff(phi,t)
    A = q*sp.diff(phi,t,2)-g*sp.diff(phi,s,2)/q**2
    C = m*K*v**(m-1)*sp.diff(v,s)/q
    P = sp.diff(A,t)-g*sp.diff(C,s)
    M = P-sp.diff(v*A/q,s)
    bed_s = -A/g
    bed_t_P,bed_t_M = -C,-v*A/(g*q)-C
    return dict(t=t,s=s,g=g,K=K,m=m,phi=phi,bed=bed,q=q,v=v,A=A,C=C,P=P,M=M,
                bed_s=bed_s,bed_t_P=bed_t_P,bed_t_M=bed_t_M,
                guards=('phi_s>0','phi_t>0','g>0','K>0','simply connected local reconstruction chart'),
                integration_constant='one additive bed datum after closedness, fixed by matching bed data')


def verify_scalar_and_material():
    z=scalar_models()
    t,s,g,K,m,phi,bed,q,v=(z[k] for k in ('t','s','g','K','m','phi','bed','q','v'))
    exner=sp.diff(bed,t)-v*sp.diff(bed,s)/q+z['C']
    relative=sp.diff(q*bed,t)+sp.diff(K*v**m-bed*v,s)
    checks={
        'relative_material_flux':sp.simplify(relative-q*exner),
        'printed_closedness':sp.simplify(g*(sp.diff(z['bed_s'],t)-sp.diff(z['bed_t_P'],s))+z['P']),
        'corrected_closedness':sp.simplify(g*(sp.diff(z['bed_s'],t)-sp.diff(z['bed_t_M'],s))+z['M']),
    }
    c=sp.Symbol('c',positive=True)
    witness= s**2/2+c*t
    def on_phi(expr,value):
        return sp.simplify(expr.subs(phi,value).doit())
    printed_witness=on_phi(z['P'],witness)
    corrected_witness=on_phi(z['M'],witness)
    checks['printed_only_witness']=printed_witness
    checks['corrected_nonzero_witness_formula']=sp.simplify(corrected_witness+3*g*c/s**4)

    # Derive the mass-coordinate chart from an actual full-system solution.
    H,U=sp.symbols('H U',positive=True)
    k,B0,x=sp.symbols('k B0 x',real=True)
    mass_label=H*(x-U*t+g*k*t**2/2)
    chi=s/H+U*t-g*k*t**2/2
    velocity=U-g*k*t
    checks['mass_label_x']=sp.diff(mass_label,x)-H
    checks['mass_label_t']=sp.diff(mass_label,t)+H*velocity
    checks['material_inverse']=sp.simplify(chi.subs(s,mass_label)-x)
    material_bed=k*chi+B0
    checks['material_momentum_bed_s']=sp.simplify(sp.diff(material_bed,s)-on_phi(z['bed_s'],chi))
    checks['correct_material_bed_t']=sp.simplify(sp.diff(material_bed,t)-on_phi(z['bed_t_M'],chi))
    omitted=sp.simplify(sp.diff(material_bed,t)-on_phi(z['bed_t_P'],chi))
    checks['omitted_transport_defect_formula']=sp.simplify(omitted-k*velocity)
    checks['mass_coordinate_jacobian']=sp.Matrix((t,mass_label)).jacobian((t,x)).det()-H
    checks={key:sp.simplify(value) for key,value in checks.items()}
    return {'all_passed':all(value==0 for value in checks.values()),'checks':checks,
            'P_only_counterexample':{'phi':witness,'P':printed_witness,'M':corrected_witness,
                                      'guards':('s>0','c>0','g>0')},
            'material_constant_slope':{'chi':chi,'mass_label':mass_label,'bed':material_bed,
                'jacobian':H,'guards':('H>0','U-g*k*t>0'),
                'wrong_printed_bed_t_defect':omitted},
            'point_algebra_equivalence_claim':False,
            'scope':'separate P/M and G=0 material controls; no full-system inference from scalar tests'}


def source_receipt():
    ledger=ROOT/'build/sve-systematic-20261020/sources/ledger.json'
    source=json.loads(ledger.read_text(encoding='utf-8'))
    required={'R01','R02','R03','R04','R07','R08'}
    selected=[]
    for item in source['sources']:
        if item['id'] not in required:
            continue
        path=Path(item['read_path'])
        actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        selected.append({'id':item['id'],'doi':item.get('doi'),'path':str(path),
            'sha256':actual,'matches_source_ledger':actual==item['sha256'],
            'anchors':item['anchors'],'primary_url':item['primary_url']})
    return {'source_ledger':str(ledger),'source_ledger_sha256':hashlib.sha256(ledger.read_bytes()).hexdigest(),
            'sources':selected,'required_ids':sorted(required),
            'all_matched':({item['id'] for item in selected}==required
                           and all(item['matches_source_ledger'] for item in selected)),
            'new_web_retrieval':False,'status':'live local byte verification of previously retrieved primary sources'}


if __name__=='__main__':
    from main import json_ready
    report={'checks':verify_scalar_and_material(),'sources':source_receipt()}
    (HERE/'parent_models_receipt.json').write_text(json.dumps(json_ready(report),indent=2),encoding='utf-8')
    print(json.dumps(json_ready(report),indent=2))
    raise SystemExit(0 if report['checks']['all_passed'] and report['sources']['all_matched'] else 1)
