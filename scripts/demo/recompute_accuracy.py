"""Recompute the accuracy check of the 2025 map from the photo-checked points.

Usage:  python recompute_accuracy.py <the 04_Data folder of the handover package>
        e.g.  python 05_Code/demo/recompute_accuracy.py 04_Data
Needs:  numpy, rasterio and pyproj  (pip install -r 05_Code/requirements-demo.txt)

Inputs (all inside 04_Data):
  validation/sample_points.csv     the 160 random points; map_class = the stratum they were drawn from
                                   (the first-run 2025 map: 50 built-up, 50 cropland, 30 trees, 30 bare)
  validation/reference_labels.csv  what the photo shows at each point (2 points under cloud are "Unclear")
  rasters/first_run_sampling_strata/lulc_2025_first_run.tif   the map the points were drawn from (gives the stratum sizes)
  rasters/lulc_2025.tif            the final 2025 map being checked
It uses the same method as scripts/analysis/accuracy.py: area-weighted accuracy and the error-adjusted
built-up area with a 95% range (Olofsson et al. 2014). The output should match slide 19 and results.json.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np
import rasterio
from pyproj import Transformer

D = Path(sys.argv[1] if len(sys.argv) > 1 else "04_Data")
CODE = {"Built-up": 1, "Cropland": 2, "Trees/vegetation": 3, "Water": 4, "Bare": 5, "Bare/fallow": 5}
NAME = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 5: "Bare/fallow"}
CLS = [1, 2, 3, 5]
pts = {r["id"]: r for r in csv.DictReader(open(D / "validation" / "sample_points.csv"))}
ref = {r["id"]: r["reference"] for r in csv.DictReader(open(D / "validation" / "reference_labels.csv"))}
ids = [i for i in sorted(pts) if ref[i] != "Unclear"]
stratum = {i: CODE[pts[i]["map_class"]] for i in pts}
strata_map = rasterio.open(D / "rasters" / "first_run_sampling_strata" / "lulc_2025_first_run.tif").read(1)
Nh = {c: int((strata_map == c).sum()) for c in CLS}
N = sum(Nh.values())
nh = {c: sum(1 for i in ids if stratum[i] == c) for c in CLS}

with rasterio.open(D / "rasters" / "lulc_2025.tif") as src:
    m, T = src.read(1), src.transform
    to_map = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
mapc = {}
for i in ids:
    x, y = to_map.transform(float(pts[i]["lon"]), float(pts[i]["lat"]))
    col, row = ~T * (x, y)
    mapc[i] = int(m[int(row), int(col)])

P = np.zeros((6, 6))           # estimated share of the area: rows = map class, columns = photo class
counts = np.zeros((6, 6), int)
for i in ids:
    h, r, k = stratum[i], CODE[ref[i]], mapc[i]
    P[k, r] += (Nh[h] / N) / nh[h]
    counts[k, r] += 1

print(f"Points used: {len(ids)} (unclear, dropped: {len(pts) - len(ids)})\n")
print("Point counts (rows = map 2025, columns = photo)")
print(f"{'':<18}" + "".join(f"{NAME[c][:12]:>14}" for c in CLS))
for k in CLS:
    print(f"{NAME[k]:<18}" + "".join(f"{counts[k, r]:>14}" for r in CLS))
print(f"\nOverall accuracy (area-weighted): {100 * sum(P[c, c] for c in CLS):.1f}%")
print(f"(simple, unweighted: {sum(counts[c, c] for c in CLS)} of {len(ids)} points = {100 * sum(counts[c, c] for c in CLS) / len(ids):.1f}%)\n")
print("Land type".ljust(18) + "user's".rjust(10) + "producer's".rjust(12))
for c in CLS:
    ua = P[c, c] / P[c, :].sum()
    pa = P[c, c] / P[:, c].sum()
    print(f"{NAME[c]:<18}{100 * ua:>9.1f}%{100 * pa:>11.1f}%")
tp = P[1, 1]
fp, fn = P[1, :].sum() - tp, P[:, 1].sum() - tp
print(f"\nBuilt-up vs not built-up: agreement {100 * (1 - fp - fn):.1f}%")
pj = var = 0.0
for h in CLS:
    yv = np.array([1.0 if CODE[ref[i]] == 1 else 0.0 for i in ids if stratum[i] == h])
    Wh = Nh[h] / N
    pj += Wh * yv.mean()
    var += Wh ** 2 * yv.var(ddof=1) / len(yv)
total_ha = N * 0.09
print(f"Built-up 2025: map {int((m == 1).sum()) * 0.09:,.0f} ha; error-adjusted {pj * total_ha:,.0f} ± {1.96 * math.sqrt(var) * total_ha:,.0f} ha (95% range)")
