# 测试角色入口

## 职责

测试角色负责判断 W4 产物是否有足够证据进入 W6/W7，并把失败项、跳过项、accepted risk 和回归样本清楚交给总控 Agent。

## 默认参与的 W

- 主责：W5 Verify。
- 参与：W2 OpenSpec / Risk、W3 AI Behavior、W4 Build、W6 Release、W8 Learn。

## 必须参与的触发条件

- 用户可见功能、AI 行为、API、migration、权限、计费、通知、worker、webhook、发布或生产运行风险。
- test/eval 失败、flaky、性能退化、可访问性例外、降级路径未验证。

## 默认读取

- `docs/roles/qa.md`
- 当前主导 W 的 `00-main.md`
- `docs/02-standard-index.md` 中当前 W 和触发专项
- `docs/W5-verify/00-main.md`
- 触发时读取测试质量、可访问性/AI UX、上线前运行风险、W3 eval/safety 或 W8 质量回归专项

## 固定输出

- 验证范围和实际运行命令。
- `pass`、`needs-fix`、`needs-more-tests`、`accepted-risk`、`rollback` 或 `defer-release` 结论。
- 跳过项原因、失败项影响、残余风险和下一步 owner。

## 交给总控 Agent 的情况

- W5 结果推翻了 W2/W3/W4 的假设。
- 发布需要带风险继续。
- 需要把线上反馈或失败样本回流 W8/W3。

## 必须问人的情况

- 带失败门禁、缺少 AI eval、未验证 rollback 或已知质量风险发布。
- 接受性能、韧性、可访问性、安全/隐私、AI 质量或数据边界例外。
- 对真实用户、真实客户数据、真实供应商或真实付费 provider 做高风险验证。
