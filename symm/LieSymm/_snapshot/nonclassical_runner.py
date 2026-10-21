"""Frozen, sequential Stage 3 search; one bounded candidate process at a time."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from gatekeeper import check_gate
from run_all import run_command
from stage2_runner import source_hashes

HERE=Path(__file__).resolve().parent
FROZEN_REGISTRY_SHA256='2409ee048ab8ed66bdf4d0840a34a95b6ea380fdb72c2aedc29ce84382b3b764'


# 1. Both classification gates and the pre-evaluation selection must be current.
def load_registry():
    path=HERE/'nonclassical_candidates.json'
    if hashlib.sha256(path.read_bytes()).hexdigest()!=FROZEN_REGISTRY_SHA256:
        raise ValueError('The pre-evaluation candidate registry changed')
    registry=json.loads(path.read_text(encoding='utf-8'))
    candidates=registry['candidates']
    if (len(candidates)!=64 or [c['id'] for c in candidates]!=[f'C{i:02d}' for i in range(64)]
            or len({(c['c'],tuple(c['a']),tuple(c['b'])) for c in candidates})!=64):
        raise ValueError('Frozen candidates are incomplete or duplicated')
    gates={str(s):check_gate(s) for s in (1,2)}
    if not all(item['passed'] for item in gates.values()):
        raise ValueError(gates)
    if gates['2']['gate_sha256']!=registry['preceding_gate_sha256']:
        raise ValueError('Registry is not bound to the executed 2D classification')
    return registry,gates


# 2. A child prints the derivation in numbered, inspectable sections.
def evaluate(candidate_id,output):
    from nonclassical import analyze_candidate
    from nonclassical_equivalence import classical_distribution_equivalence
    from ml_adapter import build_certificate
    from main import json_ready
    registry,gates=load_registry()
    candidate=next((row for row in registry['candidates'] if row['id']==candidate_id),None)
    if candidate is None:
        raise ValueError('Candidate is not in the frozen registry')
    output=Path(output).resolve()
    if not output.is_relative_to(HERE) or output.exists():
        raise ValueError('Choose a new output directory inside this cycle')
    output.mkdir(parents=True)
    analysis=json_ready(analyze_candidate(candidate))
    equivalence=json_ready(classical_distribution_equivalence(candidate,require_gate=True))
    status=analysis['conditional_status']
    admitted=status in {'verified_conditional_on_declared_chart','verified_conditional_on_regular_subchart'}
    if not admitted and status!='failed_conditional_criterion':
        raise ValueError('Unexpected/unresolved candidate status; do not label as rejected')
    certificate=build_certificate(candidate,conditional_admitted=admitted,
        conditional_status=status,equivalence_status=equivalence['status'],
        conditional_evidence={'candidate_result':'candidate.json','registry_sha256':FROZEN_REGISTRY_SHA256,
                              'regular_chart_status':analysis.get('regular_chart_status'),
                              'singular_status':analysis.get('singular_status')})
    result={'candidate':candidate,'analysis':analysis,'classical_equivalence':equivalence,
            'prior_gates':gates,'registry_sha256':FROZEN_REGISTRY_SHA256,
            'mathematical_admission':admitted,
            'release_status':'requires_independent_review_and_project_validation'}
    result_text=json.dumps(result,indent=2,ensure_ascii=False)
    (output/'candidate.json').write_text(result_text,encoding='utf-8')
    certificate['certificate']['conditional_evidence']['candidate_sha256']=hashlib.sha256(
        (output/'candidate.json').read_bytes()).hexdigest()
    (output/'ml_certificate.json').write_text(json.dumps(certificate,indent=2,ensure_ascii=False),encoding='utf-8')
    print('1. Frozen model and distribution\n'+json.dumps(candidate,indent=2))
    print('2. Joint PDE, Q, differential consequences, conditional criterion\n'+json.dumps(analysis,indent=2,ensure_ascii=False))
    print('3. Classical distribution and solution-family comparison\n'+json.dumps(equivalence,indent=2,ensure_ascii=False))
    print('4. Invariant inputs, implicit profile equations, reconstruction and masks\n'+json.dumps(certificate,indent=2,ensure_ascii=False))
    print('5. Verdict: '+status+'; release requires independent current evidence')
    return 0


# 3. Aggregate execution success separately from mathematical acceptance.
def run(output):
    registry,gates=load_registry()
    output=Path(output).resolve()
    if not output.is_relative_to(HERE) or output==HERE or output.exists():
        raise ValueError('Choose a NEW output directory inside this cycle')
    output.mkdir(parents=True)
    before=source_hashes()
    receipts=[]
    statuses=Counter()
    equivalences=Counter()
    for candidate in registry['candidates']:
        name=candidate['id']
        command=[sys.executable,'-B',str(HERE/'nonclassical_runner.py'),
                 '--candidate',name,'--out',str(output/name)]
        receipt=run_command(command,output/f'{name}.log',timeout=120)
        receipt['candidate_id']=name
        for filename in ('candidate.json','ml_certificate.json'):
            path=output/name/filename
            receipt[filename+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if receipt['exit_code']==0:
            record=json.loads((output/name/'candidate.json').read_text(encoding='utf-8'))
            statuses[record['analysis']['conditional_status']]+=1
            equivalences[record['classical_equivalence']['status']]+=1
        receipts.append(receipt)
        print(name,receipt['process_status'],receipt['exit_code'],flush=True)
    after=source_hashes()
    current_gates={str(s):check_gate(s) for s in (1,2)}
    passed=(all(row['exit_code']==0 for row in receipts) and before==after and
            all(row['passed'] for row in current_gates.values()))
    result={'stage':'3','execution_passed':passed,'candidate_count':len(receipts),
            'registry_sha256':FROZEN_REGISTRY_SHA256,'preceding_gates':gates,
            'final_gates':current_gates,'sources_unchanged_during_run':before==after,
            'source_hashes_before':before,'source_hashes_after':after,
            'conditional_status_counts':dict(statuses),'classical_equivalence_counts':dict(equivalences),
            'receipts':receipts,'training_performed':False,
            'completeness_scope':'These64 frozen proposals only; no complete nonclassical classification',
            'release_status':'requires_independent_review_and_fresh_project_validation'}
    (output/'receipts.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return 0 if passed else 1


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate')
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    raise SystemExit(evaluate(args.candidate,args.out) if args.candidate else run(args.out))
