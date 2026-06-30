# 开源许可证、AI 生成内容与知识产权来源治理规范
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE 或 attribution”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## 目标

一人公司做 AI 产品时，知识产权风险往往不是来自“写了多少代码”，而是来自看似普通的复用：复制一段网上代码、引入 AGPL 依赖、把 CC-NC 素材放进商业页面、把客户内容塞进 eval、让 AI 生成营销图并声称完全拥有版权、把第三方品牌或人物风格做成模板、发布时忘记 NOTICE。本触发专项的目标是建立最小可执行的 IP / license / provenance 治理，让每个生产 target 都能回答：用到了哪些外部材料，它们的许可证和权利基础是什么，AI 生成内容能否商用/发布，是否需要 attribution/NOTICE/source offer，什么时候必须人判断或法律审阅。

本阶段不是法律意见；它把可工程化的权利来源、许可证、归因和发布证据沉淀到仓库。真正的合同、诉讼、商标注册、专利、复杂 fair use 或客户赔偿仍需要专业审阅。

## 核心依据

- 《人月神话》：概念完整性来自少数一致决策。知识产权也一样：代码、数据、素材、模型输出和客户内容如果没有同一套来源边界，后期会变成无法拆解的概念债。
- 小型项目管理：一人公司不做大型 OSPO/GRC；只保留能阻止上线事故的五个工件：source register、license policy、AI output policy、notice attribution、IP review。
- The Cathedral and the Bazaar / Producing Open Source Software：开源复用不是“免费拿来”，而是一组协作、许可、贡献、归因和分发约定。越是小团队，越要把许可证和社区预期写清楚。
- Software Engineering at Google, Dependency Management：依赖是随时间变化的网络。许可证、来源、分发方式和 transitive dependency 会随着版本变化，因此 license 也要进入 review。
- SPDX / REUSE：许可证信息应该机器可读、文件级可追踪、可随复制和再分发保留。本专项默认使用 SPDX expression 和 REUSE 思路表达许可证。
- OSI / npm / Go package ecosystem：开源许可证定义了使用、修改和分发权利；npm package license 字段使用 SPDX expression；Go module 依赖需要可追踪的模块和许可证信息。
- GitHub Dependency Review：依赖变更可以在 PR 阶段检查漏洞和许可证；license gate 应该在引入依赖时运行，而不是发布前临时翻仓库。
- U.S. Copyright Office AI guidance：美国版权登记要求人类作者身份；包含 AI 生成材料的作品需要区分人类贡献和 AI 生成部分。AI 输出的商业使用权和可版权性不是同一件事。
- OpenAI Terms / Services Agreement / Usage Policies：OpenAI 条款会分配 input/output 权利，但输出可能不唯一，使用者仍需评估准确性、适当性、第三方权利和政策义务。
- Creative Commons / Open Data Commons / Hugging Face dataset cards：内容、数据、模型和数据集许可证与软件许可证不同；CC、ODbL、dataset/model cards 的 attribution、share-alike、non-commercial 和 usage limitations 要单独记录。
- USPTO / WIPO：版权、商标、专利和商业秘密是不同权利；生成式 AI 可能涉及 copyright、trademark、database right、publicity/personality 等多种风险，不能只看软件 license。

## 范围

适用对象：

- Go/Kratos/sqlc/gRPC 服务代码、生成代码、第三方 Go module、复制代码片段、模板、CLI、SDK。
- Vite 前端依赖、UI 模板、字体、图标、图片、音视频、示例内容、设计素材。
- AI prompt、system prompt、tool schema、eval fixture、golden examples、red-team cases、RAG seed content、dataset、model card、fine-tuning data。
- AI 生成的文本、代码、图片、音频、视频、营销文案、帮助文档、客服回复、用户可下载内容。
- 客户或用户上传内容被用于 eval、训练、演示、文档、截图、case study、support article 或内部 fixture 的场景。

不适用对象：

- 纯内部一次性草稿，且不进入仓库、不进入产品、不分发、不作为 eval/training 数据、不对外展示。
- 正式法律意见、license interpretation、fair use opinion、商标注册、专利策略、版权登记、侵权通知处理。
- 完整 OSPO、FOSSA/Snyk/Black Duck 企业平台、贡献者许可协议流程；需要时单独开 change。

## 最小工件

每个生产 target 使用同一个 `<target>` 文件名：

```text
ip-rights/
  source-register/<target>.json
  license-policy/<target>.json
  ai-output-policy/<target>.md
  notice-attribution/<target>.md
  ip-review/<target>.md
```

### `ip-rights/source-register/<target>.json`

来源登记表必须包含：

- `target`
- `owner`
- `materials`
- `ai_outputs`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`materials` 每项至少包含：

- `id`
- `name`
- `material_type`
- `origin`
- `source_url_or_ref`
- `license_expression`
- `rights_basis`
- `rights_holder`
- `intended_use`
- `distribution`
- `modification`
- `attribution_required`
- `copyleft_or_sharealike`
- `training_or_eval_use`
- `contains_personal_data`
- `status`

`material_type` 默认包含：

- `go_module`
- `npm_package`
- `copied_code`
- `generated_code`
- `template`
- `font`
- `icon`
- `image`
- `audio`
- `video`
- `dataset`
- `model`
- `prompt`
- `eval_example`
- `rag_source`
- `customer_content`
- `third_party_content`
- `documentation`

`ai_outputs` 每项至少包含：

- `id`
- `workflow`
- `model_or_provider`
- `input_rights_basis`
- `output_use`
- `human_authorship`
- `similarity_risk`
- `third_party_rights_check`
- `user_visible_disclosure`
- `status`

默认：

- 没有许可证、许可证未知、来源未知、复制自网页/聊天/issue/Stack Overflow/模型输出的代码或内容，不得进入生产，除非人审接受并记录替代方案。
- `license_expression` 使用 SPDX expression；无法表达时写 `LicenseRef-<name>` 并链接实际条款。
- 任何 `AGPL`、`GPL`、`LGPL`、`MPL`、`CC-BY-SA`、`CC-BY-NC`、`ODbL`、`proprietary`、`no_license`、`unknown` 都需要人审。
- 客户内容用于 eval、训练、演示、文档或案例，必须有 rights_basis、隐私边界、删除路径和人审。
- AI 输出可用于产品不等于一定可主张版权；对外 claim 需要记录人类选择、编排、编辑或其他可辨识贡献。

### `ip-rights/license-policy/<target>.json`

许可证策略必须包含：

- `target`
- `owner`
- `allowed_licenses`
- `restricted_licenses`
- `forbidden_licenses`
- `dependency_scan`
- `package_manager_rules`
- `redistribution_policy`
- `notice_policy`
- `ai_generated_code_policy`
- `human_checkpoint`
- `status`

默认策略：

- 默认允许：MIT、Apache-2.0、BSD-2-Clause、BSD-3-Clause、ISC、0BSD、CC0、Unlicense。
- 默认限制：MPL、LGPL、GPL、AGPL、EPL、CDDL、ODbL、CC-BY、CC-BY-SA、CC-BY-NC、custom LicenseRef、proprietary。
- 默认禁止进入商业生产：unknown、no_license、non-commercial without commercial grant、source with unclear rights、leaked code、confidential source、unlicensed web copy、user/customer content without rights basis。
- Go 依赖、npm 依赖、前端素材、模型/数据集、AI 生成代码都要有最小 license/provenance check。
- 任何公共分发、客户交付、容器镜像、SDK、CLI、前端 bundle、模型包、dataset release，都要生成或更新 notice/attribution。

### `ip-rights/ai-output-policy/<target>.md`

AI 输出策略必须包含：

```markdown
# <target> AI Output Policy
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE 或 attribution”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Scope

## Output Ownership Boundary

## Human Authorship Record

## Similarity / Non-Unique Output

## Third Party Rights

## User / Customer Content

## Publication / Commercial Use

## Generated Code

## Prohibited Claims

## Review Gates

## Linked Artifacts

## Review Cadence
```

默认：

- 不声称 AI-only output 一定可版权登记或具有排他性，除非有专业意见和人类作者贡献记录。
- 对外发布 AI 生成内容前，记录人类选择、修改、编排、编辑、事实核验、品牌审查和第三方权利检查。
- 不要求把所有 AI 输出都贴大标签；但用户可能误认为由人创作、专业审阅或完全原创时，必须披露或降级 claim。
- 生成代码必须经过普通 code review、license/provenance review 和测试；不得复制模型给出的“看起来像某开源项目”的代码。
- 不生成或发布“以某在世艺术家风格”“带真实品牌 logo”“模仿名人/客户/竞争对手素材”的高风险输出，除非有明确授权或专业审阅。

### `ip-rights/notice-attribution/<target>.md`

NOTICE / attribution 文件必须包含：

```markdown
# <target> Notice And Attribution
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE 或 attribution”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Scope

## Third Party Notices

## Open Source Dependencies

## Fonts / Icons / Media

## Datasets / Models

## Creative Commons / Open Data

## Copyleft / Source Offer

## AI Generated Content Disclosure

## Release Package

## Review Cadence
```

默认：

- 只要对外分发，就要保留第三方许可证文本、版权声明、NOTICE、attribution 或 source offer 中适用项。
- 前端 bundle、mobile/desktop app、CLI、SDK、Docker image、文档站、数据集、模型包、营销页素材的 attribution 位置可以不同，但必须在工件中说明。
- CC 和 ODbL 类材料的 attribution/share-alike/keep-open 规则不能被简单合并到软件 NOTICE 里；需要单独说明。
- 如果不分发，只 SaaS 运行，也仍要记录 AGPL/network copyleft、dataset/model terms、API terms 和 customer content rights。

### `ip-rights/ip-review/<target>.md`

IP 复盘必须包含：

```markdown
# <target> IP Review
## W2 触发定位

本文件是 W2 OpenSpec / Risk 的触发型专项规范，不是 W2 主入口。只有当 docs/W2-openspec-risk/00-main.md 的场景触发规范命中“开源许可证、第三方素材、AI 生成内容、客户内容复用、NOTICE 或 attribution”时，才读取本文件。

如果当前只是定义变更的基本意图、行为、边界、风险和退出条件，先回到 W2 核心规范 docs/W2-openspec-risk/00-main.md。
## Recent Changes

## New Sources

## License Changes

## AI Output Decisions

## Dataset / Eval Provenance

## Notices / Attribution

## Customer / User Content

## Trademarks / Publicity

## Open Risks

## One Next Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次或 public release 前。
- 有付费客户：每次新增分发包、公开页面素材、客户案例、eval/training 数据、SDK/CLI/container release 或高风险许可证前。
- 出现 copyleft、AGPL、无许可证、客户内容、AI-only copyright claim、第三方品牌/人物、data/model license 变化：立即复盘。

## Go / Kratos / sqlc / gRPC 默认规则

- Go module 新增或升级时检查 license/provenance；`replace`、fork、private module、copied code 必须进入 source register。
- generated code 记录生成工具、输入 schema/proto/query、工具许可证和是否可再生成；不要把生成代码当原创手写代码。
- gRPC/protobuf、sqlc generated code、OpenAPI/SDK 公开分发时，release package 必须带 license、NOTICE 或 attribution 中适用项。
- 代码注释、错误文案、示例数据、fixtures、eval examples 不得包含无授权第三方文本、客户内容、真实个人数据或模型吐出的长段受版权保护材料。
- license gate 失败时不通过“删掉 LICENSE 文件”解决；要替换依赖、调整使用方式、取得授权或人审接受风险。

## Vite 前端默认规则

- 字体、图标、图片、视频、插画、UI template、CSS snippet、theme token、示例内容都要有来源和许可证。
- 公开页面避免使用未授权品牌 logo、竞品截图、名人照片、受保护角色、在世艺术家风格或来源不明素材。
- 使用 Vercel/Geist 风格时只参考设计原则和公开文档，不复制 Vercel 品牌资产、专有图标、商标或受保护页面内容。
- AI 生成营销图、客户案例、help center 截图和 demo 数据必须做第三方权利检查和人类编辑记录。
- 如果用户可下载生成内容，前端应给出真实的权利/限制说明，不承诺“完全原创”“100% 可商用”“独占版权”。

## AI workflow 默认规则

- Prompt、eval、dataset、RAG source、fine-tuning 样本、red-team cases 都要记录来源、license、rights_basis 和是否允许训练/评测。
- 用户或客户内容默认不能进入通用 eval/training/demo，除非有明确授权、脱敏、删除路径和人审。
- AI 生成代码不可直接作为 license-free 代码复制入库；必须记录生成来源、审查结果、测试证据和相似性/第三方权利风险。
- 对外输出中的事实、引用、代码、长文本、歌词、图片、品牌、人物和风格请求要按内容安全、copyright 和 trademark 风险处理。
- 模型供应商 output ownership 条款要按具体服务和日期记录；不要把“供应商分配 output 权利”当成“所有司法辖区都可版权登记”。

## 需要人判断的关键点

默认不问：字段顺序、低风险 MIT/Apache/BSD 依赖、普通 notice 文案、内部未分发素材、低风险 prompt 小改。

必须问：

- 是否引入 AGPL/GPL/LGPL/MPL/EPL/CDDL/ODbL/CC-BY-SA/CC-BY-NC/custom/proprietary/no-license/unknown 来源。
- 是否复制网页、聊天、issue、Stack Overflow、论文、书籍、文档、竞品、客户材料或模型输出中的代码/文本/素材。
- 是否把用户/客户内容用于 eval、训练、演示、营销、文档、截图、样例或 case study。
- 是否对 AI 输出声明独占版权、可登记版权、完全原创、100% 可商用、无第三方风险或可替代专业意见。
- 是否公开发布包含第三方素材、品牌、人物、商标、受保护角色、在世艺术家风格或数据集/model license 限制的内容。
- 是否发布 SDK、CLI、container、前端 bundle、dataset、model、template 或客户交付物，且 NOTICE/source offer/attribution 不完整。
- 是否需要律师、IP 专业人士、商标检索、版权登记、fair use 分析、授权谈判或客户赔偿承诺。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“来源是什么、许可证策略是什么、AI 输出怎么用、NOTICE 怎么交付、多久复盘”。
- 保留：人只判断高风险许可证、无授权来源、客户内容复用、AI-only 权利主张、第三方品牌/人物/素材和公开分发。
- 调整：不要求搭 OSPO 或全量 license 平台；先用 source register + policy + verifier 管住真实上线边界。
- 调整：不把每个 MIT 小依赖都升级给人；低风险许可证由脚本和默认策略处理。
- 风险：IP 记录可能变成“填表安慰剂”。缓解：每项 material 必须写 intended_use、distribution、rights_basis 和 status；release 前看 notice 是否真的可交付。

结论：可落地。一个人可以先登记生产 target 中真正会分发、训练、展示或客户可见的材料，把未知来源和高风险许可证挡在上线前。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：避免对用户承诺“独占原创/完全可商用”但实际没有证据；AI disclosure 和 trust claim 可连接权利来源。
- 工程角度：Go/Vite/AI workflow 都有明确的 source register 和 release notice gate，不把 license review 留到发布最后一天。
- 运维角度：dependency/license 变化、public release、dataset/eval 更新和模型输出策略变化都有复盘入口。
- 安全隐私角度：客户内容、个人数据、机密材料和无授权内容不会静默进入 eval/training/demo。
- 成本角度：早期不买重型合规平台，只在高风险材料上付人工注意力；低风险依赖靠 SPDX/REUSE/GitHub gate/脚本处理。

结论：可落地。本专项把“我能不能用这个材料”变成研发前置条件，而不是等客户、平台或权利人质疑时再补证据。


