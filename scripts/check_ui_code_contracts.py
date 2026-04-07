#!/usr/bin/env python3
"""
UI source contract guard.

This script enforces the minimum conventions requested by project governance for
the Angular TypeScript slice:
1. every app `.ts` file starts with a file-level intent comment (`/** ... */`)
2. class members (properties/methods) use explicit access modifiers
3. declared methods/functions include an explicit return type annotation
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_APP = ROOT / "ui" / "src" / "app"


HEADER_RE = re.compile(r"^\s*/\*\*")
CLASS_RE = re.compile(r"^\s*export\s+class\s+\w+")
MEMBER_RE = re.compile(r"^  (readonly\s+)?[A-Za-z_]\w*\s*(=|:|\()")
METHOD_RE = re.compile(
    r"^\s*(public|private|protected)\s+(readonly\s+)?(?:async\s+)?([A-Za-z_]\w*)\s*\(([^)]*)\)\s*(?::\s*[^=/{]+)?\s*\{"
)
FUNCTION_RE = re.compile(
    r"^\s*export\s+function\s+[A-Za-z_]\w*\s*\([^)]*\)\s*(?::\s*[^=/{]+)?\s*\{"
)


def main() -> int:
    errors: list[str] = []
    for ts_file in sorted(UI_APP.rglob("*.ts")):
        text = ts_file.read_text(encoding="utf-8")
        rel = ts_file.relative_to(ROOT)
        if not HEADER_RE.search(text):
            errors.append(f"{rel}: missing top-of-file /** intent header")

        in_class = False
        brace_depth = 0
        for lineno, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if CLASS_RE.match(line):
                in_class = True
            if in_class:
                brace_depth += line.count("{")
                brace_depth -= line.count("}")
                if brace_depth <= 0:
                    in_class = False

                if stripped.startswith("@") or not stripped or stripped.startswith("//"):
                    continue
                if stripped.startswith("constructor("):
                    continue

                if brace_depth == 1 and MEMBER_RE.match(line) and not re.match(
                    r"^\s*(public|private|protected)\s+", line
                ):
                    errors.append(f"{rel}:{lineno} class member missing access modifier")

                method_match = METHOD_RE.match(line)
                if method_match and ":" not in line.split(")", 1)[-1]:
                    errors.append(f"{rel}:{lineno} method missing explicit return type")

            function_match = FUNCTION_RE.match(line)
            if function_match and ":" not in line.split(")", 1)[-1]:
                errors.append(f"{rel}:{lineno} function missing explicit return type")

    if errors:
        print("UI code contract check failed:", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print("UI code contract check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
