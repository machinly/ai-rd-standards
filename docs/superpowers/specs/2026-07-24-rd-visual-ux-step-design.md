# 研发规范增加可视 UX 步骤设计

状态：已实施并通过独立终审
日期：2026-07-24
适用对象：一名产品/研发负责人 + Codex
实施路径：Standard；实施前创建 OpenSpec change

## 1. 修订背景

当前研发规范已有“体验设计”项目，也规定了关键任务、surface、loading/empty/error/success、可访问性、高风险确认和开发后浏览器证据。然而这些要求主要以文字、JSON 和验证规则表达，尚未把“开发前看见并确认界面方案”定义成明确步骤。

因此本轮任务是调整研发规范，在现有“体验设计”中加入轻量的可视 UX 子步骤，并让计划、实现和验证项目消费这个结果。

此前设计把任务扩大成了通用 UX Kit、catalog、schema、revision 算法和专用验证器建设。本版移除这些内容；通用 UX Kit 只有在多个真实项目产生重复需求后，才作为独立 change 评估。

## 2. 目标

修改正式研发规范，使满足触发条件的用户界面变更按以下路径推进：

```text
产品行为已定义
  → 静态低保真 UX
  → 人工确认“可开发”
  → 直接开发
  → 浏览器验证
```

这一调整应做到：

- 开发前可以直接查看关键页面和状态；
- 人在编码前确认任务路径、信息层级和高风险交互；
- 不增加可交互原型阶段；
- 不把局部文案和样式修改拖入完整 UX 流程；
- 延续现有组件复用原则，不在本轮建设通用组件体系；
- 保持现有四分类、十一项目结构不变。

## 3. 非目标

- 不新增第十二个研发项目；
- 不建设通用 UX Kit、组件 catalog 或跨项目设计系统；
- 不建立 manifest schema、专用 renderer 或 UX 工件验证器；
- 不制作可交互原型；
- 不要求 Figma、Penpot 或其他外部设计工具；
- 不建立像素级视觉回归平台；
- 不自动迁移历史项目或历史界面；
- 不改变现有产品方向、风险接受和发布授权边界。

## 4. 在现有研发流程中的位置

可视 UX 是“体验设计”中的一个明确子步骤，不是新的分类或项目。

```text
定义
  ↓
体验设计
  1. 任务与 surface
  2. 可视 UX 线框
  3. 人工 UX review
  ↓
计划
  ↓
实现
  ↓
验证
```

职责边界：

- **定义**：决定用户、问题、行为、范围、非目标和高影响边界；
- **体验设计**：把这些决定变成可见的任务路径、页面结构、状态和用户控制；
- **计划**：确认 UX 输入已经具备，不重新设计界面；
- **实现**：按已确认 UX 直接开发，发现不成立时返回体验设计；
- **验证**：证明实现与已确认 UX 一致，不在验证阶段重新定义产品。

## 5. 触发条件

出现下列任一变化时，必须执行可视 UX 步骤：

- 新增或实质改变关键用户任务；
- 改变页面结构、信息架构、导航或关键 surface 关系；
- 新增或实质改变表单、确认、权限、删除、付款、敏感数据或其他高影响交互；
- 错误、空状态、等待或成功反馈会显著影响用户下一步；
- 桌面与移动端存在实质布局差异。

下列变化默认不触发：

- 不改变含义的文案修正；
- 颜色 token、局部间距和单一控件外观微调；
- 不改变任务、结构、状态和用户控制的低风险样式修复。

Standard/High-risk 在 OpenSpec proposal 中记录 `visual_ux: required | not-required` 及理由。若是否触发存在合理疑问，默认进入可视 UX，而不是在实现中猜测。

## 6. 可视 UX 步骤

### 6.1 输入

进入可视 UX 前至少已有：

- 目标用户和关键任务；
- 本轮改变与不改变的行为；
- 验收和退出条件；
- 权限、数据和高影响边界；
- 已知错误与降级场景。

上游输入不成立时返回“定义”，不能用线框替代产品决定。

### 6.2 最小产物

产物保存在仓库中，默认使用：

```text
ux/<change-id>/
  flow.md
  wireframes/
    <surface>--success.html|svg
    <surface>--loading.html|svg
    <surface>--empty.html|svg
    <surface>--error.html|svg
  review.md
```

已有唯一产品设计目录的项目可以使用等价位置，但同一 change 只能有一个权威入口。

`flow.md` 至少说明：

- 用户目标；
- 入口；
- 正常步骤；
- error、retry、cancel 和 exit；
- non-goals；
- 线框文件索引。

静态 HTML/SVG 线框：

- 只表达布局、信息层级、内容和操作位置；
- 不包含业务逻辑、真实 API、数据写入、脚本或仓库外资源；
- 覆盖关键路径及 loading、empty、error、success；
- 桌面为默认视图；
- 只有布局实质变化时才补移动端线框。

不适用的状态必须在 `flow.md` 中说明理由，不能静默省略。

### 6.3 高保真升级

低保真是默认要求。只有下列场景由人决定是否补高保真：

- 新品牌或营销页面；
- 新视觉语言；
- 信息密度或视觉层级本身构成主要风险；
- 低保真无法支持真实取舍。

高保真是条件升级，不增加可交互原型；确认后仍直接开发。

### 6.4 人工 UX review

`review.md` 至少记录：

```text
Decision owner:
Reviewed at:
Artifacts reviewed:
Decision: approved | changes-requested
Notes:
```

只有明确的人类决定可以产生 `approved`。AI 可以在收到明确决定后记录结果和来源，不能根据沉默、一般授权或后续实现状态推断批准。

人工 review 至少确认：

- 关键任务可以完成；
- 信息层级和下一步清楚；
- loading、empty、error、success 有可行动反馈；
- 高风险动作显示真实影响和退出/撤销边界；
- 移动端差异已经处理或明确不适用；
- 没有由界面静默扩大产品范围。

`approved` 是进入生产性实现的门禁。线框或任务路径在批准后发生实质变化时，必须重新 review；本轮不建设自动 revision/hash 机制。

## 7. 组件复用原则

本轮保留组件化要求，但不建设通用 UX Kit。

可视 UX 和实现应：

1. 优先使用当前项目已有组件、设计 token 和成熟可访问组件；
2. 在线框中用稳定语义名称标出重复区域，例如 `AppShell`、`FormField`、`StatePanel`、`ConfirmAction`；
3. 同一项目内重复出现的交互只实现一次，并通过组合复用；
4. 一次性业务结构保留在当前 change，不为“看起来专业”提前抽象；
5. 采用自定义复杂 widget 而不是原生或成熟组件时，继续服从现有人工判断规则。

跨项目 catalog、通用 pattern ID、晋升机制和共享 renderer 全部留给未来独立 change。只有出现至少两个真实项目的重复建设证据时，才重新评估。

## 8. 计划与实现门禁

### 8.1 计划

对 `visual_ux: required` 的 change，计划必须链接：

- `flow.md`；
- 关键线框；
- 当前 `review.md`。

UX 尚未批准时，计划可以记录技术调查或开放问题，但不能把生产性实现任务标记为 ready。

### 8.2 实现

生产性编码开始前必须确认：

- `visual_ux` 判断存在；
- required 时存在已批准的 review；
- 计划引用的是当前线框；
- 组件复用选择已经说明。

实现中若发现任务路径、状态、权限含义或高风险确认无法成立，停止该路径并返回体验设计。不得只在代码中改变界面，然后把线框当作过期附件。

若实现需要与线框产生实质偏差，应先更新线框并重新 review，再继续相关实现。

## 9. 验证

验证继续使用现有证据体系，不新增专用 UX 工件验证器。

开发后至少：

- 执行关键 Browser E2E；
- 保存桌面截图；
- 布局实质变化时补移动端截图；
- 核对 loading、empty、error、success；
- 执行适用的 keyboard-only、visible focus 和 focus order 检查；
- 对照已批准线框记录实质差异及重新 review 证据。

截图用于核对视觉结构，不替代 Browser E2E。人工 UX review 也不替代 Standard/High-risk 的独立最终审查。

## 10. 正式规范改动范围

实施只修改拥有相应决定的现有入口：

- `docs/02-product-design/README.md`：说明产品设计包含开发前可视 UX；
- `docs/02-product-design/04-experience-design.md`：加入触发、最小产物、状态覆盖、高保真升级和人工 review；
- `docs/03-engineering-delivery/06-planning.md`：加入 UX 输入和 ready 门禁；
- `docs/03-engineering-delivery/07-implementation.md`：加入批准检查和偏差回退；
- `docs/03-engineering-delivery/08-verification.md`：加入对照已批准 UX 的浏览器证据；
- `skills/one-person-openspec-rd/`：只加入路由与 review 检查，不复制正式正文；
- OpenSpec delta：更新 `accessibility-ai-ux-standard`、`ai-coding-workflow-standard` 和 `testing-quality-standard` 的对应要求；
- 现有治理追溯和规则数量按仓库当前验证要求同步更新。

`EXPERIENCE-PLAYBOOK-BOUNDARY` 应明确：轻量静态线框与开发前 review 属于体验设计；完整品牌系统、通用 UX Kit、大型组件库和视觉回归平台仍不属于本轮轻量流程。

## 11. 实施与验证路径

本次规范调整属于 Standard。实施前创建一个 OpenSpec change，并：

1. 写清 outcome、non-goals、acceptance、verification 和 rollback；
2. 先运行 OpenSpec strict validation；
3. 按现有规则更新正式正文、OpenSpec specs、运行时 skill 和追溯记录；
4. 使用至少四个场景检查路由：
   - 文案修正：不触发；
   - 新关键页面流程：触发低保真和人工 review；
   - 高风险删除确认：触发低保真、风险信息和人工 review；
   - 新品牌营销页：触发低保真，并由人决定是否升级高保真；
5. 运行：

```powershell
python tools/verify_rd_standards.py .
python tools/check_runtime_skill_sync.py .
openspec validate --all --strict --no-interactive
```

6. 完成 producer self-check；
7. 由未参与产出的 reviewer 做独立 final review。

本轮不新增 `verify_ux_*` 工具、UX schema、renderer 或通用模板生成器。

## 12. 验收条件

只有同时满足以下条件才算完成：

1. 四分类、十一项目结构保持不变；
2. “体验设计”出现明确的开发前可视 UX 步骤；
3. 触发与不触发边界可通过四个代表场景判断；
4. 规范要求关键路径和四类基本状态具有静态可视产物；
5. 人工 `approved` 成为生产性实现门禁；
6. 批准后的实质变化必须返回体验设计重新 review；
7. 计划、实现、验证只消费对应输入，不复制体验定义；
8. 组件复用作为原则保留，但没有通用 UX Kit 建设内容；
9. 没有可交互原型、外部设计工具或专用 UX 平台依赖；
10. 现有研发规范验证、skill 同步和 OpenSpec strict validation 通过；
11. 独立 reviewer 接受目标 revision。

## 13. 风险与控制

- **小改动也被迫画图**：用关键任务、结构和高风险交互作为窄触发条件。
- **线框沦为事后附件**：把人工批准放在生产性实现之前。
- **实现发现问题后静默改设计**：要求返回体验设计并重新 review。
- **组件化再次扩大成本**：只要求项目内复用，通用 Kit 另立 change。
- **低保真不足以表达视觉风险**：由人在少数适用场景决定升级高保真。
- **截图被误当作功能验收**：保留 Browser E2E、可访问性检查和独立终审。
- **规则在多个入口重复**：体验设计拥有语义，计划/实现/验证和 skill 只记录门禁或引用。

## 14. 回滚

本改造不涉及生产数据。若试用证明流程成本高于收益，可通过后续 Standard change：

1. 把强制触发范围收窄到高风险交互；
2. 保留已有线框和 review 作为历史证据；
3. 移除计划与实现中的通用门禁；
4. 保留现有状态、可访问性和 Browser E2E 要求；
5. 记录停止原因和替代验证方式。

## 15. 决策记录

- 2026-07-23：低保真后直接开发，不增加可交互原型。
- 2026-07-23：关键任务、页面结构和高风险交互触发；局部文案/样式不触发。
- 2026-07-23：静态 UX 产物保存在仓库，使用 Markdown + HTML/SVG。
- 2026-07-23：人工确认“可开发”。
- 2026-07-23：覆盖关键路径及 loading、empty、error、success；移动端按布局差异触发。
- 2026-07-24：任务收窄为调整研发规范，在现有“体验设计”中加入可视 UX 子步骤。
- 2026-07-24：通用 UX Kit、catalog、schema、renderer 和专用 verifier 移出本轮。
- 2026-07-24：用户认可收窄后的设计，可进入实施计划与 Standard change。
