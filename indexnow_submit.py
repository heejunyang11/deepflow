# -*- coding: utf-8 -*-
"""
IndexNow 送信スクリプト（Bing / Yandex 等へ即時クロール通知）。

使い方（デプロイ後にHYさんが手動実行）:
    python indexnow_submit.py            # _site/sitemap.xml の全URLを通知
    python indexnow_submit.py URL [URL...]  # 指定URLだけを通知（更新記事のみ推奨）

仕組み:
    ルートに置いたキーファイル
      https://deepflows.net/40cb5c7348fd64dd48fbeb6c92774598.txt
    の所有を根拠に、urlList を IndexNow API へ POST する。
    キーファイルは _quarto.yml の resources 経由で _site 直下に配信される。
"""
import json
import os
import re
import sys
import urllib.request

HOST = "deepflows.net"
KEY = "40cb5c7348fd64dd48fbeb6c92774598"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = os.path.join("_site", "sitemap.xml")


def urls_from_sitemap():
    if not os.path.exists(SITEMAP):
        print(f"[ERROR] {SITEMAP} が見つかりません。先に quarto render を実行してください。")
        sys.exit(1)
    with open(SITEMAP, "r", encoding="utf-8") as f:
        content = f.read()
    urls = re.findall(r"<loc>(.*?)</loc>", content)
    return [u.strip() for u in urls if u.strip()]


def submit(url_list):
    # IndexNow は 1リクエスト最大 10,000 URL
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            code = resp.getcode()
            body = resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        code = e.code
        body = e.read().decode("utf-8", "ignore")

    # 200/202 は成功。IndexNow は本文をほぼ返さない。
    if code in (200, 202):
        print(f"[OK] IndexNow 送信成功（HTTP {code}）: {len(url_list)} URL を通知しました。")
    else:
        print(f"[WARN] HTTP {code}: {body[:300]}")
        print("  403=キーファイル未配信/不一致, 422=URLとhost不一致 を確認してください。")


def main():
    if len(sys.argv) > 1:
        url_list = sys.argv[1:]
    else:
        url_list = urls_from_sitemap()
    if not url_list:
        print("[ERROR] 通知するURLがありません。")
        sys.exit(1)
    print(f"通知先: {ENDPOINT}")
    print(f"キー: {KEY_LOCATION}")
    for u in url_list:
        print("  -", u)
    submit(url_list)


if __name__ == "__main__":
    main()
