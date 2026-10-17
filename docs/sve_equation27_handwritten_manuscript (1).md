# 标量浅水主方程的李点对称约化

## 从原论文式 (7) 到式 (27) 的完整中文手算稿

本文按十二个手算单元组织；单元编号不表示固定打印页码。正文中的“原式 (27)”等编号指文献 [3]；本稿用章节编号、$\mathcal R_3$、$\mathcal R_2$、(I1)、(A27) 和星号编号区分自行推导及修正式。

研究主线是：确定 $m=3$ 时的完整局部点对称代数，说明一维最优系统的分类意义，选取 $\langle X_5\rangle$ 的不变解，再用继承对称性进行两次 ODE 商降阶，最后作明确的倒数平移变换。最终三次 Abel 方程的因变量是 $N$，与原文定义的微分不变量 $M$ 不同。

文中“定义”用于约定对象与记号；“精确恒等式”表示可由代数及链式法则核验的等式；“命题”附带适用条件与推导；“局部坐标限制”记录可逆性条件；“文献修正”表示与核读的原文印刷公式不同的重建结果；“数值一致性检查”仅报告有限区间上的计算比较。参考文献按 GB/T 7714 手工编排。群作用、延拓和约化的一般背景见 [1-2]。

## 单元 1：物质坐标、模型范围与主导数

### 1.1 欧拉系统与物质标签的定义

设欧拉坐标为 $(t,x)$，水深、流速和床面分别为 $h^E(t,x)>0$、$u^E(t,x)>0$、$B^E(t,x)$。本文考虑光滑场，并在所需运算的邻域内保留正性条件。文献 [3] 的 SVE 系统及 Grass 输沙律写为

$$
\begin{aligned}
&\partial_t h^E+\partial_x(h^E u^E)=0,\\
&\partial_t(h^E u^E)+\partial_x\left(h^E(u^E)^2+\frac g2(h^E)^2\right)+g h^E\partial_x B^E=0,\\
&\partial_tB^E+\beta(u^E)^{m-1}\partial_xu^E=0,\\
&Q_b^E=A_g(u^E)^m,\qquad
\beta=mA_g\chi=m\kappa>0,\qquad
\chi=(1-\vartheta)^{-1}.
\end{aligned}
$$

这里 $g>0$，$A_g>0$，$m\ge1$，$0\le\vartheta<1$。后文沿用论文的归一化变量，令 $b=g\beta$；$b$ 是组合参数，不能在未作量纲约定时将有量纲物理常数与纯数直接比较。

为使空间坐标随水体运动，定义物质标签 $s(t,x)$。连续性方程给出闭一形式

$$
ds=h^E\,dx-h^Eu^E\,dt,
\qquad s_x=h^E>0,\qquad s_t=-h^Eu^E,
$$

因为

$$
\partial_t s_x=\partial_t h^E
=-\partial_x(h^Eu^E)=\partial_xs_t.
$$

在单连通局部区域可积分得到 $s$；由 $s_x>0$，反函数定理给出局部逆映射 $x=\phi(t,s)$。对恒等式 $s(t,\phi(t,s))=s$ 分别求导：

$$
s_x\phi_s=1,
\qquad s_t+s_x\phi_t=0.
$$

因此

$$
\boxed{\phi_s=\frac1{h^E(t,\phi(t,s))}>0,
\qquad \phi_t=u^E(t,\phi(t,s))>0.}
\tag{1.1}
$$

### 1.2 回拉与偏导数的链式法则

**定义。** 对任意欧拉场 $f^E$，其物质回拉为 $f^L(t,s)=f^E(t,\phi(t,s))$。固定物质标签求导，得到

$$
D_sf^L=(\partial_xf^E)\circ\phi\;\phi_s,
\qquad
D_tf^L=(\partial_tf^E)\circ\phi
+(\partial_xf^E)\circ\phi\;\phi_t.
$$

解出欧拉导数的回拉：

$$
\boxed{
(\partial_xf^E)\circ\phi=\frac1{\phi_s}D_sf^L,
\qquad
(\partial_tf^E)\circ\phi=D_tf^L-\frac{\phi_t}{\phi_s}D_sf^L.}
\tag{1.2}
$$

将动量方程展开并减去 $u^E$ 乘连续性方程，得到

$$
h^E(u_t^E+u^Eu_x^E)+g h^Eh_x^E+g h^EB_x^E=0.
$$

除以 $h^E>0$，再用 $u^L=\phi_t$、$h^L=1/\phi_s$：

$$
\begin{aligned}
(u_t^E+u^Eu_x^E)\circ\phi&=\phi_{tt},\\
h_x^E\circ\phi&=\frac1{\phi_s}D_s(\phi_s^{-1})
=-\frac{\phi_{ss}}{\phi_s^3},\\
B_x^E\circ\phi&=\frac{B_s^L}{\phi_s}.
\end{aligned}
$$

因此，标准回拉下的动量方程和 Exner 方程分别为

$$
\begin{aligned}
&\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^3}
+\frac g{\phi_s}B_s^L=0,\\
&B_t^L-\frac{\phi_t}{\phi_s}B_s^L
+\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}=0.
\end{aligned}
\tag{1.3}
$$

**文献修正的范围。** 在上述标准回拉解释下，原论文式 (6) 没有保留 $-\phi_tB_s^L/\phi_s$。这是一个模型转换问题，必须与随后针对论文标量式 (7) 的对称计算分开。

### 1.3 本稿固定研究的标量方程

先定义两个表达式

$$
H=\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2},
\qquad
J=\beta\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}.
$$

若采用 (1.3)，则 $B_s^L=-H/g$，$B_t^L=-\phi_tH/(g\phi_s)-J$。相容性 $D_tB_s^L=D_sB_t^L$ 给出

$$
D_tH-D_s\left(\frac{\phi_tH}{\phi_s}\right)-gD_sJ=0.
$$

若采用原文形式关系 $B_s^L=-H/g$、$B_t^L=-J$，则相容性给出本稿此后固定研究的方程

$$
\boxed{
\Delta_m[\phi]
=D_t\left(\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2}\right)
-g\beta D_s\left(\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}\right)=0.}
\tag{1.4}
$$

这是原文式 (7) 的标量模型。本稿的约化与重构均针对 (1.4)，不据此宣称已建立它与标准欧拉 SVE 系统的等价性。

若 $\phi\in C^3$ 满足 (1.4)，则 $\omega=-J\,dt-H\,ds/g$ 闭合。在单连通矩形上，形式床面可重构为

$$
B^L(t,s)=B_0-\int_{t_0}^tJ(r,s_0)\,dr
-\frac1g\int_{s_0}^sH(t,q)\,dq.
\tag{1.5}
$$

直接核验得 $B_s^L=-H/g$；又因 $D_tH=gD_sJ$，

$$
B_t^L=-J(t,s_0)-\frac1g\int_{s_0}^sD_tH(t,q)\,dq
=-J(t,s_0)-\int_{s_0}^sD_sJ(t,q)\,dq=-J(t,s).
$$

这里 $B_0$ 是唯一未定的加法常数。

### 1.4 展开全导数并建立射流坐标

先用乘积法则和商法则展开：

$$
\begin{aligned}
D_t(\phi_s\phi_{tt})&=\phi_{ts}\phi_{tt}+\phi_s\phi_{ttt},\\
D_t\left(\frac{\phi_{ss}}{\phi_s^2}\right)
&=\frac{\phi_{tss}}{\phi_s^2}
-\frac{2\phi_{ss}\phi_{ts}}{\phi_s^3},\\
D_s\left(\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}\right)
&=(m-1)\phi_t^{m-2}\frac{\phi_{ts}^2}{\phi_s}
+\phi_t^{m-1}\frac{\phi_{tss}}{\phi_s}
-\phi_t^{m-1}\frac{\phi_{ts}\phi_{ss}}{\phi_s^2}.
\end{aligned}
$$

**定义。** 取平凡丛 $\pi:(t,s,\phi)\mapsto(t,s)$。三阶射流丛 $J^3\pi$ 记录一点处函数值和三阶以内所有导数值。引入记号

$$
\begin{gathered}
v=\phi_t,\quad\rho=\phi_s,\quad
a=\phi_{tt},\quad\ell=\phi_{ts},\quad c=\phi_{ss},\\
T=\phi_{ttt},\quad U=\phi_{tts},\quad
R=\phi_{tss},\quad V=\phi_{sss}.
\end{gathered}
$$

点坐标有三个，导数坐标有 $2+3+4=9$ 个，故 $\dim J^3\pi=12$。这些记号仅是标准导数的代数坐标名称。

于是

$$
\begin{aligned}
\Delta_m={}&\rho T+\ell a
-g(\rho^{-2}+\beta v^{m-1}\rho^{-1})R\\
&+g(2\rho^{-3}+\beta v^{m-1}\rho^{-2})\ell c
-g\beta(m-1)v^{m-2}\rho^{-1}\ell^2.
\end{aligned}
\tag{1.6}
$$

点对称分类在 $v>0,\rho>0$ 的局部射流坐标卡上进行。后续 $X_5$ 相似约化另取 $t>0,s>0$。$m=3$ 时

$$
\frac{\partial\Delta_3}{\partial T}=\rho>0,
$$

故 $\mathcal E_3=\{\Delta_3=0\}$ 是十一维正则超曲面，可解出

$$
\boxed{
T_*
=-\frac{\ell a}{\rho}
+g(\rho^{-3}+\beta v^2\rho^{-2})R
-g(2\rho^{-4}+\beta v^2\rho^{-3})\ell c
+2g\beta v\rho^{-2}\ell^2.}
\tag{1.7}
$$

在 $\mathcal E_3$ 上，$(t,s,\phi,v,\rho,a,\ell,c,U,R,V)$ 是局部独立坐标，其中 $v,\rho$ 在正开集内自由变化。后文“分离系数”依赖的正是这种独立性。

## 单元 2：无穷小判据与全部所需延拓余项

### 2.1 群、生成元与方程流形的相切条件

**定义。** 局部单参数群是满足 $\Gamma_0=\mathrm{id}$、$\Gamma_{\epsilon+\delta}=\Gamma_\epsilon\circ\Gamma_\delta$ 的局部可逆点变换，等式在各映射均有定义处成立。其无穷小生成元为

$$
\begin{aligned}
X&=\left.\frac d{d\epsilon}\right|_0\Gamma_\epsilon
=\tau(t,s,\phi)\partial_t+\xi(t,s,\phi)\partial_s
+\eta(t,s,\phi)\partial_\phi,\\
\bar t&=t+\epsilon\tau+O(\epsilon^2),\quad
\bar s=s+\epsilon\xi+O(\epsilon^2),\quad
\bar\phi=\phi+\epsilon\eta+O(\epsilon^2).
\end{aligned}
$$

延拓的几何定义是：先将函数图像作点变换，再由链式法则计算新图像的导数。必须限制在变换后图像仍能写成关于 $(\bar t,\bar s)$ 的函数的区域，即独立变量变换沿图像的雅可比不为零。在恒等变换附近该条件局部成立。

为区分点系数偏导与延拓系数，规定 $\eta_{,t}=\partial\eta/\partial t$，而 $\eta^{[t]}$ 表示 $\phi_t$ 坐标上的延拓系数。三阶延拓为

$$
\begin{aligned}
\operatorname{pr}^{(3)}X={}&X
+\eta^{[t]}\partial_v+\eta^{[s]}\partial_\rho
+\eta^{[tt]}\partial_a+\eta^{[ts]}\partial_\ell
+\eta^{[ss]}\partial_c\\
&+\eta^{[ttt]}\partial_T+\eta^{[tts]}\partial_U
+\eta^{[tss]}\partial_R+\eta^{[sss]}\partial_V.
\end{aligned}
$$

**定理的适用条件。** 本方程满足最大秩条件 $\Delta_{3,T}=\rho>0$。在正坐标卡内，其解出 $\phi_{ttt}$ 的右端是解析函数；$t=\mathrm{const}$ 为非特征初始面。取解析初值 $\phi|_{t=t_0}$、$\phi_t|_{t=t_0}$、$\phi_{tt}|_{t=t_0}$，可任意指定所需有限阶初始射流，Cauchy–Kovalevskaya 定理给出实现相容三阶射流的局部解析解。因此局部可解性成立，可使用 [1] 的无穷小对称判据：

$$
\boxed{\left.\operatorname{pr}^{(3)}X(\Delta_3)\right|_{T=T_*}=0.}
\tag{2.1}
$$

这要求在方程超曲面上相切；尚不能预设在全部射流上恒等为零。

### 2.2 全导数与递推式

对依赖有限阶射流的函数，定义全导数

$$
\begin{aligned}
D_t&=\partial_t+v\partial_\phi+a\partial_v+\ell\partial_\rho
+T\partial_a+U\partial_\ell+R\partial_c+\cdots,\\
D_s&=\partial_s+\rho\partial_\phi+\ell\partial_v+c\partial_\rho
+U\partial_a+R\partial_\ell+V\partial_c+\cdots.
\end{aligned}
$$

例如 $D_t\tau=\tau_{,t}+v\tau_{,\phi}$，$D_s\tau=\tau_{,s}+\rho\tau_{,\phi}$。链式法则给出递推

$$
\eta^{[Ji]}=D_i\eta^{[J]}-\phi_{Jt}D_i\tau-\phi_{Js}D_i\xi,
\qquad \eta^{[\varnothing]}=\eta,\quad i\in\{t,s\}.
\tag{2.2}
$$

例如对 $\bar\phi_{\bar t}$ 作一阶展开，沿原图像有

$$
D_t\bar\phi=\bar\phi_{\bar t}D_t\bar t
+\bar\phi_{\bar s}D_t\bar s.
$$

代入 $D_t\bar\phi=v+\epsilon D_t\eta$、$D_t\bar t=1+\epsilon D_t\tau$、$D_t\bar s=\epsilon D_t\xi$，比较 $\epsilon$ 系数：

$$
D_t\eta=\eta^{[t]}+vD_t\tau+\rho D_t\xi.
$$

这说明递推中的减项来自独立变量本身的变换。

### 2.3 一阶与二阶系数

由 (2.2) 逐项展开得

$$
\begin{aligned}
\eta^{[t]}={}&\eta_{,t}+(\eta_{,\phi}-\tau_{,t})v
-\xi_{,t}\rho-\tau_{,\phi}v^2-\xi_{,\phi}v\rho,\\
\eta^{[s]}={}&\eta_{,s}-\tau_{,s}v
+(\eta_{,\phi}-\xi_{,s})\rho
-\tau_{,\phi}v\rho-\xi_{,\phi}\rho^2.
\end{aligned}
\tag{2.3}
$$

二阶系数为

$$
\begin{aligned}
\eta^{[tt]}={}&(\eta_{,\phi}-2\tau_{,t}-3\tau_{,\phi}v-\xi_{,\phi}\rho)a
-2(\xi_{,t}+\xi_{,\phi}v)\ell+\mathcal E_{tt},\\
\eta^{[ts]}={}&-(\tau_{,s}+\tau_{,\phi}\rho)a
+(\eta_{,\phi}-\tau_{,t}-\xi_{,s}-2\tau_{,\phi}v-2\xi_{,\phi}\rho)\ell\\
&-(\xi_{,t}+\xi_{,\phi}v)c+\mathcal E_{ts},\\
\eta^{[ss]}={}&-2(\tau_{,s}+\tau_{,\phi}\rho)\ell
+(\eta_{,\phi}-2\xi_{,s}-\tau_{,\phi}v-3\xi_{,\phi}\rho)c
+\mathcal E_{ss}.
\end{aligned}
\tag{2.4}
$$

这里三个余项不是省略号，而是下列完整多项式：

$$
\begin{aligned}
\mathcal E_{tt}={}&\eta_{,tt}+(2\eta_{,t\phi}-\tau_{,tt})v-\xi_{,tt}\rho
+(\eta_{,\phi\phi}-2\tau_{,t\phi})v^2\\
&-2\xi_{,t\phi}v\rho-\tau_{,\phi\phi}v^3-\xi_{,\phi\phi}v^2\rho,\\
\mathcal E_{ts}={}&\eta_{,ts}+(\eta_{,s\phi}-\tau_{,ts})v
+(\eta_{,t\phi}-\xi_{,ts})\rho-\tau_{,s\phi}v^2\\
&+(\eta_{,\phi\phi}-\tau_{,t\phi}-\xi_{,s\phi})v\rho
-\xi_{,t\phi}\rho^2-\tau_{,\phi\phi}v^2\rho-\xi_{,\phi\phi}v\rho^2,\\
\mathcal E_{ss}={}&\eta_{,ss}-\tau_{,ss}v
+(2\eta_{,s\phi}-\xi_{,ss})\rho-2\tau_{,s\phi}v\rho\\
&+(\eta_{,\phi\phi}-2\xi_{,s\phi})\rho^2
-\tau_{,\phi\phi}v\rho^2-\xi_{,\phi\phi}\rho^3.
\end{aligned}
\tag{2.5}
$$

### 2.4 两个实际参与计算的三阶系数

由于 $\Delta_3$ 不含 $U,V$，$\eta^{[tts]}\Delta_{3,U}$ 与 $\eta^{[sss]}\Delta_{3,V}$ 恒为零；所需的三阶系数只有

$$
\begin{aligned}
\eta^{[ttt]}={}&(\eta_{,\phi}-3\tau_{,t}-4\tau_{,\phi}v-\xi_{,\phi}\rho)T
-3(\xi_{,t}+\xi_{,\phi}v)U+\mathcal E_{ttt},\\
\eta^{[tss]}={}&-2(\tau_{,s}+\tau_{,\phi}\rho)U
+(\eta_{,\phi}-\tau_{,t}-2\xi_{,s}-2\tau_{,\phi}v-3\xi_{,\phi}\rho)R\\
&-(\xi_{,t}+\xi_{,\phi}v)V+\mathcal E_{tss}.
\end{aligned}
\tag{2.6}
$$

注意 $U,V$ 仍会出现在这两个系数中，因而必须作为自由射流参与分离。完整低阶余项为

$$
\begin{aligned}
\mathcal E_{ttt}={}&-3\tau_{,\phi}a^2-3\xi_{,\phi}a\ell\\
&+\big[-6\tau_{,\phi\phi}v^2-3\xi_{,\phi\phi}\rho v
+3(\eta_{,\phi\phi}-3\tau_{,t\phi})v\\
&\qquad-3\xi_{,t\phi}\rho+3(\eta_{,t\phi}-\tau_{,tt})\big]a\\
&-3(\xi_{,\phi\phi}v^2+2\xi_{,t\phi}v+\xi_{,tt})\ell\\
&-\tau_{,\phi\phi\phi}v^4-\xi_{,\phi\phi\phi}\rho v^3
+(\eta_{,\phi\phi\phi}-3\tau_{,t\phi\phi})v^3\\
&-3\xi_{,t\phi\phi}\rho v^2
+3(\eta_{,t\phi\phi}-\tau_{,tt\phi})v^2
-3\xi_{,tt\phi}\rho v\\
&+(3\eta_{,tt\phi}-\tau_{,ttt})v-\xi_{,ttt}\rho+\eta_{,ttt},
\end{aligned}
\tag{2.7}
$$

$$
\begin{aligned}
\mathcal E_{tss}={}&-\tau_{,\phi}ac
-(\tau_{,\phi\phi}\rho^2+2\tau_{,s\phi}\rho+\tau_{,ss})a
-2\tau_{,\phi}\ell^2-3\xi_{,\phi}c\ell\\
&+\big[-4\tau_{,\phi\phi}\rho v-4\tau_{,s\phi}v
-3\xi_{,\phi\phi}\rho^2
+2(\eta_{,\phi\phi}-\tau_{,t\phi}-2\xi_{,s\phi})\rho\\
&\qquad+2\eta_{,s\phi}-2\tau_{,st}-\xi_{,ss}\big]\ell\\
&+\big[-\tau_{,\phi\phi}v^2-3\xi_{,\phi\phi}\rho v
+(\eta_{,\phi\phi}-\tau_{,t\phi}-2\xi_{,s\phi})v\\
&\qquad-3\xi_{,t\phi}\rho+\eta_{,t\phi}-2\xi_{,st}\big]c\\
&-\tau_{,\phi\phi\phi}\rho^2v^2
-2\tau_{,s\phi\phi}\rho v^2-\tau_{,ss\phi}v^2
-\xi_{,\phi\phi\phi}\rho^3v\\
&+(\eta_{,\phi\phi\phi}-\tau_{,t\phi\phi}-2\xi_{,s\phi\phi})\rho^2v
+(2\eta_{,s\phi\phi}-\xi_{,ss\phi}-2\tau_{,st\phi})\rho v\\
&+(\eta_{,ss\phi}-\tau_{,sst})v-\xi_{,t\phi\phi}\rho^3
+(\eta_{,t\phi\phi}-2\xi_{,st\phi})\rho^2\\
&+(2\eta_{,st\phi}-\xi_{,sst})\rho+\eta_{,sst}.
\end{aligned}
\tag{2.8}
$$

### 2.5 作用于方程的七个系数

对 (1.6) 逐坐标求偏导，$m=3$ 时得到

$$
\begin{aligned}
\Delta_{3,v}&=-2g\beta v\rho^{-1}R+2g\beta v\rho^{-2}\ell c
-2g\beta\rho^{-1}\ell^2,\\
\Delta_{3,\rho}&=T+g(2\rho^{-3}+\beta v^2\rho^{-2})R
-g(6\rho^{-4}+2\beta v^2\rho^{-3})\ell c
+2g\beta v\rho^{-2}\ell^2,\\
\Delta_{3,a}&=\ell,\\
\Delta_{3,\ell}&=a+g(2\rho^{-3}+\beta v^2\rho^{-2})c
-4g\beta v\rho^{-1}\ell,\\
\Delta_{3,c}&=g(2\rho^{-3}+\beta v^2\rho^{-2})\ell,\\
\Delta_{3,T}&=\rho,\qquad
\Delta_{3,R}=-g(\rho^{-2}+\beta v^2\rho^{-1}).
\end{aligned}
$$

由于方程不显含 $(t,s,\phi)$，作用式没有额外的 $\tau\Delta_{3,t}$ 等项。因此可完全显式地组装

$$
\begin{aligned}
\mathscr P=\rho^4\Big[&
\eta^{[t]}\Delta_{3,v}+\eta^{[s]}\Delta_{3,\rho}
+\eta^{[tt]}\ell
+\eta^{[ts]}\Delta_{3,\ell}
+\eta^{[ss]}\Delta_{3,c}\\
&+\rho\eta^{[ttt]}
-g(\rho^{-2}+\beta v^2\rho^{-1})\eta^{[tss]}
\Big]_{T=T_*}.
\tag{2.9}
\end{aligned}
$$

$\rho^4>0$，所以 $\mathscr P=0$ 与 (2.1) 等价。至此，所有参与主方程的延拓余项均已写明。

## 单元 3：确定方程的完备求解与 $X_5$ 的来源

### 3.1 六个系数先分离变量依赖

把 (1.7)、(2.3)–(2.8) 代入 (2.9)，按八个自由射流坐标展开。未施加任何系数约束前，所得多项式有 118 个非零单项式系数。手算不必按任意排列处理全部项；先选能逐步三角消元的六项。

$V$ 只来自 $\eta^{[tss]}$ 中的 $-(\xi_{,t}+\xi_{,\phi}v)V$，故其完整贡献是

$$
g(\rho^2+\beta v^2\rho^3)(\xi_{,t}+\xi_{,\phi}v)V
=g\xi_{,t}\rho^2V+g\xi_{,\phi}v\rho^2V
+g\beta\xi_{,t}v^2\rho^3V+g\beta\xi_{,\phi}v^3\rho^3V.
$$

最高两个 $v$ 次数给出 $\xi_{,\phi}=\xi_{,t}=0$。施加这两式后，再分离下表四个含 $R$ 的系数：

| 自由射流单项式 | 系数 | 推论 |
|---|---|---|
| $v^3\rho^3V$ | $g\beta\xi_{,\phi}$ | $\xi_{,\phi}=0$ |
| $v^2\rho^3V$ | $g\beta\xi_{,t}$ | $\xi_{,t}=0$ |
| $v^3\rho^3R$ | $-2g\beta\tau_{,\phi}$ | $\tau_{,\phi}=0$ |
| $v^3\rho^2R$ | $-2g\beta\tau_{,s}$ | $\tau_{,s}=0$ |
| $v^2\rho^2R$ | $2g\beta\eta_{,s}$ | $\eta_{,s}=0$ |
| $v\rho^3R$ | $-2g\beta\eta_{,t}$ | $\eta_{,t}=0$ |

这些是指定单项式的系数，不能把其中四项之和误写成全部含 $g\beta R$ 的部分。因 $g\beta>0$，没有除以零的问题。得到

$$
\tau=T_0(t),\qquad\xi=Z_0(s),\qquad\eta=H_0(\phi).
\tag{3.1}
$$

### 3.2 全部剩余系数及五个任意常数

以下 $T_0'$、$Z_0'$、$H_0'$ 分别对各自单一自变量求导。延拓简化为

$$
\begin{aligned}
\eta^{[t]}&=(H_0'-T_0')v,&
\eta^{[s]}&=(H_0'-Z_0')\rho,\\
\eta^{[tt]}&=(H_0'-2T_0')a+H_0''v^2-T_0''v,\\
\eta^{[ts]}&=(H_0'-T_0'-Z_0')\ell+H_0''v\rho,\\
\eta^{[ss]}&=(H_0'-2Z_0')c+H_0''\rho^2-Z_0''\rho,\\
\eta^{[ttt]}&=(H_0'-3T_0')T+3H_0''va-3T_0''a
+H_0'''v^3-T_0'''v,\\
\eta^{[tss]}&=(H_0'-T_0'-2Z_0')R
+2H_0''\rho\ell+H_0''vc+H_0'''v\rho^2-Z_0''\ell.
\end{aligned}
\tag{3.2}
$$

记 $L=3H_0'-2T_0'-Z_0'$、$b=g\beta$。将 (3.2) 代入 (2.9)，全部剩余非零系数恰为下列十一项：

| 单项式 | 系数 |
|---|---|
| $\rho^5v^3$ | $-(b-1)H_0'''$ |
| $\rho^4v^2\ell$ | $-(5b-1)H_0''$ |
| $\rho^5va$ | $4H_0''$ |
| $\rho^5v$ | $-T_0'''$ |
| $\rho^4v\ell$ | $-T_0''$ |
| $\rho^4v$ | $-gH_0'''$ |
| $\rho^2vc$ | $gH_0''$ |
| $\rho^5a$ | $-3T_0''$ |
| $\rho^2\ell$ | $-gZ_0''$ |
| $\rho^2R$ | $gL$ |
| $\rho\ell c$ | $-2gL$ |

按 $\rho^5va$、$\rho^5a$、$\rho^2\ell$、$\rho^2R$ 的顺序，得到

$$
H_0''=T_0''=Z_0''=0,
\qquad3H_0'-2T_0'-Z_0'=0.
$$

其余七个系数随之全部为零。没有除以 $b-1$ 或 $5b-1$，故 $b=1$、$b=1/5$ 不产生遗漏分支。积分，令 $H_0'=c_0$、$T_0'=c_0+d_0$，可得

$$
\begin{aligned}
\tau&=a_0+(c_0+d_0)t,\\
\xi&=b_0+(c_0-2d_0)s,\\
\eta&=e_0+c_0\phi.
\end{aligned}
\tag{3.3}
$$

这里 $b_0$ 是生成元中的常数，与 $b=g\beta$ 不同。于是

$$
\begin{gathered}
X=a_0X_1+b_0X_2+e_0X_3+c_0X_4+d_0X_5,\\
\boxed{
X_1=\partial_t,\quad X_2=\partial_s,\quad X_3=\partial_\phi,\quad
X_4=t\partial_t+s\partial_s+\phi\partial_\phi,\quad
X_5=t\partial_t-2s\partial_s.}
\end{gathered}
\tag{3.4}
$$

**充分性核验。** 将 (3.3) 代回尚未施加 $T=T_*$ 的作用式，得到精确恒等式

$$
\operatorname{pr}^{(3)}X(\Delta_3)=-(2c_0+d_0)\Delta_3.
\tag{3.5}
$$

必要条件的求解与充分性恒等式共同证明：在已声明的局部正则坐标卡上，$m=3$ 时完整李点对称代数正是这五维代数。

### 3.3 独立解释：为什么 $X_5$ 的系数是 $1,-2,0$

为解释系数而不依赖结果倒推相似变量，先限定在对角标度这一候选族内。其几何意义是分别按固定速率缩放三个点坐标：

$$
\bar t=e^{a_t\epsilon}t,\qquad
\bar s=e^{a_s\epsilon}s,\qquad
\bar\phi=e^{a_\phi\epsilon}\phi.
$$

这里 $a_t,a_s,a_\phi$ 是待定常数，$g,\beta$ 固定。对变换后的图像，链式法则给出

$$
\bar\phi_{\bar t^i\bar s^j}
=e^{(a_\phi-i a_t-j a_s)\epsilon}\phi_{t^is^j}.
$$

**定义。** 若 $\bar K=e^{w\epsilon}K$，称 $w$ 为 $K$ 的该群标度权重。乘积加权，商式减权；$D_t,D_s$ 分别贡献 $-a_t,-a_s$。把 $\Delta_m=I-G-\mathcal B$ 分成三类项：

$$
I=D_t(\phi_s\phi_{tt}),\quad
G=gD_t(\phi_{ss}/\phi_s^2),\quad
\mathcal B=g\beta D_s(\phi_t^{m-1}\phi_{ts}/\phi_s).
$$

逐项计算：

$$
\begin{aligned}
w_I&=(a_\phi-a_s)+(a_\phi-2a_t)-a_t
=2a_\phi-a_s-3a_t,\\
w_G&=(a_\phi-2a_s)-2(a_\phi-a_s)-a_t
=-a_\phi-a_t,\\
w_{\mathcal B}&=(m-1)(a_\phi-a_t)
+(a_\phi-a_t-a_s)-(a_\phi-a_s)-a_s\\
&=(m-1)a_\phi-ma_t-a_s.
\end{aligned}
\tag{3.6}
$$

等权显然足以保持零集。为证明在本候选族内也有必要性，不能仅要求整个表达式预先乘上常数。直接在 $\Delta_m=0$ 上用 $I=G+\mathcal B$，有

$$
\left.\operatorname{pr}^{(3)}X_{\rm sc}(\Delta_m)\right|_{\Delta_m=0}
=(w_I-w_G)G+(w_I-w_{\mathcal B})\mathcal B.
$$

取自由射流 $\ell=0$、$R\ne0$，则 $G=g\rho^{-2}R$、$\mathcal B=g\beta v^{m-1}\rho^{-1}R$。乘以 $\rho^2/(gR)$，得到

$$
(w_I-w_G)+\beta v^{m-1}\rho(w_I-w_{\mathcal B})=0.
$$

固定任意 $v>0$，该式须对开区间内所有 $\rho>0$ 成立，所以常数项与一次项分别为零。由此严格得到

$$
\begin{aligned}
w_I=w_G&\iff3a_\phi-2a_t-a_s=0,\\
w_I=w_{\mathcal B}&\iff(3-m)(a_\phi-a_t)=0.
\end{aligned}
\tag{3.7}
$$

$m\ne3$ 时，对角标度只有 $(a_t,a_s,a_\phi)=a_t(1,1,1)$。$m=3$ 时

$$
a_s=3a_\phi-2a_t,
\qquad
(a_t,a_s,a_\phi)
=a_\phi(1,1,1)+(a_t-a_\phi)(1,-2,0).
$$

选取第二个基方向 $a_\phi=0,a_t=1$，便有 $a_s=-2$。对任意点函数 $f$，

$$
\left.\frac d{d\epsilon}\right|_0
f(e^\epsilon t,e^{-2\epsilon}s,\phi)
=t f_{,t}-2s f_{,s},
$$

因此生成元就是 $X_5=t\partial_t-2s\partial_s$。这里的 $1$ 是非零方向的归一化，$-2$ 来自 (3.7) 的线性约束，而不是从 $\sigma=st^2$ 猜回来的。

**分类范围。** 这一权重计算只分类对角标度。它不能推出所有 $m\ne3$ 的完整点对称代数都为四维。例如 $m=1$ 时，(1.6) 不含 $v=\phi_t$；变换 $\bar\phi=\phi+\epsilon t$ 只改变 $v$，故 $t\partial_\phi$ 也是点对称，在维持 $\phi_t>0$ 的局部参数范围内成立。

## 单元 4：李代数、伴随作用与一维最优系统

### 4.1 李括号与子代数

**定义。** 对向量场 $A,B$，李括号由 $[A,B](f)=A(Bf)-B(Af)$ 定义。若 $A=A^i\partial_i$、$B=B^i\partial_i$，则

$$
[A,B]=(A^j\partial_jB^i-B^j\partial_jA^i)\partial_i.
$$

例如 $X_1$ 对 $X_5$ 的 $t$ 系数求导得到 $1$，$X_5$ 对 $X_1$ 的常系数求导得到 $0$，故 $[X_1,X_5]=X_1$。又 $X_2(-2s)=-2$，故 $[X_2,X_5]=-2X_2$。其余逐项计算得到完整表：

| $[\text{行},\text{列}]$ | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $X_5$ |
|---|---|---|---|---|---|
| $X_1$ | $0$ | $0$ | $0$ | $X_1$ | $X_1$ |
| $X_2$ | $0$ | $0$ | $0$ | $X_2$ | $-2X_2$ |
| $X_3$ | $0$ | $0$ | $0$ | $X_3$ | $0$ |
| $X_4$ | $-X_1$ | $-X_2$ | $-X_3$ | $0$ | $0$ |
| $X_5$ | $-X_1$ | $2X_2$ | $0$ | $0$ | $0$ |

**文献修正。** 文献 [3] Table 1 末行前两项应满足反对称性，分别为 $-X_1$、$2X_2$。

对这些向量场取常实系数线性组合所得空间，记为 $\mathfrak g$。它在括号下封闭，构成李代数。子空间 $\mathfrak h\subseteq\mathfrak g$ 若也在括号下封闭，称为李子代数。任意非零 $Z$ 的一维张成空间 $\langle Z\rangle$ 都是子代数，因为 $[Z,Z]=0$。

### 4.2 为什么需要一维最优系统

每个一维子代数给出一种不变解约化。若两个子群共轭，它们的不变解族可由原方程的对称变换相互映射，逐个重算通常重复。这里“最优”指在指定等价关系下，每一共轭类只保留一个代表；它不表示某个解在误差、稳定性或物理效果上最优。[1,3]

本文采用连通局部群作用：$g$ 是 $X_1,\ldots,X_5$ 的局部流的复合。两个非零生成元若满足

$$
\widetilde Z=\lambda\mathcal A_g Z,
\qquad\lambda\in\mathbb R\setminus\{0\},
$$

则视为同一子代数共轭类。允许 $\lambda$ 是因为 $Z$ 与非零倍数生成同一个一维方向。本文不把可能存在的非连通离散对称额外加入等价关系；正坐标卡上的平移仅在重叠的局部区域内使用。

### 4.3 伴随作用的定义、符号与完整表

设 $\Gamma^A_\epsilon$ 是 $A$ 的流。采用向量场前推约定

$$
\mathcal A_{A,\epsilon}B=(\Gamma^A_\epsilon)_*B,
\qquad
(\mathcal A_{A,\epsilon}B)_q
=d\Gamma^A_\epsilon\big|_{\Gamma^A_{-\epsilon}(q)}
B_{\Gamma^A_{-\epsilon}(q)}.
$$

在该约定下，$\left.d\mathcal A_{A,\epsilon}B/d\epsilon\right|_0=-[A,B]$，所以

$$
\mathcal A_{A,\epsilon}B
=B-\epsilon[A,B]+\frac{\epsilon^2}{2!}[A,[A,B]]
-\frac{\epsilon^3}{3!}[A,[A,[A,B]]]+\cdots.
\tag{4.1}
$$

这与 [1] 及文献 [3] 所用负号展开一致。若改用逆流前推，参数符号相反，但等价类不变。

例如 $[X_1,X_4]=X_1$，第二次括号为零，于是 $\mathcal A_{X_1,\epsilon}X_4=X_4-\epsilon X_1$。也可直接核验：平移后目标坐标为 $\bar t=t+\epsilon$，原 $X_4$ 的 $t$ 系数在目标坐标中为 $\bar t-\epsilon$。

又因 $[X_5,X_2]=2X_2$，嵌套括号依次为 $2^jX_2$，所以

$$
\mathcal A_{X_5,\epsilon}X_2
=\left[1-2\epsilon+\frac{(2\epsilon)^2}{2!}-\cdots\right]X_2
=e^{-2\epsilon}X_2.
$$

同理求得所有表项：

| $\mathcal A_{\text{行},\epsilon}(\text{列})$ | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $X_5$ |
|---|---|---|---|---|---|
| $X_1$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_1$ | $X_5-\epsilon X_1$ |
| $X_2$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_2$ | $X_5+2\epsilon X_2$ |
| $X_3$ | $X_1$ | $X_2$ | $X_3$ | $X_4-\epsilon X_3$ | $X_5$ |
| $X_4$ | $e^\epsilon X_1$ | $e^\epsilon X_2$ | $e^\epsilon X_3$ | $X_4$ | $X_5$ |
| $X_5$ | $e^\epsilon X_1$ | $e^{-2\epsilon}X_2$ | $X_3$ | $X_4$ | $X_5$ |

核读的 v3 原文 Table 2 中，“行 $X_2$、列 $X_3$”已经是 $X_3$，该项不列为印刷错误。

### 4.4 分三种情形完成共轭分类

令 $Z=a_1X_1+a_2X_2+a_3X_3+a_4X_4+a_5X_5\ne0$。由上表，三个平移依次作用为

$$
\begin{aligned}
a_1&\mapsto a_1-\epsilon_1(a_4+a_5),\\
a_2&\mapsto a_2-\epsilon_2(a_4-2a_5),\\
a_3&\mapsto a_3-\epsilon_3a_4.
\end{aligned}
\tag{4.2}
$$

两个标度作用为

$$
(a_1,a_2,a_3)\mapsto(e^{r+q}a_1,e^{r-2q}a_2,e^ra_3).
\tag{4.3}
$$

所有括号均落在平移理想 $\langle X_1,X_2,X_3\rangle$，故 $(a_4,a_5)$ 在伴随作用下不变；整体重标度 $\lambda$ 只使它同时乘以 $\lambda$。分母为零的情形必须单列。

**情形 A：$a_4\ne0$。** 先除以 $a_4$，此后各 $a_i$ 表示归一化后的系数，令 $\alpha=a_5/a_4$。

若 $\alpha\ne-1,1/2$，取

$$
\epsilon_1=\frac{a_1}{1+\alpha},\qquad
\epsilon_2=\frac{a_2}{1-2\alpha},\qquad
\epsilon_3=a_3,
$$

三个平移系数全为零，代表元为 $X_4+\alpha X_5$。

若 $\alpha=-1$，(4.2) 第一式不再改变 $a_1$；取 $\epsilon_2=a_2/3$、$\epsilon_3=a_3$，保留 $a_1X_1$。若 $a_1\ne0$，再取 (4.3) 的 $q=0,r=-\log|a_1|$，将其变成符号 $\nu$；若 $a_1=0$，令 $\nu=0$。于是得到 $X_4-X_5+\nu X_1$，其中 $\nu=0,\pm1$。正因子不能改变该剩余系数的符号。

若 $\alpha=1/2$，第二式不再改变 $a_2$；取 $\epsilon_1=2a_1/3$、$\epsilon_3=a_3$。若 $a_2\ne0$，取 $q=0,r=-\log|a_2|$；否则保留零值。得到 $X_4+\tfrac12X_5+\nu X_2$，$\nu=0,\pm1$。

**情形 B：$a_4=0,a_5\ne0$。** 先除以 $a_5$，令 $a_5=1$。取 $\epsilon_1=a_1$、$\epsilon_2=-a_2/2$ 可消去 $X_1,X_2$，但 $a_3$ 不受 (4.2) 影响。若 $a_3\ne0$，取 $r=-\log|a_3|$；若 $a_3=0$，保留零值。得到 $X_5+\nu X_3$，$\nu=0,\pm1$。特别地，不能因为 $[X_3,X_5]=0$ 就删除非零的 $a_3$；该交换关系恰好说明相应平移无法删除它。

例如 $Z=X_5+aX_1+dX_2=(t+a)\partial_t+(-2s+d)\partial_s$，取 $\epsilon_1=a,\epsilon_2=-d/2$ 后，(4.2) 给出两个系数 $a-a=0$、$d+2(-d/2)=0$，故与 $X_5$ 共轭。等价地，平移坐标 $\widehat t=t+a$、$\widehat s=s-d/2$ 将它直接写成 $\widehat t\partial_{\widehat t}-2\widehat s\partial_{\widehat s}$。这说明最优系统如何删除仅由坐标原点平移造成的重复约化。

**情形 C：$a_4=a_5=0$。** 平移伴随作用恒等，标度作用保持三个坐标的零或非零状态。

若只有一个分量非零，得到 $X_1,X_2,X_3$。若恰有两个分量非零，先归一化一个分量为 $1$，另一个分量的比值分别满足

$$
\frac{a_2}{a_1}\mapsto e^{-3q}\frac{a_2}{a_1},\qquad
\frac{a_3}{a_1}\mapsto e^{-q}\frac{a_3}{a_1},\qquad
\frac{a_3}{a_2}\mapsto e^{2q}\frac{a_3}{a_2}.
$$

故只留下相对符号，得到 $X_1\pm X_2$、$X_1\pm X_3$、$X_2\pm X_3$。

若三个分量全非零，先设 $a_1=1$，记归一化后的比值为 $r_2=a_2/a_1$、$r_3=a_3/a_1$。取 $q=\log|r_3|$ 后，第三分量为 $\varepsilon=\operatorname{sgn}(r_3)$，第二分量为

$$
k_o=\frac{r_2}{|r_3|^3}\ne0.
$$

于是代表元为 $X_1+k_oX_2+\varepsilon X_3$，$\varepsilon=\pm1$。这里 $k_o$ 是轨道分类参数，与输沙常数 $\kappa$ 不同；$\varepsilon$ 是离散符号，与群参数 $\epsilon$ 不同。

**命题：连通伴随作用下的完整一维最优系统。**

| 分支 | 一维子代数代表及参数 |
|---|---|
| 非共振标度 | $\langle X_4+\alpha X_5\rangle$，$\alpha\in\mathbb R\setminus\{-1,1/2\}$ |
| 第一共振标度 | $\langle X_4-X_5+\nu X_1\rangle$，$\nu=0,\pm1$ |
| 第二共振标度 | $\langle X_4+\tfrac12X_5+\nu X_2\rangle$，$\nu=0,\pm1$ |
| 纯 $X_5$ 标度部分 | $\langle X_5+\nu X_3\rangle$，$\nu=0,\pm1$ |
| 单分量平移 | $\langle X_1\rangle$、$\langle X_2\rangle$、$\langle X_3\rangle$ |
| 双分量平移 | $\langle X_1+\varepsilon X_2\rangle$、$\langle X_1+\varepsilon X_3\rangle$、$\langle X_2+\varepsilon X_3\rangle$，$\varepsilon=\pm1$ |
| 三分量平移 | $\langle X_1+k_oX_2+\varepsilon X_3\rangle$，$k_o\ne0$，$\varepsilon=\pm1$ |

**完备性与不重复的理由。** 非零标度对 $(a_4,a_5)$ 的射影比值区分 A、B 及不同 $\alpha$；(4.2) 精确删除非共振平移方向。共振剩余量只受正标度，零状态和符号保留。纯平移分支的支撑集不变；三个非零分量时，$\operatorname{sgn}(a_3/a_1)$ 和 $a_1^2a_2/a_3^3=\varepsilon k_o$ 是不变量，反之上述归一化给出唯一的 $k_o,\varepsilon$。因此各分支覆盖全部情形，并在声明的参数范围内不重复。

原文较短的列表不能代替这一连通作用分类：非零共振剩余项及 $X_2,X_3$ 混合平移需要补入。复现式 (27) 本身只需选取已验证的 $\langle X_5\rangle$，无需先完成全部代表的约化。

### 4.5 从代表元得到相似变换

**定义。** 点不变量 $I(t,s,\phi)$ 满足 $Z(I)=0$。在三维点空间的正则一维轨道附近，需要两个函数独立的点不变量。若图像投影满足横截性条件，才可把它们组织成不变解表达式。

例如 $Z=X_4+\alpha X_5$ 的流满足

$$
\dot{\bar t}=(1+\alpha)\bar t,\quad
\dot{\bar s}=(1-2\alpha)\bar s,\quad
\dot{\bar\phi}=\bar\phi.
$$

在 $t>0,s>0$ 且 $\alpha\ne-1$ 时，

$$
Z\left(\log s-\frac{1-2\alpha}{1+\alpha}\log t\right)=0,
\qquad
Z\left(\phi t^{-1/(1+\alpha)}\right)=0.
$$

两不变量由此得到。下表集中列出与本文有关的代表；它是相似形式表，不能代替代回 PDE 后的剖面方程。

| 生成元 $Z$ | 自变量不变量 | 因变量不变量 | 不变图像形式 |
|---|---|---|---|
| $X_5$ | $st^2$ | $\phi$ | $\phi=F(st^2)$ |
| $X_5+\nu X_3$ | $st^2$ | $\phi-\nu\log t$ | $\phi=\nu\log t+F(st^2)$ |
| $X_4+\alpha X_5$，$\alpha\ne-1$ | $s t^{(2\alpha-1)/(1+\alpha)}$ | $\phi t^{-1/(1+\alpha)}$ | $\phi=t^{1/(1+\alpha)}\Phi(s t^{(2\alpha-1)/(1+\alpha)})$ |
| $X_4-X_5$ | $t$ | $\phi s^{-1/3}$ | $\phi=s^{1/3}\Phi(t)$ |
| $X_4-X_5+\nu X_1$，$\nu=\pm1$ | $s e^{-3t/\nu}$ | $\phi e^{-t/\nu}$ | $\phi=e^{t/\nu}\Phi(s e^{-3t/\nu})$ |
| $X_4+\tfrac12X_5+\nu X_2$ | $s-\tfrac{2\nu}3\log t$ | $\phi t^{-2/3}$ | $\phi=t^{2/3}\Phi(s-\tfrac{2\nu}3\log t)$ |
| $X_1+\alpha X_2+\gamma X_3$ | $s-\alpha t$ | $\phi-\gamma t$ | $\phi=\gamma t+\Phi(s-\alpha t)$ |
| $X_2+\gamma X_3$ | $t$ | $\phi-\gamma s$ | $\phi=\gamma s+\Phi(t)$ |

第一、二个共振分支分别直接代入 $Z$ 验证，例如

$$
(\nu\partial_t+3s\partial_s+\phi\partial_\phi)(s e^{-3t/\nu})
=-3s e^{-3t/\nu}+3s e^{-3t/\nu}=0.
$$

又 $Z=\tfrac32t\partial_t+\nu\partial_s+\phi\partial_\phi$ 时，

$$
Z\left(s-\frac{2\nu}3\log t\right)=\nu-\frac{2\nu}3\frac32=0.
$$

所有形式仍须检查 $\phi_s>0,\phi_t>0$。例如单独 $X_1$ 的不变图像强制 $\phi_t=0$，单独 $X_2$ 强制 $\phi_s=0$，均不属于本文正性分支；$X_3$ 的竖直平移不存在保持不变的单值函数图像。代数分类存在某个子代数，并不保证该分支存在符合给定域条件的不变解。

## 单元 5：群轨道、不变图像与逐项链式求导

### 5.1 “积分群流”与 group orbit 的准确含义

已知 $X_5=t\partial_t-2s\partial_s$ 后，取固定初始点 $q_0=(t_0,s_0,\phi_0)$。流的定义要求轨道上的速度等于该点的向量场值，因此运动点 $\Gamma_\epsilon(q_0)=(\bar t(\epsilon),\bar s(\epsilon),\bar\phi(\epsilon))$ 满足初值问题

$$
\frac{d\bar t}{d\epsilon}=\bar t,\qquad
\frac{d\bar s}{d\epsilon}=-2\bar s,\qquad
\frac{d\bar\phi}{d\epsilon}=0,
\qquad
(\bar t(0),\bar s(0),\bar\phi(0))=(t_0,s_0,\phi_0).
$$

分别积分：

$$
\begin{aligned}
\frac{d\bar t}{\bar t}=d\epsilon
&\implies\log(\bar t/t_0)=\epsilon
\implies\bar t=e^\epsilon t_0,\\
\frac{d\bar s}{\bar s}=-2d\epsilon
&\implies\log(\bar s/s_0)=-2\epsilon
\implies\bar s=e^{-2\epsilon}s_0,\\
d\bar\phi=0&\implies\bar\phi=\phi_0.
\end{aligned}
$$

所以

$$
\boxed{\Gamma_\epsilon(t_0,s_0,\phi_0)
=(e^\epsilon t_0,e^{-2\epsilon}s_0,\phi_0).}
\tag{5.1}
$$

此处“积分群流”就是解这个初值问题。若先明确把 $t(\epsilon)$ 等定义为轨迹坐标，也可以不用横线；横线的作用是避免把固定初始坐标与运动点混淆，不能把未加横线本身判为数学错误。

**定义。** 通过 $q_0$ 的群轨道是所有允许群参数所产生点的集合

$$
\mathcal O(q_0)=\{\Gamma_\epsilon(q_0):\epsilon\in\mathbb R\}
$$

（若另有限定邻域，则只取流留在该邻域的局部部分）。对本标度，$t,s>0$ 在所有有限 $\epsilon$ 下保持，且

$$
\bar s\bar t^2=(e^{-2\epsilon}s_0)(e^\epsilon t_0)^2=s_0t_0^2,
\qquad\bar\phi=\phi_0.
$$

因此三维轨道由两个等式 $st^2=s_0t_0^2$、$\phi=\phi_0$ 标记。只给 $st^2$ 只能标记投影到 $(t,s)$ 平面的轨道，不能区分不同 $\phi_0$ 的三维轨道。

例如从 $(1,1,\phi_0)$ 出发：

| 群参数 | 轨道上的点 | $st^2$ |
|---|---|---|
| $-\log2$ | $(1/2,4,\phi_0)$ | $1$ |
| $0$ | $(1,1,\phi_0)$ | $1$ |
| $\log2$ | $(2,1/4,\phi_0)$ | $1$ |

这里 $\epsilon$ 是变换参数，$t$ 是被变换的点坐标；该运动不是物理场随时间的演化。

### 5.2 射流权重再核验 $X_5$

在此标度下，$D_{\bar t}=e^{-\epsilon}D_t$、$D_{\bar s}=e^{2\epsilon}D_s$，故 $\phi_{t^is^j}$ 权重为 $2j-i$。因此

| 射流坐标 | $v$ | $\rho$ | $a$ | $\ell$ | $c$ | $T$ | $U$ | $R$ | $V$ |
|---|---|---|---|---|---|---|---|---|---|
| 权重 | $-1$ | $2$ | $-2$ | $1$ | $4$ | $-3$ | $0$ | $3$ | $6$ |

记 $\mathcal A_m=D_tH$、$\mathcal B_m=gD_sJ$，则权重分别为 $-1$、$2-m$。微分有限变换得到全射流上的精确恒等式

$$
\operatorname{pr}^{(3)}X_5(\Delta_m)
=-\mathcal A_m-(2-m)\mathcal B_m
=-\Delta_m+(m-3)\mathcal B_m.
$$

$m=3$ 时恰为 $-\Delta_3$。这与单元 3 的完整确定方程结果相符。

### 5.3 顺直坐标与图像相切条件

为把运动方向变成坐标轴，选择沿轨道增加速率为 $1$ 的 $y$，以及沿轨道不变的 $\sigma,w$。定义

$$
y=\log t,\qquad\sigma=st^2,\qquad w=\phi.
$$

有 $X_5(y)=1$、$X_5(\sigma)=X_5(w)=0$，且

$$
\det\frac{\partial(y,\sigma,w)}{\partial(t,s,\phi)}=t>0,
\qquad(t,s,\phi)=(e^y,\sigma e^{-2y},w).
$$

故这确为当前区域的光滑坐标变换。坐标链式法则给出

$$
\partial_t=\frac1t\partial_y+\frac{2\sigma}t\partial_\sigma,
\qquad\partial_s=t^2\partial_\sigma,
$$

从而

$$
X_5=t\left(\frac1t\partial_y+\frac{2\sigma}t\partial_\sigma\right)
-2st^2\partial_\sigma=\partial_y.
$$

$w=\phi$ 是点不变量，不代表任意函数图像都不变。设某图像为 $\phi=u(t,s)$，其切向量为 $\partial_t+u_t\partial_\phi$、$\partial_s+u_s\partial_\phi$。一般生成元 $X$ 位于该切平面，当且仅当

$$
X=\tau(\partial_t+u_t\partial_\phi)
+\xi(\partial_s+u_s\partial_\phi),
\quad\text{即}\quad Q_X:=\eta-\tau u_t-\xi u_s=0.
$$

这就是不变曲面条件。对 $X_5$，

$$
Q_{X_5}=-t u_t+2s u_s=-w_y=0.
$$

因此在新图像坐标中 $w$ 与 $y$ 无关，得到

$$
\boxed{\phi(t,s)=F(\sigma),\qquad\sigma=st^2.}
\tag{5.2}
$$

几何上，不变图像是整条群轨道的并；$F$ 为每条投影轨道 $st^2=\sigma$ 指定一个函数值。$F$ 还须满足代回 PDE 后的 ODE。

也可直接检查图像变换：$\bar u(\bar t,\bar s)=u(e^{-\epsilon}\bar t,e^{2\epsilon}\bar s)$。若 $u=F(st^2)$，则括号中的乘积仍是 $\bar s\bar t^2$，因而新旧图像相同。

### 5.4 全部一至三阶导数的逐项计算

定义 $p=F'(\sigma)$、$q=F''(\sigma)$、$r=F'''(\sigma)$，此处撇号均表示 $d/d\sigma$。基本链式法则为

$$
\sigma_t=2st=\frac{2\sigma}t,\qquad\sigma_s=t^2,
\qquad D_tK(\sigma)=\frac{2\sigma}tK',\quad D_sK(\sigma)=t^2K'.
$$

先算一阶：

$$
\phi_t=p\sigma_t=\frac{2\sigma p}t,
\qquad\phi_s=p\sigma_s=t^2p.
$$

显式因子 $t$ 也必须求导。二阶分别为

$$
\begin{aligned}
\phi_{tt}
&=-\frac{2\sigma p}{t^2}
+\frac2t(p+\sigma q)\frac{2\sigma}t
=\frac{2\sigma p+4\sigma^2q}{t^2},\\
\phi_{ts}
&=\frac2t(p+\sigma q)t^2=2t(p+\sigma q),\\
\phi_{ss}&=t^2q\sigma_s=t^4q.
\end{aligned}
$$

为计算 $\phi_{ttt}$，先记 $K=2\sigma p+4\sigma^2q$，于是 $K'=2p+10\sigma q+4\sigma^2r$。因此

$$
\begin{aligned}
\phi_{ttt}
&=-2t^{-3}K+t^{-2}K'\frac{2\sigma}t\\
&=t^{-3}\big[-4\sigma p-8\sigma^2q
+4\sigma p+20\sigma^2q+8\sigma^3r\big]\\
&=\frac{12\sigma^2q+8\sigma^3r}{t^3},\\
\phi_{tts}&=t^{-2}K't^2=2p+10\sigma q+4\sigma^2r,\\
\phi_{tss}&=D_s[2t(p+\sigma q)]
=2t(2q+\sigma r)t^2=2t^3(2q+\sigma r),\\
\phi_{sss}&=D_s(t^4q)=t^4r\,t^2=t^6r.
\end{aligned}
\tag{5.3}
$$

正性条件变为 $\sigma>0$、$p>0$，因为 $\phi_s=t^2p$、$\phi_t=2\sigma p/t$。

## 单元 6：三阶剖面方程与对称性的继承

### 6.1 保留散度结构的精确回拉

在 $m=3$ 下，先代入两个散度括号内部，定义剖面表达式

$$
\begin{aligned}
\mathcal A(\sigma)
&=(t^2p)\frac{2\sigma p+4\sigma^2q}{t^2}
-g\frac{t^4q}{t^4p^2}
=2\sigma p^2+4\sigma^2pq-\frac{gq}{p^2},\\
\phi_t^2\frac{\phi_{ts}}{\phi_s}
&=\frac{4\sigma^2p^2}{t^2}\frac{2t(p+\sigma q)}{t^2p}
=t^{-3}\mathcal B(\sigma),\\
\mathcal B(\sigma)&=8\sigma^2p(p+\sigma q).
\end{aligned}
$$

逐项求导：

$$
\begin{aligned}
\mathcal A'
&=2p^2+4\sigma pq+8\sigma pq+4\sigma^2(q^2+pr)
-\frac{gr}{p^2}+\frac{2gq^2}{p^3}\\
&=2p^2+12\sigma pq+4\sigma^2(q^2+pr)
-\frac{gr}{p^2}+\frac{2gq^2}{p^3},\\
\mathcal B'
&=D_\sigma(8\sigma^2p^2+8\sigma^3pq)\\
&=16\sigma p^2+16\sigma^2pq+24\sigma^2pq
+8\sigma^3(q^2+pr)\\
&=16\sigma p^2+40\sigma^2pq+8\sigma^3(q^2+pr).
\end{aligned}
$$

因此 $D_t\mathcal A=(2\sigma/t)\mathcal A'$，$D_s(t^{-3}\mathcal B)=t^{-1}\mathcal B'$。收集 $r,q^2,q,1$ 四类项：

$$
\begin{aligned}
2\sigma\mathcal A'-b\mathcal B'
={}&\left[8(1-b)\sigma^3p-\frac{2g\sigma}{p^2}\right]r\\
&+\left[8(1-b)\sigma^3+\frac{4g\sigma}{p^3}\right]q^2\\
&+(24-40b)\sigma^2pq+(4-16b)\sigma p^2.
\end{aligned}
$$

定义

$$
\boxed{
\begin{aligned}
\mathcal R_3[F]={}&p\big[g+4(b-1)\sigma^2p^3\big]r
+\big[4(b-1)\sigma^2p^3-2g\big]q^2\\
&+(20b-12)\sigma p^4q+(8b-2)p^5.
\end{aligned}}
\tag{R3}
$$

得到主线最重要的精确回拉恒等式

$$
\boxed{
\left.\Delta_3[\phi]\right|_{\phi=F(st^2)}
=\frac1t(2\sigma\mathcal A'-b\mathcal B')
=-\frac{2\sigma}{tp^3}\mathcal R_3[F].}
\tag{6.1}
$$

在当前域中乘子非零，故 PDE 的这类不变解与 $\mathcal R_3=0$ 的正斜率剖面严格对应。该式是从原标量方程重新推导的结果，不能先把原文式 (25)–(26) 当作已成立的中间式。

### 6.2 正规化子与可投影性

约化后点空间为 $(\sigma,F)$。要从原对称 $A$ 得到此空间上的向量场，必须先保证 $A$ 作用于轨道不变量后仍给出轨道不变量。

**定义。** $\mathfrak h_5=\langle X_5\rangle$ 在 $\mathfrak g$ 中的正规化子为

$$
\mathfrak n_{\mathfrak g}(\mathfrak h_5)
=\{A\in\mathfrak g:[A,\mathfrak h_5]\subseteq\mathfrak h_5\}.
$$

这是保证下降到商空间的充分条件：若 $X_5I=0$ 且 $[X_5,A]=\lambda X_5$，则

$$
X_5(AI)=[X_5,A]I+A(X_5I)=\lambda X_5I=0.
$$

一般光滑向量场的可投影条件是保持轨道分布，即 $[X_5,A]$ 为 $X_5$ 的光滑函数倍；不能无条件把它等同于某个有限维代数的正规化子条件。在本五维代数内，直接计算

$$
[A,X_5]=a_1X_1-2a_2X_2,
\qquad A=\sum_{i=1}^5a_iX_i.
$$

该向量场在开集上沿 $X_5$ 当且仅当 $a_1=a_2=0$，所以这里恰得到

$$
\mathfrak n_{\mathfrak g}(\mathfrak h_5)
=\operatorname{span}\{X_3,X_4,X_5\}.
$$

例如 $X_1(\sigma)=2st=2\sigma/t$ 仍依赖已消去的 $t$，因而不能在 $(\sigma,F)$ 上定义相应投影向量场。

### 6.3 商投影的前推计算

为避免与原丛投影混淆，将轨道商投影记为 $\Pi(t,s,\phi)=(st^2,\phi)=(\sigma,F)$。若 $A$ 可投影，定义

$$
\Pi_*A=A(\sigma)\partial_\sigma+A(\phi)\partial_F.
$$

于是

$$
\begin{aligned}
X_3(\sigma)&=0,& X_3(\phi)&=1,
& Z=\Pi_*X_3&=\partial_F,\\
X_4(\sigma)&=t(2st)+s(t^2)=3\sigma,&X_4(\phi)&=\phi=F,
& Y=\Pi_*X_4&=3\sigma\partial_\sigma+F\partial_F,\\
\Pi_*X_5&=0.
\end{aligned}
$$

$Z,Y$ 是剖面 ODE 的继承对称；正规化子除以被约化方向后对应这两个方向。特别地，$[Y,Z]=-Z$。随后 $Y$ 可在先按 $Z$ 商降阶后继续下降，因为它保持 $\langle Z\rangle$，并不要求 $Y,Z$ 交换。交换性是充分条件，绝非必要条件。

**文献修正。** 原文第 7 页相应向量场的第二项应为 $F\partial_F$，不是把两个分量都写在 $\partial_\sigma$ 方向。

## 单元 7：两次 ODE 商降阶与原始不变量 $M$ 的方程

### 7.1 商降阶与额外不变解条件的区别

PDE 阶段施加 $Q_{X_5}=0$，选出原 PDE 的一类特殊解。ODE 阶段的目标是利用对称性消除解曲线中的等价信息，同时保留通过积分可恢复的常数；这称为商降阶。

不能把每次 ODE 降阶都解释成再施加一次 $Q=0$。例如 $Z=\partial_F$ 的不变曲面条件是 $Q_Z=1=0$，不存在这样的函数图像；但竖直平移仍能通过斜率不变量使一般剖面 ODE 降一阶。[1-2]

### 7.2 第一次降阶：斜率是平移的微分不变量

群流 $F\mapsto F+\epsilon$ 保持 $\sigma$、$F'$、$F''$ 不变。$\mathcal R_3$ 不显含 $F$，所以定义

$$
\mu(\sigma)=\frac{dF}{d\sigma},\qquad
\mu'=F'',\qquad\mu''=F'''.
$$

这把三阶方程精确改写成二阶方程

$$
\boxed{
\begin{aligned}
\mathcal R_2[\mu]={}&
\mu\big[g+4(b-1)\sigma^2\mu^3\big]\mu''
+\big[4(b-1)\sigma^2\mu^3-2g\big](\mu')^2\\
&+(20b-12)\sigma\mu^4\mu'
+(8b-2)\mu^5=0.
\end{aligned}}
\tag{R2}
$$

由任一局部 $\mu$ 解可恢复

$$
F(\sigma)=F_*+\int_{\sigma_*}^{\sigma}\mu(z)\,dz.
$$

这里 $F_*$ 恢复被平移商消去的一个常数；并未强制 $F$ 为平移不变图像。

### 7.3 从点空间前推到斜率空间：必须先延拓

已知 $Y=3\sigma\partial_\sigma+F\partial_F$。它的有限流为 $\bar\sigma=e^{3\epsilon}\sigma$、$\bar F=e^\epsilon F$，所以

$$
\bar\mu=\frac{d\bar F}{d\bar\sigma}=e^{-2\epsilon}\mu.
$$

也可用延拓公式算出斜率分量：

$$
\eta^{[\sigma]}=D_\sigma(F)-\mu D_\sigma(3\sigma)
=\mu-3\mu=-2\mu.
$$

消去 $F$ 后，二阶方程的继承生成元是

$$
Y_1=3\sigma\partial_\sigma-2\mu\partial_\mu.
$$

为构造涉及 $\mu'$ 的不变量，还须将 $Y_1$ 延拓一次。暂记 $h=\mu'=d\mu/d\sigma$，则

$$
\eta_1^{[\sigma]}=D_\sigma(-2\mu)-hD_\sigma(3\sigma)
=-2h-3h=-5h,
$$

故

$$
\operatorname{pr}^{(1)}Y_1
=3\sigma\partial_\sigma-2\mu\partial_\mu-5h\partial_h.
\tag{7.1}
$$

### 7.4 微分不变量的定义与求解

**定义。** 若某射流函数 $I$ 满足 $\operatorname{pr}^{(k)}Y_1(I)=0$，则称其为 $Y_1$ 的 $k$ 阶微分不变量。它编码沿同一对称轨道不变的导数信息。

由流 $\bar\sigma=e^{3\epsilon}\sigma$、$\bar\mu=e^{-2\epsilon}\mu$、$\bar h=e^{-5\epsilon}h$，或由特征比

$$
\frac{d\sigma}{3\sigma}=\frac{d\mu}{-2\mu}=\frac{dh}{-5h},
$$

得到两个基本不变量

$$
\boxed{\Sigma=\sigma^{2/3}\mu,
\qquad M=\sigma^{5/3}\mu'.}
\tag{7.2}
$$

直接作用 (7.1) 核验：

$$
\begin{aligned}
Y_1(\sigma^{2/3}\mu)
&=3\sigma\frac23\sigma^{-1/3}\mu-2\mu\sigma^{2/3}=0,\\
\operatorname{pr}^{(1)}Y_1(\sigma^{5/3}h)
&=3\sigma\frac53\sigma^{2/3}h-5h\sigma^{5/3}=0.
\end{aligned}
$$

由于 $\sigma>0$，这些实幂光滑。固定 $\sigma$，对 $(\mu,h)$ 的雅可比为 $\sigma^{2/3}\sigma^{5/3}=\sigma^{7/3}>0$，故两不变量函数独立。若再加入轨道坐标 $y_1=\tfrac13\log\sigma$，完整三维雅可比为 $\sigma^{4/3}/3\ne0$。

然而，“不变量函数独立”与“沿某条解可以用 $\Sigma$ 作自变量”是不同条件。沿解求导，定义

$$
\begin{aligned}
\frac{d\Sigma}{d\sigma}
&=\frac23\sigma^{-1/3}\mu+\sigma^{2/3}\mu'\\
&=\frac1\sigma\left(\frac23\Sigma+M\right)
=\frac W\sigma,\qquad
W:=M+\frac23\Sigma.
\end{aligned}
\tag{7.3}
$$

**局部坐标限制。** 只有在 $W\ne0$ 的解段上，才能将 $M$ 写成 $M(\Sigma)$。整段 $W=0$ 的解要另行处理，见单元 10。

### 7.5 所有导数替换的链式展开

由定义，

$$
\mu=\sigma^{-2/3}\Sigma,
\qquad\mu'=\sigma^{-5/3}M.
$$

这里 $\Sigma,M$ 是沿解变化的量，不能把 $M$ 对 $\sigma$ 的变化漏掉：

$$
\begin{aligned}
\mu''
&=\frac d{d\sigma}(\sigma^{-5/3}M(\Sigma(\sigma)))\\
&=-\frac53\sigma^{-8/3}M
+\sigma^{-5/3}M_{,\Sigma}\frac{d\Sigma}{d\sigma}\\
&=\sigma^{-8/3}\left(WM_{,\Sigma}-\frac53M\right).
\end{aligned}
\tag{7.4}
$$

### 7.6 代回二阶方程并收集 $M$ 的各次幂

为使每个系数可追溯，定义

$$
D(\Sigma)=g+4(b-1)\Sigma^3,
\qquad A(\Sigma)=4(b-1)\Sigma^3-2g.
$$

因为 $\sigma^2\mu^3=\Sigma^3$，$\mathcal R_2$ 的四项分别成为

$$
\begin{aligned}
\mu[g+4(b-1)\sigma^2\mu^3]\mu''
&=\sigma^{-10/3}\Sigma D\left(WM_{,\Sigma}-\frac53M\right),\\
[4(b-1)\sigma^2\mu^3-2g](\mu')^2
&=\sigma^{-10/3}A M^2,\\
(20b-12)\sigma\mu^4\mu'
&=(20b-12)\sigma^{1-8/3-5/3}\Sigma^4M\\
&=\sigma^{-10/3}(20b-12)\Sigma^4M,\\
(8b-2)\mu^5&=\sigma^{-10/3}(8b-2)\Sigma^5.
\end{aligned}
$$

除以共同非零因子 $\sigma^{-10/3}$ 后，$M$ 的一次项系数为

$$
\begin{aligned}
B(\Sigma)
&=(20b-12)\Sigma^4-\frac53\Sigma D\\
&=\left(20b-12-\frac{20}3(b-1)\right)\Sigma^4-\frac{5g}3\Sigma\\
&=\frac\Sigma3\big[8(5b-2)\Sigma^3-5g\big].
\end{aligned}
$$

再定义 $C(\Sigma)=(8b-2)\Sigma^5=2(4b-1)\Sigma^5$。得到完整一阶关系

$$
\boxed{\Sigma D\left(M+\frac23\Sigma\right)M_{,\Sigma}
+AM^2+BM+C=0.}
\tag{I1}
$$

在 $\Sigma>0,D\ne0,W\ne0$ 时，

$$
M_{,\Sigma}=-\frac{AM^2+BM+C}{\Sigma D(M+\tfrac23\Sigma)}.
\tag{7.5}
$$

因此原始不变量 $M=\sigma^{5/3}\mu'$ 满足的是有理一阶方程。不能跳过变量变化就把 (7.5) 写成关于同一 $M$ 的三次多项式方程。

## 单元 8：倒数平移与原式 (27) 的系数

### 8.1 变换的动机、定义与可逆区域

(I1) 的导数项带因子 $W=M+2\Sigma/3$。为把该因子转成能清除分母的幂次，先作平移再取倒数，定义

$$
\boxed{N=\frac1{M+\tfrac23\Sigma},
\qquad M=\frac1N-\frac23\Sigma.}
\tag{8.1}
$$

这是一阶方程因变量的代数变换，并非再使用一个李对称，也没有再次降低微分阶数。变换适用于有限 $M$ 且 $W\ne0$ 的区域；反变换需要有限且非零的 $N$。本单元还取 $\Sigma>0,D\ne0$，以便写成显式正规形。

### 8.2 代入后逐次收集

分别有

$$
M_{,\Sigma}=-\frac{N_{,\Sigma}}{N^2}-\frac23,
\qquad
M^2=\frac1{N^2}-\frac{4\Sigma}{3N}+\frac{4\Sigma^2}9.
$$

代回 (I1)：

$$
\begin{aligned}
0={}&\frac{\Sigma D}{N}
\left(-\frac{N_{,\Sigma}}{N^2}-\frac23\right)
+A\left(\frac1{N^2}-\frac{4\Sigma}{3N}+\frac{4\Sigma^2}9\right)\\
&+B\left(\frac1N-\frac{2\Sigma}3\right)+C\\
={}&-\frac{\Sigma D}{N^3}N_{,\Sigma}
+\frac A{N^2}
+\frac{B-\tfrac43A\Sigma-\tfrac23\Sigma D}{N}
+\frac49A\Sigma^2-\frac23B\Sigma+C.
\end{aligned}
$$

乘 $N^3$ 后按 $N$ 的次数收集：

$$
\begin{aligned}
0={}&-\Sigma D N_{,\Sigma}
+A N
+\left(B-\frac43A\Sigma-\frac23\Sigma D\right)N^2\\
&+\left(\frac49A\Sigma^2-\frac23B\Sigma+C\right)N^3.
\end{aligned}
\tag{8.2}
$$

因此

$$
N_{,\Sigma}=a_3(\Sigma)N^3+a_2(\Sigma)N^2+a_1(\Sigma)N,
$$

其中未经化简的系数为

$$
a_1=\frac A{\Sigma D},\quad
a_2=\frac{B-\tfrac43A\Sigma}{\Sigma D}-\frac23,\quad
a_3=\frac{\tfrac49A\Sigma^2-\tfrac23B\Sigma+C}{\Sigma D}.
\tag{8.3}
$$

特别要保留来自 $d(-2\Sigma/3)/d\Sigma=-2/3$ 的二次系数修正。

### 8.3 三个系数逐项通分

一次系数已经为

$$
a_1=\frac{4(b-1)\Sigma^3-2g}{\Sigma D}.
$$

对二次系数，把分子全部写开：

$$
\begin{aligned}
B-\frac43A\Sigma-\frac23\Sigma D
={}&\frac\Sigma3\big[8(5b-2)\Sigma^3-5g\big]\\
&-\frac\Sigma3\big[16(b-1)\Sigma^3-8g\big]
-\frac\Sigma3\big[8(b-1)\Sigma^3+2g\big]\\
={}&\frac\Sigma3\big[(40b-16-16b+16-8b+8)\Sigma^3
+(-5+8-2)g\big]\\
={}&\frac\Sigma3\big[8(1+2b)\Sigma^3+g\big].
\end{aligned}
$$

三次系数的分子为

$$
\begin{aligned}
\frac49A\Sigma^2-\frac23B\Sigma+C
={}&\frac{\Sigma^2}9\Big[
16(b-1)\Sigma^3-8g
-16(5b-2)\Sigma^3+10g\\
&\hspace{34mm}+18(4b-1)\Sigma^3\Big]\\
={}&\frac{\Sigma^2}9\big[(16b-16-80b+32+72b-18)\Sigma^3+2g\big]\\
={}&\frac{2\Sigma^2}9\big[(4b-1)\Sigma^3+g\big].
\end{aligned}
$$

于是得到第一类 Abel 方程

$$
\boxed{
\begin{aligned}
\frac{dN}{d\Sigma}={}&
\frac{2\Sigma\big[g+(4b-1)\Sigma^3\big]}{9\big[g+4(b-1)\Sigma^3\big]}N^3\\
&+\frac{g+8(1+2b)\Sigma^3}{3\big[g+4(b-1)\Sigma^3\big]}N^2\\
&+\frac{4(b-1)\Sigma^3-2g}{\Sigma\big[g+4(b-1)\Sigma^3\big]}N.
\end{aligned}}
\tag{A27}
$$

恢复 $b=g\beta$，即

$$
\begin{aligned}
\frac{dN}{d\Sigma}={}&
\frac{2\Sigma\big[g+(4g\beta-1)\Sigma^3\big]}
{9\big[g+4(g\beta-1)\Sigma^3\big]}N^3\\
&+\frac{g+8(1+2g\beta)\Sigma^3}
{3\big[g+4(g\beta-1)\Sigma^3\big]}N^2\\
&+\frac{4(g\beta-1)\Sigma^3-2g}
{\Sigma\big[g+4(g\beta-1)\Sigma^3\big]}N.
\end{aligned}
\tag{27*}
$$

**文献修正。** 这些系数与原式 (27) 的三次系数结构一致，但由本稿前面定义推出的因变量必须是 $N=1/(M+2\Sigma/3)$。这给出足以修复该计算链的明确变量替换；它不是对作者原意的断言。

## 单元 9：从 Abel 解恢复三阶剖面与 PDE 解

### 9.1 重构的定义与局部可逆性

设固定 $g>0,\beta>0$，在某个区间内已有 (A27) 的有限解 $N(\Sigma)$，并满足

$$
\Sigma>0,\qquad D(\Sigma)\ne0,\qquad N(\Sigma)\ne0.
$$

选择锚点 $\Sigma_*$、常数 $\sigma_*>0$。由 (7.3) 和 $W=1/N$，有

$$
\frac{d\Sigma}{d\sigma}=\frac1{\sigma N},
\qquad
\frac{d\sigma}{d\Sigma}=\sigma N,
\qquad
\frac{d\log\sigma}{d\Sigma}=N.
$$

积分得到

$$
\boxed{
\sigma(\Sigma)=\sigma_*\exp\left(\int_{\Sigma_*}^{\Sigma}N(z)\,dz\right).}
\tag{9.1}
$$

指数确保 $\sigma>0$，且 $\sigma_{,\Sigma}=\sigma N\ne0$，故可局部反解 $\Sigma=\Sigma(\sigma)$。

### 9.2 恢复斜率与函数值

由 $\mu=\Sigma\sigma^{-2/3}$ 和 $F_{,\sigma}=\mu$，

$$
\frac{dF}{d\Sigma}
=\frac{dF}{d\sigma}\frac{d\sigma}{d\Sigma}
=\Sigma\sigma^{-2/3}\sigma N
=\Sigma\sigma^{1/3}N.
$$

因此

$$
\boxed{
F(\Sigma)=F_*+\int_{\Sigma_*}^{\Sigma}
z\,\sigma(z)^{1/3}N(z)\,dz.}
\tag{9.2}
$$

一致性还可直接核验：

$$
\begin{aligned}
\frac{d\mu}{d\Sigma}
&=\sigma^{-2/3}-\frac23\Sigma\sigma^{-5/3}\sigma N
=\sigma^{-2/3}\left(1-\frac23\Sigma N\right),\\
\frac{d\mu}{d\sigma}
&=\frac{\mu_{,\Sigma}}{\sigma_{,\Sigma}}
=\sigma^{-5/3}\left(\frac1N-\frac23\Sigma\right)
=\sigma^{-5/3}M.
\end{aligned}
$$

这恢复了原始不变量 $M$ 的定义，而不只是形式积分。

### 9.3 回到原变量并计算常数个数

局部反解后，令

$$
\phi(t,s)=F(st^2),\qquad st^2\in\sigma(\text{重构区间}),\quad t>0,s>0.
$$

因为 $\mu=\Sigma\sigma^{-2/3}>0$，便有 $\phi_s=t^2\mu>0$、$\phi_t=2\sigma\mu/t>0$。由 (6.1)，所重构场是固定标量方程 (1.4) 的局部解。

**局部对应命题。** 在 $\sigma>0,\mu>0,D\ne0,W\ne0$ 的剖面解段上，上述变换与重构互逆；每个满足相应域条件的 Abel 解给出一个该类剖面。证明是按 (7.2)–(8.1) 顺向变换，再按 (9.1)–(9.2) 反向恢复，并使用所列非零条件和精确回拉恒等式。

三阶正则剖面的三个自由常数分别是：一阶 Abel 初值 $N(\Sigma_*)=N_*$，以及重构常数 $\sigma_*,F_*$。$\Sigma_*$ 是选定积分锚点，不应再额外算作独立解常数。

给定三阶初值 $F(\sigma_*)=F_*$、$F'(\sigma_*)=p_*>0$、$F''(\sigma_*)=q_*$，转换为

$$
\Sigma_*=\sigma_*^{2/3}p_*,\qquad
M_*=\sigma_*^{5/3}q_*,\qquad
N_*=(M_*+2\Sigma_*/3)^{-1}.
$$

其适用条件为 $D(\Sigma_*)\ne0$、$M_*+2\Sigma_*/3\ne0$。若条件失效，应回到未除式处理；不能宣称 Abel 正规形覆盖全部相似剖面。

## 单元 10：未被 Abel 坐标覆盖的分支与手算例题

### 10.1 整段 $W=0$：常不变量分支

若 $W=M+2\Sigma/3$ 在整个区间上为零，(7.3) 给出 $\Sigma=k$ 常数。由于 $\mu>0,\sigma>0$，必须 $k>0$。于是

$$
\mu=k\sigma^{-2/3},\qquad
\mu'=-\frac23k\sigma^{-5/3},\qquad
\mu''=\frac{10}9k\sigma^{-8/3}.
$$

这时不能使用 $M=M(\Sigma)$。直接代回 (R2)，四项依次为

$$
\begin{aligned}
\mu[g+4(b-1)\sigma^2\mu^3]\mu''
&=\frac{10}9k^2[g+4(b-1)k^3]\sigma^{-10/3},\\
[4(b-1)\sigma^2\mu^3-2g](\mu')^2
&=\frac49k^2[4(b-1)k^3-2g]\sigma^{-10/3},\\
(20b-12)\sigma\mu^4\mu'
&=-\frac23(20b-12)k^5\sigma^{-10/3},\\
(8b-2)\mu^5&=(8b-2)k^5\sigma^{-10/3}.
\end{aligned}
$$

合并 $gk^2$ 和 $k^5$ 的系数：

$$
\begin{aligned}
\mathcal R_2
&=k^2\sigma^{-10/3}\left[
\left(\frac{10}9-\frac89\right)g
+\left(\frac{56}9(b-1)-\frac23(20b-12)+8b-2\right)k^3\right]\\
&=\frac29k^2\sigma^{-10/3}[g+(4b-1)k^3].
\end{aligned}
$$

故正分支满足

$$
k^3=\frac g{1-4b},\qquad0<b<\frac14,
$$

积分给出精确解

$$
\boxed{F(\sigma)=F_0+3k\sigma^{1/3},
\qquad\phi(t,s)=F_0+3k(st^2)^{1/3}.}
\tag{10.1}
$$

该解在 $t,s>0$ 内光滑，且

$$
\phi_s=kt^{2/3}s^{-2/3}>0,
\qquad\phi_t=2ks^{1/3}t^{-1/3}>0.
$$

孤立点 $W=0$ 只表示所选独立变量失效，并不强制整条解为 (10.1)。边界处出现发散也不能自动证明弱激波存在；那需要另设弱形式与跳跃条件。

### 10.2 仿射剖面与 $D=0$

设 $F=F_0+C_1\sigma$，$C_1>0$，则 $q=r=0$，故 (R3) 化为 $(8b-2)C_1^5=0$。因此 $b=1/4$ 时存在精确仿射剖面；其不变量为

$$
\Sigma=C_1\sigma^{2/3},\qquad M=0,\qquad
W=\frac23\Sigma,\qquad N=\frac3{2\Sigma}.
$$

只要 $D\ne0$，该 $N$ 解 (A27)。若某点 $D=0$，仿射剖面本身仍可成立，只是 Abel 显式系数失效。

对 $0<b<1$，$D$ 的正根为

$$
\Sigma_D=\left[\frac g{4(1-b)}\right]^{1/3}.
$$

在该点，有限射流至少应满足未除式 (I1) 的代数相容性 $AM^2+BM+C=0$。用 $4(b-1)\Sigma^3=-g$ 消去 $b$，得到

$$
-3gM^2+(8\Sigma^4-5g\Sigma)M+6\Sigma^5-2g\Sigma^2=0.
$$

这是必要条件，不能单独证明光滑解可穿过该退化点，亦不能证明穿越时的唯一性。

### 10.3 一个正则初值的全部主要手算步骤

取

$$
g=1,\quad\beta=\frac18,\quad b=\frac18,
\qquad\sigma_*=1,\quad F(1)=2,\quad F'(1)=1,\quad F''(1)=0.
$$

此时 $p=1,q=0$，$r$ 的系数为

$$
p[g+4(b-1)\sigma^2p^3]=1+4(-7/8)=-5/2\ne0.
$$

(R3) 解出 $F'''$ 的右端在此解析，因此存在唯一局部解析剖面。代入方程：

$$
-\frac52r+(8b-2)=-\frac52r-1=0,
\qquad \boxed{F'''(1)=-\frac25.}
$$

为求四阶导数，把 $\mathcal R_3$ 看成 $(\sigma,p,q,r)$ 的函数，并用 $p'=q,q'=r$：

$$
0=\frac{d\mathcal R_3}{d\sigma}
=\mathcal R_{3,\sigma}+q\mathcal R_{3,p}
+r\mathcal R_{3,q}+F^{(4)}\mathcal R_{3,r}.
$$

这里各偏导完整写为

$$
\begin{aligned}
\mathcal R_{3,\sigma}&=8(b-1)\sigma p^4r
+8(b-1)\sigma p^3q^2+(20b-12)p^4q,\\
\mathcal R_{3,p}&=[g+16(b-1)\sigma^2p^3]r
+12(b-1)\sigma^2p^2q^2\\
&\quad+4(20b-12)\sigma p^3q+5(8b-2)p^4,\\
\mathcal R_{3,q}&=2[4(b-1)\sigma^2p^3-2g]q+(20b-12)\sigma p^4,\\
\mathcal R_{3,r}&=p[g+4(b-1)\sigma^2p^3].
\end{aligned}
$$

初始点处，$q=0$，且

$$
\mathcal R_{3,\sigma}=8(-7/8)(-2/5)=14/5,
\quad\mathcal R_{3,q}=20/8-12=-19/2,
\quad\mathcal R_{3,r}=-5/2.
$$

因此

$$
0=\frac{14}5+\left(-\frac25\right)\left(-\frac{19}2\right)
-\frac52F^{(4)}(1)
=\frac{33}5-\frac52F^{(4)}(1),
\qquad \boxed{F^{(4)}(1)=\frac{66}{25}.}
$$

令 $x=\sigma-1$，泰勒展开为

$$
\begin{aligned}
F(1+x)
&=2+x+\frac0{2!}x^2+\frac{-2/5}{3!}x^3+\frac{66/25}{4!}x^4+O(x^5)\\
&=\boxed{2+x-\frac{x^3}{15}+\frac{11x^4}{100}+O(x^5).}
\end{aligned}
\tag{10.2}
$$

这是局部解析解的截断展开；有限多项式本身不被声称为精确全局解。

### 10.4 同一射流的 Abel 初值核验

由定义有 $\Sigma_*=1$、$M_*=0$、$W_*=2/3$、$N_*=3/2$，$D_*=-5/2$。三个系数在初始点为

$$
a_3=-\frac2{45},\qquad a_2=-\frac{22}{15},\qquad a_1=\frac{11}5.
$$

因此

$$
\begin{aligned}
N_{,\Sigma}(1)
&=-\frac2{45}\left(\frac32\right)^3
-\frac{22}{15}\left(\frac32\right)^2
+\frac{11}5\frac32\\
&=-\frac3{20}-\frac{33}{10}+\frac{33}{10}=-\frac3{20}.
\end{aligned}
$$

另一方面，(7.4) 给出 $\mu''(1)=W_*M_{,\Sigma}(1)$，所以

$$
M_{,\Sigma}(1)=\frac{-2/5}{2/3}=-\frac35.
$$

由 $N=1/W$，

$$
N_{,\Sigma}=-N^2\left(M_{,\Sigma}+\frac23\right)
=-\frac94\left(-\frac35+\frac23\right)=-\frac3{20}.
$$

这同时核验了变换，并以具体数据说明 $M$ 与 $N$ 的导数不能混同。

### 10.5 回代原 PDE 与有限数值一致性检查

在 $(t,s)=(1,1)$，导数表给出

$$
\phi=2,\ v=2,\ \rho=1,\ a=2,\ \ell=2,\ c=0,
\quad T=-\frac{16}5,\quad R=-\frac45.
$$

代入原展开式 (1.6)：

$$
\begin{aligned}
\Delta_3
&=-\frac{16}5+4
-\left(1+\frac18\cdot4\right)\left(-\frac45\right)
-2\cdot\frac18\cdot2\cdot2^2\\
&=-\frac{16}5+4+\frac65-2=0.
\end{aligned}
$$

另分别积分两个系统：其一为 $F'=p,p'=q,q'=r(\sigma,p,q)$，其中 $r$ 由 (R3) 解出；其二为 (A27) 联立 $\sigma_{,\Sigma}=\sigma N$、$F_{,\Sigma}=\Sigma\sigma^{1/3}N$。采用 DOP853，相对容差 $10^{-11}$、绝对容差 $10^{-13}$，在 $1\le\Sigma\le1.05$ 的 101 个比较点，已有验证记录为

| 对应重构量 | 两次积分结果的最大绝对差 |
|---|---|
| $F$ | $1.87\times10^{-14}$ |
| $\mu$ | $3.86\times10^{-14}$ |
| $\mu'$ | $1.21\times10^{-13}$ |

该段终点 $\sigma\approx1.0775882790$，采样点上 $|D|\ge2.5$、$|N|>1.487$。这些数值仅检查两套实现的一致性，不能当作真解误差的严格界、解析证明或全局存在性证明。

## 单元 11：行波约化、第一积分与局部线性化

这一单元是原式 (30)–(31) 的前置计算，不属于得到 Abel 式 (27) 必经的路径。为避免与输沙常数 $\kappa$ 混淆，行波自变量记为 $\zeta$。

### 11.1 先由群作用导出行波形式

对任意允许的 $m$，方程不显含 $t,s,\phi$，故平移组合

$$
Z_{\alpha,\gamma}=\partial_t+\alpha\partial_s+\gamma\partial_\phi
$$

是对称生成元。其流的初值方程为 $d\bar t/d\epsilon=1$、$d\bar s/d\epsilon=\alpha$、$d\bar\phi/d\epsilon=\gamma$，因此

$$
(\bar t,\bar s,\bar\phi)=(t+\epsilon,s+\alpha\epsilon,\phi+\gamma\epsilon).
$$

定义两点不变量 $\zeta=s-\alpha t$、$w=\phi-\gamma t$，直接有 $Z_{\alpha,\gamma}\zeta=-\alpha+\alpha=0$、$Z_{\alpha,\gamma}w=\gamma-\gamma=0$。补充 $y=t$ 后，变换 $(t,s,\phi)\mapsto(y,\zeta,w)$ 的雅可比为 $1$，逆变换为

$$
t=y,\qquad s=\zeta+\alpha y,\qquad\phi=w+\gamma y.
$$

不变曲面条件是 $\gamma-\phi_t-\alpha\phi_s=-w_y=0$，所以

$$
\boxed{\phi(t,s)=\gamma t+\Phi(\zeta),
\qquad\zeta=s-\alpha t.}
\tag{11.1}
$$

本节重新用 $\mu(\zeta)=d\Phi/d\zeta$ 表示行波斜率，与单元 7 的相似剖面斜率具有不同自变量。撇号在本单元只表示 $d/d\zeta$。正性条件为

$$
\mu>0,\qquad\gamma-\alpha\mu>0.
\tag{11.2}
$$

第二个条件保证一般实指数的流速幂有确定的实值。$\gamma=0$ 时必须 $\alpha<0$。

### 11.2 全部所需导数与散度回拉

由于 $\zeta_t=-\alpha$、$\zeta_s=1$，逐次求导得

$$
\begin{aligned}
\phi_t&=\gamma-\alpha\mu,&\phi_s&=\mu,\\
\phi_{tt}&=(-\alpha)\mu'(-\alpha)=\alpha^2\mu',&
\phi_{ts}&=-\alpha\mu',&\phi_{ss}&=\mu',\\
\phi_{ttt}&=\alpha^2\mu''(-\alpha)=-\alpha^3\mu'',&
\phi_{tts}&=\alpha^2\mu'',\\
\phi_{tss}&=-\alpha\mu'',&\phi_{sss}&=\mu''.
\end{aligned}
$$

对只依赖 $\zeta$ 的表达式，$D_t=-\alpha d/d\zeta$、$D_s=d/d\zeta$。两个散度括号分别变为

$$
H=\left(\alpha^2\mu-\frac g{\mu^2}\right)\mu',
\qquad
\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}
=-\alpha\frac{(\gamma-\alpha\mu)^{m-1}}\mu\mu'.
$$

故

$$
\begin{aligned}
\left.\Delta_m\right|_{\phi=\gamma t+\Phi(\zeta)}
={}&-\alpha\frac d{d\zeta}
\left[\left(\alpha^2\mu-\frac g{\mu^2}\right)\mu'\right]\\
&+\alpha g\beta\frac d{d\zeta}
\left[\frac{(\gamma-\alpha\mu)^{m-1}}\mu\mu'\right]\\
={}&-\alpha\frac d{d\zeta}[K(\mu)\mu'],
\end{aligned}
\tag{11.3}
$$

其中正式定义

$$
\boxed{K(\mu)=\alpha^2\mu-\frac g{\mu^2}
-\frac{g\beta}\mu(\gamma-\alpha\mu)^{m-1}.}
\tag{11.4}
$$

### 11.3 第一积分及未除式

**局部条件。** 先假设 $\alpha\ne0$，才可由 (11.3) 推出

$$
\frac d{d\zeta}[K(\mu)\mu']=0,
\qquad
K(\mu)\mu''+K_{,\mu}(\mu)(\mu')^2=0.
\tag{11.5}
$$

系数求导的全部商法则项为

$$
\begin{aligned}
K_{,\mu}
&=\alpha^2+\frac{2g}{\mu^3}
-g\beta\left[-\frac{(\gamma-\alpha\mu)^{m-1}}{\mu^2}
-\frac{\alpha(m-1)}\mu(\gamma-\alpha\mu)^{m-2}\right]\\
&=\alpha^2+\frac{2g}{\mu^3}
+\frac{g\beta}{\mu^2}(\gamma-\alpha\mu)^{m-1}
+\frac{g\beta\alpha(m-1)}\mu(\gamma-\alpha\mu)^{m-2}.
\end{aligned}
$$

由完整导数等于零，得到第一积分

$$
\boxed{K(\mu)\mu'=C_1.}
\tag{11.6}
$$

不能未经说明把 $C_1$ 设为 $1$；$C_1=0$ 包含常斜率分支。第一积分的依据是 (11.5) 的散度结构，而不是仅凭“存在一个平移对称”作出结论。

### 11.4 可逆点变换与八维对称性的证明

为把 (11.5) 化为二阶线性方程，定义斜率空间中的新因变量

$$
z=\Psi(\mu),\qquad\Psi(\mu)=\int_{\mu_*}^{\mu}K(r)\,dr.
$$

变换 $(\zeta,\mu)\mapsto(\zeta,z)$ 的雅可比为 $\Psi'(\mu)=K(\mu)$，所以仅在 $K\ne0$ 的区域局部可逆。链式法则给出

$$
z'=K(\mu)\mu',\qquad
z''=K(\mu)\mu''+K_{,\mu}(\mu)(\mu')^2=0.
\tag{11.7}
$$

因而该正则斜率方程局部点等价于自由粒子方程 $z''=0$。

为明确“八维”并非由两个平移直接推出，现求 $z''=0$ 的一般点生成元 $V=\tau(\zeta,z)\partial_\zeta+\eta(\zeta,z)\partial_z$。设 $u=z'$，由二阶延拓递推，在 $z''=0$ 上

$$
\eta^{[\zeta\zeta]}
=\eta_{,\zeta\zeta}
+(2\eta_{,\zeta z}-\tau_{,\zeta\zeta})u
+(\eta_{,zz}-2\tau_{,\zeta z})u^2-\tau_{,zz}u^3=0.
$$

分离 $u$ 各次幂：

$$
\tau_{,zz}=0,\quad\eta_{,zz}=2\tau_{,\zeta z},\quad
2\eta_{,\zeta z}=\tau_{,\zeta\zeta},\quad\eta_{,\zeta\zeta}=0.
$$

前两式先给 $\tau=A(\zeta)z+B(\zeta)$、$\eta=A'(\zeta)z^2+C(\zeta)z+E(\zeta)$。第三式成为 $3A''z+2C'-B''=0$，第四式成为 $A'''z^2+C''z+E''=0$。由此

$$
A=a_1\zeta+a_0,\quad C=c_1\zeta+c_0,\quad
E=e_1\zeta+e_0,\quad B=c_1\zeta^2+b_1\zeta+b_0.
$$

八个独立常数给出基

$$
\begin{gathered}
\partial_\zeta,\quad\partial_z,\quad
\zeta\partial_\zeta,\quad z\partial_\zeta,\quad
\zeta\partial_z,\quad z\partial_z,\\
\zeta^2\partial_\zeta+\zeta z\partial_z,
\qquad\zeta z\partial_\zeta+z^2\partial_z.
\end{gathered}
$$

这是局部射影对称代数 $\mathfrak{sl}(3,\mathbb R)$，也是正则标量二阶 ODE 点对称维数的最大情形。[2] 经 $\partial_z=K^{-1}\partial_\mu$ 拉回可得 (11.5) 的八个对称。此结论局限于 $K\ne0$ 的局部区域；$\mathfrak{sl}(3,\mathbb R)$ 是李代数，不能与群 $\mathrm{SL}(3,\mathbb R)$ 混作同一对象。

### 11.5 保留三个积分常数的重构

积分 $z''=0$，并把 $\zeta_0$ 固定为积分锚点：

$$
\Psi(\mu(\zeta))=C_1(\zeta-\zeta_0)+C_2,
\qquad
\Phi(\zeta)=C_3+\int_{\zeta_0}^{\zeta}\mu(r)\,dr.
\tag{11.8}
$$

在 $K\ne0$ 处可局部反解 $\mu$，再取 $\phi=\gamma t+\Phi(s-\alpha t)$。$C_1,C_2,C_3$ 是固定生成元参数 $\alpha,\gamma$ 下的三个剖面常数。若 $C_1=0$，正则分支给 $\mu=\mu_0$ 常数，并要求 $\mu_0>0$、$\gamma-\alpha\mu_0>0$。

若 $\alpha=0$，不得由 (11.3) 除以 $\alpha$。此时 $\phi=\gamma t+\Phi(s)$，$\phi_{tt}=\phi_{ts}=0$，剩余括号与 $t$ 无关，所以原标量方程恒满足。任意 $C^3$ 的 $\Phi$，只要 $\Phi'>0,\gamma>0$，都属于正性分支。

若 $K=0$，则线性化失去秩，应回到 (11.3) 或 (11.6)，不可从正则反函数结论推断穿越该集合的行为。

### 11.6 $m=3$ 的显式原函数与代数关系的适用范围

将 $(\gamma-\alpha\mu)^2=\gamma^2-2\alpha\gamma\mu+\alpha^2\mu^2$ 展开，得到

$$
\begin{aligned}
K(\mu)
&=\alpha^2\mu-\frac g{\mu^2}
-b\left(\frac{\gamma^2}\mu-2\alpha\gamma+\alpha^2\mu\right)\\
&=\alpha^2(1-b)\mu+2b\alpha\gamma
-\frac{b\gamma^2}\mu-\frac g{\mu^2}.
\end{aligned}
$$

一个未锚定的原函数为

$$
\Psi_0(\mu)=\frac{\alpha^2(1-b)}2\mu^2
+2b\alpha\gamma\mu-b\gamma^2\log\mu+\frac g\mu.
\tag{11.9}
$$

四项导数分别为 $\alpha^2(1-b)\mu$、$2b\alpha\gamma$、$-b\gamma^2/\mu$、$-g/\mu^2$，恰好给出 $K$。$\gamma\ne0$ 时通常含对数，不能称为一般代数显式解。

$\gamma=0$ 时，将锚定差吸收进 $C_2$，再乘以 $\mu>0$，得到

$$
\boxed{\frac{\alpha^2(1-b)}2\mu^3
-[C_1(\zeta-\zeta_0)+C_2]\mu+g=0.}
\tag{11.10}
$$

$b=1$ 时三次项消失，正分支化为 $\mu=g/[C_1(\zeta-\zeta_0)+C_2]$，分母必须为正。

例如取 $g=1,\beta=1/8,m=3,\alpha=-1,\gamma=0$，$\zeta=s+t$，令

$$
\frac7{16}\mu^2+\frac1\mu=\frac{\zeta+21}{16},
\qquad7\mu^3-(\zeta+21)\mu+16=0.
$$

在 $(\zeta,\mu)=(2,1)$，对 $\mu$ 的偏导为 $21-23=-2\ne0$，隐函数定理给出唯一局部解析根。对该关系求导：

$$
[21\mu^2-(\zeta+21)]\mu'-\mu=0,
\quad\mu'(2)=-\frac12,
\quad K(1)=\frac78-1=-\frac18,
\quad K(1)\mu'(2)=\frac1{16}.
$$

故取 $\Phi(\zeta)=\int_2^\zeta\mu(r)\,dr$，所得 $\phi(t,s)=\Phi(s+t)$ 在 $(1,1)$ 附近是 (1.4) 的精确隐式解，且 $\phi_s=\phi_t=\mu>0$。

## 单元 12：式 (30) 到 (31) 的逐行积分与文献核验

### 12.1 先辨明本节的变量

本节对应原文第 3.6 节，取行波约化中的 $\gamma=0$、$\alpha<0$、$\mu>0$。这里的微分不变量是

$$
\Xi=\mu(\zeta),\qquad
M_{\rm tr}=\frac{d\mu}{d\zeta}.
$$

原文式 (30)–(31) 将 $M_{\rm tr}$ 简写成 $M$。它与式 (27) 路线中的 $M=\sigma^{5/3}\mu_{,\sigma}$ 不是同一不变量，本稿保留下标避免混淆。

**动机。** 行波斜率方程不显含 $\zeta$，其平移对称允许用 $\Xi=\mu$ 作新自变量。该步骤要求 $d\Xi/d\zeta=M_{\rm tr}\ne0$，与单元 7 要求 $W\ne0$ 的条件不同。

### 12.2 从固定 PDE 推导相容的一阶方程

在 $\alpha<0$ 时定义实正常数

$$
c_{\rm tr}=g\beta(-\alpha)^{m-1}>0.
$$

于是 (11.4) 在 $\gamma=0$ 下变为

$$
K(\Xi)=\alpha^2\Xi-\frac g{\Xi^2}-c_{\rm tr}\Xi^{m-2}.
$$

由 $\mu'=M_{\rm tr}(\Xi)$，链式法则为

$$
\mu''=\frac{dM_{\rm tr}}{d\Xi}\frac{d\Xi}{d\zeta}
=M_{\rm tr}M_{{\rm tr},\Xi}.
$$

代入 (11.5)：

$$
K M_{\rm tr}M_{{\rm tr},\Xi}
+K_{,\Xi}M_{\rm tr}^2=0.
$$

在 $K\ne0,M_{\rm tr}\ne0$ 的区域，除以 $K M_{\rm tr}^2$：

$$
\frac{M_{{\rm tr},\Xi}}{M_{\rm tr}}=-\frac{K_{,\Xi}}K.
\tag{12.1}
$$

这里

$$
K_{,\Xi}=\alpha^2+\frac{2g}{\Xi^3}
-(m-2)c_{\rm tr}\Xi^{m-3}.
$$

分子分母同乘 $\Xi^3$ 并改变整体符号，得到相容的修正式

$$
\boxed{
\frac{M_{{\rm tr},\Xi}}{M_{\rm tr}}
=\frac{\alpha^2\Xi^3+(2-m)c_{\rm tr}\Xi^m+2g}
{\Xi\big(g+c_{\rm tr}\Xi^m-\alpha^2\Xi^3\big)}.}
\tag{30*}
$$

### 12.3 逐行积分：由 (30*) 到 (31*)

在一个连通、非零的局部区域上，$M_{\rm tr}$ 与 $K$ 各自符号固定，故

$$
\frac d{d\Xi}\log|M_{\rm tr}|
=-\frac d{d\Xi}\log|K|.
$$

积分：

$$
\log|M_{\rm tr}|=-\log|K|+C,
\qquad |M_{\rm tr}K|=e^C.
$$

将符号吸收进非零常数 $C_1$，得到

$$
M_{\rm tr}=\frac{C_1}{K(\Xi)}
=\frac{C_1\Xi^2}{\alpha^2\Xi^3-g-c_{\rm tr}\Xi^m}.
\tag{12.2}
$$

也可把 (30*) 识别为对数导数。令 $Q(\Xi)=\alpha^2\Xi^3-g-c_{\rm tr}\Xi^m$，则

$$
Q'=3\alpha^2\Xi^2-mc_{\rm tr}\Xi^{m-1},
$$

$$
\begin{aligned}
\frac2\Xi-\frac{Q'}Q
&=\frac{2(\alpha^2\Xi^3-g-c_{\rm tr}\Xi^m)
-(3\alpha^2\Xi^3-mc_{\rm tr}\Xi^m)}{\Xi Q}\\
&=\frac{-\alpha^2\Xi^3-2g+(m-2)c_{\rm tr}\Xi^m}{\Xi Q}\\
&=\frac{\alpha^2\Xi^3+(2-m)c_{\rm tr}\Xi^m+2g}
{\Xi(g+c_{\rm tr}\Xi^m-\alpha^2\Xi^3)}.
\end{aligned}
$$

因此 $\log|M_{\rm tr}|=2\log\Xi-\log|Q|+C$，与 (12.2) 完全相同。原文式 (31) 形式的对应修正版为

$$
\boxed{
M_{\rm tr}(\Xi)
=\frac{\widetilde C\,\Xi}
{\Xi^{m-1}-c_{\rm tr}^{-1}\left(\alpha^2\Xi^2-\dfrac g\Xi\right)},
\qquad\widetilde C=-\frac{C_1}{c_{\rm tr}}.}
\tag{31*}
$$

要核验两种形式，只需将分母展开为

$$
\Xi^{m-1}-c_{\rm tr}^{-1}\left(\alpha^2\Xi^2-\frac g\Xi\right)
=-\frac{\alpha^2\Xi^3-g-c_{\rm tr}\Xi^m}{c_{\rm tr}\Xi}.
$$

若 $m$ 为整数，才可直接用无歧义的整数幂把常数写成

$$
c_{\rm tr}^{-1}
=\frac{e^{-i(m-1)\pi}}{\beta g}\alpha^{-(m-1)}.
$$

对非整数 $m$、$\alpha<0$，本稿始终保留实正底数 $(-\alpha)^{m-1}$；若拆成负底数幂和复相位，必须另外指定一致的复对数分支。

### 12.4 原文印刷的 (30) 与 (31) 是否相容

以下按核读的 v3 第 8 页印刷形式转写；仅将其 $M$ 改名为 $M_{\rm tr}$。

原式 (30) 为

$$
\frac{M_{{\rm tr},\Xi}}{M_{\rm tr}}
=\frac{\alpha^2\Xi^3+(-1)^{m-1}\beta\alpha^m(2-m)\Xi^{m-1}+2g}
{\Xi\big(g+(-1)^{m-1}\alpha^m\Xi^{m-1}-\alpha\Xi^3\big)}.
\tag{30p}
$$

原式 (31) 为

$$
M_{\rm tr}(\Xi)
=\frac{M_0\Xi}
{\Xi^{m-1}-\dfrac{e^{-i(m-1)\pi}}{\beta g}
\alpha^{-(m-1)}\left(\alpha\Xi^2-\dfrac g\Xi\right)}.
\tag{31p}
$$

注意印刷系数是 $1/(\beta g)$，不是 $\beta g$。另一方面，括号中印刷的是 $\alpha\Xi^2$；从固定 PDE 的 (11.4) 推导需要 $\alpha^2\Xi^2$。原式 (30) 的若干幂次及参数因子也不同于 (30*)，不能只改 (31) 一个字母就宣称整条原文链成立。

**精确反例。** 取 $m=3,\alpha=-1,\beta=g=1$，且 $\Xi>0$。这些参数符合 $\gamma=0$ 时的正流速分支。原式 (30) 右端成为

$$
R_{30p}(\Xi)=\frac{\Xi^3+\Xi^2+2}{\Xi(1-\Xi^2+\Xi^3)},
\qquad R_{30p}(1)=4.
$$

原式 (31) 则成为

$$
M_{\rm tr}(\Xi)=\frac{M_0\Xi^2}{2\Xi^3+1},\qquad M_0\ne0.
$$

其对数导数为

$$
\frac{M_{{\rm tr},\Xi}}{M_{\rm tr}}
=\frac2\Xi-\frac{6\Xi^2}{2\Xi^3+1},
\qquad
\left.\frac{M_{{\rm tr},\Xi}}{M_{\rm tr}}\right|_{\Xi=1}=2-2=0.
$$

两式在同一点给出 $4\ne0$，且分母均不为零。因此印刷式 (31) 不是印刷式 (30) 的一般解。这个结论是精确代数反证，不依赖数值误差或对作者意图的猜测。

相同参数代入从固定 PDE 推出的式 (12.2)，得到 $M_{\rm tr}=-C_1\Xi^2$、$M_{{\rm tr},\Xi}/M_{\rm tr}=2/\Xi$；代入 (30*) 也恰为 $2/\Xi$。这另行核验修正链的内部一致性。

### 12.5 从 $M_{\rm tr}(\Xi)$ 继续恢复行波

只求出式 (31*) 尚未得到 $\phi(t,s)$。由 $d\Xi/d\zeta=M_{\rm tr}$，若 $C_1\ne0$，则

$$
\frac{d\zeta}{d\Xi}=\frac1{M_{\rm tr}}=\frac{K(\Xi)}{C_1},
\qquad
\zeta-\zeta_0=\frac1{C_1}\int_{\Xi_0}^{\Xi}K(r)\,dr.
$$

在 $K\ne0$ 处局部反解 $\Xi=\mu(\zeta)$，再作 $\Phi'=\mu$ 的积分。这正是 (11.8) 的重构。若 $M_{\rm tr}=0$，用 $\Xi$ 作自变量失效；应回到 (11.5)，其中常斜率解仍成立。

由于 $M_{\rm tr}=C_1/K$ 可能在 $K=0$ 处发散，不能仅凭一个商式就断言所得解在整个定义域无奇点。

### 12.6 原式 (25)–(26) 的印刷乘积与精确残差

核读原文第 7 页，$\mu_{,\sigma}\sigma$ 中后一个 $\sigma$ 在基线上，表示 $\sigma\mu'$，不能转写成 $\mu''$。原式 (26) 的印刷残差据此为

$$
\begin{aligned}
\mathcal P_{26}={}&4\sigma\mu^3\mu'(\sigma\mu'+3\mu)
+2g(\mu')^2\\
&+\beta\sigma\left[(\sigma\mu'+5\mu)\sigma\mu'
+(2\mu+\sigma^2\mu'')\mu\right].
\end{aligned}
$$

取 (10.1) 的精确分支 $g=1/2,\beta=1/4,b=1/8,k=1$。在 $\sigma=1$，有 $\mu=1,\mu'=-2/3,\mu''=10/9$，且 (R2) 为零。印刷残差的三项却分别为

$$
\begin{aligned}
4(1)^3\left(-\frac23\right)\left(-\frac23+3\right)&=-\frac{56}9,\\
2\left(\frac12\right)\left(-\frac23\right)^2&=\frac49,\\
\frac14\left[\left(-\frac23+5\right)\left(-\frac23\right)
+\left(2+\frac{10}9\right)\right]
&=\frac14\left[-\frac{26}9+\frac{28}9\right]=\frac1{18}.
\end{aligned}
$$

因此

$$
\boxed{\mathcal P_{26}=-\frac{56}9+\frac49+\frac1{18}
=-\frac{103}{18}\ne0.}
$$

这证明原式 (26) 不是本稿从固定标量 PDE 推出的 (R2)。将 $(\mu,\mu',\mu'')$ 换回 $(F',F'',F''')$，同一剖面 $F=F_0+3\sigma^{1/3}$ 也检验原式 (25)。曾有转写把基线乘积当作更高阶导数而产生不同残差；该转写不能用来报告原文的精确残差。

### 12.7 修正记录与全部局部条件

| 项目 | 本稿得到的结果 | 数学地位与范围 |
|---|---|---|
| 标准物质回拉 | Exner 式含 $-\phi_tB_s^L/\phi_s$ | 链式法则精确恒等式；与固定标量模型分开 |
| $m=3$ 点对称分类 | (3.3)–(3.5) 给五维完整局部代数 | 完整确定方程的必要性及充分性证明 |
| $X_5$ 的系数 | 标度方向 $(1,-2,0)$ | 对角候选族内等权的必要性与充分性均已证明 |
| 一般 $m$ | $m\ne3$ 仅有一维对角标度 | 不是一般 $m$ 的完整点对称分类；$m=1$ 有额外反例 |
| Table 1 | $[X_5,X_1]=-X_1$、$[X_5,X_2]=2X_2$ | 直接括号计算 |
| 一维最优系统 | 包含两类共振剩余项、$X_5+\nu X_3$ 及全部平移支撑分支 | 在明确的连通伴随等价关系下完整 |
| 式 (25)–(26) | 使用 (R3)、(R2) | 精确回拉恒等式与精确反例支撑的重建 |
| 两个继承标度 | $3\sigma\partial_\sigma+F\partial_F$，$3\sigma\partial_\sigma-2\mu\partial_\mu$ | 分别由商投影前推与延拓下降得到，因变量方向分别为 $\partial_F,\partial_\mu$ |
| 式 (27) | 对 $N=(M+2\Sigma/3)^{-1}$ 成立 | 充分的变量修正；不声称还原作者未写出的计算 |
| 式 (30)–(31) | 使用 (30*)、(31*) | 从固定 PDE 的行波积分推导；印刷两式由反例证实不相容 |
| 八维行波斜率代数 | $K\ne0$ 时经 $z=\int K\,d\mu$ 化为 $z''=0$ | 局部可逆点线性化及显式确定方程 |
| 例题中的数值比较 | 两套积分结果相符 | 有限数值一致性，不是真解误差上界 |

| 被使用的操作 | 必须保留的条件或恢复信息 |
|---|---|
| 解出主导数 $T=T_*$ | $\rho=\phi_s>0$ |
| $X_5$ 顺直坐标 | $t>0$，本稿进一步取 $s>0$ |
| 不变图像 $\phi=F(st^2)$ | $Q_{X_5}=0$，并只选择这类 PDE 解 |
| $\mu=F'$ 商降阶 | $\mu>0$；积分恢复 $F_*$ |
| 微分不变量 $\Sigma,M$ | $\sigma>0$；此时不要求 $\mu'\ne0$ |
| 以 $\Sigma$ 作自变量 | $W=M+2\Sigma/3\ne0$ |
| Abel 显式正规形 | $\Sigma>0,D\ne0$，$N$ 有限且非零 |
| Abel 重构 | 恢复 $\sigma_*,F_*$，用 $\sigma_{,\Sigma}=\sigma N\ne0$ 反解 |
| 行波第一积分 | 除以 $\alpha$ 前要求 $\alpha\ne0$ |
| 行波线性化 | $\mu>0,\gamma-\alpha\mu>0,K\ne0$ |
| 行波 $\Xi=\mu$ 作自变量 | 另要求 $M_{\rm tr}=d\mu/d\zeta\ne0$ |
| $W=0,D=0,K=0$ 等集合 | 回到未除式；正则坐标结论不自动延伸 |

## 手算提交时的推导顺序

复现式 (27) 的核心顺序为：写出 (1.4) 与正性域；按 (1.6) 展开；用 (2.2)–(2.9) 组成确定多项式；由六项分离和十一项余式求出 (3.3)；核验 (3.5)；说明 $\langle X_5\rangle$ 在最优系统中的位置；解群流并导出 $Q=0$；计算 (5.3)；保留乘子核验 (6.1)；依次引入 $\mu$、$\Sigma,M$、$N$；最后按单元 9 重构并检查所除因子。

提交材料应明确写出：本稿复现的是固定标量式 (7) 的可核验约化链，并给出原印刷式的必要修正。它没有分类原 PDE 的所有解，没有证明解全局正则，也没有给出一般 Abel 方程的初等函数通解。行波式 (30)–(31) 的核验是另一条约化路径，须单独说明自变量和非零条件。

## 参考文献

以下按 GB/T 7714 的顺序编码制手工编排。Olver 引用版本为实际核读的 1986 年第一版。

[1] OLVER P J. Applications of Lie groups to differential equations[M]. New York: Springer-Verlag, 1986. DOI: [10.1007/978-1-4684-0274-2](https://doi.org/10.1007/978-1-4684-0274-2).

[2] OLIVERI F. Lie symmetries of differential equations: theory, applications, and symbolic computation[M]. Cham: Birkhäuser, 2026. DOI: [10.1007/978-3-032-12791-4](https://doi.org/10.1007/978-3-032-12791-4).

[3] PALIATHANASIS A, LEON G, LEACH P G L. Lie symmetries and similarity solutions for a shallow-water model with bed elevation in Lagrange variables[J]. Mathematics, 2026, 14(3): 433. DOI: [10.3390/math14030433](https://doi.org/10.3390/math14030433).

### 核读位置与资料整合说明

Olver [1] 第 1 章相关小节用于群轨道及子群—子代数关系；第 2 章 Theorem 2.31 及延拓部分用于无穷小判据、最大秩和局部可解性条件；第 3 章相关小节用于伴随作用及最优系统。Oliveri [2] 的延拓、降阶和二阶方程线性化部分用于方法说明。本文各具体系数、域条件与反例均由所展示计算独立核验。

原论文 [3] 的 v3 文件中，第 2 页用于欧拉—物质坐标与式 (1)–(7) 的对照；第 4–6 页用于生成元及表格；第 7 页用于式 (25)–(27) 与基线乘积的视觉核读；第 8 页用于式 (30)–(31) 的逐项转写。用户提供的英文整合手稿和新增中文审校稿作为本次修订的工作材料，不另列为已发表学术文献。

本中文版把重复的几何说明并入相应计算，保留实际作用于主方程的全部延拓余项、六项三角分离及完整十一项约化余式；不再重复列出无约束的 118 行展开表，亦不重列乘子恒为零的两个三阶延拓分量。恢复这些冗长展开只需使用已经完整给出的递推式和组装式，不改变本文的分类结论。
