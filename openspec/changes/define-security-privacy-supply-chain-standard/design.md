# 设计：安全、隐私与供应链基线规范

## 设计决策

### 1. 用四个工件表达最小安全基线

`security/threat-models` 记录攻击面和控制；`security/privacy` 记录数据处理事实；`security/supply-chain` 记录依赖和构建来源；`security/secrets` 记录密钥生命周期。四个文件能被脚本检查，也能让一个人中断后恢复上下文。

### 2. 威胁建模采用四问法

完整 STRIDE/LINDDUN 表对单人项目容易过重。第一版只回答：在做什么、会出什么错、怎么处理、做得够好吗。高风险服务可在此基础上升级。

### 3. 隐私记录聚焦数据流和外部处理方

一人公司最容易漏的是“用户数据被谁处理、保留多久、日志里有什么”。因此 privacy JSON 强制记录 data classes、processors、retention、logging、deletion/export 和 AI data use。

### 4. 供应链记录连接 release gates

安全规范不单独搭平台，而是把 Go `govulncheck`、npm audit/Dependabot、CodeQL/等价 SAST、secret scanning、SBOM/provenance 和 CI 最小权限写入 release gates。

### 5. Secrets 只记录流程，不记录值

`security/secrets/*.md` 只写 storage、access、rotation、CI/CD 和 incident response，不写真实 secret、token、connection string 或可恢复凭据。

### 6. AI 输出默认不可信

模型输出进入工具、SQL、shell、文件、权限、支付或通知前，必须经过 schema 校验、授权和必要人审。prompt injection 和 sensitive information disclosure 默认纳入 threat model。

## 取舍

- JSON/Markdown 工件增加少量书写成本，但能阻止没有安全上下文的生产上线。
- 不强制商业扫描器，降低早期成本；用官方/开源工具作为默认起点。
- 不默认完整合规认证，避免把安全工作变成多月项目。
- 不把 privacy record 当法律意见，只作为工程事实来源和人工 checkpoint 触发器。
