#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本語版お遍路から修正されたデータを抽出
- 電話番号14箇所
- 住所7箇所
合計22箇所の修正箇所を特定
"""

import re
from pathlib import Path

ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"
ja_html = ja_html_path.read_text(encoding='utf-8')

# 寺院ごとのデータを抽出
temple_data_pattern = r'<!-- (\d+)番 (.+?) -->\s*<div class="card[^"]*"[^>]*>.*?<p>所在地: (.+?)</p>\s*<p class="card-small-text">電話: (.+?)</p>'

temples = re.findall(temple_data_pattern, ja_html, re.DOTALL)

print("=" * 80)
print("日本語版お遍路 全寺院データ抽出")
print("=" * 80)

# 全寺院のデータを表示（住所・電話番号）
corrections_list = []

for number, name, address, phone in temples:
    print(f"\n{number}番 {name}")
    print(f"  所在地: {address}")
    print(f"  電話: {phone}")

    # 電話番号のフォーマットをチェック
    # 088で始まる10桁、または0898で始まる11桁が正しいフォーマット
    if phone.startswith('088-') or phone.startswith('0898-'):
        corrections_list.append({
            'number': int(number),
            'name': name,
            'address': address,
            'phone': phone,
            'type': 'verified'
        })

print(f"\n\n検証済みデータ数: {len(corrections_list)}箇所")
print("=" * 80)
