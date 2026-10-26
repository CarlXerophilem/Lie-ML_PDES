"""Review counterexamples; expected to fail on reviewed commit 57fcc19.

These tests assert the required behavior, not the observed defect. They live
outside the active regression directories so the frozen 346-test result keeps
its original scope. No REDUCE/SSH subprocess is launched by these tests.
"""
import subprocess

import sympy as sp

from scripts import run_strict_lie as runner
from symm.LieSymm import strict
from symm.LieSymm.core import JetSpace


def test_direct_crack_guard_is_not_lost_without_callback(monkeypatch):
    t, x, u, m = sp.symbols("t x u m")
    j = JetSpace((t, x), (u,))
    row = "{{},{xi_t=c_1,xi_x=0,eta_u=0},{c_1},{m-1}}"
    stdout = "LIESYMM_RESULT_BEGIN$\n{" + row + "}$\nLIESYMM_END$"
    monkeypatch.setattr(strict, "run_reduce", lambda *a, **k: {"status": "unparsed", "stdout": stdout})
    report = strict.analyze_strict(j.x, j.u, (j.jet(0, (1, 0)),), (m,), {},
                                   cas_command=["fixture"], cas_mode="crack")
    assert report["cas_solution"]["branches"][0]["nonzero_conditions"] == [m - 1]
    assert report["branch_correspondence"]["matched"] is False
    check = report["independent_checks"][0]
    retained = any(g.get("condition") == sp.Ne(m - 1, 0) for g in check.get("guard_checks", []))
    # Either preserve the authoritative direct-CRACK inequality, or fail closed.
    assert retained or not check.get("verified", False)


def test_cleanup_probe_error_is_not_confirmed_termination(monkeypatch, tmp_path):
    pidfile = tmp_path / "fixture.pid"
    pidfile.write_text("12345", encoding="ascii")
    monkeypatch.setattr(runner.subprocess, "run", lambda *a, **k:
                        subprocess.CompletedProcess(a[0], 2, "", "kill: permission denied"))
    receipt = runner.cleanup_linux(pidfile)
    assert receipt["status"] not in ("terminated", "no-linux-process-started")


def test_fast_exit_output_overflow_is_not_silently_truncated(monkeypatch):
    class FinishedProcess:
        returncode = 0

        def __init__(self, command, *, stdin, stdout, stderr, shell):
            stdout.write(b"x" * 8_000_001)
            stdout.flush()

        def poll(self):
            return self.returncode

        def wait(self):
            return self.returncode

    monkeypatch.setattr(strict.subprocess, "Popen", FinishedProcess)
    receipt = strict.run_reduce(["fixture-no-process"], "")
    assert receipt["status"] == "output-limit"


def test_returned_function_dependency_is_preserved_or_blocked(monkeypatch):
    t, x, u = sp.symbols("t x u")
    j = JetSpace((t, x), (u,))
    row = "{{},{xi_t=0,xi_x=0,eta_u=c_1},{c_1},{}}"
    stdout = ("depend c_1,x$\nSTRICT_CRACK_BRANCH_BEGIN$\n" + row +
              "$\nSTRICT_CRACK_BRANCH_END$\nLIESYMM_RESULT_BEGIN$\n{" + row + "}$\nLIESYMM_END$")
    monkeypatch.setattr(strict, "run_reduce", lambda *a, **k: {"status": "unparsed", "stdout": stdout})
    report = strict.analyze_strict(j.x, j.u, (j.jet(0, (1, 0)),), (), {},
                                   cas_command=["fixture"], cas_mode="crack")
    field_component = report["cas_solution"]["branches"][0]["assignments"][sp.Symbol("eta_u")]
    # The constant vector is valid, but it is not the entire returned c_1(x) family.
    assert field_component.has(sp.Function("c_1")(x)) or not report.get("returned_family_verified", False)


def test_algebraic_profile_constraint_is_not_labelled_ode():
    from scripts.strict_scalar_source_chains import derive_affine_characteristics
    t, x, u = sp.symbols("t x u")
    j = JetSpace((t, x), (u,))
    chain = derive_affine_characteristics(j, j.jet(0, (1, 0)) + u, (1, 0, 0))
    assert not chain["reduced_equation"].has(sp.Derivative)
    assert chain["category"] == "constant_constraints"
