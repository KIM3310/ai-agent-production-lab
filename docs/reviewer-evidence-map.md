# Review Guide - AI Agent Production Lab

Updated: 2026-05-30

Use this page as the short path through the repository. It keeps the review grounded in the code, docs, commands, and boundaries that are already present.

## Summary

| Field | Notes |
|---|---|
| Lane | B2B agent readiness lab |
| Core idea | Credential-free lab for tracing, evals, cost accounting, and bounded tool execution. |
| Primary reader | Product teams moving agents from demo to operational release. |
| Stack | Python |

## Open First

1. Start with the README fast path and architecture section.
2. Open `docs/service-launch-playbook.md` only when reviewing the product or service angle.
3. Check the commands below before making claims about quality.
4. Skim the CI workflows and fixture data before deeper implementation review.
5. Read the boundaries section before presenting the project externally.

## Checks

| Purpose | Command |
|---|---|
| Test suite | `python -m pytest` |

## CI

- .github/workflows/architecture-blueprint.yml
- .github/workflows/ci.yml
- .github/workflows/dependency-review.yml
- .github/workflows/repository-health.yml
- .github/workflows/repository-surface.yml
- .github/workflows/secret-scan.yml

## Evidence

- pytest/ruff-style local verification path
- Unit tests pass
- Demo report is generated
- Cost and trace artifacts are inspectable

## Commercial Notes

| Possible offer | Working scope assumption |
|---|---|
| Agent readiness assessment | Scope after buyer intake |
| CI eval setup | Scope after buyer intake |
| Trace/cost instrumentation package | Scope after buyer intake |

## Boundaries

- Synthetic fixtures are not production evals
- Customer workflows need custom rubrics
- Approval paths required

## Useful Metrics

- Eval pass rate
- Trace completeness
- Cost variance visibility
