# SVE general-symm 推导与验证周期

此目录实现已批准的研究流程。历史源码、冻结 ZIP/manifest、正文和文献库保持只读。
父程序接受方程、变量和分支条件；已知论文生成元只用于独立回归。

本周期的交付总览是 `DELIVERY.md`，完整文件哈希清单是 `RELEASE_MANIFEST.json`。
当前结论须通过三个阶段的门槛校验；报告中的通过数量与数学完备性分别记录。

```python
analyze(independent_variables, dependent_fields, equations,
        parameters, branch_conditions, data_case=None)
```

`main.py` 从任意生成元系数产生射流、全导数、特征 Q、延拓、方程流形上的恒等式
及自由射流的确定方程。`classification.py` 是针对声明的 SVE 模型的积分适配器，
其必要性依赖完整手工推导及独立评审；它不是任意非线性 PDE 的自动分类器。
未知模型或不匹配的方程／分支条件保留未解决状态。

二维扩展通过 `general_sve.py` 暴露同一 `analyze(...)` 接口；`main.py` 的已冻结
一维实现保持原样。`analyze_2d.py` 复用其射流和延拓，单独建立混合阶 J2 流形：
四条原方程及三条水动力方程的九个一阶微分后果。它保留 23 个自由射流，
包括 `B_tx,B_ty,B_tt`，并在光滑点函数系数域中直接收集自由射流多项式。
`radial_normal_form.py` 只使用正速度模长上的同底实幂恒等式，保留参数分层。

## 从哪里读

1. `CONTRACT.md`：研究对象、授权边界和严格阶段次序。
2. `PARENT_MODELS.md`：2022 全耦合父模型、2026 打印标量 P、校正标量 M 和物质坐标。
3. `FIRST_ORDER_DERIVATION.md`、`SLOPE_DERIVATION.md`：从任意函数到通解的必要性证明。
4. `CLASSIFICATION_REVIEW.md`：独立推导审计、负速图转移、约化及伴随作用的评审。
5. `EQUIVALENCE.md`：已验证可逆点变换和未解决的完整等价群胚问题。
6. `SUBALGEBRAS.md`：由实际伴随作用分类一维子代数，完整性单独记录。
7. `DATA_PARENT_REVIEW.md`：初值、边界通量、零速扩展和 P/M 分离的独立检查。
8. `SUMMARY_2D.md`：二维模型、17 个符号分支、完整通解公式、PDE/ODE 约化示例。
9. `FIRST_ORDER_2D_DERIVATION.md`、`SLOPE_2D_DERIVATION.md`：二维任意函数确定方程积分。
10. `CLASSIFICATION_2D_REVIEW.md`、`ALGEBRA_2D_REVIEW.md`、`DATA_2D_REVIEW.md`：
    二维独立评审。执行状态由对应 JSON 的当前源码哈希和通过字段决定。
11. `NONCLASSICAL_DERIVATION.md`、`NONCLASSICAL_EQUIVALENCE.md`：64个冻结候选的联合系统、
    奇异层、分布等价与解族经典包含关系。
12. `NONCLASSICAL_REVIEW.md`、`ML_INPUTS.md`：独立评审与经过输入／重构验证的接口。

第三阶段命令同样从项目根目录运行，输出必须选择不存在的新目录：

```powershell
python -B build/sve-general-symm-20261020/run_all.py --stage nonclassical --out build/sve-general-symm-20261020/runs/nonclassical-replay
python -B build/sve-general-symm-20261020/validate_project.py --out build/sve-general-symm-20261020/runs/validation-replay
```

正式回执保存于 `runs/stage3-candidates-final/` 与 `runs/stage3-validation/`。
发布门槛通过 `stage3_gate.check()` 校验；它同时检查前两阶段门槛、独立评审、
64个候选和全部ML证书的哈希。重放本身不覆盖冻结发布门槛。

每份 `derivation.json` 和对应 `.log` 包含编号过程：原 PDE、射流、任意 X、Q、
延拓、确定方程、生成元通解、括号／伴随、子代数代表、不变量、约化和精确重构。
不同的状态字段分别表示最大点代数、生成元有效性、子代数完整性、约化与数据兼容性。

## 一维声明族

范围是 h>0、|u|>0、g>0、K,G>=0；m 属于 [1,4]，坡度路线为 n=m-1 与 n=m。
正速图采用 u 的实幂；负速图通过 signed absolute-value 通量的精确反射转移。
不会把任意非整数 u**m 直接延拓到负数，也不会跨过 u=0。

| 子脚本 | 参数族 | 局部点代数维数 |
|---|---|---:|
| `cases/grass_generic.py` | K>0,G=0,m!=3 | 4 |
| `cases/grass_cubic.py` | K>0,G=0,m=3 | 5 |
| `cases/zero_transport.py` | K=G=0，删除 m,n | 5 |
| `cases/slope_attachment_generic.py` | K,G>0,n=m-1,m!=3 | 3 |
| `cases/slope_attachment_cubic.py` | K,G>0,m=3,n=2 | 4 |
| `cases/slope_source_generic.py` | K,G>0,n=m,m!=3 | 3 |
| `cases/slope_source_cubic.py` | K,G>0,m=n=3 | 4 |
| `cases/slope_only.py` | K=0,G>0,n in [0,4] | 4 |

每个符号脚本覆盖一个连续参数族；测试有限个指数不能替代完整参数证明。
上述最大性状态只有在 `classification_review.json` 的当前源码哈希匹配时才生效。

## 运行

在项目根目录运行，输出目录必须是此周期内尚不存在的新目录：

```powershell
python -B build/sve-general-symm-20261020/run_all.py --out build/sve-general-symm-20261020/runs/branches-new
python -B build/sve-general-symm-20261020/validate_project.py --out build/sve-general-symm-20261020/runs/validation-new
```

二维集合运行在一维门槛通过后使用：

```powershell
python -B build/sve-general-symm-20261020/run_all.py --stage 2 --out build/sve-general-symm-20261020/runs/2d-new
python -B build/sve-general-symm-20261020/general_sve.py --dimension 2 --branch slope_attachment_cubic_f_nonzero --out build/sve-general-symm-20261020/runs/2d-core-new
```

第一个命令运行全部 17 个子脚本及其约化／数据控制；第二个命令只展示核心确定方程、
通解、基和伴随作用。每次选择新输出目录。第一阶段的当前门槛已经通过，
第二阶段的最终放行仍须检查 `STAGE_2_GATE.json`，不会由执行时间或测试数量代替。

单分支可以直接执行，例如：

```powershell
python -B build/sve-general-symm-20261020/cases/slope_source_cubic.py --out build/sve-general-symm-20261020/runs/source-cubic-new
```

集合运行器逐个启动子进程，保存退出码、超时、运行时间、完整推导日志及源码哈希。
验证器运行 README 指定的 audit、data-flux、workflow、engine/chart、活动包测试和本轮测试。
失败结果保留；测试数不是必要性或最大性的证明。

`STAGE_1_GATE.json` 和 `STAGE_2_GATE.json` 必须由完整的当前证据产生。
一维门槛闭合后才研究二维；二维全部声明分支的最大分类闭合后才运行非经典搜索及 ML 导出。
缺失或过期的门槛会拒绝 `run_all.py --stage 2` / `--stage nonclassical`。

## 数据、约化与结论边界

- `reductions.py` 直接拉回原方程，检查 Q=0、不变量和局部图的可逆性。
  最高阶矩阵保持隐式，奇异分支没有被除掉；降低自变量维数不等于降低 ODE 阶数。
- `data_experiments.py` 检查均匀流、常坡加速流、平／斜／二次床初值、固定端点与初始通量。
  一个初值稳定子不保证以后所有边界数据都不变，也不构成适定性定理。
- 零速控制仅针对另行声明的光滑多项式闭合扩展。它们不属于 |u|>0 最大分类。
- 原始量与守恒量通过 q=h*u 的点变换验证。物质坐标是依赖解的坐标构造，需要单独重构。
- 完整等价群胚和更高维子代数仍是单独问题；未证明的等价不会删除参数分支。
- 本周期不声称文献首创、全局解、任意 IBVP、学习误差定理或神经算法优越性。

本轮失败与修复记录保存在 `runs/`；历史输入的保护清单为 `protected_inputs.json`。
