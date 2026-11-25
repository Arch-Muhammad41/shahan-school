import sys, os, json
from PIL import Image, ImageDraw
OUT = sys.argv[1]; TH = int(sys.argv[2])
rows = json.load(open(os.path.join(OUT, "keep.json")))
final = []
for r in rows:
    # compare with the last 6 kept photos of the same folder
    recent = [x for x in final[-12:] if os.path.dirname(x["path"]) == os.path.dirname(r["path"])]
    dup = next((x for x in recent if bin(x["hash"] ^ r["hash"]).count("1") <= TH), None)
    if dup:
        if r["sharp"] > dup["sharp"]:
            final[final.index(dup)] = r
        continue
    final.append(r)
json.dump(final, open(os.path.join(OUT, "keep2.json"), "w"))
for f in os.listdir(OUT):
    if f.startswith("sheet_"): os.remove(os.path.join(OUT, f))
per, cols, cw, chh = 100, 10, 250, 260
for s in range(0, len(final), per):
    chunk = final[s:s + per]
    nrows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, nrows * chh), "white")
    d = ImageDraw.Draw(sheet)
    for k, r in enumerate(chunk):
        x, y = (k % cols) * cw, (k // cols) * chh
        sheet.paste(Image.open(r["thumb"]), (x + 5, y + 5))
        d.rectangle([x + 5, y + 5, x + 52, y + 24], fill="black")
        d.text((x + 9, y + 8), str(s + k), fill="yellow")
    sheet.save(os.path.join(OUT, f"sheet_{s // per:02d}.jpg"), quality=78)
folders = {}
for i, r in enumerate(final):
    folders.setdefault(os.path.basename(os.path.dirname(r["path"])), []).append(i)
print(len(final), {k: (v[0], v[-1]) for k, v in folders.items()}, "sheets:", (len(final) + per - 1) // per)

