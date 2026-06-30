# 国际化、本地化、时区/货币与多语言 AI 体验规范

## W3 触发定位

本文件是 W3 AI Behavior 的触发型专项规范，不是 W3 主入口。只有当 `docs/W3-ai-behavior/00-main.md` 已经判断需要国际化、本地化、时区/货币、多语言 AI 输出、locale eval 或高风险翻译审查时，才读取本文件。

如果当前只是判断 AI 行为应该如何定义好坏、失败和降级，先回到 `docs/W3-ai-behavior/00-main.md`。

## 目标

一人公司的 AI 产品常常先用一种语言跑通，然后在用户、客户、市场或浏览器语言扩展时才发现：日期格式错、时区丢失、货币小数错、RTL 布局破、AI 回答混语言、模板变量不可翻译、日志里只有本地时间、账单 cutoff 让用户困惑。本专项只解决这个窄问题：让产品在语言、locale、文本方向、时间、数字、货币和 AI 输出语言上有可检查的事实来源和最小验证。

默认原则：**先支持少量 locale，把规则写清楚，再扩展语言**。一人公司不维护完整翻译团队或全球化平台；先把默认 locale、fallback、BCP 47 language tag、IANA time zone、ISO 4217 currency、消息目录、AI locale eval 和 review 做实。

## 核心依据

- 《人月神话》：国际化复杂度不是银弹能解决；真正要保持的是概念完整性：同一用户路径中的语言、时间、货币、AI 输出和错误文案要来自同一套规则。
- 小型项目管理：一人公司不做完整全球化平台；本专项只保留 locale policy、message catalog、time/currency rules、AI locale eval 和 localization review。
- W3C Internationalization：Web 技术应服务不同语言、文字、书写方向和文化环境；本专项把这些要求落到 HTML、CSS、消息、方向和测试。
- IETF BCP 47 / RFC 5646：语言标签用于识别人类语言；本专项使用 BCP 47 tag 记录 `en-US`、`zh-CN`、`ar` 等，而不是自造语言枚举。
- Unicode CLDR / LDML：CLDR 提供日期、数字、货币、复数、区域等 locale 数据；本专项默认使用平台 Intl/CLDR 数据，不手写格式规则。
- IANA Time Zone Database：时区规则会随政治和法律变化而更新；本专项使用 IANA zone name，不只保存 UTC offset。
- ISO 4217：货币使用标准三字母代码，减少多币种、账单和展示错误。
- ECMAScript `Intl` / W3C Intl guide：浏览器原生 Intl 支持语言敏感的日期、数字、货币和排序格式；Vite 前端优先使用 Intl 或成熟 i18n 库，而不是硬编码格式。
- Go `time` / `golang.org/x/text/language`：Go 时间计算有 location 语义；`x/text/language` 支持 BCP 47 language tag 与匹配，适合后端 locale negotiation。
- PostgreSQL date/time：`timestamp with time zone` 和 `timestamp without time zone` 语义不同；业务需要原始用户时区时必须显式存 IANA zone。
- W3C String Metadata / Unicode Bidirectional Algorithm：字符串需要语言和方向 metadata；RTL/BiDi 不能只靠猜测。
- OpenAI Prompt Engineering / eval：多语言 AI 行为必须通过明确指令、代表性样例和 eval 验证，不假设模型会自动稳定保持目标语言。

## 范围

适用对象：

- Vite / React / TypeScript 前端中的 UI copy、表单、错误、日期、数字、货币、语言切换、RTL/BiDi、通知预览、账单/用量展示、AI 输出界面。
- Go/Kratos/sqlc/gRPC 后端中的 locale negotiation、用户语言偏好、时区、日期/时间存储、账单/配额 cutoff、currency code、错误 message key。
- AI workflow 中的 prompt 输出语言、检索内容语言、引用语言、翻译/摘要/分类、多语言 eval、用户输入语言检测和 fallback。
- 邮件/SMS/push/in-app 通知、开发者文档、支持模板、账单页面、数据导出、审计证据中用户可见文本的 locale 边界。

不适用对象：

- 完整翻译管理系统、专业 L10n vendor 流程、所有语言一次性覆盖、机器翻译质量平台。
- SEO、市场站全球化、法律条款正式翻译、税务/发票本地化和区域合规；需要时单独开 change。
- W4 通知渠道治理、W4 计费账本、W5 可访问性整体契约；本专项只补 locale/time/currency/AI language 规则。

## 最小工件

每个 target 使用同一个 `<target>` 文件名：

```text
localization/
  locale-policy/<target>.json
  message-catalog/<target>.json
  time-currency-rules/<target>.md
  ai-locale-eval/<target>.json
  localization-review/<target>.md
```

### `localization/locale-policy/<target>.json`

Locale policy 是本地化事实来源。必须包含：

- `target`
- `owner`
- `default_locale`
- `supported_locales`
- `fallback_locale`
- `language_tag_policy`
- `text_direction_policy`
- `timezone_policy`
- `currency_policy`
- `number_date_formatting`
- `routing_and_persistence`
- `accessibility_refs`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`supported_locales` 每项至少包含：

- `tag`
- `display_name`
- `direction`
- `fallback`
- `coverage`
- `translation_source`
- `reviewer`
- `status`

默认规则：

- `tag` 使用 BCP 47，例如 `en-US`、`zh-CN`、`zh-Hant-TW`、`es-419`。
- `direction` 使用 `ltr` 或 `rtl`，不要只从语言代码猜测；必要时字符串级 metadata 覆盖页面级方向。
- 默认只支持 `default_locale` 和 1 到 2 个真实需要的 locale；其余进入 later。
- Locale preference 顺序默认：用户显式设置、账号/租户设置、Accept-Language、浏览器/系统、default。
- 用户可见错误和 AI 输出必须有 message key 或 locale policy，不直接散落后端英文字符串。

### `localization/message-catalog/<target>.json`

Message catalog 记录 UI、错误、状态、AI disclosure 和关键业务文本，不保存真实用户内容。必须包含：

- `target`
- `owner`
- `catalog_version`
- `namespaces`
- `messages`
- `variables`
- `plural_rules`
- `format_policy`
- `fallback_policy`
- `pseudo_localization`
- `extraction`
- `test_policy`
- `human_checkpoint`
- `status`

`messages` 每项至少包含：

- `id`
- `namespace`
- `default_message`
- `description`
- `variables`
- `risk_class`
- `locales`
- `status`

默认规则：

- `id` 稳定，不使用完整英文句子作为唯一 key。
- `description` 必须解释上下文，避免翻译者或 AI 把同词不同义翻错。
- `variables` 要带类型和示例，如 date、number、currency、count、user_safe_text，不拼接自然语言片段。
- 复数、性别、语序、日期、货币、相对时间使用 ICU/Intl 或成熟库，不手写 `count + " items"`。
- `risk_class` 可为 `low`、`product`、`billing`、`security`、`legal_policy`、`ai_output`、`incident`；高风险文案需要人工 checkpoint。
- Pseudo-localization 或长文本测试用于发现按钮溢出、布局重叠、截断和硬编码字符串。

### `localization/time-currency-rules/<target>.md`

Time/currency rules 给人读，必须包含：

```markdown
# <target> Time And Currency Rules

## Scope

## Time Storage

## Time Zone Policy

## Date / Time Display

## Scheduling And Cutoffs

## Number Formatting

## Currency Formatting

## Database Rules

## Frontend Rules

## Testing

## Human Checkpoints

## Review Cadence
```

默认规则：

- 后端持久化绝对时间默认用 UTC instant；需要用户原始时区、营业日、账单日、预约或 cutoff 时，额外保存 IANA time zone name。
- 不把 UTC offset 当作长期时区；offset 不能表达 DST 和规则变化。
- PostgreSQL 使用 `timestamptz` 存绝对时间；本地日历日期、生日、纯日期或用户输入 local time 要明确语义，避免误当 instant。
- 金额存储使用 minor unit 或 decimal，记录 ISO 4217 currency；展示交给 Intl/CLDR。
- 账单、配额、试用、优惠券、预约、通知 quiet hours 和 SLA cutoff 必须说明使用 UTC、用户时区、租户时区还是合同指定时区。
- 日志和审计默认记录 UTC 时间、request id、trace id；用户界面按用户 locale/time zone 展示。

### `localization/ai-locale-eval/<target>.json`

AI locale eval 记录多语言 AI 行为验证。必须包含：

- `target`
- `owner`
- `locales`
- `workflows`
- `eval_cases`
- `rubric`
- `pass_thresholds`
- `failure_modes`
- `telemetry`
- `linked_artifacts`
- `human_checkpoint`
- `status`

`eval_cases` 每项至少包含：

- `id`
- `workflow`
- `input_locale`
- `expected_output_locale`
- `timezone`
- `currency`
- `scenario`
- `input_summary`
- `assertions`
- `status`

默认规则：

- 改 prompt、model、RAG source、tool schema 或 locale policy 前，至少有一个 default locale、一个非英语 locale、一个格式化 edge case。
- AI 输出必须遵守用户目标语言；引用原文可保留原语言，但解释/行动建议要按目标 locale。
- 多语言 RAG 要记录检索语言、引用语言、翻译/摘要策略和低置信 fallback。
- 对账单、法律、安全、医疗、金融、权限、事故等高风险内容，AI 翻译或多语言生成只作为 draft，需人工 review。
- Telemetry 记录 output locale、fallback reason、user correction、language mismatch，不记录完整敏感 prompt/response。

### `localization/localization-review/<target>.md`

Localization review 必须包含：

```markdown
# <target> Localization Review

## Recent Changes

## Locale Coverage

## Translation Quality

## Time / Currency Findings

## AI Locale Findings

## Accessibility / Direction

## Metrics / Feedback

## Open Risks

## Next One Change

## Review Cadence
```

默认节奏：

- pre-revenue：每月一次，或新增 locale、付费国家/地区、AI 多语言输出、账单/日期规则前。
- 有活跃多语言用户：每两周一次，或每次 locale fallback、RTL、账单 cutoff、AI prompt/model、通知模板、开发者文档语言变化后。
- 每次只选一个最高影响改进：修语言错配、补 fallback、修时间/货币、补 RTL、补 pseudo-localization、补 AI eval。

## Go / Kratos / sqlc / gRPC 默认规则

- gRPC/HTTP boundary 明确 locale fields：`locale`、`time_zone`、`currency`、`message_key`、`field_errors`、`request_id`。
- Go 后端使用 `golang.org/x/text/language` 做 BCP 47 parsing/matching；不要手写 `strings.HasPrefix(lang, "en")` 当作长期策略。
- Go 时间使用 `time.Time` 表示 instant；用户时区使用 IANA location name 并在显示或 local business rule 时应用。
- sqlc schema 中用户偏好可包含 `locale_tag`、`time_zone`、`currency_code`；账单/预约/cutoff 按规则保存相关字段。
- 后端错误默认返回稳定 code/message key 和参数，不把英文句子作为契约。
- 生成审计和日志时用 UTC；用户导出和 UI 视图按用户 locale/time zone 格式化。

## Vite / Geist 前端默认规则

- Vite 前端使用 `Intl.DateTimeFormat`、`Intl.NumberFormat`、`Intl.RelativeTimeFormat` 或成熟 i18n 库，不手写日期/货币格式。
- 根元素和局部文本需要正确 `lang` 与 `dir`；混合语言/方向字符串按 W3C string metadata 处理。
- 组件必须通过 pseudo-localization 或长文本样例检查按钮、表格、卡片、toast、弹层、移动端和深色主题。
- Geist 风格在多语言环境中仍然要克制、清晰、可扫；不要用固定宽度按钮、负字距或纯图标替代本地化文本。
- 语言切换、时区设置、货币展示必须可解释；用户看不到账单或预约 cutoff 的时区时，不得发布付费/预约路径。

## AI workflow 默认规则

- Prompt 明确目标输出语言、locale、time zone、currency 和是否允许引用原文语言。
- Eval 覆盖目标语言错配、代码混杂、日期/货币格式错误、RTL 输出、翻译过度、本地法律/政策措辞误导。
- AI 生成翻译默认是 draft；高风险文案、外发通知、合同/政策、安全/事故、账单/退款、医疗/法律/金融内容需要人工 review。
- 用户纠错和语言反馈进入 W3 eval、W8 support feedback、W8 quality regression，而不是只改一次 prompt。

## 需要人判断的关键点

默认不问：

- message id 命名、普通低风险 UI 文案、默认 locale 文件路径、格式化 helper 名称。

必须问：

- 是否新增正式支持 locale、RTL 语言、付费国家/地区或多币种展示。
- 是否把 AI 翻译/多语言生成用于安全、账单、法律、医疗、金融、权限、事故或对外承诺。
- 是否接受未人工 review 的高风险翻译、机器翻译或 AI 生成文案上线。
- 是否改变账单、试用、配额、预约、SLA、通知 quiet hours 或数据导出的时区规则。
- 是否允许 fallback 到错误语言，或在不支持 locale 时继续展示付费/合规/安全路径。
- 是否引入外部翻译供应商、发送用户内容给翻译/LLM 服务或改变数据跨境边界。

## 执行顺序

1. 先写 `locale-policy`：default locale、真实支持 locale、fallback、方向、时区和货币规则。
2. 写 `message-catalog`：只纳入核心路径、错误、账单、AI disclosure 和高风险状态。
3. 写 `time-currency-rules`：明确 UTC、IANA time zone、ISO currency 和 cutoff 语义。
4. 写 `ai-locale-eval`：至少覆盖 default locale、一个非英语 locale、一个格式/时区 edge case。
5. 写 `localization-review`：只保留一个下一步改进。
6. 在 Vite/Go/OpenSpec change 中链接这些 artifacts；真实项目每次只扩一个 locale 或一个高风险路径。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“支持哪些语言、文本怎么管、时间货币怎么算、AI 多语言怎么测、下一步修什么”。
- 保留：人只判断新增正式 locale、RTL、多币种/付费地区、高风险 AI 翻译、时区 cutoff 和外部翻译供应商。
- 调整：不默认接翻译平台；先用 JSON catalog、Intl、Go `x/text/language` 和少量 eval。
- 调整：不要求所有页面本地化；先覆盖登录、设置、账单、通知、AI 输出、错误和数据导出。
- 风险：本地化容易变成大量文案工作。缓解：先支持少数 locale，review 每次只选一个最高风险改进。

结论：可落地。一个人可以先把最关键路径的 locale、时间、货币和 AI 输出语言规则写进五个文件，再逐步扩语言。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：用户看到的语言、时间、货币、AI 输出和错误状态一致，减少误解和信任损耗。
- 工程角度：Go/Kratos/sqlc/gRPC、Vite 和 AI workflow 都有明确 locale/time/currency 字段和测试入口。
- 运维角度：日志用 UTC，用户界面按 locale 展示；账单 cutoff、通知 quiet hours 和事故时间不会临场解释。
- 安全隐私角度：外部翻译、AI 多语言生成、用户内容跨境和高风险文案都有人审。
- 成本角度：不一次性全球化；先用平台 Intl/CLDR 和少量 eval，避免把一人公司变成翻译项目。

结论：可落地。本专项把“以后再国际化”压成能渐进执行的 locale/time/currency/AI language 规范。
