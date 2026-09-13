import math
import numpy as np
import pandas as pd

from .simulate import generate_population, evaluate_strategies, summarize
from .thresholds import threshold_sweep


def multiseed_summary(seeds=range(20), n_users=1200, threshold=0.70):
    """Estimate across-seed mean and 95% normal-approximation CI for each strategy."""
    rows=[]
    for seed in seeds:
        pop=generate_population(n_users, 1000+int(seed), 1.0)
        s=summarize(evaluate_strategies(pop, threshold, 5000+int(seed)))
        s=s.copy(); s['seed']=int(seed); rows.append(s)
    raw=pd.concat(rows, ignore_index=True)
    metrics=['completion_rate','mean_burden','independent_recovery',
             'repeat_success_without_help','mean_intervention_debt']
    out=[]
    for strategy,g in raw.groupby('strategy'):
        row={'strategy':strategy,'n_seeds':len(g)}
        for m in metrics:
            mean=float(g[m].mean()); sd=float(g[m].std(ddof=1)) if len(g)>1 else 0.0
            half=1.96*sd/math.sqrt(len(g)) if len(g)>1 else 0.0
            row[m+'_mean']=mean; row[m+'_ci95_low']=mean-half; row[m+'_ci95_high']=mean+half
        out.append(row)
    return pd.DataFrame(out), raw


def pareto_frontier(pop=None, thresholds=None):
    """Return threshold sweep with nondominated points: maximize completion, minimize burden and debt."""
    if pop is None:
        pop=generate_population(1200,42,1.0)
    sweep=threshold_sweep(pop, thresholds=thresholds)
    dominated=[]
    for i,r in sweep.iterrows():
        is_dom=False
        for j,q in sweep.iterrows():
            if i==j: continue
            weak=(q.completion_rate>=r.completion_rate and q.mean_burden<=r.mean_burden and
                  q.mean_intervention_debt<=r.mean_intervention_debt)
            strict=(q.completion_rate>r.completion_rate or q.mean_burden<r.mean_burden or
                    q.mean_intervention_debt<r.mean_intervention_debt)
            if weak and strict:
                is_dom=True; break
        dominated.append(is_dom)
    out=sweep.copy(); out['pareto_optimal']=[not x for x in dominated]
    return out


def longitudinal_learning(n_users=800, sessions=12, seed=77, threshold=0.70):
    """Controlled repeated-session simulation.

    Skill is updated after each task by a small success-dependent learning increment,
    discounted as intervention burden rises. This is a synthetic mechanism test, not
    a model of human learning.
    """
    rng=np.random.default_rng(seed)
    pop=generate_population(n_users,seed,1.0).copy()
    rows=[]
    for strategy in ['static_help','max_assistance','mni']:
        skill=pop['skill'].to_numpy(dtype=float).copy()
        for session in range(sessions):
            work=pop.copy(); work['skill']=skill
            res=evaluate_strategies(work, threshold, seed+session*101)
            r=res[res.strategy==strategy].copy()
            success=r.success.to_numpy(dtype=float)
            burden=r.burden.to_numpy(dtype=float)
            independent=r.independent_recovery.to_numpy(dtype=float)
            # Small bounded synthetic learning update; stronger assistance reduces the increment.
            gain=0.030*success*(1.0-0.65*burden)+0.010*independent
            skill=np.clip(skill+gain,0.03,0.99)
            rows.append({
                'strategy':strategy,'session':session+1,
                'completion_rate':float(success.mean()),
                'mean_burden':float(burden.mean()),
                'independent_recovery':float(independent.mean()),
                'mean_skill':float(skill.mean()),
                'mean_intervention_debt':float(r.intervention_debt.mean())
            })
    return pd.DataFrame(rows)


def paper_gate_checks(summary_df, robustness_df, pareto_df, multiseed_df):
    """Transparent pre-paper evidence gates; these are reporting gates, not proofs."""
    s=summary_df.set_index('strategy')
    m=multiseed_df.set_index('strategy')
    checks=[]
    checks.append(('G1_less_burden_than_max', bool(s.loc['mni','mean_burden'] < s.loc['max_assistance','mean_burden'])))
    checks.append(('G2_completion_above_static', bool(s.loc['mni','completion_rate'] >= s.loc['static_help','completion_rate'])))
    checks.append(('G3_lower_debt_than_max', bool(s.loc['mni','mean_intervention_debt'] < s.loc['max_assistance','mean_intervention_debt'])))
    adv=robustness_df[robustness_df['case']=='adversarial_25pct'].iloc[0]
    checks.append(('G4_adversarial_completion_above_half', bool(adv.completion_rate >= 0.50)))
    checks.append(('G5_has_pareto_operating_point', bool(pareto_df.pareto_optimal.any())))
    checks.append(('G6_multiseed_ci_finite', bool(np.isfinite(m.filter(like='ci95').to_numpy(dtype=float)).all())))
    return pd.DataFrame(checks, columns=['gate','passed'])
