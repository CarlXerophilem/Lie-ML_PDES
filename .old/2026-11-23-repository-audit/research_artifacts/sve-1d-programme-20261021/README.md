# 一维 SVE 精确优先研究包 — 21 October 2026

核心入口是 [PLAN.md](PLAN.md)。本包交付已验收约化清单、下一步求解设计和
可运行的独立数学验证，没有声称已经求完所有SVE解。

- [17条E约化清单](REDUCTION_INVENTORY.md) / [机器记录](reduction_registry.json)。
- [E/P/M验证示例](SOLVER_DEMONSTRATION.md) / [脚本](verify_structures.py) / [结果](verification.json)。
- [文献排查](LITERATURE_1D.md) / [来源状态](literature_1d.json)。
- [结构量与降阶](STRUCTURE_MEASURES.md) / [来源](structure_sources.json)。
- [停止纯PINN及有条件混合路线](ML_DECISION.md) / [来源](ml_sources.json)。
- [独立最终评审](FINAL_REVIEW.md)。

从仓库根运行：

```powershell
python -X utf8 research_artifacts/sve-1d-programme-20261021/verify_structures.py --out build/sve-1d-verification-new.json
```

脚本拒绝覆盖已有回执；重复运行请指定新的输出名。新的运行结果写入build，
不覆盖本包冻结回执。原始编写周期位于 `build/sve-1d-programme-20261021`。

文献排查是首轮，75份本地唯一PDF尚未阅读全文。E、打印P、校正M分别报告；
新精确控制不是论文原数值实验。纯PINN已按用户决定停止。
