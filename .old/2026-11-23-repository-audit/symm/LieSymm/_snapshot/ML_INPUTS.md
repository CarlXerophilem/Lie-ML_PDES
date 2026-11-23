# 1. 输入层实际得到什么

此层把已经验证的局部解类写成可计算的坐标、剖面和重构式。它不训练网络。
对每个冻结候选，令场顺序为 `(h,u,v,B)`，约束分布为

\[
V_1=\partial_y,\qquad
V_2=\partial_t+c\partial_x+\sum_i(a_i U_i+b_i)\partial_{U_i}.
\]

两个独立方向被消去后，剩下一个自变量 `z=x-c*t`。沿 `V2` 的场变化满足
最简单的一阶方程 `dU_i/dt=a_i U_i+b_i`，所以

\[
U_i(t,x,y)=
\begin{cases}
e^{a_it}F_i(x-ct)+b_i(e^{a_it}-1)/a_i,&a_i\ne0,\\
F_i(x-ct)+b_it,&a_i=0.
\end{cases}
\]

这给出输入不变量和输出重构。`F_i` 仍须满足导出的剖面方程；任取四个函数
并不一定得到 SVE 解。初值是 `F_i(x)`，且须与 `y` 无关。

# 2. 时间项如何精确消去

冻结表中的 `a_i` 都是整数。代入原始四条 PDE 后，残差是有限和

\[
\sum_{j,k}t^k e^{jt}R_{j,k}(F,F')=0.
\]

`ml_adapter.py` 用同一个 `rho=exp(t)` 表达所有指数项，先按照实际乘法规则
合并同底幂，再收集 `rho**j*t**k`。不同指数率和多项式次数的有限指数多项式
在任意开时间区间上线性独立，因此所有 `R_{j,k}=0` 是必要且充分的剖面条件。
这一步没有把相互有关的幂当成独立符号，也没有除以 `u`、行波速度差或特征行列式。

# 3. 证书、定义域与状态

每个 `ml_certificate.json` 给出不变量坐标、四个剖面、重构映射、原 PDE 拉回式、
全部时间系数方程、定义域、初始时间导数、边界／通量条件和零残差证书。
底空间坐标变换的行列式为 `1`，场映射的行列式为 `exp(t*sum(a_i))>0`。

分清三个事实：

1. 图的 `Q=0`、可逆性和 PDE 拉回恒等式可以验证，即使候选不是条件对称。
2. 条件对称是否成立由 `nonclassical.py` 的联合方程流形判据决定。
3. 独立评审及发布状态由 `STAGE_3_GATE.json` 的当前哈希校验决定。

完整声明域要求 `g,K>0,h>0,u²+v²>0`。仅在常规子域成立的速度平移候选还要求
`u!=0`。失效候选保留为 `diagnostic_graph_only`，不能进入已接纳输入接口。
即使一个特别构造的解能够穿过 `u=0`，也不能据此删除条件对称判据的子域限制。

# 4. 调用方式

集合运行器生成所有证书。数据端应调用 `encode_certificate`，让证书控制附加条件：

```python
import json
from ml_adapter import encode_certificate, decode
from stage3_gate import check

assert check()['passed']
certificate = json.load(open('runs/stage3-candidates-final/C01/ml_certificate.json'))
inputs = encode_certificate(certificate, t=0.2, x=1, y=0,
                            fields=(2, 1, 0.5, 0), gravity=1, transport=1)
assert inputs['valid_domain']
candidate = {'id': certificate['candidate_id'], **certificate['affine_coefficients']}
reconstructed = decode(candidate, 0.2, inputs['profiles'])
```

数值掩码只检查点值的定义域；PDE、数据和边界兼容性须另外满足证书中的方程。
有限浮点溢出与数学上有限时间的可逆性是两个问题。接口拒绝非有限输入，编码溢出
返回无效掩码；解码溢出抛出错误。

# 5. 后续机器学习的准确边界

若以后学习 `F_i(z)`，这些特征适用于证书指定的约束解类。当前完成的是输入／重构
验证，尚无训练、泛化误差估计或优于直接符号计算／经典求解器的证据。
分布不是经典分布，并不保证产生此前经典方法无法得到的解族；两者的结论在
`NONCLASSICAL_EQUIVALENCE.md` 中分开说明。
