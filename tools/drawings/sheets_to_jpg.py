"""PDF sheets -> trimmed JPG (3200 px wide) + thumbs + numbered contact sheets for review."""
import sys, os, json, io
import pymupdf
from PIL import Image, ImageOps, ImageDraw
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out + "/full", exist_ok=True); os.makedirs(out + "/thumb", exist_ok=True)
S = json.load(open(sys.argv[3], encoding="utf-8"))
thumbs = []
for i in range(len(S)):
    p = os.path.join(src, "p%03d.pdf" % i)
    if not os.path.exists(p): continue
    pg = pymupdf.open(p)[0]
    pix = pg.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    bb = ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 40 else 0).getbbox()
    if bb: im = im.crop((max(0, bb[0] - 20), max(0, bb[1] - 20), min(im.width, bb[2] + 20), min(im.height, bb[3] + 20)))
    if im.width > 3200: im = im.resize((3200, round(im.height * 3200 / im.width)), Image.LANCZOS)
    im.save(f"{out}/full/{i:03d}.jpg", quality=82, optimize=True)
    t = im.copy(); t.thumbnail((640, 640), Image.LANCZOS); t.save(f"{out}/thumb/{i:03d}.jpg", quality=80)
    thumbs.append((i, t)); print(i, im.size, flush=True)
cols, cw, ch = 6, 330, 250
for s in range(0, len(thumbs), 36):
    chunk = thumbs[s:s + 36]; sheet = Image.new("RGB", (cols * cw, ((len(chunk) + cols - 1) // cols) * ch), "white"); d = ImageDraw.Draw(sheet)
    for k, (i, t) in enumerate(chunk):
        x, y = (k % cols) * cw, (k // cols) * ch; tt = t.copy(); tt.thumbnail((320, 220)); sheet.paste(tt, (x + 5, y + 22))
        d.text((x + 5, y + 4), f"{i} {S[i]['no']} {S[i]['title'][:34]}", fill="red")
    sheet.save(f"{out}/review_{s // 36}.jpg", quality=80)
