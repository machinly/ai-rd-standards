# W4 Build 触发专项：Vite + Vercel 风格前端研发规范 v0.1

## W4 触发定位

本文件是 W4 Build 的触发型专项，不是 W4 主入口。只有当当前实现涉及 Vite、React/TypeScript、前端 API adapter、设计 token、可访问交互、构建、预览或前端最小测试门禁时，才需要读取本文件。

普通 W4 实现入口应先回到 `docs/W4-build/main.md`，由主入口判断是否触发本专项。

## 目标

给一人公司定义一条默认前端落地路径：从 OpenSpec 需求出发，用 Vite 建立轻量、可构建、可预览、可测试、可访问、视觉一致的前端。Vercel `design.md` / `design.dark.md` 作为视觉 token 和界面克制度参考，但不复制 Vercel 品牌，也不把前端做成沉重的设计系统工程。

## 本专项只解决什么

- Vite 项目结构与默认脚手架。
- 前端与 Go/gRPC 后端的接口边界。
- 环境变量与配置安全。
- Vercel Geist 风格 token 的落地方式。
- 可访问性、性能和发布前最小门禁。
- 一人公司前端 skill 与结构检查脚本。

不在本专项展开：完整组件库、设计稿协作流程、SSR/边缘渲染、国际化、复杂状态管理、端到端测试平台、埋点分析平台。这些需要时单独开 change。

## 依据转译

- 《人月神话》：前端框架和组件库不是银弹。默认路径要减少重复决策，不制造“先搭平台再做产品”的幻觉。
- 小型项目管理：前端阶段只保留能避免返工的检查点：契约、状态、样式 token、可访问性、构建、预览。
- Vite 官方：Vite 提供 dev server 和生产 build；`index.html` 是入口；当前文档显示 Vite v8.1.0，Node 要求 20.19+ 或 22.12+。
- Vite env 官方：只有 `VITE_*` 变量会暴露到客户端包中，敏感信息不能放进去。
- Vite deploy 官方：`vite preview` 只适合本地预览构建结果，不是生产服务器。
- Vitest 官方：Vitest 与 Vite 配置和转换管线贴近，适合作为前端最小测试门禁。
- Vercel Geist：颜色系统强调高对比、背景/边框/文字角色明确；Grid 适合可见 guide 的页面，不应滥用于普通列表。
- WCAG/MDN/Web Vitals：语义化 HTML、键盘焦点、对比度、LCP/INP/CLS 是低成本且高收益的前端质量底线。

## 默认决策

- 交互型产品默认 `Vite + React + TypeScript`。
- 简单静态页或原型可用 `vanilla-ts`。
- 包管理器默认沿用仓库已有工具；新项目默认 `pnpm`，因为 lockfile 小、速度快、workspace 友好。
- UI 风格默认参考 Geist：克制灰阶、高对比文字、清晰边框、少装饰、浅色/深色 token 成对存在。
- API 通信默认通过后端提供的 HTTP/BFF 层访问；浏览器不直接使用内部 gRPC。若需要 gRPC-Web 或 Connect，必须在 `design.md` 说明。
- 默认不引入全局状态库。跨页面共享状态、缓存或协作编辑真实存在时再引入。
- 默认不引入大型 UI 组件库。先用少量本地组件和 CSS token，重复出现三次以上再抽象。

## 前端目录规范

新前端默认目录：

```text
index.html
package.json
vite.config.ts
tsconfig.json
src/
  app/
  components/
  features/
  lib/
  styles/
  main.tsx
  vite-env.d.ts
public/
```

一人公司裁剪规则：

- `src/features/<feature>/` 承载业务页面、局部组件和 API adapter。
- `src/components/` 只放跨 feature 重复使用的基础组件。
- `src/lib/` 放 fetch client、date、format、schema、small helpers，不放业务流程。
- `src/styles/tokens.css` 放颜色、间距、半径、阴影、字体变量。
- 少于 3 个页面时，不拆复杂路由、状态管理、主题包、组件库包。
- 不为“以后可能有”预建 monorepo、design system package、storybook、复杂 mock 平台。

## API 与配置规范

- 前端 contract 先写 OpenSpec scenario，再写 API adapter。
- 浏览器只调用公开 HTTP/BFF endpoint，不直接依赖内部 gRPC 服务。
- 前端请求必须集中在 `src/lib/api` 或 feature-local adapter，禁止把 `fetch` 散落在视图组件里。
- 请求必须处理 loading、empty、error、success 四种状态。
- 写操作必须有防重复提交策略，至少包括 disabled 状态或幂等 key 之一。
- `VITE_*` 变量视为公开信息，不能存 secret、private API key、数据库连接、服务端 token。
- 环境变量必须在 `src/vite-env.d.ts` 或等价 schema 中类型化。

## 设计 token 规范

默认建立少量语义 token，而不是直接在组件里散落 Vercel 原始 token：

```css
:root {
  --color-bg: #ffffff;
  --color-bg-subtle: #fafafa;
  --color-text: #171717;
  --color-text-muted: #4d4d4d;
  --color-border: #e6e6e6;
  --color-accent: #006bff;
  --radius-control: 6px;
  --radius-card: 8px;
}

[data-theme="dark"] {
  --color-bg: #000000;
  --color-bg-subtle: #000000;
  --color-text: #ededed;
  --color-text-muted: #a0a0a0;
  --color-border: #292929;
  --color-accent: #006efe;
}
```

落地规则：

- 组件只使用语义 token，不直接引用 `gray-700` 这类原始 token 名。
- 卡片半径默认不超过 8px。
- 工具型/SaaS 页面优先密度、扫描、对齐、表格、筛选、状态，不做营销页式大 hero。
- 文本按钮只用于明确命令；图标按钮必须有 tooltip 或 `aria-label`。
- 深色主题不是反色补丁，必须检查边框、hover、focus、disabled、empty/error 状态。
- 不使用离散装饰光斑、渐变球、bokeh 背景。
- Vercel Geist Grid 只用于可见 guide 是设计一部分的页面；普通列表、卡片网格直接用 CSS grid。

## 可访问性规范

- 页面必须有语义结构：`main`、有层级的 heading、真实 `button`/`a`/`label`。
- 交互元素必须键盘可达，并有可见 `:focus-visible`。
- 文字和关键 UI 对比度按 WCAG AA 作为底线。
- 表单必须有 label、错误说明和提交中状态。
- 弹层、菜单、抽屉必须管理焦点和 Esc/点击外部行为。
- 图标按钮、状态点、加载状态不能只靠颜色表达含义。
- 动效必须尊重 `prefers-reduced-motion`。

## 性能与发布门禁

每个前端 change 默认运行：

```bash
pnpm install
pnpm build
pnpm test
pnpm lint
pnpm preview
```

如果项目不是 pnpm，使用仓库已有包管理器的等价命令。

最小验收：

- 本地 `vite preview` 打开关键页面，确认构建产物能运行。
- 首屏没有明显布局跳动、空白和不可读文字。
- 关键用户路径至少有一个 Vitest 测试或人工验收记录。
- 生产部署不使用 `vite preview` 作为服务器。
- 关键页面记录 LCP、INP、CLS 的目标或采集计划；早期可先用 Lighthouse/DevTools 手工记录。

## 只问人的关键判断

默认不问：目录命名、局部组件拆分、CSS 变量名、普通 loading/error UI、pnpm/vite 基础命令。

必须问：

- 是否不用 React + TypeScript。
- 是否需要 SSR、SEO 强依赖或服务端渲染。
- 是否引入大型 UI 库、复杂状态库或组件平台。
- 是否前端直接接入第三方支付、登录、地图、分析等带成本或隐私风险的 SDK。
- 是否公开新品牌视觉，而不只是产品内工具界面。
- 是否接入 gRPC-Web/Connect，而不是普通 HTTP/BFF。

## 本专项 Review A：一人公司可落地性

结论：可落地，前提是把设计系统缩成 token + 少量本地组件。

- Vite 默认脚手架和少量目录能让一个人在半天内启动项目。
- Geist 只作为视觉语言参考，避免复制完整组件系统。
- 质量门禁保持在 build/test/lint/preview，不要求一次性建 Storybook、视觉回归和完整 E2E。
- 最大摩擦是“好看”和“可维护”容易被 AI 生成的大量 CSS 冲散；需要 skill 和脚本检查基础结构、tokens 和状态。
- 下一步应在真实前端项目中用 `vite-geist-frontend` skill 创建或审查一次页面。

## 本专项 Review B：产品/工程/运维风险

结论：风险可控，主要风险是把 Vercel 风格误用成品牌复制，或把前端过早平台化。

- 已要求语义 token，降低直接拷贝 Vercel 原始 token 的耦合。
- 已把 secrets、公开 env、HTTP/BFF 边界写清，避免浏览器泄露后端能力。
- 已加入 WCAG、Web Vitals 和 `vite preview` 边界，覆盖早期上线风险。
- 没有默认引入 SSR、复杂状态库、大 UI 库，能防止一人公司陷入平台建设。
- 风险缺口是尚未定义具体 API schema 生成和前后端 contract 流程，后续可在“API/BFF 规范”阶段补齐。

## 当前只需要你判断的事项

我建议默认接受：交互型前端默认 `Vite + React + TypeScript + pnpm`。只有你明确偏好 Vue/Svelte/Vanilla 或 npm/yarn/bun 时才改变。
