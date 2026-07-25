# 提案：定义 Vite + Vercel 风格前端研发规范

## 意图

为一人公司建立默认前端落地路径，让前端研发从 OpenSpec 需求开始，稳定落到 Vite、TypeScript、可测试构建、Vercel Geist 风格 token、可访问性和最小发布验证上。

## 范围

- 定义 Vite 前端项目结构。
- 定义默认框架、包管理器、API 边界和配置安全。
- 定义 Vercel `design.md` / `design.dark.md` 的 token 落地方式。
- 定义可访问性、性能和发布前门禁。
- 创建前端落地 skill 和结构检查脚本。

## 不做

- 不创建真实产品前端。
- 不建立完整组件库或设计系统 package。
- 不定义 SSR、SEO、国际化、复杂状态管理或 E2E 平台。
- 不处理前后端 contract 代码生成细节。

## 依据

- 《人月神话》：避免把框架和组件库当银弹。
- 小型项目管理：只保留能减少返工的少量检查点。
- Vite 官方：dev server、production build、`index.html` 入口、Node 版本要求、env 暴露规则、部署和 preview 边界。
- Vitest 官方：贴近 Vite 的测试运行器。
- Vercel Geist：高对比颜色系统、浅色/深色主题、克制界面和 Grid 使用边界。
- WCAG/MDN/Web Vitals：可访问性与用户体验底线。

## 需要人的判断

建议默认采用 `Vite + React + TypeScript + pnpm`。如果用户偏好 Vue/Svelte/Vanilla 或其他包管理器，再按项目修改。

