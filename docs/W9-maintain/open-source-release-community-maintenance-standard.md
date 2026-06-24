# W9 Maintain 触发专项：开源发布、社区贡献与维护边界规范

## W9 触发定位

本文件是 W9 Maintain 的触发型专项，不是 W9 主入口。只有当当前工作涉及公开仓库、SDK/CLI/template、MCP server、开源贡献、安全报告、community health、release/security review 或维护边界时，才需要读取本文件。

普通 W9 维护入口应先回到 `docs/W9-maintain/main.md`，由主入口判断是否触发本专项。

## 目标

一人公司做 AI 产品时，开源看起来像增长和信任杠杆：公开 SDK、示例、模板、MCP server、Vite starter、Go client、CLI、operator、eval harness 或 RAG connector。但公开仓库一旦存在，就会产生隐形承诺：有人会提 issue、发 PR、报告漏洞、要求 roadmap、依赖你的 package、引用你的文档、期待安全修复和兼容性。本专项的目标是把开源发布和社区协作压成一套可维护的最小系统：公开什么、接受什么贡献、如何响应、安全漏洞怎么走、什么时候可以说不、何时暂停或归档。

本专项不替代 W2 的 IP/license/provenance，也不替代 W7 的安全事故响应、W4 的开发者文档、W2 的 API 兼容性。它负责公开仓库本身的维护边界和社区入口。

默认原则：**开源不是无成本营销页，而是一个对外运行的产品 surface**。一人公司只开源能长期维护、能自动验证、能清楚说明支持边界的东西。

## 核心依据

- 《人月神话》：公开接口和社区预期会增加协调成本；开源项目也需要概念完整性，否则 issue、PR、release 和支持会互相拉扯。
- 小型项目管理：一人公司不能维护大型 OSPO 或社区团队；只保留开源发布前最能降低维护负担的 5 个工件。
- The Cathedral and the Bazaar：开源协作可以带来反馈和改进，但前提是维护者能把问题、贡献和发布节奏组织起来。
- Producing Open Source Software：开源项目需要清晰的贡献、沟通、治理、release、bug 和安全流程；很多维护工作不是写代码。
- Working in Public：公开项目的维护者注意力是稀缺资源；issue/PR 队列、社区支持和用户期望必须被主动设计。
- GitHub Open Source Guides：维护者应记录流程、学会说不、利用社区和自动化，也可以在负担过高时暂停。
- GitHub Community Health / templates：README、LICENSE、CONTRIBUTING、CODE_OF_CONDUCT、SUPPORT、SECURITY、issue/PR template 等文件能标准化贡献入口。
- Contributor Covenant / DCO：社区行为准则和贡献权利声明能把隐性规则显式化，降低冲突和权利不清。
- OpenSSF Scorecard / Best Practices / SLSA：公开仓库和发布包需要基本供应链安全、依赖更新、构建完整性和漏洞披露能力。
- SPDX / REUSE / OSI：开源许可、文件级版权和许可证信息需要机器可读、可随分发保留。
- GitHub Security Advisories / private vulnerability reporting：公开仓库应提供私下报告漏洞、协作修复和发布 advisory 的路径。

## 范围

适用对象：

- 公开或准备公开的 GitHub/GitLab 仓库、SDK、CLI、Go module、npm package、Docker image、template、starter、example app、MCP server、connector、operator、eval harness、docs site。
- 接受外部 issue、discussion、pull request、security report、feature request、bug report、documentation contribution 的项目。
- 与 Go/Kratos/sqlc/gRPC/Vite/AI workflow 相关的开源组件和示例。

不适用对象：

- 纯内部私有仓库且不接受外部贡献、不分发包、不承诺公开支持。
- 正式基金会治理、OSPO、CLA 法律文本、商标政策、商业开源许可证设计、双许可商业策略；这些需要专业审阅或单独 change。
- W2 IP/license/provenance 已覆盖的第三方材料使用许可判断；本专项只处理你对外发布和接受贡献的维护方式。

## 最小工件

每个开源 target 使用同一个 `<target>` 文件名：

```text
open-source/
  project-register/<target>.json
  community-health/<target>.json
  contribution-policy/<target>.md
  maintainer-runbook/<target>.md
  release-security-review/<target>.md
```

### `open-source/project-register/<target>.json`

项目登记表必须包含：

- `target`
- `owner`
- `repositories`
- `packages`
- `license_policy`
- `public_scope`
- `support_boundary`
- `security_policy`
- `contribution_model`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`repositories` 每项至少包含：

- `id`
- `name`
- `url_or_path`
- `visibility`
- `purpose`
- `license_expression`
- `default_branch`
- `release_channels`
- `package_artifacts`
- `community_health_ref`
- `security_ref`
- `owner`
- `status`

默认规则：

- `visibility=public` 且 `status=active` 的仓库必须有 LICENSE、README、SECURITY、CONTRIBUTING、SUPPORT、issue/PR 模板和 release/security review。
- 公开仓库的 `purpose` 必须清楚：SDK、example、template、plugin、CLI、docs、integration、research artifact 或 experimental demo。
- `support_boundary` 必须说明：是否提供商业支持、best-effort、无 SLA、仅 security fix、仅当前 minor version、或 archive。
- 公开前必须确认不会暴露 secret、客户数据、内部 URL、商业路线图、未发布模型/供应商配置、内部 prompt、敏感 eval。

### `open-source/community-health/<target>.json`

社区健康工件必须包含：

- `target`
- `owner`
- `files`
- `templates`
- `code_of_conduct`
- `support`
- `security`
- `contributing`
- `issue_pr_templates`
- `governance`
- `linked_artifacts`
- `human_checkpoint`
- `review_cadence`
- `status`

`files` 每项至少包含：

- `name`
- `path`
- `required`
- `owner`
- `last_reviewed`
- `status`

默认 required files：

- `README`
- `LICENSE`
- `CONTRIBUTING`
- `CODE_OF_CONDUCT`
- `SECURITY`
- `SUPPORT`
- `ISSUE_TEMPLATE`
- `PULL_REQUEST_TEMPLATE`

默认规则：

- `README` 说明项目用途、稳定性、安装、quickstart、支持边界、security report 路径。
- `CONTRIBUTING` 说明哪些贡献会被接受、如何跑测试、PR 要求、AI 生成贡献披露、DCO/CLA。
- `SECURITY` 不让漏洞进入 public issue；写明 supported versions 和私下报告方式。
- `SUPPORT` 明确 GitHub issue 不是客服/SLA/生产事故通道，商业支持和安全报告另走对应路径。
- `CODE_OF_CONDUCT` 可以采用 Contributor Covenant 或等价模板，但要写清执行联系人和处理边界。

### `open-source/contribution-policy/<target>.md`

贡献策略必须包含：

```markdown
# <target> Contribution Policy

## Scope

## Contribution Types

## Triage Labels

## Issue Templates

## Pull Request Requirements

## Review Policy

## Tests / CI

## DCO / CLA

## License / Provenance

## Security Reports

## AI Generated Contributions

## Maintainer Boundaries

## Review Cadence
```

默认规则：

- PR 必须说明目的、测试、影响范围、breaking risk、security/privacy risk、license/provenance。
- 外部贡献默认需要 DCO sign-off 或明确 CLA 机制；没有贡献权利声明的非平凡 PR 不合并。
- AI 生成贡献必须披露，并由贡献者确认其有权提交、已审查、已测试、没有复制未授权代码/数据/文本。
- Security report 不走普通 issue/PR；重定向到 SECURITY/private vulnerability reporting。
- 一人维护者可以关闭不在 scope 的 issue/PR，优先维护核心路径，不承诺 review SLA。

### `open-source/maintainer-runbook/<target>.md`

维护者 runbook 必须包含：

```markdown
# <target> Maintainer Runbook

## Scope

## Support Boundary

## Issue Triage

## Pull Request Review

## Release / Versioning

## Community Conduct

## Saying No / Closing

## Automation

## Pause / Archive Criteria

## Escalation

## Linked Artifacts

## Review Cadence
```

默认规则：

- 每周或每两周固定一次开源维护时间，避免 issue/PR 抢走深度研发时间。
- 只维护少数标签：bug、docs、security、question、good first issue、needs repro、blocked、wontfix、out of scope。
- 没有复现、没有版本、没有最小示例、涉及生产客户支持或安全漏洞的 issue，应按模板请求补充或转渠道。
- 维护者可以暂停新 feature PR、关闭低价值讨论、归档实验项目；但必须写清原因和下一步。
- 行为准则问题、安全报告、法律/IP 争议、客户数据暴露、生产事故必须升级给人判断。

### `open-source/release-security-review/<target>.md`

发布与安全复盘必须包含：

```markdown
# <target> Open Source Release And Security Review

## Scope

## Recent Releases

## Supported Versions

## Release Artifacts

## License / Notice

## Dependency / Vulnerability Checks

## Security Reporting / Advisories

## Provenance / Signing / SBOM

## API / SDK Compatibility

## Open Risks

## One Next Change

## Review Cadence
```

默认规则：

- Public release 前至少跑测试、lint、license check、secret scan、dependency/vulnerability check、package dry-run。
- SDK/CLI/Go module/npm package/Docker image release 必须说明 SemVer、supported versions、deprecation、安全修复策略。
- 如果仓库是客户依赖的官方 SDK 或工具，release notes 连接 W4 developer changelog 和 W2 API compatibility。
- 安全漏洞修复使用 private advisory 或等价流程；patch 发布后再公开细节。
- SLSA/provenance/SBOM/signing 不要求一开始全做，但 public package 至少记录当前级别和下一步。

## Go / Kratos / sqlc / gRPC 默认规则

- Go module 公开前确认 module path、package docs、LICENSE、NOTICE、examples、go test、govulncheck、SemVer/tag 规则。
- Kratos/gRPC SDK 或 example 不包含内部 config、secret、tenant id、生产 endpoint、未发布 proto 或客户数据。
- sqlc schema/query 示例只使用 synthetic fixture；不公开真实业务 schema 中的敏感表名、权限、客户数据或内部迁移计划。
- Protobuf breaking changes 连接 W2 API compatibility；SDK/generated client release 连接 W4 developer docs。
- 公开 repo 的 CI 不应向 fork PR 暴露 secret；外部 PR 只跑安全的 test/lint/build。

## Vite 前端默认规则

- Vite starter/example/template 公开前确认不暴露 server API key、内部 API、analytics token、客户内容、品牌专有素材或未授权图标/字体。
- README 第一屏必须是可运行 quickstart，而不是营销 hero。
- 示例 UI 使用 Vercel/Geist 风格时只参考设计原则，不复制受保护品牌资产或页面。
- 前端 issue 模板收集复现、浏览器、版本、截图可选，不要求用户提交 secret、完整日志或个人数据。
- 公开 demo 不承诺生产 SLA、数据保留、不训练或安全能力，除非W6 对外声明证据专项 已通过。

## AI workflow 默认规则

- 开源 prompt、agent workflow、eval harness、RAG connector、MCP server、tool schema 前，移除 secret、客户数据、内部 system prompt、供应商私有配置和安全绕过样例。
- AI 生成贡献必须被视为第三方来源风险：需要测试、license/provenance review、相似性和安全检查。
- 不接受会增强滥用、绕过安全、泄露 prompt、规避付费、爬取客户数据、批量账号操作的 issue/PR。
- 安全或 abuse-sensitive 报告走 SECURITY/private vulnerability reporting，不在公开 issue 讨论 exploit 细节。
- 开源 AI 示例默认使用 sandbox/local mock/synthetic data，和 W4 开发者体验专项的 developer examples 对齐。

## 需要人判断的关键点

默认不问：

- README 小修、低风险文档 PR、typo、issue 标签、CI 文案、非发布分支上的普通测试修复。

必须问：

- 是否公开新仓库、新 SDK/CLI/template/package、MCP server、prompt/eval/RAG/tool 示例或官方集成。
- 是否接受外部 contributor 的非平凡代码、AI 生成代码、数据、prompt、模型、素材或 license/provenance 不清内容。
- 是否采用或改变许可证、DCO/CLA、治理模型、行为准则执行方式、商标/品牌使用边界。
- 是否承诺 support SLA、security fix window、兼容性、roadmap、商业支持、维护期限或官方推荐。
- 是否处理安全漏洞、private advisory、CVE、exploit、恶意包、依赖高危、secret 泄露、客户数据或内部 prompt 暴露。
- 是否暂停维护、归档、转让维护权、接受新 maintainer、发布 breaking release 或废弃 package。

其他字段完整性、required files、模板章节、状态枚举、敏感内容扫描、positive/negative fixture 和 OpenSpec linkage 由 Codex 与 verifier 处理。

## Review 1：一人公司注意力审查

- 保留：五个工件分别回答“公开了什么、社区入口是否健康、贡献怎么进、维护者怎么处理、发布是否安全”。
- 保留：人只判断公开新项目、许可证/贡献权利、外部非平凡贡献、安全漏洞、支持/维护承诺和归档/移交。
- 调整：不要求基金会治理、OSPO、bug bounty 或大社区运营；先用 GitHub community health + issue/PR template + security path。
- 调整：不把所有 issue 当客服；support boundary 明确 GitHub issue、商业支持、安全报告和生产事故的区别。
- 风险：开源仓库容易吃掉连续研发时间。缓解：maintainer runbook 规定固定维护窗口、scope、wontfix 和 pause/archive 条件。

结论：可落地。一个人可以先为每个公开 repo 写五个工件，把“能维护才公开”变成 release gate。

## Review 2：产品、工程、运维、安全、成本交叉审查

- 产品角度：公开 SDK/example/template 能降低 adoption，但必须避免把 experiment 包装成长期承诺。
- 工程角度：Go/Vite/SDK/CLI release 绑定测试、SemVer、compatibility、license 和 generated artifact gate。
- 运维角度：issue/PR/security report 进入明确队列，不和客户生产事故、support SLA 混在一起。
- 安全隐私角度：SECURITY、private vulnerability reporting、secret scan、dependency checks、fork PR secret 边界和 advisory 流程降低公开仓库风险。
- 成本角度：不追求社区规模；优先维护官方关键路径，明确关闭低价值请求和归档实验项目。

结论：可落地。本专项把开源从“把仓库设成 public”升级为可维护、可贡献、可安全发布的研发 surface。
