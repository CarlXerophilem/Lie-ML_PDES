"""Reproducible classical and neural experiments, including unsuccessful runs."""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from time import perf_counter
from typing import Callable, Any
import json

import numpy as np
from scipy.integrate import simpson, cumulative_trapezoid

from .problems import ProfileProblem, scalar_lab
from .classical_integrators import solve_reference, ReferenceSolution
from .chebyshev_control import solve_chebyshev
from .hybrid_profile import train_profile, frozen_state
from symm.selection.complexity_selector import cost_crossing, ComplexityRecord, choose_minimum_cost


def write_json(path: Path, payload: Any) -> None:
    def finite(value: Any) -> Any:
        if isinstance(value, dict):
            return {key: finite(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [finite(item) for item in value]
        if isinstance(value, (float, np.floating)):
            return float(value) if np.isfinite(value) else None
        if isinstance(value, np.integer):
            return int(value)
        return value
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(finite(payload), indent=2, allow_nan=False)+"\n")


def latency(function: Callable[[], Any], repetitions: int = 5) -> dict[str, float]:
    function()
    times = []
    for _ in range(repetitions):
        started = perf_counter()
        function()
        times.append(perf_counter()-started)
    return {"median": float(np.median(times)), "min": min(times), "max": max(times)}


def original_scaled_residual(problem: ProfileProblem, points: np.ndarray, jets: np.ndarray) -> np.ndarray:
    """Independent original-coordinate differentiation at t=1.

    This returns t*E for X5 and t^2*E for common scaling. The common formula
    reuses the independent chain-rule evaluator in the retained evidence package.
    """
    f,p,c,h=jets
    if problem.chart != "cubic_X5":
        scalar_lab()
        from sve_lab.trials import original_residual
        derivatives={(i,j):np.zeros_like(points) for n in range(4) for i in range(n+1) for j in [n-i]}
        for order, values in enumerate(jets):
            derivatives[(0,order)] = values
        return original_residual(derivatives, points, problem.exponent,
                    problem.chart == "common_corrected", problem.gravity, problem.kappa)[0]
    z=points
    phi_t,phi_s=2*z*p,p
    phi_tt,phi_ts,phi_ss=2*z*p+4*z*z*c,2*(p+z*c),c
    phi_ttt,phi_tss=12*z*z*c+8*z**3*h,2*(2*c+z*h)
    g,beta=problem.gravity,3*problem.kappa
    return (phi_s*phi_ttt+phi_ts*phi_tt-g*(phi_tss/phi_s**2-2*phi_ss*phi_ts/phi_s**3)
        -g*beta*(2*phi_t*phi_ts**2/phi_s+phi_t**2*phi_tss/phi_s-phi_t**2*phi_ts*phi_ss/phi_s**2))


def full_query(problem: ProfileProblem, points: np.ndarray, jets: np.ndarray) -> dict[str, np.ndarray]:
    guards=problem.guards(points,jets)
    if any(not np.isfinite(v) or v <= 1e-9 for v in guards.values()):
        raise ValueError("full query requires a classical fallback: sampled branch guard failed")
    raw=original_scaled_residual(problem,points,jets)
    if problem.chart == "cubic_X5":
        return {"phi":jets[0],"phi_s_at_t1":jets[1],"phi_t_at_t1":2*points*jets[1],"residual_scaled":raw}
    a=jets[2]*(points**2*jets[1]-problem.gravity/jets[1]**2)
    bed=cumulative_trapezoid(-a/problem.gravity,points,initial=0.)
    return {"phi_at_t2":2*jets[0],"depth":1/jets[1],"velocity":jets[0]-points*jets[1],
            "bed_at_t2":bed+problem.integral/problem.gravity*np.log(2),"residual_scaled":raw}


def diagnostics(problem: ProfileProblem, points: np.ndarray, jets: np.ndarray,
                reference: np.ndarray) -> dict[str, Any]:
    guards=problem.guards(points,jets)
    valid=all(np.isfinite(v) and v>1e-9 for v in guards.values()) and bool(np.all(np.isfinite(jets)))
    if not valid:
        return {"accuracy_admissible":False,"status":"invalid-branch", "sampled_guards":guards}
    reduced=np.asarray(problem.residual(points,*jets))
    original=original_scaled_residual(problem,points,jets)
    l2=float(np.sqrt(problem.weight*simpson(original**2,x=points)))
    error=float(np.max(np.abs(jets[0]-reference[0])))
    # Independently integrate the time factor/Jacobian in original coordinates.
    times,weights=np.polynomial.legendre.leggauss(16)
    times,weights=1+(times+1)/2,weights/2
    power=2 if problem.chart == "cubic_X5" else 4
    jacobian=1/times**2 if problem.chart == "cubic_X5" else times
    original_integral=float(np.dot(weights,jacobian/times**power)*simpson(original**2,x=points))
    # In (t,z): X5 E=t^-1 R, J=t^-2; common E=t^-2 R, J=t.
    quotient_integral=problem.weight*float(simpson(original**2,x=points))
    if not np.isclose(original_integral,quotient_integral,rtol=1e-12,atol=1e-16):
        raise AssertionError("original and quotient residual measures disagree")
    drift=None if problem.integral is None else float(np.max(np.abs(problem.leading(points,*jets[:3])*jets[2]-problem.integral)))
    return {"status":"sampled-validation", "accuracy_admissible":error<=1e-6 and l2<=1e-4,
        "max_profile_error":error,"max_derivative_errors":[float(np.max(np.abs(jets[i]-reference[i]))) for i in (1,2)],
        "original_residual_L2":l2,"raw_reduced_residual_Linf":float(np.max(np.abs(reduced))),
        "raw_original_scaled_residual_Linf":float(np.max(np.abs(original))),
        "original_vs_reduced_residual_Linf":float(np.max(np.abs(original-reduced))),
        "measure_pullback_difference":abs(original_integral-quotient_integral),
        "first_integral_drift":drift,"initial_trace_error":float(np.max(np.abs(jets[:3,0]-problem.initial))),
        "sampled_guards":guards,"guard_scope":"1001 sampled points; no continuous certificate for this extended interval"}


def run_benchmarks(out: Path, *, seeds: tuple[int,...]=(17,23,41), quick: bool=False,
                   adam_steps: int=500, lbfgs_evaluations: int=250,
                   campaign_seconds: float=1800.) -> dict:
    grid=np.linspace(1,1.5,1001)
    cases=[ProfileProblem("cubic_X5",eta=eta) for eta in (-.1,0.,.1)]
    cases += [ProfileProblem(chart,m,eta) for chart in ("common_printed","common_corrected")
              for m in (1.,2.,2.9,3.,3.1,4.) for eta in (-.1,0.,.1)]
    references: dict[tuple,ReferenceSolution]={}
    controls: dict[tuple,Any]={}
    classical=[]
    tolerance_records=[]
    failures=[]
    integrated_records=[]
    reference_seconds=0.
    for problem in cases:
        key=(problem.chart,problem.exponent,problem.eta)
        oracle=solve_reference(problem,rtol=1e-14)
        reference_seconds+=oracle.setup_seconds
        references[key]=oracle
        reference=oracle.state_jets(grid)
        for method in ("DOP853","Radau"):
            for tolerance in (1e-11,1e-12,1e-13,1e-14):
                solution=oracle if method=="DOP853" and tolerance==1e-14 else solve_reference(problem,method,rtol=tolerance)
                error=float(np.max(np.abs(solution.state_jets(grid)[:3]-reference[:3])))
                tolerance_records.append({"problem":asdict(problem),"method":method,"requested_rtol":tolerance,
                    "effective_rtol":solution.effective_rtol,"atol":1e-14,"warnings":solution.warnings,
                    "state_cross_reference_error":error,"setup_seconds":solution.setup_seconds,"passed":error<=1e-9})
                if tolerance==1e-12:
                    jets=solution.dense_jets(grid)
                    row={"problem":asdict(problem),"method":method,"degree":None,"setup_seconds":solution.setup_seconds,
                         "metrics":diagnostics(problem,grid,jets,reference),
                         "profile_latency":latency(lambda:solution.profile(grid)),
                         "full_query_latency":latency(lambda:full_query(problem,grid,solution.dense_jets(grid))),
                         "residual_scope":"actual scalar dense interpolant; state convergence is recorded separately"}
                    classical.append(row)
        if problem.chart != "cubic_X5":
            integrated=solve_reference(problem,integrated=True,rtol=1e-13)
            error=float(np.max(np.abs(integrated.state_jets(grid)[:3]-reference[:3])))
            if error>1e-9:
                raise AssertionError("second/third order references disagree")
            integrated_records.append({"problem":asdict(problem),"state_cross_reference_error":error,
                "setup_seconds":integrated.setup_seconds,"requested_rtol":integrated.requested_rtol,
                "effective_rtol":integrated.effective_rtol,"passed":True,"actual_order":2})
        for degree in (8,12,16,24):
            try:
                spectral=solve_chebyshev(problem,degree)
                jets=spectral.jets(grid)
                metrics=diagnostics(problem,grid,jets,reference)
                row={"problem":asdict(problem),"method":"Chebyshev","degree":degree,
                    "setup_seconds":spectral.setup_seconds,"collocation_max_residual":spectral.collocation_max_residual,
                    "optimizer_success":spectral.optimizer_success,"metrics":metrics,
                    "profile_latency":latency(lambda:spectral.profile(grid)),
                    "full_query_latency":latency(lambda:full_query(problem,grid,spectral.jets(grid)))}
                classical.append(row)
                if metrics["accuracy_admissible"] and key not in controls:
                    controls[key]=(spectral,row)
            except (ValueError,RuntimeError,FloatingPointError) as error:
                failures.append({"problem":asdict(problem),"method":"Chebyshev","degree":degree,"status":"failed", "reason":str(error)})
        if key not in controls:
            raise RuntimeError(f"no accuracy-admissible spectral control for {key}")
    if not all(row["passed"] for row in tolerance_records):
        raise AssertionError("reference tolerance ladder verification failed")
    print(f"Classical controls: {len(cases)} cases, {len(tolerance_records)} tolerance checks",flush=True)
    neural=[]
    started_campaign=perf_counter()
    fixed=[case for case in cases if case.exponent==3. and (not quick or case.eta==0.)]
    tasks=[]
    # Interleave methods within each seed/problem, then conditioned tasks within
    # each seed. A campaign stop retains every unstarted task as a negative record.
    for seed in seeds:
        for problem in fixed:
            tasks.extend((problem,kind,seed,False) for kind in ("PINN","PIKAN"))
        for chart in ("common_printed","common_corrected"):
            tasks.extend((ProfileProblem(chart),kind,seed,True) for kind in ("PINN","PIKAN"))
    for index,(problem,kind,seed,conditioned) in enumerate(tasks):
        remaining=campaign_seconds-(perf_counter()-started_campaign)
        header={"problem":asdict(problem),"method":kind,"seed":seed,"conditioned":conditioned}
        if remaining<=0:
            neural.append({**header,"status":"campaign-budget-not-run","accuracy_admissible":False})
            continue
        outcome=train_profile(problem,kind,seed=seed,conditioned=conditioned,adam_steps=adam_steps,
                    lbfgs_evaluations=lbfgs_evaluations,seconds_limit=min(120.,remaining),nodes=24 if quick else 32)
        candidate_path=out/"candidates"/f"{index:03d}-{kind}-{seed}.json"
        write_json(candidate_path,{**header,**frozen_state(outcome)})
        pairs=((3.,-.05),(3.,.05),(2.95,-.075),(3.05,.075)) if conditioned else ((problem.exponent,problem.eta),)
        validations=[]
        costs=[]
        validation_reference_seconds=0.
        for m,eta in pairs:
            query=ProfileProblem(problem.chart,m,eta)
            key=(query.chart,m,eta)
            oracle=references.get(key)
            if oracle is None:
                oracle=solve_reference(query,rtol=1e-14)
                references[key]=oracle
            validation_reference_seconds+=oracle.setup_seconds
            reference=oracle.state_jets(grid)
            jets=outcome.model.jets(grid,exponent=m,eta=eta)
            metrics=diagnostics(query,grid,jets,reference)
            baseline=controls.get(key)
            if baseline is None:
                spectral=solve_chebyshev(query,16)
                baseline_metrics=diagnostics(query,grid,spectral.jets(grid),reference)
                baseline=(spectral,{"metrics":baseline_metrics,"degree":16,"setup_seconds":spectral.setup_seconds})
                controls[key]=baseline
            spectral,baseline_row=baseline
            profile_time=latency(lambda:outcome.model.profile(grid,exponent=m,eta=eta))
            # Failed guard checks require a fallback whose work is included.
            def neural_query() -> Any:
                try:
                    candidate=outcome.model.jets(grid,exponent=m,eta=eta)
                    if not metrics["accuracy_admissible"]:
                        raise ValueError("validation accuracy gate requires fallback")
                    return full_query(query,grid,candidate)
                except ValueError:
                    fallback=solve_reference(query)
                    return full_query(query,grid,fallback.state_jets(grid))
            full_time=latency(neural_query)
            classical_cached=latency(lambda:full_query(query,grid,spectral.jets(grid)))
            classical_new=latency(lambda:full_query(query,grid,solve_chebyshev(query,spectral.degree).jets(grid)))
            validations.append({"m":m,"eta":eta,"metrics":metrics,"profile_latency":profile_time,
                "full_query_latency":full_time,"classical_cached_full_query":classical_cached,
                "classical_new_parameter_query":classical_new,"baseline_degree":spectral.degree,
                "baseline_accuracy_admissible":baseline_row["metrics"]["accuracy_admissible"]})
            costs.append((full_time["median"],classical_cached["median"],classical_new["median"],spectral.setup_seconds))
        eligible=all(v["metrics"]["accuracy_admissible"] and v["baseline_accuracy_admissible"] for v in validations)
        neural_cost=float(np.mean([c[0] for c in costs]))
        cached_cost=float(np.mean([c[1] for c in costs]))
        new_cost=float(np.mean([c[2] for c in costs]))
        setup=outcome.seconds+validation_reference_seconds
        cached_setup=float(np.mean([c[3] for c in costs]))+validation_reference_seconds
        neural.append({**header,"status":outcome.status,"accuracy_admissible":eligible,
            "training_seconds":outcome.seconds,"reference_validation_seconds":validation_reference_seconds,
            "adam_updates":outcome.adam_updates,"lbfgs_evaluations":outcome.lbfgs_evaluations,
            "best_training_loss":outcome.best_loss,"parameter_count":outcome.parameter_count,
            "candidate":str(candidate_path.relative_to(out)),"validation":validations,
            "costs":{"neural_setup":setup,"cached_classical_setup":cached_setup,
                "neural_full_query":neural_cost,"cached_classical_query":cached_cost,
                "new_parameter_classical_query":new_cost,
                "cached_profile_crossing":cost_crossing(setup,cached_setup,neural_cost,cached_cost,admissible=eligible),
                "new_parameter_crossing":cost_crossing(setup,0.,neural_cost,new_cost,admissible=eligible and conditioned),
                "scope":"measured held-out workload; arithmetic extrapolation conditional on accuracy and costs"}})
        print(f"Neural {index+1}/{len(tasks)} {problem.chart} {kind} seed={seed} family={conditioned} {outcome.status} admissible={eligible}",flush=True)
        write_json(out/"experiment_results.partial.json",{"classical":classical,"neural":neural,"tolerance_ladder":tolerance_records,"failed_controls":failures})
    decisions=[]
    for problem in cases:
        key=(problem.chart,problem.exponent,problem.eta)
        matching=[row for row in classical if row["problem"]==asdict(problem)]
        candidates=[]
        for row in matching:
            metrics=row["metrics"]
            complexity=ComplexityRecord(1,1,3,1,None,metrics["sampled_guards"]["min_abs_leading"])
            row["complexity_record"]=asdict(complexity)
            candidates.append({"id":f"{row['method']}-{row['degree']}",
                "admissible":metrics["accuracy_admissible"],
                "setup_seconds":row["setup_seconds"]+references[key].setup_seconds,
                "query_seconds":row["full_query_latency"]["median"],"complexity":asdict(complexity)})
        for row in neural:
            if row["problem"]==asdict(problem) and not row["conditioned"] and "costs" in row:
                candidates.append({"id":f"{row['method']}-seed-{row['seed']}",
                    "admissible":row["accuracy_admissible"],"setup_seconds":row["costs"]["neural_setup"],
                    "query_seconds":row["costs"]["neural_full_query"]})
        decisions.append({"problem":asdict(problem),"workload":"cached fixed profile; full reconstruction query",
                          "cost_minima":[choose_minimum_cost(candidates,count) for count in (1,1000)]})
    result={"status":"benchmarked","scope":"constructed compatible data; empirical approximation and timing",
        "grid_points":len(grid),"classical_cases":len(cases),"classical":classical,"tolerance_ladder":tolerance_records,
        "neural":neural,"failed_controls":failures,"reference_generation_seconds":reference_seconds,
        "first_integral_reference_comparisons":integrated_records,"selection_decisions":decisions,
        "neural_campaign_seconds":perf_counter()-started_campaign,
        "accuracy_targets":{"profile_Linf":1e-6,"original_residual_L2":1e-4},
        "continuous_error_certificate":False,"uniform_extended_tube_certificate":False}
    write_json(out/"experiment_results.json",result)
    return result
