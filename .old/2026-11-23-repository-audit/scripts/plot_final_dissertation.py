"""Plot recorded evidence only; the manifest binds every figure to its inputs."""
import argparse,hashlib,json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
ROOT=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--evidence',type=Path,default=ROOT/'research_artifacts/sve-final-20261027');args=parser.parse_args();ev=args.evidence;out=ROOT/'draft/figures/final-20261027';out.mkdir(parents=True,exist_ok=True)
    used={};generated={}
    def read(name):
        p=ev/name;used[name]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
    def save(fig,name):
        for extension in ('pdf','png'):
            p=out/(name+'.'+extension);fig.savefig(p,dpi=180,bbox_inches='tight');generated[p.relative_to(ROOT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
        plt.close(fig)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'figure.constrained_layout.use':True})
    audit=read('data/scalar-source-comparison.json');numbers=range(24,35);states=[audit['eq'+str(n)]['status']=='qualified' for n in numbers]
    fig,ax=plt.subplots(figsize=(8,2.2));colors=['#b45745' if not s else '#bd9d35' for s in states];ax.scatter(list(numbers),np.zeros(11),s=480,c=colors,marker='s')
    for n,s in zip(numbers,states):ax.text(n,0,'Q' if s else 'R',ha='center',va='center',color='white',weight='bold')
    ax.set(xticks=list(numbers),yticks=[],xlabel='Displayed source equation',ylim=(-.7,.7),title='R: refuted as printed     Q: valid sufficient family, necessity not established')
    save(fig,'source-audit')
    rows=read('data/revalidation-summary.json');lookup={r['case']:r for r in rows};keys=['E1:grass_generic',*lookup]
    groups=[('E1:','1D Eulerian',8),('E2:','2D Eulerian',17),('P:','Scalar P',3),('custom:','Mixed law',2)]
    matrix=[];annotations=[]
    for prefix,label,total in groups:
        members=[v for k,v in lookup.items() if k.startswith(prefix)]
        counts=[len(members),sum(v['branch_match'] for v in members)]
        matrix.append([2 if c==total else 0 for c in counts]+[1,1,1])
        annotations.append([f'{c}/{total}' for c in counts]+['open']*3)
    fig,ax=plt.subplots(figsize=(9,3));ax.imshow(matrix,cmap=ListedColormap(['#bd9d35','#eeeeef','#2a827c']),vmin=0,vmax=2,aspect='auto')
    for i,row in enumerate(annotations):
        for k,value in enumerate(row):ax.text(k,i,value,ha='center',va='center',color='white' if k<2 else '#555555')
    ax.set(yticks=range(len(groups)),yticklabels=[g[1] for g in groups],xticks=range(5),xticklabels=['Returned\nfamily','Terminal\nmatching','Complete\nstrata','All required\nreductions','General data\ncompatibility'])
    ax.set_title('Initial 30 inputs: the generic 1D Grass case timed out; complete classification remains open',fontsize=9)
    save(fig,'strict-coverage')
    a=read('data/annular-numerical.json');s={k:np.asarray(v) for k,v in a['samples'].items()};r=s['r']
    fig,axes=plt.subplots(1,3,figsize=(10,2.8));axes[0].plot(r,s['H'],color='#2a827c');axes[0].set_ylabel('Depth H')
    axes[1].plot(r,s['V'],label='Radial V');axes[1].plot(r,s['W'],label='Azimuthal W');axes[1].legend(fontsize=8)
    axes[2].plot(r,s['Z'],label='Bed, t=0');axes[2].plot(r,s['Z']+.1,'--',label='Bed, t=5');axes[2].legend(fontsize=8)
    for ax in axes:ax.set_xlabel('Radius r');ax.grid(alpha=.2)
    save(fig,'annular-fields')
    fig,axes=plt.subplots(1,2,figsize=(9,3));rk=a['rk4_convergence'];n=np.array([v['steps'] for v in rk]);err=np.array([v['max_abs_error'] for v in rk])
    axes[0].loglog(n,err,'o-',label='Recorded RK4 difference');axes[0].loglog(n,err[0]*(n/n[0])**-4.,'--',label='Fourth-order guide');axes[0].set(xlabel='Number of steps',ylabel='Difference from DOP853');axes[0].legend(fontsize=8)
    fd=a['cartesian_finite_difference_checks'];steps=[v['step'] for v in fd]
    for i,label in enumerate(['Mass','x momentum','y momentum','Bed']):axes[1].loglog(steps,[v['per_equation_max_abs_residual'][i] for v in fd],'o-',label=label)
    axes[1].set(xlabel='Cartesian difference step',ylabel='Sampled original-PDE residual');axes[1].legend(fontsize=8,ncol=2)
    for ax in axes:ax.grid(alpha=.2,which='both')
    save(fig,'annular-verification')
    remote=ev/'data/remote-summary.json'
    if remote.exists():
        q=read('data/remote-summary.json');jobs=[v for v in q['jobs'] if not v['name'].startswith('official')]
        fig,ax=plt.subplots(figsize=(8.5,2.8));names=[v['name'].replace('-',' ') for v in jobs];times=[v['elapsed_seconds'] for v in jobs]
        colors={'timeout':'#b45745','memory-limit':'#bd9d35','error':'#8c3344',
                'unparsed':'#999999','returned-partial':'#bd9d35','returned-solved':'#497ea2'}
        ax.barh(names,times,color=[colors.get(v['status'],'#999999') for v in jobs])
        for i,v in enumerate(jobs):ax.text(times[i]+15,i,f"{times[i]:.1f} s: {v['status']}",va='center',fontsize=8)
        ax.set(xlabel='Native CAS command wall time (seconds)',xlim=(0,max(times)*1.65))
        ax.set_title('A returned CAS result still requires independent verification',fontsize=10)
        save(fig,'remote-runtime')
    (ev/'figure-manifest.json').write_text(json.dumps({'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'inputs':used,'outputs':generated,'no_new_solves':True},indent=2))
    print('figures',len(generated)//2)

if __name__=='__main__':main()
