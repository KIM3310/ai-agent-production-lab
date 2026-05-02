from __future__ import annotations

import unittest
from pathlib import Path

from agent_lab.evals import load_cases, run_cases
from agent_lab.runtime import AgentRuntime, default_tools


class RuntimeTests(unittest.TestCase):
    def test_runtime_executes_expected_tools(self) -> None:
        runtime = AgentRuntime(default_tools())
        result = runtime.run("Urgent risk review with next step handoff")
        names = [tool.name for tool in result.tool_results if tool.ok]
        self.assertIn("risk_score", names)
        self.assertIn("handoff", names)
        self.assertGreater(result.estimated_tokens, 0)
        self.assertGreaterEqual(result.estimated_cost_usd, 0)

    def test_eval_fixtures_pass(self) -> None:
        root = Path(__file__).resolve().parents[1]
        outcomes = run_cases(load_cases(root / "examples" / "tasks.json"))
        self.assertTrue(all(outcome.passed for outcome in outcomes))

    def test_unknown_tool_is_rejected(self) -> None:
        runtime = AgentRuntime([])
        result = runtime.run("Summarize this")
        self.assertFalse(result.tool_results[0].ok)
        self.assertEqual(result.tool_results[0].error, "tool_not_allowed")


if __name__ == "__main__":
    unittest.main()
