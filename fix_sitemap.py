# -*- coding: utf-8 -*-
"""
Quarto post-render フック。
1) sitemap.xml のクリーンURL化・重複排除・404ページの除外
2) 全HTMLへ canonical / og:url を注入（重複コンテンツ対策）
3) alt 属性の無い <img> に alt="" を補完（装飾画像として明示）
"""
import os
import re

BASE = "https://deepflows.net"
SITE = "_site"


# ----------------------------------------------------------------------
# 1) sitemap.xml
# ----------------------------------------------------------------------
def fix_sitemap():
    path = os.path.join(SITE, "sitemap.xml")
    if not os.path.exists(path):
        print("sitemap.xml が見つかりませんでした。")
        return

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # クリーンURL化（.html の削除と /index の削除）
    content = content.replace(".html</loc>", "</loc>")
    content = content.replace("/index</loc>", "/</loc>")

    pattern = re.compile(r"<url>\s*<loc>(.*?)</loc>.*?</url>", re.DOTALL)
    seen = set()

    def replacer(m):
        loc = m.group(1).strip()
        # 404 ページはサイトマップに載せない
        if loc.rstrip("/").endswith("/404"):
            return ""
        if loc in seen:
            return ""
        seen.add(loc)
        return m.group(0)

    content = pattern.sub(replacer, content)
    content = re.sub(r"\n\s*\n", "\n", content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"SEO: sitemap.xml を整形（404除外・重複排除）。ユニークURL数: {len(seen)}")


# ----------------------------------------------------------------------
# 2) canonical / og:url の注入、3) alt 補完
# ----------------------------------------------------------------------
def canonical_url(rel_posix):
    """_site からの相対パス → 正規URL（sitemap と同じクリーンURL規則）"""
    p = rel_posix[: -len(".html")]
    if p == "index":
        return BASE + "/"
    if p.endswith("/index"):
        return BASE + "/" + p[: -len("index")]   # 末尾スラッシュを残す
    return BASE + "/" + p


def iter_html():
    for root, _dirs, files in os.walk(SITE):
        if "site_libs" in root.replace("\\", "/"):
            continue
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(root, fn)


def inject_canonical_and_alt():
    n_canon = n_ogurl = n_alt = 0
    for fp in iter_html():
        rel = os.path.relpath(fp, SITE).replace("\\", "/")
        with open(fp, "r", encoding="utf-8") as f:
            html = f.read()
        orig = html

        # 404 ページは canonical を付けない（noindex 済み）
        if rel != "404.html":
            url = canonical_url(rel)
            tags = ""
            if not re.search(r'<link[^>]+rel=["\']canonical["\']', html, re.I):
                tags += f'<link rel="canonical" href="{url}" />\n'
                n_canon += 1
            if not re.search(r'<meta[^>]+property=["\']og:url["\']', html, re.I):
                tags += f'<meta property="og:url" content="{url}" />\n'
                n_ogurl += 1
            if tags and "</head>" in html:
                html = html.replace("</head>", tags + "</head>", 1)

        # alt の無い <img> に alt="" を補完（隣接する見出しが内容を伝える装飾画像）
        def add_alt(m):
            nonlocal n_alt
            tag = m.group(0)
            if re.search(r"\balt\s*=", tag, re.I):
                return tag
            n_alt += 1
            return tag[:-1].rstrip() + ' alt="" ' + tag[-1]

        html = re.sub(r"<img\b[^>]*>", add_alt, html)

        if html != orig:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(html)

    print(f"SEO: canonical {n_canon}件 / og:url {n_ogurl}件 を注入、alt を {n_alt}件 補完しました。")


if __name__ == "__main__":
    fix_sitemap()
    inject_canonical_and_alt()
