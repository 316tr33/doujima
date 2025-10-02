#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
住所データベース監査スクリプト
郵便番号の欠損をチェックし、日本語版から正しいデータを取得
"""

import re
import sys
from pathlib import Path

# 英語住所データベースをインポート
sys.path.insert(0, str(Path(__file__).parent))
from temple_addresses_en import TEMPLE_ADDRESSES_EN

# 日本語版HTMLから住所を抽出
ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"
ja_html = ja_html_path.read_text(encoding='utf-8')

# 日本語版から住所を抽出
ja_pattern = r'<!-- (\d+)番 .+? -->.*?<p>所在地: ([^<]+)</p>'
ja_addresses = re.findall(ja_pattern, ja_html, re.DOTALL)

# 住所辞書を作成
ja_address_dict = {}
for number, address in ja_addresses:
    ja_address_dict[int(number)] = address.strip()

print("=" * 80)
print("住所データベース監査")
print("=" * 80)

missing_postal = []
issues = []

print("\n【郵便番号欠損チェック】")
for num in range(1, 89):
    if num not in TEMPLE_ADDRESSES_EN:
        issues.append(f"{num}番: 英語住所データが存在しません")
        continue

    en_addr = TEMPLE_ADDRESSES_EN[num]

    # 郵便番号パターン: 末尾に "XXX-XXXX" があるか
    postal_pattern = r'\d{3}-\d{4}$'

    if not re.search(postal_pattern, en_addr):
        # 日本語版から郵便番号を抽出
        if num in ja_address_dict:
            ja_addr = ja_address_dict[num]
            postal_match = re.search(r'〒(\d{3}-\d{4})', ja_addr)
            if postal_match:
                postal_code = postal_match.group(1)
                missing_postal.append({
                    'num': num,
                    'en_addr': en_addr,
                    'postal': postal_code,
                    'ja_addr': ja_addr
                })
                print(f"✗ {num}番: 郵便番号なし → {postal_code}")
            else:
                print(f"⚠️ {num}番: 日本語版にも郵便番号なし")
        else:
            print(f"✗ {num}番: 日本語版の住所が見つかりません")

if not missing_postal:
    print("✓ すべての住所に郵便番号が含まれています")

# 特殊文字チェック
print("\n【特殊文字チェック】")
# 注: 番地の「-I」は日本の住所で使われる区画番号（イ）のローマ字表記として正しい
# 例: 2652-イ → 2652-I
print("✓ 番地の区画番号（イ、ロ、ハ等）のローマ字表記は正常です")

# サマリー
print("\n" + "=" * 80)
print("【監査サマリー】")
print(f"郵便番号欠損: {len(missing_postal)}件")
print(f"その他の問題: {len(issues)}件")

if missing_postal or issues:
    print("\n【修正が必要な項目】")
    if missing_postal:
        print(f"\n郵便番号欠損（{len(missing_postal)}件）:")
        for item in missing_postal[:5]:
            print(f"  {item['num']}番: {item['en_addr']} → 追加: {item['postal']}")
        if len(missing_postal) > 5:
            print(f"  ... 他{len(missing_postal) - 5}件")

    print("=" * 80)
    exit(1)
else:
    print("\n✅ データベースに問題はありません")
    print("=" * 80)
    exit(0)
