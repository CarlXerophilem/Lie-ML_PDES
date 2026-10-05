"""Behavioral checks for a persistent pair and parameter-change boundaries."""
import json
from http.client import HTTPConnection
import threading

import numpy as np
import pytest

from symm.fluid_baselines.live_service import Simulation, make_server


def test_perturbation_keeps_current_field_and_changes_only_future(tmp_path):
    sim = Simulation(tmp_path, n=24, kind="shear", running=False)
    sim.advance(.2)
    before = sim.perturbed.state.copy()
    sim.control({"action":"perturb", "parameters":{"nu":.1}})
    assert sim.time == .2
    assert np.array_equal(before, sim.perturbed.state)
    assert sim.reference.params["nu"] == .01
    sim.advance(.4)
    assert sim.snapshot()["diagnostics"]["difference_l2"] > 0
    assert sim.events[-1]["time"] == .2


def test_checkpoint_recovers_fields_parameters_and_pause_state(tmp_path):
    sim = Simulation(tmp_path, n=24, running=False)
    sim.advance(.1)
    sim.control({"action":"perturb","parameters":{"nu":.02}})
    sim.advance(.2)
    sim.checkpoint()
    restored = Simulation(tmp_path)
    assert restored.run_id == sim.run_id
    assert restored.time == sim.time
    assert not restored.running
    assert restored.perturbed.params == sim.perturbed.params
    np.testing.assert_array_equal(restored.perturbed.state,sim.perturbed.state)
    restored.advance(.3)
    sim.advance(.3)
    np.testing.assert_array_equal(restored.reference.state,sim.reference.state)


def test_invalid_change_is_atomic_and_horizon_stops_run(tmp_path):
    sim = Simulation(tmp_path,n=24,horizon=.2)
    before = sim.perturbed.params.copy()
    with pytest.raises(ValueError):
        sim.control({"action":"perturb","parameters":{"nu":float("nan")}})
    assert sim.perturbed.params == before
    sim.advance(.2)
    assert not sim.running and sim.status == "horizon-reached"
    sim.control({"action":"horizon","value":1})
    sim.control({"action":"resume"})
    assert sim.running


def test_archives_survive_new_run_and_resume(tmp_path):
    sim=Simulation(tmp_path,n=24,running=False)
    sim.advance(.5)
    old=sim.run_id
    frame=sim.frame(0)
    assert frame["time"]==0
    sim.control({"action":"reset","model":"sve","n":128,"horizon":10})
    assert sim.run_id != old and sim.reference.model=="sve"
    assert (tmp_path/"runs"/old/"checkpoint.npz").exists()
    restored=Simulation(tmp_path)
    assert restored.run_id==sim.run_id


def test_http_controls_reject_cross_origin_and_apply_valid_action(tmp_path):
    sim=Simulation(tmp_path,n=24,running=False)
    server=make_server(sim,port=0)
    thread=threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        conn=HTTPConnection("127.0.0.1",server.server_port)
        body=json.dumps({"action":"perturb","parameters":{"nu":.03}})
        conn.request("POST","/api/control",body,{"Content-Type":"application/json"})
        response=conn.getresponse();response.read()
        assert response.status==403
        headers={"Content-Type":"application/json","X-LieML-Control":"1","Origin":"https://unrelated.invalid"}
        conn.request("POST","/api/control",body,headers)
        response=conn.getresponse();response.read()
        assert response.status==403
        headers.pop("Origin")
        conn.request("POST","/api/control",body,headers)
        response=conn.getresponse();result=json.loads(response.read())
        assert response.status==200
        assert result["parameters"]["perturbed"]["nu"]==.03
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
