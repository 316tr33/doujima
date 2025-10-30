#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2 翻訳適用スクリプト
英語版HTMLに翻訳データ（宿場名、説明文、ハイライト）を適用
"""

import re
from pathlib import Path
from tokaido_station_names_en import STATION_NAMES_FULL_EN
from tokaido_descriptions_en import DESCRIPTIONS_EN
from tokaido_highlights_en import HIGHLIGHTS_EN

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2: 翻訳適用")
print("=" * 80)

# 変更カウンター
changes = {
    'names': 0,
    'readings': 0,
    'descriptions': 0,
    'highlights': 0,
    'detail_labels': 0
}

# 1. 宿場名の翻訳（h3タグ）
print("\n【1. 宿場名の翻訳】")
for data_num, english_name in STATION_NAMES_FULL_EN.items():
    # data-number属性でカードを探す
    pattern = rf'(data-number="{data_num}".*?<h3>)(.+?)(</h3>)'
    match = re.search(pattern, en_html, re.DOTALL)

    if match:
        old_name = match.group(2)
        en_html = en_html.replace(match.group(0), match.group(1) + english_name + match.group(3))
        changes['names'] += 1
        print(f"  {data_num}: {old_name.strip()} → {english_name}")

# 2. 読み仮名の削除（station-reading）
print("\n【2. 読み仮名の削除】")
reading_pattern = r'\s*<div class="station-reading">[^<]+</div>\s*'
reading_matches = re.findall(reading_pattern, en_html)
changes['readings'] = len(reading_matches)
en_html = re.sub(reading_pattern, '\n        ', en_html)
print(f"  {changes['readings']}箇所の読み仮名を削除")

# 3. 説明文の翻訳
print("\n【3. 説明文の翻訳】")
for data_num, english_desc in DESCRIPTIONS_EN.items():
    # data-number属性でカードを探し、station-descriptionを置換
    pattern = rf'(data-number="{data_num}".*?<p class="station-description">\s*)(.+?)(\s*</p>)'
    match = re.search(pattern, en_html, re.DOTALL)

    if match:
        old_desc = match.group(2).strip()
        en_html = en_html.replace(match.group(0), match.group(1) + english_desc + match.group(3))
        changes['descriptions'] += 1
        print(f"  {data_num}: {old_desc[:30]}... → {english_desc[:30]}...")

# 4. ハイライトの翻訳
print("\n【4. ハイライトの翻訳】")
# station-highlights内の各spanを翻訳
for ja_keyword, en_keyword in HIGHLIGHTS_EN.items():
    pattern = rf'(<div class="station-highlights">.*?)(<span>{re.escape(ja_keyword)}</span>)(.*?</div>)'
    matches = list(re.finditer(pattern, en_html, re.DOTALL))

    for match in matches:
        old_content = match.group(0)
        new_content = old_content.replace(match.group(2), f'<span>{en_keyword}</span>')
        en_html = en_html.replace(old_content, new_content, 1)
        changes['highlights'] += 1

print(f"  {changes['highlights']}箇所のハイライトを翻訳")

# 5. 詳細情報ラベルの翻訳
print("\n【5. 詳細情報ラベルの翻訳】")
detail_labels = {
    '見学時間：': 'Visit Time: ',
    '最寄り駅：': 'Nearest Station: ',
    '住所：': 'Address: ',
    '所在地：': 'Location: ',
    '交通：': 'Access: ',
    'アクセス：': 'Access: ',
    '営業時間：': 'Hours: ',
    '入場料：': 'Admission: ',
    '無料': 'Free',
    '常時開放': 'Always Open',
    '見学自由': 'Free Admission',
    '外観のみ': 'Exterior Only'
}

for ja_label, en_label in detail_labels.items():
    count = en_html.count(ja_label)
    if count > 0:
        en_html = en_html.replace(ja_label, en_label)
        changes['detail_labels'] += count
        print(f"  {ja_label} → {en_label} ({count}箇所)")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2 翻訳適用完了")
print(f"   宿場名: {changes['names']}箇所")
print(f"   読み仮名削除: {changes['readings']}箇所")
print(f"   説明文: {changes['descriptions']}箇所")
print(f"   ハイライト: {changes['highlights']}箇所")
print(f"   詳細ラベル: {changes['detail_labels']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
