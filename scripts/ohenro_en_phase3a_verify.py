#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3A検証スクリプト: 住所のハイブリッド表示確認
英語住所と日本語住所の両方が正しく表示されているか検証
"""

import re
from pathlib import Path

en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3A検証: 住所ハイブリッド表示100点満点チェック")
print("=" * 80)

# 検証
all_ok = True
errors = []

# Test 1: 英語住所の数を確認
print("\n【Test 1: 英語住所の数確認】")
english_addresses = re.findall(r'<p class="english-address">Address: ([^<]+)</p>', en_html)
if len(english_addresses) == 88:
    print(f"✓ 英語住所: 88箇所（完全）")
else:
    print(f"✗ 英語住所: {len(english_addresses)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append(f"英語住所不足: {len(english_addresses)}箇所")

# Test 2: 日本語住所の数を確認
print("\n【Test 2: 日本語住所の数確認】")
japanese_addresses = re.findall(r'<p class="japanese-address">所在地: ([^<]+)</p>', en_html)
if len(japanese_addresses) == 88:
    print(f"✓ 日本語住所: 88箇所（完全）")
else:
    print(f"✗ 日本語住所: {len(japanese_addresses)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append(f"日本語住所不足: {len(japanese_addresses)}箇所")

# Test 3: 各寺院に英語住所と日本語住所の両方があるか確認
print("\n【Test 3: ハイブリッド表示確認】")
temple_pattern = r'<h3>Temple No\.(\d+) [^<]+(?:<span[^>]*>.*?</span>)?</h3>'
temples = re.findall(temple_pattern, en_html)

missing_temples = []
for temple_num in temples:
    num = int(temple_num)
    # 各寺院の範囲を抽出
    temple_section_pattern = rf'<h3>Temple No\.{num} [^<]+(?:<span[^>]*>.*?</span>)?</h3>.*?(?=<h3>Temple No\.\d+|<!-- \d+番|</div>\s*</div>\s*<!-- )'
    section_match = re.search(temple_section_pattern, en_html, re.DOTALL)

    if section_match:
        section = section_match.group(0)
        has_english = 'class="english-address"' in section
        has_japanese = 'class="japanese-address"' in section

        if not (has_english and has_japanese):
            missing_temples.append(f"{num}番: 英語={has_english}, 日本語={has_japanese}")

if not missing_temples:
    print(f"✓ ハイブリッド表示: 88箇所すべて英語・日本語両方あり")
else:
    print(f"✗ ハイブリッド表示不完全: {len(missing_temples)}箇所")
    for temple in missing_temples[:5]:
        print(f"  {temple}")
    if len(missing_temples) > 5:
        print(f"  ... 他{len(missing_temples) - 5}件")
    all_ok = False
    errors.extend(missing_temples)

# Test 4: 特別な寺院（75番）の確認
print("\n【Test 4: 75番善通寺の特別要素確認】")
temple_75_pattern = r'<h3>Temple No\.75 Zentsuji.*?</h3>.*?<p class="temple-significance">([^<]+)</p>.*?<p class="english-address">Address: ([^<]+)</p>.*?<p class="japanese-address">所在地: ([^<]+)</p>'
temple_75_match = re.search(temple_75_pattern, en_html, re.DOTALL)

if temple_75_match:
    significance = temple_75_match.group(1)
    english_addr = temple_75_match.group(2)
    japanese_addr = temple_75_match.group(3)
    print(f"✓ 75番: 特別説明文あり")
    print(f"✓ 75番: 英語住所あり（{english_addr}）")
    print(f"✓ 75番: 日本語住所あり")
else:
    print("✗ 75番: ハイブリッド表示が正しくありません")
    all_ok = False
    errors.append("75番のハイブリッド表示不備")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 3A検証結果: 100点満点！すべてのチェックに合格しました")
    print("📊 88箇所すべて英語住所と日本語住所のハイブリッド表示")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 3A検証結果: {len(errors)}件のエラーが見つかりました")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors[:5], 1):
        print(f"{i}. {error}")
    if len(errors) > 5:
        print(f"... 他{len(errors) - 5}件")
    print("=" * 80)
    exit(1)
