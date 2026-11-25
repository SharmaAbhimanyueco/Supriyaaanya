"""Assemble the master document (Markdown -> Word -> PDF) and the teacher-prep documents.

Usage: python build_master.py <handover folder> <master sources folder> <drafts folder> <work folder>
Needs pandoc, LibreOffice and python-docx.
"""
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

H, M, D, W = (Path(a) for a in sys.argv[1:5])
W.mkdir(parents=True, exist_ok=True)
INK, TEAL, RED = RGBColor(0x1F, 0x1F, 0x1F), RGBColor(0x1F, 0x3A, 0x44), RGBColor(0xB0, 0x3A, 0x2E)


def paragraphs_apart(md):
    """Put a blank line before bold-led lines (**Say:**, **In plain words:** ...) so each becomes its own paragraph."""
    out, prev = [], ""
    is_item = lambda l: bool(re.match(r"(\s*[-*] |\s*\d+\. )", l))
    for line in md.split("\n"):
        if line.startswith("**") and prev.strip() and not prev.lstrip().startswith(("|", "- ", "* ", "1.", ">")):
            out.append("")
        elif is_item(line) and prev.strip() and not is_item(prev) and not prev.startswith((" ", "\t", "|")):
            out.append("")  # pandoc needs a blank line before a list that follows a paragraph
        out.append(line)
        prev = line
    return "\n".join(out)


def demote(md, n=1):
    return re.sub(r"^(#+) ", lambda m: "#" * (len(m.group(1)) + n) + " ", md, flags=re.M)


def body_after_title(md):
    return md.split("\n", 1)[1] if md.startswith("# ") else md


PAGE = "\n```{=openxml}\n<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>\n```\n"
concepts = (D / "concepts.md").read_text()
concepts = re.sub(r"^## Part ([A-J]) — ", r"## \1 — ", body_after_title(concepts), flags=re.M)
teacher = (D / "teacher_prep.md").read_text()
env = demote((H / "05_Code" / "ENVIRONMENT.md").read_text())
run = demote((H / "05_Code" / "HOW_TO_RUN.md").read_text())


def inventory():
    """Table of every file in the package; big sets of similar files are summarised in one row."""
    desc = {
        "00_READ_ME_FIRST.md": "One-page guide to the package", "LICENSE": "MIT licence for the code", "LICENSE-DATA.md": "CC BY 4.0 for maps and figures; third-party credits",
        "01_Master_Document": "This document", "02_Presentation/Urban_Growth_Mohali_slides": "The 24-slide deck",
        "02_Presentation/slide_text_and_notes.md": "Every slide's text and speaker notes", "03_Maps_and_Charts/maps": "Map (PNG/JPG)",
        "03_Maps_and_Charts/charts": "Chart (PNG)", "03_Maps_and_Charts/screenshots": "Web map screenshot (taken offline, no background map)",
        "03_Maps_and_Charts/archive_superseded": "Superseded first-run or per-year figure (do not use the numbers)", "04_Data/tables": "CSV table",
        "04_Data/rasters/lulc": "Land-cover map (1 Built-up, 2 Cropland, 3 Trees, 5 Bare; GeoTIFF + QGIS style)",
        "04_Data/rasters/clusters": "The 10 K-means clusters (GeoTIFF + QGIS style)", "04_Data/rasters/first_run": "First-run 2025 map: the sampling strata of the accuracy check",
        "04_Data/landsat_composites": "Landsat 8 March composite, 6 bands, reflectance × 10,000 (GeoTIFF + style)",
        "04_Data/validation": "Accuracy-check data", "04_Data/model_checks": "Model checks and the final model's record",
        "04_Data/study_area": "PRIVATE: GADM boundary and zone mask (do not publish)", "04_Data/results.json": "Every final number",
        "04_Data/RESULTS_README.md": "The results write-up", "05_Code": "Code", "06_Web_Map": "Web map (offline copy and launchers)",
        "07_Teacher_Prep": "Teacher prep", "08_Project_Notes": "Planning notes",
    }
    rows = []
    groups = {"04_Data/validation/chips": "160 photo chips, one per sample point (PRIVATE: Esri imagery)",
              "04_Data/validation/sheets": "10 contact sheets of 16 chips (PRIVATE: Esri imagery)",
              "02_Presentation/slide_images": "Every slide as a PNG picture (24)"}
    seen = set()
    for f in sorted(p for p in H.rglob("*") if p.is_file()):
        rel = f.relative_to(H).as_posix()
        g = next((k for k in groups if rel.startswith(k + "/")), None)
        if g:
            if g not in seen:
                seen.add(g)
                n = sum(1 for _ in (H / g).iterdir())
                size = sum(p.stat().st_size for p in (H / g).iterdir())
                rows.append((f"{g}/ ({n} files)".replace("/", "/\u200b"), f"{size / 1e6:.1f} MB", groups[g]))
            continue
        if "/.venv/" in rel or rel.endswith(".pyc"):
            continue
        d = next((v for k, v in sorted(desc.items(), key=lambda kv: -len(kv[0])) if rel.startswith(k)), "")
        size = f.stat().st_size
        rows.append((rel.replace("/", "/\u200b"), f"{size / 1e6:.1f} MB" if size >= 1e6 else (f"{size / 1e3:.0f} KB" if size >= 1000 else "under 1 KB"), d))
    return ("Every file in the package, with its size. Folders of many similar files are summarised in one row.\n\n"
            "| File | Size | What it is |\n|----------------------------------------------------------|---------|---------------------------------|\n" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows) + "\n")


parts = [
    (M / "master_A.md").read_text(),
    "# Part 2 — Geospatial concepts in plain words\n\n" + paragraphs_apart(concepts),
    (M / "master_B.md").read_text(),
    (M / "master_C.md").read_text() + "\n" + env + "\n" + run,
    PAGE + "\n# Part 13 — Teacher prep: questions, demos and screenshots\n\n" + paragraphs_apart(body_after_title(teacher)),
    (M / "master_D.md").read_text() + "\n" + inventory(),
]
master_md = W / "Master_Document.md"
master_md.write_text("\n\n".join(parts))

# ---------- reference document: fonts, colours, A4, page numbers ----------
ref = W / "reference.docx"
subprocess.run(["pandoc", "-o", str(ref), "--print-default-data-file", "reference.docx"], check=True)
doc = Document(ref)
st = doc.styles


def find_style(style):
    """Look a style up by its name, or by its id (pandoc names some built-in styles in lower case)."""
    for x in st:
        if x.name == style or x.style_id == style.replace(" ", "") or (x.name or "").lower() == style.lower():
            return x
    raise KeyError(style)


def font(style, name, size=None, color=None, bold=None, before=None, after=None):
    s = find_style(style)
    s.font.name = name
    rpr = s.element.get_or_add_rPr()
    fonts = rpr.find(qn("w:rFonts"))
    if fonts is None:  # (an empty lxml element is falsy, so test for None explicitly)
        fonts = OxmlElement("w:rFonts")
        rpr.append(fonts)
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        fonts.set(qn(k), name)
    for k in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if fonts.get(qn(k)) is not None:
            del fonts.attrib[qn(k)]
    if size:
        s.font.size = Pt(size)
    if color is not None:
        s.font.color.rgb = color
    if bold is not None:
        s.font.bold = bold
    if before is not None or after is not None:
        pf = s.paragraph_format
        if before is not None:
            pf.space_before = Pt(before)
        if after is not None:
            pf.space_after = Pt(after)


for name in ("Normal", "Body Text", "First Paragraph", "Compact"):
    if any((x.name or "").lower() == name.lower() or x.style_id == name.replace(" ", "") for x in st):
        font(name, "Calibri", 11, INK, after=6)
font("Title", "Cambria", 26, TEAL, True, 0, 10)
font("Subtitle", "Cambria", 15, RED, False, 0, 18)
for name in ("Author", "Date"):
    if any((x.name or "").lower() == name.lower() or x.style_id == name.replace(" ", "") for x in st):
        font(name, "Calibri", 12, INK)
font("Heading 1", "Cambria", 20, TEAL, True, 18, 8)
font("Heading 2", "Cambria", 15, TEAL, True, 14, 6)
font("Heading 3", "Cambria", 12.5, RED, True, 10, 4)
for name in ("Heading 4", "Heading 5"):
    font(name, "Cambria", 11.5, TEAL, True, 8, 3)
for name in ("Image Caption", "Caption", "Table Caption"):
    if any((x.name or "").lower() == name.lower() or x.style_id == name.replace(" ", "") for x in st):
        font(name, "Calibri", 9.5, RGBColor(0x52, 0x51, 0x4E), False, 2, 10)
for sid in ("SourceCode", "VerbatimChar"):  # Courier New: on every Windows/Mac; LibreOffice renders it with the metric-equal Liberation Mono
    if any(x.style_id == sid for x in st):
        font({"SourceCode": "Source Code", "VerbatimChar": "Verbatim Char"}[sid], "Courier New", 8)
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
for side in ("left_margin", "right_margin"):
    setattr(sec, side, Cm(2.0))
sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(2.0)
fp = sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
fp.alignment = 1
run_ = fp.add_run()
for tag, text in (("begin", None), (None, " PAGE "), ("end", None)):
    if tag:
        el = OxmlElement("w:fldChar")
        el.set(qn("w:fldCharType"), tag)
    else:
        el = OxmlElement("w:instrText")
        el.set(qn("xml:space"), "preserve")
        el.text = text
    run_._r.append(el)
run_.font.size = Pt(9)
doc.save(ref)


def tidy_tables(path):
    """Borders, a shaded header row and smaller type for every table."""
    d = Document(path)
    for t in d.tables:
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = t._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            e = OxmlElement(f"w:{edge}")
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), "C9CCCB")
            borders.append(e)
        old = tblPr.find(qn("w:tblBorders"))
        if old is not None:
            tblPr.remove(old)
        tblPr.append(borders)
        for i, row in enumerate(t.rows):
            for cell in row.cells:
                if i == 0:
                    tcPr = cell._tc.get_or_add_tcPr()
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:val"), "clear")
                    shd.set(qn("w:color"), "auto")
                    shd.set(qn("w:fill"), "E8EEF0")
                    tcPr.append(shd)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(1)
                    p.paragraph_format.space_before = Pt(1)
                    for r in p.runs:
                        r.font.size = Pt(9.5)
                        if i == 0:
                            r.font.bold = True
    d.save(path)


def build(md_path, out_stem, extra=()):
    docx_path = out_stem.with_suffix(".docx")
    subprocess.run(["pandoc", str(md_path), "-f", "markdown+pipe_tables+raw_attribute+implicit_figures+task_lists", "-t", "docx",
                    f"--reference-doc={ref}", f"--resource-path={H}", "-o", str(docx_path), *extra], check=True)
    tidy_tables(docx_path)
    subprocess.run(["zip", "-q", "-d", str(docx_path), "*/"], check=False)
    return docx_path


out_dir = H / "01_Master_Document"
master_docx = build(master_md, out_dir / "Master_Document_Urban_Growth_Mohali")

# ---------- teacher prep as its own documents ----------
tp = W / "Teacher_QA_and_Demo.md"
tp.write_text("---\ntitle: \"Teacher prep: questions, demos and screenshots\"\nsubtitle: \"Mapping Urban Growth in the Mohali–Kharar–Zirakpur–Dera Bassi Belt\"\n"
              "author: \"Supriya Mahshere and Aanya Upadhyay\"\ndate: \"25 November 2026\"\n---\n\n" + paragraphs_apart(body_after_title(teacher)))
build(tp, H / "07_Teacher_Prep" / "Teacher_QA_and_Demo")
m = re.search(r"(^## 5\. Screenshot checklist.*?)(?=^## 6\.)", teacher, flags=re.S | re.M)
shots = W / "Screenshot_Checklist.md"
shots.write_text("---\ntitle: \"Screenshot checklist\"\nsubtitle: \"Screenshots to take yourselves, and which slide each one goes on\"\n---\n\n" + paragraphs_apart(m.group(1)))
(H / "07_Teacher_Prep" / "Screenshot_Checklist.md").write_text("# Screenshot checklist\n\n" + m.group(1))
(H / "07_Teacher_Prep" / "Teacher_QA_and_Demo.md").write_text(teacher)
build(shots, H / "07_Teacher_Prep" / "Screenshot_Checklist")
print("built", master_docx)
