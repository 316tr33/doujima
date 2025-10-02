#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 1A検証スクリプト: 構造修正が100点満点か確認
- 88箇所すべてに標準コメントマーカーがあるか
- 88箇所すべてに正しい県別クラスがあるか
- special-temple設定が正しいか（1, 21, 51, 75, 88番）
- birthplace-temple設定が正しいか（75番）
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
print("お遍路英語版 Phase 1A検証: 構造修正100点満点チェック")
print("=" * 80)

# 県別の範囲定義
prefecture_ranges = {
    'tokushima': (1, 23),
    'kouchi': (24, 39),
    'ehime': (40, 65),
    'kagawa': (66, 88)
}

def get_expected_prefecture(number):
    for pref, (start, end) in prefecture_ranges.items():
        if start <= number <= end:
            return pref
    return None

# 特別な寺院の設定
special_temples = {1, 21, 51, 75, 88}
birthplace_temple = 75

# 検証カウンター
all_ok = True
errors = []

# Test 1: コメントマーカーの存在確認（88箇所）
print("\n【Test 1: コメントマーカー確認】")
comment_pattern = r'<!-- (\d+)番 (.+?) -->'
en_comments = re.findall(comment_pattern, en_html)

if len(en_comments) == 88:
    print(f"✓ コメントマーカー数: {len(en_comments)}箇所（期待値: 88箇所）")
else:
    print(f"✗ コメントマーカー数: {len(en_comments)}箇所（期待値: 88箇所）")
    all_ok = False
    errors.append(f"コメントマーカーが{88 - len(en_comments)}箇所不足")

# 番号の連続性確認
comment_numbers = sorted([int(num) for num, _ in en_comments])
expected_numbers = list(range(1, 89))
if comment_numbers == expected_numbers:
    print("✓ コメント番号の連続性: OK（1番〜88番）")
else:
    missing = set(expected_numbers) - set(comment_numbers)
    print(f"✗ コメント番号に欠番: {missing}")
    all_ok = False
    errors.append(f"コメント番号に欠番あり: {missing}")

# Test 2: カードクラスの確認（88箇所）
print("\n【Test 2: カードクラス確認】")
card_pattern = r'<!-- (\d+)番 .+? -->\s*<div class="card ([^"]+)"'
en_cards = re.findall(card_pattern, en_html)

if len(en_cards) == 88:
    print(f"✓ カード数: {len(en_cards)}箇所（期待値: 88箇所）")
else:
    print(f"✗ カード数: {len(en_cards)}箇所（期待値: 88箇所）")
    all_ok = False
    errors.append(f"カードが{88 - len(en_cards)}箇所不足")

# 各カードの県別クラス確認
pref_errors = []
for number, classes in en_cards:
    num = int(number)
    expected_pref = get_expected_prefecture(num)

    if expected_pref not in classes:
        pref_errors.append(f"{num}番: {expected_pref}クラスなし（現在: {classes}）")

if not pref_errors:
    print("✓ 県別クラス: すべて正しく設定されています")
else:
    print(f"✗ 県別クラスエラー: {len(pref_errors)}箇所")
    for error in pref_errors[:5]:  # 最初の5件のみ表示
        print(f"  {error}")
    if len(pref_errors) > 5:
        print(f"  ... 他{len(pref_errors) - 5}件")
    all_ok = False
    errors.extend(pref_errors)

# Test 3: special-temple設定確認（1, 21, 51, 75, 88番）
print("\n【Test 3: special-temple設定確認】")
special_errors = []
for number, classes in en_cards:
    num = int(number)
    has_special = 'special-temple' in classes
    should_have_special = num in special_temples

    if should_have_special and not has_special:
        special_errors.append(f"{num}番: special-templeクラスなし")
    elif not should_have_special and has_special:
        special_errors.append(f"{num}番: 不要なspecial-templeクラスあり")

if not special_errors:
    print(f"✓ special-temple設定: 5箇所正しく設定（{special_temples}）")
else:
    print(f"✗ special-temple設定エラー: {len(special_errors)}箇所")
    for error in special_errors:
        print(f"  {error}")
    all_ok = False
    errors.extend(special_errors)

# Test 4: birthplace-temple設定確認（75番のみ）
print("\n【Test 4: birthplace-temple設定確認】")
birthplace_ok = False
for number, classes in en_cards:
    if int(number) == birthplace_temple:
        if 'birthplace-temple' in classes:
            print(f"✓ birthplace-temple設定: 75番に正しく設定")
            birthplace_ok = True
        else:
            print(f"✗ 75番にbirthplace-templeクラスなし（現在: {classes}）")
            all_ok = False
            errors.append("75番にbirthplace-templeクラスなし")
        break

if not birthplace_ok and all_ok:
    print("✗ 75番のカードが見つかりません")
    all_ok = False
    errors.append("75番のカードが見つかりません")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 1A検証結果: 100点満点！すべてのチェックに合格しました")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 1A検証結果: {len(errors)}件のエラーが見つかりました")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors[:10], 1):
        print(f"{i}. {error}")
    if len(errors) > 10:
        print(f"... 他{len(errors) - 10}件")
    print("=" * 80)
    exit(1)
