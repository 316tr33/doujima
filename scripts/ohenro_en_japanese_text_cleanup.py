#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 日本語テキスト英語化スクリプト
ALT属性とラベルを英語に変換
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 日本語テキスト英語化")
print("=" * 80)

modified_html = en_html

# 1. ALT属性の英語化
print("\n【1. ALT属性の英語化】")
alt_pattern = r'alt="YouTube動画"'
alt_replacement = 'alt="Temple video thumbnail"'
alt_count = len(re.findall(alt_pattern, modified_html))
modified_html = re.sub(alt_pattern, alt_replacement, modified_html)
print(f"✓ 'YouTube動画' → 'Temple video thumbnail': {alt_count}箇所")

# 2. 日本語住所ラベルの英語化
print("\n【2. 日本語住所ラベルの英語化】")
label_pattern = r'<p class="japanese-address">所在地: '
label_replacement = r'<p class="japanese-address">Japanese Address: '
label_count = len(re.findall(label_pattern, modified_html))
modified_html = re.sub(label_pattern, label_replacement, modified_html)
print(f"✓ '所在地:' → 'Japanese Address:': {label_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')

print("\n" + "=" * 80)
print("✅ 日本語テキスト英語化完了")
print(f"   - ALT属性: {alt_count}箇所")
print(f"   - 住所ラベル: {label_count}箇所")
print(f"   - 合計: {alt_count + label_count}箇所")
print("=" * 80)
