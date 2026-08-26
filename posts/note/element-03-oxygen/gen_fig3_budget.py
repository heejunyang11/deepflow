# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図3 : いま、酸素はどう出入りしているか。

旧図（40億年の酸素史）を差し替えたもの。
「今日その場で観測できるものだけで書く」という方針に合わせ、
過去の復元ではなく、いま測られている収支に置き換えた。

数値（すべてこのファイル内で計算する。定数だけを外から持ってくる）:
  大気の質量      5.148e21 g      Trenberth & Smith (2005)
  空気の平均分子量 28.96 g/mol
  乾燥空気の O2    20.946 vol%
    -> 大気の O2  3.72e19 mol

  総一次生産 GPP  110-250 PgC/yr  陸 120±30、海 90-120 の推定に幅がある
    光合成は C 1 mol の固定につき O2 を 1 mol 出す
    -> 0.92-2.08e16 mol O2/yr
  呼吸と分解が取り出す量は、ほぼ同量（差が有機炭素の埋没ぶん）

  実測の正味減少   年 4 ppm（空気に対して）= 19 per meg/yr
                  Scripps O2 Program（Ralph Keeling）1980 年代末から継続測定
    -> 7.1e14 mol/yr

読み取らせたいこと:
  (1) 入る量と出る量がほぼ釣り合っているから、21% が保たれている
  (2) それでも正味では減っていて、それは実測されている
  (3) ただし尽きるまで約 5 万年。心配すべきは酸素の欠乏ではない

出力: _fig3_budget.qmd
"""
import efig

P, CID = 'obud', 'obud3'

# --- 定数から計算する ------------------------------------------------------
M_ATM = 5.148e21          # 大気の質量 g
M_AIR = 28.96             # 空気の平均分子量 g/mol
F_O2 = 0.20946            # 乾燥空気中の O2 の体積比

N_AIR = M_ATM / M_AIR
N_O2 = N_AIR * F_O2                        # 3.72e19 mol

GPP_LO, GPP_HI = 110.0, 250.0              # PgC/yr
FLUX_LO = GPP_LO * 1e15 / 12.0             # mol O2/yr
FLUX_HI = GPP_HI * 1e15 / 12.0

DEC_PPM = 4.0e-6
DEC = DEC_PPM * N_AIR                      # 7.1e14 mol/yr

T_LO = N_O2 / FLUX_HI                      # 入れ替わり（年）
T_HI = N_O2 / FLUX_LO
T_EMPTY = N_O2 / DEC                       # 尽きるまで（年）

SPAN = FLUX_HI                             # 棒の全長に対応させる量


def pct(v):
    return 100.0 * v / SPAN


#  key, 見出し, 向き, 下限, 上限, 色トークン, 補足, 読み取り帯の文
BARS = [
    ('in', '光合成が、入れる', '＋', FLUX_LO, FLUX_HI, 'o',
     '陸の植物と、海の植物プランクトン',
     '水を分解して水素を材料に使い、<b>いらなくなった酸素を捨てて</b>います。'
     '水草にライトを当てると出てくる泡が、これです。'
     '幅があるのは、地球全体の光合成の量が<b>まだ正確には分かっていない</b>ため。'),
    ('out', '呼吸と分解が、取り出す', '−', FLUX_LO, FLUX_HI, 'e',
     'ほぼ同じ量が、そのまま戻っていく',
     '生き物の呼吸と、死んだものが分解される反応です。'
     '<b>入る量とほとんど同じ</b>で、この釣り合いが 21% を保っています。'
     '差はごくわずかで、それが地面に埋まる炭素のぶんです。'),
    ('burn', '人間が燃やすぶん', '−', DEC, DEC, 'other',
     '実測されている、釣り合いの外側',
     '化石燃料を燃やして消えるぶんです。'
     '<b>実際に測られていて、年に 100 万分の 4 ずつ減っています</b>'
     '（Scripps O2 Program）。上の 2 本に比べれば細いのですが、'
     '<b>こちらは戻ってきません</b>。'),
]

CSS = """
.%(p)s-res{margin:20px 8px 0;padding:16px 18px 15px;border-radius:13px;
  background:linear-gradient(90deg,rgba(216,85,42,.14),rgba(216,85,42,.07));
  border:1px solid rgba(216,85,42,.28);cursor:default;}
.%(p)s-res .k{font-size:.85rem;color:var(--dim);letter-spacing:.02em;}
.%(p)s-res .v{font-size:1.9rem;font-weight:800;color:var(--o);
  line-height:1.35;margin-top:2px;letter-spacing:.01em;}
.%(p)s-res .v em{font-style:normal;font-size:.5em;font-weight:600;opacity:.8;
  margin-left:6px;}
.%(p)s-res .n{font-size:.85rem;color:var(--dim);margin-top:4px;line-height:1.65;}

.%(p)s-flab{margin:22px 8px 9px;font-size:.92rem;color:var(--dim);}
.%(p)s-bars{margin:0 8px;display:grid;gap:13px;}
.%(p)s-r{cursor:default;}
.%(p)s-r .hd{display:flex;align-items:baseline;gap:9px;margin:0 0 5px;}
.%(p)s-r .sg{font-size:1.05rem;font-weight:800;color:var(--c);width:1em;}
.%(p)s-r .nm{font-size:1rem;font-weight:800;color:var(--ink);}
.%(p)s-r .sb{font-size:.82rem;color:var(--dim);margin-left:auto;
  text-align:right;line-height:1.5;}
.%(p)s-tr{position:relative;height:26px;border-radius:7px;
  background:rgba(122,96,52,.07);border:1px solid rgba(122,96,52,.13);
  overflow:hidden;transition:background .18s ease;}
.%(p)s-r:hover .%(p)s-tr{background:rgba(122,96,52,.15);}
.%(p)s-bd{position:absolute;top:0;bottom:0;border-radius:6px;
  background:linear-gradient(90deg,
    color-mix(in srgb,var(--c) 34%%,transparent),
    color-mix(in srgb,var(--c) 78%%,transparent));}
/* 推定に幅があるものは、右端をぼかして「ここまでは確かでない」と示す */
.%(p)s-bd.rng::after{content:"";position:absolute;top:0;bottom:0;right:0;
  width:38%%;background:linear-gradient(90deg,transparent,rgba(255,253,249,.62));}
.%(p)s-tk{position:absolute;top:-2px;bottom:-2px;width:2px;
  background:var(--c);opacity:.85;}
.%(p)s-vl{position:absolute;top:50%%;transform:translateY(-50%%);
  font-size:.8rem;font-weight:700;color:var(--ink);white-space:nowrap;
  padding:0 9px;}

.%(p)s-outs{display:grid;grid-template-columns:1fr 1fr;gap:10px;
  margin:20px 8px 8px;}
.%(p)s-o{padding:14px 16px;border-radius:12px;text-align:center;
  background:rgba(122,96,52,.075);border:1px solid rgba(122,96,52,.16);
  cursor:default;transition:background .18s ease;}
.%(p)s-o:hover{background:rgba(122,96,52,.15);}
.%(p)s-o .k{font-size:.82rem;color:var(--dim);line-height:1.5;}
.%(p)s-o .v{font-size:1.5rem;font-weight:800;color:var(--c);
  line-height:1.4;margin-top:3px;}
.%(p)s-o .v em{font-style:normal;font-size:.55em;font-weight:600;opacity:.82;
  margin-left:3px;}

@media (max-width:820px){
  .%(p)s-res{margin:16px 2px 0;padding:13px 14px 12px;}
  .%(p)s-res .v{font-size:1.45rem;}
  .%(p)s-flab{margin:18px 2px 8px;font-size:.84rem;}
  .%(p)s-bars{margin:0 2px;gap:11px;}
  .%(p)s-r .nm{font-size:.88rem;}
  .%(p)s-r .sb{display:none;}
  .%(p)s-tr{height:22px;}
  .%(p)s-vl{font-size:.72rem;padding:0 7px;}
  .%(p)s-outs{margin:16px 2px 6px;gap:8px;}
  .%(p)s-o{padding:11px 10px;}
  .%(p)s-o .v{font-size:1.15rem;}
  .%(p)s-o .k{font-size:.74rem;}
}
""" % {'p': P}


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, 'いま、酸素はどう出入りしているか',
                        '棒はすべて同じ物差しです。'
                        'カーソルを合わせる（スマホはタップ）と説明が出ます。')]

    # 貯金
    o.append('<div class="%s-res" data-detail="%s">'
             '<div class="k">空気にある酸素の総量</div>'
             '<div class="v">3.72 × 10<sup>19</sup><em>モル</em></div>'
             '<div class="n">重さにすると <b>1.19 × 10<sup>18</sup> kg</b>。'
             '大気の質量と、乾いた空気に酸素が 20.946%% 含まれることから'
             '計算した値です。</div></div>'
             % (P, efig.attr(
                 'これが「貯金」です。下の棒は、この貯金に'
                 '<b>毎年出入りしている量</b>を表しています。'
                 '貯金に比べれば、出入りはずっと小さいことに注目してください。')))

    o.append('<p class="%s-flab">毎年の出入り（酸素のモル数）</p>' % P)
    o.append('<div class="%s-bars">' % P)
    for key, name, sign, lo, hi, tok, sub, detail in BARS:
        rng = hi > lo * 1.02
        if rng:
            val = '%.1f 〜 %.1f × 10<sup>16</sup>' % (lo / 1e16, hi / 1e16)
        else:
            val = '%.2f × 10<sup>14</sup>' % (lo / 1e14)
        bar = ('<div class="%s-bd%s" style="left:0;width:%.2f%%"></div>'
               % (P, ' rng' if rng else '', pct(hi)))
        tick = ('<div class="%s-tk" style="left:%.2f%%"></div>'
                % (P, pct(lo))) if rng else ''
        # 値の札は、棒が細いときだけ外に出す
        left = 'left:%.2f%%' % min(pct(hi) + 1.2, 62.0) if pct(hi) < 30 else 'left:0'
        o.append('<div class="%s-r" data-detail="%s" style="--c:var(--%s)">'
                 '<div class="hd"><span class="sg">%s</span>'
                 '<span class="nm">%s</span><span class="sb">%s</span></div>'
                 '<div class="%s-tr">%s%s'
                 '<div class="%s-vl" style="%s">%s</div></div></div>'
                 % (P, efig.attr(detail), tok, sign, name, sub,
                    P, bar, tick, P, left, val))
    o.append('</div>')

    o.append('<div class="%s-outs">' % P)
    o.append('<div class="%s-o" data-detail="%s" style="--c:var(--o)">'
             '<div class="k">空気の酸素が、ぜんぶ<br/>入れ替わるのにかかる時間</div>'
             '<div class="v">約 %s<em>〜</em>%s<em>年</em></div></div>'
             % (P, efig.attr(
                 '貯金を、毎年の出入りで割った時間です。'
                 '<b>およそ数千年で、空気の酸素は生き物の体をひとまわりします。</b>'
                 '幅があるのは、光合成の総量の見積もりに幅があるためです。'),
                '{:,}'.format(int(round(T_LO / 100.0) * 100)),
                '{:,}'.format(int(round(T_HI / 100.0) * 100))))
    o.append('<div class="%s-o" data-detail="%s" style="--c:var(--other)">'
             '<div class="k">いまの減り方が続いたとき<br/>酸素が尽きるまで</div>'
             '<div class="v">約 %s<em>万年</em></div></div>'
             % (P, efig.attr(
                 '年 4 ppm の減少が、このまま続いたと仮定した場合の計算です。'
                 '<b>酸素が足りなくなる心配は、当面ありません。</b>'
                 '同じ燃焼で増えている二酸化炭素のほうが、はるかに速く効きます。'),
                '{:.0f}'.format(round(T_EMPTY / 1e4))))
    o.append('</div>')

    o.append(efig.close_card(
        P,
        '空気に酸素が 21% もあるのは、'
        '<b>入る量と出る量が、ほとんど釣り合っているから</b>です。'
        '光合成が入れて、呼吸と分解が同じだけ取り出す。'
        'その差はごくわずかで、そのわずかが積み上がったものを私たちは吸っています。'
        'そして<b>いま、酸素は実際に減っています</b>——年に 100 万分の 4 ずつ。'
        '化石燃料を燃やしているぶんです。'
        'ただしこの速さなら尽きるまで約 5 万年かかるので、'
        '<b>心配すべきは酸素の欠乏ではありません</b>。'
        '同じ燃焼で増えている二酸化炭素のほうです（#2 の図6を参照）。',
        '大気の酸素量は大気質量 5.148 × 10<sup>21</sup> g'
        '（Trenberth &amp; Smith 2005）、空気の平均分子量 28.96 g/mol、'
        '乾燥空気の O<sub>2</sub> 20.946 vol% から計算。'
        '光合成の量は総一次生産 110〜250 PgC/年の推定幅を、'
        '炭素 1 mol につき酸素 1 mol として換算したもの。'
        '減少速度は '
        '<a href="https://scrippso2.ucsd.edu/">Scripps O<sub>2</sub> Program</a>'
        '（Ralph Keeling）による年 19 per meg（空気に対して約 4 ppm）。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    print('大気の O2      : %.3e mol' % N_O2)
    print('光合成         : %.2e 〜 %.2e mol/yr' % (FLUX_LO, FLUX_HI))
    print('人間の燃焼     : %.2e mol/yr  (棒の %.1f%%)' % (DEC, pct(DEC)))
    print('入れ替わり     : %.0f 〜 %.0f 年' % (T_LO, T_HI))
    print('尽きるまで     : %.0f 年' % T_EMPTY)
    efig.save('_fig3_budget.qmd', build())
