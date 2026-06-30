# W3 触发专项：AI eval、数据、红队与内容安全规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项，不是 W3 主入口。只有当当前 AI capability 需要 eval 数据来源、标注口径、红队/对抗样本、内容安全、moderation、用户通知/申诉或 safety release review 时，才读取本文件。

普通 W3 工作先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

把 AI 数据集、红队和内容安全合并成一个 AI safety gate：样本从哪里来、什么算通过、怎样滥用、哪些内容要阻断或复核，发布前哪些失败会阻塞。

默认原则：没有 provenance、rubric、失败样例、安全样例和 release decision，就不能把 AI 行为变化当作已验证。

## 主要角色消费者

- QA：用它组织 AI release gate。
- 安全合规：判断滥用、moderation、敏感内容和未缓解发现。
- 产品/运营：连接用户投诉、申诉、信任请求和 W8 学习。

## 最小工件

按触发选择：

```text
ai-data/
  dataset-card/<dataset>.md
  eval-set/<dataset>.jsonl
  labeling-guide/<dataset>.md
  quality-report/<dataset>.json

ai-safety/
  abuse-case-register/<capability>.json
  adversarial-cases/<capability>.jsonl
  mitigation-map/<capability>.md
  safety-release-review/<capability>.md

content-safety/
  policy/<surface>.md
  moderation-rules/<surface>.json
  enforcement-runbook/<surface>.md
  notice-appeal/<surface>.md
```

## 必须覆盖

- eval set 至少包含 happy path、边界/失败、对抗或注入样例。
- release gate 只使用 `ready` 且属于 eval/canary/red_team 的样本。
- 真实用户数据、raw prompt/response、客户内容或公开数据必须记录 license/consent、隐私分类和用途。
- high/critical abuse case 必须有 mitigation、owner、eval ref 和 release decision。
- 自动化 enforcement 超过 label/review 时必须有 notice、appeal、audit 和复盘样本。

## 默认规则

- 模型可辅助初标，但不能直接成为 ground truth。
- 红队发现先进入 `ai-safety/`，高价值发现再转成稳定 eval case。
- 不保存完整可直接滥用 payload；优先保存 redacted/synthetic proxy 和 finding id。
- 内容审核不是一个分类器调用；policy、rules、runbook、notice/appeal 和 review 要一起生效。
- 安全失败不能被平均分掩盖；critical 默认阻塞发布，high 默认阻塞或需要明确 accepted risk。

## 需要人判断

- 使用真实/敏感/高影响数据，或将 eval case 移入训练、微调、蒸馏。
- 删除、retire 或降权当前失败样本，改变 rubric、grader、threshold 或 safety boundary。
- 带未缓解 high/critical finding 发布，或接受 `ship-with-risk-acceptance`。
- 改 moderation threshold、policy boundary、enforcement action 或申诉拒绝路径。
- 保存或公开真实攻击 payload、高危内容、红队结果、系统提示细节或供应商弱点。

## Review A：一人可执行性

本专项把 W3 的 AI 质量、安全和内容审核收成一个 gate，减少角色 Agent 需要读的文件。一个人可以先建 20-50 条 eval/red-team/content-safety 样本，再逐步补全。

## Review B：产品 / 工程 / 运维风险

保留了数据来源、train/eval 分离、红队、mitigation、moderation、notice/appeal 和发布阻塞规则。最小安全下一步是让每个 AI 行为 change 都链接 eval version 和 safety release decision。

