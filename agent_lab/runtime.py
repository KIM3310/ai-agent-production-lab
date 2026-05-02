from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Callable, Iterable


ToolHandler = Callable[[dict[str, object]], dict[str, object]]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: ToolHandler
    required: tuple[str, ...] = ()


@dataclass(frozen=True)
class ToolResult:
    name: str
    ok: bool
    output: dict[str, object]
    error: str | None = None


@dataclass(frozen=True)
class TraceEvent:
    step: int
    event: str
    detail: dict[str, object]
    elapsed_ms: float


@dataclass(frozen=True)
class RunResult:
    answer: str
    tool_results: tuple[ToolResult, ...]
    trace: tuple[TraceEvent, ...]
    estimated_tokens: int
    estimated_cost_usd: float


@dataclass
class DeterministicPlanner:
    """Small planner that maps task text to tool calls without network access."""

    def plan(self, task: str) -> list[tuple[str, dict[str, object]]]:
        lowered = task.lower()
        calls: list[tuple[str, dict[str, object]]] = []
        if "summarize" in lowered or "summary" in lowered:
            calls.append(("summarize", {"text": task}))
        if "risk" in lowered:
            calls.append(("risk_score", {"text": task}))
        if "handoff" in lowered or "next step" in lowered:
            calls.append(("handoff", {"text": task}))
        if not calls:
            calls.append(("summarize", {"text": task}))
        return calls


@dataclass
class AgentRuntime:
    tools: Iterable[Tool]
    planner: DeterministicPlanner = field(default_factory=DeterministicPlanner)
    max_steps: int = 4
    token_price_per_1k: float = 0.002

    def __post_init__(self) -> None:
        self._tools = {tool.name: tool for tool in self.tools}

    def run(self, task: str) -> RunResult:
        started = perf_counter()
        trace: list[TraceEvent] = []
        results: list[ToolResult] = []
        calls = self.planner.plan(task)[: self.max_steps]
        trace.append(self._event(0, "planned", {"tool_calls": [name for name, _ in calls]}, started))

        for step, (name, args) in enumerate(calls, start=1):
            tool = self._tools.get(name)
            if tool is None:
                result = ToolResult(name=name, ok=False, output={}, error="tool_not_allowed")
                results.append(result)
                trace.append(self._event(step, "tool_rejected", {"tool": name}, started))
                continue

            missing = [key for key in tool.required if key not in args]
            if missing:
                result = ToolResult(name=name, ok=False, output={}, error=f"missing_required:{','.join(missing)}")
                results.append(result)
                trace.append(self._event(step, "tool_invalid", {"tool": name, "missing": missing}, started))
                continue

            try:
                output = tool.handler(args)
                result = ToolResult(name=name, ok=True, output=output)
                trace.append(self._event(step, "tool_completed", {"tool": name, "keys": sorted(output)}, started))
            except Exception as exc:  # pragma: no cover - defensive boundary
                result = ToolResult(name=name, ok=False, output={}, error=type(exc).__name__)
                trace.append(self._event(step, "tool_failed", {"tool": name, "error": type(exc).__name__}, started))
            results.append(result)

        answer = self._compose_answer(task, results)
        estimated_tokens = self._estimate_tokens(task, answer, results)
        estimated_cost = round((estimated_tokens / 1000) * self.token_price_per_1k, 6)
        trace.append(
            self._event(
                len(calls) + 1,
                "answered",
                {"estimated_tokens": estimated_tokens, "estimated_cost_usd": estimated_cost},
                started,
            )
        )
        return RunResult(
            answer=answer,
            tool_results=tuple(results),
            trace=tuple(trace),
            estimated_tokens=estimated_tokens,
            estimated_cost_usd=estimated_cost,
        )

    def _compose_answer(self, task: str, results: list[ToolResult]) -> str:
        successful = [result for result in results if result.ok]
        if not successful:
            return f"No allowed tool completed for: {task}"
        parts = []
        for result in successful:
            summary = result.output.get("summary") or result.output.get("risk") or result.output.get("next_step")
            parts.append(f"{result.name}: {summary}")
        return " | ".join(parts)

    def _estimate_tokens(self, task: str, answer: str, results: list[ToolResult]) -> int:
        text = task + " " + answer + " " + " ".join(str(result.output) for result in results)
        return max(1, len(text.split()))

    def _event(self, step: int, event: str, detail: dict[str, object], started: float) -> TraceEvent:
        return TraceEvent(step=step, event=event, detail=detail, elapsed_ms=round((perf_counter() - started) * 1000, 3))


def default_tools() -> list[Tool]:
    return [
        Tool(
            name="summarize",
            description="Produce a compact task summary.",
            required=("text",),
            handler=lambda args: {"summary": str(args["text"])[:96]},
        ),
        Tool(
            name="risk_score",
            description="Estimate operational risk from task wording.",
            required=("text",),
            handler=lambda args: {"risk": "high" if "urgent" in str(args["text"]).lower() else "medium"},
        ),
        Tool(
            name="handoff",
            description="Create the next operational step.",
            required=("text",),
            handler=lambda args: {"next_step": "record owner, expected output, and verification command"},
        ),
    ]
