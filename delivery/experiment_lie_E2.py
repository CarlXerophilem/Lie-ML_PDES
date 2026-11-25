#!/usr/bin/env python3
"""Rotating exchange and the separate annular E2 quotient, with a written verifier.

The exchange swirl is an exact five-balance family. The annular record is a
selected rank-2 subalgebra on the four-balance polar chart, not a discovered
planar basis and not an X_i/Y_i label.
"""
import json


def written_verifier(reduction_record, exchange):
    reasons = []
    verdict = (reduction_record.get("verification") or {}).get("status")
    if reduction_record.get("status") != "computed" or verdict != "verified_local_identities":
        reasons.append({"id": "E2_rank2", "status": reduction_record.get("status"), "verifier": verdict})
    residuals = exchange.get("swirl_residuals", [])
    if residuals != ["0", "0", "0", "0", "0"]:
        reasons.append({"id": "exchange_swirl", "residuals": residuals})
    if exchange.get("swirl_r_Qr") != "1/20":
        reasons.append("exchange throughput")
    scope = (reduction_record.get("solver_output") or {}).get("scope", "")
    if "optimal system not computed" not in scope:
        reasons.append("E2 scope was presented as a complete optimal system")
    return {
        "status": "passed" if not reasons else "failed",
        "reasons": reasons,
        "checker": "delivery/independent_verifier.py through lie_pde_reducer.verifier; exchange residuals from symbolic_new_model2026",
    }


def main():
    from lie_pde_reducer import reduction
    from symbolic_new_model2026 import run as exchange_run

    exchange = exchange_run()
    annular = reduction("E2", 3, None)
    verdict = written_verifier(annular, exchange)
    report = {
        "models": ["E_exch", "E2"],
        "search_class": "Exact substitution on the exchange swirl, and one declared rank-2 annular subalgebra. No unrestricted planar point classification.",
        "exchange_chart": "r>0 and the selected swirl family V=0, W=Omega*r, D_a=0",
        "annular_chart": "r>0, h>0, g,K,G>0",
        "exchange": exchange,
        "annular_reduction": annular,
        "written_verifier": verdict,
        "not_claimed": "E2 and the rotating-exchange tank are different balance systems.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if verdict["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
