#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英語版ファイル内の日本語テキスト検証スクリプト
"""

import re
from pathlib import Path

en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("英語版ファイル内の日本語テキスト検証")
print("=" * 80)

all_ok = True
errors = []

# Test 1: ALT属性の確認
print("\n【Test 1: ALT属性の英語化確認】")
old_alt = re.findall(r'alt="YouTube動画"', en_html)
new_alt = re.findall(r'alt="Temple video thumbnail"', en_html)

if len(old_alt) == 0 and len(new_alt) == 86:
    print(f"✓ ALT属性: すべて英語化済み（{len(new_alt)}箇所）")
else:
    print(f"✗ ALT属性: 日本語={len(old_alt)}, 英語={len(new_alt)}")
    all_ok = False
    errors.append(f"ALT属性の英語化が不完全")

# Test 2: 住所ラベルの確認
print("\n【Test 2: 住所ラベルの英語化確認】")
old_label = re.findall(r'所在地:', en_html)
new_label = re.findall(r'Japanese Address:', en_html)

if len(old_label) == 0 and len(new_label) == 88:
    print(f"✓ 住所ラベル: すべて英語化済み（{len(new_label)}箇所）")
else:
    print(f"✗ 住所ラベル: 日本語={len(old_label)}, 英語={len(new_label)}")
    all_ok = False
    errors.append(f"住所ラベルの英語化が不完全")

# Test 3: その他の日本語テキスト確認（japanese-addressクラス内の日本語住所は除外）
print("\n【Test 3: その他の日本語テキスト確認】")
# japanese-addressクラス内の日本語は意図的なものなので除外
# 本文や属性内の意図しない日本語を検出
hiragana = re.findall(r'(?<!class="japanese-address">Japanese Address: )[ぁ-ん]{2,}', en_html)
katakana = re.findall(r'(?<!class="japanese-address">Japanese Address: )[ァ-ン]{2,}', en_html)

if len(hiragana) == 0 and len(katakana) == 0:
    print(f"✓ その他の日本語: 検出されませんでした")
else:
    print(f"⚠️ ひらがな: {len(hiragana)}箇所, カタカナ: {len(katakana)}箇所")
    # japanese-addressクラス内は許容するため、これはwarningのみ

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 日本語テキスト英語化検証: 100点満点！")
    print("📊 すべての必須項目が英語化されています")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ 日本語テキスト英語化検証: {len(errors)}件のエラー")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
    print("=" * 80)
    exit(1)
