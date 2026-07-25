# 设计：OpenSpec 默认启用边界

## 默认路由

| 路径/工作 | OpenSpec 默认 |
| --- | --- |
| Quick | 不创建 |
| Standard 实现性变更 | 创建或继续 change |
| High-risk 实现性变更 | 创建或继续 change，并保留风险、批准、回滚和独立审查 |
| 纯产品澄清、只读 review、报告 | 不自动创建；若产出后续实现变更则创建 |
| 事故止血或一次性运行操作 | 不因操作本身创建；后续修复/设计变更创建 |
| 用户明确豁免 | 记录 owner、理由、适用范围和恢复方式后跳过 |

## 单一事实来源

- 产品输入与体验设计继续是“做什么、为谁做、如何验收”的权威来源。
- OpenSpec `proposal.md` 记录本次 change 的意图、范围和非目标，只链接产品输入。
- delta spec 记录发生变化的可验证行为和 scenario。
- `design.md` 只记录本次 change 必须锁定的架构、数据、安全或回滚取舍。
- `tasks.md` 是实现状态与验证清单；默认不另建内容重复的 work brief。
- review、测试、浏览器 E2E 和运行证据保留自己的原始文件，并从 tasks/最终总结链接。

## 生命周期

1. 路由为 Standard/High-risk 实现性变更后，先创建或选择 active change。
2. 在生产性实现前完成 proposal、适用 delta spec、必要 design 和可执行 tasks，并运行 `openspec validate <change> --strict`。
3. High-risk 的 auth/data/admin/irreversible 设计先做独立审查；OpenSpec validation 不能替代该审查。
4. 实现中持续勾选 tasks、记录真实验证与偏离，不在聊天或平行 brief 维护另一套状态。
5. 实现完成后做 producer self-check 和独立终审；只有证据与结论一致时归档 change。

## 运行时同步

核心 router 是 canonical 规则；本机安装副本必须逐文件同步。Go service 和 Vite frontend skill 也必须使用相同的 Quick 豁免与 Standard/High-risk 默认规则，不能再按任务时长或执行者主观净收益决定是否创建 change。

## 风险与缓解

- 风险：Standard 工作产生过多重复文字。缓解：OpenSpec 取代重复 work brief，proposal/design 只写 change delta。
- 风险：执行者为规避流程把任务错误标成 Quick。缓解：仍按影响、可逆性和问责性分流，用户可见、跨会话或独立验收工作不能因想跳过 OpenSpec 降级。
- 风险：形式校验再次掩盖产品失败。缓解：completion 继续要求 acceptance 映射、真实用户旅程、准确证据层级和独立审查。
- 风险：紧急操作被规格流程阻塞。缓解：事故止血/一次性操作不自动创建；稳定修复和后续预防变更再创建。

