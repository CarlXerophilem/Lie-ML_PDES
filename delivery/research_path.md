# 研究路径与证据边界

整理基线为 `codex/final` 的 `126a598`。本页综合该提交可达的 40 条提交记录以及旧 `docs/` 的研究、教学、工作流与验收说明。[原始文档树](../.old/2026-11-23-repository-audit/docs/) 和 [实验包去向](artifact_audit.md) 可用于逐项追溯。历史验收结果按当时的合同解读。

## 从问题到论文

| 阶段 | 研究问题与方法 | 形成的证据与边界 |
|---|---|---|
| 2026 年 8–9 月，通用框架与流体基线 | 建模 \(J^n\)、生成元、延拓、确定方程和约化。比较显式推导、纯数值与学习层。 | 形成初版提案、流体试验和通用求解器草案。部署与可视化文档记录实现能力，数学结论仍需在指定方程上复核。 |
| 10 月上旬，SVE 专门化 | 将 Eulerian \(E_1\)、印刷标量 \(P\)、物质兼容标量 \(M\) 按坐标与通量分开。追踪三次点附近的参数障碍。 | 三次点的对角缩放延拓障碍有符号证据，范围限所选生成元类。学习与李理论笔记把表示、损失、误差和证书分开。 |
| 10 月第 3–4 周，约化与边界 | 从任意系数点场写出延拓和切触条件，分离自由射流。把一维最优系、轨道秩、可积性、边界稳定子和解的重构作为不同门槛。 | 约化合同、数据与通量相容检查、CPU 基线开始分开记录。138/156 谱组合通过历史门槛，神经候选与失败控制按原日志保留。 |
| 10 月中旬，逐式复现与平面探索 | 逐项比对 2026 原文式 (7) 至式 (27) 及其余代表元；用手算稿与动画解释从确定方程到相似变量。扩展到旋转与床高演化。 | 有效、需补假设与有反例的公式逐项标识。二维先导包与自由边界范围审计界定后续定理的内容。 |
| 10 月下旬，精度和严格验收 | 建立印刷 \(P\) 解族与目录，进行高精度独立参考检查。严格 CAS 重试考察任意函数、退化分支及等价消元链。 | 高精度参考 11/11，原 float64 结果 10/11。旧严格任务未通过，保留复核和运行错误的成因。晚期正图手工确定方程结果以自己的假设覆盖相应点对称，历史通用任务仍有原验收边界。 |
| 11 月，局部定理与答辩 | 以闭床一形式重构 \(E_1\)，构造行波和收敛的 Laurent 分支。将环域径向约化保留为 \(DH'=N\)，在相容鞍点构造两个穿越解芽。 | 定理、独立代入和受控采样分层。旋转换床示例采用固体涡旋剖面和 \(D_a=0\)，平面共享仿射分类的限制保留。 |
| 当前，复核与整理 | 确立 compact 论文和 Madrid 答辩，核验文献范围、复现入口与资料路径。 | `delivery/` 保留可运行证据。\(P\)–\(M\) 的比较与延拓列为待办。一般二维分类和等精度校正成本保持开放。 |

## 旧文档的阅读线索

- [Lie 约化](../.old/2026-11-23-repository-audit/docs/Lie_reduction.md)、[完整工作流](../.old/2026-11-23-repository-audit/docs/workflow.md) 和 [PDE 形式化](../.old/2026-11-23-repository-audit/docs/pde_formalization_and_reduction.md) 记录从射流相切到商方程与原方程重构。
- [方法总图](../.old/2026-11-23-repository-audit/docs/methodology-map-through-20261019.md)、[项目地图](../.old/2026-11-23-repository-audit/docs/project-map.md) 和 [研究路线](../.old/2026-11-23-repository-audit/docs/research-roadmap-20261021.md) 明确 exact-first、受控变体及扩展二维的顺序。
- [机器学习基础](../.old/2026-11-23-repository-audit/docs/The%20Mathematical%20Essence%20of%20Machine%20Learning.md)、[三层基线](../.old/2026-11-23-repository-audit/docs/three_layer_baselines.md) 和 [Week 4](../.old/2026-11-23-repository-audit/docs/week-4_plan.md) 解释为何要固定数据与验收，并独立比较经典算法。
- [式 (27) 手算](../.old/2026-11-23-repository-audit/docs/sve_equation27_handwritten_manuscript.md)、[动画脚本](../.old/2026-11-23-repository-audit/docs/2026-10-17-sve-equation27-manim.md) 和 [参考阅读](../.old/2026-11-23-repository-audit/docs/basic-reference-reading-notes-20261010.md) 是推导和教学资料。后续复现脚本给出逐式审计状态。
- [验收记录](../.old/2026-11-23-repository-audit/docs/validation.md)、[数值精度修复](../.old/2026-11-23-repository-audit/docs/residual-resolution-20261021.md) 和 [严格 CAS 失败分析](../.old/2026-11-23-repository-audit/docs/lie-failure-analysis-20261027.md) 保留工程与数学负结果。旧执行手册、远程交接、海报与通用计划随原树归档。

## 逐提交索引

提交日期采用作者日期。索引只覆盖复核基线的可达历史。

| 日期 | 短 SHA | 提交主题 |
|---|---|---|
| 2026-08-20 | [`eab3ff6c`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/eab3ff6c2c93a3a1de42c57bed40e0377c5cbdc0) | Initial import of LieML PDE symmetry research project |
| 2026-09-07 | [`7e2f0217`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/7e2f02174254a55240ba892dbc1564cb8d3f3773) | managed ref pdfs manually |
| 2026-09-08 | [`36e0d6e8`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/36e0d6e8f0e1e2232eb4a2bb75ca14f832c71639) | Paper_Coauthor gpt-5.6-Sol review ++ |
| 2026-09-12 | [`eb0f1963`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/eb0f1963d65aba16bb7233b3251c830a5626f382) | Solidified my proposal.tex ! |
| 2026-10-05 | [`7dc66897`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/7dc66897ebfdb418a0c6baea724bfc3cf06c8fcf) | Archive LieML baselines and prioritize near-cubic obstruction |
| 2026-10-05 | [`8b98b14b`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/8b98b14b4ab7c9d1e71958f1d77e33a33bb8a989) | human log removal + weird multi-agent skill |
| 2026-10-07 | [`8b6794a5`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/8b6794a508ea4a68083a9330364f672f9ce39f72) | revise new ideas_1 |
| 2026-10-07 | [`a31ab545`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/a31ab5454b9bd3f466ec936234b99c3ad8c4a970) | revise new ideas_1 |
| 2026-10-07 | [`f9fc11de`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/f9fc11dea40cfee5a3da406b67942b3c2c8dcfe6) | revise new ideas_1 |
| 2026-10-08 | [`e1b43622`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/e1b43622991e9e2fa524bd5d4554bce10b6e2987) | docs: design Lie-ML Q&A revision |
| 2026-10-08 | [`0e843cba`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/0e843cbab35d5a6203660f16d7df2c0d5878c517) | docs: separate ML and Lie foundations |
| 2026-10-08 | [`b0593146`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/b05931462a6717ff8e59d23fdb0004577fdcaadb) | deleted old files |
| 2026-10-09 | [`3a379306`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/3a37930637a6ed0966282e990832920ed39d9e28) | wrote interim week-3 report |
| 2026-10-09 | [`09d8ff7c`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/09d8ff7c21567b7a22e3d85a52fee1de81d809a1) | gtm 107 added |
| 2026-10-10 | [`cc901a43`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/cc901a43aec695cc8cb448229ce932b198c991c9) | Finished Methodology construction preliminaries. |
| 2026-10-10 | [`4f21dd10`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/4f21dd105f50fc3e24d355af9a7eaa1d6657abf2) | interim |
| 2026-10-11 | [`5e913b59`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/5e913b591b98989b970557a388cbf986c41319cb) | astra-free! |
| 2026-10-11 | [`1917e24a`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/1917e24a20932162fe78f470402070a0e3f60923) | astra free! |
| 2026-10-11 | [`3bc20b08`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/3bc20b083ed476d4f4bcf7564d6dd7c828269f03) | Configure Git LFS for PDF files |
| 2026-10-11 | [`e373ab08`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/e373ab08f6bb8894b73154a30a2b4af1fca3b7ca) | ?lfs? |
| 2026-10-12 | [`9849f822`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/9849f822a7c7cda6bc745b82d868438c2d8a4b13) | organized project tree |
| 2026-10-12 | [`e65b89c5`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/e65b89c56fe077503396b695d8ada5a6edbb3bf5) | organized project tree |
| 2026-10-13 | [`f8a77836`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/f8a778362953d333d6069072c71b6f7d88cf0463) | Reproduce SVE reductions and expand verified manuscript exposition |
| 2026-10-13 | [`f5ed597b`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/f5ed597b18f96fba0eae0f9ebb4fc99e5ca844df) | Clarify SVE replication with source-led tables and direct reductions |
| 2026-10-16 | [`7dac2292`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/7dac22925fa9319b61541d47f92c3b0801086001) | Publish reviewed 2D SVE extension and free-boundary scope inspections |
| 2026-10-16 | [`b058d698`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/b058d698191ea0cc66bd5050bf73629e202e15a4) | Fix research publication paths and record independent review |
| 2026-10-17 | [`39d0f80d`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/39d0f80d6180abf31c65704ede2cbd79e174d26c) | Save equation 27 manuscript, presentation, and reference reorganization |
| 2026-10-19 | [`84df7786`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/84df778685db89100e3debbe27e61e7c897cabb9) | updated Lie-Lie_reduction theories |
| 2026-10-20 | [`545eb437`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/545eb43781d599b534948e8ea3dbac54088c3934) | Archive obsolete builds and publish reviewed 1D SVE solver programme |
| 2026-10-21 | [`78ecd5d6`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/78ecd5d6ab90ca7a9cb806975dae6d43c273c0bb) | Publish LieSymm printed-P solutions and portable computation evidence |
| 2026-10-21 | [`11fe2a80`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/11fe2a8042a468405fa1b60056114ae826e34c59) | Resolve printed-P numerical precision and update research roadmap |
| 2026-10-21 | [`cbe752dd`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/cbe752dd645c6718871f07beae2f49624ddd35be) | Compact historical evidence and prepare portable Priestess handoff |
| 2026-10-26 | [`57fcc19b`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/57fcc19be31b7a4d3707e9f9e4f67eeddc7e9bdf) | Add strict CAS verification, native retry evidence and concise dissertation |
| 2026-10-26 | [`48d90f08`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/48d90f08c640b927a543a73d4dd834e5372be9ad) | Review strict acceptance and preserve failing controls |
| 2026-10-27 | [`42f56544`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/42f565443c5714599803e49fd696729bf9f732d6) | docs: publish SVE failure analysis |
| 2026-11-17 | [`415f750a`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/415f750a70f3375fb81916c91ff1f6a05bb4a121) | Publish MATH 4890 dissertation and archive superseded sources |
| 2026-11-17 | [`1dd5c2ea`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/1dd5c2ea424bef5c1475bd126101d337c9c579b1) | Prepare dissertation branch for Gemini review |
| 2026-11-20 | [`f92d4020`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/f92d4020579ec9013511420a9f1be1c060948e93) | Add the compact WKU dissertation PDF and LaTeX source |
| 2026-11-23 | [`717e2ddc`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/717e2ddca3106d70e8b3d1f60189f43271423535) | Clean dissertation delivery paths and confirm compact paper skim |
| 2026-11-23 | [`126a5981`](https://github.com/CarlXerophilem/Lie-ML_PDES/commit/126a5981d74aaa3a504a85ce509ca5c4052666f0) | Implement executable dissertation delivery and verification |
