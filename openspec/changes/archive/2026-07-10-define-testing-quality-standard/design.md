# 设计：测试与质量策略规范

## 设计决策

### 1. 用测试矩阵连接风险与命令

`test-strategy` 给人读，`test-matrix` 给脚本检查。矩阵不追求测试数量，而是把风险、stack、变更类型、测试层级、命令和 release gate 放在一个文件中。

### 2. 采用 small / medium / large，而不是争论 unit / integration 名词

Google 的测试大小分类更适合一人公司落地，因为它关注速度、资源和确定性。规范仍保留 Test Pyramid 的经济原则：多数测试应该快速、低成本、可定位，少数 E2E 保护关键路径。

### 3. 覆盖率只作为提示，不作为目标

覆盖率只能说明代码被执行，不能说明行为被验证。矩阵要求 `coverage_focus` 写清要保护的行为，避免为百分比写无断言测试。

### 4. AI eval 纳入质量矩阵

AI prompt、model、tool、agent route 和 output schema 变化既不是普通 unit test，也不能只靠手工看。矩阵要求代表样例、边界样例、失败样例、自动评分和人工校准。

### 5. Flaky 默认是质量债

retry 可以短期降低噪音，但不能长期替代修复。只要有 quarantine、retry 或已知 flaky，就要求 `flaky-tests` 文件记录 owner、影响和修复日期。

### 6. 人只判断质量例外

普通命令、默认测试组合、缺失字段由 skill 创建和检查。人只判断核心行为、可接受手工验收、是否带例外发布、AI eval 失败处理和 E2E 失败时是否继续发布。

## 取舍

- 增加轻量质量工件，但避免每次变更重新设计测试策略。
- 不要求所有项目有完整 E2E 套件，防止测试维护压垮一个人。
- 不默认 testcontainers、Playwright、AI eval 每次都跑全量，而是按 risk 和 release gate 选择。
- 不把大型测试作为主要缺陷发现手段，降低 flaky 和排障成本。
