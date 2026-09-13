import pandas as pd
from .simulate import evaluate_strategies, summarize, generate_population

def robustness_suite(df, seed=123):
    cases=[('baseline',0,0,0),('sensor_noise_low',.20,0,0),('sensor_noise_high',.55,0,0),('domain_shift',.20,.35,0),('adversarial_10pct',.20,.20,.10),('adversarial_25pct',.35,.30,.25)]
    rows=[]
    for name,noise,shift,adv in cases:
        s=summarize(evaluate_strategies(df,.70,seed,noise,shift,adv)); m=s[s.strategy=='mni'].iloc[0]
        rows.append(dict(case=name,completion_rate=m.completion_rate,mean_burden=m.mean_burden,independent_recovery=m.independent_recovery,repeat_success_without_help=m.repeat_success_without_help,mean_intervention_debt=m.mean_intervention_debt))
    return pd.DataFrame(rows)

def heterogeneity_suite(seed=42):
    rows=[]
    for h in [.6,1.0,1.5,2.0]:
        s=summarize(evaluate_strategies(generate_population(1000,seed,h),.70,123)); m=s[s.strategy=='mni'].iloc[0]
        rows.append(dict(heterogeneity=h,completion_rate=m.completion_rate,mean_burden=m.mean_burden,independent_recovery=m.independent_recovery,repeat_success_without_help=m.repeat_success_without_help,mean_intervention_debt=m.mean_intervention_debt))
    return pd.DataFrame(rows)
