---
decision_id: rd-standards-reset-2026-07-10
decision: accept-external-remediation-and-minimal-risk-router
approved_by: user
approved_at: 2026-07-10
conditions:
  - do-not-use-existing-w0-w9-as-the-review-authority
  - do-not-claim-process-effectiveness-without-real-pilot-data
  - do-not-treat-producer-self-check-as-independent-acceptance
revisit_on: after-10-eligible-pilot-records-or-any-high-risk-miss
---

# 研发规范重置决策记录

日期：2026-07-10
状态：accepted for implementation
决策人：用户
执行范围：当前研发规范仓库

## 用户指令

- 根据 reviews/2026-07-10-rd-standards-review.md 对整个项目整改。
- 整改期间不需要遵循现有研发规范。
- 以超越现有规范的外部视角处理。

## 解释

本记录只证明用户授权进行项目整改和外部 meta-review，不代表用户已经接受：

- 原 L0/L1 为正式政策；
- A0-A4 或 M0-M4 自主等级；
- OpenSpec 为默认规格工具；
- 无人值守生产动作；
- 删除、付款、外部通信或凭据操作。

## 已采纳方向

- 最小研发内核成为默认入口；
- Quick / Standard / High-risk 取代强制 W0-W9 路由；
- W0-W9、OpenSpec、角色和多 Agent 文档降为可选 playbook；
- 人持续拥有产品判断、价值边界和最终问责；
- Standard 和 High-risk 使用独立最终 reviewer；
- 真实任务数据决定流程保留、删减和自动化。

## 后续明确裁决

以下决定由用户在同一整改会话中明确补充，属于当前全局默认：

- 新应用必须通过批准、可版本化的模板生成，不手工拼装。当前 Go 服务使用 Kratos CLI；未来发布自有应用模板后改用自有模板。
- 多组件项目必须有统一、完整、可重复的本地集成环境，真实覆盖全部后端、前端和必要依赖；前端可以运行在宿主机，不强制容器化。
- 数据库默认优先 MySQL + sqlc；SQL 尽量采用 MySQL/PostgreSQL 通用语法。
- 默认不创建 foreign key；应用校验、事务、幂等、唯一/非空约束、删除策略、补偿和孤儿数据扫描承担完整性。
- 已终止的用户服务后来已删除，不恢复、不继续评价，只回灌对研发规范的验证事实。

## 回退

如果新入口阻碍真实工作，可恢复上一个 git 版本；历史 playbook 暂不删除，直到合格对照试验提供证据。达到 10 条合格 pilot 记录或再次发生高风险漏检时，重新审查本决策和保留规则。
