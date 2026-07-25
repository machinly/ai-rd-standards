# 用户中心研发规范试验：终止证据回灌

状态：negative experiment evidence；不是用户中心交付记录。
日期：2026-07-10
来源目录：`D:\Workspace\user\docs\rd-experiment-termination\`

## 读取范围与证据指纹

本次按来源 README 指定顺序读取：README、issue-register、current-state、return-to-original-process、evidence、context-pack。来源文件保留在用户中心工作区，本仓库不复制其全文。

| 文件 | SHA-256 |
| --- | --- |
| README.md | `95E8DA21EDB3B97D928A54E6E7C9CA3DDB9DE98877A844531289B1CCB7E56C9F` |
| issue-register.md | `D610B2C76A011E11123682BEBA945AF68DB1AED188A123DBA2D0D6D10F976C60` |
| current-state.md | `843C0BD8B22404987FC47BC0B95D75FC835C568FC21C6C3F03F8F35CD0733CD1` |
| return-to-original-process.md | `993D819430F6FD59A870F30EF2B072EEADBDD3BA96780B9158891BE5A80D78B2` |
| evidence.md | `656B6DD180F87AC13A0F02896B3CC1841E5CC64B8C5CA99553C72CBD7A21B2D1` |
| context-pack.md | `E32BB125CAC265383492C9E3CC9D41B302A8E1AD227FAB7AEEF293CB51283DD9` |

## 已观察事实

1. 来源记录显示实验终止时 UC-005 未提交、未发布，工作区当时被保留；用户随后确认整个用户服务已删除。当前不检查、不恢复也不评价该服务状态。
2. Go/Kratos 根项目是人工按目录规范搭建，不是 Kratos CLI 生成，因此无法证明与批准模板同源。
3. 实现批次 work brief 被当作产品输入，但缺少经人确认的产品范围、用户/管理员流程、错误状态、成功指标和六项高影响决策。
4. Docker 只覆盖 PostgreSQL、OIDC mock 和部分工具/test runner；Go 服务仍在宿主机，两套前端不存在，因此不是完整本地集成环境。
5. Go `httptest`、HTTP/gRPC integration 和 redirect 测试存在，但没有真实浏览器页面 E2E。
6. 独立终审发现一个 migration down P1，以及 profile 并发覆盖、identity-link session 绑定、成功路径覆盖和 Proto/runtime 语义等 P2。
7. 多个结构 verifier 和技术命令曾 PASS，但覆盖范围不足以证明产品正确、全系统 E2E 或发布就绪。
8. startup、上下文量、流程耗时等试验指标没有可靠采集，不能判断注意力成本是否改善。

## 全局整改决定

以下规则由真实失败直接支持，进入默认内核：

- 新用户能力先有权威产品输入、体验设计和验收映射；work brief 只承载执行，不替代产品定义。
- 所有新应用从批准、可版本化的模板生成并保留 provenance。当前 Go 服务使用 Kratos CLI；未来可由自有应用模板取代。禁止手工仿造模板目录。
- 多组件项目必须提供统一、可重复的完整本地集成环境，实际覆盖全部后端、前端、数据库和必要 mock/provider；前端可在宿主机运行，不强制容器化。
- 验证证据必须区分 unit、host integration、dependency-container、complete local integration、browser E2E、provider sandbox 和 production observation。
- auth、数据迁移、管理员权限和难回退契约在实现前进行独立设计审查，完成后再独立终审。
- stopped/terminated 是合法状态；未经授权不提交、推送、重置或删除未完成工作。
- 默认数据栈改为 MySQL + sqlc；SQL 尽量保持 MySQL/PostgreSQL 通用，默认不创建 foreign key，并把引用完整性、并发与孤儿数据验证责任显式交给应用层和一致性检查。

## 不升级为全局规则的项目条件

- 不强制所有组件进入 Compose 或要求前端制作容器镜像；强制的是统一、可重复且组件完整的本地集成入口。
- 具体 Kratos 版本、provider、页面数量和六项产品决策属于目标项目，不写入通用内核。
- 本次失败不能证明旧 W0-W9 更优，因为没有可比路线 A 数据，也没有可靠时间/上下文指标。

## 试验结论

当前数据不能验证最小内核的净收益。更强的结论是：首个真实 High-risk 项目暴露了流程缺口，并出现了独立审查前的高风险遗漏，因此“高风险漏检不增加”的假设没有得到支持。

独立终审确实发现了重要问题，证明 reviewer 分离有价值；但审查发生过晚，不能只保留最终终审而缺少 High-risk 设计前审查。

在完成上述规则修改、同步实际运行时 skill，并重新建立可测量任务记录前，pilot 保持 paused，不继续累计“完成任务”。

## 服务处置边界

用户服务本身已经删除，不是本仓库的整改对象。后续不得把恢复该服务、补齐其功能、检查其工作区或评价其当前可部署性列为待办；只保留已经回灌到研发规范的验证事实与反例。

## 运行时 skill 漂移及处置

回灌时发现：仓库 canonical router 已使用三档路径，但本机已安装副本仍默认 W0-W9/OpenSpec；`go-kratos-sqlc-service` 仍默认 PostgreSQL、按规模强制 OpenSpec，也没有批准模板、完整本地集成和无 foreign key 契约。这证明仓库文档正确不等于新会话实际执行正确规则。

现已同步全局 router 的 `SKILL.md`、三份 references 和 `agents/openai.yaml`；Go service skill 也改为 Kratos CLI/未来批准模板、MySQL + sqlc、通用 SQL、默认无 foreign key、完整本地集成和风险分流的默认 OpenSpec。`tools/check_runtime_skill_sync.py` 会逐文件比较 router，并检查 Go、Vite、quality、knowledge skills 的主体、references、agent 元数据和确定性 verifier 契约。

验证结果：两个 skill 在 `PYTHONUTF8=1` 下通过 skill-creator `quick_validate.py`；Go verifier 的有效 fixture 通过，反向 fixture 能同时拒绝手搓 provenance、PostgreSQL engine、foreign key、ILIKE 和缺失必需前端组件。fixture 已删除，未接触已删除用户服务。
