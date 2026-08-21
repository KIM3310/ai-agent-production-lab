# Contributing

Keep the lab deterministic by default.

Before opening a change:

```bash
make verify
python3 scripts/run_demo.py
```

New eval fixtures should include expected tool names and expected final-answer fragments.
