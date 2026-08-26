# -*- coding: utf-8 -*-
"""
元素 #3 酸素 / 図6 : 錆びる・燃える・呼吸する は、同じことである。

#2 の次回予告で読者に約束した回収。

骨:
  3 つとも「電子が酸素へ移る」まったく同じ反応である。
  <酸素 1 モルあたりに出るエネルギーで揃えると、どれも 450〜550 kJ>。
  違うのは速さだけ。そしてその速さを決めているのが、図2 で見た
  「電子の向きがそろっていないので、そのままでは反応できない」という壁。
  ・燃える  = 熱で壁を越えさせる（いちど越えると連鎖して一気に進む）
  ・呼吸する = 鉄を含む酵素が壁を回り道させる（体温のまま、ゆっくり確実に）
  ・錆びる  = 壁をなかなか越えられないまま、何年もかけて少しずつ

エネルギーの計算（標準生成エンタルピーから。すべて NIST の値）:
  Fe2O3(s)  -825.5 kJ/mol   NIST-JANAF 第4版
  CO2(g)    -393.51 kJ/mol  CODATA
  H2O(l)    -285.83 kJ/mol  CODATA
  CH4(g)    -74.6 kJ/mol    NIST WebBook
  glucose(s) -1273.3 kJ/mol

  4Fe + 3O2 -> 2Fe2O3            2*(-825.5)            = -1651.0 / 3 O2
  CH4 + 2O2 -> CO2 + 2H2O(l)     直接の測定値 -890.7   /  2 O2
      （NIST WebBook、Pittam & Pilcher 1972 の燃焼熱測定）
  C6H12O6 + 6O2 -> 6CO2 + 6H2O(l) 6(-393.51)+6(-285.83)-(-1273.3) / 6 O2

書いてはいけないこと（HY指示「説は説と」）:
  速さの具体的な秒数。錆びる速さは条件で桁が変わるし、
  燃焼や呼吸の「1回あたりの時間」も定義しだいで変わる。
  <エネルギーは数値で、速さは言葉で>という分け方にする。

出力: _fig6_same.qmd
"""
import efig

P, CID = 'osame', 'osame1'

# 標準生成エンタルピー（kJ/mol）
H = {'Fe2O3': -825.5, 'CO2': -393.51, 'H2O_l': -285.83,
     'CH4': -74.6, 'glucose': -1273.3}
H_COMB_CH4 = -890.7        # メタンの燃焼熱（直接の測定値）


def per_o2_iron():
    """4Fe + 3O₂ → 2Fe₂O₃。鉄は単体なので生成エンタルピーは 0。"""
    return 2 * H['Fe2O3'] / 3.0


def per_o2_methane():
    """CH₄ + 2O₂ → CO₂ + 2H₂O。測定された燃焼熱をそのまま使う。"""
    return H_COMB_CH4 / 2.0


def per_o2_glucose():
    """C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O。生成エンタルピーから組み立てる。"""
    dh = 6 * H['CO2'] + 6 * H['H2O_l'] - H['glucose']
    return dh / 6.0


# (鍵, 名前, 反応式, 酸素1モルあたり kJ, 速さ, 色)
ROW = [
    ('rust', '鉄が錆びる', '4 Fe ＋ 3 O₂ → 2 Fe₂O₃',
     per_o2_iron(), '何年もかけて、少しずつ', '#8A5A2B'),
    ('breath', 'ブドウ糖を呼吸する', 'C₆H₁₂O₆ ＋ 6 O₂ → 6 CO₂ ＋ 6 H₂O',
     per_o2_glucose(), '体温のまま、ゆっくり確実に', '#B0361B'),
    ('burn', 'メタンが燃える', 'CH₄ ＋ 2 O₂ → CO₂ ＋ 2 H₂O',
     per_o2_methane(), '火をつけた瞬間、一気に', '#D8874A'),
]

DET = {
    'rust': '<b>鉄が錆びる。</b>鉄から酸素へ電子が移り、酸化鉄になります。'
            '酸素1モルあたり <b>%.0f kJ</b>——'
            '実は3つの中で<b>いちばん多くエネルギーが出ます</b>。'
            'それでも熱くならないのは、'
            '<b>あまりにゆっくりだから</b>です。'
            '同じ量の熱が、何年もかけて少しずつ逃げていきます。'
            'カイロが温かくなるのは、'
            'この反応をわざと速めているからです。'
            % abs(per_o2_iron()),
    'breath': '<b>呼吸する。</b>あなたがいま、体の中でやっていることです。'
              '食べ物から酸素へ電子が移ります。'
              '酸素1モルあたり <b>%.0f kJ</b>——'
              '燃やしたときと<b>ほとんど変わりません</b>。'
              '違うのは、<b>鉄を含む酵素</b>が反応を何段階にも小分けし、'
              '体温のまま、エネルギーを取り出せる形で進めている点です。'
              '燃やすのではなく、<b>制御して燃やしている</b>のです。'
              % abs(per_o2_glucose()),
    'burn': '<b>燃える。</b>メタンから酸素へ電子が移ります。'
            '酸素1モルあたり <b>%.0f kJ</b>。'
            '出るエネルギーは錆びるときと大差ありません。'
            '違うのは<b>速さ</b>だけです。'
            '熱で最初の壁を越えさせると、'
            'そこで生まれた分子が次を壊し、また次を壊し——と'
            '<b>連鎖して一気に進みます</b>。'
            'これが炎です。'
            % abs(per_o2_methane()),
}

BAR_MAX = 600.0

CSS = """
.@@P@@-list{margin:20px 8px 0;}
.@@P@@-line{margin:0 0 18px;cursor:default;
  padding:12px 14px;border-radius:12px;
  background:rgba(122,96,52,.035);
  border:1px solid rgba(122,96,52,.13);
  transition:background .16s ease,border-color .16s ease;}
.@@P@@-line:hover{background:rgba(190,100,10,.06);
  border-color:rgba(190,100,10,.34);}
.@@P@@-nm{font-size:1.04rem;font-weight:800;color:var(--ink);}
.@@P@@-eq{font-size:.9rem;color:var(--dim);margin:2px 0 9px;
  font-variant-numeric:tabular-nums;}
.@@P@@-bar{display:flex;align-items:center;gap:11px;}
.@@P@@-track{position:relative;flex:1 1 auto;height:22px;border-radius:6px;
  background:rgba(122,96,52,.09);}
.@@P@@-fill{position:absolute;left:0;top:0;bottom:0;border-radius:6px;}
.@@P@@-kj{font-size:1rem;font-weight:800;color:var(--ink);
  font-variant-numeric:tabular-nums;white-space:nowrap;}
.@@P@@-sp{font-size:.86rem;color:var(--hb);font-weight:700;margin:7px 0 0;}

.@@P@@-cap{margin:16px 8px 0;font-size:.84rem;color:var(--dim);
  line-height:1.75;}
.@@P@@-punch{margin:18px 8px 0;padding:15px 17px;border-radius:12px;
  background:rgba(190,100,10,.07);border:1px solid rgba(190,100,10,.34);
  font-size:.94rem;line-height:1.85;color:var(--ink);}
.@@P@@-punch b{color:var(--hb);}

@media (max-width:820px){
  .@@P@@-list{margin:16px 2px 0;}
  .@@P@@-line{padding:10px 11px;}
  .@@P@@-nm{font-size:.94rem;}
  .@@P@@-eq{font-size:.78rem;}
  .@@P@@-kj{font-size:.88rem;}
  .@@P@@-sp{font-size:.78rem;}
  .@@P@@-cap,.@@P@@-punch{font-size:.78rem;margin:13px 2px 0;}
}
""".replace('@@P@@', P)


def check():
    print('酸素1モルあたりに出るエネルギー（標準生成エンタルピーから計算）:')
    vals = []
    for key, name, eq, kj, speed, col in ROW:
        print('  %-18s %8.1f kJ / 酸素1モル' % (name, kj))
        vals.append(abs(kj))
    lo, hi = min(vals), max(vals)
    print('  幅 %.0f 〜 %.0f kJ（最大は最小の %.2f 倍）' % (lo, hi, hi / lo))
    assert hi / lo < 1.35, 'この図の骨（どれも同じくらい）が崩れている'
    # グルコースの計算が文献値と合うか
    dh = 6 * H['CO2'] + 6 * H['H2O_l'] - H['glucose']
    print('  ブドウ糖の燃焼熱 %.1f kJ/mol（文献値 約 -2803）' % dh)
    assert abs(dh + 2803.0) < 2.0
    # 錆がいちばん多くエネルギーを出す、という意外な事実
    assert abs(per_o2_iron()) == hi
    print('  -> いちばん多くエネルギーを出すのは、実は「錆びる」')


def build():
    o = [efig.css(P, CSS),
         efig.open_card(P, CID, '錆びる、燃える、呼吸する',
                        'この3つは、まったく同じ反応です。'
                        '<b>酸素1モルあたりに出るエネルギーで揃えて</b>'
                        '並べました。'
                        'カーソルを合わせる（スマホはタップ）と、'
                        'その中身が下に出ます。'),
         '<div class="%s-list">' % P]

    for key, name, eq, kj, speed, col in ROW:
        o.append('<div class="%s-line" data-detail="%s">'
                 % (P, efig.attr(DET[key])))
        o.append('<div class="%s-nm">%s</div>' % (P, name))
        o.append('<div class="%s-eq">%s</div>' % (P, eq))
        o.append('<div class="%s-bar"><div class="%s-track">'
                 '<div class="%s-fill" style="width:%.1f%%;'
                 'background:linear-gradient(90deg,%s,%s)"></div></div>'
                 '<span class="%s-kj">%.0f kJ</span></div>'
                 % (P, P, P, abs(kj) / BAR_MAX * 100.0, col, col, P, abs(kj)))
        o.append('<p class="%s-sp">速さ：%s</p></div>' % (P, speed))
    o.append('</div>')

    lo = min(abs(r[3]) for r in ROW)
    hi = max(abs(r[3]) for r in ROW)
    o.append('<p class="%s-cap">棒の長さは、'
             '<b>酸素1モルを使ったときに出るエネルギー</b>です。'
             '%.0f 〜 %.0f kJ——'
             'いちばん大きいものでも、いちばん小さいものの<b>%.2f倍</b>しか'
             'ありません。'
             'しかも意外なことに、<b>いちばん多くエネルギーを出すのは'
             '「錆びる」</b>のほうです。</p>' % (P, lo, hi, hi / lo))

    o.append('<div class="%s-punch">では、なぜ鉄は熱くならず、'
             'メタンは炎を上げるのか。'
             '<b>違いは、速さだけです。</b>'
             'そして速さを決めているのが、'
             'この記事のはじめに見た<b>「電子の向きがそろっていない」</b>という壁。'
             '<br>・<b>燃える</b>——熱で壁を越えさせる。'
             'いちど越えると連鎖して一気に進む。'
             '<br>・<b>呼吸する</b>——鉄を含む酵素が、壁を回り道させる。'
             '体温のまま、少しずつ、取り出せる形で。'
             '<br>・<b>錆びる</b>——壁をなかなか越えられないまま、'
             '何年もかけて少しずつ。</div>' % P)

    o.append(efig.close_card(
        P,
        'あなたが呼吸することと、ガスコンロが燃えることと、'
        '自転車が錆びることは、<b>化学としてはまったく同じ現象</b>です。'
        'どれも「電子が酸素へ移る」。'
        '出てくるエネルギーも、酸素1モルあたりで揃えれば'
        '<b>ほとんど変わりません</b>。'
        '違うのは速さだけで、その速さを決めているのが'
        '<b>酸素の電子の向き</b>でした。'
        '生き物は、この壁を壊すのではなく、'
        '<b>鉄を含む酵素で回り道させる</b>という方法を見つけた。'
        'そのおかげで、私たちは燃えずに、'
        '体温のまま酸素を使えています。',
        'エネルギーはすべて標準生成エンタルピーからの計算です。'
        'Fe₂O₃(s) −825.5 kJ/mol（NIST-JANAF 第4版）、'
        'CO₂(g) −393.51 kJ/mol、H₂O(液) −285.83 kJ/mol（CODATA）、'
        'ブドウ糖(s) −1273.3 kJ/mol。'
        'メタンだけは直接測られた燃焼熱 −890.7±0.4 kJ/mol'
        '（NIST WebBook、Pittam &amp; Pilcher 1972）を使いました。'
        'ブドウ糖の燃焼熱は生成エンタルピーから −2802.7 kJ/mol と出て、'
        '文献値の約 −2803 kJ/mol と一致します。'
        '<b>速さについては数値を書いていません。</b>'
        '錆びる速さは湿り気や塩分で桁が変わりますし、'
        '「燃焼1回にかかる時間」も定義しだいで変わるためです。'
        'エネルギーは数値で、速さは言葉で示しています。',
        CID))
    return '\n'.join(o)


if __name__ == '__main__':
    check()
    efig.save('_fig6_same.qmd', build())
