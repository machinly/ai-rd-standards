# 提案：定义测试与质量策略规范

## 意图

为一人公司建立风险驱动的测试与质量基线，让每个生产服务、前端应用或用户可见 AI workflow 都能说明要保护的核心行为、测试组合、运行命令、AI eval、flaky 处理和质量例外人审点，避免只靠手工试用或覆盖率数字获得虚假信心。

## 范围

- 定义 `quality/test-strategy`、`quality/test-matrix`、`quality/test-runs`、`quality/flaky-tests` artifacts。
- 定义 small、medium、large、contract、smoke、manual exploratory 的一人公司测试组合。
- 定义 Go/Kratos/sqlc/gRPC、Vite、Playwright、AI eval 的默认质量门禁。
- 定义 flaky、coverage、race、fuzz、sqlc verify、AI eval 失败的处理策略。
- 定义质量例外的人工 checkpoint。
- 创建测试质量落地 skill 和检查脚本。

## 不做

- 不建立独立 QA 部门流程。
- 不要求所有改动都写完整测试策略。
- 不把覆盖率百分比作为唯一质量门槛。
- 不强制购买商业测试、设备云或 A/B 平台。
- 不替代 W6 发布流水线和 W3 AI eval 规范，而是为它们提供测试设计依据。

## 依据

- 《人月神话》：质量不能靠银弹解决，测试要服务于概念完整性和变更信心。
- 小型项目管理：只保留一个人能维护、能减少返工的质量工件。
- Martin Fowler Practical Test Pyramid。
- Google Software Engineering at Google, Testing Overview / Larger Testing；Google Testing Blog Test Sizes。
- Gerard Meszaros, xUnit Test Patterns。
- Go testing、fuzzing、race detector 官方文档。
- sqlc vet / verify 官方文档。
- Vitest、Playwright 官方文档。
- OpenAI eval best practices、prompt engineering、agent evals。

## 需要人的判断

建议默认：任何超过 1 个工作日的用户可见变更必须有 `quality/test-strategy/<target>.md` 和 `quality/test-matrix/<target>.json`。允许跳过 race、sqlc verify、Playwright、AI eval 或带已知 flaky 发布时，必须在人审点记录原因和回滚方式。
