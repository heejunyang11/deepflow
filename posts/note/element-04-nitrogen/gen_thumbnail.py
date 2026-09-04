# -*- coding: utf-8 -*-
"""
元素 #4 窒素 / サムネイル（thumbnail.png）を作る。

#1〜#3 と同じ作りにして、連載として見た目をそろえる。

描くもの: 窒素分子 N2 の三重結合。
  記事の主役は「941 kJ/mol の三重結合」なので、
  棒を 3 本並べて、その固さを絵で出す。

実測値:
  N-N 結合長 1.097685 A（NIST WebBook）
  結合の強さ 941 kJ/mol（78,691.09 cm-1 の実測値を換算）

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
ACCENT = (46, 110, 78)           # --n 窒素の緑
GRID = (122, 96, 52)

R_NN = 1.097685                  # N-N 結合長 A（NIST WebBook）
BOND_KJ = 941.0                  # 三重結合の強さ kJ/mol

SCALE = 205.0                    # px / A（SS 倍前）
TILT, SPIN = -14.0, 26.0
CX, CY = 322, 318

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


def stick(im, x1, y1, x2, y2, wd):
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
                c = lerp(a[1], b[1], max(0.0, min(1.0, u))) + (255,)
                break
        for x in range(L):
            p[x, y] = c
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    rot = band.rotate(-ang, expand=True, resample=Image.BICUBIC)
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    im.alpha_composite(rot, (int(mx - rot.width / 2), int(my - rot.height / 2)))


def _unused_dotted(d, x1, y1, x2, y2, wd, col, dash, gap):
    """水素結合は破線で描く。共有結合（実線の棒）と見分けられるように。"""
    L = math.hypot(x2 - x1, y2 - y1)
    if L < 1:
        return
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    t = 0.0
    while t < L:
        e = min(L, t + dash)
        d.line([(x1 + ux * t, y1 + uy * t), (x1 + ux * e, y1 + uy * e)],
               fill=col + (255,), width=int(wd))
        t = e + gap


def spun(p):
    ay, ax = math.radians(SPIN), math.radians(TILT)
    x, y, z = p
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    return x * SCALE, -y * SCALE, z


def spun3(p):
    """回転と正射影。棒を3本描くので、奥行きの順番も返す。"""
    return spun(p)


def molecule(im, d):
    """窒素分子。同じ原子2個を、3本の棒でつなぐ。

    三重結合を「3本の棒」で描くのは模式だが、
    記事が 941 という数字を「3本の手で握り合っている」と説明しているので
    絵と本文がそろう。棒は結合軸に垂直な向きへ等間隔にずらす。
    """
    h = R_NN / 2.0
    off = 0.26                      # 棒どうしの間隔（A）
    # N2 は結合が短く、共有結合半径のまま描くと棒が完全に隠れる。
    # 三重結合の3本を見せるのがこの絵の主題なので、玉は小さめの模式にする。
    rc = emol.RAD['N'] * 0.40

    items = []
    for sgn in (-1, 1):
        x, y, z = spun((sgn * h, 0.0, 0.0))
        items.append((z, x, y, rc * SCALE * (1.0 + 0.11 * z)))
    items.sort(key=lambda t: t[0])

    # 3 本の棒。中央・上・下
    for k in (-1, 0, 1):
        x1, y1, _ = spun((-h, k * off, 0.0))
        x2, y2, _ = spun((h, k * off, 0.0))
        stick(im, CX + x1, CY + y1, CX + x2, CY + y2,
              13 * SS / 3.0 * 1.5)

    for z, x, y, r in items:
        im.alpha_composite(sphere(r, emol.COLOR['N']),
                           (int(CX + x - r), int(CY + y - r)))


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

    globals()['CX'], globals()['CY'] = 316 * SS, 318 * SS
    globals()['SCALE'] = 205.0 * SS
    molecule(im, d)

    tx = 640 * SS
    d.text((tx, 148 * SS), '元素の話 #4', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 198 * SS), '窒素', font=font(112 * SS), fill=INK + (255,))
    d.text((tx + 268 * SS, 256 * SS), 'N', font=font(56 * SS), fill=ACCENT + (255,))
    d.text((tx, 348 * SS), '稲妻はなぜ', font=font(40 * SS), fill=DIM + (255,))
    d.text((tx, 402 * SS), '「稲の妻」と書くのか', font=font(40 * SS), fill=DIM + (255,))
    d.line([(tx, 476 * SS), (tx + 90 * SS, 476 * SS)],
           fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 498 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    print('N-N %.6f A / 三重結合 %.0f kJ/mol' % (R_NN, BOND_KJ))
    build()
