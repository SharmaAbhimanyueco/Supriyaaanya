"""Build the open-source web dashboard in webmap/ from results/.

Usage: python -I scripts/webmap/build_webmap.py <repo root> [<zones.npy>]
  <zones.npy> is W/analysis2/zones.npy from the analysis pipeline (West = 1, East = 2). Without it, the zone filter is
  switched off. Needs numpy, rasterio, pyproj and pillow. All numbers come from results/results.json and
  results/rasters/lulc_*.tif; place names come from scripts/webmap/places_wikidata_raw.json (Wikidata, CC0).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.warp import Resampling, calculate_default_transform, reproject

ROOT = Path(sys.argv[1]).resolve()
ZONES = np.load(sys.argv[2]) if len(sys.argv) > 2 else None
OUT = ROOT / "webmap"
for sub in ("layers", "data"):
    (OUT / sub).mkdir(parents=True, exist_ok=True)
R = json.loads((ROOT / "results" / "results.json").read_text())
CLASSES = [("Built-up", 1, (176, 58, 46)), ("Cropland", 2, (141, 182, 60)), ("Trees/vegetation", 3, (46, 107, 63)), ("Bare/fallow", 5, (217, 164, 65))]
hexc = lambda rgb: "#%02X%02X%02X" % rgb
YEARS = (2015, 2020, 2025)

# ---------- 1. display layers in Web Mercator (the browser also decodes these to filter and measure) ----------
def to_mercator(path):
    with rasterio.open(path) as src:
        tr, w, h = calculate_default_transform(src.crs, "EPSG:3857", src.width, src.height, *src.bounds)
        dst = np.zeros((h, w), "uint8")
        reproject(rasterio.band(src, 1), dst, src_transform=src.transform, src_crs=src.crs, dst_transform=tr, dst_crs="EPSG:3857",
                  resampling=Resampling.nearest, src_nodata=0, dst_nodata=0)
    return dst, tr

for yr in YEARS:
    arr, tr = to_mercator(ROOT / "results" / "rasters" / f"lulc_{yr}.tif")
    pal = [0, 0, 0] * 256
    for _, code, rgb in CLASSES:
        pal[code * 3: code * 3 + 3] = list(rgb)
    im = Image.fromarray(arr, mode="P")
    im.putpalette(pal)
    im.save(OUT / "layers" / f"lulc_{yr}.png", transparency=0, optimize=True)
mh, mw = arr.shape
minx, maxy = tr.c, tr.f
maxx, miny = tr.c + tr.a * mw, tr.f + tr.e * mh
inv = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
west, south = inv.transform(minx, miny)
east, north = inv.transform(maxx, maxy)
old = OUT / "layers" / "change_2015_2025.png"
if old.exists():
    old.unlink()  # the change view is now computed in the browser

# ---------- 2. 1 km² hexagon grid with land-cover statistics (from the 30 m UTM rasters) ----------
src = rasterio.open(ROOT / "results" / "rasters" / "lulc_2015.tif")
T, crs = src.transform, src.crs
L = {yr: rasterio.open(ROOT / "results" / "rasters" / f"lulc_{yr}.tif").read(1) for yr in YEARS}
rows, cols = np.nonzero(L[2015] > 0)
x = T.c + (cols + 0.5) * T.a
y = T.f + (rows + 0.5) * T.e
s = math.sqrt(2e6 / (3 * math.sqrt(3)))  # hexagon size (centre to corner) for an area of 1 km²
cx, cz = (math.sqrt(3) / 3 * x - y / 3) / s, (2 / 3 * y) / s
cy = -cx - cz
rx, ry, rz = np.round(cx), np.round(cy), np.round(cz)
dx, dy, dz = np.abs(rx - cx), np.abs(ry - cy), np.abs(rz - cz)
m1 = (dx > dy) & (dx > dz)
m2 = ~m1 & (dy > dz)
m3 = ~m1 & ~m2
rx[m1] = -ry[m1] - rz[m1]
ry[m2] = -rx[m2] - rz[m2]
rz[m3] = -rx[m3] - ry[m3]
q, r = rx.astype(np.int64), rz.astype(np.int64)
key = (q - q.min()) * 1_000_000 + (r - r.min())
uniq, first, inv_idx = np.unique(key, return_index=True, return_inverse=True)
n = np.bincount(inv_idx, minlength=len(uniq))
V = {yr: L[yr][rows, cols] for yr in YEARS}
cnt = lambda mask: np.bincount(inv_idx, weights=mask.astype(np.float64), minlength=len(uniq))
st = {f"{k}{str(yr)[2:]}": cnt(V[yr] == code) for code, k in ((1, "b"), (2, "c"), (3, "t"), (5, "x")) for yr in YEARS}
st["ct"] = cnt((V[2015] == 2) & (V[2025] == 1))  # cropland in 2015 that is built-up in 2025
if ZONES is not None:
    zv = ZONES[rows, cols]
    zone = np.where(cnt(zv == 1) >= cnt(zv == 2), "W", "E")
to_ll = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
hq, hr = q[first], r[first]
hcx, hcy = s * math.sqrt(3) * (hq + hr / 2), s * 1.5 * hr
feats = []
for i in range(len(uniq)):
    ring = []
    for k in range(7):
        ang = math.radians(60 * (k % 6) - 30)
        lo, la = to_ll.transform(hcx[i] + s * math.cos(ang), hcy[i] + s * math.sin(ang))
        ring.append([round(lo, 5), round(la, 5)])
    clo, cla = to_ll.transform(hcx[i], hcy[i])
    props = {"id": int(i), "a": round(n[i] * 0.09, 1), "la": round(cla, 5), "lo": round(clo, 5)}
    props.update({k: round(float(v[i]) * 0.09, 1) for k, v in st.items()})
    if ZONES is not None:
        props["z"] = str(zone[i])
    feats.append({"type": "Feature", "properties": props, "geometry": {"type": "Polygon", "coordinates": [ring]}})
(OUT / "data" / "hex.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")))

# ---------- 3. searchable places (Wikidata, CC0), kept if inside the study area or within 1.5 km of it ----------
to_utm = Transformer.from_crs("EPSG:4326", crs, always_xy=True)
inside = L[2015] > 0
TOWN = {"town", "city", "big city", "satellite city", "town in India", "planned community", "cantonment town"}
raw = json.loads((ROOT / "scripts" / "webmap" / "places_wikidata_raw.json").read_text())
types_of = {}
for b in raw:
    types_of.setdefault(b["item"]["value"].rsplit("/", 1)[1], set()).add(b["typeLabel"]["value"])
places, seen = [], set()
for row in raw:
    qid = row["item"]["value"].rsplit("/", 1)[1]
    name = row["itemLabel"]["value"]
    if qid in seen or name.startswith("Q") or "pond" in name.lower():
        continue
    seen.add(qid)
    lon, lat = map(float, row["coord"]["value"].replace("Point(", "").replace(")", "").split())
    ux, uy = to_utm.transform(lon, lat)
    c, rr = ~T * (ux, uy)
    c, rr = int(c), int(rr)
    r0, r1, c0, c1 = max(rr - 50, 0), max(rr + 51, 0), max(c - 50, 0), max(c + 51, 0)
    win = inside[r0:r1, c0:c1]
    if win.size == 0 or not win.any():
        continue
    t = types_of[qid]
    kind = "town" if t & TOWN else ("neighbourhood" if t & {"neighborhood", "central business district"} else ("village" if t & {"village in India", "village"} else "settlement"))
    p = {"n": name.split(",")[0], "t": kind, "la": round(lat, 5), "lo": round(lon, 5), "src": "Wikidata " + qid}
    if ZONES is not None:
        zw_ = ZONES[r0:r1, c0:c1]
        p["z"] = "W" if (zw_ == 1).sum() >= (zw_ == 2).sum() else "E"
    places.append(p)
places.sort(key=lambda p: p["n"])
(OUT / "data" / "places.json").write_text(json.dumps(places, separators=(",", ":"), ensure_ascii=False))

# ---------- 4. page ----------
zw, ze = R["zones"]["West zone (Kharar and Mohali)"], R["zones"]["East zone (Dera Bassi, incl. Zirakpur)"]
acc = R["acc"]
data = {
    "bounds": {"south": south, "west": west, "north": north, "east": east},
    "merc": {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy}, "size": {"w": mw, "h": mh},
    "classes": [{"name": nm, "code": c, "hex": hexc(rgb), "rgb": list(rgb)} for nm, c, rgb in CLASSES],
    "area": R["area"], "change": R["change"], "newBuilt": R["new_bu"], "bothBuilt": R["from_to"]["Built-up -> Built-up"], "cropToBuilt": R["crop_to_bu"], "cropShare": R["crop_share"],
    "zones": {"W": {"name": "West (Kharar–Mohali)", "a": zw["zone_ha"], "b15": zw["builtup_2015_ha"], "b25": zw["builtup_2025_ha"], "ueii": zw["ueii_2015_2025"]},
              "E": {"name": "East (Dera Bassi–Zirakpur)", "a": ze["zone_ha"], "b15": ze["builtup_2015_ha"], "b25": ze["builtup_2025_ha"], "ueii": ze["ueii_2015_2025"]}},
    "hasZones": ZONES is not None,
    "accuracy": {"points": R["acc_points"], "overall": acc["overall_accuracy_pct"], "binary": acc["builtup_binary"]["overall_agreement_pct"],
                 "found": acc["Built-up"]["producers_accuracy_pct"], "adj": acc["builtup_area_2025"]["error_adjusted_ha"], "ci": acc["builtup_area_2025"]["ci95_ha"]},
    "trainingPixels": R["training"]["training_pixels"],
    "repo": "https://github.com/SharmaAbhimanyueco/Supriyaaanya",
}
tpl = (ROOT / "scripts" / "webmap" / "template.html").read_text()
css = (ROOT / "scripts" / "webmap" / "leaflet-1.9.4.css").read_text()
html = tpl.replace("/*__LEAFLET_CSS__*/", css).replace("/*__DATA__*/null", json.dumps(data, separators=(",", ":")))
head, body = html.split("<!--BODY-->", 1)
html = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n" + head + "</head>\n<body>" + body + "</body>\n</html>\n")
(OUT / "index.html").write_text(html)
print(f"built webmap: {len(feats)} hexagons, {len(places)} places, layers {mw}x{mh}px")
