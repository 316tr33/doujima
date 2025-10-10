#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.11 時間単位の文法修正スクリプト
0.5-1 hours → 0.5-1 hour (最大値が1以下の場合は単数形)
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.11: 時間単位の文法修正")
print("=" * 80)

changes = 0

print("\n【時間範囲の単数・複数形修正】")

# パターン1: 0.5–1 hours → 0.5–1 hour (最大値1 = 単数)
pattern1 = r'0\.5[–~-]1 hours'
matches1 = re.findall(pattern1, en_html)
if matches1:
    en_html = re.sub(pattern1, '0.5–1 hour', en_html)
    changes += len(matches1)
    print(f"  0.5–1 hours → 0.5–1 hour ({len(matches1)}箇所)")

# パターン2: 0.5 hours → 0.5 hour (0.5 = 単数)
pattern2 = r'\b0\.5 hours\b'
matches2 = re.findall(pattern2, en_html)
if matches2:
    en_html = re.sub(pattern2, '0.5 hour', en_html)
    changes += len(matches2)
    print(f"  0.5 hours → 0.5 hour ({len(matches2)}箇所)")

# パターン3: 1 hours → 1 hour (1 = 単数)
pattern3 = r'\b1 hours\b'
matches3 = re.findall(pattern3, en_html)
if matches3:
    en_html = re.sub(pattern3, '1 hour', en_html)
    changes += len(matches3)
    print(f"  1 hours → 1 hour ({len(matches3)}箇所)")

# パターン4: X–1 hours → X–1 hour (最大値1 = 単数)
pattern4 = r'(\d+(?:\.\d+)?)[–~-]1 hours'
matches4 = re.findall(pattern4, en_html)
if matches4:
    en_html = re.sub(pattern4, r'\1–1 hour', en_html)
    changes += len(matches4)
    print(f"  X–1 hours → X–1 hour ({len(matches4)}箇所)")

print(f"\n  合計修正: {changes}箇所")

# 確認: 複数形が必要なパターンをリストアップ
print("\n【複数形を維持するパターン（参考）】")
plural_patterns = [
    r'1\.5[–~-]\d+ hours',  # 1.5–2 hours など
    r'2[–~-]\d+ hours',     # 2–3 hours など
    r'\d+\.\d+ hours',      # 2.5 hours など（1.5以上）
]

for pattern in plural_patterns:
    matches = re.findall(pattern, en_html)
    if matches:
        print(f"  {pattern}: {len(matches)}箇所（正しく複数形）")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.11 時間単位文法修正完了")
print(f"   修正箇所: {changes}箇所")
print(f"   更新ファイル: {en_html_path}")
print("\n【英文法ルール】")
print("  - 0.5 = 単数形（0.5 hour）")
print("  - 1 = 単数形（1 hour）")
print("  - 1.5以上 = 複数形（1.5 hours, 2 hours）")
print("  - 範囲表記 = 最大値で判断（0.5–1 hour, 1–2 hours）")
print("=" * 80)
