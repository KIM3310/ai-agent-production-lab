from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .runtime import AgentRuntime, default_tools


@dataclass(frozen=True)
class EvalCase:
    name: str
    task: str
    expected_tools: tuple[str, ...]
    expected_answer_contains: tuple[str, ...]


@dataclass(frozen=True)
class EvalOutcome:
    name: str
    passed: bool
    tools_seen: tuple[str, ...]
    answer: str
    estimated_tokens: int
    estimated_cost_usd: float


def load_cases(path: Path) -> list[EvalCase]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        EvalCase(
            name=item["name"],
            task=item["task"],
            expected_tools=tuple(item.get("expected_tools", [])),
            expected_answer_contains=tuple(item.get("expected_answer_contains", [])),
        )
        for item in raw["cases"]
    ]


def run_cases(cases: list[EvalCase]) -> list[EvalOutcome]:
    runtime = AgentRuntime(default_tools())
    outcomes: list[EvalOutcome] = []
    for case in cases:
        result = runtime.run(case.task)
        tools_seen = tuple(tool.name for tool in result.tool_results if tool.ok)
        tools_ok = all(tool in tools_seen for tool in case.expected_tools)
        answer_ok = all(fragment in result.answer for fragment in case.expected_answer_contains)
        outcomes.append(
            EvalOutcome(
                name=case.name,
                passed=tools_ok and answer_ok,
                tools_seen=tools_seen,
                answer=result.answer,
                estimated_tokens=result.estimated_tokens,
                estimated_cost_usd=result.estimated_cost_usd,
            )
        )
    return outcomes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    args = parser.parse_args()
    outcomes = run_cases(load_cases(args.cases))
    print(json.dumps([asdict(outcome) for outcome in outcomes], indent=2))
    if not all(outcome.passed for outcome in outcomes):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
