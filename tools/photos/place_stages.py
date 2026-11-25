"""Combine picks from both folders into stages 1-2, sort each stage by capture date, write web JPGs + thumbs."""
import sys, os, json, shutil
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

BIG_JSON, SMALL_DIR, SITE = sys.argv[1], sys.argv[2], sys.argv[3]
big = json.load(open(BIG_JSON))
big26 = json.load(open(sys.argv[4]))
S2_2026 = [165, 463, 512, 548, 651, 656, 731, 162]

S1_BIG = [2, 7, 11, 14, 19, 24, 99, 101]
S2_BIG = [20, 23, 40, 122, 142, 182, 186, 205, 223, 254, 267, 297, 335, 349, 385,
          436, 446, 527, 549, 600, 636, 658, 683, 704, 764, 789, 815, 852, 866, 928]
S1_SMALL = ["IMG_8156", "IMG_8157", "IMG_8219"]
S2_SMALL = ["IMG_8253", "IMG_8317", "IMG_8336", "IMG_8617", "IMG_8632", "IMG_8646", "IMG_8662", "IMG_8663", "IMG_8698", "IMG_8790"]

def small_path(n):
    for ext in (".HEIC", ".JPG", ".heic", ".jpg"):
        p = os.path.join(SMALL_DIR, n + ext)
        if os.path.exists(p): return p
    raise FileNotFoundError(n)

import re, time
def taken(path):
    try:
        ex = Image.open(path).getexif()
        d = ex.get_ifd(0x8769).get(36867) or ex.get(306)
        if d: return str(d)
    except Exception:
        pass
    m = re.search(r"(20\d\d)[-_]?(\d\d)[-_]?(\d\d)", os.path.basename(path))
    if m: return f"{m[1]}:{m[2]}:{m[3]} 12:00:00"
    # iPhone IMG_nnnn without EXIF: borrow the date of the nearest earlier-numbered photo that has one
    m = re.match(r"IMG_(\d+)", os.path.basename(path))
    if m:
        n = int(m[1]); best = None
        for f in os.listdir(SMALL_DIR):
            mm = re.match(r"IMG_(\d+)\.(heic|jpg)$", f, re.I)
            if mm and int(mm[1]) != n and abs(int(mm[1]) - n) < 1000 and (best is None or abs(int(mm[1]) - n) < abs(best[0] - n)):
                try:
                    ex = Image.open(os.path.join(SMALL_DIR, f)).getexif()
                    d = ex.get_ifd(0x8769).get(36867) or ex.get(306)
                    if d: best = (int(mm[1]), str(d))
                except Exception:
                    pass
        if best: return best[1][:-2] + f"{n % 60:02d}"
    return time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(os.path.getmtime(path)))

def build(folder, paths):
    paths = sorted(set(paths), key=taken)
    out = os.path.join(SITE, "img", "construction", folder)
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(os.path.join(out, "thumb"))
    for k, p in enumerate(paths, 1):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        fn = f"{k:02d}.jpg"
        b = im.copy(); b.thumbnail((1800, 1800), Image.LANCZOS)
        b.save(os.path.join(out, fn), "JPEG", quality=80, optimize=True, progressive=True)
        t = im.copy(); t.thumbnail((520, 520), Image.LANCZOS)
        t.save(os.path.join(out, "thumb", fn), "JPEG", quality=76, optimize=True, progressive=True)
    first, last = taken(paths[0])[:10], taken(paths[-1])[:10]
    print(folder, len(paths), first, "->", last)
    return len(paths)

n1 = build("s1", [big[i]["path"] for i in S1_BIG] + [small_path(n) for n in S1_SMALL])
n2 = build("s2", [big[i]["path"] for i in S2_BIG] + [small_path(n) for n in S2_SMALL] + [big26[i]["path"] for i in S2_2026])
print(json.dumps({"s1": n1, "s2": n2}))

