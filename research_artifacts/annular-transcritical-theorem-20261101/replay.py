"""Replay discovery, reduction and independent verification in a fresh directory.

Only program sources are copied. No previous result is input to the new
determining solve. Four native nodes run serially under a shared time budget.
Requires Linux, Python 3.12+, and SymPy. Refuses to overwrite an output tree.
"""
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys

PACKAGE = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE / "support"))
from native_proof_run import run_node


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--prefix", default="replay")
    args = parser.parse_args()
    if not args.prefix or Path(args.prefix).name != args.prefix:
        parser.error("prefix must be one nonempty path component")
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "src").mkdir()
    (output / "results").mkdir()
    scripts = ["determine_shared_affine.py", "derive_invariants.py",
               "replay_reduction.py", "check_cartesian.py"]
    record = {
        "start_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "campaign": str(args.campaign.resolve()),
        "source_sha256": {}, "nodes": [],
        "discovery_inputs": "Original Cartesian PDE and declared coefficient/chart/parameter domains only.",
        "independent_checker_role": "Reconstruction targets, not discovery inputs.",
        "mathematical_proof": "See document/local-continuation.tex; successful execution is not its proof.",
        "success": False,
    }
    for name in scripts:
        shutil.copyfile(PACKAGE / "src" / name, output / "src" / name)
        record["source_sha256"][name] = sha(output / "src" / name)
    record["runner_sha256"] = sha(PACKAGE / "support/native_proof_run.py")
    try:
        for index, name in enumerate(scripts, 1):
            node_name = f"{args.prefix}-{index}-{Path(name).stem}"
            receipt = run_node(args.campaign, node_name,
                               [sys.executable, "-B", str(output / "src" / name)],
                               timeout=300, cwd=Path.cwd())
            record["nodes"].append({"name": node_name, "receipt": receipt})
            if receipt["returncode"] != 0 or receipt["exit_reason"] != "exited":
                raise RuntimeError(f"Replay stage {name} failed; preserved native receipt")
        record["results_sha256"] = {
            str(p.relative_to(output)): sha(p)
            for p in sorted((output / "results").glob("*.json"))
        }
        record["success"] = True
    finally:
        record["end_utc"] = datetime.now(timezone.utc).isoformat()
        with (output / "REPLAY.json").open("x") as stream:
            json.dump(record, stream, indent=2)
            stream.write("\n")
    print(json.dumps({"success": True, "output": str(output),
                      "nodes": [n["name"] for n in record["nodes"]]}))


if __name__ == "__main__":
    main()
