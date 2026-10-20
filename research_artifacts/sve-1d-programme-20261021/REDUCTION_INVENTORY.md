# 已验收一维约化清单

读取 STAGE_1_GATE.json 绑定的8份 derivation.json，校验哈希后得到 17 条 E 约化记录。

| ID | 类型 | 不变量 | 各场最高阶 | 求解状态 |
|---|---|---|---|---|
| grass_generic/traveling | traveling | `-c*t + x` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| grass_generic/scaling-1 | diagonal_scaling | `x/t` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| grass_cubic/traveling | traveling | `-c*t + x` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| grass_cubic/scaling-1 | diagonal_scaling | `x/t` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| grass_cubic/scaling-2 | diagonal_scaling | `x` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_attachment_generic/traveling | traveling | `-c*t + x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_attachment_cubic/traveling | traveling | `-c*t + x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_attachment_cubic/scaling-1 | diagonal_scaling | `t` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_source_generic/traveling | traveling | `-c*t + x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_source_cubic/traveling | traveling | `-c*t + x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_source_cubic/scaling-1 | diagonal_scaling | `x/t**2` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_only/traveling | traveling | `-c*t + x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_only/scaling-1 | diagonal_scaling | `t**((1 - n)/(n - 2))*x` | [1, 1, 2] | 隐式ODE/DAE已验证；一般剖面待求 |
| slope_only/scaling-2 | diagonal_scaling | `t` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| zero_transport/traveling | traveling | `-c*t + x` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| zero_transport/scaling-1 | diagonal_scaling | `x/t` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |
| zero_transport/scaling-2 | diagonal_scaling | `x` | [1, 1, 1] | 隐式ODE/DAE已验证；一般剖面待求 |

登记不等于求解。每条记录的方程、生成元、图重构、最高阶矩阵、定义域和数据限制见 `reduction_registry.json`。
行波的一般正则求积路线及独立E精确解见 `SOLVER_DEMONSTRATION.md`；P/M共同缩放第一积分另列，不能覆盖E记录。
已有8分支点代数与一维子代数分类不自动意味着所有子代数组合都已生成约化；本清单仅覆盖已发出的证书。
历史P的9条来源约化仍需经恢复适配器逐项导入和复核。当前没有宣称全部本地/外部文献的ODE均已收集或求解。
