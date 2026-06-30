# 前端角色入口

## 职责

前端角色负责把用户可见路径、交互状态、可访问性、AI disclosure、错误/降级状态和发布前 preview 证据落到 Vite 前端或文档界面中。

## 默认参与的 W

- 主责：W4 Build、W5 Verify。
- 参与：W1 Discovery、W2 OpenSpec / Risk、W6 Release。

## 必须参与的触发条件

- 新 UI、关键路径、表单、设置、管理台、开发者文档、AI 输出面、通知/偏好、计费/权益展示。
- 可访问性、键盘、焦点、视觉回归、文本溢出、暗色模式、降级 UI 或用户信任状态变化。

## 默认读取

- `docs/roles/frontend.md`
- 当前主导 W 的 `00-main.md`
- `docs/02-standard-index.md` 中当前 W 和触发专项
- `docs/W4-build/00-main.md`
- `docs/W5-verify/00-main.md`
- 触发时读取 Vite 前端、可访问性/AI UX、外部 claim 或发布专项

## 固定输出

- UI 行为、状态、空/错/加载/降级路径说明。
- build、preview、Playwright、accessibility 或截图证据中适用项。
- 用户可见 copy、AI disclosure、反馈入口和信任边界风险。

## 交给总控 Agent 的情况

- UI 文案形成新的公开承诺或商业承诺。
- 交互需要后端/API/权限/计费/通知行为变化。
- 可访问性、AI UX 或用户信任门禁未通过。

## 必须问人的情况

- 发布强 claim、修改定价/权益/安全/隐私/AI 能力文案。
- 接受 WCAG、键盘、焦点、AI disclosure 或用户反馈入口例外。
- 面向真实客户发布未验证的关键 UI、计费路径或高影响 AI 界面。
