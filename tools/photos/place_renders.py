import sys, os, glob
from PIL import Image

src, site = sys.argv[1], sys.argv[2]
skip = {"p001.jpg", "p106.jpg"}          # DIORAMA cover pages with text
full = os.path.join(site, "img", "interior")
thumb = os.path.join(full, "thumb")
os.makedirs(thumb, exist_ok=True)
files = sorted(f for f in os.listdir(src) if f.startswith("p") and f.endswith(".jpg") and f not in skip)
names = []
for k, f in enumerate(files, 1):
    im = Image.open(os.path.join(src, f)).convert("RGB")
    name = f"{k:02d}.jpg"
    big = im.copy(); big.thumbnail((1800, 1800), Image.LANCZOS)
    big.save(os.path.join(full, name), "JPEG", quality=82, optimize=True, progressive=True)
    sm = im.copy(); sm.thumbnail((640, 640), Image.LANCZOS)
    sm.save(os.path.join(thumb, name), "JPEG", quality=78, optimize=True, progressive=True)
    names.append(name)
total = sum(os.path.getsize(p) for p in glob.glob(os.path.join(full, "**", "*.jpg"), recursive=True))
print(len(names), "images,", total // (1024 * 1024), "MB total")
