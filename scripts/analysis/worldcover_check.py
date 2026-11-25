import sys, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from affine import Affine
import pystac_client, planetary_computer
d, out = sys.argv[1], sys.argv[2]
env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".TIF,.tif", GDAL_HTTP_MULTIRANGE="YES", GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES", GDAL_HTTP_MAX_RETRY="4", GDAL_HTTP_RETRY_DELAY="1")
if __import__("os").path.exists("/root/.ccr/ca-bundle.crt"):  # only inside the cloud container used for this project
    env["CURL_CA_BUNDLE"] = "/root/.ccr/ca-bundle.crt"
inside = np.load(f"{d}/inside.npy")
with rasterio.open(f"{d}/lulc_2020.tif") as src:
    T = src.transform; crs = src.crs; H, W = src.height, src.width
lulc = {y: rasterio.open(f"{d}/lulc_{y}.tif").read(1) for y in (2015, 2020, 2025)}
T10 = Affine(T.a / 3, 0, T.c, 0, T.e / 3, T.f)  # 10 m grid aligned with the 30 m grid
cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
items = {it.properties["esa_worldcover:product_version"]: it for it in cat.search(collections=["esa-worldcover"], bbox=[76.5, 30.35, 76.95, 30.95]).items()}
res = {}
for ver, wcyear in (("1.0.0", 2020), ("2.0.0", 2021)):
    href = items[ver].assets["map"].href
    with rasterio.Env(**env):
        with rasterio.open(href) as src, WarpedVRT(src, crs=crs, transform=T10, width=W * 3, height=H * 3, resampling=Resampling.nearest) as vrt:
            wc = vrt.read(1)
    built10 = (wc == 50).astype("float32")
    frac = built10.reshape(H, 3, W, 3).mean(axis=(1, 3))       # share of each 30 m pixel that WorldCover calls built-up
    ref = frac >= 0.5
    r = {"worldcover_builtup_ha_fraction_sum": round(float(frac[inside].sum() * 0.09), 1),
         "worldcover_builtup_ha_majority": round(float(ref[inside].sum() * 0.09), 1)}
    for y in (2015, 2020, 2025):
        ours = (lulc[y] == 1)
        a = inside & (lulc[y] > 0)
        tp = (ours & ref & a).sum(); fp = (ours & ~ref & a).sum(); fn = (~ours & ref & a).sum(); tn = (~ours & ~ref & a).sum()
        r[f"vs_our_{y}"] = dict(our_builtup_ha=round(float(ours[a].sum() * 0.09), 1),
            agreement_pct=round(100 * (tp + tn) / a.sum(), 2),
            pct_of_our_builtup_that_worldcover_calls_builtup=round(100 * tp / (tp + fp), 1),
            pct_of_worldcover_builtup_that_we_call_builtup=round(100 * tp / (tp + fn), 1),
            mean_worldcover_builtup_fraction_in_our_builtup_pixels=round(float(frac[ours & a].mean() * 100), 1),
            mean_worldcover_builtup_fraction_in_our_other_pixels=round(float(frac[~ours & a].mean() * 100), 1))
    res[f"WorldCover_{wcyear}"] = r
    np.save(f"{out}/wc_builtup_frac_{wcyear}.npy", frac.astype("float32"))
json.dump(res, open(f"{out}/worldcover_check.json", "w"), indent=1)
print(json.dumps(res, indent=1))
