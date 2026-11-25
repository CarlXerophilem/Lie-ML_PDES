"""CPU-only series/reference experiment after the selected BB certificate passes."""
import json
from pathlib import Path
import resource
import time
import sympy as sp


def run(certificate,out):
    # Optional numerical dependencies are not imported by the symbolic core.
    import numpy as np
    import scipy
    from scipy.integrate import solve_ivp
    import mpmath as mp
    from flint import fmpq,ctx
    from .series import Series,annular
    from .run import serial
    if certificate['status']!='verified':raise ValueError('BB gate not passed')
    started=time.perf_counter();usage=resource.getrusage(resource.RUSAGE_SELF)
    ctx.cap=48;mp.mp.dps=80
    X=certificate['shared_halfwidth'];root=mp.sqrt(141)
    report={'schema':'Definition 6.1 reference experiment','scope':'selected annular saddle only',
            'ML':False,'method':'exact Q(sqrt(141)) recurrence and independent DOP853 integrator',
            'degree':40,'domain_halfwidth':X,'evaluation_points':401,'branches':[],
            'dependency_versions':{'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__},
            'reference_boundary':'DOP853 shares certified series starting data away from the critical point; integration is a sampled check, not a second proof.'}
    def rational_mp(q):return mp.mpf(str(q))
    def val(pairs,x,start=0):
        result=mp.mpf(0)
        for a,b in reversed(pairs[start:]):result=result*x+rational_mp(a)+rational_mp(b)*root
        return result
    for branch in certificate['branches']:
        sign=1 if sp.expand(branch['slope']).coeff(sp.sqrt(141))>0 else -1
        a=[fmpq(1),fmpq(-7,10)];b=[fmpq(0),fmpq(sign,30)]
        for degree in range(2,41):
            order=degree+3;r=Series([1,1],order=order);h=Series(a,b,order=order)
            D,N,_=annular(r,h);ra,rb=(D*h.diff()-N).coefficient(degree)
            divisor=Series(fmpq(1-degree,10),fmpq(sign*(degree+1),10),order=order)
            ca,cb=(-Series(ra,rb,order=order)/divisor).coefficient(0)
            a.append(ca);b.append(cb)
        h=Series(a,b,order=44);r=Series([1,1],order=44);D,N,_=annular(r,h)
        defect=D*h.diff()-N
        if not all(defect.coefficient(n)==(0,0) for n in range(41)):
            raise ArithmeticError('exact undivided residual coefficient check failed')
        pairs=h.pairs(41);Xmp=rational_mp(X);slope=mp.mpf(-7)/10+sign*root/30
        grid=[-Xmp+2*Xmp*i/400 for i in range(401)]
        sampled_DH=[]
        for rho in grid:
            hh=val(pairs,rho)
            derivative=sum(n*(rational_mp(a[n])+rational_mp(b[n])*root)*rho**(n-1) for n in range(1,41))
            DD,NN,_=annular(1+rho,hh);sampled_DH.append(abs(DD*derivative-NN))
        rows=[];R=branch['disk']['R'];W=branch['disk']['R_w'];q=X/R
        for degree in (5,10,20,40):
            tail=R*W*q**(degree+1)/(1-q)
            difference=max(abs(val(pairs,rho)-val(pairs[:degree+1],rho)) for rho in grid)
            if difference>rational_mp(tail):raise ArithmeticError('sampled truncation difference exceeds proved tail')
            rows.append({'degree':degree,'continuous_H_tail_upper':tail,
                         'sampled_difference_to_degree40':mp.nstr(difference,25),
                         'continuous_scaled_q_tail_upper':W/X*q**degree/(1-q)})
        dop=[]
        for direction in (-1,1):
            eps=direction*float(X)/128
            y0=float(val(pairs,mp.mpf(eps)))
            def rhs(rho,y):
                DD,NN,_=annular(1+rho,y[0]);return [NN/DD]
            sol=solve_ivp(rhs,(eps,direction*float(X)),[y0],method='DOP853',rtol=2.3e-14,atol=1e-15,dense_output=True)
            if not sol.success:raise ArithmeticError(sol.message)
            nodes=np.linspace(eps,direction*float(X),201);truth=np.array([float(val(pairs,mp.mpf(x))) for x in nodes])
            predicted=sol.sol(nodes)[0];field_error=float(np.max(abs(predicted-truth)))
            if field_error>1e-10:raise ArithmeticError('independent-integrator disagreement exceeds 1e-10')
            # Bound cancellation in this diagnostic by reporting it as float64 sampled only.
            scaled=float(np.max(abs(predicted-truth)/(float(X)*abs(nodes))))
            dop.append({'direction':direction,'nfev':sol.nfev,'sampled_H_disagreement':field_error,
                        'sampled_scaled_q_disagreement':scaled,'status':'solver_terminated_successfully',
                        'start_offset':eps,'initial_data':'degree40 certified branch series rounded to float64'})
        report['branches'].append({'slope':branch['slope'],'coefficients_Qsqrt141':pairs,
            'exact_residual_coefficients_zero_through':40,'sampled_80digit_residual_max':mp.nstr(max(sampled_DH),25),
            'Taylor':rows,'DOP853':dop,'status':'reference_checks_passed'})
    after=resource.getrusage(resource.RUSAGE_SELF)
    report['resources']={'wall_seconds':time.perf_counter()-started,'user_cpu_seconds':after.ru_utime-usage.ru_utime,
                         'system_cpu_seconds':after.ru_stime-usage.ru_stime,'process_peak_rss_bytes':after.ru_maxrss*1024}
    report['status']='passed'
    out=Path(out);(out/'REFERENCE_EXPERIMENT.json').write_text(json.dumps(serial(report),indent=2)+'\n')
    lines=['# Selected annular saddle: exact series experiment','',
           'The continuous tail bounds come from the complex BB disks. DOP853 disagreements are sampled diagnostics with shared series starting data.','',
           '| Branch | Degree | Continuous H tail upper | Sampled difference to degree 40 |','|---|---|---|---|']
    for branch in report['branches']:
        for row in branch['Taylor']:
            lines.append(f"| {branch['slope']} | {row['degree']} | {sp.N(row['continuous_H_tail_upper'],8)} | {row['sampled_difference_to_degree40']} |")
    (out/'REFERENCE_EXPERIMENT.md').write_text('\n'.join(lines)+'\n')
    return {'status':'passed','record':'REFERENCE_EXPERIMENT.json','resources':report['resources']}
