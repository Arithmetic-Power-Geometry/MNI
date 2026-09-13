from mni.simulate import generate_population,evaluate_strategies,summarize

def test_generation_and_benchmark_shapes():
    df=generate_population(100,seed=1)
    res=evaluate_strategies(df,seed=2)
    assert len(df)==100 and len(res)==400

def test_expected_strategy_set():
    s=summarize(evaluate_strategies(generate_population(50,seed=2),seed=3))
    assert set(s.strategy)=={'no_assistance','static_help','max_assistance','mni'}

def test_metrics_are_bounded():
    s=summarize(evaluate_strategies(generate_population(80,seed=4),seed=5))
    for col in ['completion_rate','mean_burden','independent_recovery','repeat_success_without_help']:
        assert ((s[col]>=0)&(s[col]<=1)).all()
