# 一维 SVE：从原方程到最大点对称、约化与数据检查

本文记录 2026-10-20 周期中**已经独立评审接受的 1D 数学结果**。依据是
[分类评审](</D:/MATHs/math 4890 LieML/build/sve-general-symm-20261020/CLASSIFICATION_REVIEW.md>)
和[数据／父模型评审](</D:/MATHs/math 4890 LieML/build/sve-general-symm-20261020/DATA_PARENT_REVIEW.md>)。
这些接受结论针对评审回执绑定的源码、方程与假设。

目前可以支持：声明的八个连续参数分支的局部最大光滑 Lie 点代数，已实现的行波／齐次缩放约化，以及指定初值和构造解的检查。
**一维阶段门槛已闭合，证据见 `STAGE_1_GATE.json`。** 一维子代数在连通内伴随作用
与生成元非零倍数下的完整性、非冗余性已获独立评审接受。八个子脚本全部执行成功，
本轮 134 项测试、现有 engine/chart 51 项及活动包 43 项测试通过，data-flux 与 workflow 通过。
项目总审计仍失败：234 项问题与上一周期完全一致，门槛明确保留了这一限定，未将其改写为通过。

## 1. 我们研究的变量和方程

空间只有一个方向 $x$，时间为 $t$。三个未知函数是水深 $h(t,x)$、水平速度 $u(t,x)$ 和总床面高程 $B(t,x)$。水面高程是 $h+B$。
常数 $g>0$ 表示重力系数；$K\geq0$ 控制随水流运动的输沙项；$G\geq0$ 控制沿床面下坡方向的输沙项。

完整耦合系统为

\[
\begin{aligned}
E_h&=h_t+(hu)_x=0,\\
E_u&=u_t+uu_x+g(h_x+B_x)=0,\\
E_B&=B_t+J_x=0,\qquad
J=K|u|^{m-1}u-G|u|^nB_x.
\end{aligned}                                                    \tag{1}
\]

第一行是水量守恒，第二行是速度的动量方程，第三行说明床面如何随沉积通量的空间变化而改变。床面也是未知函数，不能擅自把它当作任意给定地形。

分类先在开集

\[
h>0,\qquad u>0,\qquad g>0
\]

进行，因此 $J=Ku^m-Gu^nB_x$，实数指数也有明确含义。正输沙分支的范围是 $1\leq m\leq4$，两条坡度路线是 $n=m-1$ 和 $n=m$。当 $K=0$ 时，$m$ 已经不出现在方程里；当 $G=0$ 时，$n$ 同样应删除。

这里使用的是所声明闭合律的精确数学模型。底床坡度相关的物理模型还可能含阈值、方向规则和其他闭合项；不能把式 (1) 自动称为所有这些模型的完整复现。

若改用动量变量 $p=hu$，在 $h>0$ 上有可逆点变换 $u=p/h$，并且

\[
(hu)_t+(hu^2+gh^2/2)_x+ghB_x=hE_u+uE_h.                 \tag{2}
\]

所以原始量与动量量表示的光滑方程可以相互转换。这不包含干床 $h=0$ 或激波弱解的等价定理。

## 2. general-symm 实际做了什么

一个 Lie 点生成元写成

\[
X=\tau\partial_t+\xi\partial_x
  +\eta_h\partial_h+\eta_u\partial_u+\eta_B\partial_B.    \tag{3}
\]

最初的五个系数都是 $t,x,h,u,B$ 的任意光滑函数。它们不是先猜好的常数、线性函数或论文中的生成元列表。

程序和证明按以下顺序工作：

1. 输入原 PDE、变量、固定参数和分支条件。参数代入后的**同一组方程**同时用于延拓与方程流形，避免检查的方程和消元的方程不一致。
2. 建立导数坐标、全导数，以及特征
   $Q_i=\eta_i-\tau (U_i)_t-\xi (U_i)_x$，其中 $U=(h,u,B)$。
3. 用链式法则延拓 $X$，要求
   $\operatorname{pr}X(E_i)|_{\mathcal E}=0$。这表示变换后的方程在原方程的解上仍成立。
4. 在合法的方程流形上消去规定的导数，再按其余自由导数分离系数，得到确定方程。参数不是自由导数，不能被误当成独立变量分离。
5. 对声明的 SVE 系统，完整积分这些必要方程，记录每次分支和除法条件；最后把所得通解回代全部确定方程和原 PDE 延拓式，检查充分性。
6. 从通解对自由常数求导，得到代数基；随后才计算括号、伴随作用、不变量、约化和数据限制。

为什么这次可以说“最大”？因为独立评审接受了**任意系数的必要方程已经穷尽积分**，随后又检查了充分性。只找到几个有效生成元，最多给出代数维数的下界。

`main.py` 的延拓和确定方程构造具有通用接口；`classification.py` 的积分步骤使用已证明的 SVE 专用结构。它不是能够自动积分任意非线性 PDE 确定方程的普遍算法。未知模型必须保留未解决状态。

## 3. 通解给出的实际基

用三个最直观的生成元表示时间、空间和床面基准平移：

\[
T=\partial_t,\qquad P_x=\partial_x,\qquad Z_B=\partial_B.
\]

### 没有坡度扩散时：$G=0$

已求得的全部系数为

\[
\tau=(\beta+a)t+c_t,\quad \xi=\beta x+c_x,\quad
\eta_h=-2ah,\quad\eta_u=-au,\quad\eta_B=c_B-2aB.
                                                               \tag{4}
\]

当 $K>0$ 时，剩余条件是 $K(m-3)a=0$。因此定义

\[
D=t\partial_t+x\partial_x,\qquad
S=t\partial_t-2h\partial_h-u\partial_u-2B\partial_B,
\]

便有 $X=c_tT+c_xP_x+c_BZ_B+\beta D+aS$。一般 $m\ne3$ 必须取 $a=0$；$m=3$ 时允许额外的 $S$。当 $K=0$ 时输沙项整个消失，$a$ 也可以自由取值，而 $m$ 不再是模型参数。

### 有坡度扩散时：$G>0$

必要方程最后留下两个常数条件

\[
\theta+(2-n)d=0,\qquad mK(m-3)d=0,                      \tag{5}
\]

其中 $\theta$ 是时间缩放的常数系数。消去它后，可以把全部系数直接写为

\[
X=c_tT+c_xP_x+c_BZ_B+d\mathcal D_n,
\]
\[
\mathcal D_n=(n-2)t\partial_t+(n-1)x\partial_x
              +2h\partial_h+u\partial_u+2B\partial_B.   \tag{6}
\]

若 $K>0,m\ne3$，必须有 $d=0$。若 $K=0$ 或 $m=3$，则 $d$ 自由。$n=0,1,2$ 没有产生额外的代数维数；证明没有通过除以这些可能为零的数来丢掉分支。

尤其要区分

\[
\mathcal D_2=x\partial_x+2h\partial_h+u\partial_u+2B\partial_B,
\]
\[
\mathcal D_3=t\partial_t+2x\partial_x+2h\partial_h+u\partial_u+2B\partial_B.
\]

两个三次输沙分支的额外生成元不同，不能把 $n=2$ 的“纯空间缩放”照搬到 $n=3$。

### 八个连续参数分支

下表所有行都带有 $g>0,h>0,u>0$。每行表示一个连续参数族或一个明确的特殊层，不是几个离散指数的数值抽样。

| 程序分支 | 参数范围 | 最大局部点代数的一组基 | 维数 |
|---|---|---|---:|
| `grass_generic` | $K>0,G=0,1\leq m\leq4,m\ne3$ | $T,P_x,Z_B,D$ | 4 |
| `grass_cubic` | $K>0,G=0,m=3$ | $T,P_x,Z_B,D,S$ | 5 |
| `zero_transport` | $K=G=0$，无 $m,n$ | $T,P_x,Z_B,D,S$ | 5 |
| `slope_attachment_generic` | $K,G>0,n=m-1,1\leq m\leq4,m\ne3$ | $T,P_x,Z_B$ | 3 |
| `slope_attachment_cubic` | $K,G>0,m=3,n=2$ | $T,P_x,Z_B,\mathcal D_2$ | 4 |
| `slope_source_generic` | $K,G>0,n=m,1\leq m\leq4,m\ne3$ | $T,P_x,Z_B$ | 3 |
| `slope_source_cubic` | $K,G>0,m=3,n=3$ | $T,P_x,Z_B,\mathcal D_3$ | 4 |
| `slope_only` | $K=0,G>0,0\leq n\leq4$，无 $m$ | $T,P_x,Z_B,\mathcal D_n$ | 4 |

$m=3$ 的特殊性有可检查的原因：对额外坡度生成元的原方程延拓，剩余床面残差是

\[
mK(m-3)u^{m-1}u_x.                                     \tag{7}
\]

因为要求对自由的 $u_x$ 恒成立，正 $K$ 分支只有 $m=3$ 能让这一额外自由度留下来。这个必要条件与完整的其余确定方程共同构成分类证明。

## 4. 负速度与等价变换的准确范围

对式 (1) 的 signed absolute-value 通量，反射

\[
(t,x,h,u,B)\longmapsto(t,-x,h,-u,B)                     \tag{8}
\]

可逆，三个残差分别乘以 (1,-1,1)。独立评审接受了这个恒等式，因此可以通过共轭把正速图的最大点代数转移到负速图。这里没有把任意实数幂 $u^m$ 直接代入负数，也没有穿过 $u=0$。

已验证的正缩放子群为

\[
t'=at,\quad x'=bx,\quad u'=(b/a)u,\quad h'=Ch,\quad B'=CB+d_0,
\qquad a,b,C>0,
\]
\[
g'=\frac{b^2}{a^2C}g,\quad
K'=C(a/b)^{m-1}K,\quad
G'=b^{2-n}a^{n-1}G.                                    \tag{9}
\]

这会同时改变参数，一般属于不同方程之间的等价变换；只有变换保持既定参数时，才能把它作为那一个固定方程的对称。令 $r=b/a$，则 $g'K'=r^{3-m}gK$，故 $gK$ 在三次层上是**这个已验证子群**的一个不变量。

完整点等价群胚——所有方程之间所有可能的可逆局部点变换——仍未分类。未知的额外等价只会使当前覆盖表可能冗余；它不能成为删除分支的理由。声明族的最大 Lie 点代数覆盖，与完整点等价群胚，是两个不同的结论。

## 5. 什么时候对称真的能压缩变量

可以把 Lie 代数理解为可供选择的“变量压缩方向”。但方向有效还不够：需要生成元在 $(t,x)$ 上确有非零投影、存在可逆的局部坐标图，并且所选解图满足 $Q=0$。

最直接的例子是所有分支都含有的 $T+cP_x$。其不变量为

\[
z=x-ct,\qquad h=H(z),\quad u=U(z),\quad B=W(z).
\]

由两个自变量变成一个后，原方程精确变为

\[
\begin{aligned}
\big((U-c)H\big)'&=0,\\
\big((U-c)^2/2+g(H+W)\big)'&=0,\\
\big(KU^m-GU^nW'-cW\big)'&=0.
\end{aligned}                                                    \tag{10}
\]

零系数分支删除对应项，仍要求 $H>0,U>0$。已实现的约化把原 PDE 的直接回代结果与约化方程逐行比较。最高导数的系数矩阵保持隐式，没有为了得到显式 ODE 而丢弃静止或声速等奇异位置。

对已验证的齐次缩放

\[
X=\alpha t\partial_t+\beta x\partial_x+
\gamma_h h\partial_h+\gamma_u u\partial_u+\gamma_B B\partial_B,
\]

当 $\alpha\ne0,t>0$ 时，可取 $z=xt^{-\beta/\alpha}$ 及

\[
h=t^{\gamma_h/\alpha}H(z),\quad
u=t^{\gamma_u/\alpha}U(z),\quad
B=t^{\gamma_B/\alpha}W(z).
\]

当 $\alpha=0,\beta\ne0,x>0$ 时，要换为空间轨道图，以 $t$ 作剖面变量。于是 $n=2$ 虽然没有改变点代数维数，却必须改变 $mathcal D_n$ 的约化图。这个区别不能通过把含 $1/(n-2)$ 的公式硬代入 $n=2$ 来处理。

这些结果证明了相应不变图上的**自变量维数约化**。它们没有自动证明任意剖面存在、ODE 阶数已经降低，或所有一维子代数都已有不重复的代表。已审查的括号和伴随矩阵也不等于一个已审查完成的最优子代数系统。

## 6. 方程对称、某个解的不变性、初值稳定子

这三个问题必须分别问：

| 问题 | 要检查什么 | 能推出什么 |
|---|---|---|
| $X$ 是方程对称吗？ | 原方程上的延拓恒等式 | 它把局部解变成局部解。 |
| 某一个完整解图在 $X$ 下不变吗？ | 这个解上的 $Q=0$ | 这个解可以属于对应的不变解族。 |
| 给定初值在 $X$ 下不变吗？ | 初始面和初始图的切向条件 | 这个变换保持该组初始数据；不自动保证以后的边界数据。 |

例如，$Z_B=\partial_B$ 保持方程，因为方程只使用床面导数；但它改变指定的床面初值。并且单独的 $Z_B$ 有 $Q_B=1$，没有固定的普通解图，也不能据此消去一个独立变量。

固定初始时刻 $t=t_0$，给定 $U_0(x)=(h_0,u_0,B_0)$，稳定子由已求的一般系数再满足

\[
\tau|_{t_0}=0,\qquad
\eta_i|_{U_0,t_0}-\xi|_{U_0,t_0}U'_{0,i}(x)=0            \tag{11}
\]

得到。若端点固定，还要求 $\xi(a)=\xi(b)=0$。程序直接求这些条件对原自由常数的线性限制，保留不能证明非零的主元条件及对应未处理的零主元分支。

取具体初值 $h_0=2,u_0=3$，床面分别为 $1,1+x,1+x^2$，结果为：

| 方程分组 | 平床初值 | 非零线性床初值 | 二次床初值 |
|---|---:|---:|---:|
| $G=0$ 的三个分支 | 2 | 1 | 0 |
| $G>0$ 的五个分支 | 1 | 1 | 0 |

这些数是该组**初值稳定子**的维数，不是整条 PDE 的对称维数。线性床与二次床初值也没有被宣称为时间不变的解。对均匀初值再固定两个不同端点，会消去剩余的这些基底运动。

若还指定沉积通量，必须检查其实际值是否兼容，并使用

\[
\eta_{B_x}=D_x\eta_B-B_tD_x\tau-B_xD_x\xi
\]

计算通量的变化，不能只变换 $u$ 而漏掉床面斜率。当前通量数据检查的范围是初始切片；写下一个依赖 $t$ 的通量表达式，也不会自动得到整段未来边界上的不变性结论。

## 7. 两类精确流动与零速反例

全部八个分支都通过了完整原 PDE 的独立回代：

\[
h=H_0,\quad u=U_0,\quad B=B_0,
\]

以及恒坡加速流

\[
h=H_0,\quad u=U_0-gk(t-t_0),\quad B=kx+B_0.             \tag{12}
\]

限制是 $H_0>0$ 和所用时间区间内 $u>0$。式 (12) 的动量方程给出 $u_t=-gk$。其沉积通量可以随时间变化，但沿 $x$ 不变，所以 Exner 方程仍成立。

零速度不在本次最大点代数分类的开图内。另设的湖泊控制只在 signed 闭合可光滑写成多项式的明确分支使用 $u=0$：活跃输沙指数取 $m=1,3$，活跃扩散指数取 $n=0,2,4$。一般实指数不在零点强行求值，也不据这些构造解扩展最大代数结论。

一个重要的负控制是 $K=0,G>0,n=0$：

\[
B=x^2,\quad u=0,\quad h=L_0-x^2
\]

虽然水面平坦，床面残差却为 $-2G\ne0$。它不是解。但不能因此排除所有随时间改变水面的情形。配对地取

\[
B=x^2+2Gt,\quad L=L_0+2Gt,\quad h=L-B=L_0-x^2,\quad u=0
\]

后，三条残差都为零；仍须限制在 $h>0$ 的区域。是否成立由全部 PDE 决定，不能仅凭“水面是否静止”判断。

## 8. 打印标量 P 与修正标量 M：一个明确的分离例子

本节仅作为 $G=0$、$g,K>0$ 的父模型控制。它没有参与上面的全耦合点代数证明。

一维质量方程允许局部构造物质标签 $s$：

\[
ds=h\,dx-hu\,dt.
\]

在 $h>0$ 上，局部逆映射记为 $x=\phi(t,s)$。为避免和动量 $p=hu$ 混淆，这里另记

\[
r=\phi_s>0,\qquad v=\phi_t>0,\qquad h=1/r,
\]
\[
A=r\phi_{tt}-g\frac{\phi_{ss}}{r^2},\qquad
C=mKv^{m-1}\frac{\phi_{ts}}r.
\]

两个标量残差分别是

\[
P=D_tA-gD_sC,\qquad
M=P-D_s(vA/r).                                         \tag{13}
\]

区别来自固定空间点的时间导数与随物质标签的时间导数不同：

\[
D_x=r^{-1}\partial_s,\qquad
D_t|_x=\partial_t-(v/r)\partial_s.
\]

原动量方程给出物质床面的 $B_s=-A/g$。保留正确的物质输运后，原 Exner 方程要求

\[
B_t=-\frac{vA}{gr}-C,
\]

而打印标量构造使用的是 $B_t=-C$。让两个床面偏导数兼容，分别得到 $M=0$ 与 $P=0$。

取非常简单的

\[
\phi(t,s)=\frac{s^2}{2}+ct,\qquad s,c,g>0.
\]

此时 $r=s,v=c,A=-g/s^2,C=0$，所以

\[
P=0,\qquad M=-\frac{3gc}{s^4}\ne0.                     \tag{14}
\]

这个精确例子说明：一个打印标量方程的解，不能自动当作修正物质方程或全耦合 SVE 的解。质量标签的构造依赖具体解，也不是原 Eulerian 点空间上的普通局部点变换。床面重构还需要闭性、局部单连通图或零周期条件、一个床面基准常数，以及相容的床面数据。

## 9. 原始文献与可定位的出处

下表使用父模型回执中已经记录的原始来源及页码／公式锚点。数据／父模型评审确认本地文件哈希与既有来源账本一致；**这次核对不是新一轮网页检索，也不是新的书目内容审计。** 这些文献支撑模型来源和标准方法，不等于本周期已经证明文献首创。

| 来源 | 在本文中的用途与原文定位 |
|---|---|
| Paliathanasis，2022，*Lie Symmetry Analysis of the One-Dimensional Saint-Venant-Exner Model*，DOI [10.3390/sym14081679](https://doi.org/10.3390/sym14081679) | R02，PDF 第 2 页式 (1)–(4)：全耦合 1D 父模型；第 4 页 Proposition 1、式 (24)–(25)：论文所报告生成元的比较位置。本文基由确定方程通解导出。 |
| Paliathanasis、Leon、Leach，2026，*Lie Symmetries and Similarity Solutions for a Shallow-Water Model with Bed Elevation in Lagrange Variables*，DOI [10.3390/math14030433](https://doi.org/10.3390/math14030433) | R01，PDF 第 2 页式 (1)–(7)：Eulerian 表述、打印物质方程与标量 P；第 4 页 Proposition 1、第 6–7 页表 3 与式 (25)–(27)：标量结果的来源定位。 |
| Fernández-Nieto 等，2017，*Formal deduction of the Saint-Venant-Exner model including arbitrarily sloping sediment beds and associated energy*，DOI [10.1051/m2an/2016018](https://doi.org/10.1051/m2an/2016018) | R04，印刷第 116 页式 (1.1)、Grass 段和式 (1.2)：固定基底、活动沉积层与 signed 输沙律；第 117–118 页式 (1.5)–(1.9)：坡度及阈值闭合的范围。 |
| Castro Díaz 等，2009，*Two-dimensional sediment transport models in shallow water equations. A second order finite volume approach on unstructured meshes*，DOI [10.1016/j.cma.2009.03.001](https://doi.org/10.1016/j.cma.2009.03.001) | R03，PDF 第 3–5 页式 (2)、(4)–(8)：耦合输沙和床面符号的来源背景；第 2 页说明不连续处的非守恒项需要选定弱解框架。这里不据此给出二维分类结果。 |
| Olver，1986 第一版，*Applications of Lie Groups to Differential Equations*，DOI [10.1007/978-1-4684-0274-2](https://doi.org/10.1007/978-1-4684-0274-2) | R07，印刷第 106–107 页 Theorem 2.31、第 113 页 Theorem 2.36，以及第 162、165 页 Definition 2.70／Theorem 2.71：无穷小准则、延拓公式及必要性所需条件。 |
| Anderson、Fels、Torre，2000，*Group Invariant Solutions Without Transversality*，DOI [10.1007/s002200000215](https://doi.org/10.1007/s002200000215) | R08，印刷第 2–3 页式 (2.3)–(2.8)、第 5–6 页 Definition 3.1 与式 (3.2)–(3.4)：不变图、投影秩、横截性和约化条件。 |

## 10. 当前结论与尚未完成的工作

| 项目 | 本文可采用的状态 |
|---|---|
| 八个声明分支的局部最大光滑点代数 | 独立分类评审已接受；作用于声明的正深、非零速度图及所绑定版本。 |
| signed 负速反射、实现的约化图与伴随约定 | 分类评审附录已接受其明确范围。 |
| 指定初值稳定子、通量、构造解与 P/M 控制 | 数据／父模型独立评审已接受其明确范围。 |
| 一维子代数完整性／最优代表系统 | `SUBALGEBRA_REVIEW.md` 接受其在连通内伴随加线倍乘等价下的完整性和非冗余性；不包含外自同构或高维子代数。 |
| 本轮项目验证 | data-flux、workflow、134+51+43 项测试通过；总审计仍有 234 项未变化旧问题。原始日志在 `runs/stage1-validation/`。 |
| `STAGE_1_GATE` | 已通过，绑定八分支运行、当前源码及独立评审；完整等价群胚仍单独未解决。 |
| 完整点等价群胚 | 单独未解决；只使用已验证的变换，不据猜测合并覆盖分支。 |

进一步查阅可从
[一阶必要性推导](</D:/MATHs/math 4890 LieML/build/sve-general-symm-20261020/FIRST_ORDER_DERIVATION.md>)、
[坡度族必要性推导](</D:/MATHs/math 4890 LieML/build/sve-general-symm-20261020/SLOPE_DERIVATION.md>)
及两份独立评审进入。本文不主张任意初边值问题适定性、全局解、激波理论、学习误差保证或神经方法优势。
