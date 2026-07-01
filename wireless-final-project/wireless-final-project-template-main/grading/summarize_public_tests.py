from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_counts(text: str) -> tuple[int, int, int]:
    passed = failed = errors = 0
    patterns = [
        (r"(\d+)\s+passed", "passed"),
        (r"(\d+)\s+failed", "failed"),
        (r"(\d+)\s+error", "errors"),
        (r"(\d+)\s+errors", "errors"),
    ]
    for pattern, kind in patterns:
        matches = re.findall(pattern, text)
        if matches:
            value = int(matches[-1])
            if kind == "passed":
                passed = value
            elif kind == "failed":
                failed = value
            else:
                errors = value
    return passed, failed, errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("pytest_output.txt")
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    passed, failed, errors = parse_counts(text)
    total = passed + failed + errors
    score = 0 if total == 0 else round(100 * passed / total, 1)

    print("## Wireless Final Project Public Test Summary")
    print()
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print(f"- Errors: {errors}")
    print(f"- Public test score estimate: {score}/100")
    print()
    print("This is the public test result only. The final grade will also use hidden validation tests and document review.")
    print()
    print("<details><summary>pytest output</summary>")
    print()
    print("```text")
    print(text[-12000:])
    print("```")
    print("</details>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
