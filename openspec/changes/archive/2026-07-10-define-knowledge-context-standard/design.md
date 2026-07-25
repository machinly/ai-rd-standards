# 设计：知识管理、文档与上下文恢复规范

## 设计决策

### 1. 用 docs map 做 canonical 入口

文档散落比文档缺失更危险。`docs-map` 用 JSON 记录 canonical entrypoints、audience、type、owner、review_on 和 stale_after_days，让脚本能检查路径和过期风险。

### 2. Context pack 专门服务接手

README、OpenSpec、ADR、runbook 各有职责。Context pack 只回答“现在是什么、边界是什么、怎么继续”，并链接 canonical artifacts，不复制所有内容。

### 3. Diátaxis 裁剪，不照搬

一人公司早期不需要完整文档门户。默认必须有 how-to 和 context pack；reference/explanation 通过已有 OpenSpec、API、config、ADR、SLO 等链接补足；tutorial 仅在真实 onboarding 需要时创建。

### 4. Freshness log 只记录重要复审

每次小改都更新 freshness 会变成噪音。只在 release、incident、security/data/AI/config 高风险变更、product pivot 后追加记录。

### 5. Codex 读取顺序固定

为了保护人的注意力，Codex 接手 target 时先读 docs map 和 context pack，再读当前 OpenSpec 和相关 artifacts，避免每次从全仓库搜索开始。

## 取舍

- 增加少量知识入口文件，但降低中断恢复和 AI 接手成本。
- 不默认 wiki，避免外部系统漂移。
- 不强制 tutorial，避免为不存在的读者写文档。
- 脚本只能检查路径、结构和明显敏感内容，不能判断文档质量；两轮 review 负责可用性判断。
