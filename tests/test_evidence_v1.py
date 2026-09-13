import numpy as np
from mni.simulate import generate_population, evaluate_strategies, summarize
from mni.robustness import robustness_suite
from mni.evidence_v1 import multiseed_summary, pareto_frontier, longitudinal_learning, paper_gate_checks


def test_multiseed_summary_finite():
    agg, raw = multiseed_summary(seeds=range(3), n_users=80)
    assert len(raw) == 12
    assert np.isfinite(agg.select_dtypes(include='number').to_numpy()).all()


def test_pareto_frontier_has_point():
    p = pareto_frontier(generate_population(120, 31))
    assert p.pareto_optimal.any()


def test_longitudinal_learning_valid():
    x = longitudinal_learning(n_users=100, sessions=4, seed=32)
    assert len(x) == 12
    assert x.completion_rate.between(0,1).all()
    assert x.mean_burden.between(0,1).all()
    assert x.mean_skill.between(0,1).all()


def test_paper_gates_return_booleans():
    pop=generate_population(150,33)
    summary=summarize(evaluate_strategies(pop,.70,34))
    rob=robustness_suite(pop,35)
    par=pareto_frontier(pop)
    ms,_=multiseed_summary(seeds=range(3),n_users=100)
    gates=paper_gate_checks(summary,rob,par,ms)
    assert len(gates)==6
    assert gates.passed.map(lambda x: isinstance(x,(bool,np.bool_))).all()
