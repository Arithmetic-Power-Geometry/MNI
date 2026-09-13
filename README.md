# MNI — Minimum Necessary Intervention

**Principle:** help only as much as necessary for successful progress, verify recovery, and then withdraw assistance.

MNI is a general-purpose research prototype for adaptive human-computer assistance across education, government forms, banking-style interfaces, e-commerce, workplace software, AI assistants, and simulation.

## Core idea

Given a user state `x_t`, MNI chooses the *least costly intervention* whose predicted recovery probability reaches a required threshold:

`a_t* = min_a C(a)` subject to `P(recovery | x_t, a) >= tau`.

The intervention ladder is:

`NONE → HIGHLIGHT → CUE → HINT → EXPLAIN → GUIDE → AUTOMATE`

MNI additionally tracks **Intervention Debt**: accumulated intervention burden that is not followed by independent recovery.

## Repository contents

- `mni/core.py` — struggle, recovery, intervention selection, intervention debt
- `mni/simulate.py` — deterministic synthetic cross-domain benchmark
- `app.py` — Streamlit application
- `scripts/run_benchmark.py` — one-command experiment
- `tests/` — unit and benchmark tests
- `.github/workflows/ci.yml` — automated test + artifact generation
- `results/` — generated CSV results

## Run

```bash
python -m pip install -r requirements.txt
pytest -q
python scripts/run_benchmark.py
streamlit run app.py
```

## Reproducibility

The benchmark uses fixed seeds and generates synthetic users across six domains. It compares:

1. no assistance
2. static hint
3. maximum automation
4. MNI

Reported metrics include task completion, intervention burden, independent recovery, repeat success without help, and intervention debt.

The included benchmark is **synthetic and controlled**. It demonstrates consistency of the mechanism; it is not evidence of effectiveness on human participants.

## License

Apache License 2.0.

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
