"""Run with: python -B -m symm.fluid_baselines.run --output PATH.

All comparisons are deterministic controls, not performance/novelty proofs.
The output contains full precision NPZ arrays, lightweight dashboard JSON,
symbolic records, thresholds, package versions, and source SHA256 hashes.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import shutil
import socket
import sys

import numpy as np
from plotly.offline import get_plotlyjs

from symm.generic import PDEsReductor, reduce_in_chart
from .models import sve_scaling, fluid_translation, exact_control_residuals
from .numerics import sve_periodic, sve_reduced, vorticity_evolution


SVE_EQ = ["h_t + (h u)_x = 0", "(h u)_t + (h u^2 + g h^2/2)_x + g h B_x = 0",
          "B_t + kappa (u^m)_x = 0"]
NS_EQ = ["u_t + u u_x + v u_y + p_x = nu Laplacian(u)",
         "v_t + u v_x + v v_y + p_y = nu Laplacian(v)", "u_x + v_y = 0"]


def serial(value):
    if isinstance(value,np.ndarray):
        return value.tolist()
    if isinstance(value,np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


def write_json(path, value):
    path.write_text(json.dumps(value,default=serial,ensure_ascii=False,allow_nan=False,indent=2)+"\n",encoding="utf-8")


def symbolic_records():
    cases = [(f"sve-m{m}", sve_scaling(m)) for m in (2,3,4)]
    cases += [("NS-2D",fluid_translation()),("Oseen-2D",fluid_translation(True))]
    records = {}
    for name,(problem,gen,chart,matrix) in cases:
        outcome = reduce_in_chart(problem,gen,chart,symmetry_multipliers=matrix)
        rank = PDEsReductor().rank(problem.system)
        records[name] = {"problem":problem.as_dict(),"supplied_generator":gen.as_dict(),
                         "chart":chart.as_dict(),"multiplier_matrix":str(matrix),
                         "reduction":outcome.as_dict(),"translation_ranking":rank.as_dict(),
                         "readable_equations":list(map(str,problem.system.equations)),
                         "readable_reduced_equations":list(map(str,outcome.reduced_system.equations))
                            if outcome.reduced_system else []}
    controls = exact_control_residuals()
    return records,{name:list(map(str,values)) for name,values in controls.items()}


def run_suite(output):
    output = Path(output)
    if (output/"manifest.json").exists():
        raise FileExistsError("use a fresh output directory to preserve earlier evidence")
    output.mkdir(parents=True,exist_ok=True)
    records,controls = symbolic_records()
    write_json(output/"symbolic_records.json",{"reductions":records,"exact_controls":controls})
    cases, numerical = [],{}
    gates = {"cubic_original_SVE_chart":records["sve-m3"]["reduction"]["certificate"]["status"]=="verified",
             "noncubic_supplied_scaling_rejected":all(records[f"sve-m{m}"]["reduction"]["certificate"]["status"]=="unsupported" for m in (2,4)),
             "NS_and_Oseen_translation_charts":all(records[s]["reduction"]["certificate"]["status"]=="verified" for s in ("NS-2D","Oseen-2D")),
             "analytic_controls_original_PDE_residuals_zero":all(r=="0" for values in controls.values() for r in values)}
    def save(case_id,title,model,parameters,equations,solver,reduction,evidence,data):
        data["id"] = case_id
        arrays = {"times":data["times"],"x":data["x"],**data["fields"]}
        if "y" in data:
            arrays["y"] = data["y"]
        np.savez_compressed(output/f"{case_id}.npz",**arrays,
                            **{f"diagnostic_{k}":v for k,v in data["diagnostics"].items()})
        # Dashboard copies are rounded for transfer; the NPZ retains float64 values.
        display = {**data,"fields":{k:np.round(v,7) for k,v in data["fields"].items()}}
        (output/f"{case_id}.json").write_text(json.dumps(display,default=serial,ensure_ascii=False,
                                                       allow_nan=False,separators=(",",":"))+"\n",encoding="utf-8")
        cases.append(dict(id=case_id,title=title,model=model,parameters=parameters,equations=equations,
                          solver=solver,reduction=reduction,evidence=evidence,file=f"{case_id}.json",metrics=data["metrics"]))
        numerical[case_id] = data
        print(f"{case_id}: {json.dumps(data['metrics'])}",flush=True)

    for m in (2,3,4):
        for kappa in (.05,.1):
            case_id = f"sve-m{m}-k{kappa}"
            data = sve_periodic(m=m,kappa=kappa)
            fine = sve_periodic(n=256,m=m,kappa=kappa,snapshots=2)
            finer = sve_periodic(n=512,m=m,kappa=kappa,snapshots=2)
            def conservative(d):
                f = d["fields"]
                return np.array([f["h"][-1],f["h"][-1]*f["u"][-1],f["bed"][-1]])
            a,b,c = map(conservative,(data,fine,finer))
            coarse_error = float(np.sqrt(np.mean((a-b.reshape(3,128,2).mean(axis=2))**2)))
            fine_error = float(np.sqrt(np.mean((b-c.reshape(3,256,2).mean(axis=2))**2)))
            data["metrics"].update(refinement_128_256_rms=coarse_error,refinement_256_512_rms=fine_error,
                                    refinement_error_ratio=coarse_error/fine_error)
            M = data["metrics"]
            gates[case_id] = (M["mass_relative_drift"]<1e-11 and M["bed_mean_absolute_drift"]<1e-11
                              and M["minimum_depth"]>.5 and M["minimum_velocity"]>0
                              and M["maximum_characteristic_imaginary_part"]<1e-12
                              and 1.5<M["refinement_error_ratio"]<2.5)
            save(case_id,f"Original SVE · m={m}, κ={kappa}","Eulerian SVE (1 space + time)",
                 dict(m=m,kappa=kappa,g=1,n=128,t_end=.4,boundary="periodic [0,2pi)"),SVE_EQ,
                 "Rusanov FV + centered bed source + SSPRK3; smooth positive branch",
                 "Full PDE evolution. Cubic scaling is separately verified; these periodic data do not use that scaling.",
                 "Mass/bed drift, positive depth, sampled hyperbolicity and three-grid self-convergence checks.",data)

    for kappa in (.05,.1,.2):
        case_id = f"sve-cubic-reduced-k{kappa}"
        data = sve_reduced(kappa=kappa)
        gates[case_id] = data["metrics"]["exact_profile_max_error"]<1e-9
        save(case_id,f"Reduced SVE · κ={kappa}","Original cubic SVE invariant family",
             dict(m=3,kappa=kappa,g=1,t_start=1,t_end=1.5,x_window=[.5,2],boundary="traces of invariant solution"),SVE_EQ,
             "DOP853 on 3 profiles; rtol=1e-11, atol=1e-13",
             "h=x²H(t), u=xV(t), B=x²C(t); verified local chart x>0.",
             "Exact original-balance residuals vanish; numerical profiles checked against closed form. The plotted x-window is not a closed periodic domain.",data)

    for kind in ("shear","taylor_green","interacting"):
        for nu in (.01,.1):
            case_id = f"ns-{kind}-nu{nu}"
            data = vorticity_evolution(nu=nu,kind=kind)
            if kind=="interacting":
                fine = vorticity_evolution(n=128,nu=nu,kind=kind,snapshots=41,max_dt=.005)
                error = float(np.sqrt(np.mean((data["fields"]["vorticity"][-1]-fine["fields"]["vorticity"][-1,::2,::2])**2)))
                data["metrics"]["refinement_64_128_final_vorticity_rms"] = error
            M = data["metrics"]
            gates[case_id] = (M["divergence_max"]<1e-11 and M["energy_max_increase"]<=1e-10
                              and M["enstrophy_max_increase"]<=1e-10
                              and M.get("exact_velocity_max_error",0)<1e-8
                              and M.get("refinement_64_128_final_vorticity_rms",0)<1e-5)
            save(case_id,f"2D NS · {kind.replace('_',' ')} · ν={nu}","2D incompressible Navier–Stokes",
                 dict(nu=nu,n=64,t_end=1,boundary="periodic [0,2pi)^2"),NS_EQ,
                 "Fourier vorticity + strict 2/3 dealiasing + RK4; dt<=0.01 plus CFL/diffusion bounds",
                 "x-translation invariant shear; V=0, constant P reduces to the heat equation." if kind=="shear" else
                 "Full 2D evolution; not an x-invariant reduced solution.",
                 "Analytic velocity control; divergence and dissipation checks." if kind!="interacting" else
                 "64/128 grid and timestep refinement; divergence and dissipation checks. No closed-form reference.",data)
    for nu in (.01,.1):
        case_id = f"oseen-nu{nu}"
        data = vorticity_evolution(nu=nu,kind="interacting",mean=(.3,-.2),linear=True)
        M = data["metrics"]
        gates[case_id] = M["exact_vorticity_max_error"]<1e-8 and M["divergence_max"]<1e-11
        equations = ["u_t + a u_x + b u_y + p_x = nu Laplacian(u)",
                     "v_t + a v_x + b v_y + p_y = nu Laplacian(v)","u_x + v_y = 0; (a,b) fixed"]
        save(case_id,f"2D Oseen · ν={nu}","2D constant-drift Oseen (linear NS control)",
             dict(nu=nu,a=.3,b=-.2,n=64,t_end=1,boundary="periodic [0,2pi)^2"),equations,
             "Fourier RK4, checked against the independent exact Fourier semigroup",
             "x-translation chart verified symbolically; these full 2D data are not x-invariant.",
             "Exact Fourier propagation control and divergence check.",data)

    source_root = Path(__file__).resolve().parents[1]
    files = sorted((source_root/"fluid_baselines").glob("*"))+sorted((source_root/"generic").glob("*.py"))
    provenance = {"created_at":datetime.now(timezone.utc).isoformat(),"host":socket.gethostname(),
                  "python":sys.version,"platform":platform.platform(),
                  "packages":{name:version(name) for name in ("numpy","scipy","sympy","plotly","matplotlib","pytest")},
                  "source_sha256":{str(p.relative_to(source_root.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in files if p.is_file()},
                  "external_CAS":{"maple":shutil.which("maple"),"reduce":shutil.which("redcsl") or shutil.which("reduce")},
                  "randomness":"none", "hardware_timing_scope":"single CPU run, not a speedup comparison"}
    write_json(output/"provenance.json",provenance)
    write_json(output/"verification.json",{"passed":all(gates.values()),"gates":gates,
                "thresholds":{"analytic_max_error":1e-8,"SVE_profile_error":1e-9,"NS_divergence":1e-11,
                              "NS_refinement_rms":1e-5,"SVE_refinement_ratio":[1.5,2.5]},
                "limitations":["No learned model or ML speedup measured.","No maximal symmetry classification or CAS completion.",
                               "Local invariant pullback verification is distinct from numerical evolution accuracy.",
                               "Global view means the whole simulated finite domain, not a global existence theorem.",
                               "SVE finite-volume control is smooth/periodic and not well-balanced or shock-certified.",
                               "Self-convergence is numerical evidence, not a rigorous error bound."]})
    write_json(output/"manifest.json",{"title":"LieML · Fluid evolution baselines","created_at":provenance["created_at"],"cases":cases})
    shutil.copyfile(Path(__file__).with_name("dashboard.html"),output/"index.html")
    (output/"plotly.min.js").write_text(get_plotlyjs(),encoding="utf-8")
    overview(output,numerical)
    print(json.dumps({"passed":all(gates.values()),"gates":len(gates),"cases":len(cases),"output":str(output)},indent=2),flush=True)
    return all(gates.values())


def overview(output,data):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig,axes = plt.subplots(2,3,figsize=(13,7.5),layout="constrained")
    for i,key in enumerate(("sve-m3-k0.1","sve-cubic-reduced-k0.1")):
        d = data[key]
        for j in (0,20,40):
            axes[0,i].plot(d["x"],d["fields"]["h"][j],label=f"t={d['times'][j]:.2f}")
        axes[0,i].set(title=key,xlabel="x",ylabel="water depth h")
        axes[0,i].legend()
    for i,nu in enumerate((.01,.1)):
        d = data[f"ns-interacting-nu{nu}"]
        im=axes[1,i].pcolormesh(d["x"],d["y"],d["fields"]["vorticity"][-1],cmap="RdBu_r",shading="auto",vmin=-3,vmax=3)
        axes[1,i].set(title=f"2D NS vorticity · ν={nu} · t=1",xlabel="x",ylabel="y",aspect="equal")
        fig.colorbar(im,ax=axes[1,i],shrink=.8)
        axes[0,2].plot(d["times"],d["diagnostics"]["kinetic energy"],label=f"ν={nu}")
        probe = len(d["x"])//4
        axes[1,2].plot(d["times"],d["fields"]["vorticity"][:,probe,probe],label=f"ν={nu}")
    axes[0,2].set(title="Whole-domain kinetic energy",xlabel="time",ylabel="mean kinetic energy")
    axes[1,2].set(title="Local NS probe · x=y=π/2",xlabel="time",ylabel="vorticity")
    axes[0,2].legend()
    axes[1,2].legend()
    fig.suptitle("Original SVE and 2D fluid controls · finite-time numerical baselines")
    fig.savefig(output/"overview.png",dpi=160)
    fig.savefig(output/"overview.pdf")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True,type=Path)
    args = parser.parse_args()
    return 0 if run_suite(args.output) else 1


if __name__ == "__main__":
    raise SystemExit(main())
