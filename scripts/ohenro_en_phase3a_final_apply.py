#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3A最終版適用スクリプト: 正確な英語住所への置換
完全なローマ字形式の英語住所データベースを使用
"""

import re
import sys
from pathlib import Path

# 英語住所データベースをインポート
sys.path.insert(0, str(Path(__file__).parent))
from temple_addresses_en import TEMPLE_ADDRESSES_EN

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3A最終版: 正確な英語住所への置換")
print("=" * 80)

# 英語版HTMLを更新
modified_html = en_html
update_count = 0

for num in range(1, 89):
    if num not in TEMPLE_ADDRESSES_EN:
        print(f"警告: {num}番の英語住所データがありません")
        continue

    english_addr = TEMPLE_ADDRESSES_EN[num]

    # 現在の英語住所を正確な英語住所に置き換え
    # パターン: <p class="english-address">Address: ...</p>
    # 75番は temple-significance がある特殊ケース
    if num == 75:
        pattern = r'(<h3>Temple No\.75 [^<]+<span[^>]*>.*?</span></h3>\s*<p class="temple-significance">[^<]+</p>)\s*<p class="english-address">Address: [^<]+</p>'
    else:
        pattern = rf'(<h3>Temple No\.{num} [^<]+(?:<span[^>]*>.*?</span>)?</h3>)\s*<p class="english-address">Address: [^<]+</p>'

    replacement = rf'\1\n              <p class="english-address">Address: {english_addr}</p>'

    if re.search(pattern, modified_html, re.DOTALL):
        modified_html = re.sub(pattern, replacement, modified_html, count=1, flags=re.DOTALL)
        update_count += 1
        print(f"✓ {num}番: {english_addr}")
    else:
        print(f"✗ {num}番: パターンマッチせず")

print(f"\n更新した住所: {update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 3A最終版適用完了: {en_html_path}")

print("\n【修正サマリー】")
print(f"✓ 正確な英語住所: {update_count}箇所")
print(f"  - 形式: 番地 + 町名（正確なローマ字） + 市区町村 + 都道府県 + 郵便番号")
print("=" * 80)
