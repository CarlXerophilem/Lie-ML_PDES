以下将 `Lie_reduction.md` 与 `workflow.md` 的内容整合重构。全文以**微分几何与射流丛（Jet Bundle）上的局部群作用主线**为骨架，剔除琐碎的数值罗列，按照手工推导的逻辑链条，逐一阐明李群理论将偏微分方程（PDE）系统约化为常微分方程（ODE）系统、进而降阶并重构的**每一个步骤做什么（What）**以及**为什么这么做（Why）**。

---

### 总纲：李群约化与重构的微分几何主线

整个李对称约化、降维与重构的过程，严格浓缩于以下局部微分几何与代数序列中：

$$\boxed{
\mathfrak{g}_\Delta = \ker \mathscr{D}_\Delta 
\ \supset\ \mathfrak{h} 
\ \xrightarrow{\exp}\ H = \langle G_\epsilon \rangle 
\ \curvearrowright\ (\mathcal{E}_\Delta \cap \mathcal{I}_H^n) 
\ \xrightarrow{\pi_H^{(n)}}\ \overline{\mathcal{E}}_{\Delta, H} \subset J^n_{p-r}(M/H), 
\qquad 
\operatorname{Sol}_H(\Delta) \underset{\Gamma_F \mapsto \pi_H^{-1}(\Gamma_F)}{\overset{\Gamma_w \mapsto \Gamma_w / H}{\rightleftarrows}} \operatorname{Sol}(\overline{\mathcal{E}}_{\Delta, H})
}$$

当底空间自变量维数 $p$ 与局部群轨道的有效投影秩 $r$ 满足 $p - r = 1$ 时，商空间上的约化系统 $\overline{\mathcal{E}}_{\Delta, H}$ 严格退化为常微分方程（ODE）系统。需要注意，这一序列是**局部微分几何命题**（内部包含代数的确定方程运算），并不宣称任意非线性 PDE 或其轨道商空间是全局代数簇或全局 Hausdorff 流形。

#### 基础几何词典

* **底流形与全空间**：设底流形 $B \subset \mathbb{R}^p$ 承载独立自变量 $x = (x^1, \dots, x^p)$，全空间（点空间）$M \subset B \times \mathbb{R}^q$ 承载自变量与因变量点坐标 $(x, u) = (x^1, \dots, x^p, u^1, \dots, u^q)$，配备标准纤维丛投影 $\pi_0(x, u) = x$。


* **截面与解图**：必须严格区分**点坐标 $u$** 与**解函数（截面）$u = w(x)$**。函数 $w(x)$ 在几何上表现为全空间 $M$ 中的一个 $p$ 维子流形（即解图 $\Gamma_w = \{(x, w(x))\} \subset M$）。群变换 $\Phi(x, u) = (\tilde{x}, \tilde{u})$ 对函数的作用不是简单的函数复合，而是通过搬运整个解图 $\Gamma_w \mapsto \Phi(\Gamma_w)$ 并在 $\tilde{x}(x, w(x))$ 局部可逆的条件下重构新函数 $\tilde{w}(\tilde{x})$。



---

### 第一阶段：表示空间选定与射流流形构造（预备步）

在引入对称生成元之前，必须先锁定物理方程的坐标系表示，并将微分方程转化为射流丛上的代数超曲面。

#### 步骤 1：选定方程表示并验证坐标转换的局部等价性

* **做什么**：明确控制方程、本构闭合关系与无量纲参数。若从欧拉守恒系（如浅水波与河床演化的三场系统 $E$）转换至拉格朗日/物质坐标标量系（模型 $M$），需利用质量守恒方程 $\partial_t h + \partial_x(hu) = 0$ 定义闭 1-形式 $\mathrm{d}s = h\,\mathrm{d}x - hu\,\mathrm{d}t$，在单连通开集上引入物质势坐标 $s$ 并通过逆函数定理（依赖雅可比条件 $q = \phi_s = 1/h > 0$）反解出 $x = \phi(t, s)$，最后由动量与河床方程的混合偏导相容性（即闭 1-形式 $\omega_M$ 满足外微分 $\mathrm{d}\omega_M = 0$）消去河床变量，导出高阶标量相容方程。


* **为什么这么做**：对称性依赖于具体的方程形式与坐标表象。通过势函数 $\mathrm{d}s$ 建立的物质坐标转换依赖于具体解，它**不是**原五维点空间上的可逆点变换（属于非局部变换），因此欧拉系 $E$ 与物质标量系 $M$ 的点对称李代数不会自动等同，任何在标量系下求得的解都必须通过积分闭形式 $\omega_M$ 并求逆 $x = \phi(t, s)$ 才能还原为原物理场。



#### 步骤 2：构造 $n$ 阶射流丛 $J^n(M)$ 并执行“主射流消元”

* **做什么**：将未知函数及其直到 $n$ 阶的所有偏导数 $u_J^\alpha$（其中 $J$ 为长度 $\vert{}J\vert{} \le n$ 的非负整数多重指标）全部视作 $n$ 阶射流空间 $J^n(M)$ 上的**独立仿射坐标**。由于混合偏导数对称，精确 $k$ 阶导数有 $\binom{p+k-1}{k}$ 个，整个环境射流空间的维数为 $\dim J^n(M) = p + q\binom{p+n}{n}$。将 $n$ 阶 PDE 系统 $\Delta_\nu(x, u, u^{(1)}, \dots, u^{(n)}) = 0$ 定义为 $J^n(M)$ 中的方程子流形 $\mathcal{E}_\Delta$，并在非退化坐标卡上利用隐函数定理将方程显式解出**主射流（Principal jets，如最高阶时间导数 $u_t$ 或 $\phi_{ttt}$）**：



$$u_{\text{principal}} = \mathcal{G}(x, u, u_{\text{free}})$$



将其余未受约束的导数坐标归类为**自由参数射流（Free/parametric jets）**。


* **为什么这么做**：点变换不仅改变坐标 $(x, u)$，还会通过链式法则改变各阶导数。在求出具体解之前，必须把偏导数从“作用在函数上的微分算子”剥离出来，转化为几何空间中可自由取值的独立代数变量（注意：这种独立性是局部纤维坐标的代数自由性，并不意味着射流空间具有某种先验的正交黎曼度量）。消去主射流是为了将后续的对称检验严格限制在方程子流形 $\mathcal{E}_\Delta$ 的切空间内。



---

### 第二阶段：$\mathfrak{g}_\Delta = \ker \mathscr{D}_\Delta$ —— 链式法则延拓与确定方程拆解

此阶段的目标是找出所有使方程流形 $\mathcal{E}_\Delta$ 保持不变的无穷小点变换生成元，将非线性的群不变性问题完全转化为求解未知系数函数的**线性偏微分方程组**。

#### 步骤 3：引入无约束点生成元 $X$ 并由链式法则推导延拓算子 $\operatorname{pr}^{(n)} X$

* **做什么**：设单参数局部李群变换流 $\Phi_\epsilon = G_\epsilon = \exp(\epsilon X)$（由常微分方程组 $\frac{\mathrm{d}\tilde{x}^i}{\mathrm{d}\epsilon} = \xi^i(\tilde{x}, \tilde{u}), \frac{\mathrm{d}\tilde{u}^\alpha}{\mathrm{d}\epsilon} = \eta^\alpha(\tilde{x}, \tilde{u})$ 定义）对应的无穷小生成元为最一般的点向量场：



$$X = \sum_{i=1}^p \xi^i(x, u) \frac{\partial}{\partial x^i} + \sum_{\alpha=1}^q \eta^\alpha(x, u) \frac{\partial}{\partial u^\alpha}$$



此处不预先假设可投影性（即不假设 $\xi^i$ 与 $u$ 无关）或多项式系数。引入沿解图延拓的全微分算子 $D_i = \partial_{x^i} + \sum_{\alpha, J} u^\alpha_{J+e_i} \partial_{u^\alpha_J}$，对变换后的图接触关系 $\mathrm{d}\tilde{u}^\alpha = \tilde{u}^\alpha_i \mathrm{d}\tilde{x}^i$（即 $D_i \tilde{u}^\alpha = \tilde{u}^\alpha_{\tilde{x}^j} D_i \tilde{x}^j$）在 $\epsilon = 0$ 处按一阶 $\epsilon$ 展开，利用链式法则递推导出各阶导数坐标的变换系数：



$$\eta^\alpha_i = D_i \eta^\alpha - u^\alpha_j D_i \xi^j, \qquad \eta^\alpha_{J+e_i} = D_i \eta^\alpha_J - u^\alpha_{J+e_j} D_i \xi^j$$



定义**特征函数（Characteristic）** $Q^\alpha = \eta^\alpha - \xi^i u^\alpha_i$，则上述递推式等价于紧凑形式：



$$\eta^\alpha_J = D_J Q^\alpha + \xi^i u^\alpha_{J+e_i}, \qquad \operatorname{pr}^{(n)} X = X + \sum_{\alpha=1}^q \sum_{1 \le |J| \le n} \eta^\alpha_J \frac{\partial}{\partial u^\alpha_J}$$


* **为什么这么做**：因为偏微分方程包含导数，必须知道点流 $\Phi_\epsilon$ 如何推动射流空间中的高阶导数坐标。由于点生成元的系数 $\xi^i(x, u)$ 和 $\eta^\alpha(x, u)$ **严格只依赖点坐标 $(x, u)$ 而不含导数**，在展开 $D_J Q^\alpha$ 时表面上产生的 $n+1$ 阶导数项 $-\xi^i u^\alpha_{J+e_i}$ 恰好与后一项 $+\xi^i u^\alpha_{J+e_i}$ 逐阶完全抵消。这保证了：


1. $n$ 阶延拓算子 $\operatorname{pr}^{(n)} X$ 严格封闭在 $J^n(M)$ 内；


2. $\eta^\alpha_J$ 关于未知函数 $(\xi, \eta)$ 及其偏导数是**严格线性**的，且关于射流坐标 $u_J^\alpha$ 是显式多项式。





#### 步骤 4：施加相切判据 $\mathscr{D}_\Delta X = 0$ 并分离自由射流系数（求解确定方程）

* **做什么**：将延拓算子作用于原方程残差，施加无穷小相切条件：



$$\mathscr{D}_\Delta X := \left. \operatorname{pr}^{(n)} X(\Delta_\nu) \right|_{\mathcal{E}_\Delta} = 0$$



具体手工操作顺序为：


1. **先微分延拓**：先按步骤 3 的公式完整写出 $\operatorname{pr}^{(n)} X(\Delta_\nu)$（注意：此步**绝不能**令特征式 $Q^\alpha = 0$，否则会混淆“将解映为解的经典对称”与“固定特定解的条件对称”）；


2. **再代入消元**：将步骤 2 的主射流关系 $u_{\text{principal}} = \mathcal{G}(x, u, u_{\text{free}})$ 代入展开式，消去所有主射流；


3. **按自由射流拆解**：将消元后的表达式整理为关于剩余自由参数射流 $r = u_{\text{free}}$ 的多项式（例如一阶拟线性系统 $\Delta = w_t + \mathbf{A}(x,w)w_x - f = 0$ 代入 $w_t = f - \mathbf{A}r$ 后，整理为关于空间导数向量 $r = w_x$ 的常数项 $c$、一次项 $\mathbf{L}r$ 与二次型项 $\mathcal{N}(r)$）；


4. **系数置零并积分**：令自由射流各独立单项式的系数恒等于零（如 $c_i = 0, \mathbf{L}_{ij} = 0, S_{i,jk} = 0$），得到关于 $\xi(x,u), \eta(x,u)$ 的超定线性偏微分方程组（**确定方程**），按参数分支求解出对称李代数 $\mathfrak{g}_\Delta = \ker \mathscr{D}_\Delta$。




* **为什么这么做**：
* **几何充分性与局部可解必要性**：几何上，$\operatorname{pr}^{(n)} X(\Delta)\vert{}_{\mathcal{E}_\Delta} = 0$ 意味着延拓向量场处处与方程超曲面 $\mathcal{E}_\Delta$ 相切；对满秩系统，相切性足以保证局部流保持 $\mathcal{E}_\Delta$ 不变（Olver 定理 2.31）。反之，要使该相切恒等式成为对称的**必要条件**（从而保证求出的代数完备），还需要方程具备**局部可解性（Local Solvability，Olver 定理 2.71/2.73）**——即 $\mathcal{E}_\Delta$ 上的每一个自由射流点都能真正穿过某个局部光滑/解析解的射流图（对超定系统还需先补充交叉求导的可积性约束）。


* **为什么能直接令单项式系数为零**：在局部可解的前提下，点 $(x, u)$ 处的自由导数 $u_{\text{free}}$ 可以取任意局部初值斜率，而未知函数 $\xi(x, u), \eta(x, u)$ 及其偏导数完全不依赖 $u_{\text{free}}$。一个关于自由变量的多项式要在开集上恒为零，其所有基底系数必须逐一恒为零（例如在浅水-河床正流速分支中，利用系数矩阵 $\mathbf{A}$ 具有三个相异实特征值的性质，仅令二次型项 $\mathcal{N}(r) = 0$ 即可直接推出生成元的可投影性 $\tau_w = \xi_w = 0$，无需事先猜测）。


* **参数分层（Strata Separation）**：在化简确定方程时，若遇到形如 $(3-m)\omega_u = 0$ 的因子，必须在除以 $(3-m)$ 之前拆分为通用分支 $m \neq 3$ 与特异分支 $m = 3$，否则会直接漏掉仅在特定本构参数下涌现的扩展标度对称。





---

### 第三阶段：$\mathfrak{g}_\Delta \supset \mathfrak{h} \xrightarrow{\exp} H \curvearrowright (\mathcal{E}_\Delta \cap \mathcal{I}_H^n)$ —— 子代数遴选与不变解图横截性

求出方程允许的对称李代数 $\mathfrak{g}_\Delta$ 后，不能随意抓起一个生成元就做变量代换，必须检验代数闭合性与几何横截性。

#### 步骤 5：选取闭合李子代数 $\mathfrak{h}$ 并利用伴随作用分类

* **做什么**：在已验证的生成元空间 $\mathfrak{g}_\Delta$ 中选取 $r$ 维子空间 $\mathfrak{h} = \operatorname{span}\{X_1, \dots, X_r\}$，验证其关于李括号 $[X_a, X_b] = X_a X_b - X_b X_a$ 满足闭合性 $[\mathfrak{h}, \mathfrak{h}] \subset \mathfrak{h}$（尤其当 $\mathfrak{g}_\Delta$ 含有以任意函数参数化的无穷维族时，必须先检验括号是否闭合）。若需系统遍历不等价的相似约化，利用李群伴随表示（Adjoint Representation）：



$$\operatorname{Ad}_{\exp(\epsilon X)} Y = (G_\epsilon)_* Y = Y - \epsilon [X, Y] + \frac{\epsilon^2}{2}[X, [X, Y]] - \cdots$$



将共轭等价的子代数归入同一轨道，构造**最优系统（Optimal System）**。


* **为什么这么做**：
1. **闭合性的作用**：只有满足李括号闭合的分布（Involutive distribution），才能由 Frobenius 定理积分生成良定义的 $r$ 维局部群轨道叶状结构（要注意：Frobenius 定理是将非交换生成元张成的**切分布整体拉直**为轨道切片，而不是将一组非交换生成元同时变成彼此交换的坐标偏导算子）。


2. **区分两种截然不同的轨道**：**伴随轨道**作用在抽象李代数 $\mathfrak{g}_\Delta$ 的一维子空间（直线 $\mathbb{R}X$）上，用于消除仅差一个群共轭变换的冗余约化分支；而**点轨道** $H \cdot (x, u)$ 作用在物理空间 $M$ 上，用于后续的自变量消元。





#### 步骤 6：检验轨道投影秩、图横截性与定解数据相容性（取交集 $\mathcal{E}_\Delta \cap \mathcal{I}_H^n$）

* **做什么**：
1. **秩与横截性检验**：对基底 $X_a = \xi_a^i \partial_{x^i} + \eta_a^\alpha \partial_{u^\alpha}$，计算总空间轨道秩 $r_{\text{tot}} = \operatorname{rank}[\xi_a^i, \eta_a^\alpha]$ 与底空间投影秩 $r_{\text{base}} = \operatorname{rank}[\xi_a^i]$。仅在满足常秩横截条件 $r_{\text{tot}} = r_{\text{base}} = r \le p$ 的正则开集上构造图约化。


2. **施加不变曲面条件**：定义 $H$-不变射流子流形 $\mathcal{I}_H^n = \{ D_J Q_a^\alpha = 0 \mid |J| \le n-1 \}$，其中零阶条件为：



$$Q_a^\alpha := \eta_a^\alpha(x, u) - \sum_{i=1}^p \xi_a^i(x, u) \frac{\partial u^\alpha}{\partial x^i} = 0$$


3. **定解数据相容性检验**：若原问题附带初值或边值流形 $\rho(x) = 0$ 及数据约束 $C(x, u^{(k)}) = 0$，检验 $X_a(\rho)|_{\rho=0} = 0$ 及延拓切向条件是否在数据流形上成立。




* **为什么这么做**：
* **为什么方程有对称性不代表解不变**：$\mathfrak{g}_\Delta$ 中的对称群一般是将一条解图 $\Gamma_{w_1}$ 搬运到另一条不同的解图 $\Gamma_{w_2}$。要利用群轨道消去自变量，我们只能搜寻那些**在群作用下映射为自身的不变解子族** $\operatorname{Sol}_H(\Delta)$（即 $\Phi_\epsilon(\Gamma_w) = \Gamma_w$）。


* **为什么不变解等价于 $Q_a^\alpha = 0$**：在解图 $\Gamma_w = \{u^\alpha - w^\alpha(x) = 0\}$ 上，法向约束被向量场 $X_a$ 作用的结果恰为 $X_a(u^\alpha - w^\alpha(x))\vert{}_{\Gamma_w} = \eta_a^\alpha - \xi_a^i w_i^\alpha = Q_a^\alpha$。因此，$Q_a^\alpha = 0$ 几何上表示生成元 $X_a$ 处处与解图 $\Gamma_w$ 相切，由常微分方程流唯一性，整条群轨道必然完全躺在该解曲面内部。


* **为什么要求 $r_{\text{tot}} = r_{\text{base}}$**：若 $r_{\text{base}} < r_{\text{tot}}$（例如纯垂直平移 $Z = \partial_u$，其 $\xi^i = 0, \eta = 1$，故 $r_{\text{tot}} = 1$ 但 $r_{\text{base}} = 0$），则特征式 $Q_Z = 1 \neq 0$ 恒不成立。几何上，该群轨道沿纤维垂直上升，无法投影到底空间 $B$，因此**不存在**在垂直平移下保持不变的单值函数图像 $\Gamma_w$。





---

### 第四阶段：$(\mathcal{E}_\Delta \cap \mathcal{I}_H^n) \xrightarrow{\pi_H^{(n)}} \overline{\mathcal{E}}_{\Delta, H}$ —— 轨道商投影、相似拟设与方程拉回

在确认 $\mathcal{E}_\Delta \cap \mathcal{I}_H^n$ 具有正则横截结构后，即可沿群轨道方向将全空间“压扁”投影到商流形 $M/H$ 上。

#### 步骤 7：积分群流并构造轨道商映射 $\pi_H$ 与拉直坐标卡

* **做什么**：在 $r_{\text{tot}} = r_{\text{base}} = r$ 的正则坐标卡上，通过求解特征方程 $X_a(I) = 0$ 构造局部可逆的**轨道拉直坐标系（Orbit-straightening chart）** $(y, z, v)$：


* **轨道参数坐标** $y = (y^1, \dots, y^r)$：度量点在群轨道纤维上的内部位置（单生成元下满足 $X(y) = 1$，如 $y = \log t$ 或 $y = \log x$）；


* **底空间轨道不变量（相似自变量）** $z = (z^1, \dots, z^{p-r})$：满足 $X_a(z^b) = 0$ 的独立底不变量（如 $z = s/t$ 或 $\sigma = st^2$）；


* **纤维轨道不变量（相似因变量）** $v = (v^1, \dots, v^q)$：满足 $X_a(v^\alpha) = 0$ 且关于原场变量 $u$ 局部可逆的不变量（如 $v = \phi/t$ 或 $v_h = h/x^2$）。
写出显式正变换、逆变换 $(x, u) = \Psi(y, z, v)$，并验证底雅可比与全空间雅可比行列式处处非零。定义**轨道商投影**：



$$\pi_H: M \longrightarrow M/H, \qquad (x, u) \longmapsto (z(x, u), v(x, u))$$




* **为什么这么做**：必须将**底投影 $\pi_0(x, u) = x$** 与**轨道商投影 $\pi_H(x, u) = (z, v)$** 严格区分开来——底投影将一条群轨道映射为底流形 $B$ 中的一条曲线，而商投影 $\pi_H$ 将**整条连通局部群轨道坍缩为商流形 $M/H$ 中的单独一个点**（即 $\pi_H$ 的每一根纤维恰为一条局部群轨道）。在拉直坐标系 $(y, z, v)$ 下，群作用的所有变化都被隔离在坐标 $y$ 上，生成元简化为 $\partial_{y^a}$。



#### 步骤 8：积分不变图条件，从商流形截面导出相似拟设（Ansatz）

* **做什么**：在拉直坐标系 $(y, z, v)$ 中，将不变曲面条件 $Q_a^\alpha = 0$ 改写为拉直坐标下的偏导形式：



$$\frac{\partial v^\alpha}{\partial y^a} = 0 \quad (a = 1, \dots, r;\ \alpha = 1, \dots, q)$$



对轨道坐标 $y$ 积分，消去 $v$ 对 $y$ 的依赖，令积分常数成为其余底不变量 $z$ 的未知函数 $F^\alpha(z)$，再通过逆坐标卡 $\Psi$ 还原为原变量下的**相似约化拟设**：



$$v^\alpha = F^\alpha(z^1, \dots, z^{p-r}) \quad \Longleftrightarrow \quad u = (\mathcal{T}_H F)(x)$$


* **为什么这么做**：这揭示了相似变换拟设的真实几何身份——它不是凭空凑出的代数替换，而是**商流形 $M/H$ 上的一个低维截面图 $\Gamma_F = \{(z, F(z))\} \subset M/H$**。通过商投影的逆像 $\Gamma_w = \pi_H^{-1}(\Gamma_F)$，商空间里的一条 $(p-r)$ 维轮廓被群轨道自动“扫掠”铺展成原空间 $M$ 中的 $p$ 维不变解曲面。注意：原变量 $u$ 本身在轨道上未必不变（例如 $h = x^2 H(t)$ 沿轨道随 $x^2$ 缩放），真正沿轨道不变的是商坐标比值 $v_h = h/x^2 = H(t)$。



#### 步骤 9：全导数链式法则拉回与非退化乘子分解（建立约化方程 $\overline{\mathcal{E}}_{\Delta, H}$）

* **做什么**：利用不变截面上 $\partial_{y^a} v^\alpha = 0$ 的性质，通过链式法则将原变量直到 $n$ 阶的所有偏导数 $u_J^\alpha$ 显式展开为商函数导数 $F^{(k)}(z)$ 与轨道参数 $y$ 的组合，代入全部原方程残差 $\Delta[\mathcal{T}_H F]$。将其整理为如下矩阵或标量乘子分解形式：



$$\Delta[\mathcal{T}_H F](y, z) = \mathbf{M}(y, z, F^{(k)}) \, \mathcal{R}(z, F, DF, \dots, D^n F)$$



在正则域上验证前因子矩阵（或标量乘子）满足 $\det \mathbf{M} \neq 0$，从而提取出仅含 $(p-r)$ 个自变量 $z$ 的约化微分方程组 $\overline{\mathcal{E}}_{\Delta, H}: \mathcal{R}(z, F, \dots, D^n F) = 0$。当 $p - r = 1$ 时，$\mathcal{R} = 0$ 即为常微分方程（ODE）系统。


* **为什么这么做**：
1. **为什么轨道参数 $y$ 必然从 $\mathcal{R}$ 中消失**：因为 $\mathfrak{h}$ 是经过步骤 4 严格认证的方程对称子代数，群流 $\exp(y^a X_a)$ 将方程流形 $\mathcal{E}_\Delta$ 映入自身。因此，沿轨道方向移动不会改变 $\mathcal{R} = 0$ 的零点集，所有显式依赖轨道位置 $y$ 的幂次因子（如 $t^{-2}, x^3$ 等）必然能够整体提取到可逆乘子 $\mathbf{M}$ 中。


2. **手工推导禁忌**：在完成全部高阶偏导数的链式法则求导之前，**绝不能提前令轨道坐标取常数值（如提前令 $t=1$）**，否则会直接漏掉低阶导数对 $t$ 的显式幂次因子在继续求导时产生的交叉项。同时，必须证明 $\det \mathbf{M} \neq 0$，才能严格保证 $\Delta[\mathcal{T}_H F] = 0 \Longleftrightarrow \mathcal{R} = 0$ 的充要等价性。





---

### 第五阶段：商空间 ODE 的后续内部降阶与结构分析

**核心认知边界**：第四阶段的 PDE 商投影 $\pi_H^{(n)}$ 仅将**自变量个数**从 $p$ 压缩至 $p-r=1$，它**不会自动降低微分方程的阶数 $n$**（例如 3 阶双变量 PDE 约化后得到的是 3 阶 ODE）。若要进一步降低 ODE 的阶数，必须在 ODE 射流空间上利用**第一积分**或**微分不变量商化**。

#### 步骤 10：最高阶导数非退化检验与奇异分支剥离

* **做什么**：在除以最高阶导数 $F^{(n)}(z)$ 的系数 $L(z, F, \dots, F^{(n-1)})$ 之前，先保留未除分母的多项式残差 $\mathcal{R} = L \cdot F^{(n)} + \mathcal{P}(z, F, \dots, F^{(n-1)}) = 0$。仅在 $L \neq 0$ 的开集上将其化为显式正则型 $F^{(n)} = -\mathcal{P}/L$；将 $L = 0$ 单独列为奇异正则型分支（Singular normal-form branch）返回未除方程分析。


* **为什么这么做**：$L = 0$ 仅代表显式高阶正规形在该处奇异（主系数退化），既不代表原 PDE 无解（往往有精确幂律解恰好躺在 $L=0$ 流形上），也不等价于物理激波（物理激波需要弱解形式与跃变条件）。



#### 步骤 11：对约化 ODE 执行内部降阶（两条独立途径）

* **做什么**：
* **途径 A（全微分与第一积分降阶）**：观察未除残差 $\mathcal{R}$ 是否能通过乘积法则或积分因子 $\mathcal{B}(F')$ 写为全导数 $\mathcal{R} = \frac{\mathrm{d}}{\mathrm{d}z} I(z, F, F', \dots, F^{(n-1)}) = 0$（例如共同标度约化下 $\mathcal{R} = (L F'')' = 0$，或行波约化下 $\mathcal{B}(P)P'' + \mathcal{B}'(P)(P')^2 = (\mathcal{B}(P)P')' = 0$）。积分一次得到 $I(z, F, \dots, F^{(n-1)}) = I_0$，其中常数 $I_0$ 由初值走迹唯一锁定。


* **途径 B（ODE 对称与微分不变量降阶）**：若原系统存在满足正规化子条件 $[Y, \mathfrak{h}] \subset \mathfrak{h}$ 的额外对称元 $Y$，它会投影为约化 ODE 的诱导对称生成元 $Z = \zeta(z, F)\partial_z + \psi(z, F)\partial_F$。此时**绝不施加 $Q_Z = 0$**，而是选取零阶不变量 $\Sigma(z, F)$（满足 $Z(\Sigma)=0$）作为新自变量，一阶微分不变量 $M(z, F, F')$（满足 $\operatorname{pr}^{(1)}Z(M)=0$）作为新因变量：


1. *垂直平移降阶*：若 ODE 不显含 $F$（允许 $Z = \partial_F$），直接令 $\mu = F'$，将 3 阶 ODE 降为关于 $\mu(z)$ 的 2 阶 ODE；


2. *标度微分不变量降阶*：若 2 阶 ODE $\mu'' = f(z, \mu, \mu')$ 允许诱导标度 $Z = 3z\partial_z - 2\mu\partial_\mu$，根据导数权重构造不变量 $\Sigma = z^{2/3}\mu$ 与 $M = z^{5/3}\mu'$，利用链式法则 $\frac{\mathrm{d}M}{\mathrm{d}\Sigma} = \frac{\mathrm{d}M/\mathrm{d}z}{\mathrm{d}\Sigma/\mathrm{d}z}$ 消去 $z$，降为关于 $M(\Sigma)$ 的 1 阶有理方程（再令倒数变量 $N = (M + \frac{2}{3}\Sigma)^{-1}$ 即可化为三次多项式型 Abel 方程）。






* **为什么这么做**：
* 在 ODE 中，自变量只有 1 个；若强令 $Q_Z = 0$（如对 $\partial_F$ 令 $1 = 0$），会直接导致代数矛盾或锁死自由度。ODE 降阶的几何机制是将由群参数联系的**一族积分曲线捆绑压缩为微分不变量商空间 $(\Sigma, M)$ 中的单条曲线**。


* 在使用 $\Sigma$ 作新自变量时，必须记录链式法则分母 $\frac{\mathrm{d}\Sigma}{\mathrm{d}z} = z^{-1}(M + \frac{2}{3}\Sigma) \neq 0$ 的横截条件。使分母恒为零的排除分支 $M + \frac{2}{3}\Sigma \equiv 0$（即 $\Sigma = \Sigma_0$ 为常数，$\mu = \Sigma_0 z^{-2/3}$）只是不能以 $\Sigma$ 为自变量，代回原未除方程反而直接给出精确幂律特解。





---

### 第六阶段：$\operatorname{Sol}_H(\Delta) \rightleftarrows \operatorname{Sol}(\overline{\mathcal{E}}_{\Delta, H})$ —— 局部解分析、逼近误差传递与物理场重构

当约化后的 ODE 无法化归为初等闭式解（如一般的三次 Abel 方程）时，需转向局部解析级数、数值积分或函数逼近，并将近似剖面安全地逆映射回原物理空间。

#### 步骤 12：建立局部适定性管域、级数递推与条件缺陷误差界

* **做什么**：
1. **局部存在唯一性（Picard 压缩）**：将正则型 ODE 写成一阶系统 $Y' = G(z, Y)$，在紧致管域 $T = [z_0, z_0+b] \times \overline{B_R(Y_0)}$ 上提取连续界 $\Vert{}G\Vert{} \le M_G$ 与局部 Lipschitz 常数 $L$。当步长满足 $b M_G \le R$ 且 $b L < 1$ 时，由积分算子 $(\mathcal{P}Y)(z) = Y_0 + \int_{z_0}^z G(r, Y(r))\,\mathrm{d}r$ 的压缩映射性质确立唯一局部 $C^1$ 解；若 $G$ 解析，则由 Cauchy–Kovalevskaya 定理（Olver 定理 2.73）确立唯一局部解析芽，并由幂级数代入给出显式系数递推。


2. **导数相容的逼近架构**：若采用半解析或神经网络混合逼近，构造单标量通道加硬约束提升因子的架构：



$$\widehat{F}_\theta(z) = P_K(z) + (z - z_0)^{K+1} N_\theta(z)$$



其中 $P_K(z)$ 为由初值走迹（及方程导出的高阶初值导数）唯一确定的 $K$ 阶 Taylor 多项式，并对同一个 $\widehat{F}_\theta$ 直接求 $n$ 阶古典导数代入原残差。


3. **条件残差-误差传递（Grönwall 估计）**：对近似状态轨迹 $\widehat{Y}(z)$ 定义连续残差缺陷 $d(z) = \widehat{Y}'(z) - G(z, \widehat{Y}(z))$。仅当精确解 $Y(z)$ 与近似解 $\widehat{Y}(z)$ **共同驻留在同一凸正则 Lipschitz 管域内**时，积分作差并乘以积分因子 $e^{-L(z-z_0)}$ 导出条件误差上界：



$$\Vert{}\widehat{Y}(z) - Y(z)\Vert{} \le e^{L(z-z_0)} \Vert{}\widehat{Y}(z_0) - Y(z_0)\Vert{} + \int_{z_0}^z e^{L(z-r)} \Vert{}d(r)\Vert{}\,\mathrm{d}r$$




* **为什么这么做**：
* **为什么禁用独立多通道预测导数**：对于 3 阶标量 ODE，若用三个独立通道 $(\widehat{F}, \widehat{P}, \widehat{C})$ 拟合一阶状态并惩罚兼容性残差 $r_1 = \widehat{F}' - \widehat{P}$ 与 $r_2 = \widehat{P}' - \widehat{C}$，根据恒等式 $\widehat{F}''' - \widehat{C}' = r_1'' + r_2'$，函数值残差 $r_1, r_2$ 很小完全无法控制其二阶与一阶导数 $r_1'', r_2'$ 的爆炸，从而导致真实的 3 阶物理残差失控。


* **区分四种数学状态**：必须严格区分**逼近定理的存在性**（如 $\tanh$ 网络在 Sobolev 范数 $W^{3,\infty}$ 下的存在性要求目标函数具备 $W^{s,\infty}, s \ge 4$ 正则性）、**优化器的实际收敛性**、**离散配置点上的采样残差**与**连续区间上的一致残差上确界 $\Vert{}d\Vert{}_\infty \le \varepsilon$**——离散采样损失低并不自动构成上述 Grönwall 误差界所需的连续包络证明。





#### 步骤 13：执行逆商映射 $\pi_H^{-1}$ 重构原物理场并核算条件数

* **做什么**：
1. **逆商提升與积分重构**：若在步骤 11 中使用了微分不变量降阶（如得到了 $N(\Sigma)$ 或 $\mu(\sigma)$），先通过积分 $\sigma = \sigma_0 \exp\int N\,\mathrm{d}\Sigma$ 和 $F = F_0 + \int \mu\,\mathrm{d}\sigma$ 恢复商截面 $F(z)$；随后通过逆商映射 $\pi_H^{-1}$ 将 $F(z)$ 代回相似关系 $u = (\mathcal{T}_H F)(x)$，恢复原自变量下的不变场。


2. **跨表象重构与误差传递（如从物质系 $M$ 回到欧拉系 $E$）**：在保证斜率下界 $\phi_s, \widehat{\phi}_s \ge q_{\min} > 0$ 的条件下，利用路径积分重构河床场 $B^L(t, s)$，再对 $x = \phi(t, s)$ 求逆得到物理坐标下的水深 $h = 1/\phi_s$ 与流速 $u = \phi_t$。在固定物理坐标 $x$ 处，由中值定理核算反演坐标偏移 $\vert{}s - \widehat{s}\vert{} \le q_{\min}^{-1} \Vert{}\widehat{\phi} - \phi\Vert{}_\infty$，并計入重构场的全局误差传递界：



$$\vert{}\widehat{f}^E(t,x) - f^E(t,x)\vert{} \le \Vert{}\widehat{f}^L - f^L\Vert{}_\infty + K_f q_{\min}^{-1} \Vert{}\widehat{\phi} - \phi\Vert{}_\infty \quad \left(K_f = \Vert{}\partial_s f^L\Vert{}_\infty\right)$$


3. **原方程最终审计**：将重构后的物理场直接代入最原始的守恒型/原始型 PDE、初边值走迹以及有限区间上的积分质量/泥沙通量平衡式进行终验。




* **为什么这么做**：
* 商空间 $M/H$ 上的无权重残差与原物理空间 $M$ 上的 PDE 残差相差非恒定的雅可比因子（如 $\Delta_1^{\mathrm{c}} = x^2 r_H$），且通过逆函数 $x = \phi(t, s)$ 与倒数 $h = 1/\phi_s$ 重构物理场时，误差会被斜率下界的倒数平方 $q_{\min}^{-2}$ 放大。


* 对于近似剖面 $\widehat{\phi}$，物质系中的闭形式相容条件 $\Delta_M = 0$ 仅近似成立，积分路径不再严格无关；仅靠积分单一偏导数构造出的河床近似场不能自动保证满足另一方向的演化方程，因此唯有在原物理坐标系下通过全部 PDE 残差与通量平衡检验，整个李群约化与重构闭环才算真正完成。





---

### 附：PDE 李群约化全流程速查表

| 阶段与几何符号 | 核心操作（做什么） | 理论依据与目的（为什么这么做） | 关键防错护栏（Guards） |
| --- | --- | --- | --- |
| **1. 射流与消元**<br>

<br>$\mathcal{E}_\Delta \subset J^n(M)$ | 导数坐标独立化，解出主射流 $u_{\text{principal}} = \mathcal{G}(x, u, u_{\text{free}})$。

 | 将微分算子转化为几何流形上的代数坐标，限制在方程切空间内。

 | 主导数前系数必须非零（如 $h > 0, q > 0$）。

 |
| **2. 延拓与拆解**<br>

<br>$\mathfrak{g}_\Delta = \ker \mathscr{D}_\Delta$ | 由链式法则求 $\operatorname{pr}^{(n)}X$，令 $\operatorname{pr}^{(n)}X(\Delta)\vert{}_{\mathcal{E}_\Delta} = 0$ 中各自由射流系数为零。

 | 点对称使 $n+1$ 阶导数抵消且对 $(\xi, \eta)$ 线性；局部可解性保证自由射流系数必逐一为零。

 | **严禁**在此步令 $Q=0$；除以含参数因子前必须先拆分参数分支。

 |
| **3. 子群与横截**<br>

<br>$\mathfrak{h} \curvearrowright \mathcal{E}_\Delta \cap \mathcal{I}_H^n$ | 检验 $[\mathfrak{h}, \mathfrak{h}] \subset \mathfrak{h}$、秩条件 $r_{\text{tot}} = r_{\text{base}} = r$，施加 $Q_a^\alpha = 0$。

 | Frobenius 定理保证轨道分布可积；$Q=0$ 保证群轨道躺在单个不变解曲面内。

 | 垂直生成元（$r_{\text{base}} = 0$）无不变图，不可用于 PDE 自变量降维。

 |
| **4. 商化与拉回**<br>

<br>$\pi_H^{(n)} \to \overline{\mathcal{E}}_{\Delta, H}$ | 构造拉直坐标 $(y, z, v)$，积分 $\partial_y v = 0$ 得 $v = F(z)$，拉回导数提取 $\Delta = \mathbf{M} \mathcal{R}$。

 | 商映射 $\pi_H$ 将整条轨道压成一点，对称性保证轨道参数 $y$ 从核心方程 $\mathcal{R}$ 中彻底分离。

 | 求完高阶导数前**严禁**提前代入 $t=1$；必须验证 $\det \mathbf{M} \neq 0$。

 |
| **5. ODE 内部降阶**<br>

<br>$\overline{\mathcal{E}}_{\Delta, H} \to \text{低阶 ODE}$ | 利用第一积分 $D_z I = 0$ 或诱导对称的微分不变量 $(\Sigma, M)$ 降低 ODE 阶数。

 | PDE 商化只减自变量个数不减阶数；ODE 降阶需靠捆绑积分曲线族或守恒水平集。

 | ODE 降阶**严禁**令 $Q_Z = 0$；单独保存 $L=0$ 与 $\mathrm{d}\Sigma/\mathrm{d}z = 0$ 的奇异特解分支。

 |
| **6. 逼近与重构**<br>

<br>$\Gamma_F \mapsto \pi_H^{-1}(\Gamma_F)$ | 单通道硬约束逼近 $\widehat{F}$，利用 Grönwall 估计传递误差，求逆重构原物理场并检验守恒律。

 | 避免多通道导数失配；克服反演雅可比与斜率倒数带来的条件数放大。

 | 采样损失不等于连续残差上界；近似解需在同一正则管域内且满足 $q \ge q_{\min} > 0$。

 |