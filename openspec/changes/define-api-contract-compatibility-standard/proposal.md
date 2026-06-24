# Proposal: define API contract compatibility standard

## 意图

建立一人公司 API 契约、兼容性与版本演进规范，覆盖 gRPC/Protobuf、HTTP/BFF、webhook/event、frontend client、AI tool schema、错误模型和 contract tests，避免一人公司后期被破坏性契约变更拖住。

## 范围

- 新增 `api-contract-compatibility-standard` spec。
- 新增 W2 API compatibility 规范文档。
- 创建 `api-contract-compatibility-guard` skill 和 verifier。
- 补充来源索引与 README。

## 不做什么

- 不搭建完整 API gateway、schema registry 或文档门户。
- 不替代 W2 architecture、W9 deprecation、W5 testing、W6 release。
- 不要求所有 experimental/internal surface 都做完整 contract tests。
- 不连接真实 CI、Buf registry、OpenAI eval 平台或外部 API 管理系统。

## 依据

- Hyrum's Law。
- Google AIP-180 Backwards Compatibility。
- Protobuf proto3 guide / best practices。
- Buf breaking change detection。
- gRPC error handling / status codes。
- SemVer。
- OpenAI function calling / Structured Outputs。
- Confluent schema evolution。
- Software Engineering at Google, Deprecation。

## 需要人的判断

只有这些需要人工 checkpoint：internal/experimental 升级为 stable/public、breaking contract、字段/RPC/event/tool/route 删除、错误/权限/retry/idempotency 语义变化、多版本并行或强制迁移、消费者未知时移除 deprecated surface。
