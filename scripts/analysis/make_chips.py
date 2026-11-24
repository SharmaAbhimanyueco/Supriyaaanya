import sys, io, csv, math, time, warnings, concurrent.futures as cf
warnings.filterwarnings("ignore")
import numpy as np, rasterio, requests
from pyproj import Transformer
from PIL import Image, ImageDraw, ImageFont
d, v = sys.argv[1], sys.argv[2]
NAMES = {1: "Built-up", 2: "Cropland", 3: "Trees/vegetation", 5: "Bare/fallow"}
N = {1: 50, 2: 50, 3: 30, 5: 30}
with rasterio.open(f"{d}/lulc_2025.tif") as src:
    lulc = src.read(1); T = src.transform; crs = src.crs
rng = np.random.default_rng(2025)
pts = []
for c, n in N.items():
    rr, cc = np.nonzero(lulc == c)
    idx = rng.choice(len(rr), n, replace=False)
    for i in idx:
        x, y = T * (cc[i] + 0.5, rr[i] + 0.5)
        pts.append((c, x, y))
order = rng.permutation(len(pts))                 # shuffle so the labeller cannot guess the class from the order
pts = [pts[i] for i in order]
tr = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
Z = 17
def gpx(lon, lat):
    n = 256 * 2 ** Z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
sess = requests.Session(); sess.headers["User-Agent"] = "student-lulc-validation/1.0"
cache = {}
def tile(tx, ty):
    if (tx, ty) not in cache:
        for k in range(4):
            r = sess.get(f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{ty}/{tx}", timeout=30)
            if r.status_code == 200: break
            time.sleep(1 + k)
        cache[(tx, ty)] = Image.open(io.BytesIO(r.content)).convert("RGB")
    return cache[(tx, ty)]
HALF = 150
m_per_px = 156543.03392 * math.cos(math.radians(30.7)) / 2 ** Z
box = 30 / m_per_px
rows_key, rows_pub = [], []
def make(i):
    c, x, y = pts[i]
    lon, lat = tr.transform(x, y)
    px, py = gpx(lon, lat)
    x0, y0 = int(px - HALF), int(py - HALF)
    mosaic = Image.new("RGB", (2 * HALF, 2 * HALF))
    for tx in range(x0 // 256, (x0 + 2 * HALF) // 256 + 1):
        for ty in range(y0 // 256, (y0 + 2 * HALF) // 256 + 1):
            mosaic.paste(tile(tx, ty), (tx * 256 - x0, ty * 256 - y0))
    dr = ImageDraw.Draw(mosaic)
    cx, cy = px - x0, py - y0
    dr.rectangle([cx - box / 2, cy - box / 2, cx + box / 2, cy + box / 2], outline=(255, 235, 0), width=2)
    sb = 100 / m_per_px
    dr.rectangle([8, 2 * HALF - 14, 8 + sb, 2 * HALF - 9], fill=(255, 255, 255))
    dr.text((8, 2 * HALF - 28), "100 m", fill=(255, 255, 255))
    pid = f"P{i + 1:03d}"
    mosaic.save(f"{v}/chips/{pid}.png")
    return pid, c, lon, lat
with cf.ThreadPoolExecutor(max_workers=4) as ex:
    out = list(ex.map(make, range(len(pts))))
with open(f"{v}/.map_key_do_not_open.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "map_class", "lon", "lat"])
    for pid, c, lon, lat in out: w.writerow([pid, NAMES[c], f"{lon:.6f}", f"{lat:.6f}"])
with open(f"{v}/points.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "lon", "lat"])
    for pid, c, lon, lat in out: w.writerow([pid, f"{lon:.6f}", f"{lat:.6f}"])
# contact sheets: 4 x 4 chips per sheet, each chip labelled with its ID
font = ImageFont.load_default()
ids = [o[0] for o in out]
for s in range(0, len(ids), 16):
    sheet = Image.new("RGB", (4 * 310, 4 * 310), "white")
    for j, pid in enumerate(ids[s:s + 16]):
        im = Image.open(f"{v}/chips/{pid}.png")
        ox, oy = (j % 4) * 310, (j // 4) * 310
        sheet.paste(im, (ox, oy))
        dd = ImageDraw.Draw(sheet); dd.rectangle([ox, oy, ox + 44, oy + 14], fill=(0, 0, 0)); dd.text((ox + 3, oy + 2), pid, fill=(255, 255, 255), font=font)
    sheet.save(f"{v}/sheets/sheet_{s // 16 + 1:02d}.png")
print("points", len(out), "tiles downloaded", len(cache), "metres per pixel", round(m_per_px, 3), "30 m box px", round(box, 1))
