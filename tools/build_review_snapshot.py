#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

MANIFEST_REL = "reviews/2026-07-10-rd-standards-snapshot-manifest.json"
PACKET_REL = "reviews/2026-07-10-rd-standards-independent-review-packet.md"
EXCLUDED_FILES = {MANIFEST_REL, PACKET_REL}


def included_files(root: Path) -> list[tuple[str, Path]]:
    result: list[tuple[str, Path]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        parts = Path(rel).parts
        if ".git" in parts or "__pycache__" in parts:
            continue
        if path.suffix.lower() in {".pyc", ".pyo"}:
            continue
        if rel in EXCLUDED_FILES:
            continue
        if path.is_symlink():
            raise RuntimeError(f"Refusing symlink in review snapshot: {rel}")
        result.append((rel, path))
    return sorted(result, key=lambda item: item[0])


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_payload(root: Path) -> dict[str, Any]:
    records: list[dict[str, str]] = []
    tree = hashlib.sha256()
    for rel, path in included_files(root):
        digest = file_sha256(path)
        records.append({"path": rel, "sha256": digest})
        tree.update(f"{rel}\t{digest}\n".encode("utf-8"))
    return {
        "schema_version": 1,
        "algorithm": "sha256 of UTF-8 path<TAB>file_sha256<LF>, paths sorted by Unicode code point",
        "root": ".",
        "excluded": [
            MANIFEST_REL,
            PACKET_REL,
            ".git/**",
            "**/__pycache__/**",
            "**/*.pyc",
            "**/*.pyo",
        ],
        "file_count": len(records),
        "tree_sha256": tree.hexdigest(),
        "files": records,
    }


def write_manifest(root: Path, payload: dict[str, Any]) -> None:
    target = root / MANIFEST_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or verify the content-addressed remediation review snapshot."
    )
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    payload = build_payload(root)
    manifest_path = root / MANIFEST_REL

    if args.check:
        try:
            expected = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            print(f"SNAPSHOT_VALID=FAIL error={exc}")
            return 1
        if expected != payload:
            print(
                "SNAPSHOT_VALID=FAIL "
                f"expected_tree={expected.get('tree_sha256')} "
                f"actual_tree={payload['tree_sha256']} "
                f"expected_files={expected.get('file_count')} "
                f"actual_files={payload['file_count']}"
            )
            return 1
        print(
            "SNAPSHOT_VALID=PASS "
            f"tree=sha256:{payload['tree_sha256']} files={payload['file_count']}"
        )
        return 0

    write_manifest(root, payload)
    print(
        "SNAPSHOT_WRITTEN=PASS "
        f"path={MANIFEST_REL} tree=sha256:{payload['tree_sha256']} "
        f"files={payload['file_count']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
