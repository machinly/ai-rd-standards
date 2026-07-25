# Design

## 工件形态

每个 target 使用五个轻量工件：

- `dev-workspace/workspace-map/<target>.json`
- `dev-workspace/command-catalog/<target>.md`
- `dev-workspace/local-environment/<target>.md`
- `dev-workspace/seed-fixtures/<target>.md`
- `dev-workspace/verification/<target>.json`

JSON 用于机器检查，Markdown 用于人快速操作。工件链接 OpenSpec、release、testing、contract、knowledge artifacts，不复制长篇说明。

## 验证策略

`dev-workspace-automation-guard` 提供 `verify_dev_workspace.py`：

- 检查 workspace map 必填字段、toolchains、entrypoints、路径存在。
- 检查 command catalog、local environment、seed fixtures 的必要章节。
- 检查 verification JSON 的 one-step commands、smoke checks、generated/data/frontend/AI checks、CI mapping。
- 按 stack 检查 Go、sqlc、Protobuf/buf、Vite、AI target 的最小命令面。
- 检查 secret、PII、raw prompt/response、生产凭据不进入 dev artifacts。

## 裁剪原则

- 一人公司默认先有命令目录和 verification，再决定是否需要 devcontainer/Compose。
- one-step local verify 是快速可信子集，不是完整 CI。
- 破坏性 reset/migration/backfill/tool commit 必须显式标注并人审。
- verifier 只确认入口存在，不证明本地服务真的启动；真实项目应在 release/CI 阶段运行命令。
