"""Build an evidence-linked delivery summary and hash manifest after Stage 3."""
import datetime
import hashlib
import json
from pathlib import Path
import re

from gatekeeper import check_gate
from stage3_gate import check

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_release():
    if (HERE/'RELEASE_MANIFEST.json').exists():
        raise ValueError('Preserve the existing release manifest; use a reviewed revision')
    gates={'1':check_gate(1),'2':check_gate(2),'3':check()}
    if not all(gate['passed'] for gate in gates.values()):
        raise ValueError(gates)
    run=json.loads((HERE/'runs/stage3-candidates-final/receipts.json').read_text(encoding='utf-8'))
    validation=json.loads((HERE/'runs/stage3-validation/receipts.json').read_text(encoding='utf-8'))
    counts=run['conditional_status_counts']
    tests={}
    for row in validation['receipts']:
        if row['name'] in ('new-cycle','engine-chart','active-package'):
            found=re.search(r'(\d+) passed',Path(row['log']).read_text(encoding='utf-8'))
            if not found:
                raise ValueError('No pytest completion in '+row['name'])
            tests[row['name']]=int(found.group(1))
    review=json.loads((HERE/'nonclassical_review.json').read_text(encoding='utf-8'))
    elapsed=sum(row['elapsed_seconds'] for row in run['receipts'])
    summary=f'''# SVE general-symm：本周期交付

三个阶段的当前证据门槛均已闭合。入口是 [README.md](README.md)，通用方程接口在
[general_sve.py](general_sve.py)。生成元从任意系数确定方程的通解中提取；已知论文基
只作独立回归。历史源码、冻结证据、论文正文与文献库保持不变。

## 1. 分类、约化和数据

| 阶段 | 实际交付 | 有效范围与门槛 |
|---|---|---|
| 一维 | 8个符号类族、8个子脚本、必要性与充分性证明、可逆等价映射、括号／伴随、约化与数据实验 | h>0,abs(u)>0；[STAGE_1_GATE.json](STAGE_1_GATE.json) |
| 二维 | 17个符号类族、17个子脚本，覆盖两种坡度律及 f=0／f≠0 | h>0,u²+v²>0；[STAGE_2_GATE.json](STAGE_2_GATE.json) |
| 非经典与输入 | 64个预先冻结仿射分布逐项评价，原PDE／Q／微分后果／奇异层／重构及输入证书 | G=f=0,m=3；[STAGE_3_GATE.json](STAGE_3_GATE.json) |

一维的一维子代数已在声明的连通内伴随作用及直线重标度下分类。
二维交付经验证的子代数代表及实际伴随作用，**尚未证明最优系统完整性**。
最大点代数分类与这一单独问题不互相替代。完整点等价群胚亦未宣称解决。

## 2. 64个候选的结论

| 判据状态 | 数量 |
|---|---:|
| 完整声明域上的所有相容联合射流通过 | {counts['verified_conditional_on_declared_chart']} |
| 只在附加 u≠0 子域通过 | {counts['verified_conditional_on_regular_subchart']} |
| 条件不变性判据失败，有明确反例 | {counts['failed_conditional_criterion']} |

其中9个是经典平移／床高平移分布。其余通过的4个分布包含正负深度平移和速度平移。
这4个分布在环境开集上不等价于固定经典秩二子代数；但积分得到的全部相应局部解族
均被另一种经典约化覆盖。因此，**本次64候选没有给出新增的经典约化之外的解族**。
这是有限搜索结果，不是非经典对称不存在定理。

例如深度平移 β=±1 产生

    h=H0+β(t-x/u0), u=u0≠0, v=v0, B=B0+βx/u0.

它同时是经典分布 span{{∂y,∂t+u0∂x+β∂B}} 的不变解。
速度平移产生

    h=H0, u=U0+βt, v=V0, B=B0-βx/g.

它属于经典分布 span{{∂y,∂x-(β/g)∂B}} 的不变解。
速度平移候选在 u=0,v≠0 的相容射流上违反条件判据，因此输入证书保留 u≠0 掩码。
具体证明见 [NONCLASSICAL_DERIVATION.md](NONCLASSICAL_DERIVATION.md)、
[NONCLASSICAL_EQUIVALENCE.md](NONCLASSICAL_EQUIVALENCE.md) 和
[NONCLASSICAL_REVIEW.md](NONCLASSICAL_REVIEW.md)。

## 3. 输入与重构

每个候选目录包含 `candidate.json` 和 `ml_certificate.json`。后者记录不变量坐标、
剖面未知量、精确重构、时间系数DAE、定义域掩码、初值／边界通量条件及证据哈希。
失效候选只能作为诊断图使用。数据入口用 `encode_certificate` 自动执行附加域限制。
详见 [ML_INPUTS.md](ML_INPUTS.md)。没有训练，也没有学习误差或算法优越性结论。

## 4. 本轮执行与检查

- 非经典集合：64/64子进程正常完成，源码在批处理中未变化；累计子进程时间 {elapsed:.2f} 秒。
- 本周期测试：{tests['new-cycle']}项通过；engine/chart：{tests['engine-chart']}项通过；活动证据包：{tests['active-package']}项通过。
- data-flux、workflow通过；受保护历史输入未变化。
- 项目 audit **仍失败**：234项既有问题与原基线逐项一致。未将该失败改写为通过。
- 独立评审源代码与原始回执、候选证书、发布门槛互相绑定；失败探索和修复记录保留。

原始记录见 [非经典执行回执](runs/stage3-candidates-final/receipts.json)、
[本轮验证回执](runs/stage3-validation/receipts.json) 和
[独立评审回执](nonclassical_review.json)。文件清单为 `RELEASE_MANIFEST.json`。

## 5. 原稿与来源边界

2022年全耦合Eulerian父模型、2026年打印标量P、校正标量M和物质坐标重构分别保留来源及测试。
本轮是自主推导与验证，不把更正公式或构造数据伪称论文原结果，也不主张文献首创。
文献来源台账仍位于 `../sve-systematic-20261020/sources/ledger.json`。
本交付没有改写正文或扩展到冲击、干湿界面、任意IBVP和全局解。
'''
    (HERE/'DELIVERY.md').write_text(summary,encoding='utf-8')
    ledger_path=HERE/'ledger.json'
    ledger=json.loads(ledger_path.read_text(encoding='utf-8'))
    ledger['status']='complete_with_explicit_scope_qualifications'
    ledger['stages']['nonclassical_ml']='reviewed_executed_released'
    ledger['next']='Authorized implementation complete; unproved 2D optimality and full equivalence groupoid remain explicitly outside the accepted claim set.'
    ledger['stage3_gate']='STAGE_3_GATE.json'
    for task in ledger.get('stage3_tasks',[]):
        task['state']='accepted'
        task['release_evidence']='STAGE_3_GATE.json'
    ledger['stage3_validation']={'candidate_count':64,'conditional_status_counts':counts,
        'new_cycle_pytest':tests['new-cycle'],'engine_chart_pytest':tests['engine-chart'],
        'active_package_pytest':tests['active-package'],'data_flux':'passed','workflow':'passed',
        'project_audit':'failed:234 unchanged preexisting issues','protected_inputs':'all unchanged',
        'independent_review':'accepted','training_performed':False}
    ledger['claims'] += [
        {'id':'2D-MAX','status':'accepted_exact_version','scope':'17 declared regular point-algebra cells',
         'receipt':'classification_2d_review.json'},
        {'id':'FINITE64','status':'accepted_exact_version','scope':'64 frozen proposals; global/subchart/failed verdicts distinct',
         'receipt':'nonclassical_review.json'},
        {'id':'ML-INPUT','status':'accepted_exact_version','scope':'Input, domain and reconstruction certificates; no training',
         'receipt':'nonclassical_review.json'}]
    ledger['receipts'] += ['classification_2d_review.json','nonclassical_review.json',
                           'runs/stage3-candidates-final/receipts.json','runs/stage3-validation/receipts.json']
    ledger_path.write_text(json.dumps(ledger,indent=2,ensure_ascii=False),encoding='utf-8')
    excluded={'RELEASE_MANIFEST.json'}
    paths=[p for p in HERE.rglob('*') if p.is_file() and p.name not in excluded
           and p.suffix!='.pyc' and '__pycache__' not in p.parts
           and not any(part.startswith('tmp-') for part in p.relative_to(HERE).parts)]
    provenance=ROOT/'build/sve-systematic-20261020/sources/ledger.json'
    manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'scope':'user-approved general-symm SVE build cycle',
              'stage_gates':gates,'accepted_claims':['1D-MAX','1D-SUBALGEBRAS','2D-MAX','FINITE64','ML-INPUT'],
              'qualified_claims':['234 unchanged failed audit issues','two conditional candidates require u!=0'],
              'unproved':['2D optimal subalgebra classification','full equation-equivalence groupoid',
                          'complete nonclassical classification','global solutions','arbitrary IBVP','ML advantage'],
              'source_ledger':{'path':str(provenance),'sha256':digest(provenance)},
              'file_count':len(paths),'files':{str(p.relative_to(HERE)):digest(p) for p in sorted(paths)},
              'omitted_from_inventory':['__pycache__','pytest tmp-* working directories','manifest itself']}
    (HERE/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    changed=[name for name,sha in manifest['files'].items() if digest(HERE/name)!=sha]
    if changed or not check()['passed']:
        raise ValueError({'manifest_changed':changed,'stage3':check()})
    return {'released':True,'manifest_files':len(paths),'tests':tests,'gates':gates}


if __name__=='__main__':
    print(json.dumps(make_release(),indent=2))
