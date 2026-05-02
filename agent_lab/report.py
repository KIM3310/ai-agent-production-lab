from __future__ import annotations

import json
from dataclasses import asdict
from html import escape
from pathlib import Path

from .evals import EvalOutcome


def write_json_report(path: Path, outcomes: list[EvalOutcome]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps([asdict(outcome) for outcome in outcomes], indent=2), encoding="utf-8")


def write_html_report(path: Path, outcomes: list[EvalOutcome]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(
        "<tr>"
        f"<td>{escape(outcome.name)}</td>"
        f"<td>{'pass' if outcome.passed else 'fail'}</td>"
        f"<td>{escape(', '.join(outcome.tools_seen))}</td>"
        f"<td>{outcome.estimated_tokens}</td>"
        f"<td>{outcome.estimated_cost_usd:.6f}</td>"
        "</tr>"
        for outcome in outcomes
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Agent Lab Report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; color: #172026; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccd3da; padding: 0.5rem; text-align: left; }}
    th {{ background: #f4f6f8; }}
  </style>
</head>
<body>
  <h1>Agent Lab Report</h1>
  <p>Deterministic eval report generated from local fixtures.</p>
  <table>
    <thead><tr><th>Case</th><th>Status</th><th>Tools</th><th>Tokens</th><th>Cost</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
