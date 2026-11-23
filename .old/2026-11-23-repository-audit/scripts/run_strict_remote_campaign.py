"""Serial native campaign, including the original baseline in the 7200 s cap."""
import argparse,json,time,sys,hashlib,re
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.run_strict_lie import cas_command,cleanup_linux,atomic_json,require_cleanup
from symm.LieSymm.strict import run_reduce,parse_liepde_output


def parse_terminal_result(name, stdout):
    """CRACK returns four lists; LIEPDE's public result returns three."""
    direct=name.startswith('direct-')
    result=parse_liepde_output(stdout,_crack_frame=direct)
    if direct:result['inequalities']='returned_by_crack'
    return result


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();out=args.out.resolve();results=out/'campaign';results.mkdir(exist_ok=True)
    while not (out/'baseline.exit').exists():time.sleep(5)
    resource=(out/'baseline.resources').read_text();wall=re.search(r'Elapsed.*?\): ([0-9:.]+)',resource).group(1)
    elapsed=0
    for value in wall.split(':'):elapsed=elapsed*60+float(value)
    code=int((out/'baseline.exit').read_text());spent=elapsed
    baseline=dict(name='baseline',status='timeout' if code==124 else 'unparsed' if code==0 else 'error',returncode=code,elapsed_seconds=elapsed,
                  timeout_seconds=1800,memory_bytes=1_800_000_000,input_sha256=hashlib.sha256((out/'baseline.red').read_bytes()).hexdigest(),
                  timing_scope='CAS command including timeout/prlimit; excludes transfer and derivation',
                  stdout=(out/'baseline.stdout').read_text(errors='replace'),stderr=(out/'baseline.stderr').read_text(errors='replace'),
                  peak_rss_kib=int(re.search(r'Maximum resident set size \(kbytes\): (\d+)',resource).group(1)))
    atomic_json(results/'baseline.json',baseline)
    jobs=[('official-liepde',60),('official-applysym',60),('direct-classify',1800),('fixed-positive',1800),('direct-generic',1800)]
    rows=[{k:v for k,v in baseline.items() if k not in ['stdout','stderr']}]
    for name,requested in jobs:
        receipt_path=results/(name+'.json')
        active=results/(name+'.running.json')
        if active.exists():raise RuntimeError('Interrupted job or unconfirmed cleanup needs explicit accounting; refusing automatic restart')
        if receipt_path.exists():
            receipt=json.loads(receipt_path.read_text());require_cleanup(receipt.get('linux_cleanup',{}));spent+=receipt['elapsed_seconds'];rows.append({k:v for k,v in receipt.items() if k not in ['stdout','stderr']});continue
        remaining=7200-spent-1
        if remaining<=.1:break
        if name.startswith('official-'):
            package=name.removeprefix('official-');source=out/'runtime/usr/share/reduce/packages/crack'/(package+'.tst');script='load_package crack,liepde,applysym$\n'+source.read_text()+'\nquit$\n'
        else:script=(out/'inputs'/(name+'.red')).read_text()
        pid=results/(name+'.pid');limit=min(requested,remaining)
        atomic_json(active,{'budget_before_seconds':spent,'allowed_seconds':limit,'input_sha256':hashlib.sha256(script.encode()).hexdigest()})
        try:receipt=run_reduce(cas_command(out,limit,pid,memory_bytes=8_000_000_000),script,timeout=limit,memory_bytes=8_000_000_000,artifact_prefix=results/name)
        finally:cleanup=cleanup_linux(pid)
        receipt.update(name=name,linux_cleanup=cleanup,timing_scope='CAS command including timeout/prlimit; excludes transfer and derivation')
        if receipt['status']=='unparsed' and not name.startswith('official-'):
            try:receipt['terminal_parser']=parse_terminal_result(name,receipt['stdout']);receipt['status']='returned-solved' if receipt['terminal_parser']['solved'] else 'returned-partial'
            except ValueError as exc:receipt['parse_error']=str(exc)
        from symm.LieSymm.core import json_ready
        atomic_json(receipt_path,json_ready(receipt));require_cleanup(cleanup);active.unlink();spent+=receipt['elapsed_seconds'];rows.append({k:v for k,v in receipt.items() if k not in ['stdout','stderr','terminal_parser']})
        atomic_json(results/'summary.json',{'budget_seconds':7200,'charged_seconds':spent,'jobs':rows,'strict_pass':False,'status':'running'})
        print(name,receipt['status'],spent,flush=True)
    atomic_json(results/'summary.json',{'budget_seconds':7200,'charged_seconds':spent,'jobs':rows,'strict_pass':False,'status':'finished'})

if __name__=='__main__':main()
