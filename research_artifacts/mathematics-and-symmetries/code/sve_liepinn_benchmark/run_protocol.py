#!/usr/bin/env python3
"""Print or execute sequential research runs; never run timing trials concurrently."""
import argparse
import shlex
import subprocess
import sys


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--execute',action='store_true')
    p.add_argument('--protocol',choices=['baseline','samples','weights','zero','extended'],default='baseline')
    args=p.parse_args();commands=[]
    common=['--seeds','0','1','2','--collocation','128','--steps','600']
    if args.protocol=='baseline':
        commands=[['--task','suite','--cases','all','--methods','vanilla','lie','reweighted',*common,'--out','results/suite_pilot'],
                  ['--task','family','--architectures','mlp','modified','deeponet','--methods','vanilla','lie','reweighted','cosine','conservation',
                   *common,'--out','results/family_pilot']]
    elif args.protocol=='samples':
        commands=[['--task','family','--methods','vanilla','lie','reweighted','--collocation',str(n),
                   '--seeds','0','1','2','--steps','2400','--out',f'results/samples_{n}'] for n in [32,128,512]]
    elif args.protocol=='weights':
        commands=[['--task','family','--methods','lie','reweighted','cosine','conservation','--sym-weight',str(w),
                   *common,'--out',f'results/weight_{w}'] for w in [.1,1.,10.]]
    elif args.protocol=='zero':
        commands=[['--task','suite','--cases','sve_m3','--methods','vanilla','lie','--generators','Tx','Ty','Tt',
                   *common,'--out','results/zero_generator']]
    else:
        commands=[['--task','family','--architectures','mlp','modified','deeponet','--methods','vanilla','lie','cosine','conservation',
                   '--seeds','0','1','2','3','4','--steps','6000','--collocation','512','--grids','24','36','48',
                   '--eval-grid','32','--out','results/extended_family']]
    for command in commands:
        invocation=[sys.executable,'benchmark.py',*command]
        print(shlex.join(invocation),flush=True)
        if args.execute:subprocess.run(invocation,check=True)


if __name__=='__main__':main()
