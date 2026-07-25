# 提案：默认启用 OpenSpec

## Why

将 OpenSpec 从“只有执行者主动判断有收益时才使用”的可选工具，改为 Standard 和 High-risk 实现性变更的默认规格与状态载体，避免复杂项目在早期决定跳过后不再复评，也让后续会话能直接恢复契约、设计和任务状态。

用户中心第二轮只在模板批次记录一次“不使用”决定，后续跨越稳定身份/API/数据契约和五轮审查后没有复评，因此无法评价 OpenSpec 的成本或收益。当前“只在有净收益时使用”的规则缺少可执行默认，执行者可以持续跳过该实验变量。用户于 2026-07-11 明确决定默认启用 OpenSpec。

## What Changes

- Quick 继续保持轻量，不默认创建 OpenSpec。
- Standard/High-risk 的代码、配置、schema、API、prompt/model、数据、基础设施和发布设计变更，在实现前创建或继续一个 OpenSpec change。
- 纯只读 review、报告、产品澄清、事故止血和不产生实现变更的操作不自动创建 change；一旦形成后续实现工作，再进入默认 OpenSpec 路径。
- 只有用户明确批准并记录理由时，Standard/High-risk 实现性变更才可跳过 OpenSpec。
- OpenSpec 链接权威产品输入、体验设计、验收证据和专项工件，不复制它们；`tasks.md` 承担执行状态，默认不再并行维护重复 work brief。
- 同步核心 router、Go/Vite 运行时技能、知识恢复材料和确定性 verifier。

## 不做什么

- 不要求 Quick 工作创建 proposal/design/tasks/spec 四件套。
- 不把 OpenSpec 格式通过当作产品完成、浏览器 E2E、独立审查或发布批准。
- 不要求新任务扫描全部历史 main specs 或 W0-W9。
- 不用 OpenSpec 替代人的产品决策、High-risk 实现前独立审查和最终独立审查。

## 需要人的判断

- 已确认：Standard/High-risk 实现性变更默认启用 OpenSpec。
- 以后对具体变更的跳过必须由用户明确批准，并保留理由；执行者不能自行把“已有文档很多”作为长期豁免。
