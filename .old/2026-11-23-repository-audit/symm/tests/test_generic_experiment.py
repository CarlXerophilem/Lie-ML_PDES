import json

import pytest

from symm.generic import (
    CloudRunConfig,
    EXPERIMENT_FEATURE_SCHEMA,
    build_manifest,
    evaluate_tree_model,
    fit_tree_model,
    generate_oracle_records,
    heat_2plus1,
    cauchy_riemann,
    rank_dropping_rotation,
    run_pilot,
)


def _pilot_cases():
    return (heat_2plus1(), cauchy_riemann(), rank_dropping_rotation())


def test_manifest_preserves_structural_provenance_and_shape():
    entries = build_manifest(_pilot_cases())
    assert [entry.case_id for entry in entries] == [
        "heat-2plus1", "cauchy-riemann", "rank-dropping-rotation"
    ]
    assert entries[0].p == 3 and entries[0].q == 1 and entries[0].r == 1
    assert entries[0].structural_only
    assert "not-provided" in entries[0].boundary_initial_provenance
    assert entries[0].as_dict()["system_fingerprint"] == entries[0].system_fingerprint


def test_cloud_config_rejects_overcommitted_cpu_budget():
    with pytest.raises(ValueError):
        CloudRunConfig(vcpus=4, ml_vcpus=3, reserved_vcpus=2)
    with pytest.raises(ValueError):
        CloudRunConfig(reserved_vcpus=-1)


def test_oracle_records_are_group_split_and_status_preserving():
    records = generate_oracle_records(
        _pilot_cases(),
        held_out_case_ids=("cauchy-riemann",),
    )
    assert records
    assert all(record.split in {"train", "held-out"} for record in records)
    assert all(record.verified == (record.status == "verified") for record in records)
    assert any(record.status == "verified" for record in records)
    assert all(tuple(name for name, _ in record.features) == EXPERIMENT_FEATURE_SCHEMA
               for record in records)
    assert all(record.case_id == "cauchy-riemann" for record in records
               if record.split == "held-out")


def test_tree_model_ranks_without_mutating_exact_statuses():
    records = generate_oracle_records(
        _pilot_cases(),
        held_out_case_ids=("cauchy-riemann",),
    )
    before = tuple((record.candidate_id, record.status) for record in records)
    model = fit_tree_model(records, max_depth=2, min_leaf=1)
    result = evaluate_tree_model(model, records, abstain_threshold=0.5)
    after = tuple((record.candidate_id, record.status) for record in records)
    assert before == after
    assert result["certificate_status_mutation"] is False
    assert result["n_records"] > 0
    assert result["predictions"]


def test_run_pilot_writes_reproducible_artifact_set(tmp_path):
    result = run_pilot(
        tmp_path / "pilot",
        cases=_pilot_cases(),
        held_out_case_ids=("cauchy-riemann",),
        max_depth=2,
        min_leaf=1,
    )
    output = tmp_path / "pilot"
    expected = {
        "corpus_manifest.jsonl",
        "oracle_records.jsonl",
        "model.json",
        "evaluation.json",
        "run_metadata.json",
        "REPORT.md",
    }
    assert expected == {path.name for path in output.iterdir()}
    metadata = json.loads((output / "run_metadata.json").read_text(encoding="utf-8"))
    assert metadata["model_fingerprint"] == result["model"]["model_fingerprint"]
    assert metadata["oracle_record_count"] > 0
    assert set(metadata["backend_preflight"]) == {"maple", "reduce"}
