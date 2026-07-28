## MODIFIED Requirements

### Requirement: 项目必须提供统一治理根和项目地图

Standard/High-risk 项目 MUST 将流程/guard 工件放在 `governance/<registered-domain>/`，并提供 `governance/README.md` 与 `governance/project-map.json`，说明全部顶层目录、正式源码与过程证据、推荐阅读顺序、运行进程、常用命令和权威来源。含可部署应用的仓库 MUST 在首次模板生成前同时声明 `repository_mode` 和 `applications[]`，使仓库根与每个应用根可机器区分。

#### Scenario: 多应用仓库声明应用根

- **GIVEN** 项目实际包含多个可部署服务或前端
- **WHEN** 准备生成第一个应用
- **THEN** `repository_mode` 为 `multi-application`
- **AND** 每个 `applications[]` 项记录 `id`、`kind`、`path` 与 `manifest`
- **AND** Go 服务缺省使用 `services/<service>/`
- **AND** 前端缺省使用 `web/<app>/`

#### Scenario: 单应用仓库声明应用根

- **GIVEN** 项目只有一个可部署应用
- **WHEN** 创建项目地图
- **THEN** `repository_mode` 为 `single-application`
- **AND** 唯一应用可以声明 `path: .`

#### Scenario: 新 guard 创建工件

- **GIVEN** guard 建议写入 `quality/`、`auth/`、`reviews/` 或其他根目录
- **WHEN** 项目使用统一治理根
- **THEN** 将路径重映射到 `governance/<registered-domain>/`
- **AND** 更新 project map 中的 domain registry
- **AND** 不新增未登记的治理顶层目录

#### Scenario: 新会话接手项目

- **GIVEN** Codex 只获得仓库路径
- **WHEN** 阅读根 README 和 `governance/project-map.json`
- **THEN** 能区分仓库级资产、每个应用根、运行资产和过程证据
- **AND** 能找到 active OpenSpec、当前状态、关键旅程、运行进程和常用命令
