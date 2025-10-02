#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<main>タグ構造検証スクリプト
開始タグと閉じタグの数が一致しているか確認
"""

import re
from pathlib import Path

def verify_main_tags(file_path):
    """HTMLファイルの<main>タグの対応を検証"""
    html = file_path.read_text(encoding='utf-8')

    # <main>の開始タグと閉じタグを検索
    opening_tags = re.findall(r'<main[^>]*>', html)
    closing_tags = re.findall(r'</main>', html)

    print(f"\n=== {file_path.name} ===")
    print(f"<main> 開始タグ: {len(opening_tags)}個")
    print(f"</main> 閉じタグ: {len(closing_tags)}個")

    if len(opening_tags) == len(closing_tags):
        print(f"✓ タグの数が一致しています（{len(opening_tags)}組）")
        return True
    else:
        print(f"✗ タグの数が不一致です（開始: {len(opening_tags)}, 閉じ: {len(closing_tags)}）")
        return False

# ファイルパス
en_html = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
ja_html = Path(__file__).parent.parent / "Ohenro/shikoku.html"

print("=" * 80)
print("<main>タグ構造検証")
print("=" * 80)

# 検証実行
en_ok = verify_main_tags(en_html)
ja_ok = verify_main_tags(ja_html)

print("\n" + "=" * 80)
if en_ok and ja_ok:
    print("🎉 すべてのファイルで<main>タグの構造が正しいです")
    print("=" * 80)
    exit(0)
else:
    print("❌ <main>タグの構造に問題があります")
    print("=" * 80)
    exit(1)
