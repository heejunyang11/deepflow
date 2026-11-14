# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / サムネイル（thumbnail.png）を作る。

#1〜#5 と同じ作りにして、連載として見た目をそろえる。

描くもの: 粘土のシートのひとかけら。
  上段と下段がケイ素の四面体（三角形の枠の中の砂色の玉）、
  中段がアルミの板（銀灰色の玉）。下段の1か所だけ、ケイ素の席に
  アルミが座り、そこにマイナスの札が付いて、カルシウムが寄ってくる。
  記事のいちばん独自な節（粘土がなぜ肥料を抱えるのか）を 1 枚で出す。

1円玉は描かない。通貨の図柄を模すことになるため。

配色は emol の元素色（Si #8A6B36、Al #5B6F80）。
カルシウムは記事の図5と同じ橙。

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
ACCENT = (91, 111, 128)          # アルミの色
GRID = (122, 96, 52)
CA = '#C9822A'
NEG = (176, 42, 55)

XS = [130, 230, 330, 430, 530]   # 四面体の並び（SS 倍前）
Y_TOP, Y_AL, Y_BOT = 190, 292, 394
SUB = 2                          # 下段で置換する席

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


def tri(d, x, yb, down):
    """四面体の断面を三角形の枠で。"""
    if down:
        pts = [(x - 40, yb - 26), (x + 40, yb - 26), (x, yb + 38)]
    else:
        pts = [(x - 40, yb + 26), (x + 40, yb + 26), (x, yb - 38)]
    d.polygon([(px * SS, py * SS) for px, py in pts],
              fill=(138, 107, 54, 26), outline=(138, 107, 54, 150), width=2 * SS)


def sheet(im):
    over = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    # アルミの板
    d.rounded_rectangle([(XS[0] - 40) * SS, (Y_AL - 22) * SS,
                         (XS[-1] + 40) * SS, (Y_AL + 22) * SS],
                        radius=10 * SS, fill=(91, 111, 128, 28),
                        outline=(91, 111, 128, 90), width=2 * SS)
    for x in XS:
        tri(d, x, Y_TOP, True)
        tri(d, x, Y_BOT, False)
    im.alpha_composite(over)

    r_si = emol.RAD['Si'] * 24.0
    r_al = emol.RAD['Al'] * 24.0
    for x in XS:
        put(im, x, Y_TOP - 6, r_si, emol.COLOR['Si'])
    for i in range(len(XS) - 1):
        put(im, (XS[i] + XS[i + 1]) / 2.0, Y_AL, r_al, emol.COLOR['Al'])
    for i, x in enumerate(XS):
        if i == SUB:
            # 置換した席：光の輪
            ring = Image.new('RGBA', im.size, (0, 0, 0, 0))
            rd = ImageDraw.Draw(ring)
            for k, a in enumerate((70, 45, 24)):
                rr = (r_al + 8 + k * 7) * SS
                rd.ellipse([x * SS - rr, (Y_BOT + 6) * SS - rr,
                            x * SS + rr, (Y_BOT + 6) * SS + rr],
                           outline=(190, 100, 10, a), width=3 * SS)
            im.alpha_composite(ring)
            put(im, x, Y_BOT + 6, r_al, emol.COLOR['Al'])
        else:
            put(im, x, Y_BOT + 6, r_si, emol.COLOR['Si'])

    d2 = ImageDraw.Draw(im)
    # マイナスの札
    bx, by, br = XS[SUB] + 54, Y_BOT - 40, 17
    d2.ellipse([(bx - br) * SS, (by - br) * SS, (bx + br) * SS, (by + br) * SS],
               fill=NEG + (255,))
    d2.line([(bx - 8) * SS, by * SS, (bx + 8) * SS, by * SS], fill=(255, 255, 255, 255),
            width=4 * SS)
    # 寄ってくるカルシウム
    cx, cy = XS[SUB], Y_BOT + 96
    for k in range(3):
        yy = cy - 46 - k * 11
        d2.line([(cx - 5) * SS, yy * SS, (cx + 5) * SS, yy * SS],
                fill=(201, 130, 42, 170 - k * 45), width=3 * SS)
    put(im, cx, cy, 30, CA)
    f = font(22 * SS)
    d2.text((cx * SS, cy * SS), 'Ca²⁺', font=f, fill=(255, 255, 255, 255), anchor='mm')


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

    sheet(im)

    d = ImageDraw.Draw(im)
    tx = 650 * SS
    d.text((tx, 138 * SS), '元素の話 #6', font=font(30 * SS), fill=ACCENT + (255,))
    d.text((tx, 184 * SS), 'アルミニウム', font=font(84 * SS), fill=INK + (255,))
    d.text((tx, 290 * SS), 'Al', font=font(46 * SS), fill=ACCENT + (255,))
    d.text((tx, 368 * SS), '1円玉は、むかし', font=font(40 * SS), fill=DIM + (255,))
    d.text((tx, 422 * SS), '金より高い金属でした', font=font(40 * SS), fill=DIM + (255,))
    d.line([(tx, 496 * SS), (tx + 90 * SS, 496 * SS)], fill=ACCENT + (255,), width=4 * SS)
    d.text((tx, 518 * SS), 'DeepFlows', font=font(26 * SS), fill=FAINT + (255,))

    out = im.convert('RGB').resize((W, H), Image.LANCZOS)
    out.save('thumbnail.png', optimize=True)
    print('saved thumbnail.png  %d x %d  %.0f KB'
          % (W, H, os.path.getsize('thumbnail.png') / 1024.0))


if __name__ == '__main__':
    build()
