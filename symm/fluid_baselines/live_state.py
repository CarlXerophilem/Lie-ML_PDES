"""Persistent paired simulation; coefficient changes occur at recorded times.

The reference keeps its original parameters. The comparison keeps its current
field when parameters change. This is a piecewise-constant coefficient IVP,
not application of a Lie group action or a continuation theorem.
"""
from collections import deque
from datetime import datetime, timezone
import json
import hashlib
import math
import os
from pathlib import Path
import platform
import threading
import uuid

import numpy as np

from .live_numerics import make_stepper


FRAME_DT = .05
ARCHIVE_DT = .5
MAX_HORIZON = 1000.


def atomic_json(path, value):
    path = Path(path)
    temp = path.with_suffix(path.suffix+".tmp")
    temp.write_text(json.dumps(value,allow_nan=False,separators=(",",":"))+"\n",encoding="utf-8")
    os.replace(temp,path)


def horizon_value(value):
    value=float(value)
    if not math.isfinite(value) or not 0 < value <= MAX_HORIZON:
        raise ValueError(f"horizon must be finite and in (0,{MAX_HORIZON}]")
    return value


class Simulation:
    def __init__(self, directory, *, model="ns", n=64, kind="interacting",
                 parameters=None, horizon=100., running=True):
        self.root=Path(directory)
        self.root.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock()
        self.sequence=0
        self.checkpoint_time=0.
        self.error=None
        if (self.root/"current.json").exists():
            run_id=json.loads((self.root/"current.json").read_text())["run_id"]
            if not run_id or Path(run_id).name != run_id:
                raise ValueError("invalid saved run id")
            self.run_id=run_id
            self.directory=self.root/"runs"/run_id
            with np.load(self.directory/"checkpoint.npz",allow_pickle=False) as data:
                meta=json.loads(str(data["metadata"].item()))
                if meta.get("schema")!="lieml.live/1":
                    raise ValueError("unsupported checkpoint schema")
                self.reference,self.perturbed=self._restore_pair(meta,data)
            self.horizon=meta["horizon"]
            self.running=meta["running"]
            self.status=meta["status"]
            self.error=meta["error"]
            self.sequence=meta["sequence"]
            self.events=meta["events"]
            self.history=deque(meta["history"],maxlen=4000)
            self.frame_times=meta["frame_times"]
            self.checkpoint_time=self.time
        else:
            self._new(model,n,kind,parameters,horizon,running)

    @property
    def time(self):
        return float(self.reference.t)

    def _new(self,model,n,kind,parameters,horizon,running):
        if type(n) is not int or n<24 or n>128 or n%8:
            raise ValueError("grid n must be a multiple of 8 between 24 and 128")
        new=make_stepper(model=model,n=n,kind=kind,parameters=parameters)
        horizon=horizon_value(horizon)
        if hasattr(self,"reference"):
            self.running=False
            self.status="archived"
            self.checkpoint()
        self.reference,self.perturbed=new,new.clone()
        self.horizon=horizon
        self.running=bool(running)
        self.status="running" if self.running else "paused"
        self.error=None
        self.run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:8]
        self.directory=self.root/"runs"/self.run_id
        (self.directory/"frames").mkdir(parents=True)
        self.history=deque(maxlen=4000)
        self.frame_times=[]
        self.events=[]
        sources=Path(__file__).resolve().parent
        atomic_json(self.directory/"provenance.json",{
            "python":platform.python_version(),"numpy":np.__version__,
            "created_at":datetime.now(timezone.utc).isoformat(),
            "source_sha256":{name:hashlib.sha256((sources/name).read_bytes()).hexdigest()
                             for name in ("live_numerics.py","live_state.py","live_service.py")},
            "method":"paired periodic original-PDE stepping with piecewise-constant coefficients",
            "simulation_time_unit":"nondimensional","archive_interval":ARCHIVE_DT})
        self.sequence+=1
        self._event("created",parameters=dict(new.params))
        self._record()
        self._archive()
        self.checkpoint()
        atomic_json(self.root/"current.json",{"run_id":self.run_id})

    def _metadata(self,complete=False):
        meta={"schema":"lieml.live/1","run_id":self.run_id,"time":self.time,
              "model":self.reference.model,"kind":self.reference.kind,"n":self.reference.n,
              "parameters":{"reference":self.reference.params,"perturbed":self.perturbed.params},
              "steps":{"reference":getattr(self.reference,"steps",0),"perturbed":getattr(self.perturbed,"steps",0)}}
        if complete:
            meta.update(horizon=self.horizon,running=self.running,status=self.status,error=self.error,
                        sequence=self.sequence,events=self.events,history=list(self.history),frame_times=self.frame_times)
        return meta

    def _save(self,path,complete=False):
        temp=path.with_suffix(".tmp")
        with temp.open("wb") as stream:
            np.savez_compressed(stream,metadata=json.dumps(self._metadata(complete),allow_nan=False),
                                reference=self.reference.state,perturbed=self.perturbed.state)
        os.replace(temp,path)

    @staticmethod
    def _restore_pair(meta,data):
        pair=[]
        for name in ("reference","perturbed"):
            stepper=make_stepper(model=meta["model"],n=meta["n"],kind=meta["kind"],parameters=meta["parameters"][name])
            state=data[name].copy()
            if state.shape!=stepper.state.shape or not np.all(np.isfinite(state)):
                raise ValueError("checkpoint field shape or values invalid")
            stepper.state=state
            stepper.t=float(meta["time"])
            if hasattr(stepper,"steps"):
                stepper.steps=meta.get("steps",{}).get(name,0)
            pair.append(stepper)
        return pair

    def _event(self,action,**extra):
        event={"time":self.time,"action":action,"wall_time":datetime.now(timezone.utc).isoformat(),**extra}
        self.events.append(event)
        self.events=self.events[-200:]
        with (self.directory/"events.jsonl").open("a",encoding="utf-8") as stream:
            stream.write(json.dumps(event,allow_nan=False)+"\n")

    @staticmethod
    def _diagnostics(reference,perturbed):
        a,b=reference.fields(),perturbed.fields()
        field="h" if reference.model=="sve" else "vorticity"
        return {"reference":reference.diagnostics(),"perturbed":perturbed.diagnostics(),
                "difference_l2":float(np.sqrt(np.mean((a[field]-b[field])**2))),
                "difference_field":field}

    def _record(self):
        entry={"time":self.time,**self._diagnostics(self.reference,self.perturbed)}
        self.history.append(entry)
        return entry

    def _archive(self):
        self._save(self.directory/"frames"/f"{len(self.frame_times):06d}.npz")
        self.frame_times.append(self.time)
        with (self.directory/"diagnostics.jsonl").open("a",encoding="utf-8") as stream:
            stream.write(json.dumps(self.history[-1],allow_nan=False)+"\n")

    def checkpoint(self):
        with self.lock:
            self._save(self.directory/"checkpoint.npz",complete=True)
            self.checkpoint_time=self.time

    def advance(self,target):
        with self.lock:
            target=float(target)
            if not math.isfinite(target) or target<self.time:
                raise ValueError("target time must be finite and not in the past")
            target=min(target,self.horizon)
            if target<=self.time:
                return
            # Both branches commit together; failed stages keep the last good pair.
            left,right=self.reference.clone(),self.perturbed.clone()
            try:
                left.advance_to(target)
                right.advance_to(target)
                diagnostics=self._diagnostics(left,right)
                json.dumps(diagnostics,allow_nan=False)
            except Exception as exc:
                self.running=False; self.status="failed"; self.error=str(exc)
                self._event("failure",message=self.error)
                self.checkpoint()
                raise
            self.reference,self.perturbed=left,right
            self.sequence+=1
            self.history.append({"time":self.time,**diagnostics})
            if self.time>=self.horizon-1e-12:
                self.running=False;self.status="horizon-reached"
            if self.time-self.frame_times[-1]>=ARCHIVE_DT-1e-10 or not self.running:
                self._archive();self.checkpoint()

    @staticmethod
    def _view(reference,perturbed,meta):
        a,b=reference.fields(),perturbed.fields()
        # Keep field differences at full precision before rounding for display.
        convert=lambda values:{k:np.round(v,10).tolist() for k,v in values.items()}
        return {**meta,"dimension":reference.dimension,"x":reference.x.tolist(),
                "y":reference.y.tolist() if reference.y is not None else None,
                "reference":convert(a),"perturbed":convert(b),
                "difference":convert({k:b[k]-a[k] for k in a}),
                "diagnostics":Simulation._diagnostics(reference,perturbed)}

    def snapshot(self):
        with self.lock:
            meta=self._metadata()
            meta.update(horizon=self.horizon,running=self.running,status=self.status,error=self.error,
                        sequence=self.sequence,history=list(self.history),events=list(self.events),
                        archive_frames=len(self.frame_times),checkpoint_time=self.checkpoint_time,
                        capabilities={"max_horizon":MAX_HORIZON,"frame_dt":FRAME_DT})
            return self._view(self.reference,self.perturbed,meta)

    def frame(self,index):
        with self.lock:
            if type(index) is not int or not 0<=index<len(self.frame_times):
                raise ValueError("frame index out of range")
            with np.load(self.directory/"frames"/f"{index:06d}.npz",allow_pickle=False) as data:
                meta=json.loads(str(data["metadata"].item()))
                left,right=self._restore_pair(meta,data)
            return self._view(left,right,meta)

    def control(self,command):
        if not isinstance(command,dict):
            raise ValueError("control must be a JSON object")
        with self.lock:
            action=command.get("action")
            if action=="reset":
                model=command.get("model","ns")
                self._new(model,command.get("n",128 if model=="sve" else 64),
                          command.get("kind","interacting"),command.get("parameters"),
                          command.get("horizon",100),True)
                return self.snapshot()
            if action=="perturb":
                params=command.get("parameters")
                if not isinstance(params,dict) or not params:
                    raise ValueError("supply a nonempty parameters object")
                candidate=self.perturbed.clone()
                candidate.set_parameters(params)
                old=dict(self.perturbed.params)
                self.perturbed=candidate
                self._event("perturb",previous=old,parameters=dict(candidate.params))
                self._record(); self._archive()
            elif action=="rebase":
                self.perturbed=self.reference.clone()
                self._event("rebase",parameters=dict(self.perturbed.params))
                self._record(); self._archive()
            elif action=="pause":
                self.running=False
                if self.status!="failed":self.status="paused"
            elif action in ("resume","step"):
                if self.error:
                    raise ValueError("failed run must be replaced by a new run")
                if self.time>=self.horizon:
                    raise ValueError("extend the horizon before continuing")
                if action=="resume":self.running=True;self.status="running"
                else:
                    self.running=False;self.status="paused"
                    self.advance(min(self.time+FRAME_DT,self.horizon))
            elif action=="horizon":
                value=horizon_value(command.get("value"))
                if value<=self.time:
                    raise ValueError("new horizon must be after current time")
                self.horizon=value
            else:
                raise ValueError("unknown control action")
            self.sequence+=1
            self.checkpoint()
            return self.snapshot()
