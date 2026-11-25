import sys, json, math, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio, shapefile
from rasterio.features import rasterize
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import transform as shp_transform
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

d, shp = sys.argv[1], sys.argv[2]
NAMES = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 4: "Water", 5: "Bare/fallow"}
CLUSTER_TO_CLASS = {1: 5, 2: 1, 3: 5, 4: 3, 5: 2, 6: 3, 7: 2, 8: 2, 9: 2, 10: 2}
COL = {1: "#B03A2E", 2: "#8DB63C", 3: "#2E6B3F", 4: "#2F7FB0", 5: "#D9A441"}
YEARS = (2015, 2020, 2025)
lulc, prof = {}, None
for yr in YEARS:
    with rasterio.open(f"{d}/pclusters_{yr}.tif") as src:
        cl = src.read(1); prof = src.profile; T = src.transform; crs = src.crs
    lut = np.zeros(11, "uint8")
    for k, v in CLUSTER_TO_CLASS.items(): lut[k] = v
    lulc[yr] = lut[cl]
    p = prof.copy(); p.update(nodata=0)
    with rasterio.open(f"{d}/lulc_{yr}.tif", "w", **p) as dst: dst.write(lulc[yr], 1)
HA = 0.09
res = {"area_ha": {}, "share_pct": {}}
for yr in YEARS:
    n = np.bincount(lulc[yr].ravel(), minlength=6)
    total = n[1:].sum()
    res["area_ha"][yr] = {NAMES[c]: round(n[c] * HA, 1) for c in range(1, 6)}
    res["area_ha"][yr]["Total"] = round(total * HA, 1)
    res["share_pct"][yr] = {NAMES[c]: round(100 * n[c] / total, 2) for c in range(1, 6)}
B = {yr: res["area_ha"][yr]["Built-up"] for yr in YEARS}
res["builtup_change"] = {}
for a, b in ((2015, 2020), (2020, 2025), (2015, 2025)):
    y = b - a
    res["builtup_change"][f"{a}-{b}"] = dict(increase_ha=round(B[b] - B[a], 1), ha_per_year=round((B[b] - B[a]) / y, 1),
        pct_change=round(100 * (B[b] - B[a]) / B[a], 1), lcr_pct_per_year=round(100 * math.log(B[b] / B[a]) / y, 2))
# zones: the two GADM pieces
r = shapefile.Reader(shp)
tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform
zones = []
for rec, s in zip(r.records(), r.shapes()):
    label = {"Kharar": "West zone (Kharar and Mohali)", "Rajpura": "East zone (Dera Bassi, incl. Zirakpur)"}[rec["NAME_3"]]
    zones.append((label, shp_transform(tr, shape(s.__geo_interface__))))
zr = rasterize([(mapping(g), i + 1) for i, (lab, g) in enumerate(zones)], out_shape=lulc[2015].shape, transform=T, fill=0, dtype="uint8")
res["zones"] = {}
for i, (lab, g) in enumerate(zones):
    m = (zr == i + 1) & (lulc[2015] > 0)
    za = m.sum() * HA
    b15 = ((lulc[2015] == 1) & m).sum() * HA; b20 = ((lulc[2020] == 1) & m).sum() * HA; b25 = ((lulc[2025] == 1) & m).sum() * HA
    res["zones"][lab] = dict(zone_ha=round(za, 1), builtup_2015_ha=round(b15, 1), builtup_2020_ha=round(b20, 1), builtup_2025_ha=round(b25, 1),
        share_2015_pct=round(100 * b15 / za, 2), share_2025_pct=round(100 * b25 / za, 2),
        ueii_2015_2025=round((b25 - b15) / (za * 10) * 100, 3), lcr_2015_2025=round(100 * math.log(b25 / b15) / 10, 2))
# from-to 2015 -> 2025
ft = {}
codes = lulc[2015].astype("int16") * 10 + lulc[2025]
for c, n in zip(*np.unique(codes[(lulc[2015] > 0) & (lulc[2025] > 0)], return_counts=True)):
    ft[f"{NAMES[c // 10]} -> {NAMES[c % 10]}"] = round(n * HA, 1)
res["from_to_2015_2025_ha"] = ft
new_bu = (lulc[2025] == 1) & (lulc[2015] != 1) & (lulc[2015] > 0)
crop_to_bu = (lulc[2025] == 1) & (lulc[2015] == 2)
lost_bu = (lulc[2015] == 1) & (lulc[2025] != 1) & (lulc[2025] > 0)
res["new_builtup_2015_2025_ha"] = round(new_bu.sum() * HA, 1)
res["cropland_to_builtup_2015_2025_ha"] = round(crop_to_bu.sum() * HA, 1)
res["cropland_share_of_new_builtup_pct"] = round(100 * crop_to_bu.sum() / new_bu.sum(), 1)
res["builtup_2015_not_builtup_2025_ha"] = round(lost_bu.sum() * HA, 1)
json.dump(res, open(f"{d}/results.json", "w"), indent=1)
print(json.dumps(res, indent=1))

# maps
cm = ListedColormap(["#FFFFFF00"] + [COL[c] for c in range(1, 6)])
for yr in YEARS:
    fig, ax = plt.subplots(figsize=(4.2, 6.2))
    ax.imshow(np.ma.masked_equal(lulc[yr], 0), cmap=ListedColormap([COL[c] for c in range(1, 6)]), vmin=1, vmax=5, interpolation="nearest")
    ax.plot([60, 60 + 10000 / 30], [2110, 2110], color="black", lw=3); ax.text(60, 2075, "10 km", fontsize=11)
    ax.annotate("N", xy=(1330, 80), xytext=(1330, 230), ha="center", fontsize=13, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.set_title(f"LULC {yr}", fontsize=16, fontweight="bold"); ax.axis("off")
    plt.tight_layout(); plt.savefig(f"{d}/map_lulc_{yr}.png", dpi=220, transparent=False, facecolor="white"); plt.close()
chg = np.zeros(lulc[2015].shape, "uint8")
chg[lulc[2015] > 0] = 1
chg[(lulc[2015] == 1) & (lulc[2025] == 1)] = 2
chg[new_bu] = 3
fig, ax = plt.subplots(figsize=(4.6, 6.6))
ax.imshow(np.ma.masked_equal(chg, 0), cmap=ListedColormap(["#E3E7E4", "#5F6F73", "#B03A2E"]), vmin=1, vmax=3, interpolation="nearest")
edge = (zr == 1) & (np.roll(zr, 1, 0) == 2) | (zr == 1) & (np.roll(zr, 1, 1) == 2) | (zr == 2) & (np.roll(zr, 1, 0) == 1) | (zr == 2) & (np.roll(zr, 1, 1) == 1)
yy, xx = np.nonzero(edge); ax.scatter(xx, yy, s=0.3, c="black")
ax.text(250, 600, "West zone", fontsize=12, fontweight="bold"); ax.text(950, 1750, "East zone", fontsize=12, fontweight="bold")
ax.plot([60, 60 + 10000 / 30], [2110, 2110], color="black", lw=3); ax.text(60, 2075, "10 km", fontsize=11)
ax.legend(handles=[Patch(color="#B03A2E", label="New built-up 2015–2025"), Patch(color="#5F6F73", label="Built-up in both years"), Patch(color="#E3E7E4", label="Other land")], loc="upper right", fontsize=9, frameon=True)
ax.set_title("Built-up change, 2015–2025", fontsize=15, fontweight="bold"); ax.axis("off")
plt.tight_layout(); plt.savefig(f"{d}/map_change_2015_2025.png", dpi=220, facecolor="white"); plt.close()
print("maps ok")
