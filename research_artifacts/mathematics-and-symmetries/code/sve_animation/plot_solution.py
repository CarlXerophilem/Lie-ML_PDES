"""Scientific panels used by the Manim movie; fixed scales across all frames."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize
from solve_sve import ROOT, OUT, C0, G, H0, exact

BG, FG, MUTED = '#0c1523', '#edf4ff', '#a5b5cc'
CYAN, GOLD = '#44d9ed', '#e7b777'
plt.rcParams.update({'figure.facecolor':BG,'axes.facecolor':BG,'axes.edgecolor':MUTED,
    'text.color':FG,'axes.labelcolor':FG,'xtick.color':MUTED,'ytick.color':MUTED,
    'font.size':11,'font.family':'DejaVu Sans','savefig.facecolor':BG})

def main():
    d=np.load(OUT/'solution.npz')
    x,t,h,u=d['x'],d['t'],d['h'],d['u']
    fig=plt.figure(figsize=(12.8,7.2),dpi=100)
    gs=fig.add_gridspec(2,2,left=.07,right=.94,bottom=.13,top=.84,hspace=.47,wspace=.30,
                        height_ratios=[1.05,1.])
    ax=fig.add_subplot(gs[0,:]); ah=fig.add_subplot(gs[1,0]); au=fig.add_subplot(gs[1,1])
    fig.text(.07,.946,'SHALLOW WATER  /  FIXED-BED LIMIT',fontsize=20,weight='bold')
    fig.text(.07,.905,'Dry-bed dam break  |  numerical simulation + exact similarity reference',color=MUTED)
    stamp=fig.text(.78,.905,'t = 0.00 s',fontsize=14,color=CYAN)
    ax.set(xlim=(-40,60),ylim=(-.07,1.18),xlabel='Position x (m)',ylabel='Height z (m)')
    ax.set_title('Water cross-section   •   fill color = horizontal velocity',loc='left',fontsize=12,pad=10)
    ax.axhline(0,color=GOLD,lw=3,label='Bed B = 0')
    ax.fill_between([-40,60],-.07,0,color=GOLD,alpha=.22)
    norm=Normalize(0,2*C0)
    poly=PolyCollection([],cmap='plasma',norm=norm,edgecolors='none')
    ax.add_collection(poly)
    numerical,=ax.plot(x,h[0],color=CYAN,lw=1.4,label='Finite volume')
    analytic,=ax.plot(x,h[0],color=FG,lw=1.5,ls=(0,(5,4)),label='Exact similarity')
    head=ax.axvline(0,color=MUTED,ls=':',lw=1)
    front=ax.axvline(0,color=GOLD,ls=':',lw=1.3)
    ax.legend(loc='upper right',frameon=False,ncol=3,fontsize=9)
    cb=fig.colorbar(poly,ax=ax,pad=.015,fraction=.02)
    cb.set_label('u (m/s)');cb.set_ticks([0,2,4,6])
    imh=ah.imshow(h,origin='lower',extent=[-40,60,0,8],aspect='auto',cmap='viridis',vmin=0,vmax=1)
    uv=np.ma.masked_where(h<1e-4,u)
    cmap=plt.get_cmap('plasma').copy();cmap.set_bad(BG)
    imu=au.imshow(uv,origin='lower',extent=[-40,60,0,8],aspect='auto',cmap=cmap,vmin=0,vmax=2*C0)
    for a,title in [(ah,'Depth h(x,t)  [m]'),(au,'Velocity u(x,t)  [m/s]')]:
        a.set(xlabel='Position x (m)',ylabel='Time t (s)',xlim=(-40,60),ylim=(0,8))
        a.set_title(title,loc='left',fontsize=12,pad=9)
        a.plot(-C0*t,t,':',color=FG,lw=1,alpha=.8)
        a.plot(2*C0*t,t,':',color=GOLD,lw=1.2)
    ch=ah.axhline(0,color=FG,lw=1.5);cu=au.axhline(0,color=FG,lw=1.5)
    fig.colorbar(imh,ax=ah,pad=.02,fraction=.04)
    fig.colorbar(imu,ax=au,pad=.02,fraction=.04)
    fig.text(.07,.022,'Dotted rays: exact fan head and wet/dry front. Velocity is masked for h < 0.0001 m. Vertical scale exaggerated.',fontsize=9,color=MUTED)
    frames=ROOT/'assets'/'frames';frames.mkdir(parents=True,exist_ok=True)
    # Keep all 1200 finite-volume cells in the scientific visualization.
    edges=d['edges']
    for k,tk in enumerate(t):
        polys=np.zeros((len(x),4,2))
        polys[:,0,0]=edges[:-1];polys[:,1,0]=edges[:-1]
        polys[:,2,0]=edges[1:];polys[:,3,0]=edges[1:]
        polys[:,1:3,1]=h[k,:,None]
        poly.set_verts(polys);poly.set_array(u[k])
        numerical.set_ydata(h[k]);analytic.set_ydata(exact(x,tk)[0])
        head.set_xdata([-C0*tk]*2);front.set_xdata([2*C0*tk]*2)
        ch.set_ydata([tk]*2);cu.set_ydata([tk]*2)
        stamp.set_text(f't = {tk:4.2f} s')
        fig.savefig(frames/f'frame_{k:03d}.png')
        if k==len(t)-1: fig.savefig(OUT/'sve-space-time.png',dpi=180)
    plt.close(fig)
    print(f'Rendered {len(t)} frames')

if __name__=='__main__':main()
