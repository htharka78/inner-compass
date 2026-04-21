#!/usr/bin/env python3
"""Generate 4 icon variants for Inner Compass."""
import struct, zlib, math, os

SIZE = 180
CX, CY = 90.0, 90.0
OUT = os.path.dirname(os.path.abspath(__file__))

def lc(c1, c2, t):
    t = max(0.0, min(1.0, float(t)))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def dist(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def needle(angle_deg, tip_r, base_r, half_w):
    θ  = math.radians(angle_deg)
    dx, dy = math.sin(θ), -math.cos(θ)
    px, py = math.cos(θ),  math.sin(θ)
    tip   = (CX + dx * tip_r,  CY + dy * tip_r)
    bc    = (CX + dx * base_r, CY + dy * base_r)
    left  = (bc[0] + px * half_w, bc[1] + py * half_w)
    right = (bc[0] - px * half_w, bc[1] - py * half_w)
    return tip, left, right

def tri_sign(px, py, x1, y1, x2, y2):
    return (px - x2) * (y1 - y2) - (x1 - x2) * (py - y2)

def in_tri(px, py, v1, v2, v3):
    x, y = px + 0.5, py + 0.5
    d1 = tri_sign(x, y, v1[0], v1[1], v2[0], v2[1])
    d2 = tri_sign(x, y, v2[0], v2[1], v3[0], v3[1])
    d3 = tri_sign(x, y, v3[0], v3[1], v1[0], v1[1])
    return not ((d1 < 0 or d2 < 0 or d3 < 0) and (d1 > 0 or d2 > 0 or d3 > 0))

def write_png(rows, path):
    raw = b''
    for row in rows:
        raw += b'\x00'
        for r, g, b in row:
            raw += bytes([r, g, b])
    def chunk(tag, data):
        p = tag + data
        return struct.pack('>I', len(data)) + p + struct.pack('>I', zlib.crc32(p) & 0xFFFFFFFF)
    out = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>II', SIZE, SIZE) + bytes([8, 2, 0, 0, 0]))
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(out)
    print(f'  {path}  ({len(out):,} bytes)')

def render(bg_tl, bg_br, needles_def, needle_colors, ring_color, center_fill, center_dot, path):
    rows = []
    for y in range(SIZE):
        row = []
        for x in range(SIZE):
            t = (x + y) / (2 * SIZE - 2)
            color = lc(bg_tl, bg_br, t)
            d = dist(x + 0.5, y + 0.5, CX, CY)

            for ring_r, ring_w, ring_alpha in (needles_def.get('rings') or []):
                rt = max(0.0, 1.0 - abs(d - ring_r) / ring_w)
                if rt > 0:
                    color = lc(color, ring_color, ring_alpha * rt)

            for i, (tip, left, right) in enumerate(needles_def['tris']):
                if in_tri(x, y, tip, left, right):
                    color = needle_colors[i]

            if d <= 12.0:
                a = min(1.0, 13.0 - d)
                color = lc(color, center_fill, a)
            if d <= 5.5:
                a = min(1.0, 6.5 - d)
                color = lc(color, center_dot, a)

            row.append(color)
        rows.append(row)
    write_png(rows, path)

# ══════════════════════════════════════════
# OPTION A — current dark navy (refined)
# ══════════════════════════════════════════
print('Option A: Dark Navy (current style)')
tris_8 = {
    'rings': [(70, 1.2, 0.28), (57, 0.9, 0.13)],
    'tris':  [needle(a, tr, br, hw) for a, tr, br, hw in [
        (  0, 66, 13, 9.5),  # N
        (180, 66, 13, 9.5),  # S
        ( 90, 66, 13, 9.5),  # E
        (270, 66, 13, 9.5),  # W
        ( 45, 42, 11, 5.5),  # NE
        (135, 42, 11, 5.5),  # SE
        (225, 42, 11, 5.5),  # SW
        (315, 42, 11, 5.5),  # NW
    ]]
}
NORTH  = (224, 122,  95)
SOUTH  = lc(NORTH, (255,255,255), 0.40)
EW     = (230, 238, 250)
DIAG   = (140, 165, 202)
render(
    bg_tl=(52, 78, 120), bg_br=(22, 42, 72),
    needles_def=tris_8,
    needle_colors=[NORTH, SOUTH, EW, EW, DIAG, DIAG, DIAG, DIAG],
    ring_color=(255,255,255), center_fill=(255,255,255), center_dot=(36,58,94),
    path=f'{OUT}/icon_a.png'
)

# ══════════════════════════════════════════
# OPTION B — Warm Terracotta / earthy
# ══════════════════════════════════════════
print('Option B: Warm Terracotta')
tris_b = {
    'rings': [(70, 1.4, 0.20), (56, 1.0, 0.12)],
    'tris':  [needle(a, tr, br, hw) for a, tr, br, hw in [
        (  0, 68, 13, 10.0),   # N — cream white tip
        (180, 68, 13, 10.0),   # S
        ( 90, 68, 13, 10.0),   # E
        (270, 68, 13, 10.0),   # W
        ( 45, 44, 11,  5.5),   # NE
        (135, 44, 11,  5.5),
        (225, 44, 11,  5.5),
        (315, 44, 11,  5.5),
    ]]
}
CREAM  = (245, 238, 225)
CREAM2 = lc(CREAM, (190,150,110), 0.35)
DDIAG  = (200, 175, 148)
render(
    bg_tl=(176, 82, 54), bg_br=(110, 45, 28),
    needles_def=tris_b,
    needle_colors=[CREAM, CREAM2, CREAM, CREAM, DDIAG, DDIAG, DDIAG, DDIAG],
    ring_color=(245,238,225), center_fill=(245,238,225), center_dot=(110,45,28),
    path=f'{OUT}/icon_b.png'
)

# ══════════════════════════════════════════
# OPTION C — Deep teal + gold needle (elegant, minimal)
# Single large N/S diamond + 4 small diagonals
# ══════════════════════════════════════════
print('Option C: Deep Teal + Gold')
tris_c = {
    'rings': [(68, 1.5, 0.22), (52, 1.0, 0.14)],
    'tris':  [needle(a, tr, br, hw) for a, tr, br, hw in [
        (  0, 70, 14, 11.0),   # N — gold
        (180, 70, 14, 11.0),   # S — muted gold
        ( 90, 52, 12,  7.0),   # E — silver
        (270, 52, 12,  7.0),   # W
        ( 45, 40, 10,  5.0),
        (135, 40, 10,  5.0),
        (225, 40, 10,  5.0),
        (315, 40, 10,  5.0),
    ]]
}
GOLD   = (244, 180,  72)
GOLD2  = lc(GOLD, (255,255,255), 0.45)
SILVER = (200, 215, 230)
DDIAG2 = (120, 155, 170)
render(
    bg_tl=(24, 82, 96), bg_br=(10, 45, 58),
    needles_def=tris_c,
    needle_colors=[GOLD, GOLD2, SILVER, SILVER, DDIAG2, DDIAG2, DDIAG2, DDIAG2],
    ring_color=(200,215,230), center_fill=(255,255,255), center_dot=(10,45,58),
    path=f'{OUT}/icon_c.png'
)

# ══════════════════════════════════════════
# OPTION D — Deep forest green + soft white (calm, grounded)
# ══════════════════════════════════════════
print('Option D: Forest Green')
tris_d = {
    'rings': [(70, 1.3, 0.25), (55, 0.9, 0.13)],
    'tris':  [needle(a, tr, br, hw) for a, tr, br, hw in [
        (  0, 67, 13,  9.5),  # N — warm white
        (180, 67, 13,  9.5),  # S — muted
        ( 90, 67, 13,  9.5),  # E
        (270, 67, 13,  9.5),  # W
        ( 45, 43, 11,  5.5),
        (135, 43, 11,  5.5),
        (225, 43, 11,  5.5),
        (315, 43, 11,  5.5),
    ]]
}
WWHITE  = (235, 245, 232)
WWHITE2 = lc(WWHITE, (120,180,120), 0.45)
WDIAG   = (140, 185, 150)
render(
    bg_tl=(28, 78, 50), bg_br=(12, 42, 26),
    needles_def=tris_d,
    needle_colors=[WWHITE, WWHITE2, WWHITE, WWHITE, WDIAG, WDIAG, WDIAG, WDIAG],
    ring_color=(200,230,210), center_fill=(235,245,232), center_dot=(12,42,26),
    path=f'{OUT}/icon_d.png'
)

print('\nDone — 4 icons generated.')
