# LieML / SVE 项目第一性原理审计

**审计日期：** 2026-10-01  
**审计对象：** `draft/main.tex`、[归档的第二周 interim report](<../.old/2026-11-17-42f5654/draft/interim report week 2.docx>)、源论文 PDF、现有 SVE 证书与聚焦测试  
**当前设计阶段：** 架构审查；本文不授权修改生产算法或把未证结果写成结论

## 执行判定

项目有一个可靠但范围很窄的数学锚点：在打印的标量 Lagrangian 基准方程、固定 (m=3)、指定正则局部 chart 上，

\[
X_5=t\partial_t-2s\partial_s,
\qquad \sigma=st^2,
\qquad \phi(t,s)=F(\sigma)
\]

给出精确的一维轨道约化；当前代码还精确检查了 invariant-surface condition、off-shell multiplier identity、pullback identity 和若干非零 guard。这一部分应保留。

项目目前**没有**证明：generic-(m) 最大点对称代数、完整的 (4\to5) 维数跳跃、(m=3+\delta) 的近似生成元、一般 series engine、结构级 ML 优势、奇异分支、全局/IBVP 等价性或物理 Eulerian SVE 的完整等价约化。现有 `eta_ic` 实验改变的是约化 ODE 的初始曲率，不是输运指数 (m)。

最强且可证伪的研究方向不是“用神经网络解一个已经很便宜的 ODE”，而是：

> 对许多同类、已规范化、分支明确的 PDE 查询，ML 只提出确定算子核的候选支持/子空间或计算成本预测；exact solver 和 branchwise verifier 决定数学有效性，并在拒绝时回退到完整符号/线性代数流程。

若这种 warm start 在相同输出与验证标准下不能降低总成本，它就没有算法价值；这应被允许成为论文的负结论。

---

# A. 第一性原理数学重构

## A.1 “一个 PDE”应是什么对象

不要把所有 PDE 当成同一个欧氏参数向量。建议使用分层对象

\[
\mathscr P
=\bigsqcup_{\tau\in\mathcal T}
\bigl[\Theta_\tau/\mathcal G_\tau\bigr].
\]

- (\tau) 是**结构签名**：独立变量数 (p)、场数 (q)、方程表示数 (r)、bundle/field type、局部或非局部算子类别、整数最高阶、定义域与数据几何、函数空间、允许的等价变换。
- (\Theta_\tau) 是固定结构签名内的参数空间：连续系数、固定实分支上合法的实指数、外力或数据参数。
- (\mathcal G_\tau) 是明确声明的等价群或群胚：变量/场重命名、允许的缩放、方程的可逆组合等。
- (r) 是输入表示中的方程条数；加入冗余微分后果会改变 (r)，所以它不总是微分理想的内在不变量。

参数必须分类，而不是都放进同一个 `lambda`：

| 类型 | 例子 | 数学地位 |
|---|---|---|
| 模型参数 | (g,m,\beta_{\rm tr}) | 固定结构签名内可连续变化，但需保留 branch/单位/定义域 |
| 数据参数 | `eta_ic`、边界幅值 | 改变 IVP/IBVP，不一定改变 PDE |
| 积分常数 | (C,K) | 解族坐标，不是模型参数 |
| 群参数 | (\varepsilon) | 沿群轨道移动，不是 (m-3) |
| 离散结构 | (p,q)、整数阶数、耦合拓扑 | 一般不应伪装成连续坐标 |
| 非局部算子语义 | Caputo/RL/Riesz、下限、kernel、history space | 算子类型是离散结构；固定类型后 (\alpha) 才可连续 |

因此 (\alpha=1\) 与 (\alpha=1/2) 不能默认共用经典有限 jet prolongation。它们可以共用上层接口，但应进入不同 backend。

## A.2 方程、分支与完成

固定结构和参数后，令 (E\to X) 为场丛，局部坐标为

\[
x=(x^1,\ldots,x^p),\qquad
u=(u^1,\ldots,u^q).
\]

一个 PDE 输入不是单独的字符串 (\Delta=0)，而是

\[
\mathcal P_{\lambda}
=\bigl(\Delta=0,\;G\ne0,\;A,\;\mathcal D\bigr),
\]

其中 (G\ne0) 记录分母、leading coefficient 和局部 chart 的 guard，(A) 记录符号/实分支/正则性假设，(\mathcal D) 记录定义域和初边值数据。第 (b) 个 regular branch 是

\[
\mathcal E_{\lambda,b}^{(n)}
=\{\Delta=0,\;G_b\ne0,\;A_b\}\subset J^n(E).
\]

只有在 Jacobian 常秩时它才是光滑方程子流形。对称应作用在含全部微分后果的 (\mathcal E_{\lambda,b}^{(\infty)})，或等价的 regular/radical differential ideal 上。否则 (F=0) 与 (F^2=0) 这类同解集表示会让 naive on-shell tangency 产生假对称。

## A.3 “异常参数”必须拆成四个集合

在固定 transformation class、regular branch 和有限型假设下，可以定义

\[
\Sigma_{\dim,b}
=\{\lambda:\dim\mathfrak g_{\lambda,b}>d_{\rm gen,b}\}.
\]

但这只表示 algebra dimension jump。还必须分开：

1. (\Sigma_{\rm alg})：维数不变但 bracket/isomorphism type 改变；
2. (\Sigma_{\rm orb}\subset\Lambda\times E)：evaluation 或 projected-orbit matrix 的秩下降；
3. (\Sigma_{\rm red})：某一 branch、subalgebra 和数据组合失去 transversality/admissibility；
4. (\Sigma_{\rm op})：最高阶系数变零、方程阶数或微分结构改变。

线性 PDE 还要先分离无限维的 solution-superposition ideal。否则“generic dimension”可能没有有限基准。

对 SVE，源论文报告 generic (m) 的点代数为四维、(m=3) 增加 (X_5)。本项目独立证明的是：给定 (X_5) 在 (m=3) 被接纳，而在 (m=4) 的同一 identity 失败。后者只是否定这个候选，不是 generic-(m) 完整分类。

## A.4 exact、near、approximate、perturbative 和 small residual

- **Exact symmetry：** branch normal form 中 (\mathcal A_{\lambda,b}X=0) 严格成立。
- **Near symmetry：** 在已固定方程/生成元归一化、范数、区域和候选类后，defect 数值较小。
- **(N) 阶 approximate symmetry：** 存在 (X_\delta=\sum_{j=0}^N\delta^jX_j)，使正规形 determining residual 为 (O(\delta^{N+1}))。
- **Perturbative continuation：** 每一阶线性方程可解；它本身不证明级数收敛，也不证明附近存在 exact symmetry curve。
- **Small solution residual：** 某个候选解的 (\Delta[u]) 小；没有稳定性/后验估计时，它不控制解误差，更不证明对称。

这五个概念不能互换。

---

# B. 修正后的对象与映射层级

## B.1 几何与计算链

推荐的严格链条是

\[
\begin{aligned}
E\to X
&\longrightarrow J^n(E)
\supset \mathcal E_{\lambda,b}^{(n)}
\longrightarrow \mathcal E_{\lambda,b}^{(\infty)}\\
&\longrightarrow X
\longrightarrow \operatorname{pr}^{(n)}X
\longrightarrow \mathcal A_{\lambda,b}(X)=0\\
&\longrightarrow \mathfrak g_{\lambda,b}
\longrightarrow \mathfrak h\le\mathfrak g_{\lambda,b}
\longrightarrow \mathcal O_{\mathfrak h}
\longrightarrow \text{rank strata}\\
&\longrightarrow \text{local quotient/chart}
\longrightarrow Q_s^\alpha=0
\longrightarrow \mathcal R[U]=0
\longrightarrow \text{reconstruction certificate}.
\end{aligned}
\]

这里

\[
X=\xi^i(x,u)\partial_{x^i}+\phi^\alpha(x,u)\partial_{u^\alpha},
\qquad
Q^\alpha=\phi^\alpha-\xi^iu_i^\alpha.
\]

在 branch (b) 上，确定算子应是

\[
\mathcal A_{\lambda,b}(X)
=\operatorname{Split}\operatorname{NF}_b
\bigl(\operatorname{pr}X(\Delta_\lambda)\bigr).
\]

候选 (k)-维子代数 (\mathfrak h=\langle X_1,\ldots,X_k\rangle) 必须 bracket-closed。令 (\Xi=(\xi_s^i)) 为基空间投影矩阵；在常秩层上，完全不变图至少要求

\[
\operatorname{rank}\Xi
=\operatorname{rank}[\Xi\mid\Phi].
\]

若有效 projected orbit rank 是 (k_b)，独立变量只从 (p) 降到 (p-k_b)。所以一维对称通常只完成 (p\to p-1)；只有 (p=2,k_b=1) 时才直接得到 ODE。vertical symmetry 可能 (\dim\mathfrak g>0) 却完全不降低独立变量。

PDE symmetry 只保持完成后的 differential equation。IBVP symmetry 还必须保持定义域、边界分片和数据 differential ideal。某个 invariant ansatz 与某组人工数据相容，不等于整个物理 IBVP 被群保持。

## B.2 SVE 锚点的独立审计

### 正确且应保留的链

从

\[
X_5=t\partial_t-2s\partial_s
\]

积分得到

\[
(t,s,\phi)\mapsto(e^\varepsilon t,e^{-2\varepsilon}s,\phi).
\]

特征方程

\[
\frac{dt}{t}=\frac{ds}{-2s},\qquad d\phi=0
\]

给出 (\sigma=st^2)。图上的 invariant-surface condition 是

\[
Q=-t\phi_t+2s\phi_s=0,
\]

因此 (\phi=F(st^2))。`main.tex` 当前的 (X_5)、flow、(\sigma) 和 ansatz 已一致，不应为了迎合旧版疑问而改号。

### 对所有 (m) 的精确 defect identity

令

\[
q_m=\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}.
\]

直接 prolongation 给出

\[
\operatorname{pr}X_5(E_m)
=-E_m+g\beta_{\rm tr}(m-3)D_s(q_m).
\]

所以 (m=3) 时 multiplier 是 (-1)，而固定不变的 (X_5) 在 (m=3+\delta) 通常留下 (O(\delta)) defect。这只是“未修正候选的一阶破缺”，不是 (O(\delta^2)) approximate symmetry。

### 直接约化方程

令 (p=F',q=F'',r=F''')，则

\[
\phi_s=t^2p,
\quad \phi_t=\frac{2\sigma p}{t},
\quad \phi_{ss}=t^4q,
\quad \phi_{ts}=2t(p+\sigma q),
\quad \phi_{tt}=\frac{2\sigma p+4\sigma^2q}{t^2}.
\]

定义

\[
A=2\sigma p^2+4\sigma^2pq-gq/p^2,
\qquad
B=8\sigma^2p(p+\sigma q).
\]

则当前打印基准方程满足精确 pullback

\[
E_3[F(st^2)]=t^{-1}R_0[F],
\qquad
R_0=2\sigma A'-g\beta_{\rm tr}B'.
\]

这才是项目当前可复现的工作约化方程。

### 源论文打印式的冲突

源 PDF 的 Eq. (25) 按页面转录为

\[
P=4\sigma p^3q(\sigma q+3p)+2gq^2
+\beta\sigma[(\sigma q+5p)(\sigma q)+(2p+\sigma^2r)p].
\]

论文随后给出的 power law 在 (g=1,\beta=0.1,\sigma=1) 时产生

\[
P=-13.2970804147,
\]

而代入从 Eq. (7) 直接推导的 (R_0) 则严格为零。因此这不是整体非零乘子的差异。发表前应把它写成“Eq. (25) 与 Eq. (7) 的直接代入冲突，等待作者/勘误核实”，并把直接重推的 (R_0) 作为项目计算的权威对象；不要简单宣布原文错误而不保留复核记录。

### 物理链条的边界

若 (b(t,s)=B(t,\phi(t,s)))，Eulerian pullback 包含

\[
b_t-\frac{\phi_t}{\phi_s}b_s
+\beta_{\rm tr}\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}=0.
\]

源论文中间 Eq. (6) 省略了 (-(phi_t/\phi_s)b_s)。因此当前打印标量 Eq. (7) 可作为明确定义的 benchmark equation，但暂时不能称为已认证等价于完整 Eulerian SVE system。历史 Eulerian 三场模型中的 (O(\delta^2)) 曲线也不能转移为这里的 Lagrangian 证据。

## B.3 近异常一阶方程的几何含义

写

\[
E_\delta=E_0+\delta E_1+O(\delta^2),
\quad
Y_\delta=Y_0+\delta Y_1+O(\delta^2),
\quad
\operatorname{pr}Y_0(E_0)=c_0E_0.
\]

一阶条件

\[
\left(
\operatorname{pr}Y_1(E_0)
+\operatorname{pr}Y_0(E_1)
-c_0E_1
\right)\big|_{E_0=0}=0
\]

就是线性化 determining equation

\[
\mathcal A_0Y_1=-\mathcal A_1Y_0.
\]

可解当且仅当右侧落在 (\operatorname{im}\mathcal A_0)；其在 cokernel 中的类是 obstruction。(Y_1) 只有在存在一条可微 exact-symmetry curve 时才可解释为真实曲线的切向量；一般情况下它只是形式 lift，并且模 (\ker\mathcal A_0) 不唯一。这不是 orbit transversality 的同义词。

## B.4 series engine 的正确输出

`SeriesCertificate` 不应只返回系数表，而应至少记录：

1. expansion type：Taylor、Laurent、Puiseux、Frobenius-log 或扇区渐近；
2. expansion point/domain、branch 与 regularity guards；
3. valuation/dominant balances、indicial equation 和 resonance；
4. coefficient constraints、recurrence DAG、自由初值或自由函数；
5. 截断阶和代回原/约化方程后的精确 residual order；
6. `formal-only | asymptotic | convergence-proved | interval-bounded | empirical`；
7. 已证明的收敛半径下界与仅数值估计的最近奇点分开；
8. analytic continuation charts、monodromy（若适用）、复杂度和 provenance。

对 (p) 个变量的总阶 (N) Taylor jet，未约束系数规模约为

\[
q\binom{N+p}{p}.
\]

经 projected rank (k) 的对称约化后变为

\[
q\binom{N+p-k}{p-k}.
\]

因此“symmetry-assisted series reduction”是清晰的算法对象，但 quotient chart 也可能引入新奇点，不能先验声称它一定改善收敛。

## B.5 Lie 代数结构、表示论与 reduction 的真实关系

对称引擎首先必须返回一个在 bracket 下闭合的 Lie algebra，而不是一串彼此无关的 vector fields。各层结构的必要性不同：

| 结构 | 在首篇中的作用 | 是否为一生成元约化的硬前提 |
|---|---|---|
| brackets ([X_i,X_j])、structure constants、Jacobi | 验证候选确实构成代数；发现参数处的 algebra-type change | basis/algebra 声明需要；只验证一个已知生成元时不需要完整表 |
| subalgebra closure | 确保多生成元分布可积并可使用 Frobenius quotient | (k>1) reduction 必需 |
| adjoint action | 把共轭等价的 subalgebras 合并，构造 optimal systems | 枚举 inequivalent reductions 时需要 |
| center、derived algebra、solvable radical、Levi factor | 描述 algebra isomorphism type，区分“同维但结构改变” | 对单一局部 reduction 非必需 |
| representations on fields/jets | 定义 prolongation 后的作用和 equivariant feature maps | 数学作用本身需要；深层 representation features 非必需 |
| learned-channel intertwiners | 若使用 equivariant network，约束 (Wd\rho_{\rm in}(X)=d\rho_{\rm out}(X)W) | 只有明确设计 equivariant architecture 时才加入 |

moving frames 可以帮助构造局部 canonical section，但 global section 可能因 singular orbit 或拓扑失败。实现上应记录多个局部 charts、rank-minor strata 和 overlap maps，而不是假设一个全局 canonical coordinate transform。

所谓“quantum-inspired”只有两种严格用法：使用相同的 operator-algebra/representation/intertwiner 数学，或把对称破缺当作类比。若没有从微观模型到 SVE closure 的尺度推导，就不能把量子方程、Hilbert-space symmetry 或 decoherence 当作水动力物理机制。首篇应把它放在 outlook，而不是核心方法。

## B.6 symmetry engine 与 Noether 的首篇范围

首篇建议只把以下内容放进主证书路径：

1. classical local point symmetry；
2. unrestricted determining equations 或被明确标注的 finite ansatz candidate search；
3. exact branchwise verification；
4. bracket-closed subalgebras、rank strata、local invariants 和 reduction certificate。

其他类别必须独立命名：nonclassical/conditional symmetry 要把 (Q=0) 及微分后果加入联合系统；generalized/contact symmetry 作用在更高 jet 数据；discrete symmetry 不能塞入 Lie algebra；numerical SVD 只给 near-null candidate；approximate symmetry 要满足逐阶 determining equations。

Noether theorem 也不属于默认 point-symmetry pipeline。需要先给出 action

\[
S[u]=\int L(x,u^{(n)})\,dx,
\]

证明目标方程是相应 Euler-Lagrange system（或明确的受约束/非局部变体），并证明生成元是 variational symmetry 或 divergence symmetry，才可推出 conserved current。普通 Lie point symmetry 并不自动给出 Noether conservation law。variational/Hamiltonian/current backend 应作为后续能力，除非第一篇能为选定 SVE formulation 建立合法 action。

---

# C. 一个推荐架构

## C.1 三个可行方案及取舍

| 方案 | 核心 | 优点 | 主要风险 |
|---|---|---|---|
| 1. 纯 exact branch-aware compiler | 全部由 symbolic/CAS 完成分类、约化、series | 数学边界最清楚；最强 baseline | 成本高；backend 覆盖受限；没有 ML 研究问题 |
| **2. 证书门控的 reduction + ML warm start** | ML 提候选支持/子空间或成本；exact recovery、verifier、fallback 决定接受 | 可证伪、CPU 可行；ML 不污染数学有效性；适合多查询 | 可能被直接 RRQR/SVD 完全击败；异常点 projector 不连续 |
| 3. 约化 profile neural operator | 先约化，再学习参数到解 profile | 实现最接近现有代码 | 主要是解算器/代理模型，不是对称发现；单个 ODE 无成本优势 |

**推荐方案 2。** 方案 1 是强制 baseline 和 fallback；方案 3 可作为 downstream consumer，但不应成为主算法贡献。

## C.2 推荐流水线

\[
\boxed{
\begin{aligned}
&\text{Typed PDE AST}
\to \text{equivalence canonicalization}
\to \text{differential branches}\\
&\to \text{determining operator}
\to \text{exceptional-parameter stratification}\\
&\to \text{optional ML candidate support/subspace}
\to \text{exact kernel recovery + fallback}\\
&\to \text{branchwise symmetry certificate}
\to \text{subalgebra/rank/data gates}\\
&\to \text{local quotient + reduction certificate}
\to \text{series certificate / existing solver}\\
&\to \text{deterministic route controller}
\to \text{reconstruction in the original PDE}.
\end{aligned}}
\]

| 阶段 | 输入 -> 输出 | exact / approximate | sampling / solution labels | 失败处理 |
|---|---|---|---|---|
| Parse | typed specification -> canonical AST | exact syntax/typing | 无 | `unsupported-operator` |
| Canonicalize | AST + equivalence policy -> fingerprint + transport map | exact within declared group | 无 | 保留未规范化对象并标记 |
| Complete/branch | equations + guards -> regular branches | backend-dependent proof object | 无 | `branch-partial`, `timeout`, `backend-unavailable` |
| Determine | branch -> operator (A_{\lambda,b}) | exact symbolic or controlled finite ansatz | 可选 collocation 仅作 discovery | 不得把 ansatz/SVD 升级为 complete |
| ML warm start | canonical features -> support/subspace + confidence | approximate proposal | 需要程序生成 operator samples；不需 PDE solutions | 低置信或 verifier reject 时 full solve |
| Recover/verify | candidate -> rational/exact kernel + identities | exact acceptance | 无解标签 | mismatch -> full kernel + negative record |
| Reduce | certified subalgebra + rank/data -> quotient and (\mathcal R) | local exact certificate | 无 | rank/guard/data fail -> partial or unreduced route |
| Series/solve | (\mathcal R) -> `SeriesCertificate` or numerical profile | status-dependent | 数值 route 需要采样；监督标签可选 | formal-only/empirical 状态明确 |
| Reconstruct | profile -> original field residual/data/guards | exact map + numerical solution evidence | 需要验证网格 | 不通过则拒绝结果 |

## C.3 fusion 不是特征拼接，而是带硬门的路由

先定义有效动作集合 (\mathcal A_{\rm valid}(z))：只有 completion、symmetry、rank、data 和 operator-capability gates 允许的路线才进入。控制器再选

\[
a^*(z)=\arg\min_{a\in\mathcal A_{\rm valid}(z)}
\widehat C(a\mid z).
\]

初版应是确定性规则和可审计 cost model。只有在大量重复查询出现后，才学习 (\widehat C) 或 route regret。控制器可以预测成本，不能推翻数学 gate。

证书状态必须拆开：

`completion_status`, `symmetry_status`, `rank_stratum_status`, `reduction_status`, `data_status`, `series_status`, `numerical_status`。

一个总的 `verified=true` 会掩盖未完成分支。

---

# D. ML 的精确定义与插入点

| 插入点 | 学习对象 / 信号 | 是否需解数据 | 可认证性 | 研究判定 |
|---|---|---|---|---|
| A 坐标变换 | local invariant/section；(XI=0)、Jacobian、inverse-chart | 否 | exact chart verifier | 可用作 moving-frame 工具，但 gauge/topology 风险高，创新偏弱 |
| B 生成元 | 生成元系数；determining residual | 否 | branchwise prolongation | 可作候选发现；零生成元和尺度/基底不唯一严重 |
| **C 对称子空间** | 固定 ansatz determining operator 的候选支持/子空间 | 否 | exact restricted nullspace + full fallback | **主 ML socket**；但不能直接输出证书 |
| D defect landscape | 归一化最小奇异值或 cokernel defect | 否 | 只能诊断/主动采样 | 适合定位异常集，不足以单独成主论文 |
| E (X_1) 修正 | 一阶 determining solution | 否 | exact obstruction equation | 数学价值高；单一 SVE 家族应先直接求解，不宜先上 ML |
| F (u_1) 解修正 | linearized PDE/ODE solution correction | residual-only 可行 | 原方程 residual + error estimator | 属于解算器赛道，拥挤且偏离结构发现 |
| G 参数到 profile | neural operator/surrogate | 通常需解库；physics-informed 仍逐实例优化 | reconstruction residual | 只有高查询量时合理；当前 7170 只是诊断阈值 |

推荐的 ML 输出不是“这是一个对称”，而是

\[
(S_\theta(E),\;Q_\theta(E),\;c_\theta(E))
\]

即有限支持集、候选子空间和置信度。verifier 决定 actual nullity 和 acceptance。秩跳点的 exact nullspace projector 通常不连续，所以不要强迫网络平滑预测一个变维 projector。

ML 的必要条件是：查询多、同分布、determining matrix 大且稀疏、restricted verification 明显便宜、存在谱隙、训练成本可摊销、OOD 有可靠 fallback。若完整 (A) 已经构造、矩阵很小或需要 exact rational kernel，直接线性代数应优先。

---

# E. solution-label-free 的最小数据策略

准确名称应是 **solution-label-free procedural training**，不是 dataset-free。训练仍消耗程序生成的 PDE/operator samples、collocation rows 或 CAS labels。

在固定容量 (d) 的候选子空间模型上，可使用

\[
\mathcal L_{m subspace}
=\|A(E)Q_\theta(E)\|_F^2
+\mu\|Q_\theta^TQ_\theta-I\|_F^2
+\nu\mathcal L_{\rm support/calibration}.
\]

但推理时若先完整构造并分解 (A)，再把它喂给网络，就已经支付了 baseline 成本。模型应从 canonical AST/cheap symbolic features 提议稀疏支持，随后只在该支持上 exact solve；拒绝时再运行 full solve。

训练/评估协议：

1. 按 canonical family 和 parameter stratum 分组切分，禁止只随机切行；
2. 训练集内包含普通层、异常层邻域和负控制，但 exact 异常点单列；
3. 评价 candidate recall、verifier acceptance、最终 kernel equality、fallback rate 和 wall-clock；
4. 所有准确性比较必须以同一最终 exact 输出为前提；
5. 报告包括训练的总成本，而非只报预测延迟；
6. 任何 verifier 拒绝都保留为数据，而不是删除“坏样本”。

重复查询的真实 break-even 是

\[
Q_*=
\frac{T_{\rm train}}
{T_{\rm full}-(T_{\rm pred}+T_{\rm recover}+T_{\rm verify})},
\]

仅当分母为正且实际 (Q_{\rm use}>Q_*) 时，才可能声称摊销收益；还要加入 fallback：

\[
T_{\rm total}=T_{\rm train}
+Q_{\rm use}(T_{\rm pred}+T_{\rm recover}+T_{\rm verify})
+Q_{\rm fallback}T_{\rm full}.
\]

---

# F. 受控 PDE-family generator

## F.1 typed grammar

基础 AST 可从下列节点组合：

\[
\begin{aligned}
\texttt{Equation}&\to\sum \texttt{Term},\\
\texttt{Term}&\to c(x,\lambda)
\prod_a(u^a)^{p_a}
\prod_{b,J}D_Ju^b
\mid \operatorname{Div}F,\\
\texttt{Operator}&\to D_J
\mid \texttt{Caputo}(\alpha,t_0)
\mid \texttt{RL}(\alpha,t_0)
\mid \texttt{Riesz}(\alpha,\Omega).
\end{aligned}
\]

非局部 operator node 必须带 kernel、terminal/history、function space 和 boundary semantics，不能降格为一个小数阶标签。

## F.2 生成与过滤流水线

\[
\text{grammar}
\to\text{unit/dimension check}
\to\text{operator-domain check}
\to\text{principal symbol/order/rank}
\to\text{redundancy and coupling graph}
\to\text{branch decomposition}
\to\text{canonicalization}
\to\text{stratified sampling}.
\]

Canonicalization 至少覆盖：alpha-renaming、变量/场的允许置换、term ordering、primitive polynomial 与 leading sign、声明允许的方程行变换和缩放。fingerprint 必须包含 guards、数据和 operator semantics。

为了避免数据被平凡/退化例子支配：

- 按 effective order、differential rank、nonlinearity、coupling connectivity、branch count 和 symmetry nullity 分层配额；
- 首项系数为零的样本不是一律删除，而是进入明确的 lower-order/exceptional stratum；
- 保留无非平凡对称、rank-drop、incompatible data、verifier rejection 作为负控制；
- 阻止通过重命名/整体倍乘制造重复；
- 每个 family 先保留小规模 exact oracle subset，再扩展 procedural pool。

经典局部样本进入 finite-jet Lie backend；fractional 样本进入独立 nonlocal backend；仅在有稳定局部问题和成本预算时进入 numerical solver。series route 只对 expansion point、dominant balance 和 branch 已定义的样本开放。

---

# G. 最小可发表、可否证的实验矩阵

| # | 假设 / family / sweep | 训练信号与 baseline | 指标与期望 signature | 失败含义 / CPU 预算 |
|---|---|---|---|---|
| G1 | 已知 exact symmetry 与 ansatz 内负例；含 SVE (m=3) 及同一 (X_5) 在 (m=4) | 无 ML；exact rational kernel/直接 prolongation | 正例 identity 严格为 0；负例被拒绝 | 基础对象都不能恢复则停止；分钟级 |
| G2 | canonicalization metamorphic：重命名、允许缩放、变量/场置换 | direct canonicalizer + transported generator | fingerprint 相同；transport 后 certificate 相同 | 不通过说明模型/工具在记符号；分钟级 |
| G3 | manufactured rank-jump 与 obstruction families，例如 (A_\delta=[\delta]) | exact minors、RRQR/SVD；ML 仅候选 | nullity、principal angle、candidate recall、cokernel class | 异常点被平滑抹掉则 ML 失败；小时内 |
| G4 | SVE (m=3+\delta)，(\delta=\pm2^{-k})；先符号求 (Y_1) 或 obstruction | uncorrected (X_5)、exact first-order equation、规范化 grid | 未修正 defect slope 约 1；若 (Y_1) 存在，修正后约 2 | 无 (Y_1) 就报告 obstruction；数值 slope 不替代符号证明；小时内 |
| G5 | reduction 前后 series；含一个 (2+1\) scalar 和一个 two-field system | unreduced recurrence vs certified reduced recurrence | coefficient count、DAG size、residual order、内存/时间 | 降维但 expression swell 更坏就是负结果；小时级 |
| G6 | ML/LA amortization 与 ablation；移除 canonicalization、guards、rank loss | full exact/RRQR、sparse/recycled/randomized baselines | final-kernel equality、fallback rate、总 wall-clock、(Q_*)、CI | 分母非正、(Q_*>Q_{use}) 或 verifier 常拒绝即否证 ML 价值；CPU 小规模 2-6 小时 |

G4 的正确顺序是：先提取 (O(\delta)) 系数并 exact 判定 obstruction，再做双侧 log-log slope。历史 Eulerian 曲线只能作为独立回归，不可成为 Lagrangian G4 的证据。

---

# H. 发表前必须修正的数学问题

## H.1 严格证据等级

证据不是简单的一条大小序列，而应带“证明对象”和“适用范围”：

1. branch-aware exact symbolic identity / machine-checkable proof object；
2. 独立 backend 或独立推导的 exact 复核；
3. 有误差控制的数值证书；
4. 高质量但经验性的 numerical residual/scaling；
5. finite ansatz、SVD 和 neural prediction 作为 discovery evidence；
6. 未匹配工作量的 timing 只算诊断。

允许的声明：

| 证据 | 可以说 | 不可以说 |
|---|---|---|
| exact Lie identity | 指定 generator 在指定 branch 是对称 | maximal/complete classification，除非 determining system 完成 |
| finite polynomial ansatz | 候选类内的 kernel/稳定化 | 所有 smooth infinitesimals |
| SVD | 归一化矩阵上的 numerical near-null direction | exact symmetry 或内在 defect，除非恢复并验证 |
| numerical residual | 候选在指定网格/范数的 defect | 解误差、存在唯一性或全域有效性 |
| neural prediction | 模型提出了候选/近似 | 数学有效性或新定理 |
| repeated timing | 指定硬件与工作量下的摊销测量 | 普遍 ML speedup |

## H.2 当前陈述 - 问题 - 正解 - 行动

| 当前陈述或位置 | 问题 | 正确解释 | 行动 |
|---|---|---|---|
| 标题/摘要写 near-exceptional persistence | 实验固定 (\delta=0) | 目前是 fixed cubic branch + 研究计划 | 降级标题/摘要，或先完成 G4 |
| “(m=3) exceptional algebra” | 维数跳来自源文献；本项目未完整分类 | source-reported (4\to5)，独立验证仅覆盖 (X_5) | 明示证据来源与未证边界 |
| `main.tex` 的 (X_5)、flow、(\sigma) | 旧疑问认为它们互相冲突 | 当前三者完全一致 | **不要改符号**；增加 ISC 推导即可 |
| `main.tex` Eq. determining tangency | 仅 finite-order on-shell，未写 radical/branch completion | regular branch normal form 中的条件 | 增加 (F) 与 (F^2) 反例及 completion gate |
| generic-(m) splitting | 把 (\phi_t^{m+k}) 随意当多项式独立项会过度 split | 正分支上用 (e^{m\log\phi_t})，指数碰撞另分层 | 修正文稿和 backend contract |
| source Eq. (25) 被当作 reduced ODE | 与 Eq. (7) 直接代入及论文 power law 冲突 | 项目工作式应是 (R_0=2\sigma A'-g\beta B') | 加 erratum note 与可复现代入 |
| scalar equation 等同物理 SVE | Eulerian pullback 的 convective term 有缺口 | 目前只是打印 scalar benchmark | 分流 benchmark 与 physical-equivalence claim |
| “its bracket closure is checked” | 当前未完成 closure check | closure 是必须执行的 gate | 改为 “must be checked” |
| (Y_1) 是 symmetry-family tangent | 一阶方程尚未解，且形式 lift 未必可积 | 先计算 cokernel obstruction | 禁止把计划时态写成结果 |
| `eta_ic` family 是 near (m=3) | 它只改 reduced-profile data | fixed-(m=3) data interpolation | 与 (\delta=m-3) 完全分开 |
| current “fusion” | 实际是 reduction + Taylor hard constraint + NN correction | downstream profile approximation | 不称 structural two-engine controller |
| direct-vs-lifted residual 差约 (10^{-14}) | 只证明两种 residual 计算一致，不说明 residual 小 | 同时报告 raw/normalized residual 与 profile error | 修订 Week-2 与论文表述 |
| 7170 break-even | 未匹配 verifier/fallback 和全部工作量 | exploratory arithmetic diagnostic | 依 G6 重测；不称 speedup |
| dataset-free | 仍需 PDE/operator samples | solution-label-free procedural | 统一术语 |
| one generator -> ODE | 只在 (p=2)、projected rank 1 成立 | 一般是 (p\to p-1) | 在理论/报告中明确 dimension count |
| Lie algebra dimension -> reducibility | vertical generator、rank drop、data 可阻止约化 | reducibility 属于 branch + subalgebra + rank + data | 分开四类 exceptional set |
| Jacobian nonzero -> symmetry | Jacobian 只证明 chart 正则 | symmetry 需要 determining identity | 分开 chart gate 和 symmetry gate |
| series = Taylor coefficients | 可能是 formal/asymptotic、含 resonance/log | `SeriesCertificate` 必须标状态 | 不声称收敛，除非有证明 |
| fractional order 只是一个实参数 | operator/history 变化改变理论 | nonlocal backend 独立 | 第一篇仅保留 interface 和 limit tests |
| Noether 紧跟 Lie point symmetry | 任意 point symmetry 不给 conservation law | 需要 action + variational/divergence symmetry | 移到后续 variational branch |
| quantum analogy | 不是 SVE 物理机制 | 最多是 algebraic analogy | 移到 outlook；无派生机制就不作物理主张 |

## H.3 对 `main.tex` 的精确提案（本轮不执行）

1. 保留当前 (X_5)、flow、(\sigma)、(Q) 与 (\phi=F(\sigma))。
2. 在 SVE anchor 后加入 general defect identity 和“只验证 supplied generator”的边界。
3. 在约化式附近加入 source Eq. (25) conflict note，并把直接 (R_0) 指定为项目工作方程。
4. 写全 Eulerian-to-Lagrangian bed chain rule；将 scalar benchmark 与 physical SVE equivalence 分开。
5. 将所有 near-(m=3) 完成时态改为 research question，直到 (Y_1)/obstruction 有 exact 结果。
6. 将 `lambda` 拆为 model parameters、data parameters、integration constants；保留 (\varepsilon) 为 group parameter、(\delta=m-3)。
7. 将 one-generator chart theorem 明确限定为 local, regular, projectable, affine-fibre, constant-rank case。
8. 将 `data-compatible` 限定为构造数据的充分相容性，不涉及 IBVP well-posedness。
9. 将 current fusion 改名为 fixed-(m=3) certificate-gated profile approximation，并把 structural predictor 标为未来设计。
10. 同时报 raw residual、normalized residual、profile error 和 direct-vs-lifted difference；后者只叫 identity consistency。
11. 说明 v0.1 的 673 参数单-IVP模型与 v0.2 的参数条件 family 实验是不同实验，不能混表。
12. 把 fractional、Noether、quantum representation theory 移到边界/后续工作，除非第一篇真的实现相应 backend。

## H.4 明确非主张

当前版本不主张：

- generic-(m) maximal symmetry classification；
- (m=3+\delta) symmetry continuation 或 (O(\delta^2)) Lagrangian correction；
- 奇异 guard 分支上的解；
- global quotient 或全局 solution correspondence；
- 完整物理 Eulerian SVE 等价性；
- series convergence/interval solution certificate；
- classical/fractional symmetry 的统一 backend；
- Noether current；
- ML speedup 或结构级 ML 已实现。

---

# I. 成熟的 Week-2 报告蓝图

报告应保持课程 interim-report 外壳，但内容改成证据驱动的短研究报告：

1. **Isolated question and status.** 固定对象：打印 scalar equation、(m=3) regular branch、supplied (X_5)；一句话说明 broader architecture 仍在设计。
2. **Exact result.** 列 (X_5\to\sigma\to Q\to R_0)、guards、local scope 和 39 个聚焦测试。
3. **Source/model caveat.** 简述 Eq. (25) conflict 与 Eulerian chain-rule 缺口；不要把 benchmark 等同物理模型。
4. **Discovery evidence only.** finite ansatz、SVD、neural residual 分别能说明什么，不能说明什么。
5. **Architecture decision.** 采用 certificate-gated candidate-subspace warm start；direct exact/RRQR 是 baseline/fallback。
6. **Why ML, if at all.** 只为大量同类查询的摊销；单 ODE solve 没有优势。
7. **Minimal data.** solution-label-free procedural operator samples；不是 dataset-free。
8. **Near-exceptional experiment.** 先求 (\mathcal A_0Y_1=-\mathcal A_1Y_0)，再检查 defect slope 1 -> 2；允许 obstruction。
9. **Falsification plan.** canonicalization、rank jump、series-before/after、matched amortization 与 ablation。
10. **Explicit nonclaims and next gate.** 把所有未证项目列出；以精确研究假设结尾。

Week-2 正文还应包含一个紧凑 evidence table：`Claim | Evidence | Scope | Status`。不要把每天做了什么作为主体。学生姓名、ID、导师栏保留。

---

# J. 最终研究问题与可证伪假设

## 一句话研究问题

> 在 branch-aware canonical PDE families 的大量重复查询中，ML 提议的 determining-kernel 候选支持，能否在 exact recovery、branchwise verification 和 full fallback 后，保持与完整 baseline 相同的有限-ansatz kernel，同时降低总 CPU 成本？

## 可证伪假设

令 (A_E) 是 canonical、branchwise、固定 ansatz 的 determining operator。预测器仅输出候选支持 (S_\theta(E))；exact restricted solve、symbolic verifier 和 fallback 给出最终 kernel。主假设是：

\[
T_{\rm train}
+Q_{\rm use}(T_{\rm pred}+T_{\rm recover}+T_{\rm verify})
+Q_{\rm fallback}T_{\rm full}
<Q_{\rm use}T_{\rm full},
\]

同时：

1. 每个被接受候选在所有声明 regular branches 上满足 exact determining identities；
2. 最终有限-ansatz kernel 与 full baseline 相同；
3. exceptional/rank-drop strata 的召回达到预先冻结的阈值；
4. OOD/低置信样本可靠回退。

若分母不正、(Q_*>Q_{\rm use})、最终 kernel 不一致、异常层召回不足，或 verifier/fallback 频繁到抵消收益，则“ML 对该任务有算法价值”的假设被否证。

SVE 的角色是第一个高风险 anchor/negative-control family：固定 (m=3) 证书检验 exact path；(m=3+\delta) 的一阶 obstruction 与 defect scaling 检验 exceptional-stratum path。它不应被包装成已经完成的通用算法。

---

## 本轮证据与复现边界

- 聚焦测试命令：`python -B -m pytest symm/tests/test_chart_reduction.py symm/tests/test_sve_certificate_v02.py symm/tests/test_three_layer_demos.py -q -p no:cacheprovider`
- 本轮已记录结果：`39 passed in 15.78s`；Windows 临时目录清理 warning 不影响测试结论。
- 源论文：Paliathanasis, Leon, and Leach, *Mathematics* 14 (2026), 433, DOI `10.3390/math14030433`。
- 历史一维 SVE 近三次幂材料：DOI `10.3390/sym14081679`；它属于不同 Eulerian 三场模型，不能作为当前 scalar Lagrangian (O(\delta^2)) 证书。
- 当前结论仅适用于已声明的 local regular branches；没有把 source-reported classification 当作本项目独立定理。

## 审查门

请先审阅并批准或修改 C-H 节，尤其是主 ML socket、证书状态、SVE 物理边界和最小实验矩阵。批准前不应修改生产 symmetry engine，也不应把本设计写成已实现结果。
