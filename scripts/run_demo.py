from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agent_lab.evals import load_cases, run_cases
from agent_lab.report import write_html_report, write_json_report


def main() -> None:
    outcomes = run_cases(load_cases(ROOT / "examples" / "tasks.json"))
    write_json_report(ROOT / "artifacts" / "agent-report.json", outcomes)
    write_html_report(ROOT / "artifacts" / "agent-report.html", outcomes)
    passed = sum(outcome.passed for outcome in outcomes)
    print(f"agent_lab_demo passed={passed}/{len(outcomes)}")
    if passed != len(outcomes):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
