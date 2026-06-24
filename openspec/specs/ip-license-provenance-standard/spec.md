# ip-license-provenance-standard Specification

## Purpose

Define the minimum one-person-company governance for open source licenses, third-party code/content/data/source provenance, AI-generated output rights, customer-content reuse, dataset/eval provenance, NOTICE/attribution, public distribution, and IP review.

## Requirements

### Requirement: 第三方材料、AI 输出和公开分发必须具备 ip-rights 工件

任何生产 target 只要使用、分发、发布、训练/评测或用户可见地展示第三方代码、内容、数据、素材、模型、prompt、eval fixture、AI 输出或客户内容，MUST 具备 ip-rights artifacts。

#### Scenario: 新增第三方材料或 AI 输出

- GIVEN 一个 target 会使用或展示第三方材料、AI 输出、客户内容、dataset、model、prompt 或 eval example
- WHEN 创建研发 OpenSpec change
- THEN 创建 `ip-rights/source-register/<target>.json`
- AND 创建 `ip-rights/license-policy/<target>.json`
- AND 创建 `ip-rights/ai-output-policy/<target>.md`
- AND 创建 `ip-rights/notice-attribution/<target>.md`
- AND 创建 `ip-rights/ip-review/<target>.md`
- AND 在 OpenSpec proposal 或 design 中链接 ip-rights artifacts

### Requirement: Source register 必须记录材料来源、许可证、权利基础、用途、分发和 AI 输出边界

Source register MUST 记录 target、owner、materials、ai_outputs、linked artifacts、human checkpoint、review cadence 和状态。

#### Scenario: 登记材料来源

- GIVEN 一个 target 使用外部或 AI 生成材料
- WHEN 创建 `ip-rights/source-register/<target>.json`
- THEN 每个 material 包含 id、name、material_type、origin、source_url_or_ref、license_expression、rights_basis、rights_holder、intended_use、distribution、modification、attribution_required、copyleft_or_sharealike、training_or_eval_use、contains_personal_data、status
- AND 每个 ai_output 包含 id、workflow、model_or_provider、input_rights_basis、output_use、human_authorship、similarity_risk、third_party_rights_check、user_visible_disclosure、status
- AND unknown/no-license/proprietary/copyleft/share-alike/non-commercial/customer-content/training/eval uses require human checkpoint

### Requirement: License policy 必须定义允许、限制、禁止、扫描、分发和 NOTICE 策略

License policy MUST 记录 allowed licenses、restricted licenses、forbidden licenses、dependency scan、package manager rules、redistribution policy、notice policy、AI generated code policy、human checkpoint 和状态。

#### Scenario: 新增依赖或分发包

- GIVEN 一个 target 新增 Go module、npm package、frontend asset、dataset、model、generated code、copied code 或 public release artifact
- WHEN 创建 `ip-rights/license-policy/<target>.json`
- THEN policy 定义 allowed_licenses、restricted_licenses、forbidden_licenses、dependency_scan、package_manager_rules、redistribution_policy、notice_policy、ai_generated_code_policy、human_checkpoint、status
- AND high-risk licenses or unknown sources are blocked or require explicit human checkpoint

### Requirement: AI output policy 必须区分 output ownership、copyrightability、人类作者贡献、相似性和第三方权利

AI output policy MUST 说明输出权利边界、人类作者记录、非唯一/相似输出、第三方权利、用户/客户内容、发布/商用、生成代码、禁止声明、review gate 和链接工件。

#### Scenario: 对外发布 AI 生成内容或代码

- GIVEN 一个 target 会向用户展示、下载、发布或商用 AI 生成内容/代码
- WHEN 创建 `ip-rights/ai-output-policy/<target>.md`
- THEN policy 包含 Output Ownership Boundary、Human Authorship Record、Similarity / Non-Unique Output、Third Party Rights、Generated Code、Prohibited Claims 和 Review Gates
- AND 不得声称 AI-only output 一定可登记版权、独占、完全原创或 100% 可商用，除非人审和专业证据支持

### Requirement: NOTICE / attribution 必须覆盖第三方通知、开源依赖、素材、数据、模型、CC/ODbL、copyleft/source offer 和 release package

Notice attribution MUST 记录 third-party notices、open source dependencies、fonts/icons/media、datasets/models、Creative Commons/Open Data、copyleft/source offer、AI disclosure、release package 和 review cadence。

#### Scenario: 公开分发或客户交付

- GIVEN 一个 target 发布 SDK、CLI、container、frontend bundle、dataset、model、template、docs site、customer deliverable 或 downloadable content
- WHEN 准备 release
- THEN `ip-rights/notice-attribution/<target>.md` 记录适用的 license text、copyright notice、NOTICE、attribution、source offer 和 AI generated content disclosure
- AND 缺失 required notice/source offer/attribution blocks release or requires human checkpoint

### Requirement: IP review 必须复盘来源、许可证变化、AI 输出、数据/eval 来源、归因、客户内容和商标/肖像风险

IP review MUST 记录 recent changes、new sources、license changes、AI output decisions、dataset/eval provenance、notices/attribution、customer/user content、trademarks/publicity、open risks、one next change 和 review cadence。

#### Scenario: 高风险 IP 动作前复盘

- GIVEN 即将引入高风险许可证、复制未知来源、使用客户内容、发布 AI 生成内容、分发 artifact、改变 dataset/model license 或做强权利声明
- WHEN 做出上线或发布决定
- THEN `ip-rights/ip-review/<target>.md` 不得过期
- AND 不存在未解释的 unknown/no-license、copyleft/source offer、attribution、customer content、AI-only copyright claim、third-party rights、trademark/publicity 或 release notice 缺口
