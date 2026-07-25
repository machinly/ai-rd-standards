from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

from .coverage import RETAINED_TREATMENTS, _target_ids
from .model import CheckResult, ResultStatus
from .records import load_atomic_rules


CATEGORY_FILES = {
    "01-initiation/README.md": "立项",
    "02-product-design/README.md": "产品设计",
    "03-engineering-delivery/README.md": "工程交付",
    "04-operations-maintenance/README.md": "运行维护",
}
ITEM_FILES = {
    "01-initiation/01-topic-selection.md": "选题",
    "01-initiation/02-research.md": "调研",
    "02-product-design/03-definition.md": "定义",
    "02-product-design/04-experience-design.md": "体验设计",
    "03-engineering-delivery/05-technical-design.md": "技术设计",
    "03-engineering-delivery/06-planning.md": "计划",
    "03-engineering-delivery/07-implementation.md": "实现",
    "03-engineering-delivery/08-verification.md": "验证",
    "03-engineering-delivery/09-release.md": "发布",
    "04-operations-maintenance/10-operation.md": "运行",
    "04-operations-maintenance/11-evaluation.md": "评估",
}
CATEGORY_SECTIONS = (
    "分类目的与边界",
    "根本原则",
    "包含的项目",
    "项目之间的关系",
    "进入条件",
    "结束或循环条件",
    "与其他分类的接口",
)
ITEM_SECTIONS = (
    "项目目的与边界",
    "根本原则",
    "核心判断",
    "重新组织后的规范要求",
    "按主题整理的执行细则",
    "输入与产物",
    "完成、停止或退出条件",
    "相关项目引用",
)


def _missing_sections(text: str, required: tuple[str, ...]) -> list[str]:
    return [
        section
        for section in required
        if not re.search(rf"^##\s+{re.escape(section)}\s*$", text, flags=re.MULTILINE)
    ]


def draft_check(root: Path, policy: dict[str, Any]) -> CheckResult:
    del policy  # Current structural contract is fixed by the approved plan.
    root = root.resolve()
    draft_root = root / "rebuild-draft"
    findings: list[str] = []
    root_readme = draft_root / "README.md"
    if not root_readme.is_file():
        findings.append("draft root README missing")
    elif "持续演进" not in root_readme.read_text(encoding="utf-8"):
        findings.append("draft root README lacks continuous evolution relationship")
    category_count = 0
    for relative, category in CATEGORY_FILES.items():
        path = draft_root / relative
        if not path.is_file():
            findings.append(f"category draft missing: {category} ({relative})")
            continue
        category_count += 1
        for section in _missing_sections(
            path.read_text(encoding="utf-8"), CATEGORY_SECTIONS
        ):
            findings.append(f"category {category} missing section: {section}")
    item_count = 0
    item_texts: list[str] = []
    for relative, item in ITEM_FILES.items():
        path = draft_root / relative
        if not path.is_file():
            findings.append(f"item draft missing: {item} ({relative})")
            continue
        item_count += 1
        text = path.read_text(encoding="utf-8")
        item_texts.append(text)
        for section in _missing_sections(text, ITEM_SECTIONS):
            findings.append(f"item {item} missing section: {section}")
    markers: Counter[str] = Counter()
    for text in item_texts:
        markers.update(
            value.strip()
            for value in re.findall(
                r"<!--\s*rule-id:\s*([^>]+?)\s*-->", text, flags=re.IGNORECASE
            )
        )
    rules, rule_findings = load_atomic_rules(root)
    findings.extend(rule_findings)
    required_targets = {
        target
        for rule in rules
        if rule.get("treatment") in RETAINED_TREATMENTS
        for target in _target_ids(rule.get("target_rule_id", ""))
    }
    for target in sorted(required_targets):
        count = markers[target]
        if count == 0:
            findings.append(f"canonical target reference missing: {target}")
        elif count > 1:
            findings.append(f"canonical target reference duplicated: {target}")
    for marker in sorted(set(markers) - required_targets):
        findings.append(f"draft marker has no retained source mapping: {marker}")
    return CheckResult(
        ResultStatus.BLOCKED if findings else ResultStatus.PASS,
        "draft structure and canonical reference check",
        tuple(findings),
        {
            "category_count": category_count,
            "item_count": item_count,
            "canonical_target_count": len(required_targets),
        },
    )
