import sys, json, math, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio, shapefile
from sklearn.cluster import KMeans
from rasterio.features import rasterize
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as shp_transform
d, out, shp = sys.argv[1], sys.argv[2], sys.argv[3]
OLD_NAMING = {1: 5, 2: 1, 3: 5, 4: 3, 5: 2, 6: 3, 7: 2, 8: 2, 9: 2, 10: 2}   # 1 Built-up, 2 Cropland, 3 Trees/vegetation, 5 Bare/fallow
NAMES = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 4: "Water", 5: "Bare/fallow"}
ref_c = np.load(f"{d}/pooled_centres.npy")
inside = np.load(f"{d}/inside.npy")
A, V = {}, {}
for yr in (2015, 2020, 2025):
    with rasterio.open(f"{d}/composite_{yr}.tif") as src:
        a = src.read().astype("float64"); prof = src.profile; T = src.transform; crs = src.crs
    V[yr] = inside & np.all(a != -32768, axis=0); A[yr] = a[:, V[yr]].T / 10000.0
X = np.vstack([A[y] for y in A])
runs = {}
for seed in (0, 1, 2):
    km = KMeans(n_clusters=10, n_init=10, max_iter=300, tol=1e-4, random_state=seed).fit(X)
    c = km.cluster_centers_; ndvi = (c[:, 3] - c[:, 2]) / (c[:, 3] + c[:, 2]); order = np.argsort(ndvi)
    rank = np.empty(10, int); rank[order] = np.arange(1, 11)
    naming = {}
    for k in range(10):
        j = int(np.argmin(np.linalg.norm(ref_c - c[k], axis=1))) + 1
        naming[rank[k]] = OLD_NAMING[j]
    bu = {}; maps = {}
    for yr in A:
        lab = rank[km.predict(A[yr])]
        cl = np.zeros(inside.shape, "uint8"); cl[V[yr]] = lab
        lut = np.zeros(11, "uint8")
        for k, v in naming.items(): lut[k] = v
        maps[yr] = (cl, lut[cl])
        bu[yr] = round(float((lut[cl] == 1).sum() * 0.09), 1)
    runs[seed] = dict(inertia=float(km.inertia_), naming={int(k): NAMES[v] for k, v in sorted(naming.items())}, builtup_ha=bu, maps=maps,
                      centres=[[round(float(x), 4) for x in c[i]] for i in order])
    print(f"seed {seed}: inertia {km.inertia_:.3f} built-up ha {bu} naming {runs[seed]['naming']}")
best = min(runs, key=lambda s: runs[s]["inertia"])
print("final model = seed", best)
p = prof.copy(); p.update(count=1, dtype="uint8", nodata=0)
for yr in A:
    cl, lu = runs[best]["maps"][yr]
    with rasterio.open(f"{out}/clusters_{yr}.tif", "w", **p) as dst: dst.write(cl, 1)
    with rasterio.open(f"{out}/lulc_{yr}.tif", "w", **p) as dst: dst.write(lu, 1)
lulc = {yr: runs[best]["maps"][yr][1] for yr in A}
HA = 0.09
res = {"model": dict(training_pixels=int(len(X)), k=10, n_init=10, best_seed=int(best), inertia_by_seed={int(s): round(runs[s]["inertia"], 3) for s in runs},
                     builtup_ha_by_seed={int(s): runs[s]["builtup_ha"] for s in runs}, naming=runs[best]["naming"], centres=runs[best]["centres"]),
       "area_ha": {}, "share_pct": {}}
for yr in A:
    n = np.bincount(lulc[yr].ravel(), minlength=6); total = n[1:].sum()
    res["area_ha"][yr] = {NAMES[c]: round(n[c] * HA, 1) for c in (1, 2, 3, 5)}; res["area_ha"][yr]["Total"] = round(total * HA, 1)
    res["share_pct"][yr] = {NAMES[c]: round(100 * n[c] / total, 2) for c in (1, 2, 3, 5)}
B = {yr: res["area_ha"][yr]["Built-up"] for yr in A}
res["builtup_change"] = {}
for a0, b0 in ((2015, 2020), (2020, 2025), (2015, 2025)):
    y = b0 - a0
    res["builtup_change"][f"{a0}-{b0}"] = dict(increase_ha=round(B[b0] - B[a0], 1), ha_per_year=round((B[b0] - B[a0]) / y, 1),
        pct_change=round(100 * (B[b0] - B[a0]) / B[a0], 1), lcr_pct_per_year=round(100 * math.log(B[b0] / B[a0]) / y, 2))
r = shapefile.Reader(shp); tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform
zones = [({"Kharar": "West zone (Kharar and Mohali)", "Rajpura": "East zone (Dera Bassi, incl. Zirakpur)"}[rec["NAME_3"]], shp_transform(tr, shape(s.__geo_interface__))) for rec, s in zip(r.records(), r.shapes())]
zr = rasterize([(mapping(g), i + 1) for i, (lab, g) in enumerate(zones)], out_shape=inside.shape, transform=T, fill=0, dtype="uint8")
np.save(f"{out}/zones.npy", zr)
res["zones"] = {}
for i, (lab, g) in enumerate(zones):
    m = (zr == i + 1) & (lulc[2015] > 0); za = m.sum() * HA
    b = {yr: ((lulc[yr] == 1) & m).sum() * HA for yr in A}
    res["zones"][lab] = dict(zone_ha=round(za, 1), **{f"builtup_{yr}_ha": round(b[yr], 1) for yr in A},
        share_2015_pct=round(100 * b[2015] / za, 2), share_2025_pct=round(100 * b[2025] / za, 2),
        ueii_2015_2025=round((b[2025] - b[2015]) / (za * 10) * 100, 3), lcr_2015_2025=round(100 * math.log(b[2025] / b[2015]) / 10, 2))
codes = lulc[2015].astype("int16") * 10 + lulc[2025]; both = (lulc[2015] > 0) & (lulc[2025] > 0)
res["from_to_2015_2025_ha"] = {f"{NAMES[c // 10]} -> {NAMES[c % 10]}": round(n * HA, 1) for c, n in zip(*np.unique(codes[both], return_counts=True))}
new_bu = (lulc[2025] == 1) & (lulc[2015] != 1) & both
res["new_builtup_2015_2025_ha"] = round(new_bu.sum() * HA, 1)
res["cropland_to_builtup_2015_2025_ha"] = round(((lulc[2025] == 1) & (lulc[2015] == 2)).sum() * HA, 1)
res["cropland_share_of_new_builtup_pct"] = round(100 * ((lulc[2025] == 1) & (lulc[2015] == 2)).sum() / new_bu.sum(), 1)
res["builtup_2015_not_builtup_2025_ha"] = round(((lulc[2015] == 1) & (lulc[2025] != 1) & both).sum() * HA, 1)
for wy in (2020, 2021):
    frac = np.load(f"{sys.argv[4]}/wc_builtup_frac_{wy}.npy"); ref = frac >= 0.5
    for yr in (2020, 2025):
        ours = lulc[yr] == 1; a_ = inside & (lulc[yr] > 0)
        tp = (ours & ref & a_).sum(); fp = (ours & ~ref & a_).sum(); fn = (~ours & ref & a_).sum(); tn = (~ours & ~ref & a_).sum()
        res.setdefault("worldcover", {})[f"WC{wy}_vs_{yr}"] = dict(agreement_pct=round(100 * (tp + tn) / a_.sum(), 2),
            pct_of_our_builtup_that_wc_calls_builtup=round(100 * tp / (tp + fp), 1), pct_of_wc_builtup_we_call_builtup=round(100 * tp / (tp + fn), 1),
            mean_wc_builtup_fraction_in_our_builtup=round(float(frac[ours & a_].mean() * 100), 1), mean_wc_builtup_fraction_elsewhere=round(float(frac[~ours & a_].mean() * 100), 1),
            wc_builtup_ha=round(float(frac[inside].sum() * HA), 1))
json.dump(res, open(f"{out}/results2.json", "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "model"}, indent=1)[:6000])
