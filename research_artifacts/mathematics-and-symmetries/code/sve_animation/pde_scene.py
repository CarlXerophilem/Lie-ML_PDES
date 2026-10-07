"""Manim Community scene: equations -> Lie reduction -> numerical experiment.

First run solve_sve.py and plot_solution.py, then:
python -m manim -qm --fps 24 --disable_caching --media_dir media pde_scene.py SVEProcess
"""
from pathlib import Path
import json
import hashlib
import subprocess
import xml.etree.ElementTree as ET
import numpy as np
from manim import *

ROOT=Path(__file__).resolve().parent
BG='#0c1523'; FG='#edf4ff'; MUTED='#a5b5cc'; CYAN='#44d9ed'; GOLD='#e7b777'

class SVEProcess(Scene):
    def construct(self):
        self.camera.background_color=BG
        def text(s,size=26,color=FG):
            return Text(s,font='DejaVu Sans',font_size=size,color=color)
        def math(s,size=35,color=FG):
            # Portable fallback for hosts with pdflatex/Poppler but no dvisvgm.
            # Equations remain vector paths and are animated by Manim's Write.
            cache=ROOT/'assets'/'equations';cache.mkdir(parents=True,exist_ok=True)
            key=hashlib.sha256((str(size)+s).encode()).hexdigest()[:16]
            tex=cache/(key+'.tex');svg=cache/(key+'.svg')
            if not svg.exists():
                tex.write_text(r'\documentclass[border=1pt]{standalone}'+'\n'+
                    r'\usepackage{amsmath,amssymb}\begin{document}'+'\n'+
                    r'\fontsize{'+str(size)+r'}{'+str(size*1.2)+r'}\selectfont $\displaystyle '+s+r'$\end{document}')
                subprocess.run(['pdflatex','-interaction=batchmode','-halt-on-error',tex.name],
                    cwd=cache,check=True,stdout=subprocess.DEVNULL)
                subprocess.run(['pdftocairo','-svg',str(tex.with_suffix('.pdf')),str(svg)],check=True)
            view=ET.parse(svg).getroot().attrib['viewBox'].split()
            return SVGMobject(str(svg)).set_color(color).set(height=float(view[3])*.017)
        def heading(n,title,subtitle):
            top=text(f'{n}  /  {title}',34).to_edge(UP,buff=.50).to_edge(LEFT,buff=.65)
            sub=text(subtitle,20,MUTED).next_to(top,DOWN,aligned_edge=LEFT,buff=.22)
            self.play(FadeIn(top),FadeIn(sub),run_time=.5)
        def clear():
            self.play(*[FadeOut(m) for m in list(self.mobjects)],run_time=.5)
        def stack(lines,start=1.5,gap=.9):
            mobs=[]
            for i,line in enumerate(lines):
                m=math(line).move_to([0,start-i*gap,0])
                if m.width>12.4:m.scale_to_fit_width(12.4)
                self.play(Write(m),run_time=1.0)
                mobs.append(m)
            return mobs

        heading('01','Saint-Venant-Exner','Paper equations (1)-(4)  |  water depth, momentum and bed evolution')
        stack([r'h_t+(hu)_x=0',r'(hu)_t+\left(hu^2+\frac12gh^2\right)_x+ghB_x=0',
               r'B_t+\beta u^{m-1}u_x=0,\qquad\beta=m A_g\xi'],start=1.65,gap=1.1)
        labels=text('h: depth     u: velocity     B: bed elevation',23,CYAN).move_to([0,-2.2,0])
        cite=text('Paliathanasis, Leon & Leach (2026)  |  Mathematics 14, 433',17,MUTED).to_edge(DOWN,buff=.35)
        self.play(FadeIn(labels),FadeIn(cite));self.wait(3);clear()

        heading('02','Choose the boundary case','Fixed flat bed; a reservoir released onto dry ground')
        stack([r'A_g=\beta=0,\quad B(x,0)=0\quad\Longrightarrow\quad B(x,t)=0',
               r'h(x,0)=\begin{cases}h_0,&x<0,\\0,&x>0,\end{cases}\qquad u(x,0)=0',
               r'h_0=1\,\mathrm{m},\quad g=9.81\,\mathrm{m/s^2},\quad c_0=\sqrt{gh_0}'],start=1.7,gap=1.25)
        note=text('Chosen benchmark: m is inactive and the bed does not move.',22,GOLD).move_to([0,-2.7,0])
        self.play(FadeIn(note));self.wait(3);clear()

        heading('03','Use the scaling symmetry','Simultaneous stretching of space and time leaves h and u unchanged')
        stack([r'X=t\partial_t+x\partial_x,\qquad \frac{dt}{t}=\frac{dx}{x}',
               r'\zeta=\frac{x}{t},\qquad h=H(\zeta),\quad u=U(\zeta)',
               r'\partial_t=-\frac{\zeta}{t}\frac{d}{d\zeta},\qquad\partial_x=\frac1t\frac{d}{d\zeta}',
               r'(U-\zeta)H\prime+HU\prime=0,\qquad gH\prime+(U-\zeta)U\prime=0'],start=1.65,gap=1.05)
        note=text('Two independent variables become one similarity coordinate.',22,CYAN).to_edge(DOWN,buff=.4)
        self.play(FadeIn(note));self.wait(4);clear()

        heading('04','Solve the reduced equations','Choose the rarefaction branch and match the still reservoir')
        stack([r'(U-\zeta)^2=gH,\qquad c=\sqrt{gH},\qquad \zeta=U-c',
               r'2c\prime+U\prime=0\quad\Longrightarrow\quad U+2c=2c_0',
               r'U=\frac23(c_0+\zeta),\qquad H=\frac{(2c_0-\zeta)^2}{9g}',
               r'-c_0t<x<2c_0t,\qquad x_{\rm front}(t)=2c_0t'],start=1.65,gap=1.05)
        note=text('Exact Ritter solution: reservoir + rarefaction fan + dry bed.',22,GOLD).to_edge(DOWN,buff=.4)
        self.play(FadeIn(note));self.wait(4);clear()

        heading('04b','Return to Lagrange variables','Inside the wet fan: x = phi(s,t), with conserved mass label s < 0')
        stack([r's=-\frac{(2c_0t-x)^3}{27gt^2}',
               r'\phi(s,t)=2c_0t-3(-gs)^{1/3}t^{2/3}',
               r'\phi_t=u,\qquad \phi_s=\frac1h',
               r'\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^3}=0\quad\text{(paper equation 5, flat bed)}'],start=1.65,gap=1.05)
        note=text('The map is singular only at the dry front, where h tends to zero.',21,GOLD).to_edge(DOWN,buff=.4)
        self.play(FadeIn(note));self.wait(4);clear()

        heading('05','Simulate independently','Conservative finite volumes on 1,200 cells; CFL = 0.45')
        stack([r'Q=(h,hu)^T,\qquad F=(hu,hu^2+gh^2/2)^T',
               r'\widehat F_{i+1/2}=\frac{F_i+F_{i+1}}2-\frac{a_{i+1/2}}2(Q_{i+1}-Q_i)',
               r'Q_i^{n+1}=Q_i^n-\frac{\Delta t}{\Delta x}\left(\widehat F_{i+1/2}-\widehat F_{i-1/2}\right)',
               r'a=\max(|u|+\sqrt{gh}),\quad \Delta t\le0.45\,\Delta x/a_{\max}'],start=1.65,gap=1.05)
        note=text('Color: velocity   |   cyan surface: numerical   |   dashed: exact',21,CYAN).to_edge(DOWN,buff=.4)
        self.play(FadeIn(note));self.wait(3);clear()

        # Pre-rasterized scientific fields; Manim owns playback and video encoding.
        paths=sorted((ROOT/'assets'/'frames').glob('frame_*.png'))
        if not paths:raise RuntimeError('Run solve_sve.py and plot_solution.py first')
        mob=ImageMobject(str(paths[0])).set(height=8)
        self.add(mob);self.wait(1)
        for p in paths[1:]:
            next_frame=ImageMobject(str(p)).set(height=8)
            self.remove(mob);mob=next_frame;self.add(mob)
            self.wait(3/24)  # 20 seconds of playback for 8 seconds of physical time.
        self.wait(3);clear()

        heading('06','Check the solution','Symbolic residuals + conservation + mesh refinement')
        checks=json.loads((ROOT/'output'/'verification.json').read_text())
        rows=[('Exact fan PDE residuals','0, 0  (SymPy)'),
              ('Minimum numerical water depth','0 m'),
              ('Maximum relative mass drift',f"{checks['production']['relative_mass_drift']:.2e}"),
              ('Final normalized depth error',f"{100*checks['production']['normalized_L1_depth']:.3f}%"),
              ('Mesh refinement: 600 / 1200 / 2400',
               ' / '.join(f"{100*r['normalized_L1_depth']:.3f}%" for r in checks['convergence']))]
        for i,(label,value) in enumerate(rows):
            left=text(label,23).move_to([-3.15,1.55-i*.77,0])
            right=text(value,23,CYAN).move_to([3.3,1.55-i*.77,0])
            self.play(FadeIn(left),FadeIn(right),run_time=.5)
        note=text('A verified fixed-bed benchmark for later mobile-bed and Lie-ML work.',21,GOLD).to_edge(DOWN,buff=.5)
        self.play(FadeIn(note));self.wait(5)
