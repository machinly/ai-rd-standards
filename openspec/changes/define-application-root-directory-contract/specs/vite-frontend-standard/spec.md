## MODIFIED Requirements

### Requirement: 前端项目必须使用 Vite 默认路径

新前端项目 MUST 默认使用 Vite，并保持入口、源码、样式和公开资源目录清晰。所有前端路径 MUST 相对该前端应用根解释；含多个可部署应用的仓库 MUST 默认把每个前端应用根放在 `web/<app>/`，不得在聚合仓库根用 `src/` 承载某一个前端。

#### Scenario: 多应用仓库创建用户前端

- **GIVEN** 仓库包含后端服务及独立的用户端和管理端前端
- **WHEN** 创建用户前端
- **THEN** 先在项目地图声明 `web/user`
- **AND** Vite 模板在该空目录生成
- **AND** `package.json`、`index.html`、`src/` 与 `public/` 位于 `web/user/` 内
- **AND** 管理端使用自己的 `web/admin/` 应用根

#### Scenario: 单前端仓库

- **GIVEN** 仓库只包含一个可部署前端
- **AND** 项目地图声明 `repository_mode: single-application` 与 `path: .`
- **WHEN** 创建交互型前端
- **THEN** 仓库根可以作为前端应用根
- **AND** 使用 `Vite + React + TypeScript`

#### Scenario: 创建简单静态页

- **GIVEN** 页面只是简单静态落地页、内部说明页或原型
- **WHEN** 不需要复杂交互
- **THEN** 可以使用 Vite `vanilla-ts`
- **AND** 不引入 React 或复杂状态库
