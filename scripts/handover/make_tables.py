"""Write every result in results.json as CSV tables (open in Excel or Google Sheets).

Usage: python make_tables.py <results.json> <webmap/data folder> <output folder>
"""
import csv
import json
import sys
from pathlib import Path

R = json.loads(Path(sys.argv[1]).read_text())
WEB = Path(sys.argv[2])
OUT = Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
CL = ["Built-up", "Cropland", "Trees/vegetation", "Bare/fallow"]
Y = ["2015", "2020", "2025"]


def write(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


A = R["area"]
write("01_area_by_class_ha.csv", ["land_type", "ha_2015", "ha_2020", "ha_2025", "share_2015_pct", "share_2020_pct", "share_2025_pct"],
      [[c] + [A[y][c] for y in Y] + [round(100 * A[y][c] / A[y]["Total"], 2) for y in Y] for c in CL] + [["Total"] + [A[y]["Total"] for y in Y] + [100, 100, 100]])
write("02_builtup_change.csv", ["period", "increase_ha", "ha_per_year", "pct_change", "yearly_rate_pct_SDG11.3.1_formula"],
      [[k, v["increase_ha"], v["ha_per_year"], v["pct_change"], v["lcr_pct_per_year"]] for k, v in R["change"].items()])
write("03_zones.csv", ["zone", "zone_ha", "builtup_2015_ha", "builtup_2020_ha", "builtup_2025_ha", "share_2015_pct", "share_2025_pct", "UEII_2015_2025", "yearly_rate_2015_2025_pct"],
      [[k, z["zone_ha"], z["builtup_2015_ha"], z["builtup_2020_ha"], z["builtup_2025_ha"], z["share_2015_pct"], z["share_2025_pct"], z["ueii_2015_2025"], z["lcr_2015_2025"]]
       for k, z in R["zones"].items()])
F = R["from_to"]
write("04_from_to_2015_to_2025_ha.csv", ["2015 (rows) / 2025 (columns)"] + CL + ["total_2015"],
      [[a] + [F[f"{a} -> {b}"] for b in CL] + [round(sum(F[f"{a} -> {b}"] for b in CL), 1)] for a in CL])
write("05_new_builtup_sources.csv", ["land_type_in_2015", "ha_builtup_in_2025", "share_of_new_builtup_pct"],
      [[a, F[f"{a} -> Built-up"], round(100 * F[f"{a} -> Built-up"] / R["new_bu"], 1)] for a in CL[1:]] + [["Total new built-up", R["new_bu"], 100.0],
                                                                                                         ["(Built-up in 2015, not in 2025: mostly noise)", R["lost_bu"], ""]])
acc = R["acc"]
write("06_accuracy_by_class.csv", ["land_type", "users_accuracy_pct", "producers_accuracy_pct"],
      [[c, acc[c]["users_accuracy_pct"], acc[c]["producers_accuracy_pct"]] for c in CL])
write("07_confusion_matrix_points.csv", ["map_2025 (rows) / photo (columns)"] + CL + ["total"],
      [[k] + [acc["counts"][k][r] for r in CL] + [sum(acc["counts"][k].values())] for k in CL])
b = acc["builtup_area_2025"]
write("08_accuracy_summary.csv", ["measure", "value"],
      [["points used", R["acc_points"]], ["points dropped (cloud, unclear)", R["acc_unclear"]], ["overall accuracy, 4 classes (%)", acc["overall_accuracy_pct"]],
       ["built-up vs not, agreement (%)", acc["builtup_binary"]["overall_agreement_pct"]], ["built-up 2025, map (ha)", b["map_ha"]],
       ["built-up 2025, error-adjusted (ha)", b["error_adjusted_ha"]], ["built-up 2025, 95% range +/- (ha)", b["ci95_ha"]],
       ["raters agreed, 4 classes (points of 160)", R["raters"]["agree"]], ["raters agreed, built-up vs not (points of 160)", R["raters"]["bin_agree"]]])
write("09_worldcover_comparison_2020.csv", ["measure", "value"], [[k, v] for k, v in R["wc"].items()])
K = R["kcheck"]
write("10_model_k_selection.csv", ["k", "inertia", "silhouette", "davies_bouldin", "calinski_harabasz", "elbow_distance"],
      [[K["k"][i], K["inertia"][i], K["silhouette"][i], K["davies_bouldin"][i], K["calinski_harabasz"][i], K["elbow_distances"][i]] for i in range(len(K["k"]))])
T = R["training"]
write("11_final_model_training_runs.csv", ["seed", "inertia", "iterations", "builtup_2015_ha", "builtup_2020_ha", "builtup_2025_ha"],
      [[s, v["inertia"], v["n_iter"], R["bu_by_seed"][s]["2015"], R["bu_by_seed"][s]["2020"], R["bu_by_seed"][s]["2025"]] for s, v in T["runs"].items()]
      + [[f"training pixels: {T['training_pixels']}; ARI between runs: " + ", ".join(f"{k} {v}" for k, v in T["ari_between_runs"].items())]])
write("12_superseded_300k_sample_runs.csv", ["run", "builtup_2015_ha", "builtup_2020_ha", "builtup_2025_ha", "iterations"],
      [[k, round(v["built_up_ha"]["2015"], 1), round(v["built_up_ha"]["2020"], 1), round(v["built_up_ha"]["2025"], 1), v["n_iter"]] for k, v in R["sample_runs"]["runs"].items()])
write("13_cluster_naming.csv", ["cluster (ordered by NDVI of its centre)", "land_type"], [[k, v] for k, v in R["naming"].items()])
SC = {"2015": ["LC08_L2SP_147039_20150307_02_T1", "LC08_L2SP_147039_20150323_02_T1"], "2020": ["LC08_L2SP_147039_20200304_02_T1", "LC08_L2SP_147039_20200320_02_T1"],
      "2025": ["LC08_L2SP_147039_20250302_02_T1", "LC08_L2SP_147039_20250318_02_T1"]}
write("14_landsat_scenes.csv", ["year", "scene_id", "date", "path", "row"],
      [[y, s, f"{s[17:21]}-{s[21:23]}-{s[23:25]}", 147, 39] for y, ss in SC.items() for s in ss])
hexes = json.loads((WEB / "hex.geojson").read_text())["features"]
keys = ["id", "z", "la", "lo", "a", "b15", "b20", "b25", "c15", "c20", "c25", "t15", "t20", "t25", "x15", "x20", "x25", "ct"]
write("15_hexagons_1km2_landcover_ha.csv",
      ["hex_id", "zone", "lat", "lon", "mapped_ha", "builtup_2015", "builtup_2020", "builtup_2025", "cropland_2015", "cropland_2020", "cropland_2025",
       "trees_2015", "trees_2020", "trees_2025", "bare_2015", "bare_2020", "bare_2025", "cropland2015_to_builtup2025"],
      [[h["properties"].get(k, "") for k in keys] for h in hexes])
places = json.loads((WEB / "places.json").read_text())
write("16_places_wikidata.csv", ["name", "type", "lat", "lon", "zone", "source"], [[p["n"], p["t"], p["la"], p["lo"], p.get("z", ""), p["src"]] for p in places])
print(len(list(OUT.glob("*.csv"))), "tables written")
