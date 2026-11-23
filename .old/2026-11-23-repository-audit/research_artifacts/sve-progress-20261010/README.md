# Lie–ML PDE：2026-10-10 研究推进代码

这份可运行增量同时保留原文标量基准与物理对流修正后的标量模型。

已完成：

1. 对任意光滑 τ(t,s,φ)、ξ(t,s,φ)、η(t,s,φ) 的一阶点生成元延续，
   给出 X5 的非零系数障碍；范围超过旧的对角缩放类。
2. 一般 m 的共同缩放约化、显式一阶积分和二阶 ODE。
3. 常规 Eulerian SVE 到材料坐标的对流修正及局部床面重构。
4. 12 个经典参考算例与 40 次小规模 CPU 近似比较；原始候选和负面记录均保留。
5. 共同缩放的 Q、二阶微分后果、轨道秩与 Jacobian，以及两条标量
   balance law 的 density/flux/source/边界协向量通量 pullback 证书。

## 安装和运行

需要 Python 3.10 或更高；不要求 GPU、torch 或 sudo。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
python -m pytest -q
python run_all.py
```

Windows PowerShell 激活方式：`.\.venv\Scripts\Activate.ps1`。

```bash
python run_all.py --quick --out quick_results
python run_all.py --skip-learning --out classical_only
```

从既有结果重建比较图和报告：

```bash
python -m pip install -e '.[report]'
python build_report.py
```

默认结果写入 `results/`。重新运行会覆盖同一输出目录；保留当前证据时请用 `--out`。
已记录运行环境见 `results/environment.json`；可用 `requirements-recorded.txt`
复现本次的核心依赖版本。

## 文件

| 文件 | 内容 |
|---|---|
| `docs/THEORY.md` | 假设、完整推导、障碍证明、物理解释与限制 |
| `docs/FINDINGS.md` | 实际运行统计、方法比较和疑点状态 |
| `docs/EXPERIMENT_INDEX.md` | 当前证据入口、冻结载体和历史材料的优先级 |
| `docs/LEGACY_MANUSCRIPT_EXPERIMENTS.tex` | 从主文稿逐字移出的旧协议、旧表和实现记录；不作为当前证据 |
| `sve_lab/jets.py` | 有限 jet、总导数、任意点生成元延拓 |
| `sve_lab/symbolic.py` | 两种 PDE、约化 ODE、一阶积分、障碍、群商与标量守恒 pullback 证书 |
| `sve_lab/numerics.py` | 三阶与独立二阶求解、Taylor 前端、床面重构 |
| `sve_lab/trials.py` | hard-IVP tanh/Chebyshev 候选及独立原坐标残差 |
| `run_all.py` | 生成证书、参考解、40 次近似比较及原始候选 |
| `sve_lab/tube.py` | 参考解族 m∈[1,4] 的精确有理数 bootstrap 证书 |
| `tests/` | 43 项数学、群商、守恒与重构验证 |
| `results/symbolic_certificates.json` | 障碍、独立主符号、群商和标量守恒 pullback 的机器证书 |
| `results/experiment_results.json` | 所有预算、随机种子、状态和误差 |

## 证据边界

本次学习实验仅训练固定 tanh 隐层的输出权重，使用 scipy least_squares；
直接 PDE 对照确有二维自由度，但属于很小的候选类。
这些结果不支持对一般深度 PINN 的优越性、统一样本复杂度或普适加速结论。
16/40 次达到迭代预算上限，已明确记录，不能称为收敛运行。
经典 Chebyshev 控制在本次小而光滑的问题上精度最佳。

精确参考解族具有区间一致的解析 bootstrap 证明；
学习候选的正分支与 leading coefficient margin 仍按独立网格检查。
点对称性障碍仅针对所声明的两个标量模型，不是完整床面扩展系统的最大分类。
不覆盖弱解、冲击波、非局部对称性、分数阶算子或任意真实初边值数据。
