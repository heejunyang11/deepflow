# -*- coding: utf-8 -*-
"""
元素 #6 アルミニウム / 図1 : ありふれているのに、いちばん最後に取り出された。

金属ごとに「酸素を引き剥がすのに、少なくとも要るエネルギー」を横棒で並べ、
横に「人が金属として手にした時代」を添える。

  酸素と固く組むほど、取り出しにくい。取り出しにくいほど、人が手にしたのは遅い。
  アルミは、並べた中でいちばん固く、いちばん遅い。

数値は 25 ℃ の標準生成ギブズエネルギー ΔfG° を、酸化物に含まれる
酸素原子の数で割ったもの（kJ／酸素 1 mol）。符号を反転して「要るエネルギー」にする。

  Cu2O  −146.0 kJ/mol  → 酸素 1 個あたり 146.0
  Fe2O3 −742.2         → 3 で割って 247.4
  ZnO   −320.5         → 320.5
  SiO2  −856.3 （石英）→ 2 で割って 428.2
  Al2O3 −1582.3（コランダム）→ 3 で割って 527.4

金の酸化物は文献値に幅がある（生成エンタルピーの報告からして割れている）が、
エネルギーの上で不安定——加熱すれば酸素が外れる。ただし常温では分解が
きわめて遅く、試薬として保存できる——ことは動かない。数値の棒は立てず、「ゼロの手前（外れる側）」として描く。

時代は目安。地域と「取り出した」の定義（製錬か、単体として分離か）で幅がある。

出力: _fig1_oxygen.qmd
"""
import efig

P, CID = 'aloxy', 'aloxy1'

W, H = 680, 360
X0 = 150                 # 0 の位置
X1 = 468                 # 560 kJ の位置（右に時代の欄を空ける）
VMAX = 560.0
Y0 = 56                  # 最初の行の中心
DY = 46                  # 行の間隔

# (名前, 記号, 値 kJ/酸素1mol or None, 酸化物, 時代, 強調, 説明)
ROWS = [
    ('金', 'Au', None, '—', '有史以前（砂金として）', False,
     '金は、酸素とほとんど組みません。組ませても、<b>少し熱を加えるだけで酸素が'
     '外れます。</b>そのため川底で、砂金として<b>そのままの姿</b>で見つかりました。'
     '人がいちばん早く手にした金属のひとつです。'),
    ('銅', 'Cu', 146.0, 'Cu₂O', '紀元前5000年ごろ', False,
     '銅の酸化物は、<b>炭と一緒に焚き火より少し熱い火で焼けば</b>酸素が外れます。'
     '人が鉱石から取り出した、最初の金属です。'),
    ('鉄', 'Fe', 247.4, 'Fe₂O₃', '紀元前1200年ごろに広まる', False,
     '銅より固く組んでいますが、<b>炭をたっぷり使って高温にすれば</b>外れます。'
     'たたら製鉄も、いまの溶鉱炉も、やっていることは同じです。'),
    ('亜鉛', 'Zn', 320.5, 'ZnO', '中世（インド）', False,
     '炭で外れますが、外れた亜鉛がすぐ蒸気になって逃げてしまうため、'
     '<b>取り出して集めるのが難しい金属</b>でした。'),
    ('ケイ素', 'Si', 428.2, 'SiO₂', '1824年', False,
     '前回のケイ素です。<b>電気炉で 2000 ℃ 近くまで熱して、ようやく炭で外せます。</b>'
     '初めて単体で取り出されたのは 1824 年でした。'),
    ('アルミニウム', 'Al', 527.4, 'Al₂O₃', '1825年（工業化は1886年）', True,
     '<b>並べた中で、いちばん固く組んでいます。</b>炭をどれだけ使っても、'
     'ふつうの炉では外れません。初めて取り出されたのは 1825 年、'
     'しかも<b>ほんのひとかけら</b>でした。安く大量に作れるようになるのは、'
     '<b>電気で引き剥がす方法</b>が見つかった 1886 年からです。'),
]


def x(v):
    return X0 + v / VMAX * (X1 - X0)


def build_svg():
    o = ['<svg viewBox="0 0 %d %d" role="img" aria-label="金属ごとに、'
         '酸素を引き剥がすのに要るエネルギーと、人が手にした時代を並べた図">'
         % (W, H)]

    # 目盛
    for v in range(0, 561, 100):
        xx = x(v)
        o.append('<line class="%s-gl" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>'
                 % (P, xx, Y0 - 24, xx, Y0 + DY * (len(ROWS) - 1) + 22))
        o.append('<text class="%s-tk" x="%.1f" y="%d">%d</text>'
                 % (P, xx, Y0 + DY * (len(ROWS) - 1) + 40, v))
    o.append('<text class="%s-ax" x="%.1f" y="%d">酸素を引き剥がすのに要るエネルギー'
             '（kJ／酸素 1 mol）→ 固く組んでいる</text>'
             % (P, (X0 + X1) / 2, Y0 + DY * (len(ROWS) - 1) + 60))

    for i, (name, sym, val, ox, era, hot, detail) in enumerate(ROWS):
        yy = Y0 + DY * i
        cls = '%s-row %s-hot' % (P, P) if hot else '%s-row' % P
        o.append('<g class="%s" data-detail="%s">' % (cls, efig.attr(detail)))
        # 当たり判定を広く取る（行全体）
        o.append('<rect class="%s-hit" x="0" y="%d" width="%d" height="%d"/>'
                 % (P, yy - DY // 2, W, DY))
        o.append('<text class="%s-nm" x="%d" y="%d">%s</text>'
                 % (P, X0 - 14, yy + 1, name))
        o.append('<text class="%s-sy" x="%d" y="%d">%s</text>'
                 % (P, X0 - 14, yy + 16, sym if val is None else '%s　%s' % (sym, ox)))
        if val is None:
            # 金：ゼロの手前（外れる側）に印だけ置く
            o.append('<path class="%s-au" d="M%.1f %d l9 -7 v14 z"/>'
                     % (P, x(0) + 3, yy))
            o.append('<text class="%s-aut" x="%.1f" y="%d">組んでも、熱ですぐ外れる</text>'
                     % (P, x(0) + 18, yy + 5))
        else:
            bw = x(val) - x(0)
            o.append('<rect class="%s-bar" x="%.1f" y="%d" width="%.1f" height="18" '
                     'rx="4" style="--w:%.1fpx"/>' % (P, x(0), yy - 9, bw, bw))
            o.append('<text class="%s-v" x="%.1f" y="%d">%d</text>'
                     % (P, x(val) + 6, yy + 5, round(val)))
        o.append('<text class="%s-era" x="%d" y="%d">%s</text>'
                 % (P, W - 8, yy + 5, era))
        o.append('</g>')

    o.append('</svg>')
    return '\n'.join(o)


CSS = """
.%(p)s{--al:#5B6F80;--bar:#9DB0BF;--gl:#E6DDCB;}
.%(p)s-wrap{margin:18px 8px 0;}
.%(p)s-wrap svg{display:block;width:100%%;height:auto;}
.%(p)s-wrap text{font-family:"Hiragino Sans","Yu Gothic","Noto Sans JP",sans-serif;}
.%(p)s-gl{stroke:var(--gl);stroke-width:1;}
.%(p)s-tk{font-size:11px;fill:var(--faint);text-anchor:middle;
  font-variant-numeric:tabular-nums;}
.%(p)s-ax{font-size:11.5px;fill:var(--dim);text-anchor:middle;}
.%(p)s-hit{fill:transparent;}
.%(p)s-row{cursor:default;}
.%(p)s-row:hover .%(p)s-hit{fill:rgba(122,96,52,.06);}
.%(p)s-nm{font-size:14.5px;font-weight:800;fill:var(--ink);text-anchor:end;}
.%(p)s-sy{font-size:10.5px;fill:var(--faint);text-anchor:end;}
.%(p)s-bar{fill:var(--bar);transform-box:fill-box;transform-origin:left center;
  animation:%(p)s-grow 1.1s cubic-bezier(.2,.8,.2,1) both;}
.%(p)s-hot .%(p)s-bar{fill:var(--al);}
.%(p)s-hot .%(p)s-nm{fill:var(--al);}
.%(p)s-v{font-size:12px;font-weight:700;fill:var(--dim);
  font-variant-numeric:tabular-nums;}
.%(p)s-hot .%(p)s-v{fill:var(--al);font-size:13px;}
.%(p)s-era{font-size:12px;fill:var(--dim);text-anchor:end;}
.%(p)s-hot .%(p)s-era{fill:var(--al);font-weight:800;}
.%(p)s-au{fill:#C9A227;}
.%(p)s-aut{font-size:11.5px;fill:var(--dim);}
@keyframes %(p)s-grow{from{transform:scaleX(0);}to{transform:scaleX(1);}}
@media (max-width:820px){.%(p)s-wrap{margin:12px 0 0;}}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(
             P, CID,
             '酸素を離さない金属ほど、人が手にしたのは遅い',
             '棒の長さは、その金属から酸素を引き剥がすのに少なくとも要るエネルギーです'
             '（酸素 6×10²³ 個＝1 mol あたり）。右端は、人が金属として手にした時代の目安。'
             '行にカーソルを合わせる（スマホはタップ）と説明が出ます。')]
    o.append('<div class="%s-wrap">%s</div>' % (P, build_svg()))
    o.append(efig.close_card(
        P,
        '上ほど酸素と組むのが苦手で、下ほど固く組んでいます。'
        '<b>金は酸素とほとんど組まないので、そのままの姿で拾えました。</b>'
        '銅と鉄は、炭と一緒に焼けば酸素が外れます。'
        '<b>アルミは、並べた中でいちばん固く組んでいて、炭を燃やす昔ながらの炉では'
        '外れません。</b>地面に8%もあるのに、この中で人が手にしたのが'
        'いちばん遅かったのは、そのためです。',
        '値は 25 ℃ の標準生成ギブズエネルギーを、酸化物に含まれる酸素原子の数で割り、'
        '符号を反転したもの（Cu₂O −146.0、Fe₂O₃ −742.2、ZnO −320.5、SiO₂（石英）−856.3、'
        'Al₂O₃（コランダム）−1582.3 kJ/mol。CRC Handbook of Chemistry and Physics）。'
        '金の酸化物は報告値に幅があるため数値は示していませんが、エネルギーの上では'
        '不安定で、熱を加えると分解します（常温では分解がきわめて遅く、試薬として'
        '保存できます）。実際の製錬は高温で行うので、必要な熱や炭の量は'
        'この値そのものではありません。エネルギーの上だけで言えば、2000 ℃ を'
        '超えると炭でもアルミナから酸素を奪えるようになりますが、炭化アルミニウムが'
        'できてしまい、実用にはなりません。<b>並び順を比べるための図</b>です。'
        '時代は目安で、地域や「取り出した」の定義（製錬か、単体として分離か）によって幅があります。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    for name, sym, val, ox, era, hot, _ in ROWS:
        print('%-8s %-6s %6s  %s' % (name, ox, '—' if val is None else '%.1f' % val, era))
    efig.save('_fig1_oxygen.qmd', build())
