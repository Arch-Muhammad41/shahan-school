import sys
from PIL import Image

src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGBA")
px = im.load()
w, h = im.size
# Make near-white background transparent with a soft edge
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        m = min(r, g, b)
        if m > 245:
            px[x, y] = (r, g, b, 0)
        elif m > 225:
            px[x, y] = (r, g, b, int(255 * (245 - m) / 20))
bbox = im.getbbox()
im = im.crop(bbox)
im.save(out, optimize=True)
# Sample brand colours
print("size", im.size)
print("maroon", im.getpixel((im.size[0] // 2, int(im.size[1] * 0.75))))
print("gold", im.getpixel((im.size[0] // 2, 6)))
