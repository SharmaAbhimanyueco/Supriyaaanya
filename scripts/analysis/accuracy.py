import sys, csv, json, math, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio
from pyproj import Transformer
v, maps_ = sys.argv[1], sys.argv[2:]
CODE = {"Built-up": 1, "Cropland": 2, "Trees/vegetation": 3, "Bare": 5, "Bare/fallow": 5, "Water": 4}
NAME = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 5: "Bare/fallow"}
CLS = [1, 2, 3, 5]
key = {r["id"]: r for r in csv.DictReader(open(f"{v}/.map_key_do_not_open.csv"))}
ref = {r["id"]: r["reference"] for r in csv.DictReader(open(f"{v}/reference_labels.csv"))}
ids = [i for i in sorted(key) if ref[i] != "Unclear"]
strata = {i: CODE[key[i]["map_class"]] for i in key}
old = rasterio.open(maps_[0]).read(1)
Nh = {c: int((old == c).sum()) for c in CLS}; N = sum(Nh.values())
nh = {c: sum(1 for i in ids if strata[i] == c) for c in CLS}
out = {"points_used": len(ids), "points_unclear": len(key) - len(ids), "stratum_pixels": Nh, "stratum_sample": nh}
for path in maps_:
    with rasterio.open(path) as src:
        m = src.read(1); T = src.transform; crs = src.crs
    tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
    mapc = {}
    for i in ids:
        x, y = tr.transform(float(key[i]["lon"]), float(key[i]["lat"]))
        col, row = ~T * (x, y); mapc[i] = int(m[int(row), int(col)])
    P = np.zeros((6, 6))          # estimated area proportions: rows = map class, cols = reference class
    counts = np.zeros((6, 6), int)
    for i in ids:
        h = strata[i]; r = CODE[ref[i]]; k = mapc[i]
        P[k, r] += (Nh[h] / N) / nh[h]; counts[k, r] += 1
    oa = sum(P[c, c] for c in CLS)
    res = {"overall_accuracy_pct": round(100 * oa, 1), "counts": {NAME[k]: {NAME.get(r, "Water"): int(counts[k, r]) for r in CLS} for k in CLS}}
    for c in CLS:
        ua = P[c, c] / P[c, :].sum() if P[c, :].sum() else float("nan"); pa = P[c, c] / P[:, c].sum() if P[:, c].sum() else float("nan")
        res[NAME[c]] = {"users_accuracy_pct": round(100 * ua, 1), "producers_accuracy_pct": round(100 * pa, 1)}
    # binary built-up
    tp = P[1, 1]; fp = P[1, :].sum() - tp; fn = P[:, 1].sum() - tp
    res["builtup_binary"] = {"overall_agreement_pct": round(100 * (1 - fp - fn), 1), "users_pct": round(100 * tp / (tp + fp), 1), "producers_pct": round(100 * tp / (tp + fn), 1)}
    # error-adjusted built-up area (stratified estimator, 95% CI)
    pj, var = 0.0, 0.0
    for h in CLS:
        y = np.array([1.0 if CODE[ref[i]] == 1 else 0.0 for i in ids if strata[i] == h])
        Wh = Nh[h] / N; pj += Wh * y.mean(); var += Wh ** 2 * y.var(ddof=1) / len(y)
    area = N * 0.09
    res["builtup_area_2025"] = {"map_ha": round(float((m == 1).sum() * 0.09), 1), "error_adjusted_ha": round(pj * area, 0), "ci95_ha": round(1.96 * math.sqrt(var) * area, 0)}
    out[path.split("/")[-2] + "/" + path.split("/")[-1]] = res
json.dump(out, open(f"{v}/accuracy.json", "w"), indent=1)
print(json.dumps(out, indent=1))
