# MNI — Minimum Necessary Intervention

**MNI asks a different question:** not “How much can the system do for the user?” but **“What is the least intervention necessary for successful progress?”**

MNI is a general-purpose, closed-loop research framework for adaptive assistance across learning systems, government forms, banking-style interfaces, e-commerce, workplace software, AI assistants, and simulation.

## Principle

For user state `x_t`, MNI selects the least-cost intervention satisfying a recovery requirement:

`a_t* = min_a C(a)` subject to `P(recovery | x_t, a) >= tau`.

Interventions are ordered:

`NONE → HIGHLIGHT → CUE → HINT → EXPLAIN → GUIDE → AUTOMATE`

The full loop is:

`observe → estimate struggle → predict recovery → choose minimum intervention → verify recovery → escalate if needed → withdraw if recovered → track intervention debt`

## Intervention Debt

MNI tracks assistance burden that is not followed by independent recovery:

`D_T = sum_t C(a_t) (1 - r_t)`

This is a proposed research construct for quantifying when repeated strong assistance achieves immediate success without restoring independence.

## What is tested

The reproducibility package includes:

- cross-domain controlled benchmark
- escalation and withdrawal episode dynamics
- heterogeneous-user stress tests
- noisy struggle-estimation tests
- domain-shift tests
- adversarial/failure-rate tests
- threshold-sensitivity analysis
- ablations for personalization, static assistance, and maximum assistance
- deterministic reproduction tests
- GitHub Actions artifact generation
- interactive Streamlit research app

## Scientific boundary

The included evidence is **synthetic and controlled**. It tests internal consistency, comparative behavior, robustness, failure modes, and reproducibility of the proposed controller.

It does **not** establish effectiveness on human participants, medical benefit, accessibility benefit, banking safety, or superiority in deployed real-world systems. Those claims require empirical human-subject and domain-specific studies.

## Run locally

```bash
python -m pip install -r requirements.txt
pytest -q
python scripts/run_all.py
streamlit run app.py
```

## Generated artifacts

`results/` contains the benchmark outputs including summary, threshold sweep, robustness suite, heterogeneity suite, ablation suite, and closed-loop episode trace.

GitHub Actions runs the test suite, regenerates the scientific artifacts, verifies expected files, and uploads the result bundle.

## License

Apache License 2.0

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
