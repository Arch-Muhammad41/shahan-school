"""Extract the embedded render image of every text-free page, plus a numbered contact sheet."""
import sys, os, io
import pymupdf as fitz
from PIL import Image, ImageDraw

src, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
doc = fitz.open(src)
thumbs = []
for i, p in enumerate(doc):
    n = i + 1
    if " ".join(p.get_text().split()):
        continue
    imgs = p.get_images(full=True)
    if len(imgs) != 1 or imgs[0][2] < 1000:
        continue
    pix = fitz.Pixmap(doc, imgs[0][0])
    if pix.n - pix.alpha >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    im.save(os.path.join(outdir, f"p{n:03d}.jpg"), "JPEG", quality=90)
    # also render the full page to see whether anything is drawn on top of the image
    page_png = p.get_pixmap(dpi=40)
    pim = Image.open(io.BytesIO(page_png.tobytes("png"))).convert("RGB")
    t = im.copy(); t.thumbnail((300, 300)); thumbs.append((n, t, pim))
cols, cw, ch = 6, 320, 260
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
d = ImageDraw.Draw(sheet)
for k, (n, t, _) in enumerate(thumbs):
    x, y = (k % cols) * cw, (k // cols) * ch
    sheet.paste(t, (x + 5, y + 5))
    d.rectangle([x + 5, y + 5, x + 50, y + 24], fill="black"); d.text((x + 9, y + 8), f"p{n}", fill="yellow")
sheet.save(os.path.join(outdir, "_sheet.jpg"), quality=82)
# one full page render, to check overlays
thumbs[0][2].save(os.path.join(outdir, "_page_render.jpg"))
print(len(thumbs), "renders; size", im.size)
