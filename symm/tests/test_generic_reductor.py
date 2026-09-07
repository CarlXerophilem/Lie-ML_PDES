from symm.generic import (
    PDEsReductor,
    ReductionCertificate,
    heat_2plus1,
)


def test_reductor_is_deterministic_and_scores_do_not_certify():
    system = heat_2plus1().system
    reductor = PDEsReductor()
    first = reductor.rank(system)
    second = reductor.rank(system)
    assert first.as_dict() == second.as_dict()
    assert first.status == "unsupported"
    assert all(candidate.invariant for candidate in first.candidates)


def test_reductor_preserves_backend_unavailable_evidence():
    system = heat_2plus1().system
    certificate = ReductionCertificate(
        system.fingerprint(), "backend-unavailable", "branch-0",
        checks=(("oracle", False),),
    )
    record = PDEsReductor().rank(system, certificate=certificate)
    assert record.status == "backend-unavailable"
    assert dict(record.evidence)["certificate_upgrade_by_score"] == "forbidden"
