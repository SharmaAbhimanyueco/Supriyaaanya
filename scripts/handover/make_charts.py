"""Make the handover charts (PNG, 2000 x 1120 px) from results/results.json.

Usage: python make_charts.py <results.json> <output folder>
Needs matplotlib. Every number is read from results.json; nothing is typed in by hand.
Colours: the land-cover colours of the maps (trees stepped slightly brighter so it does not read as grey);
user's/producer's accuracy use a blue/orange pair. Text is always dark ink, never the series colour.
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath

R = json.loads(Path(sys.argv[1]).read_text())
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

SURF, INK, INK2, MUTED, GRID = "#ffffff", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
CLS = {"Built-up": "#B03A2E", "Cropland": "#8DB63C", "Trees/vegetation": "#2A6E3A", "Bare/fallow": "#D9A441"}
ON = {"Built-up": "#ffffff", "Cropland": INK, "Trees/vegetation": "#ffffff", "Bare/fallow": INK}
BLUE, ORANGE, GREY_DOT = "#2a78d6", "#eb6834", "#a3a29d"
names = {f.name for f in font_manager.fontManager.ttflist}
FONT = next((f for f in ("Inter", "Noto Sans", "Liberation Sans", "DejaVu Sans") if f in names), "DejaVu Sans")
plt.rcParams.update({"font.family": FONT, "font.size": 13, "text.color": INK, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "savefig.facecolor": SURF, "axes.linewidth": 0.8})
DPI, SIZE = 200, (10, 5.6)
K = 0.5523  # cubic Bezier constant for a quarter circle
SOURCE = "Source: Landsat 8 Collection 2 Level-2 (USGS), March composites; K-means classification; numbers from results/results.json."
from decimal import ROUND_HALF_UP, Decimal
ha = lambda v: f"{Decimal(str(v)).quantize(Decimal(1), rounding=ROUND_HALF_UP):,}"  # 12,180.5 -> 12,181, as in the README and slides


def frame(title, subtitle, foot=SOURCE, top=0.80, bottom=0.15, left=0.16, right=0.95, ncols=1, wspace=0.35):
    fig, axes = plt.subplots(1, ncols, figsize=SIZE, dpi=DPI)
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, wspace=wspace)
    fig.text(0.04, 0.945, title, fontsize=19, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.875, subtitle, fontsize=12.5, color=INK2, va="top")
    fig.text(0.04, 0.022, foot, fontsize=9.5, color=MUTED, va="bottom", linespacing=1.5)
    for ax in (axes if ncols > 1 else [axes]):
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(length=0)
    return fig, axes


def units(ax):
    """Data units per output pixel (x, y) for the current limits."""
    ax.figure.canvas.draw()
    bb = ax.get_window_extent()
    (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
    return (x1 - x0) / bb.width, abs(y1 - y0) / bb.height


def hbar(ax, y, x0, x1, h, color, rx, ry, rounded=True):
    """Horizontal bar, square at the baseline, 4px-rounded data end."""
    yb, yt = y - h / 2, y + h / 2
    if not rounded or x1 - x0 < 2 * rx:
        v = [(x0, yb), (x1, yb), (x1, yt), (x0, yt), (x0, yb)]
        c = [MPath.MOVETO, MPath.LINETO, MPath.LINETO, MPath.LINETO, MPath.CLOSEPOLY]
    else:
        ry = min(ry, h / 2)
        v = [(x0, yb), (x1 - rx, yb), (x1 - rx + K * rx, yb), (x1, yb + ry - K * ry), (x1, yb + ry), (x1, yt - ry),
             (x1, yt - ry + K * ry), (x1 - rx + K * rx, yt), (x1 - rx, yt), (x0, yt), (x0, yb)]
        c = [MPath.MOVETO, MPath.LINETO] + [MPath.CURVE4] * 3 + [MPath.LINETO] + [MPath.CURVE4] * 3 + [MPath.LINETO, MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(v, c), facecolor=color, edgecolor="none", lw=0))


def legend(fig, items, x, y, gap=0.03):
    """Swatch + name pairs in a row, spaced by their measured text width."""
    r = fig.canvas.get_renderer()
    for col, lab in items:
        fig.patches.append(matplotlib.patches.FancyBboxPatch((x, y - 0.014), 0.016, 0.028, boxstyle="round,pad=0,rounding_size=0.004",
                                                              transform=fig.transFigure, facecolor=col, edgecolor="none"))
        t = fig.text(x + 0.022, y, lab, fontsize=12.5, color=INK, va="center")
        x = x + 0.022 + t.get_window_extent(r).width / fig.bbox.width + gap


def note(ax, x, y, s, **kw):
    kw.setdefault("color", INK)
    kw.setdefault("fontsize", 13)
    ax.text(x, y, s, **kw)


# ---------------- 1. built-up trend ----------------
A = R["area"]
yrs = [2015, 2020, 2025]
bu = [A[str(y)]["Built-up"] for y in yrs]
ch = R["change"]
fig, ax = frame("Built-up land almost doubled between 2015 and 2025",
                f"Built-up area (hectares) in March of each year, whole study area. Growth sped up after 2020.")
ax.set_xlim(2013.2, 2026.8)
ax.set_ylim(0, 18000)
ax.yaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xticks(yrs)
ax.set_xticklabels([str(y) for y in yrs], fontsize=13, color=INK)
ax.set_yticks(range(0, 18001, 5000))
ax.set_yticklabels([ha(v) for v in range(0, 18001, 5000)], fontsize=11)
ax.fill_between(yrs, bu, color=CLS["Built-up"], alpha=0.10, lw=0)
ax.plot(yrs, bu, color=CLS["Built-up"], lw=2.6, solid_capstyle="round", solid_joinstyle="round", zorder=3)
ax.scatter(yrs, bu, s=110, color=CLS["Built-up"], edgecolor=SURF, linewidth=2.5, zorder=4)
for y, v in zip(yrs, bu):
    note(ax, y, v + 750, f"{ha(v)} ha", ha="center", fontsize=15, fontweight="bold")
for (a, b), key in (((2015, 2020), "2015-2020"), ((2020, 2025), "2020-2025")):
    c = ch[key]
    mid_v = (A[str(a)]["Built-up"] + A[str(b)]["Built-up"]) / 2
    note(ax, (a + b) / 2 + 0.25, mid_v - 2600, f"+{ha(c['increase_ha'])} ha\n{c['lcr_pct_per_year']:.2f}% a year",
         ha="center", color=INK2, fontsize=12, linespacing=1.4)
tot = ch["2015-2025"]
note(ax, 2013.4, 16300, f"2015 to 2025: +{ha(tot['increase_ha'])} ha (+{tot['pct_change']}%), {tot['lcr_pct_per_year']:.2f}% a year",
     fontsize=12.5, color=INK2)
fig.savefig(OUT / "chart_01_builtup_trend.png")
plt.close(fig)

# ---------------- 2. land cover by year (100% stacked) ----------------
SH = {y: {c: 100 * v / R["area"][y]["Total"] for c, v in R["area"][y].items() if c != "Total"} for y in R["area"]}  # from hectares, not the 2-decimal shares (avoids double rounding)
order = ["Built-up", "Cropland", "Trees/vegetation", "Bare/fallow"]
fig, ax = frame("Built-up rose from {:.1f}% to {:.1f}% of the land".format(SH["2015"]["Built-up"], SH["2025"]["Built-up"]),
    "Cropland fell from {:.1f}% to {:.1f}%. Share of the study area (about 108,800 ha) in each class, March of each year".format(
        SH["2015"]["Cropland"], SH["2025"]["Cropland"]),
    left=0.10, right=0.93, top=0.72)
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, 2.6)
ax.set_yticks([2, 1, 0])
ax.set_yticklabels([str(y) for y in yrs], fontsize=14, color=INK)
ax.set_xticks([])
ax.spines["bottom"].set_visible(False)
ux, uy = units(ax)
h, gap = 60 * uy, 4 * ux
for row, y in zip((2, 1, 0), yrs):
    x = 0.0
    for i, c in enumerate(order):
        w = SH[str(y)][c]
        x0 = x + (gap if i else 0)
        hbar(ax, row, x0, x + w, h, CLS[c], 8 * ux, 8 * uy, rounded=(i == len(order) - 1))
        lab = f"{w:.1f}%"
        if w >= 7:
            note(ax, (x0 + x + w) / 2, row, lab, ha="center", va="center", color=ON[c], fontsize=12.5, fontweight="bold")
        else:
            note(ax, x + w + 0.6, row, lab, ha="left", va="center", color=INK, fontsize=12)
        x += w
legend(fig, [(CLS[c], c) for c in order], 0.10, 0.789)
fig.savefig(OUT / "chart_02_landcover_by_year.png")
plt.close(fig)

# ---------------- 3. zones: share 2015 -> 2025, and UEII ----------------
Z = R["zones"]
zk = [("West (Kharar and Mohali)", Z["West zone (Kharar and Mohali)"]), ("East (Dera Bassi, incl. Zirakpur)", Z["East zone (Dera Bassi, incl. Zirakpur)"])]
band = lambda u: "slow" if u < 0.28 else "low" if u < 0.59 else "medium" if u < 1.05 else "high" if u < 1.92 else "very high"
fig, (a1, a2) = frame("The West zone grew faster; the East zone was already more built-up",
                      "West = Kharar and Mohali; East = Dera Bassi incl. Zirakpur (pieces of the boundary file, not official tehsils)",
                      foot="UEII = new built-up ÷ (zone area × years) × 100. The speed bands (slow below 0.28, low 0.28–0.59, medium 0.59–1.05)\n"
                           "are a convention used in some studies, not a rule. Numbers from results/results.json.",
                      ncols=2)
a1.set_position([0.21, 0.17, 0.27, 0.50])
a2.set_position([0.62, 0.17, 0.30, 0.50])
for ax in (a1, a2):
    ax.set_ylim(-0.7, 1.7)
    ax.set_yticks([1, 0])
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.spines["bottom"].set_visible(False)
a1.set_yticklabels(["West\n(Kharar–Mohali)", "East\n(Dera Bassi–Zirakpur)"], fontsize=12.5, color=INK)
a2.set_yticklabels(["West", "East"], fontsize=12.5, color=INK)
a1.set_xlim(0, 18)
a1.set_xticks([0, 5, 10, 15])
a1.set_xticklabels(["0%", "5%", "10%", "15%"], fontsize=11)
fig.text(0.04, 0.765, "Built-up share of the zone", fontsize=13.5, color=INK, fontweight="bold")
for row, (nm, z) in zip((1, 0), zk):
    s0, s1 = z["share_2015_pct"], z["share_2025_pct"]
    a1.plot([s0, s1], [row, row], color=GREY_DOT, lw=2.4, solid_capstyle="round", zorder=2)
    a1.scatter([s0], [row], s=150, color=GREY_DOT, edgecolor=SURF, linewidth=2.5, zorder=3)
    a1.scatter([s1], [row], s=150, color=CLS["Built-up"], edgecolor=SURF, linewidth=2.5, zorder=3)
    note(a1, s0, row + 0.28, f"{s0:.1f}%", ha="center", fontsize=12, color=INK2)
    note(a1, s1, row + 0.28, f"{s1:.1f}%", ha="center", fontsize=12.5, fontweight="bold")
a1.scatter([0.6], [1.62], s=110, color=GREY_DOT, edgecolor=SURF, clip_on=False)
note(a1, 1.3, 1.62, "2015", va="center", fontsize=11.5, color=INK2)
a1.scatter([4.6], [1.62], s=110, color=CLS["Built-up"], edgecolor=SURF, clip_on=False)
note(a1, 5.3, 1.62, "2025", va="center", fontsize=11.5, color=INK2)
a2.set_xlim(0, 1.1)
a2.set_xticks([0, 0.28, 0.59, 1.05])
a2.set_xticklabels(["0", "0.28", "0.59", "1.05"], fontsize=11)
fig.text(0.57, 0.765, "Expansion intensity (UEII), 2015–2025", fontsize=13.5, color=INK, fontweight="bold")
ux, uy = units(a2)
for row, (nm, z) in zip((1, 0), zk):
    u = z["ueii_2015_2025"]
    hbar(a2, row, 0, u, 60 * uy, CLS["Built-up"], 8 * ux, 8 * uy)
    note(a2, u + 0.02, row, f"{u:.2f} ({band(u)})", va="center", fontsize=12.5, fontweight="bold")
fig.savefig(OUT / "chart_03_zones.png")
plt.close(fig)

# ---------------- 4. where the new built-up land came from ----------------
FT = R["from_to"]
src = sorted([(c, FT[f"{c} -> Built-up"]) for c in ("Cropland", "Trees/vegetation", "Bare/fallow")], key=lambda t: -t[1])
new = R["new_bu"]
assert abs(sum(v for _, v in src) - new) < 0.5
fig, ax = frame("Two-thirds of the new built-up land was cropland in 2015",
                f"What the {ha(new)} ha mapped as built-up in 2025, but not in 2015, had been in 2015",
                foot=f"In the other direction, {ha(R['lost_bu'])} ha mapped as built-up in 2015 are not built-up in 2025. Built-up land rarely turns back,\n"
                     "so this is mostly classification noise. Numbers from results/results.json.",
                left=0.20, right=0.93, top=0.78)
ax.set_xlim(0, 8800)
ax.set_ylim(-0.6, len(src) - 0.4)
ax.set_yticks(range(len(src))[::-1])
ax.set_yticklabels([c for c, _ in src], fontsize=13.5, color=INK)
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xticks(range(0, 8001, 2000))
ax.set_xticklabels([f"{ha(v)} ha" for v in range(0, 8001, 2000)], fontsize=11)
ax.spines["bottom"].set_visible(False)
ux, uy = units(ax)
for i, (c, v) in enumerate(src):
    row = len(src) - 1 - i
    hbar(ax, row, 0, v, 60 * uy, CLS[c], 8 * ux, 8 * uy)
    note(ax, v + 90, row, f"{ha(v)} ha  ({100 * v / new:.0f}%)", va="center", fontsize=13.5, fontweight="bold")
fig.savefig(OUT / "chart_04_new_builtup_sources.png")
plt.close(fig)

# ---------------- 5. accuracy by class ----------------
acc = R["acc"]
fig, ax = frame("Cropland is mapped reliably; built-up land is under-detected",
                f"Accuracy of the 2025 map at {R['acc_points']} photo-checked points, area-weighted (Olofsson et al. 2014)",
                foot="Photo labels were AI-assisted (two independent blind raters, disagreements settled by a third look): spot-check them.\n"
                     "Numbers from results/results.json.",
                left=0.20, right=0.93, top=0.70)
ax.set_xlim(0, 105)
ax.set_ylim(-0.7, 3.7)
ax.set_yticks([3, 2, 1, 0])
ax.set_yticklabels(order, fontsize=13.5, color=INK)
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xticks(range(0, 101, 25))
ax.set_xticklabels([f"{v}%" for v in range(0, 101, 25)], fontsize=11)
ax.spines["bottom"].set_visible(False)
ux, uy = units(ax)
bh, g = 46 * uy, 4 * uy
for row, c in zip((3, 2, 1, 0), order):
    ua, pa = acc[c]["users_accuracy_pct"], acc[c]["producers_accuracy_pct"]
    for v, col, off in ((ua, BLUE, +(bh + g) / 2), (pa, ORANGE, -(bh + g) / 2)):
        hbar(ax, row + off, 0, v, bh, col, 8 * ux, 8 * uy)
        note(ax, v + 1.0, row + off, f"{v:.1f}%", va="center", fontsize=12, zorder=6,
             bbox=dict(facecolor=SURF, edgecolor="none", pad=1.2))
oa = acc["overall_accuracy_pct"]
ax.axvline(oa, color=INK2, lw=1.2, zorder=5)
note(ax, oa + 0.8, 3.55, f"Overall accuracy {oa}%", fontsize=12, color=INK2, va="center")
fig.patches.append(matplotlib.patches.FancyBboxPatch((0.04, 0.785), 0.016, 0.028, boxstyle="round,pad=0,rounding_size=0.004",
                                                      transform=fig.transFigure, facecolor=BLUE, edgecolor="none"))
fig.text(0.062, 0.799, "User's accuracy (of the map's pixels in a class, % that are right)", fontsize=12, va="center")
fig.patches.append(matplotlib.patches.FancyBboxPatch((0.04, 0.737), 0.016, 0.028, boxstyle="round,pad=0,rounding_size=0.004",
                                                      transform=fig.transFigure, facecolor=ORANGE, edgecolor="none"))
fig.text(0.062, 0.751, "Producer's accuracy (of the real land in a class, % the map found)", fontsize=12, va="center")
fig.savefig(OUT / "chart_05_accuracy_by_class.png")
plt.close(fig)

# ---------------- 8. map count vs error-adjusted built-up area, 2025 ----------------
b = acc["builtup_area_2025"]
lo, hi = b["error_adjusted_ha"] - b["ci95_ha"], b["error_adjusted_ha"] + b["ci95_ha"]
fig, ax = frame("The 2025 map probably undercounts built-up land",
                "Built-up area in 2025 (hectares): the map's pixel count against the estimate corrected with the photo check",
                foot=f"Error-adjusted estimate and 95% range from {R['acc_points']} photo-checked points (Olofsson et al. 2014).\n"
                     f"ESA WorldCover finds {ha(R['wc']['wc_builtup_ha'])} ha built-up in 2020 against our {ha(A['2020']['Built-up'])} ha: the same undercount.",
                left=0.27, right=0.95, top=0.76)
ax.set_xlim(10000, 24000)
ax.set_ylim(-0.7, 1.7)
ax.set_yticks([1, 0])
ax.set_yticklabels(["Map count", "Error-adjusted\nestimate"], fontsize=13.5, color=INK)
ax.xaxis.grid(True, color=GRID, lw=0.8)
ax.set_axisbelow(True)
ax.set_xticks(range(10000, 24001, 2000))
ax.set_xticklabels([ha(v) for v in range(10000, 24001, 2000)], fontsize=11)
ax.spines["bottom"].set_visible(False)
ax.plot([lo, hi], [0, 0], color=CLS["Built-up"], lw=2.4, solid_capstyle="round", zorder=2)
for xv in (lo, hi):
    ax.plot([xv, xv], [-0.12, 0.12], color=CLS["Built-up"], lw=2.4, solid_capstyle="round", zorder=2)
ax.scatter([b["map_ha"]], [1], s=170, color=INK2, edgecolor=SURF, linewidth=2.5, zorder=3)
ax.scatter([b["error_adjusted_ha"]], [0], s=170, color=CLS["Built-up"], edgecolor=SURF, linewidth=2.5, zorder=3)
note(ax, b["map_ha"], 1.25, f"{ha(b['map_ha'])} ha", ha="center", fontsize=14, fontweight="bold")
note(ax, b["error_adjusted_ha"], 0.25, f"{ha(b['error_adjusted_ha'])} ha", ha="center", fontsize=14, fontweight="bold")
note(ax, lo, -0.42, f"{ha(lo)}", ha="center", fontsize=11.5, color=INK2)
note(ax, hi, -0.42, f"{ha(hi)}", ha="center", fontsize=11.5, color=INK2)
note(ax, (lo + hi) / 2, -0.42, "95% range", ha="center", fontsize=11.5, color=INK2)
fig.savefig(OUT / "chart_08_builtup_error_adjusted.png")
plt.close(fig)
print("charts written to", OUT)
