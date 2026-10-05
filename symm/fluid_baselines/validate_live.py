"""Finite-time validation for live stepping; not a global error certificate."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np

from .live_numerics import make_stepper


def validate():
    started=perf_counter()
    result={"created_at":datetime.now(timezone.utc).isoformat(),"checks":{},"observations":{}}
    shear=make_stepper("ns",n=24,kind="shear")
    shear.advance_to(.2)
    shear.set_parameters({"nu":.1})
    shear.advance_to(100.)
    exact=np.exp(-(.01*.2+.1*99.8))*np.cos(shear.y)[:,None]
    error=float(np.max(abs(shear.fields()["u"]-exact)))
    result["observations"]["piecewise_viscosity_shear_max_error_t100"]=error
    result["checks"]["analytic_shear_to_t100"]=error<1e-9
    print("analytic shear",error,flush=True)

    ns=make_stepper("ns",n=128)
    fine=make_stepper("ns",n=256)
    observations=[]
    initial=ns.diagnostics()
    for target in (1.,2.,5.,10.,20.,50.,100.):
        ns.advance_to(target)
        row={"time":target,**ns.diagnostics()}
        if target==5.:
            fine.advance_to(target)
            row["refinement_128_256_vorticity_rms"]=float(np.sqrt(np.mean(
                (ns.fields()["vorticity"]-fine.fields()["vorticity"][::2,::2])**2)))
        observations.append(row)
        print("NS",target,row,flush=True)
    result["observations"]["NS_128_long_time"]=observations
    energies=[initial["kinetic_energy"]]+[r["kinetic_energy"] for r in observations]
    enstrophies=[initial["enstrophy"]]+[r["enstrophy"] for r in observations]
    result["checks"]["NS_dissipation_to_t100"]=bool(max(np.diff(energies))<=1e-10 and max(np.diff(enstrophies))<=1e-10)
    result["checks"]["NS_divergence_to_t100"]=max(r["divergence_max"] for r in observations)<1e-10
    result["checks"]["NS_spectral_tail_indicator"]=max(r["spectral_tail_ratio"] for r in observations)<1e-3
    result["checks"]["NS_refinement_at_t5"]=observations[2]["refinement_128_256_vorticity_rms"]<1e-5

    sve=make_stepper("sve",n=128)
    sve.advance_to(1.)
    changed=sve.clone()
    fields=changed.fields()
    changed.set_parameters({"m":3.02})
    jump=max(float(np.max(abs(changed.fields()[key]-value))) for key,value in fields.items())
    result["checks"]["SVE_coefficient_change_preserves_fields"]=jump==0
    observations=[]
    for target in (2.,5.,10.,20.,50.,100.):
        sve.advance_to(target);changed.advance_to(target)
        row={"time":target,"reference":sve.diagnostics(),"perturbed":changed.diagnostics(),
             "depth_difference_rms":float(np.sqrt(np.mean((sve.fields()["h"]-changed.fields()["h"])**2)))}
        observations.append(row)
        print("SVE",target,row["depth_difference_rms"],flush=True)
    result["observations"]["SVE_m3_to_3_02_at_t1"]=observations
    result["checks"]["SVE_positive_to_t100"]=all(min(r[branch]["minimum_depth"],r[branch]["minimum_velocity"])>0
                                                                for r in observations for branch in ("reference","perturbed"))
    result["checks"]["SVE_integrals_to_t100"]=all(max(r[branch]["mass_relative_drift"],r[branch]["bed_mean_absolute_drift"])<1e-10
                                                                for r in observations for branch in ("reference","perturbed"))
    result["checks"]["SVE_perturbation_changes_future"]=max(r["depth_difference_rms"] for r in observations)>1e-9
    result["passed"]=all(result["checks"].values())
    result["wall_seconds"]=perf_counter()-started
    result["source_sha256"]={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (Path(__file__),Path(__file__).with_name("live_numerics.py"))}
    result["limitations"]=["Finite-time numerical checks on specified initial data only.",
        "NS refinement is checked at t=5; diagnostics at later times are not a uniform error bound.",
        "SVE full-PDE perturbation uses a diffusive first-order smooth-flow baseline.",
        "No ML speedup, maximal symmetry classification, or global existence claim."]
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=validate()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"passed":result["passed"],"checks":result["checks"],"wall_seconds":result["wall_seconds"]}),flush=True)
    raise SystemExit(0 if result["passed"] else 1)
