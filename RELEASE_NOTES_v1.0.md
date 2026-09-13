# MNI v1.0 Research Artifact

This source freeze marks the first complete reproducibility package for **Minimum Necessary Intervention (MNI)**.

## Validated scope

MNI is a synthetic controlled research prototype for adaptive digital assistance. It selects the least-cost intervention predicted to satisfy a recovery threshold, then supports escalation, recovery verification, withdrawal, and intervention-debt tracking.

## Included validation

- baseline comparison against no assistance, static help, and maximum assistance
- closed-loop escalation/withdrawal episode simulation
- threshold sensitivity
- heterogeneous-user stress testing
- sensing-noise robustness
- domain shift
- adversarial/failure-rate stress tests
- ablations
- 20-seed confidence-interval analysis
- Pareto analysis of completion, intervention burden, and intervention debt
- repeated-session synthetic longitudinal analysis
- explicit pre-paper evidence gates
- automated GitHub Actions reproduction and artifact upload

## Scientific boundary

All reported results are generated from controlled synthetic models. They demonstrate internal consistency, comparative behavior, reproducibility, and failure modes. They do **not** constitute human-participant evidence or establish effectiveness in deployed education, banking, accessibility, healthcare, safety-critical, or other real-world systems.

## Frozen evidence run

The first complete v1 evidence workflow passed 19/19 tests, regenerated all scientific artifacts, passed all six pre-paper evidence gates, and uploaded the GitHub Actions artifact `mni-v1-evidence-results`.

## License

Apache License 2.0

Copyright (C) 2026 Mohammad Amir Khusru Akhtar
