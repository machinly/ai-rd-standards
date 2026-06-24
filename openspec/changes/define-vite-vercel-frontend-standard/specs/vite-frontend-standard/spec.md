# vite-frontend-standard 的变更规格

## ADDED Requirements

### Requirement: 前端项目必须使用 Vite 默认路径

新前端项目 MUST 默认使用 Vite，并保持入口、源码、样式和公开资源目录清晰。

#### Scenario: 创建交互型前端

- GIVEN 需要创建新的交互型产品前端
- WHEN 没有已有前端框架约束
- THEN 使用 `Vite + React + TypeScript`
- AND 包含 `index.html`、`package.json`、`vite.config.ts`、`tsconfig.json`、`src/`、`public/`

#### Scenario: 创建简单静态页

- GIVEN 页面只是简单静态落地页、内部说明页或原型
- WHEN 不需要复杂交互
- THEN 可以使用 Vite `vanilla-ts`
- AND 不引入 React 或复杂状态库

### Requirement: 前端配置必须保护客户端边界

前端配置 MUST 将 `VITE_*` 变量视为公开信息，并避免把敏感信息打包到客户端。

#### Scenario: 新增环境变量

- GIVEN 前端需要读取配置
- WHEN 新增 env 变量
- THEN 只有可公开配置使用 `VITE_` 前缀
- AND secret、private API key、数据库连接和服务端 token 不得使用 `VITE_`
- AND 在 `src/vite-env.d.ts` 或等价 schema 中声明类型

#### Scenario: 调用后端能力

- GIVEN 前端需要调用后端服务
- WHEN 浏览器发起请求
- THEN 调用公开 HTTP/BFF endpoint
- AND 不直接依赖内部 gRPC 服务

### Requirement: UI 必须使用语义设计 token

前端 UI MUST 通过语义 token 落地 Vercel Geist 风格，而不是在组件中散落原始颜色值。

#### Scenario: 创建主题 token

- GIVEN 项目需要基础视觉样式
- WHEN 建立样式入口
- THEN 创建 `src/styles/tokens.css` 或等价文件
- AND 定义背景、文字、边框、强调色、半径等语义 token
- AND 同时覆盖浅色和深色主题

#### Scenario: 编写组件样式

- GIVEN 组件需要颜色、边框或半径
- WHEN 编写 CSS
- THEN 使用语义 token
- AND 卡片半径默认不超过 8px
- AND 图标按钮提供 `aria-label` 或 tooltip

### Requirement: 前端体验必须具备可访问性底线

前端页面 MUST 满足语义结构、键盘可达、可见焦点和基本对比度要求。

#### Scenario: 创建交互页面

- GIVEN 页面包含用户交互
- WHEN 实现 UI
- THEN 使用语义 HTML
- AND 交互元素键盘可达
- AND 提供可见 `:focus-visible`
- AND 表单包含 label、错误说明和提交中状态

#### Scenario: 使用状态和图标

- GIVEN UI 使用图标、颜色或状态点表达信息
- WHEN 信息对用户重要
- THEN 不得只依赖颜色传达含义
- AND 为辅助技术提供文本或可访问名称

### Requirement: 前端交付必须运行最小门禁

前端变更交付前 MUST 运行可适用的构建、测试、lint 和预览检查。

#### Scenario: 标准 Vite 前端交付

- GIVEN 前端 change 准备交付
- WHEN 执行验证
- THEN 运行依赖安装命令
- AND 运行 build
- AND 运行 test
- AND 运行 lint
- AND 用 preview 本地检查构建产物

#### Scenario: 命令不能运行

- GIVEN 某个门禁命令在当前环境不能运行
- WHEN 交付总结
- THEN 记录未运行命令、原因、风险和后续补救项

