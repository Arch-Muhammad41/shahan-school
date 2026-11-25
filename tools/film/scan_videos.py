"""List every site video with length, date and a middle frame; write a numbered contact sheet."""
import sys, os, re, json, time
import cv2
from PIL import Image, ImageDraw

roots, out = sys.argv[1:-1], sys.argv[-1]
os.makedirs(out, exist_ok=True)
vids = []
for r in roots:
    for dp, _, fs in os.walk(r):
        for f in fs:
            if f.lower().endswith((".mp4", ".mov")) and "(2)" not in f:
                vids.append(os.path.join(dp, f))

def date_of(p):
    m = re.search(r"(20\d\d)[-_]?(\d\d)[-_]?(\d\d)", os.path.basename(p))
    if m: return f"{m[1]}-{m[2]}-{m[3]}"
    return time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(p)))

rows = []
for p in vids:
    cap = cv2.VideoCapture(p)
    n, fps = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS) or 30
    w, h = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    dur = n / fps if n > 0 else 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, int(n * .4)))
    ok, fr = cap.read(); cap.release()
    th = None
    if ok:
        im = Image.fromarray(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)); im.thumbnail((240, 240))
        th = os.path.join(out, f"v{len(rows):03d}.jpg"); im.save(th, quality=70)
    rows.append(dict(path=p, dur=round(dur, 1), w=int(w), h=int(h), date=date_of(p), thumb=th, ok=ok))
rows.sort(key=lambda r: (r["date"], r["path"]))
json.dump(rows, open(os.path.join(out, "videos.json"), "w"))
good = [r for r in rows if r["ok"]]
per, cols, cw, ch = 60, 10, 250, 270
for s in range(0, len(good), per):
    chunk = good[s:s + per]; nrows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, nrows * ch), "white"); d = ImageDraw.Draw(sheet)
    for k, r in enumerate(chunk):
        x, y = (k % cols) * cw, (k // cols) * ch
        sheet.paste(Image.open(r["thumb"]), (x + 5, y + 5))
        d.rectangle([x + 5, y + 5, x + 200, y + 24], fill="black")
        d.text((x + 9, y + 8), f"{s + k} {r['date']} {r['dur']}s {'V' if r['h'] > r['w'] else 'H'}", fill="yellow")
    sheet.save(os.path.join(out, f"vsheet_{s // per}.jpg"), quality=78)
print(len(rows), "videos;", len(good), "readable; total min", round(sum(r["dur"] for r in good) / 60, 1))
print("unreadable:", [os.path.basename(r["path"]) for r in rows if not r["ok"]][:20])
