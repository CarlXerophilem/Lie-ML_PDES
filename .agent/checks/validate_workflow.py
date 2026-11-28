#!/usr/bin/env python3
"""Check the Cartan-DEC-MiAE research workflow and its policy gates.

The checker loads the case contract, confirms the protocol and the workflow
name the same stages, and runs the promotion rules on fixed numeric cases.
It does not train a model.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENT = ROOT / ".agent"
CASE = AGENT / "cases" / "health-cartan-dec-miae"
sys.path.insert(0, str(AGENT))

from policy import (  # noqa: E402
    ablation_status,
    admit_claim,
    authorize_training,
    promote,
    unbacked_numbers,
)


class Failures(list):
    def check(self, condition: bool, message: str) -> None:
        if not condition:
            self.append(message)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check_documents(failed: Failures) -> dict:
    contract_path = CASE / "contract.json"
    contract = load_json(contract_path)
    schema = load_json(AGENT / "ledger" / "schema.json")
    template = load_json(AGENT / "ledger" / "run-template.json")
    protocol = (CASE / "PROTOCOL.md").read_text(encoding="utf-8")
    workflow = (AGENT / "WORKFLOW.md").read_text(encoding="utf-8")
    readme = (AGENT / "README.md").read_text(encoding="utf-8")

    failed.check(contract["case_id"] == "health_cartan_dec_miae", "case id")
    failed.check(
        contract["source_page"].endswith("Health%20(Cartan-DEC-MiAE)"),
        "source page fragment",
    )
    digest = hashlib.sha256(contract_path.read_bytes()).hexdigest()
    failed.check(len(digest) == 64, "contract hash")

    stage_ids = [item["id"] for item in contract["stages"]]
    failed.check(stage_ids == schema["stage_enum"], "stage order")
    for stage_id in stage_ids:
        failed.check(stage_id in protocol, f"protocol names {stage_id}")
        failed.check(stage_id in workflow, f"workflow names {stage_id}")
        failed.check(stage_id in template["stages"], f"template has {stage_id}")

    for key in schema["required"]:
        failed.check(key in template, f"template key {key}")
    failed.check(template["case_id"] == contract["case_id"], "template case")
    failed.check(template["tier"] in schema["tier_enum"], "template tier")
    failed.check(
        template["compute_authorization"] in schema["authorization_enum"],
        "template authorization",
    )

    pdf = next(item for item in contract["sources"] if item["id"] == "gallery-pdf")
    failed.check(
        pdf["sha256"] == "f172a003aec8f1b75c4a1ae5599c1598acf6a7b2cceab8396cfb5659c8b81418",
        "gallery pdf sha256",
    )
    failed.check(pdf["pages"] == 11, "gallery page count")

    table1 = {row["condition"]: row for row in contract["quoted_table1"]}
    failed.check(table1["vanilla_mae"]["ted_acc"] == 56.91, "vanilla TED accuracy")
    failed.check(table1["cartan_dec"]["cath_f1"] == 34.94, "DEC CATH F1")
    failed.check(table1["holonomy_masking"]["ted_f1"] == 30.13, "holonomy TED F1")
    failed.check(table1["miae_b_probe"]["cath_acc"] == 86.09, "MiAE-B probe CATH")
    deltas = {row["condition"]: row for row in contract["quoted_deltas_versus_vanilla"]}
    failed.check(deltas["cartan_dec"]["cath_f1"] == 11.03, "printed CATH F1 delta")
    failed.check(
        round(table1["cartan_dec"]["cath_f1"] - table1["vanilla_mae"]["cath_f1"], 2) == 11.04,
        "cell difference stays 11.04",
    )

    decoder = {row["path"]: row for row in contract["quoted_table5_decoder"]}
    failed.check(decoder["mst"]["rmsd_angstrom"] == 2.61, "MST RMSD")
    failed.check(decoder["mst"]["cath_acc"] == 41.95, "MST transfer")
    failed.check(decoder["k_shortest"]["rmsd_angstrom"] == 3.82, "K-shortest RMSD")
    failed.check(decoder["k_shortest"]["cath_acc"] == 46.40, "K-shortest transfer")

    attention = {row["bias"]: row for row in contract["quoted_table3_attention"]}
    failed.check(attention["none"]["entropy"] == 3.61, "no-bias entropy")
    failed.check(attention["combined"]["entropy"] == 3.04, "combined entropy")
    failed.check(attention["curvature_only"]["delta_cath_acc"] == -2.15, "curvature-only CATH")

    locked = {item["id"] for item in contract["locked_readings"]}
    failed.check(locked == {"N1", "N2", "N3", "N4", "N5"}, "locked readings")
    open_ids = {item["id"] for item in contract["open_readings"]}
    failed.check({"O1", "O2", "O3", "O4"} <= open_ids, "open readings")

    for needle in (
        "reconstruction.integrated_position_rmse",
        "macro_f1",
        "N5",
        "O1",
        "draft/dissertation_wku.tex",
        "probe.accuracy",
    ):
        failed.check(needle in protocol, f"protocol contains {needle}")
    for path in contract["firewall"]["dissertation_paths"]:
        failed.check(path in json.dumps(contract), f"firewall lists {path}")
    failed.check("build/cartan-dec-miae" in readme, "readme output root")
    failed.check(contract["tiers"]["smoke"]["primary_metric"].endswith("integrated_position_rmse"), "smoke primary")
    failed.check("probe.accuracy" in contract["tiers"]["smoke"]["forbidden_primary"], "probe forbidden")
    failed.check(contract["smoke_budget"]["min_relative_gain"] == 0.05, "promotion gain")
    failed.check(contract["smoke_budget"]["ablation_clean_fraction"] == 0.75, "ablation fraction")
    failed.check(len(contract["ablations"]) == 4, "four smoke ablations")
    failed.check({item["id"] for item in contract["ideas"]} == {"I1", "I2", "I3"}, "seed ideas")
    return contract


def check_policy(failed: Failures, contract: dict) -> None:
    budget = contract["smoke_budget"]
    smoke = contract["tiers"]["smoke"]
    common = dict(
        primary_metric=smoke["primary_metric"],
        direction=smoke["primary_direction"],
        min_relative_gain=budget["min_relative_gain"],
        forbidden_primary=smoke["forbidden_primary"],
    )
    one_seed = promote(
        smoke["primary_metric"],
        [{"seed": 0, "baseline": 1.00, "candidate": 0.80}],
        **common,
    )
    failed.check(one_seed["reason"] == "need_two_seeds", "one seed rejects")

    promoted = promote(
        smoke["primary_metric"],
        [
            {"seed": 0, "baseline": 1.00, "candidate": 0.90},
            {"seed": 1, "baseline": 1.20, "candidate": 1.10},
        ],
        **common,
    )
    failed.check(promoted["status"] == "promote", "agreeing seeds promote")

    split = promote(
        smoke["primary_metric"],
        [
            {"seed": 0, "baseline": 1.00, "candidate": 0.90},
            {"seed": 1, "baseline": 1.20, "candidate": 1.20},
        ],
        **common,
    )
    failed.check(split["status"] == "reject", "flat seed rejects")

    probe = promote("probe.accuracy", [{"seed": 0, "baseline": 0.5, "candidate": 0.9}], **common)
    failed.check(probe["reason"] == "forbidden_primary", "probe cannot promote")

    paper = authorize_training("paper", "smoke-only")
    failed.check(paper["status"] == "reject", "paper tier blocked by default")
    quote = authorize_training("quote", "smoke-only")
    failed.check(quote["reason"] == "quote_tier_does_not_train", "quote tier does not train")
    allowed = authorize_training("smoke", "smoke-only")
    failed.check(allowed["status"] == "allow", "smoke training allowed")

    clean = ablation_status(
        [0.04, 0.05, 0.03, 0.01],
        min_gain=budget["ablation_min_gain"],
        clean_fraction=budget["ablation_clean_fraction"],
    )
    failed.check(clean["status"] == "clean" and clean["helping"] == 3, "three of four is clean")
    partial = ablation_status(
        [0.04, 0.00, 0.00, 0.02],
        min_gain=budget["ablation_min_gain"],
        clean_fraction=budget["ablation_clean_fraction"],
    )
    failed.check(partial["status"] == "partial", "one drop is partial")

    observations = [
        {
            "id": "q-dec-cath-f1",
            "tier": "quote",
            "metric": "macro_f1",
            "value": 34.94,
            "unit": "percent",
            "source": "gallery table 1",
            "command": "",
            "seed": None,
        },
        {
            "id": "s-rmse-0",
            "tier": "smoke",
            "metric": smoke["primary_metric"],
            "value": 0.90,
            "unit": "angstrom",
            "source": "metrics.json",
            "command": "cartan_dec.train",
            "seed": 0,
        },
    ]
    open_ids = {item["id"] for item in contract["open_readings"]}
    empty = admit_claim(
        {
            "id": "c-empty",
            "kind": "measurement",
            "tier": "smoke",
            "statement": "The model improved.",
            "observation_ids": [],
        },
        observations,
        open_reading_ids=open_ids,
    )
    failed.check(empty["reason"] == "missing_observation", "claim needs an observation")
    leaked = admit_claim(
        {
            "id": "c-leak",
            "kind": "measurement",
            "tier": "smoke",
            "statement": "The smoke run reached the paper's CATH F1.",
            "observation_ids": ["q-dec-cath-f1"],
        },
        observations,
        open_reading_ids=open_ids,
    )
    failed.check(leaked["reason"] == "tier_mismatch", "smoke cannot measure a quote")
    quoted = admit_claim(
        {
            "id": "c-quote",
            "kind": "quotation",
            "tier": "quote",
            "statement": "Table 1 prints CATH macro F1 34.94 for the DEC objective.",
            "observation_ids": ["q-dec-cath-f1"],
        },
        observations,
        open_reading_ids=open_ids,
    )
    failed.check(quoted["status"] == "admit", "quotation admitted")
    collapse = admit_claim(
        {
            "id": "c-entropy",
            "kind": "mechanism",
            "tier": "smoke",
            "statement": "Combined attention prevents collapse.",
            "requires_open_reading": "O1",
            "observation_ids": ["s-rmse-0"],
        },
        observations,
        open_reading_ids=open_ids,
    )
    failed.check(collapse["reason"] == "open_reading_unresolved", "entropy claim blocked")
    bare = unbacked_numbers(
        "The encoder reached 34.94 macro F1 and a private 12.34 score.",
        observations,
    )
    failed.check(bare == ["12.34"], f"unbacked number filter, got {bare}")


def main() -> int:
    failed = Failures()
    contract = check_documents(failed)
    check_policy(failed, contract)
    if failed:
        print(f"workflow check failed ({len(failed)})")
        for item in failed:
            print(f"  - {item}")
        return 1
    print("workflow check passed")
    print(f"case {contract['case_id']}")
    print(f"stages {', '.join(item['id'] for item in contract['stages'])}")
    print(f"smoke primary {contract['tiers']['smoke']['primary_metric']}")
    print(f"paper primary {contract['tiers']['paper']['primary_metric']}")
    print(f"locked readings {', '.join(item['id'] for item in contract['locked_readings'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
