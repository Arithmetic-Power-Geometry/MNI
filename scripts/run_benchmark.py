from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from mni.simulate import generate_population, evaluate_strategies, summarize
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
df = generate_population(n_users=1200, seed=42)
res = evaluate_strategies(df, threshold=0.70, seed=123)
summary = summarize(res)
df.to_csv(OUT / 'synthetic_population.csv', index=False)
res.to_csv(OUT / 'benchmark_results.csv', index=False)
summary.to_csv(OUT / 'summary.csv', index=False)
print(summary.to_string(index=False))
