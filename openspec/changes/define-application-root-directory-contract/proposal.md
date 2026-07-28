## Why

用户服务第四轮暴露了一个可复现的规范歧义：现行条文定义了 Go 服务内部的 `api/`、`cmd/` 与 `internal/`，却没有先区分聚合仓库根和具体应用根。执行者因此可以把多应用仓库根误当成 Go 服务根，在根目录创建 `go.mod` 与 `internal/`，同时仍声称遵循服务目录规范。

前三轮实际使用过 `services/user-center/`、`web/user/` 和 `web/admin/`，第五轮也明确需要多个可部署应用。本 change 把“仓库根—应用根—应用内部”补成一个可检查合同，并让第五轮在任何模板或代码生成前验证该合同。

## Routing

- path: Standard
- visual_ux: not-required
- reason: 本 change 修改研发规范、项目地图和静态验证器，不改变产品界面或用户任务。

## What Changes

- 区分 `single-application` 与 `multi-application` 仓库。
- 要求含可部署应用的 Standard/High-risk 项目在首次模板生成前声明应用根。
- 多应用仓库默认把 Go 服务放在 `services/<service>/`，把前端放在 `web/<app>/`。
- 明确服务的 `go.mod`、`internal/` 等路径和前端的 `package.json`、`src/` 都相对应用根，而不是无条件相对仓库根。
- 扩展项目证据验证器，在启用应用目录门禁时拒绝多应用仓库根的 `internal/` 等应用私有目录。
- 第五轮用户服务实验使用新合同作为编码前门禁。

## Non-Goals

- 不强迫单应用仓库增加 `services/` 或 `web/` 包装目录。
- 不为假想的未来应用预建 monorepo、共享包或组件库。
- 不规定所有语言、移动端或基础设施仓库的目录布局。
- 不恢复、移动、删除或评价任何既有用户服务代码。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `go-service-standard`
- `vite-frontend-standard`
- `knowledge-context-standard`

## Impact

- 四分类十一项目和 2,337 个正式 rule-id 数量不变；本 change 收紧既有 `IMPL-*` 与 `EVALUATION-GOV-MAP-002` 的含义。
- `tools/verify_project_evidence.py` 新增 `--require-application-layout` 和单一职责的 `--application-layout-only`，旧调用保持兼容。
- 用户服务第五轮必须使用多应用目录模式；其他仓库只有在规则适用或显式启用验证时受影响。
