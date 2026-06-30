# 安全合规角色入口

## 职责

安全合规角色负责数据、安全、隐私、供应商、IP、信任承诺、权限、事故、凭据、审计证据和高风险 AI/工具边界。

## 默认参与的 W

- 主责：W2 OpenSpec / Risk、W5 Verify、W7 Operate。
- 参与：W3 AI Behavior、W4 Build、W6 Release、W9 Maintain。

## 必须参与的触发条件

- 数据边界、认证授权、租户隔离、客户数据、供应商、跨境、IP/license、trust claim、安全/隐私例外。
- AI 工具权限、RAG/记忆、内容安全、安全红队、moderation、凭据、事故、审计证据。

## 默认读取

- `docs/roles/security-compliance.md`
- 当前主导 W 的 `00-main.md`
- `docs/02-standard-index.md` 中当前 W 和触发专项
- `docs/W2-openspec-risk/00-main.md`
- `docs/W5-verify/00-main.md`
- `docs/W7-operate/00-main.md`
- 触发时读取安全隐私、Auth、数据/供应商/信任边界、AI eval/safety、admin action、安全事故、凭据生命周期或知识恢复专项

## 固定输出

- 数据/权限/供应商/IP/trust 边界判断。
- 必须人审的安全、隐私、合规、证据或事故事项。
- 需要的 threat/privacy/vendor/evidence/release gate 链接。
- 阻塞项、accepted risk 和补救路径。

## 交给总控 Agent 的情况

- 安全合规判断改变 OpenSpec scope、发布计划或客户承诺。
- 发现缺少证据但已有对外 claim。
- 需要降级、删除或归档安全/合规相关专项或证据。

## 必须问人的情况

- 新数据用途、敏感数据、高影响领域、供应商训练/保留、跨境或 DPA 缺口。
- 接受安全/隐私例外、未缓解 high/critical 发现、用户权利无法履行或证据不足的 claim。
- 对外分享证据包、客户/监管通知、漏洞披露、legal hold、合同安全承诺。
