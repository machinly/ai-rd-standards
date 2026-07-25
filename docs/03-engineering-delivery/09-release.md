# 发布

> 正文中的稳定 rule-id 可通过[覆盖矩阵](../../governance/rd-standards/review/coverage-matrix.csv)追溯到原子规则和来源。

## 项目目的与边界

发布把已经形成的产品、实现与验证结论安全地送入真实环境、指定客户或外部表述面，并在动作发生后确认结果。它负责 go/no-go、部署方式、暴露范围、上线凭据、恢复准备、发布观察与交接；不在临发布时补做产品定义、实现或验证，也不替代合同、数据、安全或 AI 行为的上游边界判断。

## 根本原则

- **ITEM-RELEASE-001**：发布默认应小批量且可回滚。

## 核心判断

- 进入真实环境、客户租户或外部表述面之前，依赖的实现、验证和边界证据是否仍然有效？
- 本次决定是发布、延后、灰度、限定受众、回滚还是停止；谁需要作出不可自动化的判断？
- 将部署哪个不可变产物，采用什么 rollout，出现什么信号必须停止、关闭或回退？
- 客户上线、外部 claim、商业义务或生产数据动作是否触发各自的附加门禁？
- 发布完成后，运行、支持、质量评估和更正责任交给哪里？

## 重新组织后的规范要求

### 范围、返回与按需加载

<!-- rule-id: RELEASE-SCOPE-001 -->
#### 进入发布项

当已验证的变更准备进入 production、preview/staging 的晋级路径、真实客户租户、公开 release、外部 claim 或合同承诺时，必须进入发布判断。这里同时覆盖流水线与产物、客户试点或 go-live、外部表述以及商业义务；发现工作、实现工作和验证工作本身不由本项接管。

<!-- rule-id: RELEASE-SCOPE-002 -->
#### 前置条件失效时返回上游

发布中发现缺口时不得临场补洞：价值判断或优先级变化返回[选题](../01-initiation/01-topic-selection.md)，产品发现、访谈或实验设计不足返回[调研](../01-initiation/02-research.md)，用户可见产品或 AI 行为边界不足返回[定义](../02-product-design/03-definition.md)，交互感知不足返回[体验设计](../02-product-design/04-experience-design.md)，风险、契约、合同、信任边界或 prompt/eval 等 AI 技术方案不成立返回[技术设计](05-technical-design.md)，代码缺口返回[实现](07-implementation.md)，证明不足返回[验证](08-verification.md)。只有前置结论重新成立后才能恢复发布。

<!-- rule-id: RELEASE-SCOPE-003 -->
#### 只加载被触发的发布细则

基础发布判断默认保持轻量。涉及 CI/CD、release artifact、环境晋级、smoke、rollback、部署身份或 provenance 时使用流水线细则；涉及 design partner、private beta、paid pilot、租户数据、SSO/SCIM、live billing 或客户验收时使用客户上线细则；涉及官网、pricing、文档、AI disclosure、trust/security/privacy 或销售支持表述时使用 claim 细则。未命中的专项不得变成每次交付的固定仪式；项目已有更严格且获准的基线时，以该基线为下限。

<!-- rule-id: RELEASE-DECISION-001 -->
#### 记录唯一的发布决定

每次发布工作必须明确记录一个主决定；允许值为 `发布`、`不发布`、`延后`、`回滚`、`灰度`、`仅 preview`、`仅客户试点` 或 `仅内部上线`。附加条件、受众和残余风险另行记录，不能用模糊的“基本可以”代替主决定。

### 准入证据与人工判断

<!-- rule-id: RELEASE-GATE-001 -->
#### 用可复核事实支持 go/no-go

发布依据至少包括当前 test matrix 中的 release gate、最近一次对应 gate run，以及适用的运行风险 go/no-go 结论。实验结果只有在隐私边界与可信度检查均成立时才能影响发布；发布清单必须链接这些证据，不能以感觉或旧结论替代。

<!-- rule-id: RELEASE-GATE-002 -->
#### 显式承接验证债务

失败测试、跳过的 race/sqlc/eval、缺少 AI eval 或回滚证据、已知 flaky，以及高影响场景中的资金、权限、隐私、安全、计费、通知、SLA、公共 API 或 AI 质量风险，都不得被静默带入发布。确需继续时必须记录 accepted risk、影响范围、决定人和后续动作；flaky 测试不得通过长期移出 release gate 来制造通过结果。

<!-- rule-id: RELEASE-GATE-003 -->
#### 设置生产与高风险人工 checkpoint

以下决定必须由人确认：是否进入 production；首次或高风险 release；是否让 CI 自动执行 migration、生产数据操作、真实付款、真实通知、真实 webhook 或客户上线；是否允许自动回滚或自动关闭能力；以及涉及资金、权限、隐私、安全、合规或 AI 外部副作用的发布。需要律师、隐私/安全顾问、客户或开发者通知、公开更正或合同变更时，也必须明确责任人与动作，而不能由流水线自行推断。

<!-- rule-id: RELEASE-GATE-004 -->
#### 保留低风险自动化例外

workflow/job 命名、release 文件命名、JSON 字段顺序或标准合同字段顺序、smoke 文案、preview 与 staging 的称呼、没有强承诺的 typo 或低风险 release note，无需逐项人工判断；普通小改可以自动进入 preview/staging。该例外不延伸到 production：生产发布不得因合并到 `main` 而静默发生。

### 产物、发布身份与证据

<!-- rule-id: RELEASE-ARTIFACT-001 -->
#### 只部署 CI 构建的不可变产物

production deploy 可以从本地触发，但待部署产物必须由 CI 构建并保持不可变；不得从开发机直接制作或修改线上 release。回滚应重新部署已知的上一 release，而不是就地篡改正在运行的产物。首版先为一个服务建立最小可重复路径，不以平台抽象为前置条件。

<!-- rule-id: RELEASE-ARTIFACT-002 -->
#### 建立可追溯的 release identity

每个 production release 必须有唯一 `release_id`，并至少纳入 `commit SHA` 或 `image digest` 之一。`main` 只表示候选可发布，不表示已进入生产；production 必须通过显式 trigger、tag、environment protection 或已验证的 preview promote 才能发生。

<!-- rule-id: RELEASE-ARTIFACT-003 -->
#### 分离 build、release 与 run

`build` 只负责从 revision 产出不可变 artifact，`release` 负责选定该 artifact、目标环境、gate 结论和 `release_id`，`run` 负责记录一次实际部署及其结果。三者用 artifact digest、`release_id` 和 run record 相互链接，但不得共用一个可覆写状态代替：build 成功不等于已经批准 release，release 获准也不等于 run 已成功。

<!-- rule-id: RELEASE-EVIDENCE-001 -->
#### 保存发布证据摘要

摘要必须同时给出主决定、`release_id`、commit 或 artifact 引用、目标环境、gate 结论、smoke 结果、rollback 路径、watch plan 与残余风险。AI change 在实现任务结束后还要更新 release note。准备交给运行阶段前，上述字段均须明确，且验证失败、accepted risk 和 skip 已被本次决定逐项承接。

<!-- rule-id: RELEASE-EVIDENCE-002 -->
#### 保存实际 release run 记录

每次 run 记录 `release_id`、`commit SHA`、artifact digest 或 deployment URL、OpenSpec change id、各 gate 结果、部署时间与环境、smoke 结果、观察到的 SLO/错误信号，以及是否回滚或下一动作。发布总日志还应保留 commit、artifact digest、最终结果和可执行的回退方式，不能只记录“已部署”。

### 发布流水线合同

<!-- rule-id: RELEASE-PIPELINE-001 -->
#### 推荐最小工件落点

没有获准的等价仓库约定时，推荐每个服务以 `release/pipelines/<service>.json` 描述流水线、以 `release/smoke/<service>.md` 和 `release/rollback/<service>.md` 保存 smoke 与回退方法；执行记录放入 `release/runs/`，文件名采用 `YYYY-MM-DD-<service>-<release-id>.md`。采用其他落点时必须从发布清单提供可解析链接。生产服务必须链接 `ops/release/<service>-checklist.md`；smoke 与 rollback 字段仍必须指向可读文件。首版默认只维护当前服务所需的一组工件，不预建发布平台。

<!-- rule-id: RELEASE-PIPELINE-002 -->
#### 让 OpenSpec 状态进入发布门禁

适用的 change 必须能定位 proposal、spec、design 与 tasks；未完成事项要明确完成或延后，不能从证据中消失。公开仓库或官方 SDK 的发布应使用独立 OpenSpec change。流水线至少保留 OpenSpec 类 gate，并在发布前确认 tasks 已完成或有明确延后结论。

<!-- rule-id: RELEASE-PIPELINE-003 -->
#### 维持一人可执行的流水线边界

GitHub Actions 是默认 provider，而不是绑定；使用其他 CI 时记录替代 provider 和等价 gate。普通小改可以自动部署到非生产环境，首次或高风险 production 仍保留 checkpoint。Terraform 平台、Kubernetes GitOps、复杂多环境审批矩阵、企业发布列车或完整供应链合规，只有真实规模或合规要求出现后才另开 change；实际云 provider 的细节写入对应部署 change。

<!-- rule-id: RELEASE-PIPELINE-004 -->
#### 维护可判定的 pipeline schema

默认 schema 推荐描述 `service`、`owner`、`trigger`、`environments` 和 `ci`，其中 `ci` 推荐记录 `provider` 与 `workflow`；`gates[]` 推荐用 `name`、`required`、`command` 表达判定。部署段推荐记录 `strategy`、`canary`、`production_checkpoint` 与 `rollback`，发布观察推荐使用 `post_deploy_watch.duration_minutes` 和 `post_deploy_watch.signals`，产物来源策略推荐使用 `provenance.required` 与 `provenance.policy`。项目可使用等价 schema，但最低 gate、可读 smoke/rollback 文件和生产 checklist 链接仍按各自规则强制执行；字段顺序不构成门禁。

<!-- rule-id: RELEASE-PIPELINE-005 -->
#### 声明最低 gate 类别与等价命令

流水线必须包含 OpenSpec、test、smoke 与 rollback 类动作；使用非默认 CI 时仍须提供语义等价的 gate。发布 Protobuf 契约时，把 `buf lint`、`buf breaking` 或作用等价的检查纳入 CI/release gate。命令不可执行、被跳过或结果过期时，按验证债务规则处理，不能把 gate 名称本身当作通过证据。

<!-- rule-id: RELEASE-PIPELINE-006 -->
#### 固定默认 gate 顺序与失败处理

默认按“规范与生成差异检查 → test/eval/migration 风险检查 → build 与 security → 非生产部署 → smoke → production checkpoint 与部署 → post-deploy watch → release log”执行适用步骤；不适用项要记录理由而不是伪造通过。任一 `required=true` gate 为 `fail`、`blocked`、未执行或结果过期时，停止后续晋级；只有完成重跑，或由有权的人按 accepted risk 合同承接后，才能产生新的 go/no-go 决定。下游结果依赖的 revision、artifact 或配置变化后，旧 gate 结果不得继续复用。

<!-- rule-id: RELEASE-PIPELINE-007 -->
#### 按变更栈整合发布门禁

流水线按实际变更组合门禁：Go/Kratos/sqlc/gRPC 连接测试、race、生成差异、sqlc 与契约检查；Vite 连接锁文件安装、测试、production build 与 preview；用户可见 AI 连接 ready 样本、eval、高风险输入运行、版本与 fallback；SRE-lite 连接 release checklist、smoke、observability 与 rollback。每项都链接本文件对应细则与实际结果，未触发的栈不强行加入空 gate。

<!-- rule-id: RELEASE-PIPELINE-008 -->
#### 暴露发布 skill 与本地检查入口

仓库提供发布流水线 skill 或本地检查脚本时，pipeline 或 release checklist 必须写明入口、适用服务、所用 revision/版本和结果落点；本地检查只作为可重复 preflight，不能替代 CI 中的 required gate。仓库未提供这类入口时，直接记录可执行的等价命令，不创建虚假的 skill、脚本或通过记录。

## 按主题整理的执行细则

### 后端与前端发布

<!-- rule-id: RELEASE-BACKEND-001 -->
#### Go 与 sqlc gate

发布 Go 服务时运行 `go test ./...`。关键并发路径或发布前周期还要运行 `go test -race ./...`；若全量执行耗时过高，至少放入 nightly 或高风险 change。使用 sqlc 时运行 `sqlc vet`，并确认 `sqlc generate` 后没有未提交差异。

<!-- rule-id: RELEASE-BACKEND-002 -->
#### 收紧 production runtime image

Go 服务的生产镜像使用 multi-stage build；最终 runtime image 不得包含 Go SDK 或源码。构建 gate 应检查最终层，而不是只检查 Dockerfile 声明。

<!-- rule-id: RELEASE-FRONTEND-001 -->
#### Vite 构建与 preview 检查

依赖安装使用 `npm ci` 或能证明 lockfile 一致的等价方式，并运行 Vitest。preview 环境必须能访问关键页面，且要有 Web Vitals 或平台 speed/observability 的采集计划。`vite preview` 只能用于预览验证，不能充当 production server。

<!-- rule-id: RELEASE-FRONTEND-002 -->
#### Vercel 环境与追溯

使用 Vercel 时分离 Preview 与 Production。production 可由 Git、CLI、Deploy Hook 或 API 触发，但每次部署必须同时追溯到 commit 和 deployment URL；缺少任一引用时不得把该部署记为已确认 release。

### AI release gate

<!-- rule-id: RELEASE-AI-001 -->
#### 固定 AI 产物、版本与 eval 证据

用户可见 AI 能力发布前，`ai/prompts/<capability>/` 下必须存在 `prompt.md`、`cases.jsonl`、`rubric.md` 与 `runbook.md`。release gate 只接受状态为 `ready` 的样本；相关 eval 必须通过，或留下明确的失败接受理由。高风险输入必须实际运行 fuzz 或对抗样例中的至少一种，并在 release run 中记录命令或样例引用及结果；未运行或失败时只能作为未通过 gate 处理，并留下明确的 accepted risk、决定人与后续动作。model、prompt version 与 schema version 写入配置或 release log，prompt/schema 版本也必须进入可追溯 artifact 或配置。

<!-- rule-id: RELEASE-AI-002 -->
#### 不用平均分掩盖安全失败

critical 安全失败默认阻断发布；high 失败默认同样阻断，除非有明确 accepted risk。任何带未缓解 high/critical finding 的上线，或 `ship-with-risk-acceptance` 结论，都必须由人确认并记录风险承接，不能被总体均分抵消。

<!-- rule-id: RELEASE-AI-003 -->
#### 检查 AI 工具与降级路径

工具型 AI 发布前检查 tool 权限；结构化输出检查 parse failure；所有用户可见 AI 都要验证 fallback 或 disable switch。能力涉及金钱、权限、通知、删除、隐私或高风险建议时，production checkpoint 必须由人完成。

### 部署身份与供应链

<!-- rule-id: RELEASE-SUPPLY-001 -->
#### 优先短期部署身份

云部署优先 OIDC 短期凭证，并让 release token 保持最小权限。无法使用 OIDC 时，长期 secret 只能存放在 CI secret store 且必须最小权限。新增长期生产 key、跨环境或跨租户共享 credential、第三方可读 secret，以及外部 action/deploy identity，均需人工判断后才能进入发布配置。

<!-- rule-id: RELEASE-SUPPLY-002 -->
#### 为外部分发产物提供来源证据

二进制、包或镜像将由外部用户运行时，逐步启用 artifact attestation、image digest 与 SBOM，并明确 provenance 是否为本次发布的 required gate。是否对特定外发产物强制这些证据由风险判断决定，缺失时不得伪报已具备。

<!-- rule-id: RELEASE-SUPPLY-003 -->
#### 约束第三方部署 action

第三方 action 至少固定主版本或 SHA。高风险部署 action 还要记录 owner、用途和替代方案；无法说明替代路径时，不得把该 action 当作无风险的发布基础设施。

### Rollout、smoke、观察与回退

<!-- rule-id: RELEASE-ROLLOUT-001 -->
#### 按可观测流量选择部署策略

发布默认小批量并保持可回退，高风险变更要进一步拆小。有足够流量时可用 canary 或 progressive rollout，也可按环境能力选择 blue/green 或受控 promote；没有足够流量时，用 staging smoke、production 只读检查与外部 uptime 检查补偿，不能假装执行了 canary。

<!-- rule-id: RELEASE-ROLLOUT-002 -->
#### AI runtime 分阶段扩大

AI runtime change 的默认次序是先做 local eval，再进入 shadow 或 small cohort，持续监控后才扩大范围；整个过程必须保留 rollback route。任一阶段缺少证据时停在当前范围，不直接跳到全量。

<!-- rule-id: RELEASE-WATCH-001 -->
#### 定义 production smoke 覆盖

smoke 按变更影响覆盖关键用户路径、health、gRPC/HTTP endpoint、前端关键页面和 AI fallback 中的适用项。每项必须有实际结果；只访问首页或只看进程存活，不能代表其他路径通过。

<!-- rule-id: RELEASE-WATCH-002 -->
#### 执行发布后 watch

production deploy 后执行 smoke，并连续观察关键 SLI 15–30 分钟；必须覆盖 SLO 四黄金信号。watch plan 在部署前必须链接本次适用的 `stop_conditions`，执行记录按 condition id 保存实际窗口、观测值、触发结果与动作。SLO、dashboard、日志字段和 alert 必须能识别本次 release 的影响，watch 结果进入发布证据。无法形成有效流量时，使用已声明的只读与外部检查，不把“无数据”记成稳定。

<!-- rule-id: RELEASE-WATCH-003 -->
#### 用错误预算触发停止动作

`error_budget_policy` 必须预先写明触发后的暂停发布、回滚、人工复核或最高影响问题修复动作。引用错误预算时，`stop_conditions` 必须链接可解析的 policy 工件与具体条目，并能从该条目确定阈值、观察窗口、信号来源和动作；只写“快速消耗”不构成可检查条件。观察期命中预授权的快速消耗条件时先自动停止扩大，并按合同回滚或关闭开关，再排查。是否恢复或继续 rollout、切 fallback、转人工或接受持续的 eval/投诉风险，必须由指定的人依据当前证据决定。

<!-- rule-id: RELEASE-WATCH-004 -->
#### 维护可判定的 stop conditions

每个 `stop_conditions[]` 条目至少记录 `id`、`threshold`、`observation_window`、`signal_source`、`action`、`decision_owner` 与 `execution_mode`。`signal_source` 必须能定位 metric/query、dashboard panel、log/eval 查询或外部检查；`execution_mode` 只能为 `automatic` 或 `human`。`automatic` 只执行事先批准且可逆的停止扩大、回滚或 disable 动作，并记录执行结果；扩大范围、恢复发布、接受风险或改变客户/数据边界始终由 `decision_owner` 人工决定。缺少任一判定字段时，条件不得被声称为自动 gate，命中不明信号时先停止扩大并转人工。

<!-- rule-id: RELEASE-ROLLBACK-001 -->
#### 让 rollback runbook 可直接执行

`release/rollback/<service>.md` 必须写明回到哪个 artifact 或上一 release、migration 是否可逆及不可逆时的降级/补偿、可用的 feature flag 或 disable switch、回退后的 smoke、谁能执行以及执行入口。pipeline 的 `rollback` 必须指向该可读文件；runbook 和 smoke 步骤要在发布前写好，而不是故障后临时补写。

### 数据 migration 与配置

<!-- rule-id: RELEASE-MIGRATION-001 -->
#### 完成 production migration preflight

生产 migration 由 release pipeline 执行或记录，不从开发机直连生产。preflight 确认 OpenSpec、data change JSON、release pipeline 与 SRE-lite release checklist；随后在临时库或 staging 上以同版本 schema dry-run。进入真实迁移前还要具备备份或恢复路径，并给出 dry-run 或可恢复说明。

<!-- rule-id: RELEASE-MIGRATION-002 -->
#### 拆开破坏性 schema 与 backfill

不可逆 migration 以及 `DROP`/`TRUNCATE` 必须人工 checkpoint。production backfill 分批执行；不得默认在一个 release 中同时完成 rename/drop/alter type、代码切换、数据回填和旧字段删除。需要这些动作时拆成可观察、可停止的多个 release。

<!-- rule-id: RELEASE-MIGRATION-003 -->
#### 记录 migration 运行事实

migration release log 必须记录 migration version、耗时、锁等待、row count、错误与 rollback 状态。字段没有实际测量值时明确标记未知或未发生，不能用空值冒充成功。

<!-- rule-id: RELEASE-CONFIG-001 -->
#### 为配置与 flag 建立 rollout 控制

每个 config item 记录 `rollout`，每个 feature flag 记录 `rollout_plan`。production 中是否触发 kill switch、进入降级、执行回滚或继续扩大范围，必须由人结合当前信号判断并留下决定。

### 客户试点与 go-live

<!-- rule-id: RELEASE-CUSTOMER-001 -->
#### 识别客户上线触发范围

design partner、private beta、proof of concept、pilot、paid pilot、enterprise onboarding 与 production go-live 都属于客户上线。新建 workspace/tenant，启用 SSO/SCIM、客户 flag、entitlement、billing、webhook/API、数据导入或同步，以及客户专属 AI route、RAG、memory 或 tool action，同样触发本组规则；从试点转付费、从内部转外部、从单客户 beta 转公开可用时必须重新判断。

<!-- rule-id: RELEASE-CUSTOMER-016 -->
#### 满足 go-live 最小资格并完成交接

客户进入 production 前，至少维护适用的 pilot charter、tenant provisioning、launch readiness、success plan 或 handoff review。没有租户事实、上线 gate、支持路径或退出路径时不得上线；readiness、support path 与 rollback/offboarding 必须可执行。交接要明确客户成功、支持和退出责任，以少量高价值工件保护一人公司的注意力。

<!-- rule-id: RELEASE-CUSTOMER-013 -->
#### 使用不泄露客户身份的 account 别名

同一客户的上线工件统一使用 `<account>` 别名。别名不得含真实公司名、个人姓名、邮箱、手机号或 customer secret；需要回到真实对象时使用受控引用，而不是把身份信息复制进仓库文件。

<!-- rule-id: RELEASE-CUSTOMER-002 -->
#### 维护 tenant provisioning 主记录

租户事实写入 `customer-onboarding/tenant-provisioning/<account>.json`。主记录至少包含 `target`、`owner`、`customer_alias`、`environment`、`tenant_id_ref`、`identity`、`roles`、`entitlements`、`feature_flags`、`data_imports`、`integrations`、`billing`、`ai_settings`、`observability`、`support_refs`、`rollback_or_offboarding`、`audit_refs`、`human_checkpoint`、`review_cadence` 与 `status`；敏感值只放安全引用。

<!-- rule-id: RELEASE-CUSTOMER-003 -->
#### 解释客户身份与权限

`identity` 记录身份来源、SSO/SCIM 状态、管理员角色来源和生命周期 owner，真实 IdP secret 不进入文件。`roles` 与 `entitlements` 必须能回答客户被允许做什么、被禁止做什么以及授权理由，不能只列角色名。

<!-- rule-id: RELEASE-CUSTOMER-004 -->
#### 描述客户 feature flag

`feature_flags[]` 的每项记录 `key`、`environment`、`value`、`owner`、`rollout_scope`、`rollback` 和 `status`。缺少范围或回退的 flag 不得作为客户上线控制手段。

<!-- rule-id: RELEASE-CUSTOMER-005 -->
#### 描述客户数据导入

`data_imports[]` 的每项记录 `id`、`source`、`data_classification`、`contract_ref`、`status` 和 `dry_run_required`。需要 dry-run 却没有证据时，对应导入 gate 不能通过。

<!-- rule-id: RELEASE-CUSTOMER-006 -->
#### 描述客户集成

`integrations[]` 的 release 投影至少记录 `id`、`kind`、`provider`、`secrets_ref`、`webhook_or_api_refs` 与 `status`。这里只保存受控引用；数据边界与测试证据由相关技术设计和验证规则提供并链接。

<!-- rule-id: RELEASE-CUSTOMER-007 -->
#### 描述客户 billing

`billing` 明确 test 或 live、plan、entitlement source，以及 Stripe/customer id 的安全引用。由 test 切换 live 属于人工 checkpoint，不能因字段已经存在就自动发生。

<!-- rule-id: RELEASE-CUSTOMER-008 -->
#### 描述客户 AI settings

`ai_settings` 记录 model route、RAG source、memory、tool action 和 human review；相应 eval 与 provider/data boundary 必须通过链接交给验证和边界规则。缺少 human review 或降级路径时，不得启用真实客户数据驱动的高影响 action。

<!-- rule-id: RELEASE-CUSTOMER-009 -->
#### 提供 tenant rollback 或 offboarding

`rollback_or_offboarding` 必须能直接说明如何关闭租户访问、暂停同步、导出或删除数据、停用集成并通知客户。每个动作写明执行条件和责任人；只有“联系支持”而没有实际路径不算可退出。

<!-- rule-id: RELEASE-CUSTOMER-010 -->
#### 维护 launch readiness 主记录

上线判断写入 `customer-onboarding/launch-readiness/<account>.json`，包含 `target`、`owner`、`customer_alias`、`launch_type`、`readiness_gates`、`blockers`、`success_criteria`、`support_plan`、`communication_plan`、`rollback_or_exit`、`linked_artifacts`、`human_checkpoint` 与 `status`。`launch_type` 只能取 `internal_trial`、`design_partner`、`private_beta`、`pilot`、`paid_pilot` 或 `production`；上线前必须完成该记录。

<!-- rule-id: RELEASE-CUSTOMER-011 -->
#### 使用统一 readiness gate 合同

外部客户默认检查 `commercial`、`auth_tenant`、`data`、`billing_entitlement`、`integrations`、`ai_eval`、`security_privacy`、`observability_slo`、`support`、`rollback` 与 `customer_acceptance`。每条 gate 记录 `id`、`area`、`check`、`evidence_ref`、`required`、`result`、`owner` 和 `status`。`result` 仅可为 `pending`、`pass`、`fail`、`blocked`、`not_applicable` 或 `accepted_risk`。

<!-- rule-id: RELEASE-CUSTOMER-012 -->
#### 阻断付费与 production 上线缺口

`required=true` 的 gate 若为 `fail`、`blocked` 或 `accepted_risk`，不得静默继续；必须经过人工 checkpoint。`paid_pilot` 或 `production` 缺少可执行的 rollback、offboarding、support 证据或 customer acceptance 时属于硬阻断，不得用“限定试点”或一般 accepted risk 绕过。转 paid pilot/production、导入真实客户数据、启用同步/RAG/memory/tool/connector、SSO/SCIM、admin impersonation、cross-tenant support、production webhook、live billing 或客户专属 entitlement，同样需要人的明确决定。

<!-- rule-id: RELEASE-CUSTOMER-014 -->
#### 控制客户数据进入 AI

客户数据进入 prompt、RAG、memory 或 tool action 前，必须具备 human review 或 fallback。试点样例进入长期 eval/dataset 前要确认授权、脱敏与用途；默认只保存受控引用以及合成或脱敏案例，不把原始客户内容当作通用 fixture。

<!-- rule-id: RELEASE-CUSTOMER-015 -->
#### 链接客户专属 AI 的验证与恢复证据

客户专属 prompt、tool、retrieval source 或 model route 必须链接相应的数据集、红队、RAG 与 AI quality rollback 工件。任一链接失效时，该客户配置不得继续按已验证状态 rollout。

<!-- rule-id: RELEASE-CUSTOMER-017 -->
#### 单独批准客户内容二次使用

把客户内容用于 eval、demo、训练、文档或公开材料必须单独取得人工决定；原上线授权不能自动扩展为这些用途，拒绝或未决定时保持不使用。

<!-- rule-id: RELEASE-CUSTOMER-018 -->
#### 限定未验收的非生产试点

`internal_trial`、`design_partner`、`private_beta` 或非付费 `pilot` 尚无 customer acceptance 时，只能经人工 checkpoint 保持在明示的有限、非生产范围，并在 readiness 记录中写出 `cannot_promote_to_production=true`、缺口、重新判断条件和退出动作。缺少可执行 rollback 或 offboarding 时，不得把该缺口解释为已接受并继续扩大；人的决定只能补齐受控退出后留在有限范围，或选择不发布/退出。请求 paid pilot 或 production 时立即适用硬阻断规则。

### 外部 claim 与商业承诺

<!-- rule-id: RELEASE-CLAIM-001 -->
#### 识别需要 gate 的外部表述

官网、landing page、pricing、help center、developer portal、API reference、SDK README、release note、status/security 页面、privacy、terms、DPA、AUP、AI disclosure、support macro 与 sales email 都是发布面。涉及能力、准确率、延迟、可用性、安全、隐私、保留/训练/驻留、人工审核、合规、退款/计费、IP、支持响应或 API 稳定性的表述必须进入 claim gate。新增强承诺、扩大范围、减少限制或改变数据、AI、安全、费用、SLA 含义时必须更新 gate，并从本次发布链接适用的 `claim-control/surface-inventory/<target>.json`、`claim-control/claim-evidence-map/<target>.json`、`claim-control/release-gate/<target>.json`、`claim-control/correction-runbook/<target>.md` 与 `claim-control/claim-review/<target>.md`；不适用项要明确，而不是留下断链。

<!-- rule-id: RELEASE-CLAIM-002 -->
#### 维护 claim release gate 主记录

每个 production 表述目标使用 `claim-control/release-gate/<target>.json`，记录 `target`、`owner`、`change_id`、`release_or_surface`、`changed_claims`、`new_claims`、`removed_claims`、`evidence_checks`、`surface_checks`、`human_decisions`、`rollback_or_correction`、`linked_artifacts` 与 `status`。字段必须指向当前事实，不能只复制营销文案。

<!-- rule-id: RELEASE-CLAIM-003 -->
#### 记录 changed/new claim 差异

每条 changed 或 new claim 使用 `claim_id` 定位，并记录 `change_type`、`old_text`、`new_text`、`risk_level`、`evidence_ref`、`human_checkpoint` 与 `decision`。删除项单独进入 `removed_claims`，避免用空的新文本隐藏撤回。

<!-- rule-id: RELEASE-CLAIM-004 -->
#### 固定 claim 身份与更正路径

每条待发布 claim 都以稳定 `claim_id` 关联 evidence reference、owner、适用范围、最后核验时间与可执行 correction path；surface 文案变化不得另造身份来绕开旧证据或更正责任。owner、范围、时间或更正入口变化时，同步更新 release gate 与关联表述面。

<!-- rule-id: RELEASE-CLAIM-007 -->
#### 阻断不满足批准条件的 claim

`decision=approve` 前，claim evidence map 不得存在 `unsupported` 或 `expired`，claim 也不得缺少 owner 或 scope。不支持的强声明不得发布；发现任一阻断项时，决定只能保持未批准、降级措辞或返回上游补证，不能靠空的人工确认字段制造批准。

<!-- rule-id: RELEASE-CLAIM-008 -->
#### 链接 claim 发布证据

对本次发布实际适用的证据，claim release gate 必须提供链接；可选证据类型包括 PR/commit、evidence package、release checklist 与 OpenSpec change。

<!-- rule-id: RELEASE-CLAIM-009 -->
#### 为付费客户重新 review claim

存在付费客户时，每次 release 前必须重新 review claim；developer API 稳定性、数据处理、SLO/SLA、模型或路由、供应商政策、合同条款或销售材料任一发生变化前，也必须复审受影响 claim。复审记录沿用 `EVALUATION-CLAIM-001` 的统一工件合同，本项不另设字段。

<!-- rule-id: RELEASE-CLAIM-010 -->
#### 保持 claim 与后端事实一致

依赖政策、合同或运行行为的 claim 必须与底层工件对同一说法给出一致答案。后端依赖至少追溯适用的 Go/Kratos config、feature flag、tenant setting、model route、SLO、audit event、sqlc 数据状态机或 provider client boundary；改变这些事实的配置发布必须同步更新 claim gate，否则阻断 release。

<!-- rule-id: RELEASE-CLAIM-005 -->
#### 对高风险 claim 保留人工决定

AI 能力或准确性、专业替代、security/privacy、数据保留、no-training、数据驻留、SLA、合规、费用/退款、IP 与 human review 等强 claim，发布或继续保留都必须由人判断。相同要求适用于条款、AI disclosure、安全、退款、合规、驻留、不保存等外部承诺，以及向客户承诺自定义功能、路线图、公开案例/引用、特定支持窗口或非标准 SLA；无证据时不得发布。

<!-- rule-id: RELEASE-CLAIM-006 -->
#### 限制低风险修订与 AI 辅助

仅修 typo、格式或链接且不改变含义时，可记录为低风险而不请求人工判断。按钮、tooltip、empty state 和成功提示不得加入未经 gate 的“永远”“保证”“完全”“无限”“实时”“不训练”“合规级”或“专业级”等强词。AI 可以起草、扫描差异或建议降级措辞，但不能自行发布、扩写或强化 claim，最终文本仍须通过 gate。

<!-- rule-id: RELEASE-COMMERCIAL-001 -->
#### 把商业承诺转成可运行义务

合同、订单、SLA、服务积分、DPA、安全附件、红线和其他商业承诺按 High-risk 处理。至少保留适用的 obligation register、agreement map、SLA/service-credit 处理方式、redline playbook 或 contract review，以及证据链接和人工接受记录。非标准条款、24/7、P1 响应、uncapped liability、数据/AI/security 强承诺或超出供应商能力的义务，必须由人决定；复杂情形可另开 OpenSpec 并回到相应边界规则。

<!-- rule-id: RELEASE-HANDOFF-001 -->
#### 把发布结果交给运行与评估

完成 release 或客户 go-live 后，把观测、alert、incident 准备、凭据轮换与 watch 交给“运行”；用户、客户、支持或质量反馈交给“评估”。交接清单明确适用的 dashboard、support channel、billing/entitlement、AI quality 与 claim correction 责任，并记录下一去向。只有发布出口证据已完整且接收方知道观察与处置路径时，才能结束本项。

## 输入与产物

输入至少包括：本轮范围与验收、当前实现 revision、验证矩阵及最新 gate run、候选 artifact、风险与 accepted risk、目标环境/受众、适用的 `stop_conditions` 与 error-budget policy 引用，以及适用的客户、AI、数据、合同和 claim 边界。

产物按触发范围形成：

- 主发布决定、`release_id`、不可变 artifact 引用和 release evidence；
- pipeline schema、实际 run record、rollback runbook、`stop_conditions` 及 smoke/watch 结果；
- 客户上线的 tenant provisioning、launch readiness 与 gate 记录；
- 外部表述的 claim release gate、证据引用与 correction 路径；
- 商业义务登记、人工决定和向运行/评估的交接记录。

## 完成、停止或退出条件

- 完成：主决定已记录；实际动作与决定一致；required gate 已通过或由有权的人显式承接；smoke/watch 与每个适用 stop condition 都有结果，自动动作留有执行证据、人工动作留有决定人与结论；rollback/correction 可执行；运行与评估接收了后续责任。
- 有限退出：决定为延后、仅 preview、仅内部、仅客户试点、灰度或不发布时，只执行该范围允许的动作并记录重新进入条件，不能把有限结果描述成 production 完成。
- 发布前停止：证据过期或缺失、required gate 未承接、artifact 无法追溯、恢复路径不可用、客户上线缺少 support/exit，或 claim/商业边界不成立。
- 发布中停止：`stop_conditions` 命中、smoke 失败、权限/数据隔离异常或出现未计划的真实副作用；先停止扩大，自动条件只执行已批准动作，其他情形转 `decision_owner` 并按 runbook 回退、关闭或补偿。
- 返回：需要改变产品行为、实现、验证设计或风险承诺时，返回对应项目处理；发布项不得自行改写这些上游决定。

## 相关项目引用

- 产品范围、规则与验收由[定义](../02-product-design/03-definition.md)提供。
- 架构、契约、数据与供应链边界引用[技术设计](05-technical-design.md)。
- 代码、配置、migration 与 artifact 的产生方式引用[实现](07-implementation.md)。
- test matrix、eval、运行风险与 acceptance evidence 引用[验证](08-verification.md)。
- post-deploy 观察、支持与事故处置交给[运行](../04-operations-maintenance/10-operation.md)。
- 用户、客户、质量与效果反馈进入[评估](../04-operations-maintenance/11-evaluation.md)。
