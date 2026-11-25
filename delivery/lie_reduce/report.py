from collections import Counter


def write_inventory(report,out):
    lines=['# Computed Lie reductions (no ML)','',
           'Generated from PDE pullbacks. `verified` means symbolic local identity, not certified numerical data or global chart admissibility.',
           'Finite polynomial discovery: degree 2 at m=1,2,3,4. All-real-m smooth claims belong to the separately frozen proofs.','']
    counts=Counter();wall=0
    for run in report['runs']:
        lines += [f"## {run['model']}, m={run['m']}",'',f"Discovery: {run['discovery']['status']}.",'']
        wall+=run['discovery']['wall_seconds']
        for item in run['reductions']:
            v=item['value'] or {};status=v.get('status',item['status']);counts[status]+=1
            wall+=item['wall_seconds']
            lines += [f"### {item['id']}",'',f"Generator: `{item['generator']}`",'',f"Status: **{status}**.",'']
            if v.get('reason') or item.get('reason'):lines += [v.get('reason') or item['reason'],'']
            if v.get('graph'):lines += [f"Graph: `{v['graph']['lifts']}`",'']
            for eq in v.get('equations',[]):lines += [f'```text\n{eq} = 0\n```','']
            for integral in v.get('first_integrals',[]):lines += [f"First integral: `{integral}`",'']
            if v.get('conditions'):lines += [f"Conditions: `{v['conditions']}`",'']
    lines += ['## Annular E2 manual rank-two section','',f"```text\n{report['E2']}\n```",'']
    (out/'ODE_INVENTORY.md').write_text('\n'.join(lines))
    (out/'SUMMARY.md').write_text('# Symbolic run summary\n\n'+
        f"Total run: {report['total_wall_seconds']:.3f} wall seconds; finite searches and catalogue reductions: {wall:.3f} seconds.\n\n"+
        '\n'.join(f'- {k}: {v}' for k,v in counts.items())+'\n\n'+
        'Every candidate has a status. Unsupported, chart-incompatible and timed-out cases are not passed reductions.\n')
