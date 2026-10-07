#!/usr/bin/env python3
"""Shared offline visualizer: colored 2D profiles, time slider/play, heatmaps.

Every solver calls render(). Also run: python pde_scene.py results
Use --coordinates eulerian to plot against x=phi(t,s), or lagrangian for s.
This is a (1+1)D model: plots show one spatial/material axis and time, not a
simulated two-dimensional fluid. Browser HTML is self-contained (no CDN).
"""
from pathlib import Path
import argparse
import json
import numpy as np


def render(out='results',coordinates='lagrangian'):
    if coordinates not in ('lagrangian','eulerian'):raise ValueError(coordinates)
    out=Path(out);runs=[]
    for name in ('LiePINN','PINN','LieReduct'):
        file=out/(name+'.npz')
        if file.exists():
            with np.load(file,allow_pickle=False) as data:
                runs.append({key:data[key].copy() for key in data.files}|{'name':name})
    if not runs:raise FileNotFoundError(f'No solver .npz files in {out}')
    first=runs[0]
    for run in runs[1:]:
        for axis in ('t','s'):
            if not np.array_equal(first[axis],run[axis]):
                raise ValueError('Cannot compare different grids; use separate --out folders.')
        if json.loads(str(first['metrics']))['problem']!=json.loads(str(run['metrics']))['problem']:
            raise ValueError('Cannot compare different parameter settings in one scene.')
    payload={'t':first['t'].tolist(),'s':first['s'].tolist(),'coordinates':coordinates,
             'runs':[{k:(v.tolist() if isinstance(v,np.ndarray) else v)
                      for k,v in run.items() if k in ('name','phi','v','h','residual')} for run in runs],
             'reference':{k:first['exact_'+k].tolist() for k in ('phi','v','h')}}
    html=HTML.replace('__PAYLOAD__',json.dumps(payload,allow_nan=False))
    (out/'scene.html').write_text(html,encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(len(runs),4,figsize=(15,3*len(runs)),squeeze=False,constrained_layout=True)
    T,S=np.meshgrid(first['t'],first['s'],indexing='ij')
    for row,run in enumerate(runs):
        x=run['phi'] if coordinates=='eulerian' else S
        for col,key in enumerate(('phi','v','h','residual')):
            z=run[key]
            # Shared color scales across methods for each physical field.
            values=np.concatenate([r[key].ravel() for r in runs]);lo,hi=values.min(),values.max()
            if key=='residual':
                hi=max(abs(lo),abs(hi),1e-15);lo=-hi
            mesh=axes[row,col].pcolormesh(x,T,z,shading='auto',cmap='coolwarm' if key=='residual' else 'viridis',vmin=lo,vmax=hi)
            axes[row,col].set(title=run['name']+' | '+key,xlabel='x=phi(t,s)' if coordinates=='eulerian' else 'material label s',ylabel='time t')
            fig.colorbar(mesh,ax=axes[row,col])
    fig.suptitle('Scalar SVE benchmark, m=3 | spacetime fields and original PDE residual')
    fig.savefig(out/'spacetime.png',dpi=150);plt.close(fig)
    print('Visualizer:',(out/'scene.html').resolve(),flush=True)
    return out/'scene.html'


HTML=r'''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Symmetry reduction: scalar SVE benchmark</title>
<style>
body{max-width:1120px;margin:30px auto;padding:0 22px;font:16px system-ui;color:#182936;background:#f6f8fa}
h1{font-size:26px} .card{background:white;padding:18px;border:1px solid #dce3e8;border-radius:12px;margin:16px 0}
canvas{width:100%;height:420px}button,select{padding:9px;margin-right:12px}input{width:55%;vertical-align:middle}
code{white-space:normal}small{color:#4a5e6b}.legend span{margin-right:22px;font-weight:600}
</style>
<h1>Lie reduction and neural correction</h1>
<p>Scalar SVE-informed benchmark · m = 3 · one spatial coordinate + time</p>
<div class="card"><code>∂t(φs φtt − g φss / φs²) − gβ ∂s(φt² φts / φs) = 0</code>
<p>Lie branch: σ = st², φ = F(σ). Reconstruction: x = φ, v = φt, h = 1/φs.</p>
<small>The full bed-evolution SVE system is not solved here. Dashed lines are the exact verification solution; they are not interior training labels.</small></div>
<div class="card"><button id="play">Play</button><input id="time" type="range" min="0" step="1" value="0"><output id="clock"></output>
<p><select id="field"><option value="h">Depth h</option><option value="v">Velocity v</option><option value="phi">Particle position φ</option><option value="residual">Original PDE residual</option></select>
<select id="coord"><option value="lagrangian">Lagrangian: s</option><option value="eulerian">Eulerian: x = φ(t,s)</option></select></p>
<div class="legend" id="legend"></div><canvas id="plot" width="1050" height="420"></canvas>
<small>Axes retain fixed scales during playback. Eulerian curves cover moving material intervals; values outside those intervals are not extrapolated.</small></div>
<script>
const D=__PAYLOAD__;
const palette=['#146eb4','#d34d38','#25915d'],canvas=document.getElementById('plot'),ctx=canvas.getContext('2d');
const slider=document.getElementById('time'),field=document.getElementById('field'),coord=document.getElementById('coord');
slider.max=D.t.length-1;coord.value=D.coordinates;
document.getElementById('legend').innerHTML=D.runs.map((r,i)=>`<span style="color:${palette[i]}">${r.name}</span>`).join('')+'<span>— — exact</span>';
function extent(arr){let lo=Infinity,hi=-Infinity;for(const a of arr)for(const row of a)for(const x of row){lo=Math.min(lo,x);hi=Math.max(hi,x)}return [lo,hi]}
function draw(){
 const k=+slider.value,f=field.value,euler=coord.value==='eulerian';
 document.getElementById('clock').textContent=' t = '+D.t[k].toFixed(4);
 const series=D.runs.map((r,i)=>({x:euler?r.phi[k]:D.s,y:r[f][k],color:palette[i]}));
 if(f!=='residual')series.push({x:euler?D.reference.phi[k]:D.s,y:D.reference[f][k],color:'#333',dash:true});
 let [y0,y1]=extent(D.runs.map(r=>r[f]).concat(f==='residual'?[]:[D.reference[f]]));
 let [x0,x1]=euler?extent(D.runs.map(r=>r.phi).concat([D.reference.phi])):[D.s[0],D.s[D.s.length-1]];
 const pad=Math.max((y1-y0)*.08,Math.max(Math.abs(y0),Math.abs(y1))*1e-4,1e-12);y0-=pad;y1+=pad;
 const L=85,R=1025,T=22,B=357,px=x=>L+(x-x0)/(x1-x0)*(R-L),py=y=>B-(y-y0)/(y1-y0)*(B-T);
 ctx.clearRect(0,0,1050,420);ctx.font='13px system-ui';ctx.fillStyle='#354c5c';
 for(let i=0;i<=5;i++){let y=y0+(y1-y0)*i/5,x=x0+(x1-x0)*i/5;
  ctx.strokeStyle='#e6ebee';ctx.beginPath();ctx.moveTo(L,py(y));ctx.lineTo(R,py(y));ctx.stroke();
  ctx.fillText(y.toPrecision(4),5,py(y)+4);ctx.fillText(x.toFixed(3),px(x)-18,B+25)}
 for(const a of series){ctx.strokeStyle=a.color;ctx.lineWidth=a.dash?1.7:2.5;ctx.setLineDash(a.dash?[7,5]:[]);ctx.beginPath();a.x.forEach((x,i)=>i?ctx.lineTo(px(x),py(a.y[i])):ctx.moveTo(px(x),py(a.y[i])));ctx.stroke()}
 ctx.setLineDash([]);ctx.fillStyle='#182936';ctx.fillText(euler?'Eulerian position x':'Material label s',450,407);ctx.fillText(f,10,15);
}
slider.oninput=draw;field.onchange=draw;coord.onchange=draw;
let timer=null;document.getElementById('play').onclick=function(){if(timer){clearInterval(timer);timer=null;this.textContent='Play'}else{this.textContent='Pause';timer=setInterval(()=>{slider.value=(+slider.value+1)%D.t.length;draw()},140)}};draw();
</script></html>'''


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out',nargs='?',default='results',type=Path)
    parser.add_argument('--coordinates',choices=['lagrangian','eulerian'],default='lagrangian')
    args=parser.parse_args();render(args.out,args.coordinates)
