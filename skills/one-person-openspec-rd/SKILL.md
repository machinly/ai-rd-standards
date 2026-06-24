---
name: one-person-openspec-rd
description: "Route one-person-company AI product R&D through the W0-W9 workflow and OpenSpec. Use when planning, prioritizing, designing, implementing, validating, releasing, operating, learning from, or maintaining solo-company software work, AI-assisted coding, Go/Kratos/sqlc/gRPC/Vite projects, prompt/eval/model/tool changes, SRE-lite operations, documentation standards, or any request that needs minimal human attention and two landing reviews."
---

# One-Person OpenSpec R&D

## Overview

把研发请求先路由到一人公司 AI 研发工作流 W0-W9，再决定是进入 planning、product discovery、OpenSpec、AI eval、实现、验证、发布、运维、学习还是知识维护。保护人的注意力：只有高影响决策才升级给用户，其余按仓库规范、官方文档和 `references/stack-defaults.md` 的技术偏好默认推进。

## Routing Workflow

1. 在当前仓库定位 `README.md`、`docs/00-start-here.md`、`docs/00-standard-index.md` 和 `knowledge/context-packs/rd-standards.md`。如果这些文件不存在，读取 `references/workflow-map.md`。
2. 先判断当前请求处于 W0-W9 哪一步，并用一句话告诉用户，例如：`当前处于 W3 AI Behavior`。
3. 只读取当前 step、上一步输入和下一步门禁对应的规范；不要扫描全部阶段。
4. W0/W1 默认先产出 planning 或 product discovery artifacts；当工作进入 W2 或会影响用户、生产、数据、安全、成本、AI 行为时，创建或更新 OpenSpec change。
5. 对 W2-W7 的生产相关工作，在 `openspec/changes/<kebab-change-id>/` 下创建或更新 `proposal.md`、`design.md`、`tasks.md` 和 `specs/*/spec.md`。
6. 只为高影响决策询问用户：进入 now/expedite、产品方向、数据边界、不可逆迁移、合规/安全风险、显著支出、多日工作量、生产发布、事故升级或架构锁定。
7. 按 `tasks.md` 或当前 workflow artifact checklist 逐项实现，完成一项勾选一项。
8. 每完成一个规范段落、OpenSpec artifact 集合或实现里程碑，用 `references/review-rubric.md` 做两轮 review。
9. 保持下一步明确且小。

## W0-W9 Decision Rules

- W0 Intake：先用 roadmap/intake 判断该不该做；不要直接实现。
- W1 Discovery：先补用户问题、证据、成功指标和 non-goals；证据不足时升级给用户判断。
- W2 OpenSpec / Risk：定义行为、边界、风险、退出条件和 OpenSpec artifacts。
- W3 AI Behavior：任何用户可见 AI 行为变化必须先有最小 eval、失败样例和安全边界。
- W4 Build：按 Go/Kratos/sqlc/gRPC、Vite、migration、config、AI coding batch 落地。
- W5 Verify：代码完成不等于完成；至少有 test/eval/accessibility/performance/resilience 中适用的证据。
- W6 Release：发布前必须有 release checklist、smoke、rollback 和 claim/customer boundary。
- W7 Operate：上线后补 SLO、观测、runbook、事故/恢复或凭据轮换路径。
- W8 Learn：从用户、指标、支持、eval、事故学习，再回到 W0 更新取舍。
- W9 Maintain：文档、依赖、证据、索引和 context pack 问题归到维护，不伪装成新功能。

## OpenSpec Artifact Rules

- `proposal.md`：意图、范围、不做什么、依据、需要人的判断。
- `specs/*/spec.md`：包含 scenario 的 requirements；正文必须包含 OpenSpec 可识别的 `SHALL` 或 `MUST`。
- `design.md`：只写安全实现所需的技术决策，不写长篇泛论。
- `tasks.md`：可独立完成和验证的 checklist。

## Default Stack

当请求涉及后端、前端、数据库、API contract、观测、UI 设计或 AI 行为时，读取 `references/stack-defaults.md`。版本敏感内容以官方文档为准。

## Workflow References

- 如果仓库有 `docs/00-start-here.md` 和 `docs/00-standard-index.md`，优先使用仓库版本。
- 如果仓库缺少 workflow 文档，读取 `references/workflow-map.md` 作为默认路由表。
- 如果新增、删除或重命名编号规范，运行 `python tools\verify_workflow_index.py .`，若仓库没有该脚本则在 OpenSpec tasks 中记录跳过原因。

## Review Discipline

每个规范段落交付前读取 `references/review-rubric.md`，并输出两轮 review：

- Review A：一人可执行性。
- Review B：产品、工程和运维风险。

每轮 review 都要短、具体、面向行动。当前段落可 review 且下一步明确后，再进入下一阶段。

## AI Feature Rule

对用户可见 AI 行为，在改变 prompt、模型设置、工具 workflow 或自主行为前，必须先有最小 eval。生产 prompt builder 必须进入代码或配置，并在 change 中包含代表样例、边界样例和失败样例。

## Output Shape

优先写入持久文件，而不是在聊天里堆长文。最终总结要包含变更文件、未决人工判断、验证结果和推荐的下一个 OpenSpec change。
