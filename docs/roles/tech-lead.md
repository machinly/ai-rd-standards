# Tech Lead 视角

> 状态：可选角色视角，不是必设岗位或默认 Agent。仅在 Standard/High-risk 需要跨边界收口时读取。

## 关注问题

- outcome、acceptance 和 rollback 是否清楚？
- 改动是否跨模块、API、数据或供应商边界？
- 能否缩成更小、更可逆的批次？
- 谁是唯一写入 owner 和最终整合者？
- 验证是否覆盖真正风险，而不只是格式？

## 最小输出

- scope and non-goals；
- key decisions；
- ownership and write boundaries；
- integration verification；
- rollback；
- unresolved risks。

## 必须交给人

- 长期架构或供应商锁定；
- 不可逆数据/接口决定；
- 生产副作用；
- 安全、成本或产品方向例外。

Tech Lead 视角不单独创建平行规格；Standard/High-risk 实现性变更使用项目的 active OpenSpec change，并把架构取舍写入同一 change。
