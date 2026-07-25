# 后端视角

> 状态：可选角色视角，不是必设岗位或默认 Agent。仅在任务涉及服务端、API 或数据访问时读取。

## 关注问题

- 契约、错误语义和兼容性是否明确？
- 数据所有权、事务和幂等是否正确？
- 权限和租户过滤是否在服务端强制？
- 超时、重试、取消和外部依赖失败如何处理？
- 是否有足够测试、观测和回滚？

## 最小输出

- changed contracts and data paths；
- implementation summary；
- tests and verification；
- migration or compatibility risk；
- operational notes。

## 必须交给人

- breaking API；
- 生产迁移或删数；
- auth/tenant boundary 变化；
- 长期供应商或成本锁定。
