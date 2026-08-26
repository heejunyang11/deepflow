# -*- coding: utf-8 -*-
"""
元素 #1 水素 / サムネイル（thumbnail.png）を作る。

旧 thumbnail.jpg は「宇宙の始まりを味わう」という文字が画像に焼き込まれていて、
記事の方針転換（今日その場で観測できるものだけで書く）と合わなくなったため
作り直したもの。#2・#3 と同じ作りにして、連載として見た目をそろえる。

描くもの: 水素結合でつながった水の二量体。
  記事の主役は水素原子ではなく「水素結合」なので、
  H2 ではなく、O-H...O を描くのが内容に合う。

実測値:
  O-H 結合長      0.9572 A     H-O-H 結合角 104.51 度  （NIST CCCBDB）
  水素結合 O...H  約 1.8 A     O...O は約 2.8 A       （水の代表値）

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
ACCENT = (190, 100, 10)          # --hb 水素結合の色
GRID = (122, 96, 52)

R_OH = 0.9572                    # A
A_HOH = 104.51                   # 度
R_HB = 1.80                      # O...H（水素結合）A

SCALE = 116.0                    # px / A（SS 倍前）
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


def dotted(d, x1, y1, x2, y2, wd, col, dash, gap):
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


def water(ox, oy, oz, flip):
    """水 1 分子ぶんの原子座標。O を頂点に、H を 2 本、104.51 度に開く。

    flip=+1 は右へ、-1 は左へ H を向ける。二量体では
    片方の H が相手の O を向くように、この向きで置き分ける。
    """
    h = math.radians(A_HOH / 2.0)
    out = [('O', (ox, oy, oz))]
    for s in (-1, 1):
        dx = R_OH * math.sin(h) * s * flip
        dy = R_OH * math.cos(h) * flip
        out.append(('H', (ox + dx, oy + dy, oz)))
    return out


def molecule(im, d):
    """水素結合でつながった水 2 分子。左の分子の H が、右の分子の O を向く。"""
    # 左の分子は H を上へ、右の分子は H を下へ向けて、間を水素結合でつなぐ
    gap = R_OH * math.cos(math.radians(A_HOH / 2.0)) + R_HB
    left = water(-0.95, -gap / 2.0, 0.0, +1)
    right = water(+0.95, +gap / 2.0, 0.0, -1)

    # 水素結合を先に敷く（玉より奥に見えるように）
    ha = left[2][1]                 # 左分子の、右上を向いた H
    ob = right[0][1]                # 右分子の O
    x1, y1, _ = spun(ha)
    x2, y2, _ = spun(ob)
    dotted(d, CX + x1, CY + y1, CX + x2, CY + y2,
           7 * SS / 3.0 * 1.7, ACCENT, 15 * SS / 3.0, 12 * SS / 3.0)

    items = []
    for mol in (left, right):
        o = mol[0][1]
        for el, p in mol:
            x, y, z = spun(p)
            r = emol.RAD[el] * 0.74 * SCALE * (1.0 + 0.11 * z)
            items.append((z, x, y, r, el, o, p))
    items.sort(key=lambda t: t[0])

    # 共有結合の棒
    for mol in (left, right):
        ox, oy, oz = spun(mol[0][1])
        for el, p in mol[1:]:
            hx, hy, _ = spun(p)
            stick(im, CX + ox, CY + oy, CX + hx, CY + hy, 21 * SS / 3.0 * 1.55)

    for z, x, y, r, el, _, _ in items:
        im.alpha_composite(sphere(r, emol.COLOR[el]), (int(CX + x - r),
                                                       int(CY + y - r)))


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

    globals()['CX'], globals()['CY'] = 318 * SS, 316 * SS
    globals()['SCALE'] = 116.0 * SS
    molecule(im, d)

    tx = 640 * SS
    d.text((tx, 148 * SS), '元素の話 #1', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 198 * SS), '水素', font=font(112 * SS), fill=INK + (255,))
    d.text((tx + 268 * SS, 256 * SS), 'H', font=font(56 * SS), fill=ACCENT + (255,))
    d.text((tx, 348 * SS), '朝の寝癖は、', font=font(40 * SS), fill=DIM + (255,))
    d.text((tx, 402 * SS), 'なぜ水で直るのか', font=font(40 * SS), fill=DIM + (255,))
    d.line([(tx, 476 * SS), (tx + 90 * SS, 476 * SS)],
           fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 498 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    print('O-H %.4f A / H-O-H %.2f deg / O...H %.2f A' % (R_OH, A_HOH, R_HB))
    build()
