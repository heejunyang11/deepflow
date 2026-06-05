import os
import re

sitemap_path = os.path.join('_site', 'sitemap.xml')

if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. クリーンURL化（.htmlの削除と /index の削除）
    content = content.replace('.html</loc>', '</loc>')
    content = content.replace('/index</loc>', '/</loc>')
    
    # 2. 重複する <url> ブロックの削除
    pattern = re.compile(r'<url>\s*<loc>(.*?)</loc>.*?</url>', re.DOTALL)
    seen_locs = set()
    
    def replacer(match):
        loc = match.group(1).strip()
        full_block = match.group(0)
        if loc not in seen_locs:
            seen_locs.add(loc)
            return full_block
        else:
            return ""

    new_content = pattern.sub(replacer, content)
    
    # 空行の整理
    new_content = re.sub(r'\n\s*\n', '\n', new_content)
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"SEO: sitemap.xml のクリーンURL化および重複排除が完了しました。ユニークなURL数: {len(seen_locs)}")
else:
    print("sitemap.xml が見つかりませんでした。")
