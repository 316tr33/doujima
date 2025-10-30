#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3適用スクリプト: HTMLファイルに新しい説明文を一括置換
"""

import re
from pathlib import Path

# 新しい説明文をインポート
import sys
sys.path.append(str(Path(__file__).parent))
from phase3_new_descriptions import new_descriptions

html_path = Path("/Users/macmiller/Desktop/doujima/Tokaido/stations.html")
html_content = html_path.read_text(encoding='utf-8')

# 現在の説明文を抽出して置換
modified_html = html_content

for number, new_desc in sorted(new_descriptions.items()):
    # 現在の説明文を検索するパターン
    pattern = rf'(<!-- {number}宿 .+? -->.*?<p class="station-description">\s*)(.+?)(\s*</p>)'

    def replace_desc(match):
        # 元のインデントを保持
        return match.group(1) + new_desc + match.group(3)

    # 置換実行
    modified_html = re.sub(pattern, replace_desc, modified_html, count=1, flags=re.DOTALL)
    print(f"✓ {number}番: 説明文を更新しました")

# 結果を保存
html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 3適用完了: {len(new_descriptions)}箇所の説明文を更新しました")
