# 提案：定义知识管理、文档与上下文恢复规范

## 意图

为一人公司建立可检查的知识管理基线，让产品、服务、前端应用和 AI workflow 拥有稳定文档入口、上下文包、术语表、常见任务 how-to 和复审记录，降低中断后难以恢复、Codex 接手靠猜、术语漂移和过期文档误导的风险。

## 范围

- 定义 `knowledge/docs-map`、`knowledge/context-packs`、`knowledge/glossary`、`knowledge/how-to`、`knowledge/freshness` artifacts。
- 定义 Diátaxis 在一人公司中的裁剪方式。
- 定义 Codex 接手 target 时的上下文读取顺序。
- 定义文档风格、canonical source、术语、过期、归档和高风险变更后的复审规则。
- 创建知识上下文落地 skill 和检查脚本。

## 不做

- 不建立大型知识库或 wiki 平台。
- 不要求每个 target 都完整写 tutorial、how-to、reference、explanation 四大类。
- 不把知识工件替代 OpenSpec、ADR、SLO、runbook、security record 或 product bet。
- 不把 secret、PII、生产凭据或完整 prompt/response 写入文档。

## 依据

- 《人月神话》：概念完整性需要共享语言和一致文档。
- 小型项目管理：文档只保留能恢复上下文和支持行动的内容。
- Diátaxis documentation framework。
- Google Software Engineering at Google, Knowledge Sharing / Documentation is Like Code。
- Google Developer Documentation Style Guide。
- Write the Docs documentation principles。
- Docs-as-code。
- OpenSpec change artifacts。

## 需要人的判断

建议默认：任何生产 target、超过 1 周的 product bet、AI workflow、架构/安全/数据高风险变更，都必须有 docs map 和 context pack。人只判断 canonical source、术语、归档/删除和 context pack 是否足够接手。
