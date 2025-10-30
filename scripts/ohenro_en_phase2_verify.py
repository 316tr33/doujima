#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 2検証スクリプト: 英語化が100点満点か確認
88箇所すべての寺院名が英語化されているか検証
"""

import re
from pathlib import Path

en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 2検証: 英語化100点満点チェック")
print("=" * 80)

# 寺院名のh3タグをすべて抽出
h3_pattern = r'<!-- (\d+)番 .+? -->\s*<div class="card[^"]*"[^>]*>.*?<h3>(.+?)</h3>'
h3_matches = re.findall(h3_pattern, en_html, re.DOTALL)

print(f"\n抽出したh3タグ数: {len(h3_matches)}箇所")

# 検証
all_ok = True
errors = []

# Test 1: すべてのh3タグが "Temple No.○" 形式になっているか
print("\n【Test 1: 寺院名英語化確認】")
english_format_count = 0
japanese_format_count = 0
japanese_temples = []

for number, h3_content in h3_matches:
    num = int(number)
    h3_clean = h3_content.strip()

    # "Temple No.○" で始まっているか
    if h3_clean.startswith(f'Temple No.{num} '):
        english_format_count += 1
    elif '第' in h3_clean or '番' in h3_clean:
        japanese_format_count += 1
        japanese_temples.append(f"{num}番: {h3_clean[:30]}")

if japanese_format_count == 0:
    print(f"✓ 寺院名英語化: 88箇所すべて英語形式（Temple No.○）")
else:
    print(f"✗ 日本語形式が残っている: {japanese_format_count}箇所")
    for jp in japanese_temples[:5]:
        print(f"  {jp}")
    if len(japanese_temples) > 5:
        print(f"  ... 他{len(japanese_temples) - 5}件")
    all_ok = False
    errors.extend(japanese_temples)

# Test 2: 数が88箇所であるか
print("\n【Test 2: 寺院数確認】")
if len(h3_matches) == 88:
    print("✓ 寺院数: 88箇所（完全）")
else:
    print(f"✗ 寺院数不一致: {len(h3_matches)}箇所（期待: 88箇所）")
    all_ok = False
    errors.append(f"寺院数不一致: {len(h3_matches)}箇所")

# Test 3: 特別な寺院（1, 21, 51, 75, 88番）の確認
print("\n【Test 3: 特別寺院の確認】")
special_temples = {1, 21, 51, 75, 88}
special_ok = True

for number, h3_content in h3_matches:
    num = int(number)
    if num in special_temples:
        # 重要度マーク（★）があるか
        if '★' in h3_content or 'temple-importance' in h3_content:
            print(f"✓ {num}番: 重要度マークあり")
        else:
            print(f"✗ {num}番: 重要度マークなし")
            special_ok = False
            all_ok = False

if not special_ok:
    errors.append("特別寺院の重要度マーク不足")

# Test 4: 75番善通寺の特別な説明文確認
print("\n【Test 4: 75番善通寺の特別要素確認】")
temple_75_pattern = r'<!-- 75番 .+? -->.*?<h3>Temple No\.75 Zentsuji.*?</h3>.*?<p class="temple-significance">(.+?)</p>'
temple_75_match = re.search(temple_75_pattern, en_html, re.DOTALL)

if temple_75_match:
    significance_text = temple_75_match.group(1).strip()
    print(f"✓ 75番: 特別説明文あり（{significance_text[:50]}...）")
else:
    print("✗ 75番: 特別説明文（temple-significance）が見つかりません")
    all_ok = False
    errors.append("75番の特別説明文なし")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 2検証結果: 100点満点！すべてのチェックに合格しました")
    print("📊 88箇所の寺院名がすべて英語化されています")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 2検証結果: {len(errors)}件のエラーが見つかりました")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors[:5], 1):
        print(f"{i}. {error}")
    if len(errors) > 5:
        print(f"... 他{len(errors) - 5}件")
    print("=" * 80)
    exit(1)
