# Design

## 工件形态

每个 target 使用轻量契约工件：

- `contracts/surface-map/<target>.json`
- `contracts/compatibility-policy/<target>.md`
- `contracts/protobuf-evolution/<target>.md`
- `contracts/error-model/<target>.md`
- `contracts/contract-tests/<target>.json`
- `contracts/ai-tool-schemas/<target>.json`，仅 AI tool / structured output target 必需。

JSON 用于机器检查，Markdown 用于人审语义。契约工件只链接 proto、OpenSpec、generated client、eval 和 release artifacts，不复制全部 API 文档。

## 验证策略

`api-contract-compatibility-guard` 提供 `verify_api_contracts.py`：

- 检查 surface map 必填字段、surface path、stability、consumer、version、compatibility。
- 检查 compatibility policy、protobuf evolution、error model 必要章节。
- 检查 contract-tests JSON 的 baseline、test suites、fixtures、CI/release gates 和人审点。
- 如果存在 gRPC/protobuf surface，要求 protobuf root、protobuf evolution 和 breaking check gate。
- 如果存在 AI tool schema surface，要求 `contracts/ai-tool-schemas/<target>.json`、schema path、eval link 和 AI 行为人审点。
- 检查 secret、PII、raw prompt/response 不进入契约工件。

## 裁剪原则

- Additive change 默认快速推进，但必须保留 contract tests。
- Stable/public surface 比 internal/experimental surface 更严格。
- Breaking change 必须单独 OpenSpec change，链接 deprecation/removal 和 release/rollback。
- verifier 不判断业务语义是否真的兼容，只检查证据是否存在；语义变化仍然需要人审。
