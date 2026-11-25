import sys, os
from PIL import Image, ImageOps, ImageDraw
import pillow_heif
pillow_heif.register_heif_opener()

src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
files = sorted(f for f in os.listdir(src) if f.lower().endswith((".heic", ".jpg", ".jpeg", ".png")))
thumbs = []
for f in files:
    im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert("RGB")
    name = os.path.splitext(f)[0] + ".jpg"
    big = im.copy(); big.thumbnail((1800, 1800), Image.LANCZOS)
    big.save(os.path.join(out, name), "JPEG", quality=82, optimize=True, progressive=True)
    t = im.copy(); t.thumbnail((300, 300)); thumbs.append((os.path.splitext(f)[0], t))
    print(name, im.size)

cols, cell = 6, 310
for part in range(0, len(thumbs), 18):
    chunk = thumbs[part:part + 18]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for k, (n, t) in enumerate(chunk):
        x, y = (k % cols) * cell, (k // cols) * (cell + 24)
        sheet.paste(t, (x + 5, y + 5))
        d.text((x + 8, y + cell + 4), n, fill="red")
    sheet.save(os.path.join(out, f"_sheet{part // 18 + 1}.jpg"), quality=82)
print("total", len(files))
