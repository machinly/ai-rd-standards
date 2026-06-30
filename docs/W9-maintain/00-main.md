# W9 Maintain 核心规范

## W9 核心入口

本文件是 W9 Maintain 的核心入口。进入 `docs/W9-maintain/` 时先读它，再按触发条件读取知识恢复、维护债务、审计证据或开源维护专项。

W9 只回答一个问题：**这套产品、系统、证据和文档在下一次被你或 Codex 接手时，是否还能被理解、验证、维护、审计和安全演进？**

W9 不是继续做新功能，也不是把所有遗留问题堆成 backlog。它负责把 W0-W8 的结果沉淀成可恢复上下文、可维护依赖、可信证据和可持续对外维护边界。

## 适用范围

适用：

- docs map、context pack、glossary、how-to、freshness log、canonical entrypoint 和上下文恢复。
- 依赖 inventory、update policy、upgrade plan、debt register、deprecation plan 和长期维护节奏。
- audit evidence、audit log policy、retention、evidence package、customer/auditor evidence 和 evidence review。
- 开源仓库、SDK、CLI、template、MCP server、example、community health、contribution policy、security advisory 和 maintainer boundary。
- release、incident、AI 行为、安全/隐私、客户上线、合同、支持、运营和数据变更后的长期证据与知识收尾。

不适用：

- 新工作优先级，回到 `docs/W0-intake/00-main.md`。
- 产品学习、支持反馈或 AI 质量回归，回到 `docs/W8-learn/00-main.md`。
- 运行事故、凭据、恢复和生产操作，回到 `docs/W7-operate/00-main.md`。
- 发布、客户上线、对外声明和合同承诺，回到 `docs/W6-release/00-main.md`。
- 实现、验证或 AI 行为设计，回到 W4/W5/W3。

## W9 最小产出

每个 W9 工作至少留下这些产出：

- 更新后的 canonical 入口：README、`docs/00-start-here.md`、`docs/02-standard-index.md`、docs map 或 context pack 中适用项。
- 可恢复上下文：目标、当前 product bet、系统形状、关键命令、边界、风险、开放决策和 handoff prompt。
- 维护事实：关键依赖、升级策略、技术债利息、弃用计划、下次复审日期。
- 证据索引：release、incident、AI 行为、安全隐私、admin action、audit log、evidence package 的引用和留存策略。
- 对外维护边界：开源支持范围、贡献入口、安全报告路径、release/security review、归档或暂停条件。

## 人工判断点

默认不问：

- 低风险链接修正、字段顺序、typo、普通 freshness log、没有行为影响的 README 小修。

必须人工判断：

- 哪个文档或工件是 canonical source。
- 是否删除、归档、降级、改名或公开文档/证据/开源仓库。
- 是否接受过期文档、缺少证据、缺少 audit log、缺少 freshness、缺少 context pack 或维护债继续延期。
- 是否对客户、审计方、监管方、律师、供应商或公众导出证据包。
- 是否改变许可证、开源支持边界、security fix window、贡献权利、公开 roadmap、SDK/API 兼容性或维护期限。
- 是否升级 runtime/framework/provider major version、接受可达漏洞例外、删除弃用接口或改变 AI 行为契约。

## 触发型专项

只在触发条件出现时读取对应文件：

- 文档入口、context pack、docs map、glossary、how-to、freshness、Codex handoff：`docs/W9-maintain/01-knowledge-context-recovery-standard.md`
- 依赖升级、技术债、弃用、runtime/framework/AI SDK 维护、Dependabot、deprecation：`docs/W9-maintain/02-maintenance-dependency-debt-standard.md`

低频治理默认降级到本文件的触发提醒：

- 审计证据、证据包、audit log、retention、customer/security evidence、SOC 2 readiness：先在 W9 最小产出的证据索引中登记；真实客户/审计导出时单独开 OpenSpec change。
- 开源仓库、SDK/CLI/template、community health、贡献策略、security advisory、公开维护边界：先在 W9 维护事实和对外维护边界中登记；公开仓库或官方 SDK 发布时单独开 OpenSpec change。

常见跨 W 触发：

- 维护项变成新产品工作：回到 W0。
- 文档发现产品语言或成功指标漂移：回到 W1。
- 证据缺口暴露安全/隐私/合同/供应商边界问题：回到 W2。
- AI 行为证据或 eval 不足：回到 W3。
- 依赖升级需要实现或验证：回到 W4/W5。
- 对外证据包或开源 release 变成公开承诺：回到 W6。
- 证据来自事故、凭据、恢复或生产操作：回到 W7。
- 支持/质量信号需要沉淀：回到 W8 后再收尾。

## W9 出口

W9 完成时必须能回答：

- 下次从哪里开始读？
- 哪些文档是 canonical，哪些只是历史？
- 哪些依赖、债务、证据或开源承诺需要下一次复审？
- 哪些风险必须回到 W0-W8 继续处理？

出口选择：

- `archive`：归档或降级历史内容。
- `refresh`：更新 context pack、docs map、freshness 和索引。
- `maintain`：登记依赖、债务、弃用或开源维护项。
- `evidence`：形成证据包或 audit review。
- `new-work`：回到 W0 创建下一项工作。

## W9 完成检查

- 当前 W9 目录只有一个 `00-main.md` 作为核心入口。
- 所有其它 W9 文件都是触发型专项，并在开头说明不是主入口。
- 入口、索引和 source map 都指向 `docs/W9-maintain/00-main.md` 与带目录内顺序编号前缀的语义化专项文件名。
- 没有未编号专项文件、`core-*` wrapper 或只用旧“阶段 NN”作主身份的正文。
- `python tools\verify_workflow_index.py .` 通过。
