# 提案：整理一人公司研发规范导航层

## 意图

现有规范已经覆盖很多研发场景，但 README 把所有阶段平铺展示，第一版导航也仍偏“场景/主题分组”。这个变更把索引改成 AI 研发工作流：从 intake、discovery、OpenSpec、AI 行为设计、实现、验证、发布、运行、学习到维护。

## 范围

- 缩短 README，让它只承担根入口职责。
- 新增 `docs/00-start-here.md` 作为 AI 研发工作流入口。
- 新增 `docs/00-standard-index.md` 作为 workflow-to-standard map。
- 将规范文件移动到 `docs/Wx-*/main.md` 与语义化触发专项，使物理结构和 workflow 一致。
- 新增 `knowledge/` 工件，让 Codex 和人可以恢复上下文。
- 为导航层新增 OpenSpec 规格。

## 不做什么

- 不新增编号阶段。
- 不重写既有 55 份规范正文。
- 不改变已有技术偏好和 skill 行为。
- 不建立复杂文档门户或站点。

## 依据

- W2 OpenSpec / Risk：一人公司只把高影响判断交给人。
- W9 知识恢复专项：文档必须有 canonical 入口、context pack 和 freshness。
- W0 Intake（历史编号 50）：一人公司不维护无限 backlog，只维护当前选择和下一步。
- Diataxis：how-to、reference、explanation 要分离。
- 《人月神话》：概念完整性依赖少数清晰入口，而不是更多并列材料。

## 需要人的判断

- 是否接受 W0-W9 AI 研发工作流成为默认索引方式。
- 是否接受 README 不再展示完整阶段清单。
