from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mni.simulate import *
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)

pop=generate_population(1200,42,1.0)
bench=evaluate_strategies(pop,.70,123)
summary=summarize(bench)
sweep=threshold_sweep(pop)
rob=robustness_suite(pop)
het=heterogeneity_suite()
abl=ablation_suite(pop)
episode=simulate_episode()

for name,df in {
    'synthetic_population':pop,'benchmark_results':bench,'summary':summary,
    'threshold_sweep':sweep,'robustness_suite':rob,'heterogeneity_suite':het,
    'ablation_suite':abl,'episode_trace':episode
}.items():
    df.to_csv(OUT/f'{name}.csv',index=False)

print('=== SUMMARY ==='); print(summary.to_string(index=False))
print('\n=== ROBUSTNESS ==='); print(rob.to_string(index=False))
print('\n=== ABLATIONS ==='); print(abl.to_string(index=False))
