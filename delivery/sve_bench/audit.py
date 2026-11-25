"""Derive profile equations from PDE operators, without exact profiles or data."""
import json
import resource
import subprocess
import sys
import time
from pathlib import Path
import sympy as sp
from .record import ROOT, save, run_record, Timer, digest


def command(args, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    with out.open("w") as stdout, out.with_suffix(".stderr").open("w") as stderr:
        result = subprocess.run(args, cwd=ROOT, stdout=stdout, stderr=stderr)
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    record = {"command": list(map(str,args)), "exit_code": result.returncode,
              "wall_seconds":time.perf_counter()-start,
              "user_cpu_seconds":after.ru_utime-before.ru_utime,
              "system_cpu_seconds":after.ru_stime-before.ru_stime,
              "children_peak_rss_bytes":after.ru_maxrss*1024}
    save(out.with_suffix(".resources.json"),record)
    if result.returncode:
        raise RuntimeError(f"Failed command; inspect {out.with_suffix('.stderr')}")
    return record


def derive_additional():
    import reproduce_sve2026 as scalar
    from symbolic_sve2026 import compatible
    t,x = sp.symbols('t x',positive=True)
    g,k = sp.symbols('g kappa',positive=True)
    m,alpha = sp.symbols('m alpha',real=True)
    H,U,Z = [sp.Function(n)(x) for n in ('H','U','Z')]
    def euler(h,u,b,exponent):
        return [h.diff(t)+(h*u).diff(x),u.diff(t)+u*u.diff(x)+g*(h+b).diff(x),
                b.diff(t)+k*(u**exponent).diff(x)]
    rows=[{"id":"E1_bed_drift","model":"E1","graph":[str(H),str(U),str(alpha*t+Z)],
           "residuals":list(map(str,euler(H,U,alpha*t+Z,m))),
           "conditions":["H>0","U>0","g,kappa>0","m>=1"],"orbit_rank":1}]
    cubic=euler(H/t**2,U/t,Z/t**2,3)
    rows.append({"id":"E1_cubic","model":"E1","graph":[str(H/t**2),str(U/t),str(Z/t**2)],
                 "residuals":[str(sp.simplify(v*t**power)) for v,power in zip(cubic,(3,2,3))],
                 "conditions":["t>0","H,U>0","m=3"],"orbit_rank":1})
    t,s,z=scalar.t,scalar.s,scalar.z
    fun=sp.Function('F')
    gamma,c=sp.symbols('gamma c',real=True)
    jets={sp.diff(fun(z),z,n):v for n,v in enumerate((scalar.F,scalar.P,scalar.C,scalar.H))}
    for model in ('M','P'):
        for kind,exponent,graph,section,factor in (
            ('tilted',2,gamma*t+fun(s-c*t),{s:z+c*t},1),
            ('tilted',3,gamma*t+fun(s-c*t),{s:z+c*t},1),
            ('cubic',3,fun(s*t**2),{s:z/t**2},t),
            ('common',2,t*fun(s/t),{s:z*t},t**2),
            ('affine',2,gamma*s+fun(t),{t:z},1)):
            operator=compatible(exponent) if model=='M' else scalar.master(exponent)
            mapping={v:sp.diff(graph,t,i,s,j).subs(section).doit().xreplace(jets)
                     for (i,j),v in scalar.JETS.items()}
            pulled=sp.factor(factor*operator.xreplace(mapping))
            assert not pulled.has(t,s), (model,kind)
            row={"id":f'{model}_{kind}_m{exponent}',"model":model,"m":exponent,
                 "graph":str(graph),"residual":str(pulled),"orbit_rank":1,
                 "conditions":["phi_s>0","phi_t>0","g,kappa>0"],
                 "derivation":"original PDE differentiated on unknown profile; no initial values"}
            if kind in ('common','tilted'):
                leading=sp.factor(sp.diff(pulled,scalar.H))
                first=leading*scalar.C
                check=sp.factor(pulled-scalar.profile_total(first))
                assert check==0
                row.update(first_integral=str(first),leading=str(leading),identity_remainder=str(check))
            rows.append(row)
    shear=t*s+fun(t)
    mapping={v:sp.diff(shear,t,i,s,j).subs(t,z).doit().xreplace(jets)
             for (i,j),v in scalar.JETS.items()}
    rows.append({"id":"P_m1_shear","model":"P","residual":str(sp.factor(scalar.master(1).xreplace(mapping))),
                 "conditions":["t>0","s+F_prime>0"],"orbit_rank":1})
    return rows


def run(out):
    out=Path(out); timer=Timer()
    report=run_record('symbolic_audit',{'ML':False,'initial_data_supplied':False})
    report['scope']='Executed ODE families, not exhaustive enumeration of all subalgebras; E2 affine search only.'
    runs=[]; maintained={}
    for name in ('symbolic_sv2022','symbolic_sve2026','symbolic_new_model2026','test_sve2026_ansatz_layers'):
        path=ROOT/'delivery'/f'{name}.py'
        runs.append(command([sys.executable,'-B',str(path)],out/f'{name}.json'))
        if not name.startswith('test_'):
            maintained[name]=json.loads((out/f'{name}.json').read_text())
    runs.append(command([sys.executable,'-B','delivery/reproduce_sve2026.py','--output',str(out/'scalar.json')],out/'scalar.stdout'))
    runs.append(command([sys.executable,'-B','delivery/annular-transcritical-theorem-20261101/replay.py',
                         '--out',str(out/'annular'),'--campaign',str(out/'campaign'),'--prefix','nonlinear'],out/'annular.stdout'))
    scalar=json.loads((out/'scalar.json').read_text())
    import reproduce_sve2026 as source
    reductions=[]
    for case in [f'3.{i}' for i in range(1,10)]+['table3-mixed']:
        for mix in ([sp.Rational(1,4),-1] if case=='table3-mixed' else [sp.Rational(1,4)]):
            reductions.append(source.jsonable({'case':case,'mix_alpha':mix,**source.derive_reduction(case,mix_alpha=mix)}))
    report.update(status='passed',maintained=maintained,additional=derive_additional(),
                  printed_reductions=reductions,source_formula_audit=scalar['reductions']['source_witnesses'],
                  source_hashes={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'delivery').glob('symbolic_*.py')},
                  commands=runs,resources=timer.result())
    save(out/'ODE_INVENTORY.json',report)
    return report
