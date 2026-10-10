# 一般 m 的约化、一般点对称性障碍与物理 SVE 修正

日期：2026-10-10。本文给出独立推导；不声称新颖性、最大对称分类或全局解定理。

## 1. 固定问题与两个不同模型

全部公式按无量纲约定解释，参考速度取 1。固定 g>0、κ>0，令 β=mκ。
变量 t,s 为时间和质量标签，φ 为流体粒子位置。采用光滑经典解、
t>0、p=φ_t>0、q=φ_s>0 的局部连通分支。非整数幂按正实数分支定义。

设

\[
A=\phi_s\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^2},\qquad
C_m=\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}.
\]

原文的标量数学基准是

\[
E_m^{\mathrm{print}}=D_tA-gm\kappa D_sC_m=0.
\]

本次由常规 Eulerian SVE 系统独立推导的修正方程是

\[
E_m^{\mathrm{phys}}=D_tA-D_s\left(\frac{\phi_tA}{\phi_s}\right)
-gm\kappa D_sC_m=0.
\]

代码同时保留两种模型，所有结果按模型标记。

## 2. 物理推导与局部等价性

考虑标准光滑一维系统及速度幂律输沙闭合：

\[
h_t+(hu)_x=0,\qquad
u_t+uu_x+g(h_x+B_x)=0,\qquad
B_t+m\kappa u^{m-1}u_x=0.
\]

令 x=φ(t,s)，φ_t=u(t,φ)，φ_s=1/h(t,φ)，
b(t,s)=B(t,φ(t,s))。连续性方程与此质量坐标相容。
链式法则给出

\[
\phi_{tt}-g\frac{\phi_{ss}}{\phi_s^3}
+g\frac{b_s}{\phi_s}=0,
\qquad
b_t-\frac{\phi_t}{\phi_s}b_s
+m\kappa\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}=0.
\]

故

\[
b_s=-A/g,\qquad
b_t=-\phi_tA/(g\phi_s)-m\kappa C_m.
\]

相容性 b_st=b_ts 恰为 E_m^phys=0。
在充分小的单连通正则域上，此相容性使一阶微分形式
b_t dt+b_s ds 闭合，Poincaré 引理重构 b 至一个加法常数。
用 φ_s>0 逆变换回 Eulerian 坐标，即恢复上述光滑 SVE 系统。
在非单连通域还需要零周期条件；已有床面数据必须匹配该原函数。
这不涉及冲击波、弱解或其他输沙闭合。

原文式 (6) 在 b 被解释为 Eulerian 床面拉回时缺少上述对流项。
这一结论基于该变量解释；若作者采用另一床面变量，其定义需要另行给出。
本次已经给出在明确变量解释下的数学修正，不推测作者意图。

## 3. 任意光滑点生成元的一阶延续障碍

两种标量模型都满足精确恒等式

\[
\operatorname{pr}^{(3)}X_5E_m+E_m
=(m-3)gm\kappa D_sC_m,
\qquad X_5=t\partial_t-2s\partial_s.
\]

固定 g,κ，令 m=3+δ。
若存在 C^1 参数依赖的正则点对称性族

\[
X_\delta=X_5+\delta Y+o(\delta),\qquad
Y=\tau(t,s,\phi)\partial_t+\xi(t,s,\phi)\partial_s
+\eta(t,s,\phi)\partial_\phi,
\]

其必要的一阶切向条件为

\[
\left.\left(\operatorname{pr}^{(3)}YE_3+T_3\right)\right|_{E_3=0}=0,
\qquad
T_3=3g\kappa D_s\left(\phi_t^2\frac{\phi_{ts}}{\phi_s}\right).
\]

这里 τ,ξ,η 是任意足够光滑的点系数函数；未假设对角缩放、
多项式系数或投影性，也未先解一个有限维生成元 ansatz。
参数导数中的对数项通过已验证的缺陷恒等式消去；不能将其省略后直接猜测强迫项。

**命题。** 在上述正则分支及通常的方程流形切向定义下，
对两种标量模型，该一阶切向条件均无解。

**证明。** 记 φ 为点坐标 u，记

\[
p=\phi_t,\ q=\phi_s,\ a=\phi_{tt},\ b=\phi_{ts},\ c=\phi_{ss},
\ r=\phi_{ttt},\ w=\phi_{tts},\ x=\phi_{tss},\ y=\phi_{sss}.
\]

两种模型中 ∂E_3/∂r=q>0，故在壳 E_3=0 上可精确消去 r。
其余上述 jet 坐标在该正则方程图上自由。这也补足了形式分裂与局部解
之间的正则性桥梁：残差零集在 q>0 上是最大秩超曲面；固定实数 m 时，
两模型在 p,q>0 上的系数均为解析函数，并可对纯时间 leading jet
φ_ttt 求解，因此方程是解析 normal form。由 Olver 的解析 normal-form
局部可解性结果，无穷小切向判据在该局部分支上适用，而不只是一条形式
jet 恒等式。
令 Ω 为消去 r 后的 pr^(3)Y E_3+T_3。
递归延拓并清除已声明非零的 q 分母，得到

\[
\boxed{[p^2q^2]\left(q^3\frac{\partial\Omega}{\partial x}\right)
=3g\kappa\ne0.}
\]

左侧括号指关于自由变量 p,q 的多项式系数。
τ,ξ,η 及其点坐标偏导数不依赖这些 jet 变量。
若 Ω 在正实数开分支上恒为零，该多项式每个系数必须为零，矛盾。
这里没有在 p=0 或 q=0 的物理奇异分支上评价原方程；
使用的是开集上的多项式恒等式原则。证毕。

下面给出无需依赖软件输出即可核对的最高阶系数。
令 e_t=D_tη-pD_tτ-qD_tξ，e_s=D_sη-pD_sτ-qD_sξ。
原文模型的 N=q³∂_xΩ 为

\[
N_{\mathrm{print}}=(3g+6g\kappa p^2q)e_s
-6g\kappa pq^2e_t
+2g(q+3\kappa p^2q^2)(D_s\xi-D_t\tau)
+3g\kappa p^2q^2.
\]

这是从主符号 q r-(g/q²+3gκp²/q)x 与一阶延拓系数直接得到的。
修正模型相对原文模型的差为

\[
N_{\mathrm{phys}}-N_{\mathrm{print}}
=p(3g\kappa p^2q-2g)(q\tau_u+\tau_s)
+2pq^3(p\xi_u+\xi_t).
\]

展开总导数后，两式中 η_u、τ_t、ξ_s 对 p²q² 系数的贡献分别相消，
修正差式也没有 p²q² 项，所以剩下的系数恰为 3gκ。

`symbolic_certificates.json` 保存两种模型的完整最高阶系数多项式、
壳消元公式、强迫项来源、选取的单项式和分支条件。
原文模型的最高阶系数还通过独立的主符号推导核对。

该结果排除参数依赖为 C^1、而点系数关于 (t,s,φ) 足够光滑的正则延续，
也排除具有上述非零零阶项的标准一阶 BGI 型点生成元提升。允许任意 Y
已包含零阶代数的一阶 gauge 添加。
它不排除奇异参数依赖、FS 扩展场系统的对称性、接触/广义/非局部对称性，
也不是完整 SVE 系统中依赖额外床面场的最大点对称分类。
不需要为了得到这一障碍而完成所有确定方程。

## 4. 一般 m 的精确共同缩放与二阶约化

对固定参数，两种模型均有

\[
X_c=t\partial_t+s\partial_s+\phi\partial_\phi,
\qquad\operatorname{pr}^{(3)}X_cE_m=-2E_m.
\]

选取完整局部坐标

\[
y=\log t,\quad z=s/t,\quad v=\phi/t,
\qquad t=e^y,\ s=ze^y,\ \phi=e^y v.
\]

base Jacobian det D_(t,s)(y,z)=1/t² 非零。
在 t>0 上，X_c 在总空间与 (t,s) 基空间的轨道秩均为 1；其特征方程为

\[
Q_c=\phi-t\phi_t-s\phi_s=0.
\]

不变图还满足 D_JQ_c=0（|J|≤2）。轨道对依赖变量竖直方向横截，
而上述 Jacobian 保证 (y,z) 是合法的局部基坐标。因此 v=F(z)，故
φ=tF(s/t)，是正则局部不变图，而不只是一次形式代换。
设 P=F'，V=F-zP>0，P>0，β=mκ，令

\[
\mathcal A=F''(z^2P-g/P^2),\qquad
\mathcal J=zV^{m-1}F''/P.
\]

直接链式代入给出 E_m=t^(-2) R_m，其中

\[
R_m^{\mathrm{print}}=-\mathcal A-z\mathcal A'+g\beta\mathcal J',
\qquad
R_m^{\mathrm{phys}}=R_m^{\mathrm{print}}-(V\mathcal A/P)'.
\]

它们都有一阶积分 R=I'，并且

\[
I^{\mathrm{print}}=L_{\mathrm{print}}F'',\qquad
L_{\mathrm{print}}=-z^3P+gz/P^2+g\beta zV^{m-1}/P,
\]

\[
I^{\mathrm{phys}}=L_{\mathrm{phys}}F'',\qquad
L_{\mathrm{phys}}=F(g/P^3-z^2)+g\beta zV^{m-1}/P.
\]

因此在 L≠0 的分支上，约化问题是二阶 ODE

\[
F''=I_0/L(z,F,F';m).
\]

第三个原始 IVP 数据 F''(z0) 用于确定 I0=L(z0,F0,P0)F''0。
常规局部存在唯一性及解析 ODE 定理适用；区间外延拓和一致界需另证。
这一约化保持参数 m，完全不需要 X5 延续。

## 5. 床面、数据与积分常数

任一此类约化解的床面为

\[
b(t,s)=\mathcal B(s/t)+\frac{I_0}{g}\log t,
\qquad\mathcal B'(z)=-\mathcal A(z)/g.
\]

对修正模型，此 b 同时满足两条床面导数关系。
一般不能删去对数项：它代表积分常数，而非任意机器学习补偿。
完整系统的不变图可用已验证的 lift

\[
X_c+(I_0/g)\partial_b
\]

描述；I0 在选取该子群时为固定积分参数。
Eulerian 重构由 x/t=F(z) 局部求逆，随后
h=1/F'(z)，u=F(z)-zF'(z)，B=𝔅(z)+(I0/g)log t。

构造的共同缩放兼容数据面是 Γ0={s=z0 t}：
φ/t=F0，φ_s=P0，tφ_ss=F''0，且
b=b0+(I0/g)log t。任意已有渠段边界或通量不能自动满足这些条件。
本次实验使用构造的数据，不宣称对应真实渠段测量。

## 6. 测度与解析前端

在 1≤t≤2、1≤z≤1.4 上，dt ds=t dt dz。
共同缩放不变候选的原坐标残差积分为

\[
\int|E|^2dt ds=\frac38\int|R(z)|^2dz.
\]

直接二维候选 φ=t U(log t,s/t) 则用
∫exp(-2y)|t²E|²dy dz；训练与最终验证使用不同采样/求积。

在普通点，可由第三阶正规形 F'''=G 求
F''''=G_z+F'G_F+F''G_(F')+G G_(F'')，
得到第四阶 Taylor 先验。该先验的局部解析性来自正规形；
本次没有证明 Taylor 级数覆盖整个测试区间。

## 7. 构造参考解族的区间一致正则性

对本次固定数据 g=1、κ=1/30、m∈[1,4]、
(F,F',F'')(1)=(2,1/2,1/10)，可证明整个 z∈[1,7/5] 上

\[
2\le F\le56/25,\quad 1/2\le F' <3/5,\quad
V=F-zF'\ge29/25>0.
\]

证明采用 P<3/5 的 bootstrap。I0>0，所以 L>0 的分支上 P'=I0/L>0。
由 P∈[1/2,3/5] 得 F 的上述上下界和 V 下界，输沙项为正。
原文模型有 I0≤11/25，且

\[
L\ge(25/9)z-(3/5)z^3\ge98/45.
\]

后一函数在区间上凹，最小值在端点。于是
P(z)-1/2≤99/1225<1/10，无法触及 P=3/5。

修正模型有 I0≤149/100，且

\[
L\ge\ell(z)=(3/2+z/2)(125/27-z^2)>0.
\]

ℓ 在区间上严格递减，故用四段精确右端 Riemann 和可得

\[
P(z)-1/2\le
\frac1{10}\sum_{i=1}^4\frac{149/100}{\ell(1+i/10)}
<1/10.
\]

同样不能触及 barrier。紧致正则管中的 ODE 延拓定理保证整个区间存在。
因此这是对连续参数 m∈[1,4] 的参考解族证明，超出仅检查六个离散 m 值。
确切分数与 barrier slack 保存于 `reference_tube_certificates.json`。
训练候选的区间界仍仅按网格检查，此参考解定理不自动转移给候选。

## 8. 参考与归属

- Peter J. Olver, *Applications of Lie Groups to Differential Equations*,
  Chapter 2（延拓与方程流形切向条件），Chapter 3（不变解约化）。
- Francesco Oliveri, *Lie Symmetries of Differential Equations: Theory,
  Applications, and Symbolic Computation*, Chapter 11（近似对称性的不同框架）。
- A. Paliathanasis, G. Leon, P. G. L. Leach,
  [Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables](https://doi.org/10.3390/math14030433),
  *Mathematics* 14 (2026), 433。原文方程和 X5 的归属在此；
  对流修正、局部相容性和上述障碍证明按本次独立推导处理。
- 本次推进基于 2026-10-10 的 `main(1).tex` 和 `interim report week 3.docx`，
  未覆盖或重写其历史结果。
