import numpy as np, pandas as pd
from .core import *

DOMAINS=np.array(['education','banking','government','ecommerce','workplace','ai_assistant'])

def generate_population(n_users=1200,seed=42,heterogeneity=1.0):
    rng=np.random.default_rng(seed); rows=[]
    for uid in range(n_users):
        skill=float(np.clip(rng.beta(3,2.5)+(heterogeneity-1)*rng.normal(0,.12),.03,.99))
        resilience=float(np.clip(rng.beta(4,2)+(heterogeneity-1)*rng.normal(0,.10),.02,.99))
        base=rng.normal(0,1)
        rows.append(dict(user_id=uid,domain=rng.choice(DOMAINS),skill=skill,resilience=resilience,
            dwell_z=float(max(-2,base+rng.normal(0,.7*heterogeneity))),
            errors=int(rng.poisson(max(.05,1.7-1.15*skill))),retries=int(rng.poisson(max(.05,1.3-.85*skill))),
            reversals=int(rng.poisson(max(.05,1.0-.55*skill))),help_requests=int(rng.poisson(max(.03,.55-.28*skill))),
            progress_ratio=float(np.clip(rng.beta(2+3*skill,2),0,1))))
    return pd.DataFrame(rows)

def _state(r):
    return UserState(r.dwell_z,int(r.errors),int(r.retries),int(r.reversals),int(r.help_requests),r.progress_ratio)

def evaluate_strategies(df,threshold=.70,seed=123,noise_sd=0.0,domain_shift=0.0,adversarial_rate=0.0):
    rng=np.random.default_rng(seed); out=[]
    for r in df.itertuples():
        struggle=estimate_struggle(_state(r),rng.normal(0,noise_sd))
        adv=(rng.random()<adversarial_rate); penalty=.65 if adv else 0.0
        mni,_=choose_minimum_intervention(struggle,threshold,r.skill,domain_shift,penalty)
        strategies={'no_assistance':Intervention.NONE,'static_help':Intervention.HINT,'max_assistance':Intervention.AUTOMATE,'mni':mni}
        for name,a in strategies.items():
            p=recovery_probability(struggle,a,r.skill,domain_shift,penalty); success=int(rng.random()<p); burden=INTERVENTION_COST[a]
            independent=float(success)*max(0,1-.72*burden)
            repeat_p=np.clip(.22+.64*r.skill+.22*independent-.20*burden+.06*r.resilience,.01,.99)
            repeat=int(rng.random()<repeat_p); debt=intervention_debt([a],[independent])
            out.append(dict(user_id=r.user_id,domain=r.domain,strategy=name,skill=r.skill,struggle=struggle,intervention=a.name,
                intervention_level=int(a),success=success,burden=burden,independent_recovery=independent,
                repeat_success_without_help=repeat,intervention_debt=debt,adversarial=int(adv),noise_sd=noise_sd,domain_shift=domain_shift))
    return pd.DataFrame(out)

def summarize(res):
    return res.groupby('strategy',as_index=False).agg(completion_rate=('success','mean'),mean_burden=('burden','mean'),
        independent_recovery=('independent_recovery','mean'),repeat_success_without_help=('repeat_success_without_help','mean'),
        mean_intervention_debt=('intervention_debt','mean'),mean_struggle=('struggle','mean'))
