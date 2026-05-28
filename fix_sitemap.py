import os
import xml.etree.ElementTree as ET

sitemap_path = os.path.join('_site', 'sitemap.xml')

if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # すべての .html</loc> を </loc> に置換（全言語・全ページ共通のクリーンURL対応）
    new_content = content.replace('.html</loc>', '</loc>')
    
    # _site/index.html などのように、フォルダのインデックスページが直接URLになっている場合は、
    # 最後の /index</loc> を /</loc> にする（トップページやカテゴリトップなど）
    new_content = new_content.replace('/index</loc>', '/</loc>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SEO: sitemap.xml のクリーンURL化（.htmlの削除）が完了しました。")
else:
    print("sitemap.xml が見つかりませんでした。")
