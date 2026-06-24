# 任务

## 1. 来源与约束

- [x] 1.1 查证 Vite、Vitest、Vercel Geist、WCAG、MDN、Web Vitals 官方资料。
- [x] 1.2 补充阶段 3 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 前端规范

- [x] 2.1 编写阶段 3 规范正文。
- [x] 2.2 定义项目结构、API 边界、配置安全、设计 token、可访问性、性能门禁。
- [x] 2.3 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 3 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `vite-geist-frontend` skill。
- [x] 4.2 添加前端结构与 token 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证前端检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不适用的 Vite 项目门禁。

验证说明：本仓库是规范仓库，不是 Vite 前端仓库，因此 `pnpm build`、`pnpm test`、`pnpm lint`、`pnpm preview` 不适用于当前仓库。已通过 `verify_vite_frontend.py` 的临时 Vite 项目正向测试，并确认该脚本会在当前规范仓库上报告缺失项。
