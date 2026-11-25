import sys, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio
from sklearn.cluster import KMeans
d = sys.argv[1]
inside = np.load(f"{d}/inside.npy")
X, V, P = {}, {}, None
for yr in (2015, 2020, 2025):
    with rasterio.open(f"{d}/composite_{yr}.tif") as src:
        a = src.read().astype("float32"); P = src.profile
    V[yr] = inside & np.all(a != -32768, axis=0)
    X[yr] = (a[:, V[yr]] / 10000.0).T
rng = np.random.default_rng(42)
sample = np.vstack([X[y][rng.choice(len(X[y]), 100000, replace=False)] for y in X])
km = KMeans(n_clusters=10, n_init=5, max_iter=100, random_state=42).fit(sample)
c = km.cluster_centers_; ndvi_c = (c[:, 3] - c[:, 2]) / (c[:, 3] + c[:, 2])
order = np.argsort(ndvi_c); remap = np.empty(10, int); remap[order] = np.arange(1, 11)
print("cluster | centre: blue green red nir swir1 swir2 | NDVI MNDWI | share% 2015 2020 2025")
shares = {}
for yr in X:
    lab = remap[km.predict(X[yr])]
    cl = np.zeros(inside.shape, "uint8"); cl[V[yr]] = lab
    p = P.copy(); p.update(count=1, dtype="uint8", nodata=0)
    with rasterio.open(f"{d}/pclusters_{yr}.tif", "w", **p) as dst: dst.write(cl, 1)
    shares[yr] = np.bincount(lab, minlength=11)[1:] / len(lab) * 100
for k in range(1, 11):
    v = c[order[k - 1]]
    print(f"   {k:2d}   | " + " ".join(f"{x:5.3f}" for x in v) + f" | {(v[3]-v[2])/(v[3]+v[2]):4.2f} {(v[1]-v[4])/(v[1]+v[4]):5.2f} | " + "  ".join(f"{shares[y][k-1]:5.2f}" for y in shares))
np.save(f"{d}/pooled_centres.npy", c[order])
