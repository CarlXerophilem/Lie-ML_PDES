"""Post-solve diagnostics. Reference data never enter training or its callbacks."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse
import json
from pathlib import Path
import time
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from ode_methods.task import Task
from symbolic_input import Expressions

ROOT=Path(__file__).resolve().parent


def evaluate(candidate,s):
    reader=Expressions()
    if candidate['representation']=='polynomial':
        c=np.array([float(reader.read(v)) for v in candidate['coefficients']])
        return np.polynomial.polynomial.polyval(s,c),np.polynomial.polynomial.polyval(s,np.arange(1,len(c))*c[1:])
    if candidate['representation']!='network':raise ValueError('sampling this representation is not implemented')
    y=s[:,None];dy=np.ones_like(y)
    for layer in candidate['layers']:
        W=np.array(layer['weight']);b=np.array(layer['bias']);v=y@W.T+b;d=dy@W.T
        if layer['kind']=='linear':y,dy=v,d
        elif layer['kind']=='tanh':y=np.tanh(v);dy=(1-y*y)*d
        else:
            alpha=np.array(layer['alpha']);act=np.tanh(v);y=y+alpha*act;dy=dy+alpha*(1-act*act)*d
    y,dy=y[:,0],dy[:,0]
    if candidate.get('prefix') is not None:
        c=np.array([float(reader.read(v)) for v in candidate['prefix']]);p=len(c)
        yy=np.polynomial.polynomial.polyval(s,c);dd=np.polynomial.polynomial.polyval(s,np.arange(1,len(c))*c[1:])
        dy=dd+p*s**(p-1)*y+s**p*dy;y=yy+s**p*y
    return y,dy


def reference(task,s,annular_record):
    X=float(sp.Rational(task['physical_scale']))
    if task['id']=='N1':return np.sqrt(1-X*s),'closed positive square-root branch, float64 evaluation'
    if task['id']=='N2':
        def G(p):return -1/(4*p*p)-3*p/5-np.log(p)/20
        return np.array([.5 if v==0 else brentq(lambda p:G(p)-G(.5)-X*v,.5,.9,xtol=5e-15) for v in s]),'independent implicit quadrature roots, float64'
    sign=1 if task['id']=='N3plus' else -1
    branch=next(v for v in annular_record['branches'] if ('+ sqrt' in v['slope'])==(sign==1))
    coefficients=[float(sp.N(sp.Rational(a)+sp.Rational(b)*sp.sqrt(141),30)) for a,b in branch['coefficients_Qsqrt141']]
    c=[0.]+[coefficients[n]*X**(n-2) for n in range(2,len(coefficients))]
    return np.polynomial.polynomial.polyval(s,c),'separately certified degree40 annular series, float64 evaluation; bounds in REFERENCE_EXPERIMENT.json'


def run(run_dir,tasks_path,annular_path):
    start=time.perf_counter();run_dir=Path(run_dir)
    if tasks_path is None:tasks_path=run_dir/'TASKS.json' if (run_dir/'TASKS.json').exists() else ROOT/'managed_results/tasks.json'
    tasks={v['id']:v for v in json.loads(Path(tasks_path).read_text())['tasks']}
    ann=json.loads(Path(annular_path).read_text());rows=[]
    for path in sorted(run_dir.glob('*.json')):
        data=json.loads(path.read_text())
        if not isinstance(data,dict) or 'candidate' not in data:continue
        task=tasks[data['task']];lo,hi=map(float,task['interval']);s=np.linspace(lo,hi,1025)
        try:
            y,dy=evaluate(data['candidate'],s);truth,kind=reference(task,s,ann)
            R=Task(task).numpy_functions()[0];residual=np.asarray(R(s,y,dy))
            if not all(np.all(np.isfinite(v)) for v in (y,dy,truth,residual)):raise ValueError('nonfinite candidate or residual on evaluation grid')
            if task['id']=='N2' and np.any(y==0):raise ValueError('p=0 leaves the material chart')
            profile_error=float(np.max(abs(y-truth)));X=float(sp.Rational(task['physical_scale']))
            if task['operator']=='BB':
                ell=float(Expressions().read(task['slope']));H=1+ell*X*s+X*X*s*y
                physical=float(np.max(abs(X*X*s*(y-truth))))
                guards={'sampled_H_min':float(np.min(H)),'sampled_w_max':float(np.max(abs(X*y))),
                        'sampled_BB_ball_membership':bool(np.max(abs(X*y))<=float(sp.Rational(task['remainder_radius'])))}
                admissible=guards['sampled_H_min']>0 and guards['sampled_BB_ball_membership']
            else:
                physical=profile_error;guards={'sampled_positive_profile_min':float(np.min(y))};admissible=np.min(y)>0
                if task['id']=='N2':
                    L=(10-y*y-12*y**3)/(20*y**3);guards['sampled_abs_L_min']=float(np.min(abs(L)));admissible=bool(admissible and np.all(L>0))
            value,_=evaluate(data['candidate'],np.array([0.]));trace=float(abs(value[0]-float(sp.Rational(task['initial']))))
            quadrature={}
            if data['method']=='prefix':
                check_nodes=np.linspace(lo,hi,65);at_nodes=evaluate(data['candidate'],check_nodes)[0]
                defects={}
                for order in (16,32,64):
                    nodes,weights=np.polynomial.legendre.leggauss(order);u=(nodes+1)/2;weights=weights/2
                    at=check_nodes[:,None]*u;yy=evaluate(data['candidate'],at.ravel())[0].reshape(at.shape)
                    r0=R(at,yy,np.zeros_like(yy))
                    if task['operator']=='BB':
                        b=float(task['b']);defects[order]=at_nodes-np.sum(weights*u**(b-1)*(b*yy-r0),axis=1)
                    else:
                        r1=R(at,yy,np.ones_like(yy));rhs=-r0/(r1-r0)
                        defects[order]=at_nodes-float(sp.Rational(task['initial']))-check_nodes*np.sum(weights*rhs,axis=1)
                quadrature={'sampled_nodes':65,'defect_max_by_order':{str(k):float(np.max(abs(v))) for k,v in defects.items()},
                            'defect_change_16_to_64':float(np.max(abs(defects[16]-defects[64])))}
            rows.append({'quadrature_sensitivity':quadrature,'task':data['task'],'method':data['method'],'reference':kind,'evaluation_points':1025,
                         'profile_error_max':profile_error,'physical_field_error_max':physical,
                         'sampled_residual_max':float(np.max(abs(residual))),'trace_error':trace,'guards':guards,
                         'sampled_admissible':bool(admissible),'cost':data['cost'],'run_class':data['settings']['run_class'],
                         'status':data['candidate']['status'],'verification':data['verification']['status']})
        except Exception as exc:rows.append({'task':data['task'],'method':data['method'],'status':'diagnostic_failed','reason':str(exc)})
    record={'scope':'sampled differences to numerical references; reference uncertainty is not subtracted; no continuous neural error certificate','wall_seconds':time.perf_counter()-start,'rows':rows}
    (run_dir/'STATISTICS.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    text=['# Managed ODE pilot diagnostics','','1025 evaluation coordinates. Profile error is in q for N3; the physical field error is in H. These are sampled reference differences, not true-error or continuous bounds; differences below reference uncertainty must not be used to rank methods.','',
          '| Task | Method | Profile/reference difference | Physical/reference difference | Residual max | Trace error | Chart guards |','|---|---|---:|---:|---:|---:|---|']
    for row in rows:
        if row['status']=='diagnostic_failed':text.append(f"| {row['task']} | {row['method']} | failed | — | — | — | {row['reason']} |")
        else:text.append(f"| {row['task']} | {row['method']} | {row['profile_error_max']:.3e} | {row['physical_field_error_max']:.3e} | {row['sampled_residual_max']:.3e} | {row['trace_error']:.3e} | {row['sampled_admissible']} |")
    (run_dir/'STATISTICS.md').write_text('\n'.join(text)+'\n');return record


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True,type=Path)
    p.add_argument('--tasks',type=Path,help='default: immutable TASKS.json beside candidates')
    p.add_argument('--annular-reference',type=Path,default=ROOT/'lie_reduce/results/REFERENCE_EXPERIMENT.json')
    a=p.parse_args();run(a.run,a.tasks,a.annular_reference)
