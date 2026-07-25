# rd-standards How-To

## 开始

1. 读取根 `README.md`。
2. 选择一个主要分类：立项、产品设计、工程交付或运行维护。
3. 读取该分类 `README.md` 和一个或少数直接相关的项目正文。
4. 将工作分为 Quick、Standard 或 High-risk。

## 执行

### Quick

- 写清一个结果和非目标。
- 做最小可逆变更。
- 运行相关检查并报告剩余风险。
- 不强制创建 OpenSpec。

### Standard

- 实现前创建或继续一个 OpenSpec change。
- 记录 outcome、non-goals、acceptance、scope、risks、verification 和 rollback；`tasks.md` 是执行状态来源。
- 用户可见工作先确定产品行为、体验与关键旅程；OpenSpec 只链接这些输入。
- 需要独立终审。

### High-risk

- 记录 decision owner、影响范围、停止条件和回滚。
- 将准备与真实副作用分开。
- 在生产、删除、付款、外部通信、权限或凭据动作前取得用户明确批准。
- 不可逆设计先由未参与产出的审查者预审；缺少批准、权限或回滚证据时停止。

Standard/High-risk 的代码、配置、schema、API、AI 行为、数据、基础设施或发布设计变更默认使用 OpenSpec。只有用户明确批准并记录 owner、理由、范围和恢复方式时，具体实现才可跳过。

默认单 Agent。只有任务可以独立切分、写域不重叠且有基线证据时，才进行有限并行；主执行者负责整合和验证。

## 验证

运行：

    python tools/verify_rd_standards.py .
    python tools/check_runtime_skill_sync.py .
    openspec validate --all --strict --no-interactive

分别解释结果：正式规范验证只证明四分类十一项、规则追溯、链接与治理入口一致；runtime 验证只证明唯一研发 skill 已同步且旧研发 skill 已清理；OpenSpec validation 只证明格式与规格结构。三者都不能替代真实任务证据或独立审查。

## 更新知识

结构变化后：

1. 更新根入口、受影响的分类与项目正文。
2. 更新 `knowledge/docs-map/rd-standards.json` 和本 context pack。
3. 向 `knowledge/freshness/rd-standards.jsonl` 追加事实记录。
4. 更新治理当前状态和替换证据。
5. 不在多个入口复制同一动态状态。
