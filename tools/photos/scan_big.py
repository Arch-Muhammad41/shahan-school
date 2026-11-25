"""Scan a big photo folder: score sharpness, drop near-duplicates, write contact sheets of the keepers."""
import sys, os, json
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageOps, ImageDraw
import numpy as np, cv2

ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

def analyse(path):
    try:
        im = Image.open(path)
        im.draft("RGB", (640, 640))          # fast JPEG decode at reduced size
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((640, 640))
        g = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
        sharp = float(cv2.Laplacian(g, cv2.CV_64F).var())
        bright = float(g.mean())
        small = cv2.resize(g, (9, 8), interpolation=cv2.INTER_AREA)
        dh = (small[:, 1:] > small[:, :-1]).flatten()
        h = int("".join("1" if b else "0" for b in dh), 2)
        t = im.copy(); t.thumbnail((240, 240))
        tp = os.path.join(OUT, "t", os.path.relpath(path, ROOT).replace(os.sep, "__") + ".jpg")
        os.makedirs(os.path.dirname(tp), exist_ok=True)
        t.save(tp, quality=70)
        return dict(path=path, sharp=sharp, bright=bright, hash=h, thumb=tp, w=im.width, h_=im.height)
    except Exception as e:
        return dict(path=path, error=str(e))

if __name__ == "__main__":
    files = []
    for dp, _, fs in os.walk(ROOT):
        for f in fs:
            if f.lower().endswith((".jpg", ".jpeg")):
                files.append(os.path.join(dp, f))
    files.sort()
    with ProcessPoolExecutor() as ex:
        res = list(ex.map(analyse, files, chunksize=8))
    ok = [r for r in res if "error" not in r]
    # drop blurry / too dark
    keep = [r for r in ok if r["sharp"] > 60 and 35 < r["bright"] < 235]
    # near-duplicate removal within each folder (keep the sharpest of a burst)
    keep.sort(key=lambda r: (os.path.dirname(r["path"]), os.path.basename(r["path"])))
    final, last = [], None
    for r in keep:
        if last and os.path.dirname(last["path"]) == os.path.dirname(r["path"]) and bin(last["hash"] ^ r["hash"]).count("1") <= 10:
            if r["sharp"] > last["sharp"]:
                final[-1] = r; last = r
            continue
        final.append(r); last = r
    json.dump(final, open(os.path.join(OUT, "keep.json"), "w"))
    print(f"scanned {len(files)}, errors {len(res)-len(ok)}, sharp&lit {len(keep)}, after dedupe {len(final)}")
    # contact sheets: 8 x 6 = 48 per sheet, labelled with an index
    per, cols, cw, chh = 48, 8, 250, 270
    for s in range(0, len(final), per):
        chunk = final[s:s + per]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rows * chh), "white")
        d = ImageDraw.Draw(sheet)
        for k, r in enumerate(chunk):
            x, y = (k % cols) * cw, (k // cols) * chh
            t = Image.open(r["thumb"]); sheet.paste(t, (x + 5, y + 5))
            d.rectangle([x + 5, y + 5, x + 48, y + 22], fill="black")
            d.text((x + 8, y + 7), str(s + k), fill="yellow")
        sheet.save(os.path.join(OUT, f"sheet_{s // per:02d}.jpg"), quality=78)
    folders = {}
    for i, r in enumerate(final):
        folders.setdefault(os.path.relpath(os.path.dirname(r["path"]), ROOT), []).append(i)
    print({k: (v[0], v[-1]) for k, v in folders.items()})
