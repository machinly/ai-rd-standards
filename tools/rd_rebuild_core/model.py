from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class ResultStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    TOOL_ERROR = "TOOL_ERROR"


EXIT_CODES = {
    ResultStatus.PASS: 0,
    ResultStatus.WARN: 0,
    ResultStatus.BLOCKED: 1,
    ResultStatus.REVIEW_REQUIRED: 2,
    ResultStatus.TOOL_ERROR: 3,
}

STATUS_PRIORITY = {
    ResultStatus.PASS: 0,
    ResultStatus.WARN: 1,
    ResultStatus.REVIEW_REQUIRED: 2,
    ResultStatus.BLOCKED: 3,
    ResultStatus.TOOL_ERROR: 4,
}


@dataclass(frozen=True)
class CheckResult:
    status: ResultStatus
    summary: str
    findings: tuple[str, ...] = ()
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def exit_code(self) -> int:
        return EXIT_CODES[self.status]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "exit_code": self.exit_code,
            "summary": self.summary,
            "findings": list(self.findings),
            "evidence": self.evidence,
        }


def combine_results(
    results: Iterable[CheckResult], summary: str = "combined checks"
) -> CheckResult:
    items = list(results)
    if not items:
        return CheckResult(
            ResultStatus.BLOCKED,
            summary,
            ("no checks were run",),
            {"check_count": 0},
        )
    status = max((item.status for item in items), key=STATUS_PRIORITY.__getitem__)
    findings = tuple(
        finding for item in items for finding in item.findings
    )
    return CheckResult(
        status,
        summary,
        findings,
        {
            "check_count": len(items),
            "results": [item.to_dict() for item in items],
        },
    )


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", text=True
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
