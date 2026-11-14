# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / サムネイル（thumbnail.png）を作る。

#1〜#6 と同じ作りにして、連載として見た目をそろえる。

描くもの: 水分子6個に囲まれたナトリウムイオン（記事の図3と同じ主題）。
  水は酸素の側を内側に向ける。下に波の線を3本引いて、海を添える。
  記事の芯「ナトリウムは、いつも溶けている」を 1 枚で出す。

配色は emol の元素色（Na #7B4FA0、O #B8401B、H #E6DCC8）。

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
ACCENT = (123, 79, 160)          # ナトリウムの色
GRID = (122, 96, 52)
SEA = (95, 150, 196)

CX, CY = 320, 290                # イオンの中心（SS 倍前）
R_O = 150                        # 中心から酸素までの距離（px）

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
    """左上から光が当たった玉（#5 と同じ描き方）。"""
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


def put(im, x, y, r, color):
    s = sphere(r * SS, color)
    im.alpha_composite(s, (int(x * SS - r * SS), int(y * SS - r * SS)))


def hydration(im):
    """水6個を六角形に。酸素が内側、水素2個が外側に開く。"""
    d = ImageDraw.Draw(im)
    half = math.radians(104.48 / 2.0)
    oh = 58                                      # O–H の見かけの長さ（px）
    r_o = emol.RAD['O'] * 52.0
    r_h = emol.RAD['H'] * 52.0
    waters = []
    for k in range(6):
        a = math.radians(90 + 60 * k + 15)
        ox, oy = CX + R_O * math.cos(a), CY + R_O * math.sin(a)
        hs = [(ox + oh * math.cos(a + s * half), oy + oh * math.sin(a + s * half))
              for s in (-1, 1)]
        waters.append(((ox, oy), hs))
    # 引き合いの点線（共有結合ではないので棒にしない）
    for (ox, oy), _hs in waters:
        n = 9
        for i in range(1, n):
            t = i / float(n)
            x = CX + (ox - CX) * t
            y = CY + (oy - CY) * t
            if 0.38 < t < 0.78:
                d.ellipse([(x - 2.2) * SS, (y - 2.2) * SS, (x + 2.2) * SS, (y + 2.2) * SS],
                          fill=ACCENT + (120,))
    # 棒（O–H）
    for (ox, oy), hs in waters:
        for hx, hy in hs:
            d.line([ox * SS, oy * SS, hx * SS, hy * SS], fill=(198, 186, 163, 255),
                   width=int(11 * SS))
    for (ox, oy), hs in waters:
        for hx, hy in hs:
            put(im, hx, hy, r_h, emol.COLOR['H'])
        put(im, ox, oy, r_o, emol.COLOR['O'])
    # 中心のイオン
    put(im, CX, CY, emol.RAD['Na'] * 64.0, emol.COLOR['Na'])
    d = ImageDraw.Draw(im)
    d.text((CX * SS, CY * SS), 'Na⁺', font=font(40 * SS), fill=(255, 255, 255, 255),
           anchor='mm')
    # 海の波
    for j in range(3):
        y0 = 520 + j * 22
        pts = []
        for i in range(0, 121):
            x = 60 + i * 4.6
            pts.append((x * SS, (y0 + 7 * math.sin(i / 7.0 + j)) * SS))
        d.line(pts, fill=SEA + (150 - j * 40,), width=4 * SS, joint='curve')


def build():
    im = Image.new('RGBA', (W * SS, H * SS), BG1 + (255,))
    d = ImageDraw.Draw(im)
    for y in range(H * SS):
        d.line([(0, y), (W * SS, y)], fill=lerp(BG1, BG2, y / float(H * SS)) + (255,))

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
    im.alpha_composite(Image.composite(grid, Image.new('RGBA', grid.size, (0, 0, 0, 0)), mask))

    hydration(im)

    d = ImageDraw.Draw(im)
    tx = 650 * SS
    d.text((tx, 138 * SS), '元素の話 #7', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 184 * SS), 'ナトリウム', font=font(84 * SS), fill=INK + (255,))
    d.text((tx, 290 * SS), 'Na', font=font(46 * SS), fill=ACCENT + (255,))
    d.text((tx, 368 * SS), '海は、なぜ', font=font(40 * SS), fill=DIM + (255,))
    d.text((tx, 422 * SS), 'しょっぱいのか', font=font(40 * SS), fill=DIM + (255,))
    d.line([(tx, 496 * SS), (tx + 90 * SS, 496 * SS)], fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 518 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    build()
