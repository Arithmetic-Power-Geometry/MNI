from mni.core import Intervention, escalate, withdraw
from mni.simulate import generate_population
from mni.experiments_episode import simulate_episode
from mni.thresholds import threshold_sweep
from mni.robustness import robustness_suite, heterogeneity_suite
from mni.ablation import ablation_suite

def test_escalate_and_withdraw_bounds():
    assert escalate(Intervention.AUTOMATE)==Intervention.AUTOMATE
    assert withdraw(Intervention.NONE)==Intervention.NONE

def test_episode_outputs_are_valid():
    e=simulate_episode()
    assert (e.action_level.between(0,6)).all()
    assert (e.recovery_probability.between(0,1)).all()

def test_threshold_sweep_runs():
    assert len(threshold_sweep(generate_population(60,4)))>=5

def test_robustness_cases_present():
    r=robustness_suite(generate_population(60,5))
    assert {'baseline','domain_shift','adversarial_25pct'}.issubset(set(r.case))

def test_heterogeneity_suite_runs():
    assert len(heterogeneity_suite(6))==4

def test_ablation_suite_runs():
    assert len(ablation_suite(generate_population(60,7)))==4

def test_generation_is_deterministic():
    assert generate_population(30,9).equals(generate_population(30,9))
