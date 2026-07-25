# QA 视角

> 状态：可选角色视角，不是必设岗位或默认 Agent。仅在 Standard/High-risk 需要独立验证设计时读取。

## 关注问题

- acceptance 是否可以被真实验证？
- 测试是否覆盖风险，而不只是代码路径？
- 是否有代表、边界、失败和回滚样例？
- 跳过、flaky 和已知缺口是否透明？
- 执行者是否修改了验收标准来让结果通过？

## 最小输出

- risk-based test matrix；
- executed evidence；
- failures and skipped checks；
- residual risk；
- accept / changes-requested / reject recommendation。

最终 QA reviewer 不得是产出生产者。
