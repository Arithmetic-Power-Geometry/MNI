import numpy as np
import pandas as pd
from .core import Intervention, sigmoid, choose_minimum_intervention, recovery_probability, escalate, withdraw

def simulate_episode(skill=.5,steps=12,threshold=.70,seed=7):
    rng=np.random.default_rng(seed); rows=[]; current=Intervention.NONE; recovered_prev=True
    for t in range(steps):
        difficulty=.15+.07*t
        struggle=float(np.clip(sigmoid(-1+2.6*difficulty-1.6*skill+rng.normal(0,.2)),0,1))
        proposed,_=choose_minimum_intervention(struggle,threshold,skill)
        if recovered_prev and int(current)>int(proposed): current=withdraw(current)
        elif int(proposed)>int(current): current=escalate(current)
        p=recovery_probability(struggle,current,skill); success=int(rng.random()<p); recovered_prev=bool(success)
        rows.append(dict(step=t,difficulty=difficulty,struggle=struggle,action=current.name,action_level=int(current),recovery_probability=p,success=success))
    return pd.DataFrame(rows)
