#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3B検証スクリプト: 電話番号の国際形式化確認
すべての電話番号が国際形式（+81-xx-xxx-xxxx）になっているか検証
"""

import re
from pathlib import Path

en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3B検証: 電話番号国際形式100点満点チェック")
print("=" * 80)

# 検証
all_ok = True
errors = []

# Test 1: 国際形式の電話番号の数を確認
print("\n【Test 1: 国際形式電話番号の数確認】")
international_phones = re.findall(r'<p class="card-small-text">Tel: \+81-\d{1,4}-\d{1,4}-\d{4}</p>', en_html)
if len(international_phones) == 88:
    print(f"✓ 国際形式電話番号: 88箇所（完全）")
else:
    print(f"✗ 国際形式電話番号: {len(international_phones)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append(f"国際形式不足: {len(international_phones)}箇所")

# Test 2: 日本国内形式（0xx-）が残っていないか確認
print("\n【Test 2: 旧形式の電話番号確認】")
domestic_phones = re.findall(r'<p class="card-small-text">電話: 0\d{1,4}-\d{1,4}-\d{4}</p>', en_html)
if len(domestic_phones) == 0:
    print(f"✓ 旧形式の電話番号: 0件（すべて変換済み）")
else:
    print(f"✗ 旧形式が残っている: {len(domestic_phones)}箇所")
    for phone in domestic_phones[:3]:
        print(f"  {phone}")
    if len(domestic_phones) > 3:
        print(f"  ... 他{len(domestic_phones) - 3}件")
    all_ok = False
    errors.extend(domestic_phones)

# Test 3: ラベルが「Tel:」に変更されているか確認
print("\n【Test 3: ラベル確認】")
tel_labels = re.findall(r'<p class="card-small-text">Tel:', en_html)
phone_labels = re.findall(r'<p class="card-small-text">電話:', en_html)

if len(tel_labels) == 88 and len(phone_labels) == 0:
    print(f"✓ ラベル: すべて「Tel:」に統一（88箇所）")
else:
    print(f"✗ ラベル不統一: Tel={len(tel_labels)}, 電話={len(phone_labels)}")
    all_ok = False
    errors.append(f"ラベル不統一: Tel={len(tel_labels)}, 電話={len(phone_labels)}")

# Test 4: サンプル電話番号の確認
print("\n【Test 4: サンプル電話番号確認】")
sample_checks = {
    1: '+81-88-689-1111',
    23: '+81-88-477-0023',
    75: '+81-877-62-0111',
    88: '+81-879-56-2278'
}

for num, expected_phone in sample_checks.items():
    pattern = rf'<h3>Temple No\.{num} .*?</h3>.*?<p class="card-small-text">Tel: ([^<]+)</p>'
    match = re.search(pattern, en_html, re.DOTALL)
    if match:
        actual_phone = match.group(1)
        if actual_phone == expected_phone:
            print(f"✓ {num}番: {actual_phone}")
        else:
            print(f"✗ {num}番: 期待={expected_phone}, 実際={actual_phone}")
            all_ok = False
            errors.append(f"{num}番の電話番号不一致")
    else:
        print(f"✗ {num}番: 電話番号が見つかりません")
        all_ok = False
        errors.append(f"{num}番の電話番号なし")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 3B検証結果: 100点満点！すべてのチェックに合格しました")
    print("📊 88箇所すべて国際形式（+81-xx-xxx-xxxx）に変換完了")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 3B検証結果: {len(errors)}件のエラーが見つかりました")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors[:5], 1):
        print(f"{i}. {error}")
    if len(errors) > 5:
        print(f"... 他{len(errors) - 5}件")
    print("=" * 80)
    exit(1)
