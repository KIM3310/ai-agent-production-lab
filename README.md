# AI Agent Production Lab

## Live Demo

- [Open the public GitHub Pages demo](https://kim3310.github.io/ai-agent-production-lab/)
- Scope: credential-free, synthetic-data demo for architecture inspection paths and evaluators.

Self-contained lab for agent runtime reliability, evaluation, tracing, and cost accounting. The lab uses a deterministic planner so the full workflow can be tested without external APIs or credentials.

## Product and System Surface

A production-readiness lab for agents that makes planning, tracing, cost, and evaluation visible before real rollout.

| Lens | Definition |
|---|---|
| Audience | AI platform teams, backend teams, and product teams moving agents beyond demos. |
| Architecture path | Validate the demo, README, architecture notes, and quality gate before deeper workflow architecture. |
| System signal | Deterministic planning fixtures, traces, cost accounting, eval assertions, and HTML reports. |
| Safety boundary | Lab fixtures are controlled; production rollouts need workflow-specific evals, rate limits, and approval paths. |
| Fast path | Run the lab scripts and inspect generated HTML reports, traces, and eval assertions. |

## System Fast Path

- **First minute:** Read the trace/cost/eval loop before looking at individual tools.
- **Local demo:** Run `python3 scripts/run_demo.py` and open the generated HTML report under `artifacts/`.
- **Verification:** Run `python3 -m unittest discover -s tests` and `python3 -m agent_lab.evals examples/tasks.json`.

## Service Launch Playbook

- [Service launch playbook](docs/service-launch-playbook.md) maps the repository to architecture audiences, operating gates, operating boundaries, and risk controls.

## Architecture Notes

- [Architecture guide](docs/architecture-evidence-map.md) summarizes the project angle, first files to inspect, runtime commands, and known boundaries.
- [Quality notes](docs/quality-gate.md) lists the local checks, CI surface, and release expectations for this repository.
- [Enterprise readiness notes](docs/enterprise-readiness.md) outlines security, data, operations, integration, and handoff expectations.

## What It Demonstrates

- bounded tool execution
- deterministic traces
- eval cases with pass/fail assertions
- estimated token and cost accounting
- HTML and JSON report generation
- CI-friendly tests with no network dependency

## Architecture

```mermaid
flowchart LR
    Task["Task fixture"] --> Planner["Deterministic planner"]
    Planner --> Runtime["Agent runtime"]
    Runtime --> Tools["Allowed tools"]
    Tools --> Trace["Trace events"]
    Trace --> Eval["Eval runner"]
    Eval --> Report["JSON and HTML reports"]
```

## Quick Start

```bash
python3 -m unittest discover -s tests
python3 scripts/run_demo.py
```

The demo writes:

- `artifacts/agent-report.json`
- `artifacts/agent-report.html`

## Design Boundary

This repository does not try to simulate a full model provider. It isolates the production concerns around an agent loop: tool allowlisting, bounded execution, trace shape, evaluation scoring, and reproducible reports.

## Consolidated Patterns

- [Provider-neutral agent patterns](docs/provider-neutral-agent-patterns.md) folds scattered cookbook notes into a single runtime, eval, tracing, retrieval, and fallback checklist.

## Project Layout

```text
agent_lab/
  runtime.py   # runtime, tools, planner, trace events
  evals.py     # eval case loading and scoring
  report.py    # JSON and HTML report writer
examples/
  tasks.json   # deterministic eval cases
docs/
  provider-neutral-agent-patterns.md
scripts/
  run_demo.py  # local report generator
tests/
  test_runtime.py
```

## Verification

```bash
python3 -m unittest discover -s tests
python3 -m agent_lab.evals examples/tasks.json
```

All fixtures are synthetic.

## Cloud + AI Architecture

This repository includes a neutral cloud and AI engineering blueprint that maps the current proof surface to runtime boundaries, data contracts, model-risk controls, deployment posture, and validation hooks.

- [Cloud + AI architecture blueprint](docs/cloud-ai-architecture.md)
- [Machine-readable architecture manifest](docs/architecture/blueprint.json)
- Validation command: `python3 scripts/validate_architecture_blueprint.py`

## Enterprise Productization

- [Product operating model](docs/product-operating-model.md) defines the architecture inspection, trust boundary, trust boundary, operating checks, and service path for this repository.

## System Architecture

- [System architecture](docs/system-architecture.md) maps the runtime boundary, data/control flow, cloud or local deployment surface, and operating assumptions for this repository.

## Service Architecture

- [Service architecture](docs/service-architecture.md) defines the cloud resources, account information, cost controls, and production guardrails needed to turn this repo into a scoped service without publishing public financial assumptions.

<!-- search-growth-readme:start -->

## Search And Service Surface

- Public entry: free production checklist and sample report
- Paid boundary: paid readiness report, hardened template pack, and hosted scorecard dashboard
- Canonical URL: https://kim3310.github.io/ai-agent-production-lab/
- Lead capture: mailto:ehdjs1351@gmail.com?subject=AI%20Agent%20Production%20Lab%20private%20workspace&body=I%20am%20interested%20in%20paid%20readiness%20report%2C%20hardened%20template%20pack%2C%20and%20hosted%20scorecard%20dashboard%20for%20AI%20Agent%20Production%20Lab.
- Machine-readable offer: [docs/service-offer.json](docs/service-offer.json)
- Search growth implementation: [docs/search-growth-implementation.md](docs/search-growth-implementation.md)
- Revenue architecture: [docs/revenue-architecture.md](docs/revenue-architecture.md)

<!-- search-growth-readme:end -->
