#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 1B検証スクリプト: データ修正が100点満点か確認
日本語版と英語版の住所・電話番号が完全に一致するか検証
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
print("お遍路英語版 Phase 1B検証: データ修正100点満点チェック")
print("=" * 80)

# 日本語版と英語版から各寺院の住所・電話番号を抽出
pattern = r'<!-- (\d+)番 (.+?) -->\s*<div class="card[^"]*"[^>]*>.*?<p>所在地: (.+?)</p>\s*<p class="card-small-text">電話: (.+?)</p>'

ja_temples = re.findall(pattern, ja_html, re.DOTALL)
en_temples = re.findall(pattern, en_html, re.DOTALL)

# 辞書化
ja_data = {}
for number, name, address, phone in ja_temples:
    ja_data[int(number)] = {
        'address': address.strip(),
        'phone': phone.strip()
    }

en_data = {}
for number, name, address, phone in en_temples:
    en_data[int(number)] = {
        'address': address.strip(),
        'phone': phone.strip()
    }

print(f"\n日本語版データ数: {len(ja_data)}箇所")
print(f"英語版データ数: {len(en_data)}箇所")

# 検証
all_ok = True
errors = []

# Test 1: データ数の一致確認
print("\n【Test 1: データ数確認】")
if len(ja_data) == len(en_data) == 88:
    print("✓ データ数: 88箇所（両方とも完全）")
else:
    print(f"✗ データ数不一致: 日本語版{len(ja_data)}箇所、英語版{len(en_data)}箇所")
    all_ok = False
    errors.append(f"データ数不一致")

# Test 2: 各寺院のデータが完全一致するか
print("\n【Test 2: 住所・電話番号の完全一致確認】")
address_errors = []
phone_errors = []

for number in range(1, 89):
    if number not in ja_data or number not in en_data:
        errors.append(f"{number}番: データが見つかりません")
        all_ok = False
        continue

    ja_addr = ja_data[number]['address']
    en_addr = en_data[number]['address']
    ja_phone = ja_data[number]['phone']
    en_phone = en_data[number]['phone']

    # 住所の比較
    if ja_addr != en_addr:
        address_errors.append(f"{number}番: 住所不一致\n  日本語版: {ja_addr}\n  英語版: {en_addr}")

    # 電話番号の比較
    if ja_phone != en_phone:
        phone_errors.append(f"{number}番: 電話番号不一致\n  日本語版: {ja_phone}\n  英語版: {en_phone}")

# 住所の検証結果
if not address_errors:
    print("✓ 住所: 88箇所すべて一致")
else:
    print(f"✗ 住所エラー: {len(address_errors)}箇所")
    for error in address_errors[:3]:  # 最初の3件のみ表示
        print(f"  {error}")
    if len(address_errors) > 3:
        print(f"  ... 他{len(address_errors) - 3}件")
    all_ok = False
    errors.extend(address_errors)

# 電話番号の検証結果
if not phone_errors:
    print("✓ 電話番号: 88箇所すべて一致")
else:
    print(f"✗ 電話番号エラー: {len(phone_errors)}箇所")
    for error in phone_errors[:3]:  # 最初の3件のみ表示
        print(f"  {error}")
    if len(phone_errors) > 3:
        print(f"  ... 他{len(phone_errors) - 3}件")
    all_ok = False
    errors.extend(phone_errors)

# Test 3: 特定の修正箇所の確認（Phase 2で修正された22箇所）
print("\n【Test 3: Phase 2修正箇所の確認】")
critical_checks = {
    23: {'address': '徳島県海部郡美波町奥河内寺前285-1', 'phone': '088-477-0023'},
    36: {'address': '高知県土佐市宇佐町竜163', 'phone': '088-856-3010'},
    40: {'address': '愛媛県宇和郡愛南町御荘平城2253-1', 'phone': '0895-72-0416'},
    57: {'address': '愛媛県今治市玉川町八幡甲200', 'phone': '0898-55-2432'},
    58: {'address': '愛媛県今治市玉川町別所甲483', 'phone': '0898-55-2141'},
    66: {'address': '徳島県三好市池田町白地ノロウチ763-2', 'phone': '0883-74-1707'}
}

critical_ok = True
for number, expected in critical_checks.items():
    if number in en_data:
        actual = en_data[number]
        if actual['address'] == expected['address'] and actual['phone'] == expected['phone']:
            print(f"✓ {number}番: 正しく修正されています")
        else:
            print(f"✗ {number}番: 期待値と異なります")
            print(f"  期待: {expected['address']} / {expected['phone']}")
            print(f"  実際: {actual['address']} / {actual['phone']}")
            critical_ok = False
            all_ok = False

if critical_ok:
    print("\n✓ 重要修正箇所: すべて正しく適用されています")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 1B検証結果: 100点満点！すべてのチェックに合格しました")
    print("📊 日本語版と英語版のデータが完全に一致しています")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 1B検証結果: {len(errors)}件のエラーが見つかりました")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors[:5], 1):
        print(f"{i}. {error}")
    if len(errors) > 5:
        print(f"... 他{len(errors) - 5}件")
    print("=" * 80)
    exit(1)
