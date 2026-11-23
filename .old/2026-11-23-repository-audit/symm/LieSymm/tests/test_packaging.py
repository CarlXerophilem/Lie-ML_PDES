"""Behavioral packaging checks; historical regression tests are separate."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import sympy as sp

from symm.LieSymm import JetSpace, analyze, verify_generator
from symm.LieSymm._loader import PACKAGE_ROOT, snapshot_path
from symm.LieSymm.provenance import check_historical_gate, verify_adapter, verify_snapshot


def _run(code, cwd, pythonpath):
    env = dict(os.environ, PYTHONPATH=str(pythonpath), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-B", "-c", code], cwd=cwd, env=env,
                          text=True, capture_output=True, timeout=45)


def test_complete_frozen_snapshot_and_adapter_hashes():
    result = verify_snapshot()
    assert result["passed"], result
    assert result["file_count"] == 398
    assert verify_adapter()["passed"]


@pytest.mark.parametrize("stage", [1, 2, 3])
def test_historical_gates_keep_their_exact_hashes(stage):
    result = check_historical_gate(stage)
    assert result["passed"], result
    assert result["evidence_kind"] == "frozen_historical_gate"


def test_unknown_model_keeps_determining_equations_and_unresolved_status():
    t, x, u = sp.symbols("t x u", real=True)
    jets = JetSpace((t, x), (u,))
    equations = (jets.jet(0, (1, 0)) - jets.jet(0, (0, 1)),)
    report = analyze((t, x), (u,), equations, (), {"model_id": "unknown_transport"})
    assert report["classification_status"] == "unresolved"
    assert report["determining_equations"]
    assert "basis" not in report["integration"]
    assert verify_generator(jets, equations, (0, 1), (0,))["verified"]


def test_matching_model_name_does_not_authorize_wrong_equations():
    t, x, u = sp.symbols("t x u", real=True)
    jets = JetSpace((t, x), (u,))
    report = analyze((t, x), (u,), (jets.jet(0, (1, 0)),), (), {"model_id": "grass_cubic"})
    assert report["classification_status"] == "unresolved"
    assert "fingerprint" in report["integration"]["reason"]


def test_existing_main_and_models_survive_and_legacy_symm_coexists(tmp_path):
    root = PACKAGE_ROOT.parents[1]
    result = _run('''
import builtins, sys, types
from concurrent.futures import ThreadPoolExecutor
sentinels = {name: types.ModuleType(name) for name in ("main", "models", "classification", "reductions")}
sys.modules.update(sentinels)
paths, finders, importer = list(sys.path), list(sys.meta_path), builtins.__import__
from symm.sym_engine import Engine, PDE
from symm.LieSymm import JetSpace, branch_model
from symm.LieSymm._loader import load_module
with ThreadPoolExecutor(max_workers=4) as pool:
    modules = list(pool.map(load_module, ["models"] * 8))
assert all(module is modules[0] for module in modules)
assert list(sys.path) == paths and list(sys.meta_path) == finders
assert builtins.__import__ is importer
assert all(sys.modules[name] is value for name, value in sentinels.items())
assert JetSpace.__module__.startswith("symm.LieSymm._runtime.")
assert branch_model("grass_cubic")["branch_conditions"]["model_id"] == "grass_cubic"
''', tmp_path, root)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.fixture(scope="module")
def relocated(tmp_path_factory):
    root = tmp_path_factory.mktemp("liesymm-relocated")
    shutil.copytree(PACKAGE_ROOT, root / "LieSymm",
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "scalar2026"))
    return root


def test_relocated_standalone_package_has_no_build_dependency(relocated):
    result = _run('''
from pathlib import Path
import sys
import LieSymm
from LieSymm.provenance import verify_snapshot, check_historical_gate
root = Path.cwd() / "LieSymm"
assert Path(LieSymm.__file__).resolve().is_relative_to(root)
assert verify_snapshot()["passed"]
assert all(check_historical_gate(stage)["passed"] for stage in (1, 2, 3))
assert all(Path(module.__file__).resolve().is_relative_to(root)
           for name, module in sys.modules.items()
           if name.startswith("LieSymm._runtime.") and getattr(module, "__file__", None))
assert "main" not in sys.modules and "models" not in sys.modules
''', relocated, relocated)
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_refuses_snapshot_output_before_analysis(relocated):
    env = dict(os.environ, PYTHONPATH=str(relocated), PYTHONDONTWRITEBYTECODE="1")
    destination = relocated / "LieSymm" / "_snapshot" / "forbidden-new-output"
    result = subprocess.run([sys.executable, "-B", "-m", "LieSymm", "--out", str(destination)],
                            cwd=relocated, env=env, capture_output=True, text=True, timeout=20)
    assert result.returncode == 2
    assert "outside" in result.stderr and not destination.exists()


def test_modified_copied_source_is_rejected_before_execution(relocated):
    path = relocated / "LieSymm" / "_snapshot" / "main.py"
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"\nraise AssertionError('must never execute')\n")
        result = _run("import LieSymm", relocated, relocated)
        assert result.returncode != 0
        assert "Frozen source hash mismatch: main.py" in result.stderr
        assert "AssertionError: must never execute" not in result.stderr
    finally:
        path.write_bytes(original)


def test_changed_proof_revokes_historical_gate_and_necessity_review(relocated):
    path = relocated / "LieSymm" / "_snapshot" / "FIRST_ORDER_DERIVATION.md"
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"\nchanged proof\n")
        result = _run('''
from LieSymm.provenance import check_historical_gate, verify_snapshot
from LieSymm._loader import load_module
assert not verify_snapshot()["passed"]
assert not check_historical_gate(1)["passed"]
assert not load_module("classification").review_gate()["passed"]
''', relocated, relocated)
        assert result.returncode == 0, result.stdout + result.stderr
    finally:
        path.write_bytes(original)


def test_separator_normalization_never_accepts_missing_or_changed_evidence(tmp_path):
    from symm.LieSymm._loader import _check_hashes
    (tmp_path / "nested").mkdir()
    item = tmp_path / "nested" / "evidence.txt"
    item.write_bytes(b"pinned")
    hashes = {"nested\\evidence.txt": hashlib.sha256(b"pinned").hexdigest()}
    assert _check_hashes(hashes, root=tmp_path) == []
    item.write_bytes(b"changed")
    assert _check_hashes(hashes, root=tmp_path) == list(hashes)
    item.unlink()
    assert _check_hashes(hashes, root=tmp_path) == list(hashes)
    assert _check_hashes({"../outside": "0"}, root=tmp_path) == ["../outside"]


@pytest.mark.parametrize("name", ["../outside", "a/../../outside", "C:/outside", "/outside"])
def test_snapshot_paths_cannot_escape(name):
    with pytest.raises(ValueError):
        snapshot_path(name)
