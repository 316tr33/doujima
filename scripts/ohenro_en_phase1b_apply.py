#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 1B適用スクリプト: データ修正を適用
日本語版の住所・電話番号を英語版に適用
"""

import re
from pathlib import Path

# ファイルパス
ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"

# 日本語版と英語版を読み込み
ja_html = ja_html_path.read_text(encoding='utf-8')
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 1B: データ修正適用")
print("=" * 80)

# 日本語版から各寺院の住所・電話番号を抽出
ja_pattern = r'<!-- (\d+)番 (.+?) -->\s*<div class="card[^"]*"[^>]*>.*?<p>所在地: (.+?)</p>\s*<p class="card-small-text">電話: (.+?)</p>'
ja_temples = re.findall(ja_pattern, ja_html, re.DOTALL)

ja_data = {}
for number, name, address, phone in ja_temples:
    ja_data[int(number)] = {
        'name': name,
        'address': address.strip(),
        'phone': phone.strip()
    }

print(f"\n日本語版から抽出したデータ: {len(ja_data)}箇所")

# 英語版のデータを日本語版と同じに更新
modified_html = en_html
address_updates = []
phone_updates = []

for number in range(1, 89):
    if number not in ja_data:
        continue

    correct_address = ja_data[number]['address']
    correct_phone = ja_data[number]['phone']

    # 該当する番号の住所・電話番号を検索して置換
    # パターン: <!-- ○番 ... --> 以降の最初の住所と電話番号
    card_section_pattern = rf'(<!-- {number}番 .+? -->\s*<div class="card[^"]*"[^>]*>.*?<p>所在地: )(.+?)(</p>\s*<p class="card-small-text">電話: )(.+?)(</p>)'

    match = re.search(card_section_pattern, modified_html, re.DOTALL)
    if match:
        old_address = match.group(2).strip()
        old_phone = match.group(4).strip()

        address_changed = old_address != correct_address
        phone_changed = old_phone != correct_phone

        if address_changed:
            address_updates.append(f"{number}番: {old_address} → {correct_address}")
        if phone_changed:
            phone_updates.append(f"{number}番: {old_phone} → {correct_phone}")

        replacement = match.group(1) + correct_address + match.group(3) + correct_phone + match.group(5)
        modified_html = re.sub(card_section_pattern, replacement, modified_html, count=1, flags=re.DOTALL)

update_count = len(address_updates) + len(phone_updates)

print(f"\n更新した寺院数: {update_count}箇所")
print(f"  - 住所更新: {len(address_updates)}箇所")
print(f"  - 電話番号更新: {len(phone_updates)}箇所")

# 詳細な更新リスト
if address_updates:
    print("\n【住所更新詳細】")
    for update in address_updates:
        print(f"  {update}")

if phone_updates:
    print("\n【電話番号更新詳細】")
    for update in phone_updates:
        print(f"  {update}")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 1B適用完了: {en_html_path}")

# 検証用サマリー
print("\n【修正サマリー】")
print(f"✓ データ修正適用: {update_count}箇所")
print(f"  - 住所: {len(address_updates)}箇所")
print(f"  - 電話: {len(phone_updates)}箇所")
print("=" * 80)
