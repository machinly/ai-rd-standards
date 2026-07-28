# Tasks

- [x] 从前四轮方案、回灌记录和第三轮仓库树确认目录歧义与既有应用根。
- [x] 创建 Standard OpenSpec change，限定为目录合同、项目地图和验证器。
- [x] 在正式实现与评估条文中区分仓库根和应用根。
- [x] 扩展项目证据验证器与正反回归测试。
- [x] 编写用户服务第五轮全新执行方案，并把目录合同设为编码前门禁。
- [x] 运行 change strict validation、标准完整测试与静态检查。
- [x] 完成 producer self-check 并记录未覆盖项。
- [ ] 由未参与产出的 reviewer 完成 independent final review。
- [ ] 根据 review 处理结论并归档 change，或保持 `changes_requested`。

## Producer self-check（2026-07-27）

- 路由：R&D / Deliver / Standard；本 change 不改变用户界面，`visual_ux: not-required`。
- 视角 A（可执行性）：规则只扩展既有正式条文，不新增 rule-id 或平行规范；验证器提供目录-only 模式；第五轮仍只维护一份实验方案，实施状态后续由一个 OpenSpec `tasks.md` 承载。
- 视角 B（产品/工程风险）：单应用仓库仍可使用根目录；多应用仓库的 Go/Vite 应用根、manifest 和根级私有目录均有正反测试；目录证据没有被描述为产品、运行或 Browser E2E 证据。
- 用户已有工作：未修改第四轮实验文件中的既有未提交内容，未接触或处置目标仓库代码，未触碰 `.superpowers/`。
- 验证：111 项 Python tests 通过；本 change strict validation 通过；全量 OpenSpec 59 passed / 0 failed；正式规范验证通过（4 categories、11 items、2,337 rule IDs、7 review files）；runtime skill sync 通过；pilot record 格式通过；`git diff --check` 无错误。
- 未覆盖：第五轮尚未获用户批准、未执行 Product/UX review、未在目标仓库运行目录 verifier、未产生代码或 Browser E2E；本 standards change 尚无 independent final review，不能归档或声称最终接受。
- Superpowers：0；没有具体复杂度 trigger。Multi-Agent：0；用户未要求或授权。
