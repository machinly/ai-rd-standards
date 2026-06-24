# 任务

## 1. 来源与约束

- [x] 1.1 查证 Kratos、sqlc、gRPC、Protobuf、Go、OpenTelemetry 官方资料。
- [x] 1.2 补充阶段 2 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 服务端规范

- [x] 2.1 编写阶段 2 规范正文。
- [x] 2.2 定义服务目录、API、数据访问、实现顺序、质量门禁、最小运维要求。
- [x] 2.3 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 2 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `go-kratos-sqlc-service` skill。
- [x] 4.2 添加服务结构验证脚本。
- [x] 4.3 校验 skill。
- [x] 4.4 用阶段 2 结果回填阶段 1 skill 的 forward-test 任务。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 记录不能运行或暂不适用的验证。

验证说明：本仓库是规范仓库，不是 Go 服务仓库，因此阶段 2 中的 `go test ./...`、`sqlc generate`、`sqlc vet` 等服务门禁不适用于当前仓库。已通过 `verify_service_layout.py` 的临时服务结构正向测试，并确认该脚本会在当前规范仓库上报告缺失项。
