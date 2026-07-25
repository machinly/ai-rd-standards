# OpenSpec 资产说明

状态：Standard/High-risk 实现性变更的默认规格工作区；Quick 不使用。

当前默认规则在：

- README.md
- docs/01-initiation/README.md
- docs/02-product-design/README.md
- docs/03-engineering-delivery/README.md
- docs/04-operations-maintenance/README.md

## 当前状态

- active changes：以 `openspec list` 实时结果为准；
- archived changes：历史 change 持续累积，目录数量不是治理完成门禁；
- main specs：56，均在文件内标为可选历史主题规格；
- 归档决策：openspec/ARCHIVE-DECISION-2026-07-10.md。

## 默认使用边界

- Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施和发布设计变更，在实现前创建或继续 change；
- Quick、只读 review、报告、产品澄清和事故止血不自动创建；
- 只有用户明确批准并记录 owner、理由、范围和恢复方式时，具体实现变更才可跳过；
- 任务时长本身不触发 OpenSpec，风险路径和变更性质才触发。

## 解释历史 specs

`openspec/specs/` 保留历史主题规格作为来源与决策记录，不是当前研发规范入口，也不覆盖四分类十一项正式正文。历史文件中的旧路径仅用于解释当时上下文，不应作为当前路由。

OpenSpec 只写本次 change 的增量并链接权威输入。`tasks.md` 承担执行状态，默认不另建内容重复的 work brief。格式验证不替代真实验收和独立审查。
