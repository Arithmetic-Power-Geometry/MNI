import numpy as np
import pandas as pd
from .simulate import evaluate_strategies, summarize

def threshold_sweep(df, thresholds=None, seed=123):
    thresholds=np.arange(.55,.91,.05) if thresholds is None else thresholds
    rows=[]
    for tau in thresholds:
        s=summarize(evaluate_strategies(df,float(tau),seed))
        m=s[s.strategy=='mni'].iloc[0]
        rows.append(dict(threshold=float(tau),completion_rate=m.completion_rate,mean_burden=m.mean_burden,independent_recovery=m.independent_recovery,repeat_success_without_help=m.repeat_success_without_help,mean_intervention_debt=m.mean_intervention_debt))
    return pd.DataFrame(rows)
