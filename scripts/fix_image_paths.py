#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版: 画像パス修正スクリプト
../images/ → ../../images/ に変更
"""

from pathlib import Path
import re

en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版: 画像パス修正")
print("=" * 80)

# ../images/ → ../../images/ に置換
old_path = '../images/'
new_path = '../../images/'

# 置換前の数を数える
old_count = en_html.count(old_path)
print(f"\n修正対象: {old_count}箇所")

# 置換実行
updated_html = en_html.replace(old_path, new_path)

# 置換後の確認
new_count = updated_html.count(new_path)
remaining_old = updated_html.count(old_path)

print(f"修正後: {new_path} が {new_count}箇所")
print(f"残存: {old_path} が {remaining_old}箇所")

# ファイルに書き込み
en_html_path.write_text(updated_html, encoding='utf-8')

print("\n" + "=" * 80)
if remaining_old == 0 and new_count == old_count:
    print("✅ 画像パス修正完了")
    print(f"   すべてのパスを {new_path} に変更しました")
else:
    print("⚠️ 一部のパスが修正されていない可能性があります")
print("=" * 80)
