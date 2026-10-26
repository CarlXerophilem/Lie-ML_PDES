"""Serial, resource-bounded strict campaign; never converts a timeout to a theorem."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import os
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sympy as sp
from symm.LieSymm.core import JetSpace, json_ready
from symm.LieSymm.models import BRANCHES, branch_model
from symm.LieSymm.models_2d import BRANCHES_2D, branch_model_2d
from symm.LieSymm.strict import (analyze_strict, run_reduce, reduce_from_analysis,
                                StrictMixedShell)
from symm.LieSymm.core import point_action, prolongation_coefficients


def cases():
    return ([f'E1:{n}' for n in BRANCHES] + [f'E2:{n}' for n in BRANCHES_2D]
            + ['P:general', 'P:1', 'P:3', 'custom:f0', 'custom:f_nonzero'])


def model(key):
    family, name = key.split(':')
    if family == 'E1':
        definition=branch_model(name);cell=BRANCHES[name]
        definition['branch_conditions']['fixed_parameters']={k:sp.sympify(cell[k]) for k in ('m','n') if cell[k] is not None}
        return definition
    if family == 'E2':
        definition=branch_model_2d(name);cell=BRANCHES_2D[name]
        fixed={k:sp.sympify(cell[k]) for k in ('m','n') if cell[k] is not None}
        if cell['coriolis']=='f0': fixed['f']=sp.S.Zero
        definition['branch_conditions']['fixed_parameters']=fixed
        return definition
    if family == 'P':
        t, s, phi = sp.symbols('t s phi', real=True)
        g, kappa = sp.symbols('g kappa', positive=True)
        m = sp.Symbol('m', real=True) if name == 'general' else sp.Integer(name)
        j = JetSpace((t, s), (phi,))
        velocity, gradient = j.jet(0, (1, 0)), j.jet(0, (0, 1))
        equation = j.D(gradient*j.jet(0, (2, 0))-g*j.jet(0, (0, 2))/gradient**2, 0)-g*j.D(m*kappa*velocity**(m-1)*j.jet(0, (1, 1))/gradient, 1)
        return dict(independent_variables=j.x, dependent_fields=j.u, equations=(equation,),
                    parameters=(g,kappa)+((m,) if isinstance(m,sp.Symbol) else ()),
                    branch_conditions=dict(model_id=key, guards=['phi_t>0', 'phi_s>0', 'g>0', 'kappa>0']))
    if family != 'custom':
        raise ValueError(key)
    t, x, y, u, v, B = sp.symbols('t x y u v B', real=True)
    h, g, K1, K3, G = sp.symbols('h g K1 K3 G', positive=True)
    f = sp.S.Zero if name == 'f0' else sp.Symbol('f', nonzero=True, real=True)
    j = JetSpace((t,x,y),(h,u,v,B))
    speed = u*u+v*v
    flux = [(K1+K3*speed)*w-G*speed*j.jet(B,j.unit(i)) for i,w in enumerate((u,v),1)]
    equations = (j.jet(h,(1,0,0))+j.D(h*u,1)+j.D(h*v,2),
                 j.jet(u,(1,0,0))+u*j.D(u,1)+v*j.D(u,2)+g*j.D(h+B,1)-f*v,
                 j.jet(v,(1,0,0))+u*j.D(v,1)+v*j.D(v,2)+g*j.D(h+B,2)+f*u,
                 j.jet(B,(1,0,0))+j.D(flux[0],1)+j.D(flux[1],2))
    return dict(independent_variables=j.x, dependent_fields=j.u, equations=equations,
                parameters=(g,K1,K3,G)+((f,) if f != 0 else ()),
                branch_conditions=dict(model_id=key,fixed_coriolis=f,
                                       guards=['h>0','g>0','K1>0','K3>0','G>0']+(['f!=0'] if f != 0 else [])))


def linux_path(path):
    path=Path(path).resolve()
    if not path.drive:
        return path.as_posix()
    return '/mnt/'+path.drive[0].lower()+path.as_posix()[2:]


def atomic_json(path,value):
    temporary=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temporary.write_text(json.dumps(value,indent=2),encoding='utf-8')
    os.replace(temporary,path)


def source_hashes():
    paths=[Path(__file__).resolve(),*sorted((ROOT/'symm/LieSymm').rglob('*.py'))]
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def cleanup_linux(pidfile):
    if not pidfile.exists():
        return dict(status='no-linux-process-started')
    value=pidfile.read_text().strip()
    if not value.isdigit() or int(value) <= 1:
        raise ValueError('Invalid Linux process group receipt')
    prefix=['wsl','--exec'] if sys.platform=='win32' else []
    result=subprocess.run([*prefix,'kill','-KILL','--','-'+value],capture_output=True,text=True,timeout=15)
    check=subprocess.run([*prefix,'kill','-0','--','-'+value],capture_output=True,text=True,timeout=15)
    return dict(status='terminated' if check.returncode != 0 else 'cleanup-failed',
                process_group=int(value),kill_returncode=result.returncode,check_returncode=check.returncode)


def require_cleanup(cleanup):
    if cleanup.get('status') not in ('terminated','no-linux-process-started'):
        raise RuntimeError('CAS process cleanup unconfirmed; refusing further execution')


def cas_command(out, timeout, pidfile=None, *, platform=None, memory_bytes=1_800_000_000):
    platform=platform or sys.platform
    binary = out.resolve()/'cas/runtime/usr/lib/reduce/cslbuild/csl/reduce'
    linux = linux_path(binary) if platform=='win32' else str(binary)
    # Linux prlimit covers the actual WSL process; Windows RSS cannot do so.
    heap=1024 if memory_bytes<=1_800_000_000 else min(4096,int(memory_bytes/2**20*.6))
    command=['timeout','--signal=TERM','--kill-after=5',str(timeout),'prlimit',f'--as={memory_bytes}','--',linux,
            '-w','-k128M','--maxmem',f'{heap}M','--no-rcfile','--stop-on-error']
    if pidfile is not None:
        command=['setsid','--wait','sh','-c','printf "%s" "$$" > "$1"; shift; exec "$@"',
                 'strict-cas',linux_path(pidfile) if platform=='win32' else str(pidfile),*command]
    return ['wsl','--exec',*command] if platform=='win32' else command


def custom_diagnostics(definition):
    j=JetSpace(definition['independent_variables'],definition['dependent_fields'])
    t,x,y=j.x;h,u,v,B=j.u
    equations=definition['equations'];shell=StrictMixedShell(j,equations)
    candidates={'joint_rotation':((0,-y,x),(0,-v,u,0)),
                'old_cubic_scaling':((0,x,y),(2*h,u,v,2*B)),
                'wrong_spatial_only_rotation':((0,-y,x),(0,0,0,0))}
    results={}
    for label,(xi,eta) in candidates.items():
        coefficients=prolongation_coefficients(j,xi,eta,2,'recursive')
        residuals=[sp.simplify(shell.reduce(point_action(j,e,xi,eta,coefficients=coefficients))) for e in equations]
        results[label]=dict(residuals=residuals,admitted=all(v==0 for v in residuals),
                           scope='candidate diagnostic only, not basis discovery')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'build/sve-strict-lie-20261026')
    parser.add_argument('--case')
    parser.add_argument('--tier',type=int,choices=(60,300,1800),default=60)
    parser.add_argument('--samples',action='store_true')
    parser.add_argument('--pid-file',type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    if args.samples:
        for package in ('liepde','applysym'):
            source=args.out/'cas/runtime/usr/share/reduce/packages/crack'/f'{package}.tst'
            script='load_package crack,liepde,applysym$\n'+source.read_text()+'\nquit$\n'
            pidfile=args.out/(uuid.uuid4().hex+'.pid')
            try:
                result=run_reduce(cas_command(args.out,args.tier,pidfile),script,timeout=args.tier)
            finally:
                cleanup=cleanup_linux(pidfile)
            result['linux_cleanup']=cleanup
            result['source_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
            (args.out/f'official-{package}-{args.tier}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
            require_cleanup(cleanup)
            print(package,result['status'],flush=True)
        return
    if args.case:
        hashes=source_hashes()
        token=uuid.uuid4().hex
        pidfile=args.pid_file or args.out/(token+'.pid')
        try:
            definition=model(args.case)
            report=analyze_strict(**definition,cas_command=cas_command(args.out,args.tier,pidfile),timeout=args.tier,
                                  cas_log_prefix=args.out/(args.case.replace(':','--')+'-'+token+'.cas'))
        finally:
            cleanup=cleanup_linux(pidfile)
        report['source_sha256'] = hashes
        report['source_changed_during_run'] = hashes != source_hashes()
        report['linux_cleanup'] = cleanup
        report['translation_reduction']=reduce_from_analysis(report)
        if args.case.startswith('custom:'):
            report['transfer_diagnostics']=custom_diagnostics(definition)
        destination=args.out/(args.case.replace(':','--')+f'-{args.tier}.json')
        if destination.exists():
            destination.rename(destination.with_name(destination.stem+'.superseded-'+uuid.uuid4().hex+'.json'))
        atomic_json(destination,json_ready(report))
        require_cleanup(cleanup)
        print(args.case,report['cas']['status'],report.get('returned_family_verified',False),flush=True)
        return
    rows=[]
    for key in cases():
        destination=args.out/(key.replace(':','--')+f'-{args.tier}.json')
        if destination.exists():
            try:
                report=json.loads(destination.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                report={}
            if report.get('source_sha256') == source_hashes() and not report.get('source_changed_during_run'):
                require_cleanup(report.get('linux_cleanup',{}))
                rows.append(dict(case=key,status=report['classification_status'],cas_status=report['cas']['status']))
                continue
            destination.rename(destination.with_name(destination.stem+'.superseded-'+uuid.uuid4().hex+'.json'))
        token=uuid.uuid4().hex
        pidfile=args.out/(token+'.pid')
        command=[sys.executable,'-B',str(Path(__file__).resolve()),'--out',str(args.out),'--case',key,'--tier',str(args.tier),
                 '--pid-file',str(pidfile)]
        try:
            receipt=run_reduce(command,'',timeout=args.tier,artifact_prefix=args.out/(token+'.worker'))
        finally:
            cleanup=cleanup_linux(pidfile)
        receipt['linux_cleanup']=cleanup
        atomic_json(args.out/(key.replace(':','--')+f'-worker-{args.tier}.json'),receipt)
        require_cleanup(cleanup)
        if destination.exists():
            report=json.loads(destination.read_text(encoding='utf-8'))
            row=dict(case=key,status=report['classification_status'],cas_status=report['cas']['status'],family_verified=report.get('returned_family_verified',False))
        else:
            row=dict(case=key,status=receipt['status'],cas_status='no-complete-receipt')
        rows.append(row)
        atomic_json(args.out/f'coverage-{args.tier}.json',rows)
        print(row,flush=True)


if __name__ == '__main__':
    main()
