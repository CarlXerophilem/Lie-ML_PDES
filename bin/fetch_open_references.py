#!/usr/bin/env python3
"""Download linked, publicly readable copies to an ignored local directory.
No proxying or access-control bypass; no automatic public PDF redistribution.
"""
import argparse
import json
from pathlib import Path
from urllib.request import urlopen, Request

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/references")
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--key", action="append", help="Restrict to named bibliography key(s)")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    entries = json.loads((ROOT / "ref/doi_inventory.json").read_text())["entries"]
    failed = False
    for item in entries:
        if args.key and item["key"] not in args.key:
            continue
        url = item["open_read_pdf_url"]
        if not url or item["repository_file"]:
            print(f'{item["key"]}: existing local copy or link only')
            continue
        target = args.output / (item["title"] + ".pdf")
        if target.exists() and target.read_bytes().startswith(b"%PDF-"):
            print(f'{item["key"]}: already downloaded')
            continue
        try:
            req = Request(url, headers={"User-Agent": "Lie-ML-PDES bibliography reader/0.1"})
            with urlopen(req, timeout=args.timeout) as response:
                data = response.read()
            if not data.startswith(b"%PDF-") or b"%%EOF" not in data[-2048:]:
                raise ValueError("response is not a complete PDF")
            tmp = target.with_suffix(".pdf.part")
            tmp.write_bytes(data)
            tmp.replace(target)
            print(f'{item["key"]}: downloaded {len(data)} bytes')
        except (OSError, ValueError) as exc:
            failed = True
            print(f'{item["key"]}: unavailable: {exc}')
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
