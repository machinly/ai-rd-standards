# 任务

## 1. 来源与约束

- [x] 1.1 查证 Twelve-Factor Config / Dev-Prod Parity。
- [x] 1.2 查证 Google SRE Configuration Design / Specifics / Progressive Rollouts。
- [x] 1.3 查证 Martin Fowler Feature Toggles 和 OpenFeature specification。
- [x] 1.4 查证 Kratos Config、Vite Env and Modes、gRPC Service Config。
- [x] 1.5 补充阶段 14 来源到 `docs/sources/2026-06-23-source-map.md`。

## 2. 配置与 Flag 规范

- [x] 2.1 编写阶段 14 规范正文。
- [x] 2.2 定义 config registry、environment matrix、flag registry、runtime changes、runbook artifacts。
- [x] 2.3 定义 Go/Kratos、Vite、gRPC、AI 配置和 Feature Flag 生命周期规则。
- [x] 2.4 添加两轮一人公司落地 review。

## 3. OpenSpec artifacts

- [x] 3.1 创建阶段 14 change。
- [x] 3.2 编写 proposal。
- [x] 3.3 编写 design。
- [x] 3.4 编写 tasks。
- [x] 3.5 编写 delta spec 和当前 source-of-truth spec。

## 4. Skill 落地

- [x] 4.1 创建 `config-flag-runtime-guard` skill。
- [x] 4.2 添加 config/flag artifacts 验证脚本。
- [x] 4.3 校验 skill。

## 5. 验证

- [x] 5.1 运行 OpenSpec validate。
- [x] 5.2 验证 config/flag 检查脚本的失败和通过路径。
- [x] 5.3 记录当前规范仓库不包含真实服务 config artifacts，因此不连接真实配置平台、secret manager 或 feature flag provider。

验证说明：本仓库是规范仓库，不包含真实生产服务配置 artifacts，也不应在规范阶段连接真实配置平台或 secret manager。已通过 `verify_config_flags.py` 的临时 `ai-assistant` artifacts 正向测试，并确认该脚本会在当前规范仓库上报告缺失 `config/registry`。
