# W4 触发专项：开发工作区、命令自动化与 AI 协作编码规范

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及本地工具链、命令目录、seed/fixtures、one-step verify、Codex/AI coding agent、批次日志、自审或 verification JSON 时，才读取本文件。

普通 W4 实现先回到 `docs/W4-build/00-main.md`。

## 目标

把开发工作区可复现性和 AI 协作编码合并成一个执行入口：一个人和 Codex 都能知道怎么开始、改哪一批、跑什么命令、怎么自审、失败时何时停。

默认原则：AI 可以加速实现，不能替代 OpenSpec 边界和人的高影响判断；本地命令必须可复现，不能靠聊天记录或个人记忆。

## 主要角色消费者

- Tech Lead：制定 brief、batch scope、stop conditions。
- 后端/前端：执行命令、生成代码、跑本地验证。
- QA：读取 verification 和 residual risks。

## 最小工件

```text
dev-workspace/
  workspace-map/<target>.json
  command-catalog/<target>.md
  local-environment/<target>.md
  seed-fixtures/<target>.md
  verification/<target>.json

ai-coding/
  implementation-brief/<change-id>.md
  batch-log/<change-id>.md
  review/<change-id>.md
  verification/<change-id>.json
```

小修可以只写最短 brief 和验证记录；影响生产、数据、安全、AI 行为或发布流水线时必须留下完整 AI coding 证据。

## 必须覆盖

- Go/Node/sqlc/protoc/buf/Vite/OpenSpec 等工具链来源和 install check。
- setup、generate、develop、test、verify、run local、reset、debug、release prep 命令。
- seed/fixtures 不使用真实用户数据，AI fixtures 包含代表、边界和失败样例。
- implementation brief 链接 OpenSpec change、context sources、target files、allowed autonomy、human checkpoints、stop conditions。
- batch log 一批只回答一个 review 问题；generated code、schema/proto、业务逻辑、UI、migration、eval fixture 尽量分批。
- review 检查意图、架构、AI 常见错误、依赖/安全和验证结果。

## 默认规则

- 至少有一个 one-step local verify 命令；Go 跑 `go test ./...`，Vite 跑 build，sqlc/proto/AI eval 按触发补。
- 本地 AI workflow 默认 dry-run、mock provider 或低成本 sandbox，不默认调用真实模型和真实工具。
- 无法解释的失败测试不能删除或 skip；标记 `needs-human` 或 `needs-more-tests`。
- AI 不得访问真实 secret、真实用户数据、生产数据或真实供应商，除非人审允许。
- 如果 AI 反复犯同类错误，更新 skill、script、template 或仓库指令，而不是靠下次记住。

## 需要人判断

- 本地命令调用真实供应商、真实模型、真实支付、真实邮件或真实生产数据。
- 暴露破坏性 reset、migration、backfill、生产发布或 tool commit 为一键命令。
- 新增长期工具链、devcontainer、compose stack、付费开发工具或多个 agent 并行修改同一边界。
- 让 AI 执行有副作用命令、访问真实数据、扩大自主权限或改变产品/OpenSpec scope。
- 接受失败测试被删除/跳过、未解释 flaky、未覆盖高风险路径。

## Review A：一人可执行性

合并后，W4 的“如何跑起来”和“AI 如何安全改代码”共用同一个执行面，减少重复命令和重复 handoff。一个人可以先写黄金路径，再让 Codex 按小批次推进。

## Review B：产品 / 工程 / 运维风险

保留了真实副作用、破坏性命令、AI 越权、失败测试和验证缺口的人审门禁。最小安全下一步是让每个 OpenSpec change 都能说清本地验证命令和 AI 批次证据。

