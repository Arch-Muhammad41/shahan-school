"""usage: python build_drawings.py <site dir> <img dir>
One-time: it replaces "const DRAWINGS = [];" in index.html. To change the grouping now, edit DRAWING_TABS in index.html directly.
Copy chosen sheet images into the site and write the DRAWINGS / DRAWING_TABS data into index.html."""
import json, re, shutil, os, sys
SCR = os.path.dirname(os.path.abspath(__file__)); SITE = sys.argv[1]
IMG = sys.argv[2]   # folder with full/ and thumb/ made by sheets_to_jpg.py and x_to_jpg.py
S = json.load(open(os.path.join(SCR, "sheets.json"), encoding="utf-8"))
XN = json.load(open(os.path.join(SCR, "x_names.json")))
out_full = os.path.join(SITE, "img", "drawings"); out_th = os.path.join(out_full, "thumb")
os.makedirs(out_th, exist_ok=True)

def clean(t):
    t = t.replace("Fisrt", "First").replace("Basment", "Basement").replace("Groundfloor", "Ground floor").replace("Pent house", "Penthouse").replace("Pent House", "Penthouse").replace("pent house", "Penthouse")
    t = re.sub(r"\s*-\s*", " – ", t.strip()); t = re.sub(r"\s+", " ", t)
    small = {"and", "for", "of", "&"}
    return " ".join(w if w.lower() in small or w.isupper() and len(w) <= 3 else w[:1].upper() + w[1:] for w in t.split(" "))

TABS = [
  ("Architectural", [
    ("Index & Site", ["s0", "s1", "x0", "s2", "s3"]),
    ("Architectural Plans", ["s9", "s10", "s11", "s12", "s13"]),
    ("Furniture Plans", ["s4", "s5", "s6", "s7", "s8"]),
    ("Elevations", ["s78", "s79", "s80", "s81", "x17"]),
    ("Exterior Plans", ["s14", "s15", "s16"]),
    ("Dimension Plans", ["s22", "s23", "s24", "s25", "s26"]),
    ("Stair Plans", ["s56", "s57", "s58", "s59", "s60", "s61"])]),
  ("Finishes", [
    ("Ceiling Plans", ["s17", "s18", "s19", "s20", "s21"]),
    ("Floor Finishing", ["s27", "s28", "s29", "s30", "s31"]),
    ("Floor Tile Finishing", ["s33", "s32", "s36", "s37", "s38"]),
    ("Floor & Wall Tile Areas", ["s39", "s40", "s41"]),
    ("Plastering Plans", ["s42", "s43", "s44", "s45", "s46"]),
    ("Doors & Windows", ["s47", "s48", "s49", "s50", "s51", "s52", "s53", "s54", "s55"])]),
  ("Structural", [
    ("General Notes", ["x1"]),
    ("Foundation", ["x6"]),
    ("Column Key Plans", ["x2", "x3", "x4", "x5"]),
    ("Beam Layout Plans", ["x7", "x8", "x9", "x10"]),
    ("Structural Details", ["x11", "x12", "x13", "x14"]),
    ("Retaining Walls & Fence", ["x15", "x16"])]),
  ("Mechanical", [
    ("Fire Fighting", ["s62", "s63", "s64", "s65", "s66"]),
    ("VRF Air Conditioning", ["s67", "s68", "s69", "s70", "s71", "s72"]),
    ("HVAC Ventilation", ["s73", "s74", "s75", "s76", "s77"]),
    ("Plumbing", ["s87"])]),
]
drawings, tabs = [], []
for tname, areas in TABS:
    ta = []
    for aname, keys in areas:
        pick = []
        for k in keys:
            n = len(drawings) + 1; name = f"{n:03d}.jpg"
            if k[0] == "s":
                i = int(k[1:]); src = f"{i:03d}.jpg"; s = S[i]
                title = clean(s["title"]); no = s["no"]
                if title.lower() == "top view" and i in (0, 1): title = f"Index of Drawings ({i + 1}/2)"
                if "Exterior" in title: title = f"Architectural Plan for Exterior ({keys.index(k) + 1}/3)"
                if title.startswith("HVAC System"): title = f"HVAC System ({keys.index(k) + 1}/5)"
                if title == "Elevation": title = f"Elevation ({keys.index(k) + 1}/4)"
                label = f"{no} · {title}"
            else:
                i = int(k[1:]); src = f"x{i:02d}.jpg"; label = XN[i]
            shutil.copy(os.path.join(IMG, "full", src), os.path.join(out_full, name))
            shutil.copy(os.path.join(IMG, "thumb", src), os.path.join(out_th, name))
            drawings.append({"src": f"img/drawings/{name}", "thumb": f"img/drawings/thumb/{name}", "title": label})
            pick.append(n)
        ta.append({"name": aname, "pick": pick})
    tabs.append({"name": tname, "wide": True, "contain": True, "areas": ta})

js = "const DRAWINGS = " + json.dumps(drawings, ensure_ascii=False, indent=1) + ";\n"
js += "// Shop drawing tabs -> areas; pick = numbers in DRAWINGS (1-based)\nconst DRAWING_TABS = " + json.dumps(tabs, ensure_ascii=False) + ";"
p = os.path.join(SITE, "index.html"); h = open(p, encoding="utf-8").read()
assert "const DRAWINGS = [];" in h
h = h.replace("const DRAWINGS = [];", js, 1)
h = h.replace("const tabbed = { exterior: EXTERIOR_TABS, interior: INTERIOR_TABS };",
              "const tabbed = { exterior: EXTERIOR_TABS, interior: INTERIOR_TABS, drawings: DRAWING_TABS };", 1)
open(p, "w", encoding="utf-8").write(h)
print(len(drawings), "drawings")
