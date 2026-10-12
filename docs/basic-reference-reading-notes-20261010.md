# Lie 对称、近似对称与符号计算：基础文献阅读笔记

初读日期：2026-10-10；证据状态同步：2026-10-11
用途：为 LieML/SVE 的确定方程自动化、参数延拓判定和守恒约化提供可审查的理论基线。本文是阅读与方法审计，不是新的最大对称分类。

## 结论先行

1. 最新 SVE 实验已经超过旧的“对角缩放 ansatz 失败”。在两个明确的三阶标量模型、固定 \(g,\kappa>0\) 及 \(p=\phi_t>0,\ q=\phi_s>0\) 上，它排除了
   
   \[
   X_\delta=X_5+\delta Y+o(\delta),\qquad
   Y=\tau(t,s,\phi)\partial_t+\xi(t,s,\phi)\partial_s+
   \eta(t,s,\phi)\partial_\phi
   \]
   
   这种任意光滑**点**修正。决定性证据是
   
   \[
   [p^2q^2]\!\left(q^3\frac{\partial\Omega}{\partial\phi_{tss}}\right)
   =3g\kappa\ne0.
   \]

2. 该结论可称为“声明正则分支上的一阶 \(C^1\) 点对称延拓障碍”，也排除以 \(X_5\) 为零阶项的标准一阶 BGI 点生成元提升。它不是最大点代数分类，也不是 generalized/contact/nonlocal/nonclassical 或 FS 障碍。

3. Olver 的条件使该证书不仅是形式代数矛盾。在 \(q>0\) 上，
   \(\partial E_m/\partial\phi_{ttt}=q\ne0\)，故方程零集是最大秩的正则超曲面；固定实数 \(m\) 时，\(p,q>0\) 分支上的系数为解析函数，方程可对纯时间 leading jet \(\phi_{ttt}\) 求解。由解析 normal-form 的局部可解性结果，可使用 Olver 的充要无穷小判据。现有 [THEORY.md](../research_artifacts/sve-progress-20261010/docs/THEORY.md) 已明确写出这座局部解析桥梁；它不是全局或光滑数据适定性证明。

4. BGI 与 FS 是不同问题。BGI 展开生成元；FS 展开场并求两场系数系统的精确对称。Tarayrah--Pitzel--Cheviakov 的 Theorem 3.1 是带强假设的单向充分命题，而且 \(X_5\) 的演化特征
   \(Q_5=-t\phi_t+2s\phi_s\) 依赖一阶 jets，不满足其中 \(\zeta^0(x,t)\) 的假设。因此当前证书对 FS 没有结论。

5. 当前共同缩放 \(X_c=t\partial_t+s\partial_s+\phi\partial_\phi\) 的一变量约化有理论依据；但“由两个自变量降为一个”来自群商，“三阶降为二阶”来自另一个一阶积分 \(R_m=(LF'')'\)，两者必须分开陈述。

6. 当前 [project-map.md](project-map.md) 与 [main.tex](../draft/main.tex) 按两标量模型、正则分支、一阶、\(C^1\) 参数依赖及任意足够光滑点系数同步证据。两条独立障碍推导、\(Q_c,D_JQ_c\)、轨道秩/Jacobian 和所声明的标量 current pullback 已完成；任意初边值数据、FS 与完整床面场结论仍未建立。

复核入口（仓库根目录）：

```bash
python scripts/project.py workflow --out build/workflow
python scripts/project.py data-flux --out build/data-flux
```

第一条生成主文稿证据报告和流程图；第二条已验证两标量模型的构造共同缩放 ray-data/flux 家族：\(g=1,\kappa=1/30\)，在 \(s/t=1\) 上指定 \(\phi/t=2,\phi_s=1/2,t\phi_{ss}=1/10\)。这一完成状态不推广到任意 IBVP。

## 一、第一性原理图景

把 Lie 代数理解为“变量压缩工具”是合适的，但压缩之前必须回答三个不同问题。

1. **方程对称吗？** 点生成元
   
   \[
   X=\xi^i(x,u)\partial_{x^i}+\eta^\alpha(x,u)\partial_{u^\alpha}
   \]
   
   必须延拓到 jet 空间，并在方程流形上相切。
2. **不变解能写成图吗？** 群轨道必须 regular，并且对依赖变量的竖直方向 transversal；否则“令不变量等于 profile”可能不是单值函数。
3. **约化保留了什么？** 原 PDE、约束、初边值数据、守恒密度/通量和分支条件都要 pull back；只得到一个形式 ODE 不等于得到有效的原问题约化。

这三步分别对应“代数正确性”“几何可约化性”“物理/数据相容性”。ML 只能在这些门之后提出候选或近似尚未解析求解的对象。

## 二、文献证据矩阵

| 文献 | 选读位置 | 硬约束 | 对本项目的直接含义 |
|---|---|---|---|
| Olver, *Applications of Lie Groups to Differential Equations* | Ch. 2 §§2.3--2.4, 2.6；Ch. 3 §§3.1, 3.5 | 最大秩、局部可解性、延拓、自由-jet 分裂、regular/transversal 群商 | 决定方程证书必须带正则图；约化必须带轨道秩、特征方程、Jacobian 和重构 |
| Oliveri, *Lie Symmetries of Differential Equations* | §§4.2--4.3, 6.2, 6.4, 7.3.3, 8.3, Ch. 11, §§12.2.1, 12.2.7, 12.2.10 | leading derivative、非多项式 jet、参数分支、未解条件、数据与守恒律 | AST 不能只存一个 residual；求解器不能把 CAS 返回等同于分支完备证明 |
| Tarayrah--Pitzel--Cheviakov (2023) | §§2.2.2--2.2.3, 3.4--3.5, 6 | BGI/FS 定义不同；PDE 中高阶自由 jet 可造成稳定性障碍 | 当前 \(3g\kappa\) witness 是 BGI-type 点障碍；FS 必须另建系数系统 |

Olver 扫描件中印刷页 119--122 的顺序异常；本笔记按印刷页与定理编号核对，而不是依赖 PDF 页序。

## 三、Olver：何时决定方程真的刻画对称

### 3.1 延拓和无穷小判据

- Definition 2.30（印刷页 106）把“最大秩”定义为残差对全部 jet 坐标的 Jacobian 在零集上满行秩。
- Theorem 2.31（106--107）说明：最大秩下，
  
  \[
  \operatorname{pr}^{(n)}X(\Delta_A)=0\quad\text{on }\Delta=0
  \]
  
  足以得到局部对称；等价地可在独立残差图上写成 multiplier 关系。
- Theorem 2.36（113）给出通用延拓公式
  
  \[
  \eta_J^\alpha=D_JQ^\alpha+\xi^i u^\alpha_{J,i},
  \qquad Q^\alpha=\eta^\alpha-\xi^iu_i^\alpha.
  \]
- §2.4 的实际计算规则是：先用方程消去 dependent leading jets，再把剩余 unconstrained jets 当作独立变量逐系数分裂。
- Definition 2.70（162）要求“nondegenerate = maximal rank + locally solvable”；Theorem 2.71（165）在该条件下才给出对解映射意义下的必要且充分判据。
- Definition 2.78、Theorem 2.79 和 Corollary 2.80（170）给出本项目需要的解析桥梁：解析且 normal 的方程局部可解。

### 3.2 对 SVE 障碍的应用

对两个实验模型都有

\[
\frac{\partial E_m}{\partial r}=q,
\qquad r=\phi_{ttt},\quad q=\phi_s>0.
\]

所以可在声明分支上精确消去 \(r\)，其余相容 jet 是局部自由坐标。令

\[
\Omega=\left.\bigl(\operatorname{pr}^{(3)}Y(E_3)+T_3\bigr)
\right|_{r=r_{\rm shell}}.
\]

若一阶点延拓存在，\(\Omega\) 必须在正开集上恒为零。对自由 jet \(x=\phi_{tss}\) 求偏导、乘 \(q^3\) 清除已声明非零的分母，再对自由 \(p,q\) 作多项式分裂，得到不可消去的 \(3g\kappa\)。这与 Olver §2.4 的逻辑完全一致：它不是采样残差，也不是有限 generator ansatz 的失败。

正式证据采用的局部正则性链是：

\[
q>0
\Rightarrow \text{maximal rank and a leading-jet chart}
\Rightarrow \text{analytic normal form on }p,q>0
\Rightarrow \text{local solvability}
\Rightarrow \text{Theorem 2.71 applies locally}.
\]

### 3.3 对约化的应用

Olver Chapter 3 的要求不是“找到一个不变量”而已。

- §3.1：总空间作用与基空间投影作用都应 regular，轨道维数同为 \(s<p\)；约化后有 \(p-s\) 个自变量。
- Proposition 3.37：轨道必须对竖直空间 transversal，才能局部得到不变图。
- Theorem 3.38：不变 jet 不只满足 \(Q=0\)，还满足
  \(D_JQ=0\)（\(|J|\le n-1\)）。
- Theorems 3.36、3.41：约化方程来自
  \((\mathcal E\cap\operatorname{Inv}_H^n)/H\)，并依赖 regular quotient 和完整不变量坐标。

对共同缩放 \(X_c\)，在 \(t>0\) 上 projected rank 和 total rank 都为 1，且

\[
Q_c=\phi-t\phi_t-s\phi_s=0,
\qquad z=s/t,\quad v=\phi/t,\quad v=F(z).
\]

坐标 \(y=\log t,\ z=s/t\) 的基 Jacobian 为 \(1/t^2\ne0\)，因此
\(\phi=tF(s/t)\) 是合法的局部 invariant graph。当前机器证书已显式记录
\(Q_c,D_JQ_c=0\)（\(|J|\le2\)）、两种轨道秩和 Jacobians，而不只记录最终 substitution。

## 四、Oliveri：符号程序应保存什么

### 4.1 ReLie 的可审查流水线

ReLie 的核心流程是

    jetorder, xvar, uvar
        -> diffeqs, leadders
        -> relieinit()
        -> relieinv()
        -> reliedet()
        -> reliesolve().

- `leadders` 明确指定用方程消去的 leading derivatives；每个方程必须能在当前分支对相应 leading derivative 求解。
- `relieinv()` 生成延拓后的上壳不变性式；`reliedet()` 对自由 derivatives 分裂；`reliesolve()` 再求线性确定 PDE。
- `reliedet()` 默认自由 derivatives 以多项式方式出现。若不是，必须声明 `nonpolyders`，否则分裂可错。
- `freepars`、`nonzeropars`、任意元素的允许依赖以及等价变换设置都是问题语义的一部分，而不是后处理注释。
- `symmetries` 的输出包括四部分：未解条件、无穷小量解、参数、必须非零表达式。未解条件非空时不能报告“完整求解”。
- `commutatortable`、`reliedistrib`、`inverselie`、`testrank` 表明 bracket closure 和 orbit/distribution rank 是独立验证步骤。

因此，一个可复用引擎至少需要以下机器可读对象：

| 对象 | 必需字段 |
|---|---|
| `ProblemSpec` | 方程/守恒块 AST、场角色、固定时间轴、参数与任意元素、允许依赖、smooth branch、数据与边界通量 |
| `JetChart` | multi-index、leading/free jets、消元式、每次除法及非零 guard、参数 strata |
| `DeterminingSystem` | 原始延拓式、上壳式、split variables、`nonpolynomial_atoms`、系数方程、未解条件、后端状态 |
| `AlgebraCertificate` | 回代恒等式、基/维数、brackets、结构常数、最大性状态、rank strata |
| `ReductionCertificate` | 子代数闭合、projected/total ranks、\(Q,D_JQ\)、不变量、逆图、Jacobians、重构 |
| `ConservationCertificate` | density、spatial flux、source、constraints、Jacobian weight、边界法向通量 pullback、等价/平凡状态 |

Oliveri 对守恒律和 Noether 理论的处理也要求保持概念分离：一般 balance law 的守恒证书不等于变分/Noether 证书。当前 reduced ODE 的 first integral 也不自动成为原 PDE 的局部守恒律。

### 4.2 Chapter 11 不是一个可混用的标签

Oliveri Chapter 11 先比较 BGI 与 FS，再采用一种“展开因变量并诱导展开 Lie operator”的 consistent framework。ReLie 的 `approxorder` 模式遵从书中所选框架，并要求显式截断规则，例如 `epsilon^2=0`；遇到非显式函数还需先作相应级数展开。

因此实现必须保存

    approximation_semantics =
        exact_parameter_family
      | BGI_generator_expansion
      | FS_field_expansion
      | Oliveri_consistent
      | nearby_equation_numerical_algebra.

这些状态不能通过都含有“小参数”而合并。当前实验首先研究精确点对称族的 \(C^1\) 参数延拓；它的一阶必要条件同时给出 BGI-type 点 lift 的障碍，但它没有运行 Oliveri-consistent 或 FS 分类。

## 五、Tarayrah--Pitzel--Cheviakov：BGI 与 FS 的严格边界

### 5.1 BGI

对

\[
F[u;\epsilon]=F_0[u]+\epsilon F_1[u]=o(\epsilon),
\]

BGI 展开原场空间上的生成元

\[
X=X^0+\epsilon X^1.
\]

\(O(1)\) 条件要求 \(X^0\) 是 \(F_0=0\) 的精确对称；\(O(\epsilon)\) 条件是线性非齐次确定问题

\[
\left.\operatorname{pr}X^1(F_0)\right|_{F_0=0}=H[X^0,F_1].
\]

若该问题有解，\(X^0\) 称 BGI-stable；否则称 unstable。当前 SVE 的自由-jet witness 证明：对声明的两个标量模型和正则分支，\(X_5\) 在**点生成元类别**中是一阶 BGI-unstable。

### 5.2 FS

FS 展开场

\[
u=v+\epsilon w+o(\epsilon)
\]

并构造

\[
G_1=F_0[v]=0,
\qquad
G_2=D F_0[v](w)+F_1[v]=0.
\]

FS 对称是 \((v,w)\) 两场系统的精确 Lie 对称。其 leading \(v\)-component 甚至可以依赖 \(w\)，这类“混合”对称没有 BGI 对应物。故 FS 任务不能由一个 BGI obstruction flag 代替。

### 5.3 为什么 Theorem 3.1 不能替 SVE 做 FS 推论

该定理只在以下条件同时成立时给出 BGI \(\Rightarrow\) FS 的单向映射：

1. 标量 \(1+1\) PDE 已写成指定 Kovalevskaya form；
2. 已经存在 BGI lift；
3. \(\zeta^0=\zeta^0(x,t)\)，而 \(\zeta^1\) 仅有指定的一阶依赖；
4. \(F_0\) 满足论文 Eq. (3.25) 的 Hessian-contraction 条件。

SVE 当前首先得到的是“不存在点 BGI lift”，而且
\(Q_5=-t\phi_t+2s\phi_s\) 依赖 jets，所以该定理既不能证明 FS 存在，也不能证明 FS 不存在。

### 5.4 §3.4 与当前 witness 的关系

论文 §3.4 的 wave-PDE 例子说明一个重要机制：延拓后出现的更高自由 derivatives 在分裂时可迫使零阶生成元系数为零，从而产生真实的 PDE 稳定性障碍。当前 SVE 的 \(3g\kappa\) witness 是同类机制的独立实例。

但“机制相同”不是“定理转移”。论文的例子分别完成了 BGI 和 FS 方程；当前 SVE 只完成了 point BGI-type 方程。因此不能引用 §3.4 把 SVE 结论扩成 FS 或任意 local generalized obstruction。

## 六、最新 SVE artifact 的审计状态

| 项目 | 当前判定 | 依据/缺口 |
|---|---|---|
| \(X_5\) at \(m=3\) | exact anchor | 两模型 multiplier/defect identity remainder 为 0 |
| 任意光滑点 \(Y\) 的一阶延拓 | obstruction certified on declared branch | 两模型 selected coefficient 均为 \(3g\kappa\ne0\) |
| Olver nondegeneracy | 局部解析条件已写入证据 | \(q>0\)、解析 normal form、Cor. 2.80；不含全局适定性 |
| 一般 \(m\) 的共同缩放约化 | local reduction verified | exact symmetry、rank/transversality、有效不变量、\(Q_c,D_JQ_c\) 和 Jacobians |
| 二阶 profile ODE | verified after an extra first integral | 对称商先产生三阶 \(R_m=0\)；\(R_m=(LF'')'\) 才降阶 |
| physical-corrected witness | 两条独立符号路径通过 | recursive prolongation 与独立 principal-symbol derivation 给出相同系数 \(3g\kappa\) |
| 两条标量 balance-law 与边界协向量通量 | exact pullback verified | \((T,z)=(t,s/t)\) 下 density 为 \(tA\)，flux 为 \(J-(s/t)A\)，divergence 为 \(tE_m\)；边界通量与 \(dz\) 配对 |
| 构造的 ray-data/flux 相容性 | 两模型 exact symbolic checks 已通过 | \(g=1,\kappa=1/30\)，\(s/t=1\) 上 \(\phi/t=2,\phi_s=1/2,t\phi_{ss}=1/10\)；\(\det D(t,s)/D(T,z)=T\)，正 \(z\) 方向边界 current 为 \(I_0/T\)；不推广到任意 IBVP |
| 构造家族的负控 | 5 个拒绝检查通过 | 两模型均拒绝不相容的常数物理 \(\phi\) 数据和零 chart determinant；另拒绝 \(t=0\) |
| 构造家族的数值复核 | 12 个参考算例通过 | \((F,F',F'')\) 最大跨求解器差 \(3.33\times10^{-15}\)，积分漂移 \(1.80\times10^{-14}\)，均低于 \(10^{-9}\)；数值证据与精确 reference-tube 界分开 |
| FS SVE 分类 | not run | 必须构造 \((\phi_0,\phi_1)\) 系数系统并单独求精确对称 |
| 最大点分类/optimal system | not established | 未求完整确定系统和所有共轭子代数 |
| ML 优越性或加速 | unsupported | 经典 Chebyshev 控制在本小实验中最好；16/40 优化运行耗尽预算 |

初读时的独立运行记录（历史）

    python -B -m pytest -q -p no:cacheprovider
    38 passed in 7.36s

现行证据包另记录 43 项通过测试，见 [experiment index](../research_artifacts/sve-progress-20261010/docs/EXPERIMENT_INDEX.md)。这些运行验证代码路径和已编码恒等式，不单独证明数学完备性。初读时发现未解压目录缺少 manifest 中的 52 个 `.npz`，而随附 ZIP 含全部 78 个 manifest 条目且哈希匹配；冻结候选的完整复核应以 ZIP 为证据载体。

## 七、建议的精确算法

目标类先固定为连续、光滑、固定时间方向、1--2 个空间维的非线性 balance-law 系统，可带 differential constraints：

\[
D_t\rho_a(U)+\sum_{i=1}^{d}D_{x_i}J_a^i(U^{(n)};\lambda)
=S_a,\qquad d\in\{1,2\}.
\]

算法应按以下顺序执行。

1. **冻结语义。** 记录变量角色、单位/无量纲化、参数路径、方程块、约束、数据面、boundary flux、smooth regime 和非零 guards。
2. **建立正则图。** 按参数和非零条件分支；检查 residual Jacobian；选 leading jets，并记录每次除法。区分 maximal rank、local solvability 和尚未证明的 formal integrability。
3. **构造延拓。** 用规范 multi-index 和总导数递归产生 \(\operatorname{pr}^{(n)}X\)，不先限制 \(\tau,\xi,\eta\) 为多项式或缩放 ansatz。
4. **上壳消元。** 用原方程及确有需要的微分后果消去 leading jets；不得把一个启发式 simplification 当成完整 normal form。
5. **自由-jet 分裂。** 显式区分 polynomial variables 与 `nonpolynomial_atoms`；生成线性确定 PDE，并保存未解条件和参数 strata。
6. **兼容性判定。** 若出现 \(0=c(\lambda)\ne0\) 的可复核 witness，输出 scoped obstruction；否则运行声明的 differential-completion/solver backend。超时、有限 ansatz 失败或后端缺失只能输出 `unresolved`。
7. **独立回代。** 把候选代回原始 prolonged identity；用第二条推导路径核对关键符号/最高阶系数；保存原始表达式、hash、guards 和软件版本。
8. **恢复 Lie 结构。** 计算 kernel、brackets、structure constants 和 rank strata；候选集合不是 Lie algebra，除非 closure 已验证。最大性与“已验证候选”分别标记。
9. **选择约化子代数。** 检查 bracket closure、projected/total orbit ranks、数据和边界相容性；optimal-system 完备性单列状态。
10. **构造群商。** 计算 \(Q,D_JQ\)、完整不变量、局部逆和 Jacobians；只在 regular/transversal chart 上生成 reduced equations 和 reconstruction map。
11. **认证守恒 pullback。** 分别变换 density、spatial flux、source、constraints 和 boundary normal flux，并包含坐标 Jacobian weight；不要用一个 reduced first integral 代替此步骤。
12. **选择近似语义。** exact-family、BGI、FS、Oliveri-consistent 各走不同分支。FS 必须显式生成 coefficient system。
13. **最后才使用 ML。** ML 只提出候选 kernel/subalgebra 或近似已合法定义的 reduced object；所有结构结论回到精确恢复、closure 和原坐标残差验证。

简化的状态机是

\[
\boxed{
\text{regular equation chart}
\to\text{prolongation}
\to\text{on-shell elimination}
\to\text{free-jet splitting}
\to\text{compatibility witness/solve}
\to\text{closure and orbit tests}
\to\text{certified conservative reduction}.}
\]

## 八、对 ML 任务的约束

以下是项目设计推论，不是三份文献已经证明的 ML 定理。

- **Symmetry-algebra estimator** 的统计输出应是
  \(p_\theta(k,P\mid E)\)，其中 \(P\in\mathrm{Gr}(k,N)\) 是规范 ansatz coefficient space 上的 projector；不要回归任意选取的基向量。
- **Reduction-subalgebra selector** 应在 exact \(\mathfrak g\)、structure constants、orbit ranks、守恒/数据特征上排序 bracket-closed \(\mathfrak h\le\mathfrak g\)。它与 algebra estimator 是两个任务。
- 预测必须经过 exact determining residual、rank/nullity calibration、basis/equivalence covariance、bracket closure 和 OOD rejection。
- profile/solution learner 是 downstream consumer，不是 Lie-space estimator。若 exact obstruction 已排除 \(X_5\) 的点 lift，就不能硬编码其近似不变量作为 profile 坐标。
- 当前小实验中经典方法表现最好，所以尚无“ML 必需”“ML 更快”或“深 PINN 更优”的证据。

## 九、明确非主张与下一步

当前不主张：

- 两个标量方程的最大点对称代数或最优子代数系；
- contact/generalized/nonlocal/nonclassical 对称障碍；
- 奇异参数依赖的延拓障碍；
- FS 或 Oliveri-consistent 的 SVE 障碍；
- 含独立床面场的完整 Eulerian/Lagrangian SVE 分类；
- shock/weak-solution regime、全局存在或真实渠段数据覆盖；
- 一般守恒 pullback 定理、任意数据/边界通量相容性、Noether 结构、ML 加速或连续误差界已经认证。所声明的两条标量 balance-law 与边界协向量 current pullback 是已完成的有限范围证书。

已完成 analytic normal-form 论证、\(Q_c,D_JQ_c\)/轨道/Jacobian 字段、修正模型独立主符号复核、标量 current pullback 与构造的 normalized-ray 数据/通量相容性。后续复核与开放问题是：

1. 用 `workflow` 独立复核主文稿的已有恒等式与覆盖边界，保留失败状态。
2. 用 `data-flux` 重现已通过的构造数据面、profile jets 和边界 current 检查；符号恒等式针对正分支上的 real \(m\)，精确参考管界限于 \(g=1,\kappa=1/30,m\in[1,4],z\in[1,7/5]\)。
3. 若要讨论 FS，单独构造 \((\phi_0,\phi_1)\) 系数系统；不要从 BGI 结果类推。
4. 完整床面场、一般 IBVP、全局/弱解和 ML 性能分别需要新的问题契约与证据。

## 参考文献与本地来源

1. P. J. Olver, *Applications of Lie Groups to Differential Equations*, selected Chapters 2--3. 本地文件：[Olver PDF](../ref/pdfs/applications-of-lie-groups-to-differential-equations-graduate-texts-in-mathematics-9781468402766-9781468402742-1468402765_compress.pdf).
2. F. Oliveri, *Lie Symmetries of Differential Equations: Theory, Applications, and Symbolic Computation*, selected Chapters 11--12 and supporting exact-symmetry sections. 本地文件：[Oliveri PDF](../ref/pdfs/lie-symmetries-of-differential-equations-theory-applications-and-symbolic-computation_compress.pdf).
3. M. R. Tarayrah, B. Pitzel, and A. Cheviakov, “Two approximate symmetry frameworks for nonlinear partial differential equations with a small parameter: Comparisons, relations, approximate solutions,” *European Journal of Applied Mathematics* 34 (2023), 1017--1045, DOI `10.1017/S0956792522000407`. 本地文件：[article PDF](../ref/pdfs/two-approximate-symmetry-frameworks-for-nonlinear-partial-differential-equations-with-a-small-parameter-comparisons-relations-approximate-solutions.pdf).
4. 当前实验理论：[THEORY.md](../research_artifacts/sve-progress-20261010/docs/THEORY.md)；机器证书：[symbolic_certificates.json](../research_artifacts/sve-progress-20261010/results/symbolic_certificates.json)；结果边界：[FINDINGS.md](../research_artifacts/sve-progress-20261010/docs/FINDINGS.md).
