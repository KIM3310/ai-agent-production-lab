# Provider-Neutral Agent Patterns

This document consolidates the reusable agent patterns that were previously spread across provider-specific cookbook repositories. The goal is a compact, runnable reference that stays focused on runtime behavior, testability, and operational boundaries.

## Consolidated Scope

| Pattern | Canonical Handling |
|---|---|
| Tool calls | Normalize every model output into a `tool_name`, JSON arguments, and a bounded execution result. |
| Multi-step plans | Keep plan state explicit, append each tool result to the trace, and stop on budget, policy, or completion. |
| Retrieval | Store source identifiers with each retrieved chunk and require citations to resolve to known inputs. |
| Reranking | Treat rankers as replaceable scoring functions, not as application control flow. |
| Streaming | Stream user-visible tokens separately from trace events so replay stays deterministic. |
| Evaluation | Use fixtures with expected tool sequences, safety boundaries, and final-answer assertions. |
| Cost and latency | Estimate token use and wall-clock time per step; fail tests when budgets are exceeded. |
| Fallbacks | Switch providers behind one adapter contract and record the selected backend in the trace. |

## Runtime Contract

Every agent path should expose the same minimal contract:

```text
input task
  -> normalized planner decision
  -> allowlisted tool execution
  -> trace event
  -> eval assertion
  -> report artifact
```

The contract keeps model-specific behavior behind adapters. Tests can then exercise the orchestration layer without live credentials or network calls.

## Tool Invocation Checklist

- Validate arguments before calling a tool.
- Reject tools that are not in the allowlist for the task.
- Bound retries with a fixed retry policy.
- Capture structured errors as trace events.
- Never let raw model text choose shell commands or file paths directly.

## Retrieval Checklist

- Keep source IDs stable across runs.
- Reject generated citations that are not in the retrieved source set.
- Score the final answer against both factual coverage and source grounding.
- Include a small negative fixture where retrieval is empty or contradictory.

## Evaluation Checklist

- Store eval fixtures as plain JSON.
- Assert the number and order of critical tool calls.
- Assert final status, safety boundary, and report schema.
- Run tests without credentials in CI.
- Generate a JSON artifact for machines and an HTML artifact for readers.

## Consolidation Outcome

Provider-specific examples are now treated as adapter variants. The canonical implementation belongs here because this repository already provides deterministic runtime tests, trace artifacts, and CI-friendly reports.
