#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.9 英語表現の修正スクリプト
日本語ローマ字表現を適切な英語に修正
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.9: 英語表現の修正")
print("=" * 80)

changes = {
    'shuuhen': 0,
    'jikan': 0,
    'other_jp': 0
}

print("\n【1. 'shuuhen'（周辺）を英語に修正】")

# "shuuhen" を "area" に置換
old_count = en_html.count('shuuhen')
old_count_cap = en_html.count('Shuuhen')

en_html = en_html.replace('shuuhen', ' area')
en_html = en_html.replace('Shuuhen', ' area')

changes['shuuhen'] = old_count + old_count_cap
print(f"  {changes['shuuhen']}箇所を修正: shuuhen → area")

print("\n【2. '時間'を'hours'に修正】")

# "見学時間：" → "Visit Time: "
en_html = en_html.replace('見学時間：', 'Visit Time: ')
print("  見学時間ラベルを英語化")

# "0.5–1時間" → "0.5–1 hours" など
time_pattern = r'(\d+(?:\.\d+)?(?:–|~|-)\d+(?:\.\d+)?)時間'
matches = re.findall(time_pattern, en_html)
changes['jikan'] = len(matches)

en_html = re.sub(time_pattern, r'\1 hours', en_html)
print(f"  {changes['jikan']}箇所を修正: XX時間 → XX hours")

print("\n【3. その他の日本語表現を英語に修正】")

# 正規表現を使って単語境界を考慮した置換
# 接尾辞として使われる場合のみ置換（大文字で始まる前に付く場合）

# パターン1: 大文字の前の接尾辞（例: "KitaMachi" → "Kita Town"）
suffix_patterns = [
    (r'([A-Z][a-z]+)Machi\b', r'\1 Town'),  # XxxMachi → Xxx Town
    (r'([A-Z][a-z]+)Chou\b', r'\1 Town'),   # XxxChou → Xxx Town
    (r'([A-Z][a-z]+)Gun\b', r'\1 District'),  # XxxGun → Xxx District

    # その他の接尾辞
    (r'\bIttai\b', 'Area'),
    (r'\bNado\b', 'etc.'),
    (r'\bRiyou\b', 'use'),
    (r'\bBasu\b', 'Bus'),
    (r'\bTakushii\b', 'Taxi'),
]

for pattern, replacement in suffix_patterns:
    matches = re.findall(pattern, en_html)
    if matches:
        en_html = re.sub(pattern, replacement, en_html)
        changes['other_jp'] += len(matches)
        print(f"  {pattern} → {replacement} ({len(matches)}箇所)")

print(f"\n  合計: {changes['other_jp']}箇所を修正")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.9 英語表現修正完了")
print(f"   周辺(shuuhen): {changes['shuuhen']}箇所 → area")
print(f"   時間(jikan): {changes['jikan']}箇所 → hours")
print(f"   その他の日本語: {changes['other_jp']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
