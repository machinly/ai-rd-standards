# localization-locale-time-ai-standard Specification

## Purpose

Define the minimum internationalization, localization, locale, time zone, currency, and multilingual AI experience standard for a one-person AI company so products can support languages and regions gradually without breaking user trust, billing semantics, UI layout, or AI output language behavior.

## Requirements

### Requirement: 多语言或区域化 target 必须定义 localization artifacts

Targets that support multiple user languages, AI multilingual output, locale-specific formatting, user time zones, paid countries/regions, multi-currency display, RTL/BiDi text, localized notifications, or user-visible date/time cutoffs MUST define localization artifacts.

#### Scenario: 创建 localization artifacts

- GIVEN 一个 target 支持多语言、locale fallback、时区、货币、RTL、AI 多语言输出或区域化计费/通知
- WHEN 创建 localization artifacts
- THEN 创建 `localization/locale-policy/<target>.json`
- AND 创建 `localization/message-catalog/<target>.json`
- AND 创建 `localization/time-currency-rules/<target>.md`
- AND 创建 `localization/ai-locale-eval/<target>.json`
- AND 创建 `localization/localization-review/<target>.md`
- AND 在 OpenSpec design 或 tasks 中链接 localization artifacts

### Requirement: Locale policy 必须定义 supported locales、fallback、方向、时区和货币

Locale policy MUST record target, owner, default locale, supported locales, fallback locale, language tag policy, text direction policy, timezone policy, currency policy, number/date formatting, routing/persistence, accessibility refs, linked artifacts, human checkpoint, review cadence, and status.

#### Scenario: 创建 locale policy

- GIVEN reviewer 打开 `localization/locale-policy/<target>.json`
- WHEN 检查 locale policy
- THEN 文件包含 `target`、`owner`、`default_locale`、`supported_locales`、`fallback_locale`、`language_tag_policy`、`text_direction_policy`、`timezone_policy`、`currency_policy`、`number_date_formatting`、`routing_and_persistence`、`accessibility_refs`、`linked_artifacts`、`human_checkpoint`、`review_cadence`、`status`
- AND 每个 supported locale 包含 `tag`、`display_name`、`direction`、`fallback`、`coverage`、`translation_source`、`reviewer`、`status`
- AND locale tag 使用 BCP 47-compatible 格式

### Requirement: Message catalog 必须使用稳定 message id、变量 metadata 和 fallback policy

Message catalog MUST record target, owner, catalog version, namespaces, messages, variables, plural rules, format policy, fallback policy, pseudo-localization, extraction, test policy, human checkpoint, and status.

#### Scenario: 创建 message catalog

- GIVEN reviewer 打开 `localization/message-catalog/<target>.json`
- WHEN 检查 message catalog
- THEN 文件包含 `target`、`owner`、`catalog_version`、`namespaces`、`messages`、`variables`、`plural_rules`、`format_policy`、`fallback_policy`、`pseudo_localization`、`extraction`、`test_policy`、`human_checkpoint`、`status`
- AND 每个 message 包含 `id`、`namespace`、`default_message`、`description`、`variables`、`risk_class`、`locales`、`status`
- AND 高风险文案的 `risk_class` 为 `billing`、`security`、`legal_policy`、`ai_output` 或 `incident` 时，必须有 human checkpoint 覆盖

### Requirement: Time/currency rules 必须定义 UTC、IANA time zone、ISO currency 和 cutoff 语义

Time/currency rules MUST define time storage, time zone policy, date/time display, scheduling and cutoffs, number formatting, currency formatting, database rules, frontend rules, testing, human checkpoints, and review cadence.

#### Scenario: 创建 time/currency rules

- GIVEN reviewer 打开 `localization/time-currency-rules/<target>.md`
- WHEN 检查 time/currency rules
- THEN 文档包含 Scope、Time Storage、Time Zone Policy、Date / Time Display、Scheduling And Cutoffs、Number Formatting、Currency Formatting、Database Rules、Frontend Rules、Testing、Human Checkpoints、Review Cadence
- AND 明确何时使用 UTC instant
- AND 明确何时保存 IANA time zone name
- AND 明确金额展示使用 ISO 4217 currency code 或等价来源

### Requirement: AI locale eval 必须验证输出语言、格式化、时区/货币和 fallback

AI locale eval MUST record target, owner, locales, workflows, eval cases, rubric, pass thresholds, failure modes, telemetry, linked artifacts, human checkpoint, and status.

#### Scenario: 创建 AI locale eval

- GIVEN reviewer 打开 `localization/ai-locale-eval/<target>.json`
- WHEN 检查 AI locale eval
- THEN 文件包含 `target`、`owner`、`locales`、`workflows`、`eval_cases`、`rubric`、`pass_thresholds`、`failure_modes`、`telemetry`、`linked_artifacts`、`human_checkpoint`、`status`
- AND 每个 eval case 包含 `id`、`workflow`、`input_locale`、`expected_output_locale`、`timezone`、`currency`、`scenario`、`input_summary`、`assertions`、`status`
- AND 至少覆盖 default locale 和一个非 default locale

### Requirement: Localization review 必须保留覆盖、质量、时间/货币、AI locale、方向和下一步

Localization review MUST record recent changes, locale coverage, translation quality, time/currency findings, AI locale findings, accessibility/direction, metrics/feedback, open risks, one next change, and review cadence.

#### Scenario: 创建 localization review

- GIVEN reviewer 打开 `localization/localization-review/<target>.md`
- WHEN 检查 localization review
- THEN 文档包含 Recent Changes、Locale Coverage、Translation Quality、Time / Currency Findings、AI Locale Findings、Accessibility / Direction、Metrics / Feedback、Open Risks、Next One Change、Review Cadence
- AND Next One Change 非空

### Requirement: 高风险本地化变更必须人工 checkpoint

Official supported locale additions, RTL language support, paid country/region enablement, multi-currency display, high-risk AI translation, legal/security/billing/incident/policy copy translation, timezone cutoff changes, and external translation/LLM provider use MUST have human checkpoint coverage.

#### Scenario: 处理高风险本地化变更

- GIVEN target 新增正式 locale、RTL、多币种、付费地区、高风险翻译、账单/配额/试用/预约/SLA/事故/通知时区规则变化，或外部翻译供应商
- WHEN 更新 localization artifacts
- THEN `human_checkpoint` MUST 记录 owner、判断、风险、验证和 rollback/fallback

### Requirement: Localization artifacts 不得保存敏感内容

Localization artifacts MUST NOT store secrets, production tokens, private keys, payment data, raw prompts, raw responses, raw tool outputs, full user content, unredacted personal data, protected health/financial/legal content, or customer-confidential translation samples.

#### Scenario: 写入 localization artifacts

- GIVEN Codex 或 reviewer 要记录翻译样例、AI locale eval、用户反馈、错误、账单文本或通知文本
- WHEN 写入 `localization/` artifacts
- THEN 使用 synthetic example、message id、redacted summary、trace id、request id、eval case id、hash 或 controlled attachment reference
- AND 不保存 secret、生产 token、支付数据、完整 raw prompt/response/tool output、完整用户内容、未脱敏个人数据或客户机密文本
