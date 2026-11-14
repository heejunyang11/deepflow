# -*- coding: utf-8 -*-
"""
元素 #7 ナトリウム / 図6 : 島の地下に浮かぶ真水（淡水レンズ）と塩水化。

島の断面。雨がしみこんだ真水が、重い海水の上にレンズの形で浮く。
ガイベン–ヘルツベルグの関係: 境目の深さ z = 40 h（h は地下水面の海面からの高さ）。
  40 = ρ_f / (ρ_s − ρ_f) = 1.000 / (1.025 − 1.000)
図の縦方向は、この 1 : 40 をそのまま守って描く（h を何 px にしても境目は 40 倍）。
横方向の縮尺は任意。

汲みすぎて島全体の地下水面が δ 下がると、境目は 40δ せり上がる。
井戸の真下で局所的に吸い上げられる現象（アップコーニング）は 40 倍則に従わないので、
図ではそれを描かない（2026-11-14 の第三者検証による）。
その 2 つの状態を SMIL の <animate> で行き来させる（d 属性の補間）。
動かない環境では、ふだんの状態の絵になる。

出力: _fig6_lens.qmd
"""
import math

import efig

P, CID = 'nalen', 'nalen1'

W, H = 680, 330
SEA_Y = 112                 # 海面
CX, HALF = 340, 190         # 島の中心と、レンズの半幅（px）
H_TOP = 4.0                 # 島の中心での地下水面の高さ（px）
RATIO = 1.000 / (1.025 - 1.000)     # 40
WELL_X = 300
LOWER = 0.40                # 汲みすぎたとき、地下水面の高さが何割下がるか
N = 80


def shape(x):
    u = (x - CX) / float(HALF)
    return math.sqrt(max(0.0, 1.0 - u * u))


def wt(x, k):
    """地下水面（画面の y）。k=0 ふだん、k=1 汲みすぎ（島全体で水面が下がる）。"""
    return SEA_Y - H_TOP * (1.0 - LOWER * k) * shape(x)


def itf(x, k):
    """真水と海水の境目（画面の y）。地下水面の高さの 40 倍の深さ。"""
    h = SEA_Y - wt(x, k)
    return SEA_Y + RATIO * h


def lens_path(k):
    xs = [CX - HALF + 2 * HALF * i / float(N) for i in range(N + 1)]
    top = ['%.1f %.2f' % (x, wt(x, k)) for x in xs]
    bot = ['%.1f %.2f' % (x, itf(x, k)) for x in reversed(xs)]
    return 'M' + ' L'.join(top) + ' L' + ' L'.join(bot) + ' Z'


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="島の断面図。雨がしみこんだ真水が、'
         '重い海水の上にレンズの形で浮いている。井戸で汲みすぎると、下の海水がせり上がる">'
         % (W, H)]
    # 空・海・海底
    o.append('<rect class="%s-salt" x="0" y="%d" width="%d" height="%d"/>'
             % (P, SEA_Y, W, H - SEA_Y - 24))
    o.append('<rect class="%s-bed" x="0" y="%d" width="%d" height="24"/>' % (P, H - 24, W))
    # 島（地面の上に出ている部分）
    o.append('<path class="%s-land" d="M%d %d C%d %d %d %d %d %d C%d %d %d %d %d %d Z"/>'
             % (P, CX - HALF - 30, SEA_Y, CX - 120, SEA_Y - 30, CX - 60, SEA_Y - 54,
                CX, SEA_Y - 54, CX + 60, SEA_Y - 54, CX + 120, SEA_Y - 30,
                CX + HALF + 30, SEA_Y))
    # 地下の地層（海面より下の島の部分。海水がしみこんでいる）
    o.append('<rect class="%s-aq" x="%d" y="%d" width="%d" height="%d" rx="0"/>'
             % (P, CX - HALF - 30, SEA_Y, 2 * HALF + 60, H - 24 - SEA_Y))
    # 雨
    for i in range(10):
        x = CX - 150 + i * 32
        o.append('<path class="%s-rain" style="animation-delay:%.2fs" d="M%d 8 l-4 12"/>'
                 % (P, (i * 0.29) % 1.4, x))
    # 淡水レンズ
    a, b = lens_path(0), lens_path(1)
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>淡水レンズ</b>：雨がしみこんでできた真水です。塩が溶けていないぶん海水より'
        '少し軽いので、下の海水と混ざりきらずに<b>上に浮いています</b>。'
        '島の井戸が汲んでいるのは、この水です。'))
    o.append('<path class="%s-fresh" d="%s">'
             '<animate attributeName="d" dur="9s" repeatCount="indefinite" '
             'values="%s;%s;%s;%s;%s" keyTimes="0;0.2;0.45;0.75;1"/></path>'
             % (P, a, a, a, b, b, a))
    o.append('</g>')
    o.append('<line class="%s-sl" x1="0" y1="%d" x2="%d" y2="%d"/>' % (P, SEA_Y, W, SEA_Y))
    o.append('<text class="%s-slt" x="12" y="%d">海面</text>' % (P, SEA_Y - 6))
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>海水</b>：島の地下の深いところは、まわりの海から海水がしみこんでいます。'))
    o.append('<text class="%s-st" x="%d" y="%d">海水</text>' % (P, CX + HALF - 10, H - 40))
    o.append('<text class="%s-st" x="60" y="%d">海</text>' % (P, SEA_Y + 40))
    o.append('</g>')
    o.append('<text class="%s-ft" x="%d" y="%d">真水（淡水レンズ）</text>'
             % (P, CX + 70, SEA_Y + 60))

    # 1 : 40 の物差し（島の中心で）
    x_r = CX + 12
    o.append('<g data-detail="%s">' % efig.attr(
        '<b>1 : 40</b>：地下水面が海面より<b>1メートル</b>高いと、真水と海水の境目は'
        '海面より<b>約40メートル</b>深いところにあります。図の縦方向は、この比をそのまま守って描きました。'))
    o.append('<line class="%s-dim" x1="%d" y1="%.1f" x2="%d" y2="%d"/>'
             % (P, x_r, wt(CX, 0), x_r, SEA_Y))
    o.append('<line class="%s-dim" x1="%d" y1="%d" x2="%d" y2="%.1f"/>'
             % (P, x_r, SEA_Y, x_r, itf(CX, 0)))
    o.append('<text class="%s-dt" x="%d" y="%d">水面の高さ 1</text>' % (P, x_r + 6, SEA_Y - 8))
    o.append('<text class="%s-dt" x="%d" y="%.1f">境目の深さ 40</text>'
             % (P, x_r + 6, itf(CX, 0) - 6))
    o.append('</g>')

    # 井戸
    o.append('<g class="%s-wg" data-detail="%s">' % (P, efig.attr(
        '<b>汲みすぎると</b>：島全体で地下水面が<b>1</b>下がると、真水と海水の境目は'
        '<b>約40</b>せり上がってきます（図は数秒おきに、ふだんと汲みすぎを行き来します）。'
        'そのうえ井戸の真下では、海水が局所的に吸い上げられることもあります。'
        'やがて井戸から塩水が出るようになる——<b>塩水化</b>です。')))
    o.append('<line class="%s-well" x1="%d" y1="%d" x2="%d" y2="%d"/>'
             % (P, WELL_X, SEA_Y - 44, WELL_X, SEA_Y + 70))
    o.append('<rect class="%s-pumpb" x="%d" y="%d" width="18" height="12" rx="2"/>'
             % (P, WELL_X - 9, SEA_Y - 56))
    o.append('<text class="%s-wt" x="%d" y="%d">井戸</text>' % (P, WELL_X - 14, SEA_Y - 62))
    o.append('<text class="%s-up" x="%d" y="%d">汲みすぎると、海水がせり上がる</text>'
             % (P, CX - 50, H - 40))
    o.append('<path class="%s-uparr" d="M%d %d l0 -40 m-5 8 l5 -8 l5 8"/>'
             % (P, CX - 70, H - 58))
    o.append('</g>')
    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s-wrap{margin:14px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-salt{fill:#9FC3D6;}
.%(p)s-bed{fill:#CDBF9F;}
.%(p)s-land{fill:#CDBB96;}
.%(p)s-aq{fill:#8FB2C0;opacity:.55;}
.%(p)s-fresh{fill:#E6F3F7;stroke:#5E96C4;stroke-width:1.4;}
.%(p)s-sl{stroke:#2F6D9E;stroke-width:1.2;stroke-dasharray:6 4;}
.%(p)s-slt{font-size:11.5px;font-weight:700;fill:#2F6D9E;}
.%(p)s-st{font-size:14px;font-weight:800;fill:#1F4E6E;text-anchor:middle;}
.%(p)s-ft{font-size:13px;font-weight:800;fill:#2F6D9E;}
.%(p)s-dim{stroke:var(--ink);stroke-width:1.4;}
.%(p)s-dt{font-size:11.5px;font-weight:700;fill:var(--ink);}
.%(p)s-well{stroke:var(--ink);stroke-width:3;}
.%(p)s-pumpb{fill:var(--hb);}
.%(p)s-wt{font-size:11.5px;font-weight:700;fill:var(--ink);text-anchor:end;}
.%(p)s-wg{cursor:default;}
.%(p)s-up{font-size:12px;font-weight:800;fill:#B02A37;text-anchor:end;}
.%(p)s-uparr{fill:none;stroke:#B02A37;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.%(p)s-rain{stroke:#7FA7C4;stroke-width:1.6;stroke-linecap:round;opacity:0;
  animation:%(p)s-rain 1.4s linear infinite;}
@keyframes %(p)s-rain{0%%{transform:translateY(0);opacity:0;}
  15%%{opacity:.55;}100%%{transform:translateY(34px);opacity:0;}}
@media (max-width:820px){.%(p)s-wrap{margin:10px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '島の地下では、真水が海水の上に浮いています',
             '島の断面です。雨がしみこんだ真水（白っぽい青）が、重い海水の上にレンズの形で'
             '浮いています。数秒おきに、井戸で汲みすぎたときの姿に変わります。'
             'カーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        '真水の水面が海面より<b>1</b>高いと、真水と海水の境目は海面より<b>40</b>深いところにあります。'
        '裏を返せば、汲みすぎて島の水面が<b>1</b>下がると、境目が<b>40</b>せり上がってくる。'
        '<b>水面のわずかな高さが、その40倍の深さの真水を支えています。</b>',
        '模式図です。縦方向は、地下水面の高さと境目の深さの比 1 : 40 を守って描きました'
        '（ガイベン–ヘルツベルグの関係。海水の密度 1.025、真水 1.000 として 1 ÷ 0.025 ＝ 40）。'
        '横方向の縮尺は任意です。水が動いていないとみなした近似で、実際の境目は'
        'ある幅をもって混ざり合います。40倍の関係は、島全体で水面が下がって落ち着いたときの姿で、'
        '井戸の真下で海水が局所的に吸い上げられる現象（アップコーニング）はこの比に従いません。'
        'くわしくは地下水科学入門 #7。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('比 %.1f' % RATIO)
    d0 = itf(CX, 0) - SEA_Y
    d1 = itf(CX, 1) - SEA_Y
    h0 = SEA_Y - wt(CX, 0)
    h1 = SEA_Y - wt(CX, 1)
    print('島の中心: 水面 %.2f → %.2f px（低下 %.2f）、境目 %.1f → %.1f px（上昇 %.1f）'
          % (h0, h1, h0 - h1, d0, d1, d0 - d1))
    assert abs((d0 - d1) / (h0 - h1) - RATIO) < 1e-6
    assert h1 > 0, '汲みすぎた状態で水面が海面より下がっている'
    assert itf(CX, 0) < H - 24, '境目が海底を突き抜ける'
    efig.save('_fig6_lens.qmd', build())
