# 任务

## 1. 来源与约束

- [x] 1.1 查证 Diátaxis、Google Developer Documentation Style Guide。
- [x] 1.2 查证 Software Engineering at Google 的 Knowledge Sharing / Documentation is Like Code。
- [x] 1.3 查证 Write the Docs documentation principles 和 docs-as-code。
- [x] 1.4 补充阶段 16 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 知识管理规范

- [x] 2.1 编写阶段 16 规范正文。
- [x] 2.2 定义 docs map、context pack、glossary、how-to、freshness artifacts。
- [x] 2.3 定义 Diátaxis 裁剪、Codex 上下文恢复、文档风格和人审点规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 16 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `knowledge-context-recovery-guard` skill。
- [x] 4.2 添加 knowledge artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 knowledge 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实 target knowledge artifacts，因此不连接外部 wiki 或文档平台。

验证说明：本仓库是规范仓库，不包含真实产品 target 的 knowledge artifacts，也不应在规范阶段连接外部 wiki。已通过 `verify_knowledge_context.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `knowledge/docs-map`。
