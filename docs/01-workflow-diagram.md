# W0-W9 运转图

这张图说明 W0-W9 不是文档分类，也不是线性瀑布。它更像一套一人公司 AI 研发调度图：W0-W2 决定做什么和边界是什么；W3-W7 可以围绕同一个 OpenSpec change 并行推进；W8/W9 持续把线上信号和上下文回流到下一轮选择。

## 总览

```mermaid
flowchart TB
  signal["请求 / 客户信号 / 事故 / 想法"] --> W0

  W0["W0 Intake<br/>现在该不该做？<br/>work-intake / decision-board"]
  W1["W1 Discovery<br/>要解决的是真问题吗？<br/>product bet / metrics / evidence"]
  W2["W2 OpenSpec / Risk<br/>行为、边界、风险是什么？<br/>proposal / spec / design / tasks"]
  W8["W8 Learn<br/>学到了什么，下一步做什么？<br/>learning decision / quality review"]
  W9["W9 Maintain<br/>下次还能接起来吗？<br/>context pack / docs map / evidence"]
  done["可恢复状态 / 完成<br/>下次能从 artifact 接上"]

  subgraph parallel["并行推进区：同一个 change 下可以重叠执行"]
    direction LR
    W3["W3 AI Behavior<br/>AI 怎样算好、坏、危险？<br/>eval / prompt / route / red-team"]
    W4["W4 Build<br/>如何落到系统？<br/>code / migration / config / batch log"]
    W5["W5 Verify<br/>上线前证据够吗？<br/>test / eval / risk review"]
    W6["W6 Release<br/>能发布、能回滚、能承诺吗？<br/>release checklist / rollback"]
    W7["W7 Operate<br/>线上怎么观察和恢复？<br/>SLO / dashboard / incident / restore"]
  end

  W0 -- "证据不足 / 问题不清" --> W1
  W0 -- "值得做 / 需要边界" --> W2
  W0 -- "只是维护或上下文恢复" --> W9
  W1 -- "产品证据补足" --> W2
  W2 -- "AI 行为" --> W3
  W2 -- "系统实现" --> W4
  W2 -- "验证计划" --> W5
  W2 -. "发布准备可提前" .-> W6
  W2 -. "运行准备可提前" .-> W7

  W3 <-- "prompt、eval、fallback 影响实现" --> W4
  W3 -- "AI 质量证据" --> W5
  W4 -- "实现证据" --> W5
  W5 -- "门禁通过才发布" --> W6
  W6 -- "发布后进入运行" --> W7
  W7 -- "运行信号出现" --> W8

  W5 -- "证据不足 / 风险暴露" --> W2
  W5 -- "AI 行为缺口" --> W3
  W5 -- "实现缺口" --> W4
  W8 -- "取舍变化 / 停车" --> W0
  W8 -- "问题定义变化" --> W1
  W8 -- "边界或风险变化" --> W2
  W8 -- "AI 行为或 eval 缺口" --> W3
  W8 -- "实现修复" --> W4
  W8 -- "验证缺口" --> W5
  W8 -- "回滚 / 声明 / 客户沟通" --> W6
  W8 -- "事故 / 恢复 / 凭据" --> W7
  W8 -- "需要沉淀上下文" --> W9
  W9 -- "新工作、债务、风险" --> W0
  W9 -- "入口、索引、证据刷新" --> done

  human["人工只判断高影响点<br/>now / expedite / 数据边界 / 安全例外 / 发布 / 回滚 / canonical 入口"]
  human -.-> W0
  human -.-> W1
  human -.-> W2
  human -.-> W3
  human -.-> W5
  human -.-> W6
  human -.-> W7
  human -.-> W9
```

## 单个 W 的内部节奏

单个 W 也不是“做完才允许看下一步”。实际做法是：先判断这个 W 的核心问题，留下能恢复上下文的最小工件；如果相邻 W 的工作已经清楚，就可以并行推进，但关键门禁不能跳过。

```mermaid
flowchart TD
  input["上一步输入"] --> read["只读当前 W 主规范<br/>必要时读触发专项"]
  read --> question["回答这个 W 的一个核心问题"]
  question --> artifact["留下最小 artifact"]
  artifact --> gate{"是否触发人工判断？"}
  gate -- "否" --> default["Codex 按规范默认推进"]
  gate -- "是" --> human["用户做高影响决策"]
  default --> next["进入下一步门禁"]
  human --> next
  next --> route{"出口"}
  route -- "前进" --> forward["下一个 W"]
  route -- "证据或风险不足" --> back["回到更早的 W"]
  route -- "不值得继续" --> stop["停车 / 杀掉 / 归档"]
  route -- "需要沉淀" --> maintain["W9 维护上下文"]
```

## 每个 W 的职责

| W | 核心问题 | 最小产出 | 常见出口 |
| --- | --- | --- | --- |
| W0 Intake | 现在该不该做？ | work-intake、decision-board | W1、W2、W9、停车 |
| W1 Discovery | 要解决的是真问题吗？ | product bet、metrics、feedback evidence | W2、W0 |
| W2 OpenSpec / Risk | 行为、边界、风险是什么？ | proposal、spec、design、tasks | W3、W4、W0 |
| W3 AI Behavior | AI 怎样算好、坏、危险？ | eval、prompt、route、red-team、fallback | W4、W2 |
| W4 Build | 如何落到系统？ | code、migration、config、batch log | W5 |
| W5 Verify | 上线前证据够吗？ | test/eval run、risk review、rollback plan | W6、W2/W3/W4 |
| W6 Release | 能发布、能回滚、能承诺吗？ | release checklist、smoke、rollback、claim evidence | W7 |
| W7 Operate | 线上怎么观察和恢复？ | SLO、dashboard、alert、incident、restore | W8 |
| W8 Learn | 学到了什么，下一步做什么？ | learning decision、quality review、support feedback | W0-W7、W9 |
| W9 Maintain | 下次还能接起来吗？ | docs map、context pack、freshness、evidence、debt review | 完成或 W0-W8 |

## 顺畅性核对

- 入口顺：任何请求先落到 W0；证据不清走 W1，值得推进且有边界风险走 W2，纯维护走 W9。
- 边界顺：W2 是并行区的调度口，不是实现阶段；它把同一个 change 拆给 W3/W4/W5/W6/W7。
- 并行顺：W3/W4/W5 可互相修正；W6/W7 可提前准备，但 W5 没过不能真实发布。
- 回流顺：W8 是学习路由器，能回 W0-W7 的任一步；不是只能回产品或 AI。
- 收口顺：W9 把上下文、证据和索引沉淀成可恢复状态；只有发现新工作、风险或证据缺口时才回到 W0-W8。
- 人审顺：人只卡高影响判断；普通字段、链接、索引、验证和低风险实现由 Codex 与 verifier 推进。

## 并行规则

- W0/W1/W2 是路由和边界层，通常先启动；没有它们，后面的并行会变成散工。
- W3、W4、W5 经常并行：AI 行为设计、实现、测试/eval 会互相修正。
- W6、W7 可以提前准备 release checklist、rollback、SLO、dashboard、runbook，但真实发布要等 W5 门禁。
- W8、W9 不是最后一步才做；运行信号、质量回归、文档和证据可以随时把工作带回 W0-W7。
- 并行不等于跳门禁；每个 W 仍要留下自己的最小 artifact。

## 使用口诀

```text
先定位 W，再只读当前 W；
能并行就并行，但门禁不能省；
先留最小工件，再过关键门禁；
代码完成不算完成，至少走到 W5；
上线后还要 W7/W8，沉淀后才到 W9；
学到新东西，回到 W0 重新选择。
```
