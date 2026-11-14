"""Single-period production plan under scarce materials: LP -> MPQ rounding -> recovery.
Synthetic data (seeded), scipy HiGHS."""
import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(3)
S, M = 20, 5
margin = rng.uniform(2, 10, S)
demand = rng.integers(300, 1500, S).astype(float)
mpq = rng.choice([50, 100, 200], S).astype(float)
bom = rng.uniform(0, 1, (M, S)) * (rng.random((M, S)) < 0.5)  # material units per product unit
avail = 0.45 * bom @ demand  # scarce: 45% of what full demand needs

res = linprog(-margin, A_ub=bom, b_ub=avail, bounds=list(zip([0] * S, demand)), method="highs")
lp = res.x

# MPQ rounding: floor to batch multiples (always material-feasible)
rounded = np.floor(lp / mpq) * mpq

# Recovery: spend leftover material on whole MPQ batches, best margin per scarce-material cost first
rec = rounded.copy()
price = bom.sum(axis=0) + 1e-9
for s in np.argsort(-margin / price):
    while rec[s] + mpq[s] <= demand[s] and np.all(bom @ rec + bom[:, s] * mpq[s] <= avail + 1e-9):
        rec[s] += mpq[s]


def fill(x):
    return x.sum() / demand.sum()


for name, x in [("LP relaxation", lp), ("after MPQ rounding", rounded), ("after recovery", rec)]:
    assert np.all(bom @ x <= avail + 1e-6) and np.all(x <= demand + 1e-6)
    print(f"{name:20s} fill {fill(x):6.1%}   margin {margin @ x:9.0f}")
assert fill(lp) >= fill(rec) >= fill(rounded)
assert np.all(rec % mpq == 0)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = ["LP", "Rounded", "Recovered"]
    plt.bar(labels, [fill(lp) * 100, fill(rounded) * 100, fill(rec) * 100], color="#4c6ef5")
    plt.ylabel("Fill rate (%)")
    plt.title("Synthetic example")
    plt.savefig("fill_rate.png", dpi=120, bbox_inches="tight")
except ImportError:
    pass
