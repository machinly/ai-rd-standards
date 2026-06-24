# 任务

## 1. 来源与约束

- [x] 1.1 查证 Hyrum's Law、Software Engineering at Google deprecation。
- [x] 1.2 查证 Google AIP-180、Protobuf proto3/best practices、Buf breaking。
- [x] 1.3 查证 gRPC error/status、SemVer、OpenAI function calling/Structured Outputs、schema evolution。
- [x] 1.4 补充阶段 18 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. API 契约规范

- [x] 2.1 编写阶段 18 规范正文。
- [x] 2.2 定义 surface map、compatibility policy、protobuf evolution、error model、contract tests、AI tool schema。
- [x] 2.3 定义 Go/Kratos/gRPC/Protobuf、HTTP/Vite、AI workflow 默认规则和人审点。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 18 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `api-contract-compatibility-guard` skill。
- [x] 4.2 添加 API contract artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 API contract 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target contract artifacts，因此不连接 Buf registry、OpenAI eval 或 API gateway。

验证说明：本仓库是规范仓库，不包含真实产品 target 的 contract artifacts，也不应在规范阶段连接 Buf registry、OpenAI eval 或 API gateway。已通过 `verify_api_contracts.py` 的临时 `assistant-api` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `contracts/surface-map`。
