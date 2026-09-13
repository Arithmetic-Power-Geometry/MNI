import numpy as np
import pandas as pd
from .core import UserState,Intervention,INTERVENTION_COST,estimate_struggle,recovery_probability,choose_minimum_intervention,intervention_debt

def generate_population(n_users=1200,seed=42):
    rng=np.random.default_rng(seed)
    domains=np.array(['education','banking','government','ecommerce','workplace','ai_assistant'])
    rows=[]
    for uid in range(n_users):
        skill=float(np.clip(rng.beta(3.0,2.5),0.05,0.98))
        rows.append({'user_id':uid,'domain':rng.choice(domains),'skill':skill,'dwell_z':float(max(-1.5,rng.normal(0,1)+rng.normal(0,.7))),'errors':int(rng.poisson(max(.1,1.6-1.1*skill))),'retries':int(rng.poisson(max(.1,1.2-.8*skill))),'reversals':int(rng.poisson(max(.1,.9-.5*skill))),'help_requests':int(rng.poisson(max(.05,.5-.25*skill))),'progress_ratio':float(np.clip(rng.beta(2+3*skill,2),0,1))})
    return pd.DataFrame(rows)

def _state(r):
    return UserState(float(r.dwell_z),int(r.errors),int(r.retries),int(r.reversals),int(r.help_requests),float(r.progress_ratio))

def evaluate_strategies(df,threshold=.70,seed=123):
    rng=np.random.default_rng(seed); out=[]
    for r in df.itertuples():
        struggle=estimate_struggle(_state(r)); mni_a,_=choose_minimum_intervention(struggle,threshold,r.skill)
        strategies={'no_assistance':Intervention.NONE,'static_help':Intervention.HINT,'max_assistance':Intervention.AUTOMATE,'mni':mni_a}
        for name,a in strategies.items():
            p=recovery_probability(struggle,a,r.skill); success=rng.binomial(1,p); burden=INTERVENTION_COST[a]
            independent=float(success)*(1.0-.72*burden)
            repeat_p=np.clip(.25+.62*r.skill+.20*independent-.18*burden,.01,.99)
            repeat=rng.binomial(1,repeat_p); debt=intervention_debt([a],[independent])
            out.append({'user_id':r.user_id,'domain':r.domain,'strategy':name,'skill':r.skill,'struggle':struggle,'intervention':a.name,'intervention_level':int(a),'success':success,'burden':burden,'independent_recovery':independent,'repeat_success_without_help':repeat,'intervention_debt':debt})
    return pd.DataFrame(out)

def summarize(results):
    return results.groupby('strategy',as_index=False).agg(completion_rate=('success','mean'),mean_burden=('burden','mean'),independent_recovery=('independent_recovery','mean'),repeat_success_without_help=('repeat_success_without_help','mean'),mean_intervention_debt=('intervention_debt','mean'),mean_struggle=('struggle','mean'))
