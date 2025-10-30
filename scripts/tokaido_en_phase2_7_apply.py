#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.7 駅名ハイブリッド化スクリプト
お遍路方式の2行表示（英語駅名 + 日本語駅名）に変更
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.7: 駅名ハイブリッド化")
print("=" * 80)

# 駅名の翻訳辞書
STATION_TRANS = {
    '駅': ' Station',
    '東京メトロ': 'Tokyo Metro',
    '京急': 'Keikyu',
    'JR': 'JR',
    '小田急': 'Odakyu',
    '私鉄': 'Private Railway',
    '地下鉄': 'Subway',
    '市営地下鉄': 'Municipal Subway'
}

changes_count = 0

# 駅情報（fa-train）のパターン
pattern = r'(<i class="fas fa-train"></i>\s*<span>)([^<]+)(</span>)'

for match in re.finditer(pattern, en_html):
    original_station = match.group(2).strip()

    # 英語駅名の生成
    english_station = original_station

    # 路線名の翻訳
    for ja, en in STATION_TRANS.items():
        # 括弧内の路線名を翻訳
        english_station = re.sub(rf'\(({ja})\)', rf'(\1 {en})', english_station)
        english_station = english_station.replace(f'({ja}', f'({en}')
        english_station = english_station.replace(ja, en)

    # 区切り記号を英語化
    english_station = english_station.replace('・', ', ')
    english_station = english_station.replace('/', ' / ')

    # 重複を削除（例: "Keikyu Keikyu" → "Keikyu"）
    english_station = re.sub(r'\b(\w+)\s+\1\b', r'\1', english_station)

    # ハイブリッド形式のHTML生成
    hybrid_html = f'<span class="english-station">{english_station}</span><br>\n            <span class="japanese-station">Japanese: {original_station}</span>'

    # HTMLを置換
    old_html = match.group(0)
    new_html = match.group(1) + hybrid_html + match.group(3)

    en_html = en_html.replace(old_html, new_html, 1)
    changes_count += 1

    print(f"  {changes_count}. {original_station[:30]}... → ハイブリッド化")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.7 駅名ハイブリッド化完了")
print(f"   変更箇所: {changes_count}箇所")
print(f"   形式: 英語駅名 + 日本語駅名（2行表示）")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
