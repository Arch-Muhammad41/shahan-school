"""Stream a huge DXF: sections sizes, layouts, block count, entity counts in entities section, top texts."""
import sys, collections
f = open(sys.argv[1], "r", encoding="cp1256", errors="replace")
def pairs():
    while True:
        c = f.readline()
        if not c: return
        v = f.readline().rstrip("\r\n")
        yield c.strip(), v
section = None; prev = None; ent = collections.Counter(); sec_lines = collections.Counter()
layouts = []; in_layout = False; blocks = 0; texts = collections.Counter(); cur = None; owner_ps = 0
layers = collections.Counter(); curlayer = None; inserts = collections.Counter(); grab = None
n = 0
for c, v in pairs():
    n += 1
    if c == "0" and v == "SECTION": grab = "sec"; continue
    if grab == "sec" and c == "2": section = v; grab = None; continue
    sec_lines[section] += 1
    if c == "0":
        cur = v
        if section == "ENTITIES": ent[v] += 1
        if section == "BLOCKS" and v == "BLOCK": blocks += 1
        in_layout = False
    if section == "OBJECTS" and c == "100" and v == "AcDbLayout": in_layout = True
    if in_layout and c == "1": layouts.append(v); in_layout = False
    if section == "ENTITIES":
        if c == "8": layers[v] += 1
        if cur in ("TEXT", "MTEXT") and c == "1" and 3 < len(v) < 80: texts[v] += 1
        if cur == "INSERT" and c == "2": inserts[v] += 1
print("pairs", n)
print("sections", dict(sec_lines))
print("layouts", layouts)
print("blocks", blocks)
print("entities", ent.most_common(20))
print("layers", layers.most_common(40))
print("inserts", inserts.most_common(30))
print("texts", [t for t, _ in texts.most_common(150)])
