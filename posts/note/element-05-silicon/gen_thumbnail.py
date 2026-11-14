# -*- coding: utf-8 -*-
"""
元素 #5 ケイ素 / サムネイル（thumbnail.png）を作る。

#1〜#4 と同じ作りにして、連載として見た目をそろえる。

描くもの: SiO2 の網のひとかけら。
  ケイ素（大きい玉）と酸素（小さい玉）が交互に並んだ環に、
  外へ伸びる手を付ける。「この網には終わりがない」という
  記事の主題を、1 枚で出す。

配色は emol の元素色をそのまま使う（第2回の図と同じ）。
  Si  #8A6B36 / 半径 1.11 A
  O   #B8401B / 半径 0.66 A

出力: thumbnail.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

import emol

W, H = 1200, 630
SS = 3
BG1, BG2 = (255, 253, 249), (250, 246, 238)
INK, DIM, FAINT = (43, 38, 33), (95, 85, 70), (122, 110, 92)
ACCENT = (138, 107, 54)          # ケイ素の色
GRID = (122, 96, 52)

CX, CY = 322, 316                # 網の中心（SS 倍前）
RING = 118.0                     # 環の半径 px
STUB = 62.0                      # 外へ伸びる手の長さ px

FONTS = ['C:/Windows/Fonts/meiryob.ttc', 'C:/Windows/Fonts/YuGothB.ttc',
         'C:/Windows/Fonts/BIZ-UDGothicB.ttc', 'C:/Windows/Fonts/msgothic.ttc']


def font(size):
    for p in FONTS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


def rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def sphere(r, base):
    """左上から光が当たった玉。図の放射グラデーションと同じ配色。"""
    stops = [(0.00, rgb(emol.lighten(base, .60))),
             (0.32, rgb(emol.lighten(base, .21))),
             (0.72, rgb(base)),
             (1.00, rgb(emol.darken(base, .46)))]
    d = max(2, int(r * 2))
    im = Image.new('RGBA', (d, d), (0, 0, 0, 0))
    px = im.load()
    hx, hy = d * 0.34, d * 0.26
    rad = d * 0.76
    for y in range(d):
        for x in range(d):
            dx, dy = x - r + .5, y - r + .5
            if dx * dx + dy * dy > r * r:
                continue
            t = min(1.0, math.hypot(x - hx, y - hy) / rad)
            for i in range(len(stops) - 1):
                a, b = stops[i], stops[i + 1]
                if t <= b[0] or i == len(stops) - 2:
                    u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0.0
                    px[x, y] = lerp(a[1], b[1], max(0.0, min(1.0, u))) + (255,)
                    break
    ex, ey = r * .34, r * .24
    cxh, cyh = r - r * .33, r - r * .38
    for y in range(d):
        for x in range(d):
            if px[x, y][3] == 0:
                continue
            u = math.hypot((x - cxh) / ex, (y - cyh) / ey)
            if u >= 1.0:
                continue
            c = px[x, y]
            px[x, y] = lerp(c[:3], (255, 255, 255), (1.0 - u) ** 2.0 * .85) + (255,)
    return im


def stick(im, x1, y1, x2, y2, wd, fade=1.0):
    """円柱に見える棒。断面方向に明暗を付けた帯を回して貼る。"""
    L = int(round(math.hypot(x2 - x1, y2 - y1)))
    if L < 2:
        return
    wd = max(2, int(wd))
    band = Image.new('RGBA', (L, wd), (0, 0, 0, 0))
    p = band.load()
    stops = [(0.00, (139, 127, 107)), (0.16, (198, 186, 163)),
             (0.38, (228, 219, 201)), (0.62, (194, 180, 155)),
             (1.00, (126, 114, 89))]
    for y in range(wd):
        t = y / max(1.0, wd - 1)
        for i in range(len(stops) - 1):
            a, b = stops[i], stops[i + 1]
            if t <= b[0] or i == len(stops) - 2:
                u = (t - a[0]) / (b[0] - a[0]) if b[0] > a[0] else 0.0
                c = lerp(a[1], b[1], max(0.0, min(1.0, u))) + (int(255 * fade),)
                break
        for x in range(L):
            p[x, y] = c
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    rot = band.rotate(-ang, expand=True, resample=Image.BICUBIC)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    im.alpha_composite(rot, (int(mx - rot.width / 2), int(my - rot.height / 2)))


def network(im):
    """SiO2 の環をひとつ描き、外へ手を伸ばして「続き」を示す。

    環は 12 個の席からなり、ケイ素と酸素が交互に座る。
    実際の SiO2 も Si-O-Si-O と交互に繋がるので、この並びは正しい。
    """
    n = 12
    pos = []
    for k in range(n):
        a = math.radians(90 + k * 360.0 / n)
        pos.append((CX + RING * math.cos(a), CY - RING * math.sin(a)))

    # 環の棒
    for k in range(n):
        x1, y1 = pos[k]
        x2, y2 = pos[(k + 1) % n]
        stick(im, x1 * SS, y1 * SS, x2 * SS, y2 * SS, 13 * SS)

    # 外へ伸びる手（ケイ素の席からだけ）。網に終わりがないことを示す
    stubs = []
    for k in range(0, n, 2):
        a = math.radians(90 + k * 360.0 / n)
        x1, y1 = pos[k]
        x2 = x1 + STUB * math.cos(a)
        y2 = y1 - STUB * math.sin(a)
        stick(im, x1 * SS, y1 * SS, x2 * SS, y2 * SS, 11 * SS, fade=.55)
        stubs.append((x2, y2))

    # 玉。奥から手前ではなく、外側の酸素 -> 環 の順に置く
    r_o = emol.RAD['O'] * 34.0
    r_si = emol.RAD['Si'] * 34.0
    for x, y in stubs:
        s = sphere(r_o * .92 * SS, emol.COLOR['O'])
        im.alpha_composite(Image.blend(Image.new('RGBA', s.size, (0, 0, 0, 0)),
                                       s, .62),
                           (int(x * SS - s.width / 2), int(y * SS - s.height / 2)))
    for k in range(n):
        el = 'Si' if k % 2 == 0 else 'O'
        r = (r_si if el == 'Si' else r_o) * SS
        s = sphere(r, emol.COLOR[el])
        x, y = pos[k]
        im.alpha_composite(s, (int(x * SS - r), int(y * SS - r)))


def build():
    im = Image.new('RGBA', (W * SS, H * SS), BG1 + (255,))
    d = ImageDraw.Draw(im)
    for y in range(H * SS):
        d.line([(0, y), (W * SS, y)],
               fill=lerp(BG1, BG2, y / float(H * SS)) + (255,))

    step = 40 * SS
    grid = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W * SS, step):
        gd.line([(x, 0), (x, H * SS)], fill=GRID + (255,), width=SS)
    for y in range(0, H * SS, step):
        gd.line([(0, y), (W * SS, y)], fill=GRID + (255,), width=SS)
    mask = Image.new('L', (W * SS, H * SS), 0)
    mp = mask.load()
    for y in range(0, H * SS, SS):
        for x in range(0, W * SS, SS):
            t = 1.0 - min(1.0, math.hypot(x / float(W * SS) - .18,
                                          y / float(H * SS) - .0) / 1.05)
            v = int(26 * max(0.0, t) ** 1.6)
            for j in range(SS):
                for i in range(SS):
                    if x + i < W * SS and y + j < H * SS:
                        mp[x + i, y + j] = v
    im.alpha_composite(Image.composite(grid, Image.new('RGBA', grid.size,
                                                       (0, 0, 0, 0)), mask))

    network(im)

    tx = 640 * SS
    d.text((tx, 150 * SS), '元素の話 #5', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 200 * SS), 'ケイ素', font=font(112 * SS), fill=INK + (255,))
    d.text((tx + 372 * SS, 258 * SS), 'Si', font=font(56 * SS),
           fill=ACCENT + (255,))
    d.text((tx, 350 * SS), '腕時計の「QUARTZ」は', font=font(40 * SS),
           fill=DIM + (255,))
    d.text((tx, 404 * SS), 'なぜ砂と同じものなのか', font=font(40 * SS),
           fill=DIM + (255,))
    d.line([(tx, 478 * SS), (tx + 90 * SS, 478 * SS)],
           fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 500 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    print('Si %.2f A (%s) / O %.2f A (%s)'
          % (emol.RAD['Si'], emol.COLOR['Si'], emol.RAD['O'], emol.COLOR['O']))
    build()
