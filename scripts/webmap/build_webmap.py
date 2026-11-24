"""Build webmap/index.html and webmap/layers/*.png from results/ (numbers come only from results/results.json).

Usage: python -I scripts/webmap/build_webmap.py <repo root>
Needs numpy, rasterio, pyproj and pillow.
"""
import json
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.warp import Resampling, calculate_default_transform, reproject

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "webmap"
(OUT / "layers").mkdir(parents=True, exist_ok=True)
R = json.loads((ROOT / "results" / "results.json").read_text())

CLASSES = [("Built-up", 1, (176, 58, 46)), ("Cropland", 2, (141, 182, 60)), ("Trees/vegetation", 3, (46, 107, 63)), ("Bare/fallow", 5, (217, 164, 65))]
BOTH = (95, 111, 115)
hexc = lambda rgb: "#%02X%02X%02X" % rgb


def to_mercator(path):
    with rasterio.open(path) as src:
        tr, w, h = calculate_default_transform(src.crs, "EPSG:3857", src.width, src.height, *src.bounds)
        dst = np.zeros((h, w), "uint8")
        reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs, dst_transform=tr, dst_crs="EPSG:3857",
                  resampling=Resampling.nearest, src_nodata=0, dst_nodata=0)
    return dst, tr


def save_png(arr, palette, name):
    pal = [0, 0, 0] * 256
    for idx, rgb in palette.items():
        pal[idx * 3: idx * 3 + 3] = list(rgb)
    im = Image.fromarray(arr, mode="P")
    im.putpalette(pal)
    im.save(OUT / "layers" / name, transparency=0, optimize=True)


lulc = {}
for yr in (2015, 2020, 2025):
    lulc[yr], tr = to_mercator(ROOT / "results" / "rasters" / f"lulc_{yr}.tif")
    save_png(lulc[yr], {code: rgb for _, code, rgb in CLASSES}, f"lulc_{yr}.png")
h, w = lulc[2015].shape
change = np.zeros_like(lulc[2015])
change[(lulc[2015] == 1) & (lulc[2025] == 1)] = 2
change[(lulc[2025] == 1) & (lulc[2015] != 1) & (lulc[2015] > 0)] = 3
save_png(change, {2: BOTH, 3: CLASSES[0][2]}, "change_2015_2025.png")

minx, maxy = tr.c, tr.f
maxx, miny = tr.c + tr.a * w, tr.f + tr.e * h
inv = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
west, south = inv.transform(minx, miny)
east, north = inv.transform(maxx, maxy)

zones = R["zones"]
zw, ze = zones["West zone (Kharar and Mohali)"], zones["East zone (Dera Bassi, incl. Zirakpur)"]
bu = {y: R["area"][y]["Built-up"] for y in ("2015", "2020", "2025")}
total = R["area"]["2015"]["Total"]
acc = R["acc"]
data = {
    "bounds": {"south": south, "west": west, "north": north, "east": east},
    "merc": {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy},
    "size": {"w": w, "h": h},
    "classes": [{"name": n, "code": c, "hex": hexc(rgb), "rgb": list(rgb)} for n, c, rgb in CLASSES],
    "colors": {"built": hexc(CLASSES[0][2]), "newBuilt": hexc(CLASSES[0][2]), "both": hexc(BOTH)},
    "area": R["area"],
    "builtup": bu,
    "changeStats": R["change"],
    "change": {"newBuilt": R["new_bu"], "both": R["from_to"]["Built-up -> Built-up"]},
    "zones": [
        {"name": "West (Kharar–Mohali)", "b15": zw["builtup_2015_ha"], "b25": zw["builtup_2025_ha"], "ueii": zw["ueii_2015_2025"]},
        {"name": "East (Dera Bassi–Zirakpur)", "b15": ze["builtup_2015_ha"], "b25": ze["builtup_2025_ha"], "ueii": ze["ueii_2015_2025"]},
        {"name": "Whole study area", "b15": bu["2015"], "b25": bu["2025"], "ueii": (bu["2025"] - bu["2015"]) / (total * 10) * 100},
    ],
    "accuracy": {"points": R["acc_points"], "overall": acc["overall_accuracy_pct"], "binary": acc["builtup_binary"]["overall_agreement_pct"],
                 "bu_found": acc["Built-up"]["producers_accuracy_pct"], "adj": acc["builtup_area_2025"]["error_adjusted_ha"],
                 "ci": acc["builtup_area_2025"]["ci95_ha"]},
    "trainingPixels": R["training"]["training_pixels"],
    # approximate town centres, used only as orientation labels
    "towns": [["Mohali", 30.7046, 76.7179], ["Kharar", 30.7461, 76.6457], ["Kurali", 30.8312, 76.5776], ["Zirakpur", 30.6425, 76.8173],
              ["Dera Bassi", 30.5872, 76.8426], ["Lalru", 30.4858, 76.8037], ["Chandigarh", 30.7333, 76.7794]],
}
tpl = (ROOT / "scripts" / "webmap" / "template.html").read_text()
css = (ROOT / "scripts" / "webmap" / "leaflet-1.9.4.css").read_text()
html = tpl.replace("/*__LEAFLET_CSS__*/", css).replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
(OUT / "index.html").write_text(html)
print("webmap built:", OUT / "index.html", f"layers {w}x{h}px", {p.name: p.stat().st_size for p in sorted((OUT / 'layers').glob('*.png'))})
