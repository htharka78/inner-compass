#!/usr/bin/env python3
"""Combine 4 icons into a 2×2 comparison grid with labels."""
import struct, zlib, os

DIR = os.path.dirname(os.path.abspath(__file__))
ICON_SIZE = 180
PAD = 20
LABEL_H = 28
CELL_W = ICON_SIZE + PAD * 2
CELL_H = ICON_SIZE + PAD * 2 + LABEL_H
GRID_W = CELL_W * 2
GRID_H = CELL_H * 2
BG = (245, 242, 238)

# ── Read PNG pixels ──────────────────────────────────
def read_png(path):
    import zlib as z
    with open(path, 'rb') as f:
        data = f.read()
    # find IDAT chunks
    pos = 8
    chunks = {}
    idat = b''
    width = height = 0
    while pos < len(data):
        length = int.from_bytes(data[pos:pos+4], 'big')
        tag = data[pos+4:pos+8]
        body = data[pos+8:pos+8+length]
        if tag == b'IHDR':
            width  = int.from_bytes(body[0:4], 'big')
            height = int.from_bytes(body[4:8], 'big')
        elif tag == b'IDAT':
            idat += body
        pos += 12 + length
    raw = z.decompress(idat)
    rows = []
    stride = 1 + width * 3
    for y in range(height):
        row = []
        base = y * stride + 1
        for x in range(width):
            o = base + x * 3
            row.append((raw[o], raw[o+1], raw[o+2]))
        rows.append(row)
    return rows

# ── 4×4 anti-aliased digit bitmaps (0-9, A-Z subset) ──
# Each char: 5 rows × 4 cols of bits (top row first)
FONT = {
    'A': [0b0110,0b1001,0b1111,0b1001,0b1001],
    'B': [0b1110,0b1001,0b1110,0b1001,0b1110],
    'C': [0b0111,0b1000,0b1000,0b1000,0b0111],
    'D': [0b1110,0b1001,0b1001,0b1001,0b1110],
    ' ': [0b0000]*5,
    '-': [0b0000,0b0000,0b1111,0b0000,0b0000],
}

def draw_char(pixels, cx, cy, ch, color, scale=3):
    bits = FONT.get(ch.upper())
    if not bits:
        return
    for row_i, row_bits in enumerate(bits):
        for col_i in range(4):
            if row_bits & (1 << (3 - col_i)):
                for dy in range(scale):
                    for dx in range(scale):
                        px = cx + col_i * scale + dx
                        py = cy + row_i * scale + dy
                        if 0 <= py < GRID_H and 0 <= px < GRID_W:
                            pixels[py][px] = color

def draw_text(pixels, x, y, text, color, scale=3):
    for i, ch in enumerate(text):
        draw_char(pixels, x + i * (4 * scale + scale), y, ch, color, scale)

# ── Build grid ──────────────────────────────────────
icons = ['icon_a.png', 'icon_b.png', 'icon_c.png', 'icon_d.png']
labels = ['A  Dark Navy', 'B  Terracotta', 'C  Teal   Gold', 'D  Forest Green']
label_short = ['A', 'B', 'C', 'D']

icon_pixels = [read_png(os.path.join(DIR, p)) for p in icons]

# init grid with background
pixels = [[BG] * GRID_W for _ in range(GRID_H)]

for idx, (icon, label) in enumerate(zip(icon_pixels, label_short)):
    col = idx % 2
    row = idx // 2
    ox = col * CELL_W + PAD
    oy = row * CELL_H + PAD

    # blit icon
    for y in range(ICON_SIZE):
        for x in range(ICON_SIZE):
            pixels[oy + y][ox + x] = icon[y][x]

    # label below icon — center it
    label_text = ['A', 'B', 'C', 'D'][idx]
    lx = ox + ICON_SIZE // 2 - 6
    ly = oy + ICON_SIZE + 8
    draw_text(pixels, lx, ly, label_text, (60, 60, 60), scale=3)

# ── Write PNG ──────────────────────────────────────
raw = b''
for row in pixels:
    raw += b'\x00'
    for r, g, b in row:
        raw += bytes([r, g, b])

def chunk(tag, body):
    p = tag + body
    return struct.pack('>I', len(body)) + p + struct.pack('>I', zlib.crc32(p) & 0xFFFFFFFF)

out = (b'\x89PNG\r\n\x1a\n'
       + chunk(b'IHDR', struct.pack('>II', GRID_W, GRID_H) + bytes([8, 2, 0, 0, 0]))
       + chunk(b'IDAT', zlib.compress(raw, 6))
       + chunk(b'IEND', b''))

path = os.path.join(DIR, 'icon_compare.png')
with open(path, 'wb') as f:
    f.write(out)
print(f'Written {path}  ({GRID_W}×{GRID_H},  {len(out):,} bytes)')
