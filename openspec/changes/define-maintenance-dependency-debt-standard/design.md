# Design

## 工件形态

每个 target 使用五个轻量工件：

- `maintenance/dependency-inventory/<target>.json`
- `maintenance/update-policy/<target>.md`
- `maintenance/upgrade-plans/<target>.md`
- `maintenance/debt-register/<target>.jsonl`
- `maintenance/deprecation-plans/<target>.md`

JSON 用于机器检查，Markdown 用于人快速理解，JSONL 用于追加式技术债登记。

## 验证策略

`maintenance-dependency-debt-guard` 提供 `verify_maintenance_debt.py`：

- 检查 dependency inventory 必填字段、critical dependencies、manifest/lockfile/generated artifact 路径。
- 按 stack 检查 Go 与 npm/Vite 的最小安全扫描和 lockfile 纪律。
- 检查 update policy、upgrade plan、deprecation plan 必要章节。
- 检查 debt register JSONL 字段、日期、状态、linked change。
- 检查人审点覆盖 major upgrade、漏洞例外、fork/replace、breaking change、deprecation removal、AI 行为契约变化。
- 检查 secret、PII、raw prompt/response 不进入维护工件。

## 裁剪原则

- 一人公司默认月度 batch patch/minor，security 按风险加速，major 单独 OpenSpec change。
- 技术债只记录会影响未来修改、可靠性、安全、成本或 AI 行为的债。
- 弃用计划只用于会影响用户、数据、API、配置、AI 行为或外部消费者的 surface。
- verifier 只挡结构性风险，不替代人工判断“是否值得升级/删除”。
