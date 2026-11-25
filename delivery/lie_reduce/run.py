"""Bounded-time, no-ML symbolic pipeline: python -m lie_reduce.run."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import argparse
import dataclasses
import hashlib
import json
import resource
import platform
import sys
import signal
import time
from pathlib import Path
import sympy as sp
from .models import scalar,euler
from .determining import symmetries
from .reduce import reduce
from .algebra import catalogue,weights,add,coordinates_in_basis,verify_lie_algebra


class StageTimeout(Exception): pass


def timed(fn,seconds):
    def interrupt(*_):raise StageTimeout('symbolic stage exceeded '+str(seconds)+' seconds')
    old=signal.signal(signal.SIGALRM,interrupt);signal.setitimer(signal.ITIMER_REAL,seconds)
    start=time.perf_counter(); cpu=time.process_time(); usage=resource.getrusage(resource.RUSAGE_SELF)
    try:
        value=fn();status='completed';reason=None
    except Exception as exc:
        value=None;status='time_limit' if isinstance(exc,StageTimeout) else 'failed';reason=f'{type(exc).__name__}: {exc}'
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old)
    return {'status':status,'reason':reason,'wall_seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,
            'user_cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime-usage.ru_utime,
            'system_cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_stime-usage.ru_stime,
            'process_peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'value':value}


def serial(value):
    from .jets import JetSpace
    if isinstance(value,JetSpace):
        return {'independent':serial(value.independent),'dependent':serial(value.dependent),'order':value.order,'jet_symbols':serial(value.jets)}
    if dataclasses.is_dataclass(value): return serial(dataclasses.asdict(value))
    if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [serial(v) for v in value]
    if isinstance(value,sp.MatrixBase):return serial(value.tolist())
    if isinstance(value,sp.Basic):return str(value)
    return value


def span_equal(left,right,coords):
    terms=sorted(set(mon for X in left+right for e in X for mon,_ in sp.Poly(e,*coords).terms()))
    def column(X):return sp.Matrix([sp.Poly(e,*coords).coeff_monomial(mon) for e in X for mon in terms])
    A=sp.Matrix.hstack(*map(column,left));B=sp.Matrix.hstack(*map(column,right))
    return A.rank()==B.rank()==A.row_join(B).rank()


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='delivery/lie_reduce/results')
    parser.add_argument('--stage-seconds',type=int,default=15);parser.add_argument('--catalogue',action='store_true');parser.add_argument('--reference-experiment',action='store_true')
    args=parser.parse_args();out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    whole_start=time.perf_counter();whole_cpu=time.process_time()
    from .frozen_PM import verify
    frozen=verify()
    report={'frozen_PM':frozen,'schema':'Definition 6.1 symbolic provenance extension','ML':False,'degree':2,
            'scope':'finite polynomial discovery; Appendix B catalogue supplied, not automatically proved optimal',
            'runs':[],'unrestricted_claim':'only frozen positive-chart proofs, not inferred from finite search'}
    for name,factory in [('P',scalar),('M',scalar),('E1',euler)]:
        for m in (1,2,3,4):
            spec,basis=factory(name,m) if name!='E1' else factory(m)
            def discovery():
                result=symmetries(spec,2)
                equal=span_equal(result['basis'],list(basis.values()),spec.jets.independent+spec.jets.dependent)
                if not equal: raise ArithmeticError('degree-2 kernel differs from degree-1 canonical labels')
                if name in ('P','M'):
                    frozen_data=json.loads((Path(__file__).with_name('frozen')/'PM.json').read_text())['models'][name]['bases']
                    frozen_basis=frozen_data.get(str(m),frozen_data['m'])
                    env=dict(zip(('t','s','u'),spec.jets.independent+spec.jets.dependent))
                    reference=[tuple(sp.sympify(v,locals=env) for v in X) for X in frozen_basis]
                    if not span_equal(result['basis'],reference,spec.jets.independent+spec.jets.dependent):
                        raise ArithmeticError('discovery differs from immutable frozen basis')
                    result['frozen_basis_span_equal']=True
                result.pop('matrix')
                result['basis_source']='degree-1 determining nullspace, canonically labeled'
                result['reference_span_equal']=equal
                return result
            entry={'model':name,'m':m,'discovery':timed(discovery,args.stage_seconds),'brackets':weights(spec,basis),
                   'principal_chart':timed(spec.shell_certificate,args.stage_seconds),
                   'algebra':timed(lambda:verify_lie_algebra(spec,basis),args.stage_seconds),'reductions':[]}
            choices=catalogue(spec,basis,m) if args.catalogue else []
            if m==3:choices += [{'id':'table3.2.cubic','generator':basis['Y5' if name!='E1' else 'X5']}]
            if name!='E1':
                c,gamma=sp.symbols('c gamma',real=True)
                choices += [{'id':'table3.2.'+label,'generator':X} for label,X in (
                    ('Y4',basis['Y4']),('tilted',add((1,basis['Y1']),(c,basis['Y3']),(gamma,basis['Y2']))),
                    ('spatial',add((1,basis['Y3']),(gamma,basis['Y2']))),('vertical',basis['Y2']))]
            else:
                alpha=sp.Symbol('alpha',real=True)
                choices += [{'id':'table3.2.bed_drift','generator':add((1,basis['X1']),(alpha,basis['X3']))}]
            for row in choices:
                row['basis_coordinates']=coordinates_in_basis(row['generator'],list(basis.values()),spec.jets.independent+spec.jets.dependent)
                result=timed(lambda:reduce(spec,row['generator']),args.stage_seconds)
                entry['reductions'].append({**row,**result})
            report['runs'].append(entry)
            (out/'pipeline.json').write_text(json.dumps(serial(report),indent=2)+'\n')
            print(name,m,entry['discovery']['status'],len(choices),'reductions',flush=True)
    from .annular import derive
    report['E2']=timed(derive,args.stage_seconds)
    from .frozen.reproduce_sve2026 import printed_equation_witnesses
    report['source_formula_audit']=printed_equation_witnesses()
    report['source_X5_note']='Source X5 is manuscript Y5; corrected PDE pullback is computed. Printed equation (25) is refuted by its exact witness, not an acceptance target.'
    report['coverage']={'symbolic_real_m':'frozen proof only; generic polynomial splitter does not accept symbolic noninteger powers',
                        'finite_search_exponents':[1,2,3,4],
                        'completeness':'no automatic optimal-system or unrestricted smooth classification claim'}
    from .benchmarks import export
    report['task_exports']=timed(export,args.stage_seconds)
    from .critical import certify
    report['critical_certificate']=timed(certify,max(args.stage_seconds,30))
    if args.reference_experiment:
        from .experiment import run as reference_experiment
        if report['critical_certificate']['status']=='completed':
            report['reference_experiment']=timed(lambda:reference_experiment(report['critical_certificate']['value'],out),60)
        else:
            report['reference_experiment']={'status':'blocked','reason':'BB certificate failed'}
    from .edge_cases import run as edge_cases
    report['presentation_and_fixed_graph_checks']=timed(edge_cases,args.stage_seconds)
    from .obligations import ledger,write_ledger
    report['proof_obligations']=ledger(report)
    write_ledger(report['proof_obligations'],out)
    report['environment']={'python':sys.version,'sympy':sp.__version__,'platform':platform.platform(),
                           'cpu':Path('/proc/cpuinfo').read_text().split('model name')[1].split('\n')[0].strip(': \t')}
    report['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py')}
    report['total_wall_seconds']=time.perf_counter()-whole_start
    report['parent_cpu_seconds']=time.process_time()-whole_cpu
    report['child_cpu_seconds']=resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime+resource.getrusage(resource.RUSAGE_CHILDREN).ru_stime
    from .report import write_inventory
    write_inventory(serial(report),out)
    report['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024
    report['status']='completed_with_explicit_scope_limits'
    (out/'pipeline.json').write_text(json.dumps(serial(report),indent=2)+'\n')


if __name__=='__main__':main()
