# 实现：工作区、模板与 AI coding

## 规范要求

<!-- rule-id: IMPL-REPRODUCIBLE-WORKSPACE -->
- 本地命令与模板来源须可复现。

<!-- rule-id: IMPL-NEW-APP-APPROVED-TEMPLATE -->
- 所有新应用先在项目地图声明的空应用根目录使用当前批准模板生成；模板命令必须显式指向该应用根。禁止覆盖既有非空应用根，禁止在多应用仓库的聚合根直接生成某个应用，也禁止手工仿造目录后声称来自模板。

<!-- rule-id: IMPL-KRATOS-TEMPLATE-PROVENANCE -->
- Go 服务的模板 provenance 须保存 CLI 版本、`kratos new` 命令、模板来源或 revision 与初始文件清单。

<!-- rule-id: IMPL-OWN-TEMPLATE-PROVENANCE -->
- 使用已批准自有应用模板时，须记录模板版本与生成参数。

<!-- rule-id: IMPL-COMPLETE-LOCAL-ENVIRONMENT -->
- 多组件项目须有统一入口，启动产品要求的全部后端、全部前端、MySQL 与必要 mock/provider，并支持日志定位和清理。

<!-- rule-id: IMPL-LOCAL-COMMAND-CATALOG-FIELDS -->
- 本地 command catalog 须记录组件清单、端口、健康条件、启动顺序、失败诊断与一键清理。

<!-- rule-id: IMPL-WORKSPACE-ARTIFACT-PATHS -->
- 工作区工件缺省位于 `dev-workspace/workspace-map/<target>.json`、`dev-workspace/command-catalog/<target>.md`、`dev-workspace/local-environment/<target>.md` 与 `dev-workspace/seed-fixtures/<target>.md`。

<!-- rule-id: IMPL-AI-CODING-ARTIFACT-PATHS -->
- AI coding 工件缺省位于 `ai-coding/implementation-brief/<change-id>.md` 与 `ai-coding/batch-log/<change-id>.md`。

<!-- rule-id: IMPL-TOOLCHAIN-PROVENANCE -->
- 工作区须记录 Go、Node、sqlc、protoc、buf、Vite、OpenSpec 等实际工具链的来源与 install check。

<!-- rule-id: IMPL-APP-TEMPLATE-RECORD -->
- 创建应用时须记录模板名称、版本或 revision、生成命令与初始 diff。

<!-- rule-id: IMPL-LOCAL-ENVIRONMENT-RECORD -->
- 完整本地集成环境须记录组件清单、统一启动命令、就绪命令与清理命令。

<!-- rule-id: IMPL-COMMAND-CATALOG-COVERAGE -->
- command catalog 须覆盖 setup、generate、develop、test、verify、run local、reset、debug 与 release prep 命令。

<!-- rule-id: IMPL-AI-FIXTURE-CASES -->
- AI fixtures 须包含代表样例与失败样例。

<!-- rule-id: IMPL-IMPLEMENTATION-BRIEF-FIELDS -->
- implementation brief 须链接 OpenSpec change、context sources 与 target files，并记录 allowed autonomy、human checkpoints 与 stop conditions。

<!-- rule-id: IMPL-ONE-STEP-LOCAL-VERIFY -->
- 工作区至少须提供一个 one-step local verify 命令。

<!-- rule-id: IMPL-TRIGGERED-VERIFY-COMMANDS -->
- 实现触发 sqlc、Proto 或 AI eval 时，须补对应 verify 命令；验证结论由验证项目维护。

<!-- rule-id: IMPL-REPEATED-AI-ERROR-AUTOMATION -->
- AI 反复犯同类错误时，须更新适用的 skill、script、template 或仓库指令。

<!-- rule-id: IMPL-REAL-EXTERNAL-RESOURCE-HUMAN-GATE -->
- 本地命令会调用真实供应商、真实模型、真实支付、真实邮件或真实生产数据时，须交由人工判断。

<!-- rule-id: IMPL-DESTRUCTIVE-ONE-CLICK-HUMAN-GATE -->
- 把破坏性 reset、migration、backfill、生产发布或 tool commit 暴露成一键命令须交由人工判断。
