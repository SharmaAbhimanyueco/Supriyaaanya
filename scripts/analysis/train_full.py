import sys, time, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
d, out = sys.argv[1], sys.argv[2]
inside = np.load(f"{d}/inside.npy")
X, V = [], {}
for yr in (2015, 2020, 2025):
    a = rasterio.open(f"{d}/composite_{yr}.tif").read().astype("float64")
    V[yr] = inside & np.all(a != -32768, axis=0)
    X.append(a[:, V[yr]].T / 10000.0)
X = np.vstack(X)
print("training pixels (all three years):", len(X))
models = {}
for seed in (0, 1, 2):
    t = time.time()
    km = KMeans(n_clusters=10, n_init=10, max_iter=300, tol=1e-4, random_state=seed).fit(X)
    models[seed] = km
    print(f"seed {seed}: inertia {km.inertia_:.3f}  iterations {km.n_iter_}  ({time.time()-t:.0f}s)")
rng = np.random.default_rng(11); sub = X[rng.choice(len(X), 300000, replace=False)]
lab = {s: m.predict(sub) for s, m in models.items()}
ari = {f"{a}-{b}": round(adjusted_rand_score(lab[a], lab[b]), 4) for a, b in ((0, 1), (0, 2), (1, 2))}
print("agreement between the three runs (adjusted Rand index):", ari)
best = min(models, key=lambda s: models[s].inertia_)
c = models[best].cluster_centers_
ndvi = (c[:, 3] - c[:, 2]) / (c[:, 3] + c[:, 2]); order = np.argsort(ndvi)
np.save(f"{out}/centres_full.npy", c[order])
json.dump({"training_pixels": int(len(X)), "runs": {s: {"inertia": float(m.inertia_), "n_iter": int(m.n_iter_)} for s, m in models.items()},
           "ari_between_runs": ari, "best_seed": int(best)}, open(f"{out}/training.json", "w"), indent=1)
ref = np.load(f"{d}/pooled_centres.npy")
print("\nnew cluster (NDVI order) | centre blue green red nir swir1 swir2 | NDVI | nearest old cluster (distance)")
for k, i in enumerate(order, 1):
    v = c[i]; dist = np.linalg.norm(ref - v, axis=1); j = int(np.argmin(dist))
    print(f"  {k:2d} | " + " ".join(f"{x:5.3f}" for x in v) + f" | {(v[3]-v[2])/(v[3]+v[2]):4.2f} | old {j+1} ({dist[j]:.3f})")
