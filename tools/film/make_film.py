"""Build the construction film: title card, ~25 dated site clips with captions, end card, generated music.
usage: python make_film.py <ffmpeg.exe> <videos.json> <work dir> <site dir>"""
import sys, os, json, subprocess, math, wave, struct, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FF, VJ, WORK, SITE = sys.argv[1:5]
os.makedirs(WORK, exist_ok=True)
vids = [r for r in json.load(open(VJ)) if r["ok"]]
W, H, FPS, SEG, CH = 1280, 720, 30, 6.0, 3.5

# (index in videos.json, caption, month)
SHOTS = [
    (0,   "Site Preparation", "July 2025"),            (3,   "Excavation", "July 2025"),
    (9,   "Levelling the Site", "July 2025"),          (12,  "Soil Investigation", "August 2025"),
    (20,  "Concrete Pump Arrives", "August 2025"),     (22,  "Foundation Pour at Sunset", "August 2025"),
    (23,  "Night Concrete Pour", "August 2025"),       (28,  "The Site Takes Shape", "August 2025"),
    (36,  "Raft Foundation", "September 2025"),        (46,  "Pouring the Raft", "September 2025"),
    (48,  "Basement Slab Pour", "September 2025"),     (42,  "Wall Formwork", "September 2025"),
    (58,  "Basement Walls", "September 2025"),         (63,  "Wall Concrete", "September 2025"),
    (76,  "Basement Walls", "September 2025"),         (83,  "Columns & Formwork", "September 2025"),
    (91,  "Beam Reinforcement", "October 2025"),       (94,  "Slab Reinforcement", "October 2025"),
    (98,  "Slab Concrete", "October 2025"),            (105, "Ground Floor Slab", "October 2025"),
    (107, "Ground Floor Slab", "October 2025"),        (122, "Upper Floor Reinforcement", "November 2025"),
    (124, "Evening Pour", "November 2025"),            (125, "Slab Pour at Dusk", "November 2025"),
    (126, "The Site from Above", "November 2025"),     (137, "Sunset on the Slab", "November 2025"),
    (142, "First Floor Slab", "December 2025"),        (151, "Working Through the Night", "December 2025"),
    (152, "The Frame Rises", "December 2025"),         (154, "Pumping to the Top Floor", "December 2025"),
    (153, "The Frame Rises", "December 2025"),         (156, "Roof Slab", "January 2026"),
    (161, "The Site from Above", "February 2026"),     (162, "Roof Reinforcement", "February 2026"),
    (164, "Roof Slab Pour", "February 2026"),          (165, "The Concrete Crew", "February 2026"),
    (157, "Brick Walls", "February 2026"),             (158, "Brick Walls", "February 2026"),
    (159, "The Building Takes Shape", "February 2026"), (169, "Last Slab Pour", "March 2026"),
    (173, "Formwork & Pump", "March 2026"),            (176, "Inside the Building", "April 2026"),
    (178, "Masonry Complete", "April 2026"),           (177, "Boundary Wall Foundations", "April 2026"),
    (179, "Basement Ramp", "April 2026"),              (180, "Basement Works", "May 2026"),
    (183, "Waterproofing the Basement", "May 2026"),   (184, "Mechanical Pipes", "May 2026"),
    (204, "Façade Today", "2026"),                     (206, "Façade Today", "2026"),
    (208, "Façade Today", "2026"),
]

# chapter starts: (first shot index in SHOTS, title, dates)
CHAPTERS = [(0, "Site Preparation & Foundations", "July – September 2025"),
            (11, "Basement & Ground Floor", "September – November 2025"),
            (27, "The Frame Rises", "December 2025 – March 2026"),
            (41, "Walls, Services & Façade", "April 2026 – Today")]

def font(sz, bold=False):
    for f in (["C:/Windows/Fonts/georgiab.ttf", "C:/Windows/Fonts/arialbd.ttf"] if bold else ["C:/Windows/Fonts/georgia.ttf", "C:/Windows/Fonts/arial.ttf"]):
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def caption_png(text, month, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    g = Image.new("L", (W, 170)); gd = ImageDraw.Draw(g)
    for y in range(170): gd.line([(0, y), (W, y)], fill=int(170 * (y / 170) ** 1.6))
    im.paste((20, 8, 12, 255), (0, H - 170), g)
    d.rectangle([48, H - 92, 52, H - 40], fill=(190, 161, 69, 255))
    d.text((66, H - 96), text.upper(), font=font(30, True), fill=(255, 255, 255, 255))
    d.text((68, H - 56), month, font=font(20), fill=(227, 207, 138, 255))
    im.save(path)

def card(path, lines, logo=True):
    bg = Image.new("RGB", (W, H), (110, 26, 49)); d = ImageDraw.Draw(bg)
    for r in range(0, 900, 6):  # soft radial glow
        a = max(0, 60 - r // 15); d.ellipse([W / 2 - r, H / 2 - r - 40, W / 2 + r, H / 2 + r - 40], outline=(110 + a, 26 + a // 3, 49 + a // 3))
    y = 120
    if logo:
        lg = Image.open(os.path.join(SITE, "img", "logo.png")).convert("RGBA"); lg.thumbnail((170, 210))
        bg.paste(lg, ((W - lg.width) // 2, y), lg); y += lg.height + 30
    for txt, sz, bold, col in lines:
        f = font(sz, bold); tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y), txt, font=f, fill=col); y += sz + 18
    bg.save(path)

def run(args):
    r = subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error"] + args, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-1500:])

parts = []
# ---- opening card
card(os.path.join(WORK, "open.png"), [("SHAHAN SCHOOL", 54, True, (255, 255, 255)),
     ("CONSTRUCTION FILM", 26, False, (227, 207, 138)), ("July 2025 — 2026", 22, False, (240, 225, 230))])
# ---- closing card
card(os.path.join(WORK, "close.png"), [("Shahan Schools & Kindergarten", 40, True, (255, 255, 255)),
     ("Prepared by Arch. Muhammad Mudhafer  ·  Supervised by Home Engineering", 20, False, (240, 225, 230)),
     ("Project Manager Eng. Sherzad Jahfar  ·  Site Manager Eng. Ako Ahmed", 20, False, (240, 225, 230))])
for c, (_, title, dates) in enumerate(CHAPTERS):
    card(os.path.join(WORK, f"ch{c}.png"), [(f"CHAPTER {c + 1}", 24, False, (227, 207, 138)),
         (title.upper(), 50, True, (255, 255, 255)), (dates, 24, False, (240, 225, 230))], logo=False)
for name, dur in [("open", 4.0), ("close", 5.0)] + [(f"ch{c}", CH) for c in range(len(CHAPTERS))]:
    out = os.path.join(WORK, f"{name}.mp4")
    # a single still frame in; zoompan itself makes dur*FPS frames (looping the image would multiply that)
    run(["-i", os.path.join(WORK, f"{name}.png"), "-t", str(dur), "-vf",
         f"scale={W}:{H},zoompan=z='min(zoom+0.0006,1.06)':d={int(dur*FPS)}:s={W}x{H}:fps={FPS},fade=t=in:st=0:d=0.8,fade=t=out:st={dur-0.8}:d=0.8,format=yuv420p",
         "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-an", out])
parts.append(os.path.join(WORK, "open.mp4"))
T = 4.0; chap_meta = []; starts = {s: c for c, (s, _, _) in enumerate(CHAPTERS)}

# ---- site clips
for k, (i, text, month) in enumerate(SHOTS):
    if k in starts:
        c = starts[k]; chap_meta.append({"n": c + 1, "title": CHAPTERS[c][1], "dates": CHAPTERS[c][2], "t": round(T, 2)})
        parts.append(os.path.join(WORK, f"ch{c}.mp4")); T += CH
    v = vids[i]; cap = os.path.join(WORK, f"cap{k:02d}.png"); caption_png(text, month, cap)
    ln = round(min(SEG, v["dur"] - 0.3) * FPS) / FPS
    start = max(0.0, min(v["dur"] * 0.3, v["dur"] - ln - 0.15))
    vertical = v["h"] > v["w"]
    if vertical:   # blurred fill behind a vertical phone clip
        fc = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=20:2,eq=brightness=-0.08[bg];"
              f"[b]scale=-2:{H}[fg];[bg][fg]overlay=(W-w)/2:0[v0];")
    else:
        fc = f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}[v0];"
    fc += (f"[v0]fps={FPS},setsar=1[v1];[v1][1:v]overlay=0:0,fade=t=in:st=0:d=0.4,fade=t=out:st={ln-0.4}:d=0.4,format=yuv420p[v]")
    out = os.path.join(WORK, f"clip{k:02d}.mp4")
    run(["-ss", f"{start:.2f}", "-t", f"{ln:.3f}", "-i", v["path"], "-loop", "1", "-t", f"{ln:.3f}", "-i", cap,
         "-filter_complex", fc, "-map", "[v]", "-an", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "24", out])
    parts.append(out); T += ln; print("clip", k, text, ln, flush=True)
parts.append(os.path.join(WORK, "close.mp4"))

# ---- join
lst = os.path.join(WORK, "list.txt")
open(lst, "w").write("".join(f"file '{p.replace(os.sep, '/')}'\n" for p in parts))
silent = os.path.join(WORK, "silent.mp4")
run(["-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])
total = T + 5.0
json.dump(chap_meta, open(os.path.join(SITE, "video", "film-chapters.json"), "w"), indent=1, ensure_ascii=False)

# ---- music (generated): warm A-major pad with slow chord changes + soft bells, fades in and out
sr = 44100; n = int(total * sr); t = np.arange(n) / sr
A = 440.0; f = lambda s: A * 2 ** (s / 12)
chords = [[-24, -17, -12, -8, -5], [-19, -15, -10, -7, -3], [-22, -15, -10, -6, -3], [-24, -17, -12, -8, -1]]   # A  D  F#m  A(add9)
bar = 6.0
mix = np.zeros(n)
for ci in range(int(total // bar) + 1):
    ch = chords[ci % len(chords)]; s0 = int(ci * bar * sr); s1 = min(n, int((ci + 1) * bar * sr + sr))
    if s0 >= n: break
    tt = t[s0:s1] - ci * bar
    env = np.minimum(1, tt / 1.5) * np.minimum(1, np.maximum(0, (bar + 1 - tt) / 1.5))
    for j, s in enumerate(ch):
        fr = f(s); amp = .10 if j == 0 else .05
        mix[s0:s1] += amp * env * (np.sin(2 * np.pi * fr * tt) + .3 * np.sin(2 * np.pi * fr * 1.003 * tt))
random.seed(7)
scale = [0, 2, 4, 7, 9, 12, 14, 16]
for k in range(int(total / 1.7)):          # gentle bell melody
    st = 2.0 + k * 1.7 + random.choice([0, .0, .85]); s = scale[(k * 3 + random.randint(0, 2)) % len(scale)]
    i0 = int(st * sr)
    if i0 >= n: break
    dur = min(n - i0, int(2.5 * sr)); tt = np.arange(dur) / sr; fr = f(s)
    mix[i0:i0 + dur] += .06 * np.exp(-tt * 2.2) * (np.sin(2 * np.pi * fr * tt) + .3 * np.sin(4 * np.pi * fr * tt))
# simple echo for space, then overall fade
d1 = int(.32 * sr); mix[d1:] += .35 * mix[:-d1]
fade = np.minimum(1, t / 2.5) * np.minimum(1, (total - t) / 3.5)
mix *= fade; mix /= max(1e-6, np.abs(mix).max()) / .8
wav = os.path.join(WORK, "music.wav")
with wave.open(wav, "w") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    w.writeframes((mix * 32767).astype("<i2").tobytes())

# ---- final film + poster
os.makedirs(os.path.join(SITE, "video"), exist_ok=True)
final = os.path.join(SITE, "video", "construction-film.mp4")
run(["-i", silent, "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", final])
run(["-ss", str(4.0 + CH + SEG * 2.5), "-i", final, "-frames:v", "1", "-q:v", "3", os.path.join(SITE, "video", "construction-film.jpg")])
print("done", round(total, 1), "s", round(os.path.getsize(final) / 1e6, 1), "MB")
