import sys, json, csv, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio
from pyproj import Transformer
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from PIL import Image, ImageDraw, ImageFont
S = sys.argv[1]; a2 = f"{S}/analysis2"; v = f"{S}/validation"
COL = {1: "#B03A2E", 2: "#8DB63C", 3: "#2E6B3F", 4: "#2F7FB0", 5: "#D9A441"}
lulc = {y: rasterio.open(f"{a2}/lulc_{y}.tif").read(1) for y in (2015, 2020, 2025)}
zr = np.load(f"{a2}/zones.npy")
cm = ListedColormap([COL[c] for c in range(1, 6)])
for yr in lulc:
    fig, ax = plt.subplots(figsize=(4.2, 6.2))
    ax.imshow(np.ma.masked_equal(lulc[yr], 0), cmap=cm, vmin=1, vmax=5, interpolation="nearest")
    ax.plot([60, 60 + 10000 / 30], [2110, 2110], color="black", lw=3); ax.text(60, 2075, "10 km", fontsize=11)
    ax.annotate("N", xy=(1330, 80), xytext=(1330, 230), ha="center", fontsize=13, fontweight="bold", arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.set_title(f"LULC {yr}", fontsize=16, fontweight="bold"); ax.axis("off")
    plt.tight_layout(); plt.savefig(f"{a2}/map_lulc_{yr}.png", dpi=220, facecolor="white"); plt.close()
new_bu = (lulc[2025] == 1) & (lulc[2015] != 1) & (lulc[2015] > 0)
chg = np.zeros(lulc[2015].shape, "uint8"); chg[lulc[2015] > 0] = 1; chg[(lulc[2015] == 1) & (lulc[2025] == 1)] = 2; chg[new_bu] = 3
fig, ax = plt.subplots(figsize=(4.6, 6.6))
ax.imshow(np.ma.masked_equal(chg, 0), cmap=ListedColormap(["#E3E7E4", "#5F6F73", "#B03A2E"]), vmin=1, vmax=3, interpolation="nearest")
edge = ((zr == 1) & (np.roll(zr, 1, 0) == 2)) | ((zr == 1) & (np.roll(zr, 1, 1) == 2)) | ((zr == 2) & (np.roll(zr, 1, 0) == 1)) | ((zr == 2) & (np.roll(zr, 1, 1) == 1))
yy, xx = np.nonzero(edge); ax.scatter(xx, yy, s=0.3, c="black")
ax.text(250, 600, "West zone", fontsize=12, fontweight="bold"); ax.text(950, 1750, "East zone", fontsize=12, fontweight="bold")
ax.plot([60, 60 + 10000 / 30], [2110, 2110], color="black", lw=3); ax.text(60, 2075, "10 km", fontsize=11)
ax.legend(handles=[Patch(color="#B03A2E", label="New built-up 2015–2025"), Patch(color="#5F6F73", label="Built-up in both years"), Patch(color="#E3E7E4", label="Other land")], loc="upper right", fontsize=9)
ax.set_title("Built-up change, 2015–2025", fontsize=15, fontweight="bold"); ax.axis("off")
plt.tight_layout(); plt.savefig(f"{a2}/map_change_2015_2025.png", dpi=220, facecolor="white"); plt.close()
# validation example chips: photo label vs map label
key = {r["id"]: r for r in csv.DictReader(open(f"{v}/.map_key_do_not_open.csv"))}
ref = {r["id"]: r["reference"] for r in csv.DictReader(open(f"{v}/reference_labels.csv"))}
with rasterio.open(f"{a2}/lulc_2025.tif") as src:
    m = src.read(1); T = src.transform; crs = src.crs
tr = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
NAME = {1: "Built-up", 2: "Cropland", 3: "Trees", 5: "Bare/fallow"}
def mapclass(i):
    x, y = tr.transform(float(key[i]["lon"]), float(key[i]["lat"])); c, r = ~T * (x, y); return NAME[int(m[int(r), int(c)])]
examples = ["P005", "P009", "P003", "P006", "P010", "P130"]
font = ImageFont.load_default(size=22) if hasattr(ImageFont, "load_default") else None
sheet = Image.new("RGB", (3 * 310, 2 * 372), "white"); dd = ImageDraw.Draw(sheet)
ex_info = []
for j, pid in enumerate(examples):
    im = Image.open(f"{v}/chips/{pid}.png"); ox, oy = (j % 3) * 310, (j // 3) * 372
    sheet.paste(im, (ox, oy))
    p = ref[pid].replace("Trees/vegetation", "Trees"); mc = mapclass(pid); ok = (p == mc) or (p == "Bare" and mc == "Bare/fallow")
    dd.text((ox + 4, oy + 304), f"Photo: {p}", fill=(31, 42, 46), font=font)
    dd.text((ox + 4, oy + 334), f"Map: {mc} {'(match)' if ok else '(miss)'}", fill=(46, 107, 63) if ok else (176, 58, 46), font=font)
    ex_info.append((pid, p, mc, ok))
sheet.save(f"{a2}/validation_examples.png"); print("examples", ex_info)
# final numbers for the slides
r2 = json.load(open(f"{a2}/results2.json")); acc = json.load(open(f"{v}/accuracy.json")); mc_ = json.load(open(f"{S}/diagnostics/model_checks.json"))
tj = json.load(open(f"{a2}/training.json"))
A = acc["analysis2/lulc_2025.tif"]
labA = list(csv.DictReader(open(f"{v}/labels_A.csv"))); labB = {r["id"]: r for r in csv.DictReader(open(f"{v}/labels_B.csv"))}
agree = sum(1 for r in labA if r["label"] == labB[r["id"]]["label"]); bagree = sum(1 for r in labA if (r["label"] == "Built-up") == (labB[r["id"]]["label"] == "Built-up"))
bys = r2["model"]["builtup_ha_by_seed"]
final = {"area": r2["area_ha"], "share": r2["share_pct"], "change": r2["builtup_change"], "zones": r2["zones"],
         "new_bu": r2["new_builtup_2015_2025_ha"], "crop_to_bu": r2["cropland_to_builtup_2015_2025_ha"], "crop_share": r2["cropland_share_of_new_builtup_pct"],
         "lost_bu": r2["builtup_2015_not_builtup_2025_ha"], "from_to": r2["from_to_2015_2025_ha"], "naming": r2["model"]["naming"], "training": tj,
         "bu_by_seed": bys, "wc": r2["worldcover"]["WC2020_vs_2020"], "acc": A, "acc_points": acc["points_used"], "acc_unclear": acc["points_unclear"],
         "raters": {"agree": agree, "bin_agree": bagree, "n": len(labA)}, "kcheck": mc_["task2"],
         "sample_runs": mc_["task3"]}
json.dump(final, open(f"{a2}/final.json", "w"), indent=1)
print("final.json written")
