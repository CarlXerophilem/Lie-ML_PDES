"""Standalone scientific plots, training GIF, and seed-preserving summaries."""
import csv
import io
import json
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def read_history(directory):
    with (Path(directory)/'history.csv').open() as f:
        rows=list(csv.DictReader(f))
    return {k:np.array([float(r[k]) for r in rows]) for k in rows[0]}


def primary_scores(run):
    return [v for k,v in run['test_metrics'].items() if k!='test_translated']


def relocate_directories(runs,out):
    for run in runs:
        relative=Path(run['group'])/run['architecture']/f"seed{run['seed']}"/run['method']
        local=out/relative
        if local.is_dir():run['directory']=str(local)


def render(out):
    out=Path(out).resolve();payload=json.loads((out/'results.json').read_text());runs=payload['runs']
    relocate_directories(runs,out)
    figures=out/'figures';figures.mkdir(exist_ok=True)
    grouped=defaultdict(list)
    for run in runs:
        key=(run['group'],run['architecture'],run['method'])
        grouped[key].append(run)
    summary=[]
    for (group,arch,method),items in grouped.items():
        errors=np.array([np.mean([s['evolution_relative_l2'] for s in primary_scores(r)]) for r in items])
        worst=np.array([max(s['max_active_field_evolution_error'] for s in primary_scores(r)) for r in items])
        times=np.array([r['train_seconds'] for r in items])
        summary.append({'group':group,'architecture':arch,'method':method,'seeds':[r['seed'] for r in items],
                        'parameters':items[0]['parameters'],'error_median':float(np.median(errors)),
                        'error_min':float(errors.min()),'error_max':float(errors.max()),
                        'max_field_error_median':float(np.median(worst)),
                        'train_seconds_median':float(np.median(times)),
                        'train_seconds_min':float(times.min()),'train_seconds_max':float(times.max()),
                        'matched_runs':sum(all(s['matched_accuracy'] for s in primary_scores(r)) for r in items),
                        'total_runs':len(items)})
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    plt.rcParams.update({'font.size':10,'figure.dpi':130,'axes.grid':True,'grid.alpha':.2})
    # All seeds remain visible; no best-seed plot masquerades as a typical result.
    fig,axes=plt.subplots(1,3,figsize=(13,3.8))
    methods=list(dict.fromkeys(r['method'] for r in runs));colors=dict(zip(methods,plt.cm.tab10.colors))
    for run in runs:
        h=read_history(run['directory']);label=f"{run['architecture']}/{run['method']}/s{run['seed']}"
        key='monitor_pde' if 'monitor_pde' in h else 'pde'
        axes[0].semilogy(h['step'][1:],h[key][1:],color=colors[run['method']],alpha=.5,label=label)
        axes[1].semilogy(h['train_seconds'],h['validation_evolution_error'],color=colors[run['method']],alpha=.5)
        axes[2].scatter(run['training_wall_seconds'],np.mean([s['evolution_relative_l2'] for s in primary_scores(run)]),
                        color=colors[run['method']],marker={'mlp':'o','modified':'s','deeponet':'^'}[run['architecture']],alpha=.7)
    measured=all('monitor_pde' in read_history(r['directory']) for r in runs)
    axes[0].set(xlabel='Optimization steps',ylabel='Normalized PDE MSE',
                title='Fixed independent points' if measured else 'Last-update PDE loss (cases cycle)')
    axes[1].set(xlabel='Optimizer compute time (s)',ylabel='Relative evolution L2',title='Held-out diagnostic')
    axes[2].set(xlabel='Training wall time incl. monitoring (s)',ylabel='Final relative evolution L2',title='Measured cost / accuracy',yscale='log')
    from matplotlib.lines import Line2D
    axes[0].legend(handles=[Line2D([0],[0],color=colors[m],label=m) for m in methods],fontsize=8)
    architectures=list(dict.fromkeys(r['architecture'] for r in runs))
    axes[2].legend(handles=[Line2D([0],[0],color='gray',marker={'mlp':'o','modified':'s','deeponet':'^'}[a],
                                  linestyle='',label=a) for a in architectures],fontsize=8)
    fig.suptitle('Fixed final checkpoint; every seed shown; conditional diagnostics do not select models',fontsize=10)
    fig.tight_layout();fig.savefig(figures/'learning_process.png');plt.close(fig)
    fig,ax=plt.subplots(figsize=(max(7,len(summary)*.65),4))
    x=np.arange(len(summary));med=np.array([s['error_median'] for s in summary])
    lo=med-np.array([s['error_min'] for s in summary]);hi=np.array([s['error_max'] for s in summary])-med
    ax.errorbar(x,med,yerr=[lo,hi],fmt='o',capsize=3,color='#15658b')
    ax.set(yscale='log',ylabel='Relative evolution L2: seed median and range',title='Architecture and loss comparison')
    ax.set_xticks(x,[f"{s['group']}\n{s['architecture']}\n{s['method']}" for s in summary],rotation=55,ha='right',fontsize=8)
    fig.tight_layout();fig.savefig(figures/'comparison.png');plt.close(fig)
    audit=json.loads((out/'symbolic.json').read_text())
    names=list(audit);fig,axes=plt.subplots(1,2,figsize=(10,4))
    axes[0].bar(names,[audit[n]['total_seconds'] for n in names],color='#377d83')
    axes[0].set(ylabel='Seconds',title='Exact candidate audit + scaling ansatz')
    axes[1].bar(names,[audit[n]['equation_ops'] for n in names],color='#bc7340')
    axes[1].set(ylabel='SymPy operation count',title='Expression size (not asymptotic complexity)')
    for ax in axes:ax.tick_params(axis='x',rotation=65,labelsize=7)
    fig.tight_layout();fig.savefig(figures/'symbolic_cost.png');plt.close(fig)
    # Visual exemplar chosen by median error within one method, not highest accuracy.
    eligible=[r for r in runs if r['architecture']=='mlp' and r['method']=='lie' and r['group']==runs[0]['group']]
    if not eligible:eligible=[r for r in runs if r['group']==runs[0]['group']]
    errors=np.array([np.mean([s['evolution_relative_l2'] for s in primary_scores(r)]) for r in eligible])
    exemplar=eligible[int(np.argmin(abs(errors-np.median(errors))))]
    test=next(iter(exemplar['test_metrics']))
    data=np.load(Path(exemplar['directory'])/(test+'.npz'));ref=data['reference'][-1]
    snaps=np.load(Path(exemplar['directory'])/'snapshots.npz');frames=[]
    for fields,step in zip(snaps['fields'],snaps['steps']):
        fig,axes=plt.subplots(2,3,figsize=(10,6),layout='constrained')
        for row,index in enumerate([0,3]):
            vmin,vmax=ref[...,index].min(),ref[...,index].max()
            for col,array in enumerate([ref[...,index],fields[...,index],fields[...,index]-ref[...,index]]):
                kwargs={'vmin':vmin,'vmax':vmax,'cmap':'viridis'} if col<2 else {
                    'vmin':-max(abs(fields[...,index]-ref[...,index]).max(),1e-12),
                    'vmax':max(abs(fields[...,index]-ref[...,index]).max(),1e-12),'cmap':'RdBu_r'}
                im=axes[row,col].imshow(array,origin='lower',extent=[0,2*np.pi,0,2*np.pi],**kwargs)
                axes[row,col].set_title(['Numerical reference','PINN prediction','Signed error'][col]+(' / depth' if row==0 else ' / bed'))
                axes[row,col].set(xlabel='x',ylabel='y');axes[row,col].grid(False)
                fig.colorbar(im,ax=axes[row,col],shrink=.65)
        fig.suptitle(f"{test}: {exemplar['architecture']} / {exemplar['method']} / seed {exemplar['seed']} / step {step}\n"
                     'All panels at final physical time; frames show optimization progress',fontsize=11)
        buffer=io.BytesIO();fig.savefig(buffer,format='png');plt.close(fig)
        frames.append(Image.open(buffer).convert('RGB').copy())
    frames[0].save(figures/'training.gif',save_all=True,append_images=frames[1:],duration=900,loop=0)
    frames[-1].save(figures/'final_fields.png')
    text=['# Measured benchmark results','',
          'Pilot measurements on the recorded CPU, not paper reproduction or a general speed/accuracy claim.',
          'Final checkpoints are fixed in advance. Ranges preserve every seed. The translated case is a structural equivariance check and is excluded from aggregate test errors.','',
          '| Group | Architecture | Loss | Parameters | Evolution error: median [min, max] | Training compute: median seconds | Matched runs |',
          '|---|---|---|---:|---:|---:|---:|']
    for s in summary:
        text.append(f"| {s['group']} | {s['architecture']} | {s['method']} | {s['parameters']} | {s['error_median']:.4g} [{s['error_min']:.4g}, {s['error_max']:.4g}] | {s['train_seconds_median']:.3f} | {s['matched_runs']}/{s['total_runs']} |")
    text+=['','Accuracy matching uses the stricter **maximum per-field evolution error**, not the aggregate error displayed above.',
           'No cost advantage is asserted when that threshold is unmet. A single-PDE numerical trajectory is cached for repeated field queries.',
           'Symbolic computation, numerical reference construction, training compute, monitoring, total wall time, and inference are logged separately.',
           'The supplied-generator symbolic audit is not a maximal symmetry classification.','',
           f"GIF exemplar: {exemplar['architecture']}/{exemplar['method']}, seed {exemplar['seed']}, {test}; selected by median error for display only."]
    (out/'SUMMARY.md').write_text('\n'.join(text)+'\n')


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('out');render(parser.parse_args().out)
