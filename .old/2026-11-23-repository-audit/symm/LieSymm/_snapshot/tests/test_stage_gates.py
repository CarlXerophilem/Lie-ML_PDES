import json
import gatekeeper


def test_bare_passed_flag_does_not_unlock_a_stage(tmp_path,monkeypatch):
    monkeypatch.setattr(gatekeeper,'HERE',tmp_path)
    (tmp_path/'STAGE_1_GATE.json').write_text(json.dumps({'passed':True}))
    assert not gatekeeper.check_gate(1)['passed']
    assert not gatekeeper.check_gate(2)['passed']


def test_gate_invalidates_on_source_or_evidence_change(tmp_path,monkeypatch):
    monkeypatch.setattr(gatekeeper,'HERE',tmp_path)
    source=tmp_path/'source.py';source.write_text('old source')
    evidence=tmp_path/'receipt.json';evidence.write_text('verified receipt')
    gate={'passed':True,'inputs_sha256':{'source.py':gatekeeper.digest(source)},
          'evidence_sha256':{'receipt.json':gatekeeper.digest(evidence)}}
    (tmp_path/'STAGE_1_GATE.json').write_text(json.dumps(gate))
    source.write_text('different equation')
    result=gatekeeper.check_gate(1)
    assert not result['passed']
    assert 'source.py' in result['changed']
