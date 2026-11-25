"""Collect every modelspace TEXT/MTEXT with insertion point + height, and layer extents, to JSON."""
import sys, json, re
f = open(sys.argv[1], "r", encoding="cp1256", errors="replace")
out = sys.argv[2]
section = None; grab = False; cur = None; rec = None; rows = []
def flush():
    if rec and rec.get("t"): rows.append(rec)
while True:
    c = f.readline()
    if not c: break
    v = f.readline().rstrip("\r\n"); c = c.strip()
    if c == "0" and v == "SECTION": grab = True; continue
    if grab and c == "2": section = v; grab = False; continue
    if section != "ENTITIES": continue
    if c == "0":
        flush(); rec = {"k": v, "t": ""} if v in ("TEXT", "MTEXT") else None; continue
    if rec is None: continue
    if c == "8": rec["l"] = v
    elif c == "10": rec["x"] = float(v)
    elif c == "20": rec["y"] = float(v)
    elif c == "40" and "h" not in rec: rec["h"] = float(v)
    elif c in ("1", "3"): rec["t"] += v
    elif c == "67": rec["ps"] = v
flush()
for r in rows:
    t = re.sub(r"\\[A-Za-z][^;\\{}]*;", "", r["t"]); t = re.sub(r"\\P", " ", t); r["t"] = re.sub(r"[{}]", "", t).strip()
json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(len(rows))
