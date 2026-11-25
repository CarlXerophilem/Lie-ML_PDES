#!/usr/bin/env python3
"""Regression, independent certification, resource summaries and figures."""
import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import argparse
from pathlib import Path
from sve_bench.record import RESULTS

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--regression',action='store_true')
    parser.add_argument('--evaluate',action='store_true')
    parser.add_argument('--report',action='store_true')
    parser.add_argument('--out',type=Path,default=RESULTS)
    args=parser.parse_args()
    if args.regression:
        from sve_bench.regression import run
        run(args.out/'m0')
    if args.evaluate:
        from sve_bench.evaluate import run
        run(args.out)
    if args.report:
        from sve_bench.reporting import run
        run(args.out)
    if not any((args.regression,args.evaluate,args.report)): parser.error('choose an action')

if __name__=='__main__': main()
