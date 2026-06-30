# 一人公司 AI 研发规范

这个仓库不是给人从头读完的。它是一套“一人公司 + AI 助手”的研发操作台：每次只选择当前任务需要的少数规范、一个 OpenSpec change、一个对应 skill，然后落地和验证。

## 先看哪里

1. 按流程读：先看 `docs/00-start-here.md`，它按 W0-W9 AI 研发工作流组织。
2. 按角色读：看 `docs/03-role-index.md`，它把产品、Tech Lead、后端、前端、测试、运维、运营、安全合规映射到 W0-W9。
3. 想找完整映射：看 `docs/02-standard-index.md`，它把主规范和触发专项挂到 workflow step。
4. 让 Codex 接手：先给它 `knowledge/context-packs/rd-standards.md`。
5. 查来源依据：看 `docs/sources/2026-06-23-source-map.md`。

## 当前默认路径

每个超过 30 分钟、影响用户、生产、数据、安全、成本或 AI 行为的工作，都先进入 OpenSpec：

```text
openspec/changes/<change-id>/
  proposal.md
  design.md
  tasks.md
  specs/*/spec.md
```

然后先定位当前处于 AI 研发工作流的哪一步，再选择需要的角色泳道，只读取该 step、相邻门禁和命中的角色入口。不要一次阅读全部规范。

```text
按流程读：
README -> docs/00-start-here.md -> 当前 W -> 触发专项

按角色读：
README -> docs/03-role-index.md -> 角色入口 -> 当前 W 相关规范
```

## 人只判断这些

- 当前是否值得进入 `now` / `expedite`。
- 是否改变产品方向、目标用户、定价或数据边界。
- 是否接受无证据、无 eval、无 rollback 的高影响实现。
- 是否执行不可逆迁移、生产回滚、公开承诺、合同/SLA 承诺。
- 是否引入长期供应商、架构锁定或显著成本。
- 是否接受安全、隐私、合规、凭据、客户数据相关例外。
- 是否删除、归档或更换 canonical 文档入口。

其余字段补齐、索引、链接、检查脚本、默认技术选型和低风险实现细节，交给 Codex 按规范处理。

## 默认技术偏好

- 后端：Go、go-kratos、sqlc、gRPC/Protobuf。
- 前端：Vite。
- UI 参考：Vercel `design.md` / `design.dark.md`。
- 规格流：OpenSpec。
- 研发节奏：一个 active change、两轮一人公司 review、落地后验证。

## 常用命令

```powershell
openspec validate --all
python tools\verify_workflow_index.py .
python C:\Users\machinly\.codex\skills\knowledge-context-recovery-guard\scripts\verify_knowledge_context.py .
```

## Codex skills

本仓库已沉淀大量 skills，不需要人工记忆全部名字。按 AI 研发工作流触发即可；完整映射见 `docs/02-standard-index.md`。

仓库内维护的 skill 本体放在 `skills/`。其中 `skills/one-person-openspec-rd/` 是本仓库 AI 研发工作流的 canonical skill；个人环境里的 `C:\Users\machinly\.codex\skills\one-person-openspec-rd\` 只作为本机可发现副本，更新时应以仓库版本为准。

最常用入口：

- `one-person-openspec-rd`：先把研发请求路由到 W0-W9，再创建需要的 OpenSpec 或 workflow artifacts，并执行两轮一人公司 review。
- `roadmap-prioritization-guard`：决定当前做什么、停什么、延后什么。
- `knowledge-context-recovery-guard`：维护文档入口、上下文包和索引。
- `go-kratos-sqlc-service`：Go/Kratos/sqlc/gRPC 服务实现与检查。
- `vite-geist-frontend`：Vite + Geist 风格前端实现与检查。
- `ai-prompt-eval-loop`：AI prompt/eval/agent workflow 实现与检查。
- `sre-lite-ops`：SLO、runbook、发布、事故复盘和最小运维。
