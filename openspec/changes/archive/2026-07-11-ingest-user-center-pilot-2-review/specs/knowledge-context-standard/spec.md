# knowledge-context-standard 的变更规格

## MODIFIED Requirements

### Requirement: 生产 target 必须定义知识入口和上下文包

生产服务、前端应用、AI workflow、超过 1 周的 product bet 或高风险架构/安全/数据变更 MUST 在 `governance/knowledge/` 具备知识管理 artifacts，并由项目根导航链接。

#### Scenario: 新生产 target 进入研发

- GIVEN 一个 target 会进入生产或需要长期维护
- WHEN 创建 OpenSpec change
- THEN 创建 `governance/knowledge/docs-map/<target>.json`
- AND 创建 `governance/knowledge/context-packs/<target>.md`
- AND 创建 `governance/knowledge/glossary/<target>.md`
- AND 创建 `governance/knowledge/how-to/<target>.md`

#### Scenario: 仅本地实验

- GIVEN 一个实验不会进入生产、不会访问生产数据、不会对用户开放
- WHEN 不创建 knowledge artifacts
- THEN 在 OpenSpec tasks 或 design 中记录跳过原因

## ADDED Requirements

### Requirement: 项目必须提供统一治理根和项目地图

Standard/High-risk 项目 MUST 将流程/guard 工件放在 `governance/<registered-domain>/`，并提供 `governance/README.md` 与 `governance/project-map.json`，说明全部顶层目录、正式源码与过程证据、推荐阅读顺序、运行进程、常用命令和权威来源。

#### Scenario: 新 guard 创建工件

- GIVEN guard 建议写入 `quality/`、`auth/`、`reviews/` 或其他根目录
- WHEN 项目使用统一治理根
- THEN 将路径重映射到 `governance/<registered-domain>/`
- AND 更新 project map 中的 domain registry
- AND 不新增未登记的治理顶层目录

#### Scenario: 新会话接手项目

- GIVEN Codex 只获得仓库路径
- WHEN 阅读根 README 和 governance/project-map.json
- THEN 能区分源码、运行资产和过程证据
- AND 能找到 active OpenSpec、当前状态、关键旅程、运行进程和常用命令

