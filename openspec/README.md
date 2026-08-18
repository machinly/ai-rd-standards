# OpenSpec 当前资产

本目录是 Standard/High-risk 实现性变更的规格工作区。正式研发规范入口仍是根 `README.md` 与 `docs/`；这里不复制整套正式正文。

## 当前保留内容

- `config.yaml`：OpenSpec 项目配置。
- `changes/<change-id>/`：仍有未完成任务、待审查或待最终处置的 active changes；实时状态以 `openspec list` 为准。

仓库级 base specs、completed-change archive 和旧 archive 决策均不再保留；正式规则只从 canonical `README.md + docs/` 读取。如需恢复已删除内容，使用 Git 历史。

## 使用边界

- Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施和发布设计变更，在实现前创建或继续 change。
- Quick、轻量 Explore、只读 review、报告、产品澄清和事故止血不自动创建。
- proposal、specs、design 与 tasks 只记录本 change 的增量并链接权威输入；`tasks.md` 承担执行状态。
- `openspec validate --all --strict --no-interactive` 只证明 active changes 格式有效，不替代真实验收、独立审查或发布批准。
