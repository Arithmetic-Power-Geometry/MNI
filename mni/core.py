from dataclasses import dataclass
from enum import IntEnum
import math

class Intervention(IntEnum):
    NONE=0; HIGHLIGHT=1; CUE=2; HINT=3; EXPLAIN=4; GUIDE=5; AUTOMATE=6

INTERVENTION_COST={
    Intervention.NONE:0.00, Intervention.HIGHLIGHT:0.08, Intervention.CUE:0.15,
    Intervention.HINT:0.25, Intervention.EXPLAIN:0.40, Intervention.GUIDE:0.65,
    Intervention.AUTOMATE:1.00
}
EFFECT={
    Intervention.NONE:0.00, Intervention.HIGHLIGHT:0.28, Intervention.CUE:0.42,
    Intervention.HINT:0.58, Intervention.EXPLAIN:0.72, Intervention.GUIDE:0.86,
    Intervention.AUTOMATE:0.98
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
    z=max(min(float(z),30.0),-30.0)
    return 1/(1+math.exp(-z))

def estimate_struggle(s, noise=0.0):
    z=(-1.10+0.85*s.dwell_z+0.55*s.errors+0.40*s.retries+
       0.35*s.reversals+0.25*s.help_requests-1.15*s.progress_ratio+noise)
    return sigmoid(z)

def recovery_probability(struggle, intervention, skill=0.5, domain_shift=0.0, adversarial_penalty=0.0):
    return sigmoid(-1.2+1.7*skill+2.5*EFFECT[intervention]-2.2*struggle-domain_shift-adversarial_penalty)

def choose_minimum_intervention(struggle, threshold=.70, skill=.5, domain_shift=0.0, adversarial_penalty=0.0):
    for a in Intervention:
        p=recovery_probability(struggle,a,skill,domain_shift,adversarial_penalty)
        if p>=threshold:
            return a,p
    return Intervention.AUTOMATE,recovery_probability(struggle,Intervention.AUTOMATE,skill,domain_shift,adversarial_penalty)

def escalate(current):
    return Intervention(min(int(current)+1, int(Intervention.AUTOMATE)))

def withdraw(current):
    return Intervention(max(int(current)-1, int(Intervention.NONE)))

def intervention_debt(history,recoveries):
    return sum(INTERVENTION_COST[Intervention(int(a))]*(1-float(r)) for a,r in zip(history,recoveries))

def assistance_efficiency(success, burden, eps=1e-9):
    return float(success)/(float(burden)+eps)
