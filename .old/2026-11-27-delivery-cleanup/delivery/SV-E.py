#!/usr/bin/env python3
"""Symbolic audits, references and classical invariant-profile solvers."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import argparse
from pathlib import Path
from sve_bench.record import RESULTS

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-only',action='store_true')
    parser.add_argument('--references',action='store_true')
    parser.add_argument('--classical',action='store_true')
    parser.add_argument('--out',type=Path,default=RESULTS)
    args=parser.parse_args()
    if args.audit_only:
        from sve_bench.audit import run
        run(args.out/'m0'/'audit')
    elif args.references:
        from sve_bench.reference import build
        build(args.out)
    elif args.classical:
        from sve_bench.classical import run
        run(args.out)
    else: parser.error('choose --audit-only, --references or --classical')

if __name__=='__main__': main()
