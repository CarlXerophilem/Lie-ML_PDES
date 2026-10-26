"""Capture CRACK's documented branch callback without changing its solution.

The callback records remaining equations, assignments, free quantities, and
nonzero/or-inequalities before LIEPDE discards information in its final return.
Frames are raw evidence, not a verified mapping to LIEPDE's reordered branches.
"""
from pathlib import Path
import argparse
import hashlib
import re
import sys
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import model,cas_command,cleanup_linux,atomic_json
from symm.LieSymm.strict import liepde_script,run_reduce


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',default='P:general')
    parser.add_argument('--tier',type=int,choices=(60,300,1800),default=60)
    args=parser.parse_args()
    out=ROOT/'build/sve-strict-lie-20261026'
    script=liepde_script(**model(args.case))
    token=uuid.uuid4().hex
    pidfile=out/(token+'.pid')
    try:
        receipt=run_reduce(cas_command(out,args.tier,pidfile),script,timeout=args.tier,
                           artifact_prefix=out/(args.case.replace(':','--')+'-'+token+'.trace'))
    finally:
        cleanup=cleanup_linux(pidfile)
    receipt['linux_cleanup']=cleanup
    receipt['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    receipt['crack_branch_frames']=re.findall(r'STRICT_CRACK_BRANCH_BEGIN\$?(.*?)STRICT_CRACK_BRANCH_END',receipt['stdout'],re.S)
    receipt['scope']='Raw branch conditions captured; correspondence and completeness not certified'
    atomic_json(out/(args.case.replace(':','--')+f'-trace-{args.tier}.json'),receipt)
    print(args.case,receipt['status'],'raw branch frames',len(receipt['crack_branch_frames']))


if __name__=='__main__':
    main()
