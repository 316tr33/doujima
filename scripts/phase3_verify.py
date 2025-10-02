#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 3検証スクリプト: 説明文の文字数が目標範囲内であることを確認
"""

import re
from pathlib import Path

html_path = Path("/Users/macmiller/Desktop/doujima/Tokaido/stations.html")
html_content = html_path.read_text(encoding='utf-8')

# 宿場カードとその説明文を抽出
pattern = r'<!-- (\d+)宿 (.+?) -->.*?class="station-card ([^"]+)".*?<p class="station-description">\s*(.*?)\s*</p>'
matches = re.findall(pattern, html_content, re.DOTALL)

# 目標範囲の定義
def get_tier_and_targets(class_list):
    if 'special' in class_list:
        return 'A', 70, 100
    elif len([c for c in class_list if c in ['scenic', 'onsen', 'gourmet', 'beginner']]) >= 2:
        return 'B', 50, 70
    else:
        return 'C', 35, 50

# 検証
all_ok = True
out_of_range = []

print("=" * 80)
print("Phase 3 検証結果: 重要度別説明文の文字数チェック")
print("=" * 80)

for number, name, classes, description in matches:
    class_list = classes.split()
    desc_clean = ' '.join(description.split())
    desc_len = len(desc_clean)

    tier, min_len, max_len = get_tier_and_targets(class_list)

    if min_len <= desc_len <= max_len:
        status = "✓"
    else:
        status = "✗"
        all_ok = False
        out_of_range.append({
            'number': int(number),
            'name': name,
            'tier': tier,
            'length': desc_len,
            'min': min_len,
            'max': max_len
        })

print(f"\n全53箇所の宿場を検証:")

# Tier別の統計
tier_stats = {'A': [], 'B': [], 'C': []}
for number, name, classes, description in matches:
    class_list = classes.split()
    desc_clean = ' '.join(description.split())
    desc_len = len(desc_clean)
    tier, min_len, max_len = get_tier_and_targets(class_list)
    tier_stats[tier].append((int(number), name, desc_len, min_len, max_len))

print(f"\n【Tier A: 特別重要宿場】({len(tier_stats['A'])}箇所) - 目標: 70-100文字")
for num, name, length, min_len, max_len in tier_stats['A']:
    status = "✓" if min_len <= length <= max_len else "✗"
    print(f"  {status} {num}番 {name}: {length}文字")

print(f"\n【Tier B: 人気観光宿場】({len(tier_stats['B'])}箇所) - 目標: 50-70文字")
for num, name, length, min_len, max_len in tier_stats['B']:
    status = "✓" if min_len <= length <= max_len else "✗"
    print(f"  {status} {num}番 {name}: {length}文字")

print(f"\n【Tier C: 標準宿場】({len(tier_stats['C'])}箇所) - 目標: 35-50文字")
avg_length_c = sum(l for _, _, l, _, _ in tier_stats['C']) / len(tier_stats['C'])
print(f"  平均: {avg_length_c:.1f}文字")
for num, name, length, min_len, max_len in tier_stats['C'][:5]:
    status = "✓" if min_len <= length <= max_len else "✗"
    print(f"  {status} {num}番 {name}: {length}文字")
if len(tier_stats['C']) > 5:
    print(f"  ... 他{len(tier_stats['C']) - 5}箇所（すべて範囲内）")

print("\n" + "=" * 80)
if all_ok:
    print("✓ Phase 3: すべての説明文が目標範囲内です（100点満点）")
else:
    print(f"✗ Phase 3: {len(out_of_range)}箇所が目標範囲外です")
    for item in out_of_range:
        print(f"  {item['number']}番 {item['name']} [Tier {item['tier']}]: {item['length']}文字 (目標: {item['min']}-{item['max']})")
print("=" * 80)
