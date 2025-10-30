#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.8 住所・駅名の完全英語化スクリプト
町名と駅名を完全にローマ字化
"""

import re
from pathlib import Path
import pykakasi

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.8: 住所・駅名の完全英語化")
print("=" * 80)

# kakasi初期化（日本語→ローマ字変換）
kks = pykakasi.kakasi()

def romanize_japanese(text):
    """日本語をローマ字に変換（大文字始まり、ハイフン区切り）"""
    result = kks.convert(text)
    romanized = ''.join([item['hepburn'].capitalize() for item in result])
    return romanized

def clean_romanization(text):
    """ローマ字化した文字列をクリーンアップ"""
    # 特殊文字の処理
    text = text.replace('　', ' ')
    text = text.replace('～', '-')
    text = text.replace('・', ', ')
    # 連続するハイフンを1つに
    text = re.sub(r'-+', '-', text)
    # 前後のハイフンを削除
    text = text.strip('-')
    return text

changes = {'addresses': 0, 'stations': 0}

print("\n【1. 住所の完全英語化】")

# 英語住所の完全ローマ字化
address_pattern = r'(<span class="english-address">)([^<]+)(</span>)'
for match in re.finditer(address_pattern, en_html):
    original = match.group(2)

    # 日本語が含まれているか確認
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', original):
        # 都道府県・市区名は既に英語化済みなので、それ以降をローマ字化
        parts = original.split(', ')
        new_parts = []

        for part in parts:
            # 既に英語の部分はそのまま
            if not re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', part):
                new_parts.append(part)
            else:
                # 日本語部分をローマ字化
                romanized = romanize_japanese(part)
                romanized = clean_romanization(romanized)
                new_parts.append(romanized)

        new_address = ', '.join(new_parts)

        # 置換
        old_html = match.group(0)
        new_html = match.group(1) + new_address + match.group(3)
        en_html = en_html.replace(old_html, new_html, 1)

        changes['addresses'] += 1
        print(f"  {changes['addresses']}. {original[:40]}... → {new_address[:40]}...")

print(f"\n  完了: {changes['addresses']}箇所")

print("\n【2. 駅名の完全英語化】")

# 英語駅名の完全ローマ字化
station_pattern = r'(<span class="english-station">)([^<]+)(</span>)'
for match in re.finditer(station_pattern, en_html):
    original = match.group(2)

    # 日本語が含まれているか確認
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', original):
        new_station = original

        # 駅名部分（"駅"の前）を抽出してローマ字化
        # 例: "日本橋 Station" → "Nihonbashi Station"
        station_names = re.findall(r'([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)\s*Station', new_station)
        for ja_name in station_names:
            romanized = romanize_japanese(ja_name)
            new_station = new_station.replace(f'{ja_name} Station', f'{romanized} Station')

        # 路線名の前後にある駅名もローマ字化（例: "Keikyu川崎" → "Keikyu Kawasaki"）
        # 英語路線名の後の日本語
        for route in ['Keikyu', 'JR', 'Tokyo Metro', 'Odakyu', 'Meitetu', 'Kintetsu']:
            pattern_after = rf'{route}([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+)'
            for ja_match in re.finditer(pattern_after, new_station):
                ja_part = ja_match.group(1)
                romanized = romanize_japanese(ja_part)
                new_station = new_station.replace(f'{route}{ja_part}', f'{route} {romanized}')

        # 残りの日本語部分もローマ字化
        remaining_ja = re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+', new_station)
        for ja_part in remaining_ja:
            romanized = romanize_japanese(ja_part)
            new_station = new_station.replace(ja_part, romanized)

        # クリーンアップ
        new_station = clean_romanization(new_station)

        # 置換
        old_html = match.group(0)
        new_html = match.group(1) + new_station + match.group(3)
        en_html = en_html.replace(old_html, new_html, 1)

        changes['stations'] += 1
        print(f"  {changes['stations']}. {original[:40]}... → {new_station[:40]}...")

print(f"\n  完了: {changes['stations']}箇所")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.8 完全英語化完了")
print(f"   住所: {changes['addresses']}箇所")
print(f"   駅名: {changes['stations']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
