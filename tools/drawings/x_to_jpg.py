import json, io, pymupdf
from PIL import Image, ImageOps, ImageDraw
N = json.load(open("sheets/x_names.json")); th = []
for i, n in enumerate(N):
    pg = pymupdf.open(f"sheets/x{i:02d}.pdf")[0]
    im = Image.open(io.BytesIO(pg.get_pixmap(matrix=pymupdf.Matrix(1.6, 1.6), alpha=False).tobytes("png"))).convert("RGB")
    bb = ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 40 else 0).getbbox()
    if bb: im = im.crop((max(0, bb[0]-30), max(0, bb[1]-30), min(im.width, bb[2]+30), min(im.height, bb[3]+30)))
    if im.width > 3200: im = im.resize((3200, round(im.height*3200/im.width)), Image.LANCZOS)
    im.save(f"sheets/img/full/x{i:02d}.jpg", quality=82, optimize=True)
    t = im.copy(); t.thumbnail((640, 640), Image.LANCZOS); t.save(f"sheets/img/thumb/x{i:02d}.jpg", quality=80); th.append(t)
sheet = Image.new("RGB", (6*330, 3*250), "white"); d = ImageDraw.Draw(sheet)
for k, t in enumerate(th):
    x, y = (k % 6)*330, (k // 6)*250; tt = t.copy(); tt.thumbnail((320, 220)); sheet.paste(tt, (x+5, y+22)); d.text((x+5, y+4), f"x{k} {N[k]}", fill="red")
sheet.save("sheets/img/review_x.jpg", quality=80); print("ok")
