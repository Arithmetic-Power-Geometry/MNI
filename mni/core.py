from dataclasses import dataclass
from enum import IntEnum
import math

class Intervention(IntEnum):
    NONE=0
    HIGHLIGHT=1
    CUE=2
    HINT=3
    EXPLAIN=4
    GUIDE=5
    AUTOMATE=6

INTERVENTION_COST={
    Intervention.NONE:0.00,
    Intervention.HIGHLIGHT:0.08,
    Intervention.CUE:0.15,
    Intervention.HINT:0.25,
    Intervention.EXPLAIN:0.40,
    Intervention.GUIDE:0.65,
    Intervention.AUTOMATE:1.00,
}

@dataclass
class UserState:
    dwell_z:float=0.0
    errors:int=0
    retries:int=0
    reversals:int=0
    help_requests:int=0
    progress_ratio:float=0.5

def sigmoid(z):
    z=max(min(z,30.0),-30.0)
    return 1.0/(1.0+math.exp(-z))

def estimate_struggle(s):
    z=(-1.10+0.85*s.dwell_z+0.55*s.errors+0.40*s.retries+0.35*s.reversals+0.25*s.help_requests-1.15*s.progress_ratio)
    return sigmoid(z)

def recovery_probability(struggle, intervention, skill=0.5):
    effect={Intervention.NONE:0.00,Intervention.HIGHLIGHT:0.28,Intervention.CUE:0.42,Intervention.HINT:0.58,Intervention.EXPLAIN:0.72,Intervention.GUIDE:0.86,Intervention.AUTOMATE:0.98}[intervention]
    return sigmoid(-1.2+1.7*skill+2.5*effect-2.2*struggle)

def choose_minimum_intervention(struggle, threshold=0.70, skill=0.5):
    for intervention in Intervention:
        p=recovery_probability(struggle,intervention,skill)
        if p>=threshold:
            return intervention,p
    return Intervention.AUTOMATE,recovery_probability(struggle,Intervention.AUTOMATE,skill)

def intervention_debt(history,recoveries):
    total=0.0
    for a,r in zip(history,recoveries):
        a=Intervention(int(a))
        total+=INTERVENTION_COST[a]*(1.0-float(r))
    return total
