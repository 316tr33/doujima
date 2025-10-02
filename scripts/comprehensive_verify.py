#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 包括的検証スクリプト
すべてのフェーズの実装を検証
"""

import re
from pathlib import Path

en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"

en_html = en_html_path.read_text(encoding='utf-8')
ja_html = ja_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 包括的検証")
print("=" * 80)

all_ok = True
errors = []

# Test 1: HTMLタグ構造
print("\n【Test 1: HTMLタグ構造】")
en_main_open = len(re.findall(r'<main[^>]*>', en_html))
en_main_close = len(re.findall(r'</main>', en_html))
ja_main_open = len(re.findall(r'<main[^>]*>', ja_html))
ja_main_close = len(re.findall(r'</main>', ja_html))

if en_main_open == en_main_close == ja_main_open == ja_main_close == 4:
    print(f"✓ <main>タグ: 英語版{en_main_open}組、日本語版{ja_main_open}組（正常）")
else:
    print(f"✗ <main>タグ: 英語版 開{en_main_open}/閉{en_main_close}, 日本語版 開{ja_main_open}/閉{ja_main_close}")
    all_ok = False
    errors.append("<main>タグ構造エラー")

# Test 2: 寺院数確認
print("\n【Test 2: 寺院数確認】")
en_cards = len(re.findall(r'<div class="card ', en_html))
ja_cards = len(re.findall(r'<div class="card ', ja_html))

if en_cards == ja_cards == 88:
    print(f"✓ 寺院カード数: {en_cards}箇所（両方完全）")
else:
    print(f"✗ 寺院カード数: 英語版{en_cards}箇所、日本語版{ja_cards}箇所")
    all_ok = False
    errors.append(f"寺院カード数不一致")

# Test 3: 寺院名の英語化
print("\n【Test 3: 寺院名の英語化】")
en_temple_names = re.findall(r'<h3>Temple No\.\d+ [A-Za-z\-]+(?:<span[^>]*>.*?</span>)?</h3>', en_html)
if len(en_temple_names) == 88:
    print(f"✓ 英語寺院名: {len(en_temple_names)}箇所（完全）")
else:
    print(f"✗ 英語寺院名: {len(en_temple_names)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append("寺院名英語化不完全")

# Test 4: 英語住所
print("\n【Test 4: 英語住所】")
en_addresses = re.findall(r'<p class="english-address">Address: .+?</p>', en_html)
if len(en_addresses) == 88:
    print(f"✓ 英語住所: {len(en_addresses)}箇所（完全）")
else:
    print(f"✗ 英語住所: {len(en_addresses)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append("英語住所不完全")

# Test 5: 日本語住所
print("\n【Test 5: 日本語住所】")
ja_addresses_en = re.findall(r'<p class="japanese-address">Japanese Address: .+?</p>', en_html)
if len(ja_addresses_en) == 88:
    print(f"✓ 日本語住所: {len(ja_addresses_en)}箇所（完全）")
else:
    print(f"✗ 日本語住所: {len(ja_addresses_en)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append("日本語住所不完全")

# Test 6: 国際電話番号
print("\n【Test 6: 国際電話番号】")
international_phones = re.findall(r'<p class="card-small-text">Tel: \+81-\d{1,4}-\d{1,4}-\d{4}</p>', en_html)
if len(international_phones) == 88:
    print(f"✓ 国際電話番号: {len(international_phones)}箇所（完全）")
else:
    print(f"✗ 国際電話番号: {len(international_phones)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append("国際電話番号不完全")

# Test 7: ALT属性の英語化
print("\n【Test 7: ALT属性の英語化】")
old_alt = len(re.findall(r'alt="YouTube動画"', en_html))
new_alt = len(re.findall(r'alt="Temple video thumbnail"', en_html))
if old_alt == 0 and new_alt > 0:
    print(f"✓ ALT属性: すべて英語化済み（{new_alt}箇所）")
else:
    print(f"✗ ALT属性: 日本語={old_alt}, 英語={new_alt}")
    all_ok = False
    errors.append("ALT属性の英語化不完全")

# Test 8: 県別クラス設定
print("\n【Test 8: 県別クラス設定】")
tokushima = len(re.findall(r'<div class="card tokushima', en_html))
kouchi = len(re.findall(r'<div class="card kouchi', en_html))
ehime = len(re.findall(r'<div class="card ehime', en_html))
kagawa = len(re.findall(r'<div class="card kagawa', en_html))

if tokushima == 23 and kouchi == 16 and ehime == 26 and kagawa == 23:
    print(f"✓ 県別クラス: 徳島{tokushima}, 高知{kouchi}, 愛媛{ehime}, 香川{kagawa}")
else:
    print(f"✗ 県別クラス: 徳島{tokushima}, 高知{kouchi}, 愛媛{ehime}, 香川{kagawa}")
    all_ok = False
    errors.append("県別クラス設定エラー")

# Test 9: 特別寺院設定
print("\n【Test 9: 特別寺院設定】")
special_temples = len(re.findall(r'<div class="card [a-z]+ special-temple', en_html))
if special_temples == 5:
    print(f"✓ 特別寺院: {special_temples}箇所（1, 21, 51, 75, 88番）")
else:
    print(f"✗ 特別寺院: {special_temples}箇所（期待: 5箇所）")
    all_ok = False
    errors.append("特別寺院設定エラー")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 包括的検証: 100点満点！")
    print("📊 すべてのフェーズの実装が正常に完了しています")
    print("\n【完了フェーズ】")
    print("  ✓ Phase 1A: 構造修正（コメント、クラス、特別寺院）")
    print("  ✓ Phase 1B: データ修正（住所、電話番号）")
    print("  ✓ Phase 2: 寺院名の英語化")
    print("  ✓ Phase 3A: 英語住所の実装（詳細版）")
    print("  ✓ Phase 3B: 国際電話番号の実装")
    print("  ✓ Additional: 日本語テキストの英語化（ALT、ラベル）")
    print("  ✓ Additional: HTMLタグ構造の修正")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ 包括的検証: {len(errors)}件のエラー")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
    print("=" * 80)
    exit(1)
