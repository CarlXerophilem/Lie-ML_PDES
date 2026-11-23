在李对称分析以及你提供的这份手稿（Sheets 1–18）中，“应用无穷小生成元 $X$”之所以容易令人困惑，是因为它在整个推导链条中实际上对应**四种完全不同的代数与几何运算**：

1. **求解未知生成元（Sheets 2–5）：** 将含待定函数 $\tau, \xi, \eta$ 的生成元作三阶延拓 $\operatorname{pr}^{(3)} X$，作用到原偏微分方程（PDE）上，通过分离自由射流变量解出对称代数基 $X_1, \dots, X_5$。


2. **验证与筛选标度生成元（Sheet 6）：** 利用生成元的单参数流或射流权重（Weight），直接检验算子对 PDE 各守恒项的齐次缩放作用。


3. **利用生成元将 PDE 约化为 ODE（Sheets 7–9）：** 通过求解特征方程构造不变量 $(\sigma, F)$，**施加不变曲面条件 $Q = 0$**，消去一个自变量。


4. **利用继承生成元对 ODE 逐阶降阶（Sheets 10–13）：** 将高维生成元诱导（Pushforward）**到低维空间，**不施加 $Q=0$**，而是通过零阶与一阶**微分不变量（Differential Invariants）做商空间投影，将三阶 ODE 降为二阶、再降为一阶 Abel 方程。



以下按这四个阶段，将手稿中所有省略的中间代数步骤、二阶与三阶余项展开以及生成元作用机制完整推导出来。

---

### 一、 阶段一：展开三阶延拓与二阶余项，完整求解确定方程组（对应 Sheets 2–5）

#### 1. 射流坐标设定与主导数消去（Sheet 2）

在 $m=3$ 分支下，令 $\mathfrak{b} = g\beta$（其中 $\beta = 3\kappa > 0, g > 0$），引入射流坐标简记：


$$v = \phi_t, \quad \rho = \phi_s, \quad a = \phi_{tt}, \quad l = \phi_{ts}, \quad c = \phi_{ss}, \quad T = \phi_{ttt}, \quad U = \phi_{tts}, \quad R = \phi_{tss}, \quad V = \phi_{sss}$$


原三阶标量 PDE 写作：


$$\Delta_3 = \rho T + l a - g(\rho^{-2} + \beta v^2 \rho^{-1}) R + g(2\rho^{-3} + \beta v^2 \rho^{-2}) l c - 2g\beta v \rho^{-1} l^2 = 0$$


由正则区域条件 $\rho = \phi_s > 0$，解出主导数 $T = \phi_{ttt}$：


$$T = -\frac{la}{\rho} + g(\rho^{-3} + \beta v^2 \rho^{-2}) R - g(2\rho^{-4} + \beta v^2 \rho^{-3}) l c + 2g\beta v \rho^{-2} l^2$$

#### 2. 一阶、二阶（含完整余项 $R^{tt}, R^{ts}, R^{ss}$）及三阶延拓系数的显式展开（Sheet 4）

设待定无穷小生成元为 $X = \tau(t,s,\phi)\partial_t + \xi(t,s,\phi)\partial_s + \eta(t,s,\phi)\partial_\phi$。全导数算子为：


$$D_t = \partial_t + v\partial_\phi + a\partial_v + l\partial_\rho + T\partial_a + U\partial_l + R\partial_c + \cdots$$

$$D_s = \partial_s + \rho\partial_\phi + l\partial_v + c\partial_\rho + U\partial_a + R\partial_l + V\partial_c + \cdots$$

* **一阶延拓系数 $\eta_t, \eta_s$：**
由递推公式 $\eta_i = D_i \eta - v D_i \tau - \rho D_i \xi$，完全展开得：



$$\eta_t = \eta_t + (\eta_\phi - \tau_t)v - \xi_t \rho - \tau_\phi v^2 - \xi_\phi v \rho$$


$$\eta_s = \eta_s - \tau_s v + (\eta_\phi - \xi_s)\rho - \tau_\phi v \rho - \xi_\phi \rho^2$$



（注：等号右侧下标表示对点变量 $t, s, \phi$ 的偏导数。）


* **二阶延拓系数 $\eta_{tt}, \eta_{ts}, \eta_{ss}$ 及其完整余项 $R^{tt}, R^{ts}, R^{ss}$：**
由 $\eta_{Ji} = D_i \eta_J - \phi_{Jt} D_i\tau - \phi_{Js} D_i\xi$，将二阶导数 $(a, l, c)$ 的线性主部与仅依赖一阶导数 $(v, \rho)$ 的余项分离：


1. **$\eta_{tt} = D_t \eta_t - a D_t\tau - l D_t\xi$：**

$$\eta_{tt} = (\eta_\phi - 2\tau_t - 3\tau_\phi v - \xi_\phi \rho) a - (2\xi_t + 2\xi_\phi v) l + R^{tt}$$



其中余项 $R^{tt}$ 为：

$$R^{tt} = \eta_{tt} + (2\eta_{t\phi} - \tau_{tt}) v - \xi_{tt}\rho + (\eta_{\phi\phi} - 2\tau_{t\phi}) v^2 - 2\xi_{t\phi} v\rho - \tau_{\phi\phi} v^3 - \xi_{\phi\phi} v^2\rho$$


2. **$\eta_{ts} = D_s \eta_t - a D_s\tau - l D_s\xi$：**

$$\eta_{ts} = -(\tau_s + \tau_\phi \rho) a + (\eta_\phi - \tau_t - \xi_s - 2\tau_\phi v - 2\xi_\phi \rho) l - (\xi_t + \xi_\phi v) c + R^{ts}$$



其中余项 $R^{ts}$ 为：

$$R^{ts} = \eta_{ts} + (\eta_{s\phi} - \tau_{ts}) v + (\eta_{t\phi} - \xi_{ts})\rho - \tau_{s\phi} v^2 + (\eta_{\phi\phi} - \tau_{t\phi} - \xi_{s\phi}) v\rho - \xi_{t\phi}\rho^2 - \tau_{\phi\phi} v^2\rho - \xi_{\phi\phi} v\rho^2$$


3. **$\eta_{ss} = D_s \eta_s - l D_s\tau - c D_s\xi$：**

$$\eta_{ss} = -(2\tau_s + 2\tau_\phi \rho) l + (\eta_\phi - 2\xi_s - \tau_\phi v - 3\xi_\phi \rho) c + R^{ss}$$



其中余项 $R^{ss}$ 为：

$$R^{ss} = \eta_{ss} - \tau_{ss} v + (2\eta_{s\phi} - \xi_{ss})\rho - 2\tau_{s\phi} v\rho + (\eta_{\phi\phi} - 2\xi_{s\phi})\rho^2 - \tau_{\phi\phi} v\rho^2 - \xi_{\phi\phi}\rho^3$$




* **三阶延拓系数 $\eta_{ttt}$ ($\eta_T$) 与 $\eta_{tss}$ ($\eta_R$)：**
对 $\eta_{tt}$ 作用 $D_t$、对 $\eta_{ts}$ 作用 $D_s$，并显式保留所有三阶导数 $(T, U, R, V)$ 及与一阶导数相乘的关键项：

$$\eta_T = D_t \eta_{tt} - T D_t\tau - U D_t\xi = (\eta_\phi - 3\tau_t - 4\tau_\phi v - \xi_\phi \rho) T - (3\xi_t + 3\xi_\phi v) U + \tilde{R}^{ttt}(t,s,\phi,v,\rho,a,l,c)$$


$$\eta_R = D_s \eta_{ts} - U D_s\tau - R D_s\xi = -(2\tau_s + 2\tau_\phi \rho) U + (\eta_\phi - \tau_t - 2\xi_s - 2\tau_\phi v - 3\xi_\phi \rho) R - (\xi_t + \xi_\phi v) V + \tilde{R}^{tss}(t,s,\phi,v,\rho,a,l,c)$$



#### 3. 推导 Sheet 5 表格中的 6 个决定性单项式（剥离变量依赖性）

在 Sheet 4 中，定义了清除分母后的确定多项式：


$$P := \rho^4 \left.\operatorname{pr}^{(3)} X(\Delta_3)\right|_{T = T(\text{其余射流})} = 0$$


展开式为：


$$P = \rho^4 \left[ \eta_t \frac{\partial \Delta_3}{\partial v} + \eta_s \frac{\partial \Delta_3}{\partial \rho} + \eta_{tt} \frac{\partial \Delta_3}{\partial a} + \eta_{ts} \frac{\partial \Delta_3}{\partial l} + \eta_{ss} \frac{\partial \Delta_3}{\partial c} + \rho \eta_T - g(\rho^{-2} + \beta v^2 \rho^{-1}) \eta_R \right]_{T = T(\dots)}$$


手算时无需盲目展开全部 118 项，只需按以下顺序提取三阶自由导数 $V = \phi_{sss}$ 和 $R = \phi_{tss}$ 的系数，即可重现 Sheet 5 的表格：

1. **提取含 $V = \phi_{sss}$ 的项（确定 $\xi$）：**
原方程 $\Delta_3$ 和 $T$ 的代入式中均不含 $V$。整个 $P$ 中唯一含有 $V$ 的来源是 $-g(\rho^{-2} + \beta v^2 \rho^{-1})\eta_R$ 中的 $-(\xi_t + \xi_\phi v)V$ 项。乘以 $\rho^4$ 后，含 $V$ 的部分为：



$$P\big|_{V\text{-terms}} = \rho^4 \left[-g(\rho^{-2} + \beta v^2 \rho^{-1})\right] \left[-(\xi_t + \xi_\phi v) V\right] = g(\rho^2 + \beta v^2 \rho^3)(\xi_t + \xi_\phi v) V$$



展开括号即可直接读出 Sheet 5 表格中的第 3、4 行（注：Sheet 5 表中第 3 行漏印了因子 $\beta$，但不影响符号与零点）：


* 单项式 $v^3 \rho^3 V$ 的系数：$\beta g \xi_\phi = 0 \implies \xi_\phi = 0$；


* 单项式 $v^2 \rho^3 V$ 的系数：$\beta g \xi_t = 0 \implies \xi_t = 0$。
由此立刻得到 $\xi = Z_0(s)$（仅依赖于 $s$）。




2. **提取含 $R = \phi_{tss}$ 的项（确定 $\tau$ 与 $\eta$）：**
将 $\xi_t = \xi_\phi = 0$ 代入后，考察 $P$ 中所有含 $R$（且不含二阶导数 $a,l,c$）的项。它们来自以下四处：


* 来自 $\rho^4 \eta_t \frac{\partial \Delta_3}{\partial v}$：其中 $\frac{\partial \Delta_3}{\partial v}\big\vert{}_R = -2g\beta v \rho^{-1} R$，贡献为 $-2g\beta v \rho^3 \eta_t R$；


* 来自 $\rho^4 \eta_s \frac{\partial \Delta_3}{\partial \rho}$：其中 $\frac{\partial \Delta_3}{\partial \rho}\big\vert{}_R = T\big\vert{}_R + g(2\rho^{-3} + \beta v^2 \rho^{-2})R = g(3\rho^{-3} + 2\beta v^2 \rho^{-2})R$，贡献为 $g(3\rho + 2\beta v^2 \rho^2)\eta_s R$；


* 来自 $\rho^5 \eta_T\big\vert{}_R$：由 $\eta_T$ 中 $(\eta_\phi - 3\tau_t - 4\tau_\phi v)T$ 代入 $T\big\vert{}_R = g(\rho^{-3} + \beta v^2 \rho^{-2})R$，贡献为 $g(\rho^2 + \beta v^2 \rho^3)(\eta_\phi - 3\tau_t - 4\tau_\phi v)R$；


* 来自 $-\rho^4 g(\rho^{-2} + \beta v^2 \rho^{-1})\eta_R\big\vert{}_R$：贡献为 $-g(\rho^2 + \beta v^2 \rho^3)(\eta_\phi - \tau_t - 2\xi_s - 2\tau_\phi v)R$。




将上述四项相加，并代入 $\eta_t = \eta_t + (\eta_\phi - \tau_t)v - \tau_\phi v^2$ 与 $\eta_s = \eta_s - \tau_s v + (\eta_\phi - \xi_s)\rho - \tau_\phi v\rho$，整理含 $\beta g$ 的各项系数：



$$P\big|_{\beta g R\text{-terms}} = \beta g R \Big[ -2v\rho^3\big(\eta_t + (\eta_\phi - \tau_t)v - \tau_\phi v^2\big) + 2v^2\rho^2\big(\eta_s - \tau_s v + (\eta_\phi - \xi_s)\rho - \tau_\phi v\rho\big) + v^2\rho^3(\eta_\phi - 3\tau_t - 4\tau_\phi v) - v^2\rho^3(\eta_\phi - \tau_t - 2\xi_s - 2\tau_\phi v) \Big]$$



逐项合并同类项，直接读出 Sheet 5 表格中剩余的 4 行：


* 单项式 $v^3 \rho^3 R$ 的系数：$(2 - 2 - 4 + 2)\beta g \tau_\phi = -2\beta g \tau_\phi = 0 \implies \tau_\phi = 0$；


* 单项式 $v^3 \rho^2 R$ 的系数：$-2\beta g \tau_s = 0 \implies \tau_s = 0$；


* 单项式 $v^2 \rho^2 R$ 的系数：$2\beta g \eta_s = 0 \implies \eta_s = 0$；


* 单项式 $v \rho^3 R$ 的系数：$-2\beta g \eta_t = 0 \implies \eta_t = 0$。




至此，三个生成元系数被完全分离为单变量函数：



$$\tau = T_0(t), \qquad \xi = Z_0(s), \qquad \eta = H_0(\phi)$$


3. **代回分离后的函数求解剩余常微分方程（Sheet 5 下半部分）：**
当 $\tau = T_0(t), \xi = Z_0(s), \eta = H_0(\phi)$ 时，所有交叉偏导数全为 $0$，延拓系数急剧简化为：

$$\eta_t = (H_0' - T_0')v, \qquad \eta_s = (H_0' - Z_0')\rho$$


$$\eta_{tt} = (H_0' - 2T_0')a + H_0'' v^2 - T_0'' v, \qquad \eta_{ts} = (H_0' - T_0' - Z_0')l + H_0'' v\rho, \qquad \eta_{ss} = (H_0' - 2Z_0')c + H_0'' \rho^2 - Z_0'' \rho$$


$$\eta_T = (H_0' - 3T_0')T + 3H_0'' va - T_0''' v + H_0''' v^3, \qquad \eta_R = (H_0' - T_0' - 2Z_0')R + H_0''(\rho a + 2vl) + \cdots$$



将它们代回 $P = 0$：


* 提取含 $H_0''$ 的二次导数耦合项（如 $v\rho^4 l a$ 等），得 $4H_0''(\phi) = 0 \implies H_0(\phi) = e_0 + c_0 \phi$（线性函数）；


* 提取 $a, l, c$ 一次项中的二阶导数余项，得 $-T_0''(t) = 0$ 和 $-g Z_0''(s) = 0$，故 $T_0'(t)$ 与 $Z_0'(s)$ 均为常数；


* 提取不含 $\beta$ 的引力项系数（如 $\rho^2 R$ 的系数）：

$$g\rho^2 R \big[ 3(H_0' - Z_0') + (H_0' - 3T_0') - (H_0' - T_0' - 2Z_0') \big] = g(3H_0' - 2T_0' - Z_0')\rho^2 R = 0$$



这正是 Sheet 5 给出的关键代数约束：



$$g(3H_0' - 2T_0' - Z_0') = 0 \implies Z_0' = 3H_0' - 2T_0'$$



令 $H_0' = c_0$，$T_0' = c_0 + d_0$，则上式给出 $Z_0' = 3c_0 - 2(c_0 + d_0) = c_0 - 2d_0$。积分后即得全部点对称生成元通解：



$$\tau(t) = a_0 + (c_0 + d_0)t, \qquad \xi(s) = b_0 + (c_0 - 2d_0)s, \qquad \eta(\phi) = e_0 + c_0\phi$$



按 5 个独立常数 $(a_0, b_0, e_0, c_0, d_0)$ 拆分，即得 5 维李代数基：



$$X_1 = \partial_t, \quad X_2 = \partial_s, \quad X_3 = \partial_\phi, \quad X_4 = t\partial_t + s\partial_s + \phi\partial_\phi, \quad X_5 = t\partial_t - 2s\partial_s$$





---

### 二、 阶段二：应用标度生成元 $X_5$ 的“权重法（Weight Method）”（对应 Sheet 6）

当你手里已经有了一个具体的标度生成元（如例外生成元 $X_5 = t\partial_t - 2s\partial_s + 0\partial_\phi$），**绝对不要**再去套用第一阶段那套复杂的延拓余项公式，而是使用 Sheet 6 的**流变换与射流权重法**：

1. **求解单参数群流（Flow）：**
解常微分方程组：



$$\frac{d\bar{t}}{d\epsilon} = \bar{t}, \quad \frac{d\bar{s}}{d\epsilon} = -2\bar{s}, \quad \frac{d\bar{\phi}}{d\epsilon} = 0 \implies \bar{t} = e^\epsilon t, \quad \bar{s} = e^{-2\epsilon}s, \quad \bar{\phi} = \phi$$


2. **计算算子与射流坐标的权重（Weight）：**
在 $(\bar{t}, \bar{s}, \bar{\phi}) = (e^\epsilon t, e^{-2\epsilon}s, \phi)$ 下，根据链式法则：

$$D_{\bar{t}} = e^{-\epsilon} D_t \implies D_t \text{ 的权重为 } -1$$


$$D_{\bar{s}} = e^{2\epsilon} D_s \implies D_s \text{ 的权重为 } +2$$



由于 $\phi$ 本身权重为 $0$，任意高阶偏导数 $\phi_{t^a s^j} = D_t^a D_s^j \phi$ 在群变换下变为 $e^{(2j - a)\epsilon}\phi_{t^a s^j}$，其权重（Weight）直接由导数阶数决定：



$$w(\phi_{t^a s^j}) = 2j - a$$



对指数 $e^{(2j-a)\epsilon}$ 在 $\epsilon = 0$ 处求导，即得延拓生成元作用在任意射流变量上的法则：**直接乘以其权重**：



$$\operatorname{pr}^{(3)} X_5(\phi_{t^a s^j}) = (2j - a)\phi_{t^a s^j}$$



例如：$w(\phi_t) = -1, w(\phi_s) = 2, w(\phi_{tt}) = -2, w(\phi_{ts}) = 1, w(\phi_{ss}) = 4$。


3. **直接作用于原方程两端验证对称性：**
将原方程拆为两项 $\Delta_m = A_m - B_m$：


* 第一项 $A_m = D_t\left(\phi_s\phi_{tt} - g\frac{\phi_{ss}}{\phi_s^2}\right)$：
括号内第一部分 $\phi_s\phi_{tt}$ 的权重为 $w(\phi_s) + w(\phi_{tt}) = 2 + (-2) = 0$；第二部分 $\frac{\phi_{ss}}{\phi_s^2}$ 的权重为 $w(\phi_{ss}) - 2w(\phi_s) = 4 - 2(2) = 0$。再作用一次 $D_t$（权重为 $-1$），故整项 $A_m$ 的总权重为 $0 + (-1) = -1$！因此：



$$\operatorname{pr}^{(3)} X_5(A_m) = -1 \cdot A_m = -A_m$$


* 第二项 $B_m = g\beta D_s\left(\phi_t^{m-1}\frac{\phi_{ts}}{\phi_s}\right)$：
括号内权重为 $(m-1)w(\phi_t) + w(\phi_{ts}) - w(\phi_s) = (m-1)(-1) + 1 - 2 = -m$。再作用一次 $D_s$（权重为 $+2$），故整项 $B_m$ 的总权重为 $2 - m$！因此：



$$\operatorname{pr}^{(3)} X_5(B_m) = (2 - m) B_m$$



两者相减即得 Sheet 6 的核心恒等式：



$$\operatorname{pr}^{(3)} X_5(\Delta_m) = -A_m - (2-m)B_m = -(A_m - B_m) + (m-3)B_m = -\Delta_m + (m-3)B_m$$



当且仅当 $m=3$ 时，余项 $(m-3)B_m$ 消失，$\operatorname{pr}^{(3)} X_5(\Delta_3) = -\Delta_3$ 在解流形 $\Delta_3 = 0$ 上恒等于 $0$。





---

### 三、 阶段三：应用生成元 $X_5$ 将 PDE 约化为三阶 ODE（对应 Sheets 7–9）

证明了 $X_5 = t\partial_t - 2s\partial_s$ 是对称生成元后，如何用它把二元函数 $\phi(t,s)$ 的偏微分方程变成一元函数 $F(\sigma)$ 的常微分方程？标准操作分为四步：

#### 第一步：解特征方程求零阶不变量（Sheet 7）

对于 $X_5 = t\partial_t - 2s\partial_s + 0\partial_\phi$，写出拉格朗日特征方程组：


$$\frac{dt}{t} = \frac{ds}{-2s}, \qquad d\phi = 0$$

* 由第一式：$2\frac{dt}{t} + \frac{ds}{s} = 0 \implies d(\ln(st^2)) = 0 \implies \sigma := st^2 = \text{常数}$（自变量相似不变量）；


* 由第二式：$F := \phi = \text{常数}$（因变量相似不变量）。



#### 第二步：补全顺直坐标系（Canonical Coordinates）并施加不变曲面条件（Sheet 7）

为了让生成元 $X_5$ 变成单坐标平移算子 $\partial_y$，再选一个辅助轨道坐标 $y(t,s)$ 使其满足 $X_5(y) = 1$。
取 $y = \ln t$，检验得：


$$X_5(y) = t\frac{\partial(\ln t)}{\partial t} - 2s\frac{\partial(\ln t)}{\partial s} = 1, \qquad X_5(\sigma) = t(2st) - 2s(t^2) = 0, \qquad X_5(F) = 0$$


因此在 $(y, \sigma, F)$ 坐标系下，生成元化为最简平移形式 $X_5 = \partial_y$。

接着，写出生成元 $X_5$ 的**特征函数（Characteristic）** $Q$ 并令其为 $0$（即寻找在群变换下保持不变的解曲面）：


$$Q := \eta - \tau\phi_t - \xi\phi_s = 0 - t\phi_t - (-2s)\phi_s = -t\phi_t + 2s\phi_s = 0$$


在 $(y, \sigma, F)$ 坐标下，$-t\phi_t + 2s\phi_s = -X_5(\phi) = -\partial_y F = 0$，这意味着 $F$ 不依赖于轨道坐标 $y$，只依赖于不变量 $\sigma$：


$$\phi(t, s) = F(\sigma), \qquad \sigma = st^2$$

#### 第三步：转换全导数算子并逐阶求偏导（Sheet 8）

由多元复合函数求导法则，原自变量 $(t, s)$ 的全导数算子在新坐标 $(y=\ln t, \sigma=st^2)$ 下表示为：


$$D_t = \frac{\partial y}{\partial t} D_y + \frac{\partial \sigma}{\partial t} D_\sigma = \frac{1}{t} D_y + 2st D_\sigma = \frac{1}{t} D_y + \frac{2\sigma}{t} D_\sigma$$

$$D_s = \frac{\partial y}{\partial s} D_y + \frac{\partial \sigma}{\partial s} D_\sigma = 0 \cdot D_y + t^2 D_\sigma = t^2 D_\sigma$$


记剖面函数的各阶常导数为 $p = F'(\sigma), q = F''(\sigma), r = F'''(\sigma)$。**注意一个极易算错的细节**：虽然 $F(\sigma)$ 不含 $y$（即 $D_y F = D_y p = D_y q = 0$），但一旦求导后出现了显式的 $t = e^y$ 因子，再次作用 $D_t$ 时必须对显式的 $t$ 因子求导（或者直接在原式上对 $t$ 用乘积法则）！

* **一阶导数：**

$$\phi_t = D_t F(\sigma) = \frac{2\sigma}{t} F'(\sigma) = \frac{2\sigma p}{t}, \qquad \phi_s = D_s F(\sigma) = t^2 F'(\sigma) = t^2 p$$


* **二阶导数：**

$$\phi_{tt} = D_t\left(\frac{2\sigma p}{t}\right) = \frac{\partial}{\partial t}\left(\frac{1}{t}\right)(2\sigma p) + \frac{1}{t}\frac{2\sigma}{t}\frac{d}{d\sigma}(2\sigma p) = -\frac{2\sigma p}{t^2} + \frac{2\sigma}{t^2}(2p + 2\sigma q) = \frac{2\sigma p + 4\sigma^2 q}{t^2}$$


$$\phi_{ts} = D_s\left(\frac{2\sigma p}{t}\right) = \frac{1}{t}\cdot t^2 \frac{d}{d\sigma}(2\sigma p) = 2t(p + \sigma q)$$


$$\phi_{ss} = D_s(t^2 p) = t^2 \cdot t^2 \frac{dp}{d\sigma} = t^4 q$$



#### 第四步：保留散度形式代入 PDE，消去非不变因子 $t$（Sheet 9）

将 Sheet 8 的导数代入原散度方程 $\Delta_3 = D_t(\phi_s\phi_{tt} - g\phi_{ss}/\phi_s^2) - \mathfrak{b} D_s(\phi_t^2 \phi_{ts}/\phi_s) = 0$：

1. 先算第一个括号内部：

$$\phi_s\phi_{tt} - g\frac{\phi_{ss}}{\phi_s^2} = (t^2 p)\frac{2\sigma p + 4\sigma^2 q}{t^2} - g\frac{t^4 q}{(t^2 p)^2} = 2\sigma p^2 + 4\sigma^2 pq - \frac{gq}{p^2} =: \mathcal{A}(\sigma)$$



由于 $\mathcal{A}(\sigma)$ 完全不含显式的 $t$（即 $D_y \mathcal{A} = 0$），对其作用 $D_t$ 极其简便：



$$D_t \mathcal{A}(\sigma) = \frac{2\sigma}{t} \mathcal{A}'(\sigma)$$


2. 再算第二个括号内部：

$$\phi_t^2 \frac{\phi_{ts}}{\phi_s} = \left(\frac{4\sigma^2 p^2}{t^2}\right)\frac{2t(p + \sigma q)}{t^2 p} = t^{-3} \cdot 8\sigma^2 p(p + \sigma q) =: t^{-3} \mathcal{B}(\sigma)$$



对其作用 $D_s = t^2 D_\sigma$（此时 $t^{-3}$ 对 $s$ 是常数）：



$$D_s\big(t^{-3}\mathcal{B}(\sigma)\big) = t^2 \cdot t^{-3} \mathcal{B}'(\sigma) = \frac{1}{t}\mathcal{B}'(\sigma)$$


3. 合并两项，非不变坐标 $t$ 自动提取为整体公因子 $\frac{1}{t}$：



$$\Delta_3[F(st^2)] = \frac{1}{t}\big(2\sigma \mathcal{A}'(\sigma) - \mathfrak{b} \mathcal{B}'(\sigma)\big) = -\frac{2\sigma}{t p^3} \mathcal{R}_3[F] = 0$$



将 $\mathcal{A}'$ 与 $\mathcal{B}'$ 展开合并，即得三阶常微分方程 $\mathcal{R}_3 = 0$：



$$\mathcal{R}_3 = p\big[g + 4(\mathfrak{b}-1)\sigma^2 p^3\big]r + \big[4(\mathfrak{b}-1)\sigma^2 p^3 - 2g\big]q^2 + (20\mathfrak{b}-12)\sigma p^4 q + (8\mathfrak{b}-2)p^5 = 0$$



---

### 四、 阶段四：应用继承生成元将三阶 ODE 逐次降为一阶 Abel 方程（对应 Sheets 10–13）

**核心概念区分（为什么 ODE 降阶不能像 PDE 那样令 $Q = 0$？）：**

* 对 **PDE** 施加 $Q = 0$，是在解空间中切出一个特殊的不变解子族，将**自变量个数**从 2 个降为 1 个，但微分阶数仍是 3 阶。


* 对 **ODE** 而言，自变量只有 1 个（$\sigma$）。如果强行令 $Q = 0$，比如对平移生成元 $Z = \partial_F$ 令 $Q_Z = 1 - 0\cdot F' = 1 = 0$，根本无解！对 ODE 应用生成元的正确方法是**构造零阶与一阶微分不变量（Differential Invariants）**，在李群轨道的商空间上改写方程，从而在不丢失通解积分常数的前提下，每应用一个单参数生成元就将 **ODE 的微分阶数降低 1 阶**。



#### 第一步：应用平移生成元 $Z = \partial_F$ 将三阶 ODE 降为二阶 ODE（Sheet 10）

1. **识别生成元与不变量：**
观察 $\mathcal{R}_3$，方程中只出现了导数 $p = F', q = F'', r = F'''$，没有显式出现因变量 $F$。这意味着平移算子 $Z = 0\partial_\sigma + 1\partial_F = \partial_F$ 是 $\mathcal{R}_3 = 0$ 的对称生成元。


2. **一阶延拓与微分不变量：**
因为 $Z$ 的系数全是常数，其各阶延拓系数全为 $0$：

$$\operatorname{pr}^{(3)} Z = \partial_F + 0\partial_{F'} + 0\partial_{F''} + 0\partial_{F'''}$$



したがって，它的零阶不变量是 $\sigma$，一阶微分不变量是 $\mu(\sigma) := F'(\sigma) = p$。


3. **代换降阶：**
令 $\mu = F'(\sigma)$，则 $q = F'' = \mu'$，$r = F''' = \mu''$。代入 $\mathcal{R}_3 = 0$，三阶 ODE 立即降为关于 $\mu(\sigma)$ 的二阶 ODE $\mathcal{R}_2 = 0$：



$$\mathcal{R}_2 = \mu\big[g + 4(\mathfrak{b}-1)\sigma^2 \mu^3\big]\mu'' + \big[4(\mathfrak{b}-1)\sigma^2 \mu^3 - 2g\big](\mu')^2 + (20\mathfrak{b}-12)\sigma \mu^4 \mu' + (8\mathfrak{b}-2)\mu^5 = 0$$



#### 第二步：计算生成元的“诱导映射（Pushforward）” $X_4 \mapsto Y \mapsto Y_1$（Sheet 10 下半部分）

原 PDE 还有一个标度对称生成元 $X_4 = t\partial_t + s\partial_s + \phi\partial_\phi$。如何把它“搬运（诱导）”到新的变量 $(\sigma, \mu)$ 上？

1. **检查李括号可交换性：**
计算李括号 $[X_4, X_5]$：

$$[X_4, X_5] = [t\partial_t + s\partial_s + \phi\partial_\phi, \, t\partial_t - 2s\partial_s] = (t\cdot 1 - t\cdot 1)\partial_t + (s(-2) - (-2s)(1))\partial_s = 0$$



因为 $[X_4, X_5] = 0$，$X_4$ 保持 $X_5$ 的不变量子空间不变，必然可以投影到 $(\sigma, F)$ 空间上。


2. **将 $X_4$ 投影到 $(\sigma, F)$ 空间得到生成元 $Y$：**
直接将算子 $X_4 = t\partial_t + s\partial_s + \phi\partial_\phi$ 作用在坐标函数 $\sigma = st^2$ 和 $F = \phi$ 上：

$$Y(\sigma) = X_4(st^2) = t\frac{\partial(st^2)}{\partial t} + s\frac{\partial(st^2)}{\partial s} = t(2st) + s(t^2) = 3st^2 = 3\sigma$$


$$Y(F) = X_4(\phi) = \phi = F$$



所以在 $(\sigma, F)$ 平面上，诱导出的对称生成元为：



$$Y = 3\sigma\partial_\sigma + F\partial_F$$


3. **将 $Y$ 投影到 $(\sigma, \mu)$ 空间得到生成元 $Y_1$：**
因为 $\mu = F'(\sigma)$ 是 $F$ 对 $\sigma$ 的一阶导数，我们需要计算 $Y = 3\sigma\partial_\sigma + F\partial_F$ 在一阶导数 $\mu = F'$ 上的延拓系数 $\eta^\mu$：



$$\eta^\mu = D_\sigma(F) - \mu D_\sigma(3\sigma) = \mu - 3\mu = -2\mu$$



从而得到 $Y$ 在一阶射流空间 $(\sigma, F, \mu)$ 上的延拓为 $\operatorname{pr}^{(1)} Y = 3\sigma\partial_\sigma + F\partial_F - 2\mu\partial_\mu$。丢掉已经消去的坐标 $F$，就得到了作用在 $(\sigma, \mu)$ 平面上的诱导生成元 $Y_1$：



$$Y_1 = 3\sigma\partial_\sigma - 2\mu\partial_\mu$$



#### 第三步：应用标度生成元 $Y_1 = 3\sigma\partial_\sigma - 2\mu\partial_\mu$ 将二阶 ODE 降为一阶 ODE（Sheets 11–12）

现在我们要用 $Y_1 = 3\sigma\partial_\sigma - 2\mu\partial_\mu$ 把二阶常微分方程 $\mathcal{R}_2(\sigma, \mu, \mu', \mu'') = 0$ 降为一阶方程。完整标准步骤如下：

1. **对 $Y_1$ 做一阶延拓 $\operatorname{pr}^{(1)} Y_1$（求 $\mu'$ 的变换系数）：**
在 $(\sigma, \mu)$ 空间中，自变量是 $\sigma$，因变量是 $\mu$，一阶导数是 $\mu' = \frac{d\mu}{d\sigma}$。套用一阶延拓公式：

$$\eta^{\mu'} = D_\sigma(-2\mu) - \mu' D_\sigma(3\sigma) = -2\mu' - 3\mu' = -5\mu'$$



因此一阶延拓算子为：



$$\operatorname{pr}^{(1)} Y_1 = 3\sigma\partial_\sigma - 2\mu\partial_\mu - 5\mu'\partial_{\mu'}$$


2. **解特征方程求零阶不变量 $\Sigma$ 与一阶微分不变量 $M$：**
写出 $\operatorname{pr}^{(1)} Y_1$ 的特征常微分方程组：



$$\frac{d\sigma}{3\sigma} = \frac{d\mu}{-2\mu} = \frac{d\mu'}{-5\mu'}$$


* **求零阶不变量 $\Sigma(\sigma, \mu)$（联立前两项）：**

$$\frac{d\mu}{\mu} = -\frac{2}{3}\frac{d\sigma}{\sigma} \implies \ln\mu + \frac{2}{3}\ln\sigma = \text{const} \implies \Sigma := \sigma^{2/3}\mu$$


* **求一阶微分不变量 $M(\sigma, \mu, \mu')$（联立第一项与第三项）：**

$$\frac{d\mu'}{\mu'} = -\frac{5}{3}\frac{d\sigma}{\sigma} \implies \ln\vert{}\mu'\vert{} + \frac{5}{3}\ln\sigma = \text{const} \implies M := \sigma^{5/3}\mu'$$



这就得到了 Sheet 11 的两个核心不变量：



$$\Sigma = \sigma^{2/3}\mu, \qquad M = \sigma^{5/3}\mu'$$




3. **用新变量 $(\Sigma, M)$ 及导数 $M_\Sigma = \frac{dM}{d\Sigma}$ 表达二阶导数 $\mu''$（Sheet 11 下半部分）：**
把 $\Sigma$ 当作新的自变量，$M = M(\Sigma)$ 当作新的因变量。


* 先对 $\Sigma = \sigma^{2/3}\mu$ 关于 $\sigma$ 求全导数：



$$\frac{d\Sigma}{d\sigma} = \frac{2}{3}\sigma^{-1/3}\mu + \sigma^{2/3}\mu' = \frac{1}{\sigma}\left(\frac{2}{3}\sigma^{2/3}\mu + \sigma^{5/3}\mu'\right) = \frac{M + \frac{2}{3}\Sigma}{\sigma}$$


* 再由 $\mu' = \sigma^{-5/3}M(\Sigma)$ 对 $\sigma$ 求全导数（应用乘积法则与链式法则 $\frac{dM}{d\sigma} = M_\Sigma \frac{d\Sigma}{d\sigma}$）：



$$\mu'' = \frac{d}{d\sigma}\left(\sigma^{-5/3}M\right) = -\frac{5}{3}\sigma^{-8/3}M + \sigma^{-5/3} M_\Sigma \frac{d\Sigma}{d\sigma} = -\frac{5}{3}\sigma^{-8/3}M + \sigma^{-5/3} M_\Sigma \left(\frac{M + \frac{2}{3}\Sigma}{\sigma}\right)$$



提取公因子 $\sigma^{-8/3}$，即得 Sheet 11 的二阶导数代换公式：



$$\mu'' = \sigma^{-8/3}\left[\left(M + \frac{2}{3}\Sigma\right)M_\Sigma - \frac{5}{3}M\right]$$




4. **代入 $\mathcal{R}_2 = 0$ 约去 $\sigma$，并作倒数平移恢复 Abel 方程（Sheets 12–13）：**
将 $\mu = \sigma^{-2/3}\Sigma$、$\mu' = \sigma^{-5/3}M$ 和 $\mu''$ 代入二阶 ODE $\mathcal{R}_2 = 0$：


* 第一项：$\mu\big[g + 4(\mathfrak{b}-1)\sigma^2\mu^3\big]\mu'' = \sigma^{-10/3}\Sigma\big[g + 4(\mathfrak{b}-1)\Sigma^3\big]\left[\left(M + \frac{2}{3}\Sigma\right)M_\Sigma - \frac{5}{3}M\right]$；


* 第二项：$\big[4(\mathfrak{b}-1)\sigma^2\mu^3 - 2g\big](\mu')^2 = \sigma^{-10/3}\big[4(\mathfrak{b}-1)\Sigma^3 - 2g\big]M^2$；


* 第三项：$(20\mathfrak{b}-12)\sigma\mu^4\mu' = \sigma^{-10/3}(20\mathfrak{b}-12)\Sigma^4 M$；


* 第四项：$(8\mathfrak{b}-2)\mu^5 = \sigma^{-10/3}(8\mathfrak{b}-2)\Sigma^5$。




每一项都精确分离出同一个非零幂因子 $\sigma^{-10/3}$！约去 $\sigma^{-10/3}$ 并按 $M$ 的幂次整理，即得关于 $M(\Sigma)$ 的一阶有理常微分方程（Sheet 12 式 (11)）：



$$\Sigma D(\Sigma)\left(M + \frac{2}{3}\Sigma\right)M_\Sigma + A(\Sigma)M^2 + B(\Sigma)M + C(\Sigma) = 0$$



最后，为了消去 $M_\Sigma$ 前面的因式 $\left(M + \frac{2}{3}\Sigma\right)$ 并化为多项式右端项，令 $N := \left(M + \frac{2}{3}\Sigma\right)^{-1}$（即 $M = \frac{1}{N} - \frac{2}{3}\Sigma$，$M_\Sigma = -\frac{N_\Sigma}{N^2} - \frac{2}{3}$），代入上式同乘 $\frac{N^3}{\Sigma D(\Sigma)}$，即完整推导出文献中的第一类 Abel 方程（Sheet 13 式 (A27)）：



$$N_\Sigma = a_3(\Sigma)N^3 + a_2(\Sigma)N^2 + a_1(\Sigma)N$$



---

### 五、 总结对照表：全流程中四次应用生成元的范式对比

| 所在页码 | 应用的生成元 | 作用对象 | 核心代数操作 | 几何/分析效果 |
| --- | --- | --- | --- | --- |
| **Sheets 2–5** | 未知点生成元 $X = \tau\partial_t + \xi\partial_s + \eta\partial_\phi$<br> | 三阶原方程 $\Delta_3 = 0$<br> | 展开 $\operatorname{pr}^{(3)} X(\Delta_3)$，代入 $T=\phi_{ttt}$，提取自由射流 $V, R, a, l, c$ 单项式系数令为 $0$<br> | 解出 5 维对称李代数基 $X_1, \dots, X_5$<br> |
| **Sheet 6**<br> | 例外标度生成元 $X_5 = t\partial_t - 2s\partial_s$<br> | 散度项 $A_m, B_m$<br> | 计算各阶偏导数权重 $w(\phi_{t^a s^j}) = 2j - a$，直接对算子做齐次幂次计数

 | 免展开验证 $\operatorname{pr}^{(3)} X_5(\Delta_3) = -\Delta_3$<br> |
| **Sheets 7–9** | 例外标度生成元 $X_5 = t\partial_t - 2s\partial_s$<br> | 二元函数 $\phi(t,s)$ 的三阶 PDE

 | 解特征方程 $\frac{dt}{t} = \frac{ds}{-2s}$ 得 $\sigma = st^2$，**令特征式 $Q = -t\phi_t + 2s\phi_s = 0$**<br> | **自变量降维：** 2 维 PDE $\to$ 1 维三阶 ODE $\mathcal{R}_3 = 0$<br> |
| **Sheets 10–13** | 平移 $Z = \partial_F$ 与诱导标度 $Y_1 = 3\sigma\partial_\sigma - 2\mu\partial_\mu$<br> | 一元函数 $F(\sigma)$ 的三阶 ODE

 | **不令 $Q=0$**；对生成元做一阶延拓，构造零阶与一阶微分不变量 $\mu = F'$ 及 $(\Sigma, M)$<br> | **微分阶数降阶：** 三阶 ODE $\to$ 二阶 ODE $\to$ 一阶 Abel 方程

 |