# 提案：建立角色泳道并精简研发规范

## 意图

当前规范已经按 W0-W9 形成流程主线，但用户从传统研发角色视角进入时仍不够直观：产品、前端、后端、测试、运维、运营、安全合规分别该读什么、输出什么、什么时候参与，还没有显式入口。

这个变更把研发规范整理成两套互补坐标：

- W0-W9 是主线，回答一件工作处于研发生命周期的哪一步。
- 角色泳道是执行视角，回答产品、Tech Lead、后端、前端、测试、运维、运营、安全合规如何参与。

同时用角色泳道反向清理专项规范：保留高频和高风险角色工作，合并重复专项，降级低频专项，避免一人公司和 Agent 被过多主题文档拖住。

## 范围

- 新增角色入口 `docs/03-role-index.md`。
- 新增角色文档：
  - `docs/roles/product.md`
  - `docs/roles/tech-lead.md`
  - `docs/roles/backend.md`
  - `docs/roles/frontend.md`
  - `docs/roles/qa.md`
  - `docs/roles/ops.md`
  - `docs/roles/support-ops.md`
  - `docs/roles/security-compliance.md`
- 更新 README、`docs/00-start-here.md`、`docs/02-standard-index.md`，说明两种读法：按流程读、按角色读。
- 建立多 Agent 使用方案：总控 Agent 先定位 W0-W9，再调度角色 Agent；角色 Agent 只读自己的角色入口和当前 W 相关规范。
- 按角色价值清理专项规范：
  - 保留高频角色入口和高风险门禁。
  - 合并重复专项。
  - 降级低频专项为父级 `00-main.md` 的触发清单。
  - 删除或合入重复入口。
- 更新校验脚本和知识恢复工件，使角色入口、规范索引和精简后的专项数量可维护。

## 不做什么

- 不把流程改成传统瀑布，不采用“产品 -> 前端 -> 后端 -> 测试 -> 运维”的线性流程。
- 不让每个角色 Agent 通读全库。
- 不为低频场景继续新增独立专项。
- 不在本变更中重写所有规范正文；优先做入口、合并、降级和引用关系清理。
- 不建立复杂文档站或权限系统。

## 精简原则

保留专项必须至少满足一项：

- 服务一个高频角色工作，例如前端、后端、测试、发布、运维、AI eval。
- 承接高风险人审点，例如数据边界、安全隐私、生产发布、不可逆迁移、凭据、合同或公开承诺。
- 有独立最小工件和验证门禁，不能被父级 `00-main.md` 轻易覆盖。

优先合并或降级：

- 低频、未来可能才需要的治理主题。
- 与相邻专项高度重叠的模板文档。
- 只提供长清单、但没有独立执行入口的专项。
- 已经被 README、W0-W9 入口、skill 或 OpenSpec 主流程覆盖的重复入口。

## 精简处置摘要

删除或降级的入口不再作为独立触发专项出现；它们的剩余判断被合入对应 W 的主入口或高风险门禁。

- W1 产品发现循环：降级到 `docs/W1-discovery/00-main.md`，指标和实验保留在 `docs/W1-discovery/01-product-analytics-experiment-standard.md`。
- W2 一人公司 operating model：降级到 `docs/00-start-here.md`、`docs/W2-openspec-risk/00-main.md` 和 `docs/03-role-index.md`。
- W2 安全/Auth/供应链：合并为 `docs/W2-openspec-risk/03-security-auth-supply-chain-standard.md`。
- W2 成本/客户数据/供应商/IP/信任：合并为 `docs/W2-openspec-risk/04-cost-data-vendor-trust-boundary-standard.md`。
- W3 eval 数据、红队和内容安全：合并为 `docs/W3-ai-behavior/02-ai-eval-safety-standard.md`。
- W3 记忆、RAG、上下文和本地化触发：合并为 `docs/W3-ai-behavior/03-ai-context-memory-retrieval-standard.md`。
- W3 模型路由和工具运行时：合并为 `docs/W3-ai-behavior/04-ai-runtime-routing-tools-standard.md`。
- W3 模型优化：降级为 `docs/W3-ai-behavior/00-main.md` 的高成本/高风险触发提醒；真实训练或微调另开 OpenSpec change。
- W4 本地开发和 AI 协作编码：合并为 `docs/W4-build/05-dev-workspace-ai-coding-standard.md`。
- W4 billing、webhook/event、notification 和外部开发者副作用：合并为 `docs/W4-build/06-external-side-effects-standard.md`。
- W5 performance 和 resilience：合并为 `docs/W5-verify/03-operational-risk-verification-standard.md`。
- W6 商业合同：降级到 `docs/W6-release/00-main.md` 的对外承诺/合同人审点。
- W7 observability、backup 和 infra：并入 `docs/W7-operate/01-sre-lite-operations-standard.md`。
- W9 审计证据和开源社区维护：降级到 `docs/W9-maintain/00-main.md`，只有真实审计、客户证据包或公开维护义务时另开 change。

## 需要人的判断

- 是否接受 W0-W9 做主线、角色做泳道作为默认使用方式。
- 是否接受专项从约 54 个压缩到 25-30 个左右。
- 哪些低频但战略重要的专项必须保留独立文档。
- 是否接受删除、归档或降级现有专项文档。
