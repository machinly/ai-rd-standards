# 设计：Vite + Vercel 风格前端研发规范

## 设计决策

### 1. 默认 React + TypeScript，但保留 Vite 的多框架能力

Vite 官方支持多种模板。为了减少一人公司每次重新选型的消耗，交互型产品默认 React + TypeScript；简单静态页可用 vanilla-ts。已有项目约束优先。

### 2. 用语义 token 吸收 Geist，而不是复制 Vercel 品牌

Vercel `design.md` 和 `design.dark.md` 提供了浅色/深色 token。规范只要求抽象成 `--color-bg`、`--color-text`、`--color-border`、`--color-accent` 等语义 token，避免组件依赖 Vercel 原始命名。

### 3. 浏览器只接公开 HTTP/BFF 层

W4 Go/Kratos 服务端专项已定义后端内部 gRPC first。前端运行在浏览器，默认不直接接内部 gRPC；公开 HTTP/BFF 是更简单、安全、可缓存、可调试的边界。gRPC-Web/Connect 必须单独说明。

### 4. 质量门禁保持少而硬

默认门禁为 install、build、test、lint、preview 和关键路径人工验收。不要求一开始有完整 Storybook、视觉回归和 E2E 平台，避免平台化过早。

### 5. 可访问性和性能从第一天进入验收

语义 HTML、键盘焦点、对比度、表单错误状态、LCP/INP/CLS 是前端用户体验的最低成本信号。

## 取舍

- React 默认值会降低选择成本，但不是 Vite 的唯一合理选择。
- 不默认 UI 库会让早期组件手写更多，但避免早期被组件库 API 锁死。
- 不默认 SSR 简化部署，但 SEO 强依赖产品需要单独决策。
- Geist 风格有利于开发者工具界面，但营销页、消费级品牌页可能需要更强视觉定制。

