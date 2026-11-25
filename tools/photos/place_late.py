"""Rebuild stages 3-6 from the August 2026 iPhone photos plus the November 2026 WhatsApp photos, sorted by date."""
import sys, os, re, time, shutil, json
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

CH, AKO, SITE = sys.argv[1], sys.argv[2], sys.argv[3]
big26 = json.load(open(sys.argv[4]))
AKO2 = os.path.join(AKO, "بەشی ٢")
ls = lambda d: sorted(f for f in os.listdir(d) if f.lower().endswith((".jpg", ".jpeg", ".png")))
ako, ako2 = ls(AKO), ls(AKO2)

# stage: (iPhone Aug-2026 names, Nov-2026 folder indices, Sep/Oct-2026 "بەشی ٢" indices)
STAGES = {
    # Review 2026-11-23: dropped duplicate views; no steel in the windows/curtain-wall stage (aluminium only);
    # concrete pump outside (Nov #11) and drainage pit (Nov #13) moved to External Works.
    "s3": (["IMG_1733", "IMG_1734", "IMG_1815", "IMG_1816", "IMG_1822"], [0, 2, 28], [0]),
    "s4": (["IMG_1802", "IMG_1805", "IMG_1808"],
           [8, 16, 18, 21, 22, 23, 26, 29, 30], [1, 3, 10, 15, 17, 28]),
    "win": (["IMG_1825", "IMG_1826"], [6, 10, 17], [29]),
    "s5": (["IMG_1819", "IMG_1821", "IMG_1824"], [5, 12, 15, 20, 24, 27], [11, 18, 24, 25, 30, 32]),
    "s6": (["IMG_1818", "IMG_1823"], [1, 3, 4, 14, 19, 25], [2, 5, 6, 9, 16, 21, 22, 27]),
    "ext": ([], [11, 13], [13, 14, 19]),
}

def ch_path(n):
    for ext in (".HEIC", ".JPG", ".heic", ".jpg"):
        p = os.path.join(CH, n + ext)
        if os.path.exists(p): return p
    raise FileNotFoundError(n)

def taken(p):
    try:
        ex = Image.open(p).getexif()
        d = ex.get_ifd(0x8769).get(36867) or ex.get(306)
        if d: return str(d)
    except Exception:
        pass
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d) at (\d+)\.(\d\d)\.(\d\d) ?(AM|PM)?", os.path.basename(p))
    if m:
        h = int(m[4]) % 12 + (12 if m[7] == "PM" else 0)
        return f"{m[1]}:{m[2]}:{m[3]} {h:02d}:{m[5]}:{m[6]}"
    return time.strftime("%Y:%m:%d %H:%M:%S", time.localtime(os.path.getmtime(p)))

result = {}
EXTRA = {'s3': [194, 669, 690, 751, 753, 765, 768, 776, 780, 801, 850, 857], 's4': [262, 270, 297], 'win': [247], 's5': [222, 225, 243, 274, 288, 891], 's6': [231, 253, 256, 278, 291, 804, 879, 885], 'ext': [216, 583, 589, 786, 790, 793, 821, 831, 848, 871, 873]}
STAGES["wp"] = ([], [], [])
EXTRA["wp"] = [133, 136, 815, 818, 855, 856, 864]
for st, (chs, idx, idx2) in STAGES.items():
    paths = [ch_path(n) for n in chs] + [os.path.join(AKO, ako[i]) for i in idx] + [os.path.join(AKO2, ako2[i]) for i in idx2] + [big26[i]["path"] for i in EXTRA.get(st, [])]
    paths.sort(key=taken)
    out = os.path.join(SITE, "img", "construction", st)
    shutil.rmtree(out, ignore_errors=True); os.makedirs(os.path.join(out, "thumb"))
    for k, p in enumerate(paths, 1):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        fn = f"{k:02d}.jpg"
        b = im.copy(); b.thumbnail((1800, 1800), Image.LANCZOS)
        b.save(os.path.join(out, fn), "JPEG", quality=80, optimize=True, progressive=True)
        t = im.copy(); t.thumbnail((520, 520), Image.LANCZOS)
        t.save(os.path.join(out, "thumb", fn), "JPEG", quality=76, optimize=True, progressive=True)
    result[st] = (len(paths), taken(paths[0])[:10], taken(paths[-1])[:10])
print(json.dumps(result))

