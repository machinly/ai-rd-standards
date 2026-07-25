# 用户中心第二轮试验：正式回灌记录

状态：formal ingestion implemented；独立最终审查待完成。
日期：2026-07-11
来源：`D:\Workspace\user\governance\user-center-service-pilot-2-review\`

## 来源指纹

| 文件 | SHA-256 |
| --- | --- |
| `README.md` | `7CD9C01A0654C9A710354E8BD290EBAA86D6A2FB086F36A41F37FD0026BC91EA` |
| `findings.md` | `D59C9994FEFBE3C595BABB6C3D3E9C9EC574E8B5A08B467DFBA83D949053B95A` |
| `standards-actions.md` | `79F22F8BC926FFFEB90666A33982DBF776AFB4B80EB2C758CABB9DFF1151F262` |
| `evidence-index.md` | `394B1A642BCAD397FFFDFDDF752255A1B2DFF1283F971FC5C864AB63D2D2DD48` |

来源文件保留完整观察、限制和项目证据索引；本仓库只保存去敏后的规范结论，不复制服务实现、凭据或个人数据。

补充发现的项目级记录：`D:\Workspace\user\experiments\rd-standard-pilot.jsonl`，SHA-256 为 `C26642795DFF0A2FBBBE7ADC368839D68A45E516B05C3443FF7457962B2D0849`，共 8 条 checkpoint。源项目没有随附 `rd-pilot-record.schema.json`；按本仓库当前 schema 校验时，8 条均缺少 `openspec` 对象，唯一 `completed` checkpoint 还缺少可比较核心指标。部分记录把 in-app 人工浏览器控制标成 `browser-e2e`，已被最终复盘的 UC2-02 否定。因此原始 8 条不直接复制为合格 pilot；本仓库只新增一条去敏汇总记录，诚实标记 `changes-requested`、`openspec.used=false`、manual browser evidence 和 0 eligible。

## 可采信事实

1. 第二轮有产品/体验验收、模板 provenance、完整本地环境、安全/数据/运维工件和多轮独立审查，但最新终审仍为 `changes_requested`。
2. 验证主要覆盖 Go 单元/集成、接口、数据库、CLI 和局部人工浏览器检查；没有可重复 Playwright/Cypress 套件证明关键页面旅程。
3. 人工浏览器局部检查被宽泛称为 Browser E2E，容易支持过强结论。
4. API、事务和安全检查没有发现部分实际按钮/页面路径不可用；review 轮数不能替代产品任务验收。
5. 较早验证摘要与最新 `changes_requested` 没有通过单一状态和失效规则自动收口。
6. guard 工件分散到多个顶层目录；项目缺少完整目录地图和统一阅读入口。
7. 多个 Go `cmd` 入口没有统一运行拓扑和命令注册表；复杂代码的业务/安全设计意图注释不足。
8. 治理工件数量增长快于基本产品闭环的验证，注意力排序失衡。
9. 第二轮没有实际使用 OpenSpec，因此不能评价 OpenSpec 的净收益；用户随后已单独决定 Standard/High-risk 实现默认启用 OpenSpec。

## 正式处置

| 发现 | 正式处置 |
| --- | --- |
| UC2-01 / UC2-05 | 用户可见 Standard/High-risk 工作新增关键旅程矩阵，并尽早关闭一条真实浏览器闭环。 |
| UC2-02 | Browser E2E 采用可重复自动化、真实页面动作、业务状态断言、失败 artifacts 和干净完整环境的最低证据契约。 |
| UC2-03 | 独立终审增加陌生验收者执行关键用户旅程的产品视角；review 轮数不作为质量指标。 |
| UC2-04 | 项目维护单一当前状态；较新的 `changes_requested`、失败旅程或失效 manifest 否决旧完成摘要。 |
| UC2-06 / UC2-07 | guard 工件统一进入 `governance/<registered-domain>/`，并要求 governance README/project map。 |
| UC2-08 | 高风险复杂逻辑必须在代码附近解释设计意图，不设置注释覆盖率。 |
| UC2-09 | 多个 Go `cmd` 必须有 command registry，覆盖环境、生命周期、权限、写入、恢复和停用。 |
| UC2-10 | 实验先建立产品输入、最小旅程、完整本地环境和浏览器闭环，再按风险增加治理域；每个域登记可观察用途。 |
| UC2-11 | 已由 `decisions/2026-07-11-default-enable-openspec.md` 处置；试点 schema 同时强制记录 `openspec.used`、change id、跳过批准和原因。没有批准的 `used=false` 可保留为负面证据，但不得计入 eligible，不再用格式失败把真实遗漏排除在证据之外。 |

实现 change：`openspec/changes/archive/2026-07-11-ingest-user-center-pilot-2-review`。

## 服务处置边界

- 不修复、恢复、发布或继续评价用户中心实现。
- 不把本回灌记录当作用户中心交付证据。
- 不从构建、接口测试、结构 verifier 或 review 次数推导产品完成。
- 当前证据只适用于本地合成实验，不支持生产就绪结论。

## 尚未证明

- 新门禁尚未在第三个真实项目中运行，不能证明降低了总注意力或返工。
- OpenSpec 默认启用尚无真实对照数据。
- 统一 governance 目录和新增 verifier 的可用性仍需后续 pilot 验证。
- 本次整改的独立最终审查仍为 pending；生产者自检不能接受自己。
