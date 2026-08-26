# -*- coding: utf-8 -*-
"""
元素 #2 炭素 / サムネイル（thumbnail.png）を作る。

Field Notes の一覧に並ぶカード用。1200x630。
図と同じ紙のパレット・同じ玉の描き方でそろえ、
座標も図と同じ実測値（ダイヤモンドの C-C 1.5445 A、正四面体）から出す。

SVG の放射グラデーションは PIL に無いので、球は 1 画素ずつ塗って作る。
3 倍の大きさで描いてから縮めることで、輪郭のがたつきを消している。

出力: thumbnail.png
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

import emol

W, H = 1200, 630
SS = 3                       # 3 倍で描いてから縮める
BG1, BG2 = (255, 253, 249), (250, 246, 238)
INK, DIM, FAINT = (43, 38, 33), (95, 85, 70), (122, 110, 92)
ACCENT = (190, 100, 10)
GRID = (122, 96, 52)

A_DIA = 3.567
D_DIA = A_DIA * math.sqrt(3) / 4.0      # 1.5445 Å
SCALE = 118.0                            # px / Å（3 倍前の値）
# 向きは候補を並べて描き、目で選んだ。
# 平面上での離れ具合を数値で最大化すると SPIN60/TILT-35 が選ばれるが、
# それは正四面体が「平面の十字」に見える向きで、炭素の話としては最悪である。
# 4 個が判別でき、かつ立体に見えるのはこの向き。
TILT, SPIN = -18.0, 45.0
CX, CY = 330, 330                        # 分子の中心

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
    """左上から光が当たった玉。図の放射グラデーションと同じ配色で塗る。"""
    stops = [(0.00, rgb(emol.lighten(base, .60))),
             (0.32, rgb(emol.lighten(base, .21))),
             (0.72, rgb(base)),
             (1.00, rgb(emol.darken(base, .46)))]
    d = int(r * 2)
    im = Image.new('RGBA', (d, d), (0, 0, 0, 0))
    px = im.load()
    hx, hy = d * 0.34, d * 0.26          # 光の中心（左上寄り）
    rad = d * 0.76                        # グラデーションの広がり
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
    # 艶。楕円を重ねると白い塊になるので、画素ごとになめらかに落とす。
    # 図の SVG では白→透明の放射グラデーションを使っている。それに合わせる。
    ex, ey = r * .34, r * .24
    cxh, cyh = r - r * .33, r - r * .38
    for y in range(d):
        for x in range(d):
            if px[x, y][3] == 0:
                continue
            u = math.hypot((x - cxh) / ex, (y - cyh) / ey)
            if u >= 1.0:
                continue
            a = (1.0 - u) ** 2.0                 # 中心ほど白く、縁で消える
            c = px[x, y]
            px[x, y] = lerp(c[:3], (255, 255, 255), a * .85) + (255,)
    return im


def stick(im, x1, y1, x2, y2, wd):
    """円柱に見える棒。断面方向に明暗を付けた帯を回して貼る。"""
    L = int(round(math.hypot(x2 - x1, y2 - y1)))
    if L < 2:
        return
    band = Image.new('RGBA', (L, int(wd)), (0, 0, 0, 0))
    p = band.load()
    stops = [(0.00, (139, 127, 107)), (0.16, (198, 186, 163)),
             (0.38, (228, 219, 201)), (0.62, (194, 180, 155)),
             (1.00, (126, 114, 89))]
    for y in range(int(wd)):
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


def spun(p):
    ay, ax = math.radians(SPIN), math.radians(TILT)
    x, y, z = p
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    return x * SCALE, -y * SCALE, z


def molecule(im):
    """ダイヤモンドの骨組みの芯。中心の炭素と、それを囲む炭素4個。"""
    pts = [((0.0, 0.0, 0.0), False)]
    pts += [(tuple(c * D_DIA for c in v), True) for v in emol.tetra()]
    rc = emol.RAD['C'] * 0.72

    items = []
    for p, outer in pts:
        x, y, z = spun(p)
        r = rc * SCALE * (1.0 + 0.11 * z)
        items.append((z, x, y, r, outer, p))
    items.sort(key=lambda t: t[0])

    for z, x, y, r, outer, p in items:
        if outer:
            u = [c / D_DIA for c in p]
            sx, sy, _ = spun([c * rc for c in u])
            stick(im, CX + sx, CY + sy, CX + x, CY + y, 20 * SS / 3.0 * 1.6)
        s = sphere(r, emol.COLOR['C'])
        im.alpha_composite(s, (int(CX + x - r), int(CY + y - r)))


def build():
    im = Image.new('RGBA', (W * SS, H * SS), BG1 + (255,))
    d = ImageDraw.Draw(im)
    # 地の淡いグラデーション
    for y in range(H * SS):
        d.line([(0, y), (W * SS, y)],
               fill=lerp(BG1, BG2, y / float(H * SS)) + (255,))
    # 方眼紙の罫
    step = 40 * SS
    grid = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W * SS, step):
        gd.line([(x, 0), (x, H * SS)], fill=GRID + (255,), width=SS)
    for y in range(0, H * SS, step):
        gd.line([(0, y), (0 + W * SS, y)], fill=GRID + (255,), width=SS)
    # 左上を濃く、右下へ消えていくように覆いを掛ける（図のカードと同じ考え方）
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
    grid.putalpha(Image.composite(grid.getchannel('A'), mask,
                                  grid.getchannel('A').point(lambda v: 0)))
    grid.putalpha(Image.eval(grid.getchannel('A'), lambda v: v))
    im.alpha_composite(Image.composite(grid, Image.new('RGBA', grid.size,
                                                       (0, 0, 0, 0)), mask))

    globals()['CX'], globals()['CY'] = 335 * SS, 330 * SS
    globals()['SCALE'] = 118.0 * SS
    molecule(im)

    # 文字
    tx = 640 * SS
    d.text((tx, 150 * SS), '元素の話 #2', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 200 * SS), '炭素', font=font(112 * SS), fill=INK + (255,))
    d.text((tx + 268 * SS, 258 * SS), 'C', font=font(56 * SS), fill=ACCENT + (255,))
    d.text((tx, 350 * SS), 'ダイヤモンドと鉛筆の芯は、',
           font=font(40 * SS), fill=DIM + (255,))
    d.text((tx, 404 * SS), 'まったく同じものです',
           font=font(40 * SS), fill=DIM + (255,))
    d.line([(tx, 478 * SS), (tx + 90 * SS, 478 * SS)],
           fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 500 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    print('ダイヤモンドの C–C = %.4f Å（a=%.3f の面心立方から）' % (D_DIA, A_DIA))
    build()
