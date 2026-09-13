import pandas as pd
from .simulate import evaluate_strategies, summarize

def ablation_suite(df, seed=123):
    base=evaluate_strategies(df,.70,seed)
    rows=[]
    s=summarize(base)
    full=s[s.strategy=='mni'].iloc[0]
    rows.append({'ablation':'full_mni','completion_rate':full.completion_rate,'mean_burden':full.mean_burden,'independent_recovery':full.independent_recovery,'mean_intervention_debt':full.mean_intervention_debt})
    tmp=df.copy(); tmp['skill']=.5
    s=summarize(evaluate_strategies(tmp,.70,seed)); r=s[s.strategy=='mni'].iloc[0]
    rows.append({'ablation':'no_skill_personalization','completion_rate':r.completion_rate,'mean_burden':r.mean_burden,'independent_recovery':r.independent_recovery,'mean_intervention_debt':r.mean_intervention_debt})
    r=summarize(base); r=r[r.strategy=='static_help'].iloc[0]
    rows.append({'ablation':'static_help_only','completion_rate':r.completion_rate,'mean_burden':r.mean_burden,'independent_recovery':r.independent_recovery,'mean_intervention_debt':r.mean_intervention_debt})
    r=summarize(base); r=r[r.strategy=='max_assistance'].iloc[0]
    rows.append({'ablation':'max_assistance_only','completion_rate':r.completion_rate,'mean_burden':r.mean_burden,'independent_recovery':r.independent_recovery,'mean_intervention_debt':r.mean_intervention_debt})
    return pd.DataFrame(rows)
