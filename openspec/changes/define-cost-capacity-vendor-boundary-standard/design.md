# 设计：成本、容量与供应商边界规范

## 设计决策

### 1. 用三个必需工件表达成本容量边界

`cost/budgets` 记录预算、单位指标、用量驱动、限额和降级；`cost/vendors` 记录供应商依赖、锁定和退出；`cost/runbooks` 记录超支、过载和供应商故障动作。这样一个人可以恢复上下文，脚本也能检查缺项。

### 2. 默认内部预算，不硬编码外部价格

OpenAI、云厂商和 SaaS 价格会变化。预算 artifact 只记录内部可承受预算、限制和动作；外部价格只作为复审时查证来源，不作为长期固定事实。

### 3. AI workflow 必须有 token/request/tool 上限

一人公司最容易失控的是 autonomous agent、批量任务和重试风暴。用户可见 AI workflow 默认需要 `ai_max_tokens_per_task`、`ai_max_tool_iterations` 和 per-user/per-day 或等价限制。

### 4. 先降级，再失败

参考 Google SRE 的 overload 思路，过载时先减少工作量：缓存、较小模型、排队、关闭非核心 workflow、提前拒绝。降级路径必须可测试。

### 5. 单供应商可以接受，但必须可解释

早期强行多云会增加维护成本。W2 cost/capacity 专项接受托管服务和单供应商，但要求 critical path 记录 fallback、exit trigger、数据格式和人工迁移成本。

### 6. 只升级高影响支出决策

预算上调、取消硬限制、承诺消费、高价优先处理、关键供应商无 fallback、发送用户数据给新供应商，都需要人工 checkpoint。普通阈值文案和 artifact 格式由规范默认处理。

## 取舍

- JSON 工件增加少量书写成本，但能阻止没有预算和硬限制的生产上线。
- 不强制实时云账单接入，降低早期复杂度；真实账单上线后通过 `cost/usage` 月度记录。
- 不默认多云，避免为低概率迁移支付高维护成本。
- 不把成本优化变成只追求低价；每次优化必须保留用户体验、可靠性和安全边界。
