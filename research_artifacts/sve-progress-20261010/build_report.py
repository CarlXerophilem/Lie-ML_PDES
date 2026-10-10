"""Build a concise evidence report from completed runs without rerunning them."""
import json
import statistics as st
from pathlib import Path

def main():
    root=Path(__file__).parent
    out=root/'results'
    classical=json.loads((out/'classical_results.json').read_text())['cases']
    experiment=json.loads((out/'experiment_results.json').read_text())['cases']
    methods=['hard_ivp_tanh','taylor4_tanh','hard_ivp_chebyshev','direct_2d_tanh']
    texts=[
      '# 2026-10-10：实际完成结果与疑点处理\n',
      '主要结论：X5 的一阶点生成元延续确实受阻；一般 m 的共同缩放约化仍可精确推进。'
      '床面对流项可在明确变量定义下修正，约化方程还有显式一阶积分。\n',
      '## 疑点处理状态\n',
      '| 疑点 | 本次结果 | 结论范围 |',
      '|---|---|---|',
      '| 是否只是对角缩放类失败？ | 已获得任意光滑点系数的一阶障碍 | 两种明确标量模型；非最大分类 |',
      '| 一般 m 是否还能约化？ | 可以，共同缩放给出 ODE 与一阶积分 | 仅选定不变图与兼容数据 |',
      '| 缺少床面对流项怎么办？ | 从 Eulerian 系统重新推导，得到修正标量方程 | 正深度、光滑、速度幂律闭合 |',
      '| 床面如何重构？ | B_profile(z)+(I0/g)log(t) | 局部单连通域与匹配床面数据 |',
      '| 整个参考区间是否正则？ | 有精确有理数 bootstrap 证明 | 固定构造数据，连续 m∈[1,4] |',
      '| 学习候选是否全区间已认证？ | 尚未；独立网格检查分支和 leading margin | 不把采样当成区间定理 |',
      '| 神经网络是否必需或更快？ | 当前证据不支持；经典控制精度最好 | 此次小规模固定特征实验 |\n',
      '## 数学与经典验证\n',
      '- 38 项验证通过：任意点延拓、缺陷符号、独立链式代入、'
      '物理相容性、一阶积分、二阶/三阶求解一致性和数据硬约束。',
      '- 12 个经典参考算例：两种模型 × m=1,2,2.9,3,3.1,4。',
      f"- 二阶与三阶求解最大数值差：{max(r['two_vs_three_order_error'] for r in classical):.3e}。",
      f"- 床面时间方程最大数值缺陷：{max(r['bed_time_equation_error'] for r in classical):.3e}。",
      f"- 一阶积分最大数值漂移：{max(r['first_integral_drift'] for r in classical):.3e}。",
      '- 上述差值表示交叉验证的一致性，不能解释为绝对解误差的严格上界。\n',
      '## 40 次近似比较\n',
      '参数 m=2.9,3.1；两种模型。tanh 方法用种子 17,23,41，'
      'Chebyshev 方法确定性运行。每次 12 个可训练输出权重、64 个配点、'
      '150 次函数评价预算上限，权重界 [-10,10]。',
      '初值 (F,F′,F″)(1)=(2,0.5,0.1)，g=1，κ=1/30，'
      'z∈[1,1.4]，t∈[1,2]。参考解没有参与训练。最终验证使用新的 25×161 网格。\n',
      '| 模型 | 方法 | 次数 | max U 参考误差中位数 | 原坐标残差 L² 中位数 | 拟合秒数中位数 | 预算耗尽 |',
      '|---|---|---:|---:|---:|---:|---:|'
    ]
    groups=[]
    for model in ['printed','physical_corrected']:
      for method in methods:
        rows=[r for r in experiment if r['model']==model and r['method']==method]
        med=lambda key:st.median(r[key] for r in rows)
        failed=sum(not r['optimizer_success'] for r in rows)
        texts.append(f"| {model} | {method} | {len(rows)} | {med('max_U_error'):.3e} | "
                     f"{med('original_residual_L2'):.3e} | {med('training_seconds'):.3f} | {failed} |")
        groups.append((model,method,rows))
    texts.extend([
      '\n16/40 次达到预算上限，没有被改写为“优化收敛”。所有冻结候选都保留了权重、'
      '特征、先验、独立网格值和原坐标残差。残差经过新网格求积，但不是严格连续范数界。',
      '\n四阶先验在这些匹配运行中降低了原坐标残差，训练时间没有因此普遍减少；'
      '一些 profile 参考误差已接近浮点/参考精度，不能夸大其细微排序。',
      '\nChebyshev 控制在本次精度比较中最好。直接二维 tanh 候选更快停止，精度更低；'
      '这是固定小特征类和所选不变目标的结果，不能推断普遍的二维 PINN 劣势。',
      '\n![Residual and cost comparison](../results/experiment-summary.png)\n',
      '## 仍然未建立的命题\n',
      '- 接触、广义、非局部或依赖床面额外场的完整系统对称分类。',
      '- 任意真实渠段初边值/通量条件下的共同缩放不变解覆盖。',
      '- 学习候选的区间一致误差证书、深度 PINN 优越性或样本复杂度定理。',
      '- 超出当前正则管的全局延拓、冲击波/弱解及其他输沙闭合。',
      '\n这些是明确的结论边界，当前的障碍证明、一般 m 约化和物理修正不依赖它们完成。',
      '\n完整证明见 [THEORY.md](THEORY.md)，复现入口见 [README.md](../README.md)。'
    ])
    (root/'docs'/'FINDINGS.md').write_text('\n'.join(texts)+'\n',encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({'font.size':10})
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
    for n,key in enumerate(['original_residual_L2','training_seconds']):
      ax=axes[n]
      for mi,model in enumerate(['printed','physical_corrected']):
        selected=[item for item in groups if item[0]==model]
        xpos=np.arange(4)+(mi-.5)*.32
        medians=[st.median(r[key] for r in rows) for _,_,rows in selected]
        ax.bar(xpos,medians,.3,label=model,color=['#245a81','#bf7b36'][mi])
        for pos,(_,_,rows) in zip(xpos,selected):
          ax.scatter([pos]*len(rows),[r[key] for r in rows],s=10,color='#222',alpha=.5)
      ax.set_xticks(np.arange(4),['Hard IVP\ntanh','Taylor-4\ntanh','Chebyshev','Direct 2D\ntanh'])
      ax.set_yscale('log');ax.grid(axis='y',alpha=.2)
      ax.set_ylabel('Original-coordinate residual L2' if n==0 else 'Fit wall time (seconds)')
      ax.set_title('Independent residual evidence' if n==0 else 'Measured cost; no equal-time claim')
    axes[0].legend()
    fig.suptitle('Constructed smooth data, m = 2.9 / 3.1; bars: medians, dots: individual runs')
    fig.savefig(out/'experiment-summary.png',dpi=170)
    plt.close(fig)

if __name__=='__main__':main()
