#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4適用スクリプト: station-highlights/featuresを更新
"""

import re
from pathlib import Path

# 更新データをインポート
import sys
sys.path.append(str(Path(__file__).parent))
from phase4_highlights_update import updated_highlights

html_path = Path("/Users/macmiller/Desktop/doujima/Tokaido/stations.html")
html_content = html_path.read_text(encoding='utf-8')

modified_html = html_content

# 起点（station-features → station-highlights に変更 + タグ更新）
if 0 in updated_highlights:
    tags = updated_highlights[0]
    # station-features を見つけて置換
    pattern_start = r'<div class="station-features">\s*<span class="feature">起点</span>\s*<span class="feature">歴史</span>\s*<span class="feature">名所</span>\s*</div>'
    replacement_start = f'''<div class="station-highlights">
                  <span>{tags[0]}</span>
                  <span>{tags[1]}</span>
                  <span>{tags[2]}</span>
                </div>'''
    modified_html = re.sub(pattern_start, replacement_start, modified_html)
    print("✓ 起点: station-features → station-highlights に変更 + タグ更新")

# 1-53番の宿場
for number in range(1, 54):
    if number in updated_highlights:
        tags = updated_highlights[number]
        # 現在のhighlightsを検索して置換
        pattern = rf'(<!-- {number}宿 .+? -->.*?<div class="station-highlights">\s*)(<span>.+?</span>\s*<span>.+?</span>\s*<span>.+?</span>)(\s*</div>)'

        def replace_highlights(match):
            return match.group(1) + f'''<span>{tags[0]}</span>
                  <span>{tags[1]}</span>
                  <span>{tags[2]}</span>''' + match.group(3)

        modified_html = re.sub(pattern, replace_highlights, modified_html, count=1, flags=re.DOTALL)
        print(f"✓ {number}番: タグを更新しました")

# 終点
if 54 in updated_highlights:
    tags = updated_highlights[54]
    pattern_end = r'(<!-- 終点 -->.*?<div class="station-highlights">\s*)(<span>.+?</span>\s*<span>.+?</span>\s*<span>.+?</span>)(\s*</div>)'

    def replace_end(match):
        return match.group(1) + f'''<span>{tags[0]}</span>
                  <span>{tags[1]}</span>
                  <span>{tags[2]}</span>''' + match.group(3)

    modified_html = re.sub(pattern_end, replace_end, modified_html, count=1, flags=re.DOTALL)
    print("✓ 終点: タグを更新しました")

# 結果を保存
html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 4適用完了: {len(updated_highlights)}箇所のstation-highlightsを更新しました")
