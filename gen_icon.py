#!/usr/bin/env python3
"""Inner Compass — 8-pointed compass star icon (180×180 PNG, no external deps)."""
import struct, zlib, math

SIZE = 180
CX, CY = 90.0, 90.0

def lc(c1, c2, t):
    t = max(0.0, min(1.0, float(t)))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def dd(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def needle(angle_deg, tip_r, base_r, half_w):
    """Returns (tip, left, right) for a triangular compass needle."""
    θ  = math.radians(angle_deg)
    dx, dy = math.sin(θ), -math.cos(θ)   # forward direction
    px, py = math.cos(θ),  math.sin(θ)   # perpendicular (screen coords)
    tip    = (CX + dx * tip_r,  CY + dy * tip_r)
    bc     = (CX + dx * base_r, CY + dy * base_r)
    left   = (bc[0] + px * half_w, bc[1] + py * half_w)
    right  = (bc[0] - px * half_w, bc[1] - py * half_w)
    return tip, left, right

def tri_sign(px, py, x1, y1, x2, y2):
    return (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)

def in_tri(px, py, v1, v2, v3):
    x, y = px + 0.5, py + 0.5
    d1 = tri_sign(x, y, v1[0], v1[1], v2[0], v2[1])
    d2 = tri_sign(x, y, v2[0], v2[1], v3[0], v3[1])
    d3 = tri_sign(x, y, v3[0], v3[1], v1[0], v1[1])
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))

# ── Color palette ──────────────────────────────────────────
BG_TL  = ( 52,  78, 120)   # top-left
BG_BR  = ( 22,  42,  72)   # bottom-right
NORTH  = (224, 122,  95)   # terracotta  (N)
SOUTH  = lc(NORTH, (255,255,255), 0.40)  # muted terracotta (S)
EW_COL = (230, 238, 250)   # cool white  (E, W)
DIAG   = (140, 165, 202)   # blue-grey   (NE, SE, SW, NW)
RING   = (255, 255, 255)
CDOT   = ( 36,  58,  94)   # centre dot

# ── 8 compass needles: (angle°, triangles, fill) ──────────
# Cardinals  – long, prominent
# Diagonals  – shorter, subtle
NEEDLES = [
    needle(  0,  66, 13, 9.5),  # N  → painted last = on top
    needle(180,  66, 13, 9.5),  # S
    needle( 90,  66, 13, 9.5),  # E
    needle(270,  66, 13, 9.5),  # W
    needle( 45,  42, 11, 5.5),  # NE
    needle(135,  42, 11, 5.5),  # SE
    needle(225,  42, 11, 5.5),  # SW
    needle(315,  42, 11, 5.5),  # NW
]
NEEDLE_COLORS = [NORTH, SOUTH, EW_COL, EW_COL, DIAG, DIAG, DIAG, DIAG]

rows = []
for y in range(SIZE):
    row = []
    for x in range(SIZE):
        pcx, pcy = x + 0.5, y + 0.5

        # Gradient background
        t = (x + y) / (2 * SIZE - 2)
        color = lc(BG_TL, BG_BR, t)

        d = dd(pcx, pcy, CX, CY)

        # Outer decorative ring  r=70
        ring_t = max(0.0, 1.0 - abs(d - 70.0) / 1.2)
        if ring_t > 0:
            color = lc(color, RING, 0.28 * ring_t)

        # Inner decorative ring  r=57
        ring_t2 = max(0.0, 1.0 - abs(d - 57.0) / 0.9)
        if ring_t2 > 0:
            color = lc(color, RING, 0.13 * ring_t2)

        # Compass needles (order: diagonals first, then cardinals on top)
        for i, (tip, left, right) in enumerate(NEEDLES):
            if in_tri(x, y, tip, left, right):
                color = NEEDLE_COLORS[i]

        # Center white circle  r=11.5
        if d <= 11.5:
            a = min(1.0, 12.0 - d)
            color = lc(color, RING, a)

        # Centre dot  r=5.5
        if d <= 5.5:
            a = min(1.0, 6.0 - d)
            color = lc(color, CDOT, a)

        row.append(color)
    rows.append(row)

# ── Write PNG ──────────────────────────────────────────────
def chunk(tag, data):
    p = tag + data
    return struct.pack('>I', len(data)) + p + struct.pack('>I', zlib.crc32(p) & 0xFFFFFFFF)

raw = b''
for row in rows:
    raw += b'\x00'
    for r, g, b in row:
        raw += bytes([r, g, b])

out = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>II', SIZE, SIZE) + bytes([8, 2, 0, 0, 0]))
       + chunk(b'IDAT', zlib.compress(raw, 9))
       + chunk(b'IEND', b''))

path = '/Users/htharka/dev/sandbox/self_dev/icon.png'
with open(path, 'wb') as f:
    f.write(out)
print(f'Written {path}  ({SIZE}×{SIZE},  {len(out):,} bytes)')
