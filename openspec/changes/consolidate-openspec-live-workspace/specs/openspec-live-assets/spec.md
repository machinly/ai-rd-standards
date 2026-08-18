## ADDED Requirements

### Requirement: OpenSpec 只保留当前 active 资产

本仓库 MUST 将正式研发规范保留在 canonical `README.md + docs/`，并将 `openspec/` 限定为项目配置、当前说明和真实 active changes。仓库级历史 base specs、completed-change archive 与旧 archive 决策 MUST NOT 留在当前工作区。

#### Scenario: 验证正式 UX 规则

- **WHEN** 当前规范测试核对 viewport、主题、页面 review 或 Browser E2E 边界
- **THEN** 测试只读取 canonical `docs/`
- **AND** 不要求 OpenSpec specs 复制同一规则

#### Scenario: 资产只提供历史追溯

- **WHEN** spec、archive、决策或固定快照工具没有当前 live consumer
- **THEN** 从当前工作区删除
- **AND** 需要恢复时使用 Git 历史

#### Scenario: 验证器仍防止当前错误结论

- **WHEN** 验证器仍有正式入口、active change、当前方案或可复用证据门禁
- **THEN** 保留验证器及其回归测试
- **AND** 不因当前数据不足而把验证器误判为历史工具
