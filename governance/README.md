# 研发治理入口

本目录保存研发规范与具体项目的治理状态、批准和证据，不复制正式规范正文。

读取顺序：

1. 根 `README.md`：正式研发规范总入口。
2. `governance/project-map.json`：治理域、owner 与权威状态位置。
3. `governance/current-status.json`：唯一当前状态。
4. 仅在需要追溯时读取对应 domain 的批准、manifest、review 或报告。

## 当前治理域

- `rd-standards`：正式四分类十一项规范、完全覆盖证据与规则追溯账本。
- `rd-standards-rebuild`：本次重建的历史 gate、批准、来源基线与审查报告；完成替换后不再作为当前规范状态。

动态完成状态只写入 `current-status.json`。历史报告、OpenSpec tasks 或旧摘要不得覆盖更新的失败、`changes_requested`、撤销或失效证据。
