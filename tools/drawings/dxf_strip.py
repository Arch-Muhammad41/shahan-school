"""Copy a DXF dropping the ACDSDATA section and ACIS-based entities (3DSOLID, SURFACE family, REGION, BODY)."""
import sys
DROP = {"3DSOLID", "REGION", "BODY", "SURFACE", "EXTRUDEDSURFACE", "LOFTEDSURFACE", "REVOLVEDSURFACE",
        "SWEPTSURFACE", "PLANESURFACE", "NURBSURFACE"}
src = open(sys.argv[1], "rb"); dst = open(sys.argv[2], "wb", buffering=1 << 22)
section = None; grab = False; skip_ent = False; skip_sec = False; dropped = 0
while True:
    c = src.readline()
    if not c: break
    v = src.readline()
    cs = c.strip(); vs = v.strip()
    if cs == b"0" and vs == b"SECTION":
        # look ahead to the section name
        c2 = src.readline(); v2 = src.readline(); name = v2.strip()
        skip_sec = name == b"ACDSDATA"; section = name; skip_ent = False
        if not skip_sec: dst.write(c + v + c2 + v2)
        continue
    if skip_sec:
        if cs == b"0" and vs == b"ENDSEC": skip_sec = False
        continue
    if cs == b"0":
        skip_ent = section in (b"ENTITIES", b"BLOCKS") and vs.decode("latin1") in DROP
        if skip_ent: dropped += 1
    if not skip_ent: dst.write(c + v)
dst.close(); print("dropped", dropped)
