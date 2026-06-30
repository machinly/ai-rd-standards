# W2 触发专项：成本、客户数据、供应商、IP 与信任边界规范

## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项，不是 W2 主入口。只有当当前 change 涉及成本容量、客户数据导入/导出/删除、供应商处理方、数据出境、IP/license、AI 生成内容、隐私/条款/AI disclosure 或公开承诺时，才读取本文件。

普通 W2 工作先回到 `docs/W2-openspec-risk/00-main.md`。

## 目标

把原先分散的成本、客户数据、供应商、IP 和信任政策专项合并成一个边界判断：这次工作会不会让一人公司在钱、数据、外部供应商、权利来源或用户承诺上背上不可承受的义务。

默认原则：成本要有硬限制，客户数据要有生命周期，供应商处理要有证据，外部材料要有来源，承诺要能连接实现或证据。

## 主要角色消费者

- Tech Lead：在 W2 判断变更边界和退出条件。
- 产品/运营：确认 pricing、claim、客户数据和用户权利承诺。
- 安全合规：判断供应商、数据出境、IP 和 trust claim。
- 后端/运维：实现 quota、删除、导出、同步、降级和审计。

## 最小工件

按真实触发选择最小集合：

```text
cost/
  budgets/<target>.json
  vendors/<target>.md
  runbooks/<target>.md

customer-data/
  data-map/<target>.json
  transfer-contract/<target>.json
  rights-deletion-policy/<target>.json

vendor-risk/
  processor-register/<target>.json
  dpa-checklist/<target>.json
  transfer-impact/<target>.json

ip-rights/
  source-register/<target>.json
  license-policy/<target>.json
  notice-attribution/<target>.md

trust/
  commitment-register/<target>.json
  ai-disclosure/<target>.md
  data-rights/<target>.md
```

## 必须覆盖

- AI token、请求、工具循环、batch、导出、重试和供应商调用必须有上限。
- 客户数据必须有 system of record、导入/导出格式、删除传播、备份例外和第三方传播说明。
- 新供应商必须记录 role、purpose、data classes、DPA/terms、retention、region、training/use 政策和删除协助。
- 外部代码、素材、dataset、eval、RAG source、AI output 和客户内容复用必须有来源、license/rights basis、NOTICE/attribution。
- 对外 claim 必须有 evidence ref；没有证据的强承诺只能是 draft。

## 默认实现规则

- `cost/budgets` 至少包含 50%、80%、100% 阈值、hard cap 和 degradation。
- 删除/导出/同步默认异步 job，有 dry-run、幂等、audit、状态和例外解释。
- 供应商调用收口到 client boundary，有 timeout、retry budget、disable switch 和数据最小化。
- license gate 失败时替换、授权或人审接受风险，不通过删除 license 文件解决。
- AI disclosure 不把供应商能力当成产品已验证能力。

## 需要人判断

- 上调预算、取消 hard cap、允许无限 agent loop 或高成本真实供应商运行。
- 新增客户数据类别、敏感数据、跨租户/跨产品数据流、批量删除、删除例外或跨境处理。
- 接受没有 DPA/等价条款、删除协助、事故通知、子处理方透明度或训练/保留边界的供应商。
- 引入 GPL/AGPL/未知许可证、无授权素材、客户内容复用、AI-only 强版权声明。
- 发布隐私、条款、AI disclosure、安全、退款、合规、SLA、数据驻留、不训练、不保存等强承诺。

## Review A：一人可执行性

本专项用一个 W2 入口承接原先五类低频但高风险治理主题。每次只按触发条件补最小工件，避免角色 Agent 被多份长清单拖住。

## Review B：产品 / 工程 / 运维风险

保留了钱、数据、供应商、权利来源和信任承诺这些不可逆风险的人工门禁。最小安全下一步是让任何对外 claim、供应商数据流或高成本 AI workflow 都有证据链接和降级路径。

