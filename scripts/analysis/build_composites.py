import sys, time, warnings, concurrent.futures as cf
warnings.filterwarnings("ignore")
import numpy as np, rasterio, shapefile
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rasterio.windows import from_bounds
from rasterio.features import geometry_mask
from pyproj import Transformer
from shapely.geometry import shape, mapping
from shapely.ops import unary_union, transform as shp_transform
import pystac_client, planetary_computer

shp, outdir = sys.argv[1], sys.argv[2]
SCENES = {2015: ["LC08_L2SP_147039_20150307_02_T1", "LC08_L2SP_147039_20150323_02_T1"],
          2020: ["LC08_L2SP_147039_20200304_02_T1", "LC08_L2SP_147039_20200320_02_T1"],
          2025: ["LC08_L2SP_147039_20250302_02_T1", "LC08_L2SP_147039_20250318_02_T1"]}
BANDS = ["blue", "green", "red", "nir08", "swir16", "swir22", "qa_pixel"]
cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1", modifier=planetary_computer.sign_inplace)
items = {it.id: it for it in cat.search(collections=["landsat-c2-l2"], ids=sum(SCENES.values(), [])).items()}
print("items found:", len(items))

env = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".TIF,.tif",
           GDAL_HTTP_MULTIRANGE="YES",
           GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES", GDAL_HTTP_MAX_RETRY="4", GDAL_HTTP_RETRY_DELAY="1")
if __import__("os").path.exists("/root/.ccr/ca-bundle.crt"):  # only inside the cloud container used for this project
    env["CURL_CA_BUNDLE"] = "/root/.ccr/ca-bundle.crt"
aoi_ll = unary_union([shape(s.__geo_interface__) for s in shapefile.Reader(shp).shapes()])
with rasterio.Env(**env):
    first = items[SCENES[2015][0]].assets["red"].href
    with rasterio.open(first) as src:
        crs = src.crs
        aoi = shp_transform(Transformer.from_crs("EPSG:4326", crs, always_xy=True).transform, aoi_ll)
        win = from_bounds(*aoi.buffer(300).bounds, transform=src.transform).round_offsets().round_lengths()
        T = src.window_transform(win); W, H = int(win.width), int(win.height)
print("native CRS", crs, "grid", W, "x", H)
inside = ~geometry_mask([mapping(aoi)], out_shape=(H, W), transform=T)
print("pixels inside study area:", int(inside.sum()))

def read(args):
    sid, band = args
    href = items[sid].assets[band].href
    with rasterio.Env(**env):
        with rasterio.open(href) as src, WarpedVRT(src, crs=crs, transform=T, width=W, height=H, resampling=Resampling.nearest) as vrt:
            return sid, band, vrt.read(1)

t0 = time.time()
jobs = [(sid, b) for yr in SCENES for sid in SCENES[yr] for b in BANDS]
data = {}
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    for sid, band, arr in ex.map(read, jobs):
        data[(sid, band)] = arr
print(f"downloaded {len(jobs)} band windows in {time.time()-t0:.0f}s")

prof = dict(driver="GTiff", width=W, height=H, count=6, dtype="int16", crs=crs, transform=T, nodata=-32768, compress="deflate", tiled=True)
for yr, sids in SCENES.items():
    stack = []
    for sid in sids:
        qa = data[(sid, "qa_pixel")]
        clear = (qa & 0b11111) == 0
        refl = np.stack([data[(sid, b)].astype("float32") * 0.0000275 - 0.2 for b in BANDS[:6]])
        refl[:, ~clear] = np.nan
        stack.append(refl)
        print(f"  {sid}: clear pixels in study area {100*clear[inside].mean():.1f}%")
    comp = np.nanmedian(np.stack(stack), axis=0)
    comp[:, ~inside] = np.nan
    missing = np.isnan(comp[3][inside]).mean() * 100
    print(f"{yr}: composite done, study-area pixels with no clear view: {missing:.2f}%")
    out = np.where(np.isnan(comp), -32768, np.round(comp * 10000)).astype("int16")
    with rasterio.open(f"{outdir}/composite_{yr}.tif", "w", **prof) as dst:
        dst.write(out)
        dst.descriptions = ("blue", "green", "red", "nir", "swir1", "swir2")
np.save(f"{outdir}/inside.npy", inside)
print("done in", f"{time.time()-t0:.0f}s")
