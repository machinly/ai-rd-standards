# 仓库原生可视 UX 工件设计

状态：已完成方案确认，待用户审阅书面规格
日期：2026-07-23
适用对象：一名产品/研发负责人 + Codex
实施路径：Standard；实施前创建 OpenSpec change

## 1. 背景

当前研发规范已经要求关键任务、surface、loading/empty/error/success、可访问性、AI 披露、高风险确认和浏览器验证，但体验设计的主要产物仍是 Markdown、JSON 和文字契约。截图又主要出现在开发后的验证阶段，因此缺少一层“开发前可查看、可讨论、可批准”的视觉表达。

这不是体验规则缺失，而是缺少轻量、仓库原生、可版本化的视觉 UX 工件。新方案应补齐这层表达，同时保持一人研发可执行，不引入独立设计工具、可交互原型或大型设计系统。

## 2. 目标

建立一套仓库原生的轻量 UX Kit 和变更级 UX Package，使满足触发条件的用户可见变更：

1. 在开发前具有可直接用浏览器查看的静态低保真线框；
2. 由人确认任务路径、信息层级、关键状态和移动端差异后再开发；
3. 通过稳定的语义模式 ID 连接线框与生产组件，减少重复设计和重复实现；
4. 在设计变化后自动识别旧批准已经失效；
5. 在开发后以 Browser E2E、截图和键盘/焦点证据验证实现；
6. 与现有 OpenSpec、体验设计、实现和验证规则建立单向链接，不复制事实。

## 3. 非目标

- 不制作可交互原型；
- 不要求 Figma、Penpot 或其他外部设计工具；
- 不建设完整品牌系统、大型组件库或专门设计团队工作流；
- 不建立像素级视觉回归平台；
- 不把低保真线框变成生产代码；
- 不要求局部文案、颜色、间距或其他不改变任务、结构和状态的修改创建 UX Package；
- 不以 UX 人工批准替代工程独立终审、可访问性验证或 Browser E2E；
- 不在本设计阶段修改正式规范、运行时 skill、验证器或 OpenSpec 主规格。

## 4. 已确认的产品决定

### 4.1 渐进路径

默认路径是：

```text
静态低保真线框 → 人工确认“可开发” → 直接开发 → 浏览器验证
```

不存在可交互原型阶段。只有品牌页、营销页、新视觉语言或信息层级存在较高视觉风险时，才在线框确认和开发之间增加高保真视觉稿。

### 4.2 触发范围

出现下列任一变化时必须创建并批准 UX Package：

- 新增或实质改变关键用户任务；
- 改变页面结构、信息架构、导航或关键 surface 关系；
- 新增或实质改变高风险确认、权限、删除、付款、敏感数据或其他高影响交互。

仅修改文案、颜色 token、局部间距或不改变任务、结构和状态的样式时，可记录 `visual_ux: not-required` 及理由后直接开发。Standard/High-risk 将该决定写入 OpenSpec proposal；Quick 写入当前任务记录或提交说明，不为此单独创建流程文件。若是否触发存在合理疑问，默认进入 UX Package，而不是在实现中猜测。

本设计不创建新的事故或紧急绕过规则；真实事故处置继续服从现有运行和 High-risk 边界。

### 4.3 人工门禁

触发 UX Package 的工作只有在决策人批准当前工件 revision 后才能进入生产性开发。AI 可以生成、组合、检查和修订线框，但不能替人决定关键任务、信息层级、高风险交互或是否可开发。

## 5. 权威边界

三类事实保持分离：

| 事实 | 权威位置 | 责任 |
| --- | --- | --- |
| 产品与体验意图 | `product/ux/` | 任务流、surface、线框、语义模式引用和人工批准 |
| 生产实现 | 源码与生产组件目录 | 实际行为、组件组合、样式和运行状态 |
| 验证证据 | `governance/quality/` 及现有验证工件 | Browser E2E、截图、键盘/焦点、独立终审和当前结论 |

`product/ux/` 保存产品输入，不属于通用 guard 或流程账本。OpenSpec 只链接本次 UX Package，不复制 journey、线框或批准内容。`governance/quality/user-journeys.json` 继续保存验证用关键旅程，只引用已批准 UX Package，不成为第二份体验定义。

## 6. 目标目录

目标项目使用以下默认结构：

```text
product/ux/
  kit/
    catalog.yaml
    wireframe.css
    patterns/
      shell-app.html
      form-field.html
      feedback-state.html
  changes/<change-id>/
    journey.md
    manifest.yaml
    wireframes/
      <surface>--success.html
      <surface>--loading.svg
      <surface>--empty.svg
      <surface>--error.svg
    visuals/                  # 仅高保真触发时存在
    approval.md
```

v1 使用固定的 `product/ux/` 根目录，不增加路径配置层。现有项目若已有等价且唯一的产品 UX 事实源，应在迁移 change 中显式决定是否迁移；不得长期保留两套权威目录。

## 7. 工件职责

### 7.1 `journey.md`

每个 UX Package 只有一份任务流文档，至少包含：

- outcome；
- target user；
- entry condition；
- critical task；
- normal steps；
- error、retry、cancel 和 exit 分支；
- non-goals；
- 需要人的产品决定。

进入 `review-ready` 时不得仍有未决的产品方向或高风险交互含义。实现细节不写入此文件。

### 7.2 `manifest.yaml`

`manifest.yaml` 是机器可核查索引，不替代线框或任务流。顶层至少包含：

- `schema_version`；
- `change_id`；
- `owner`；
- `journey_ref`；
- `kit_revision`；
- `surfaces`；
- `high_fidelity`。

每个 surface 至少包含：

- `id`；
- `critical_tasks`；
- `viewports`；
- `responsive_change`；
- `states`；
- `patterns`。

`states` 必须逐项定义 `loading`、`empty`、`error` 和 `success`。每一项要么指向静态 HTML/SVG 工件，要么声明 `not_applicable` 并给出具体理由；不得省略键值。桌面是默认 viewport。只有布局发生实质变化时才要求移动端线框，并只补发生结构差异的状态。

`high_fidelity` 使用以下语义：

```yaml
high_fidelity:
  required: false
  reason: "No brand, marketing, visual-language, or hierarchy risk"
  artifacts: []
```

当 `required: true` 时，`artifacts` 必须引用 `visuals/` 中的文件，且这些文件进入批准 revision。

一个最小 surface 的索引格式如下：

```yaml
surfaces:
  - id: account-settings
    critical_tasks:
      - update-profile
    viewports:
      - desktop
    responsive_change: false
    states:
      loading:
        artifact: wireframes/account-settings--loading.svg
      empty:
        artifact: wireframes/account-settings--empty.svg
      error:
        artifact: wireframes/account-settings--error.svg
      success:
        artifact: wireframes/account-settings--success.html
    patterns:
      - id: shell.app
        scope: kit
      - id: local.update-profile.profile-form
        scope: local
```

`scope` 只允许 `kit` 或 `local`。`not_applicable` 状态使用 `{not_applicable: true, reason: "<具体原因>"}` 代替 `artifact`，二者不能同时存在。

### 7.3 `wireframes/`

线框使用静态 HTML 或 SVG：

- 只表达布局、信息层级、文案占位、操作位置和状态；
- 不包含业务逻辑、真实 API、数据写入、网络请求或用户跟踪；
- HTML/SVG 不包含脚本、事件处理器或仓库外资源；
- HTML 默认引用共享 `wireframe.css`；SVG 使用同一组低保真视觉 token；
- 语义模式引用以 `manifest.yaml` 为权威，不要求验证器解析展示标记；
- 每个文件能通过本地静态 HTTP 服务或仓库预览工具打开。

线框不是像素契约。生产实现可以采用不同的内部组件组合，但不得改变已批准的任务、层级、状态或风险含义。

### 7.4 `approval.md`

`approval.md` 使用 YAML front matter 保存机器可核查字段，正文保存人的说明：

```markdown
---
schema_version: "1.0"
change_id: "<change-id>"
decision: "approved"
decision_owner: "<human>"
decision_source: "<explicit human decision reference>"
reviewed_at: "<ISO-8601 timestamp>"
target_revision: "sha256:<hex>"
---

## Notes

Approved for development.
```

`decision` 只允许：

- `approved`；
- `changes-requested`；
- `rejected`。

只有人的明确决定可以授权 `approved`。AI 可以在收到明确用户决定后原样落盘，并把可定位的决定来源写入 `decision_source`；不得根据沉默、先前的一般授权或实现状态推断批准。`approval.md` 保存当前决定，历史决定由 Git 保留。

## 8. 轻量 UX Kit

### 8.1 Kit 内容

UX Kit 只保存跨变更复用的语义模式、低保真样式和参考片段，不保存具体业务页面。首批模式限定为高频基础项：

- `shell.app`；
- `navigation.primary`；
- `form.field`；
- `data.table`；
- `feedback.state`；
- `action.confirm`。

不在 v1 预先建立更多模式。真实变更先使用 change-local 组合，出现重复后再晋升。

v1 不实现 wireframe 编译器、组件运行时或专门构建链。`patterns/*.html` 是可复用的参考片段，`wireframe.css` 提供共享视觉原语，真正稳定的复用契约由 catalog ID、状态、可访问性约束和生产映射承担。只有真实使用证明静态组合成本仍然过高时，才通过后续 change 评估生成器。

### 8.2 `catalog.yaml`

每个 kit pattern 至少记录：

- `id`；
- `name`；
- `purpose`；
- `status`；
- `states`；
- `accessibility_contract`；
- `example_ref`；
- `implementation_refs`；
- `replacement_id`。

`status` 只允许 `active` 或 `deprecated`。弃用模式必须给出 `replacement_id`；没有替代项时需给出保留理由。`implementation_refs` 可以指向一个组件，也可以指向多个组件的组合，不能为了追求一比一映射而制造巨型生产组件。

模式 ID 使用小写点分命名并保持稳定，例如 `form.field`。展示名称、参考片段和内部实现可以变化，但已有 ID 不重命名。生产代码不需要携带运行时 `data-*` 属性；映射保存在 catalog 或验证证据中，避免把设计治理耦合进运行时。

### 8.3 两次复用规则

一次性业务结构保留在 UX Package 中，并使用 `local.<change-id>.<name>` 标识。只有同一模式在至少两个独立 surface 或 change 中表达相同任务与状态契约时，才提议晋升到 kit。

晋升不是自动动作。维护者必须确认：

- 两个使用场景的目的确实相同；
- 状态和可访问性契约可以稳定复用；
- 抽象不会隐藏重要业务差异；
- 生产映射不会形成巨型组件。

## 9. Revision 与批准失效

### 9.1 Kit revision

验证器对 `catalog.yaml`、`wireframe.css` 和当前 manifest 引用的 kit pattern 文件计算聚合 SHA-256。聚合算法为：

1. 使用相对 `product/ux/` 的 POSIX 路径；
2. 按路径字典序排序；
3. 为每个文件生成 `<file-sha256>  <relative-path>\n`；
4. 对连接后的 UTF-8 字节再次计算 SHA-256；
5. 写成 `sha256:<hex>`。

该值必须等于 `manifest.yaml` 中的 `kit_revision`。

### 9.2 Target revision

`target_revision` 使用同一聚合算法，但输入限定为：

- `journey.md`；
- `manifest.yaml`；
- manifest 引用的全部 `wireframes/` 文件；
- `high_fidelity.required: true` 时引用的全部 `visuals/` 文件。

`approval.md` 不参与计算，避免自引用。由于 manifest 已包含 `kit_revision`，当前 UX Package 同时绑定所用 kit 版本。

### 9.3 失效规则

验证器每次重新计算当前 revision：

- 当前 revision 与最新 `approved` 的 `target_revision` 相等时，开发门禁通过；
- 任一受控文件或所用 kit 内容变化时，门禁状态派生为 `stale`；
- `stale` 不改写历史 approval，但不能作为当前开发依据；
- 修订后必须重新运行校验并由人重新批准。

`draft`、`review-ready`、`approved` 和 `stale` 都是根据工件和校验结果派生的状态，不再维护第二份手工状态文件。

## 10. 端到端工作流

1. 判断是否触发可视 UX；未触发时记录 `visual_ux: not-required` 和理由。
2. 触发时创建 `product/ux/changes/<change-id>/`。
3. 先写 `journey.md`，再确定 surface 和四类状态。
4. 从 UX Kit 选择适用模式；一次性组合使用 change-local ID。
5. 生成静态 HTML/SVG 线框和 `manifest.yaml`。
6. 运行 UX 工件校验器。只有结构、引用、状态和 revision 全部有效时进入 `review-ready`。
7. 人在浏览器中查看线框，并在 `approval.md` 对当前 revision 作出决定。
8. 只有当前 revision 为 `approved` 时进入生产性开发。
9. 实现者沿用语义模式及交互契约；生产组件可以是一对一或组合映射。
10. 实现发现任务、状态或风险含义无法成立时，停止该路径，返回 UX Package 修改并重新批准。
11. 开发完成后执行关键 Browser E2E、截图、键盘/焦点和适用的可访问性验证。
12. 独立 reviewer 对照已批准 UX Package 和当前实现作最终审查。

## 11. 异常和偏差处理

| 情况 | 处置 |
| --- | --- |
| 缺少文件、四类状态、viewport 判断或模式引用 | 阻止 `review-ready`，补齐后重新校验 |
| 引用未知或已弃用且无替代说明的 kit ID | 阻止 `review-ready` |
| revision 与批准不一致 | 状态为 `stale`，阻止进入开发 |
| 实现发现线框无法成立 | 返回体验设计，修改并重新批准 |
| 实现与线框存在合理偏差 | 调整实现，或更新 UX Package 并重新批准；不得只在 review 备注中放行 |
| 新组合只服务一个业务场景 | 保留 change-local，不进入 kit |
| 同一 local 模式在至少两个场景重复 | 提出晋升评审；不自动创建共享组件 |
| 高保真风险在开发中才被发现 | 停止视觉相关实现，补充 `visuals/` 并重新批准 |

## 12. 验证设计

### 12.1 开发前 UX 工件校验

新增单一职责的验证器，至少检查：

- 目录和必需文件存在；
- YAML front matter 和 manifest schema 可读取；
- 每个关键 surface 定义 loading、empty、error、success；
- `not_applicable` 具有非空理由；
- 所有工件引用存在且位于当前 UX 根目录内；
- pattern ID 存在、状态可用或明确为 change-local；
- desktop 基线存在；
- `responsive_change: true` 时存在相应 mobile 线框；
- high-fidelity 决定与工件一致；
- `kit_revision` 和 `target_revision` 计算正确；
- 最新人工决定对当前 revision 有效。

验证器必须提供正向 fixture，并为缺状态、未知模式、缺文件、路径逃逸、错误 revision 和 stale approval 提供负向 fixture。

### 12.2 开发后验证

开发后证据至少包括：

- 对关键任务执行可重复 Browser E2E；
- 保存桌面截图；
- 仅在布局实质变化时保存移动端截图；
- 对关键路径执行 keyboard-only、visible focus 和 focus order 检查；
- 核对 loading、empty、error、success 的实际行为；
- 记录生产组件与语义模式 ID 的映射；
- 记录已批准设计与实现之间的任何差异及其重新批准证据。

线框是结构和行为基准，不执行像素级 diff。截图用于人工核对和未来回归证据，不能单独替代 Browser E2E。

### 12.3 独立终审

Standard/High-risk 的独立 reviewer 必须：

- 未参与 UX Package 或实现的产出；
- 从干净完整环境运行关键旅程；
- 读取当前批准 revision，而不是历史批准摘要；
- 检查实现没有静默改变任务、状态、风险或退出方式；
- 区分 Browser E2E、人工截图检查和可访问性 smoke 的证据层级；
- 记录 target revision、证据、结论和剩余风险。

## 13. 与现有规范的集成

实施时按单一权威原则修改：

- `docs/02-product-design/04-experience-design.md`：拥有触发条件、UX Kit、UX Package、状态覆盖和人工批准；
- `docs/03-engineering-delivery/07-implementation.md`：拥有当前批准 revision 门禁、生产组件映射和发现缺口时回退；
- `docs/03-engineering-delivery/08-verification.md`：拥有校验器、Browser E2E、截图、键盘/焦点和独立终审证据；
- `skills/one-person-openspec-rd/`：只增加路由和链接，不复制上述规则；
- OpenSpec delta：分别更新 `accessibility-ai-ux-standard`、`ai-coding-workflow-standard` 和 `testing-quality-standard` 的对应要求。

实现性改造本身属于 Standard：创建一个 OpenSpec change，写清 outcome、non-goals、acceptance、verification 和 rollback，运行 strict validation，并由未参与产出的 reviewer 做最终审查。

## 14. 实施范围

后续实施计划应覆盖：

1. OpenSpec change 及三项 delta spec；
2. 正式规范与运行时 skill 的最小同步修改；
3. UX Kit 和 UX Package 的模板；
4. schema、验证器、正负 fixtures 和单元测试；
5. 一个代表性示例 UX Package；
6. 文档链接、现有研发规范验证和 strict OpenSpec validation；
7. producer self-check 与独立 final review。

首版不自动迁移历史项目，不扫描外部仓库，也不批量生成业务线框。

## 15. 验收条件

只有同时满足以下条件，实施才可宣称完成：

1. 触发条件和 `not-required` 边界在体验设计中明确；
2. 用户可从模板创建仓库内 UX Package，无需外部设计工具；
3. 示例包含关键任务及 loading、empty、error、success；
4. 示例使用至少一个 kit pattern 和一个 change-local pattern；
5. 人工批准绑定当前 target revision；
6. 修改任一受控工件后，验证器能识别 approval 已 stale；
7. 缺状态、未知 pattern、缺文件、路径逃逸和错误 revision 的 fixtures 均失败；
8. 有效 fixture 通过并可在浏览器中查看；
9. 实现门禁、回退和开发后验证分别由正确的正式项目拥有；
10. 不引入可交互原型、外部设计工具或像素级视觉回归依赖；
11. 现有研发规范验证、相关单元测试和 OpenSpec strict validation 通过；
12. 独立 reviewer 接受目标 revision。

## 16. 风险与控制

- **流程成本扩散到小改动**：用窄触发条件和 `visual_ux: not-required` 保持 Quick 路径。
- **为组件化而过度抽象**：一次性组合留在 change-local，至少两次真实复用才评审晋升。
- **线框与当前设计脱节**：批准绑定内容 revision，任何受控变化都会使门禁 stale。
- **共享 kit 变化破坏既有批准**：manifest 绑定 kit revision，验证器重新计算。
- **低保真不足以表达品牌风险**：只在品牌、营销、新视觉语言或高信息层级风险时升级高保真。
- **设计批准被误当作工程验收**：Browser E2E、可访问性检查和独立终审保持独立。
- **HTML 线框引入执行或供应链风险**：禁止交互脚本、网络请求和外部资源。
- **验证器演变为第二份规范**：验证器只检查结构、引用、枚举和 revision；产品语义仍由正式规范与人工批准拥有。

## 17. 回滚

本改造不改变生产数据或运行系统。若试用后流程成本高于收益，可通过后续 Standard change：

1. 停止新增 UX Package；
2. 保留已有 `product/ux/` 作为历史设计证据；
3. 移除实现入口中的强制门禁；
4. 保留正式规范的关键状态、可访问性和 Browser E2E 要求；
5. 记录停止原因、受影响项目和替代验证方式。

不得删除已有人工批准和已被实现引用的 UX Package；其历史关系继续通过 Git 和验证证据追溯。

## 18. 决策记录

- 2026-07-23：选择“关键 UX 变化触发”，不要求所有用户可见修改创建线框。
- 2026-07-23：选择仓库内 Markdown + 静态 HTML/SVG，不使用外部设计工具。
- 2026-07-23：选择人工“可开发”门禁。
- 2026-07-23：选择关键路径与 loading/empty/error/success 覆盖；移动端按真实布局差异触发。
- 2026-07-23：选择共享语义 UX 模式目录，并以两次真实复用作为晋升条件。
- 2026-07-23：取消可交互原型，批准后直接开发。
- 2026-07-23：高保真仅按品牌、营销、新视觉语言或高视觉风险触发。
