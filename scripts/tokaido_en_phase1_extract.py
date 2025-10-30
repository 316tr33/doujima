#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 1 データ抽出スクリプト
日本語版から宿場データを抽出してJSON形式で保存
"""

import re
import json
from pathlib import Path

# ファイルパス
ja_html_path = Path(__file__).parent.parent / "Tokaido/stations.html"
ja_html = ja_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 1: データ抽出")
print("=" * 80)

# 簡潔なパターンで抽出
# まずコメントマーカーを見つけて、その後のstation-cardブロック全体を取得
# station-info の</div>まで確実に取得
comment_pattern = r'<!-- (\d+)宿 (.+?) -->\s*(<div\s+class="station-card[^"]*"[^>]*>.*?<div class="station-info">.*?</div>\s*</div>\s*</div>)'

stations = []
for match in re.finditer(comment_pattern, ja_html, re.DOTALL):
    num, name, full_card = match.groups()
    card_html = full_card

    # 各要素を個別に抽出
    classes_match = re.search(r'class="station-card ([^"]+)"', match.group(0))
    data_num_match = re.search(r'data-number="(\d+)"', match.group(0))
    data_features_match = re.search(r'data-features="([^"]*)"', match.group(0))
    image_src_match = re.search(r'<img[^>]+src="([^"]+)"', card_html)
    image_alt_match = re.search(r'<img[^>]+alt="([^"]+)"', card_html)
    display_num_match = re.search(r'<div class="station-number">(\d+)</div>', card_html)
    badges_html = re.search(r'<div class="station-badges">(.*?)</div>', card_html, re.DOTALL)
    name_h3_match = re.search(r'<h3>(.+?)</h3>', card_html)
    reading_match = re.search(r'<div class="station-reading">(.+?)</div>', card_html)
    desc_match = re.search(r'<p class="station-description">\s*(.+?)\s*</p>', card_html, re.DOTALL)

    # 詳細情報
    detail_spans = re.findall(r'<div class="detail-item">.*?<span>([^<]+)</span>', card_html, re.DOTALL)

    # highlights
    highlights_match = re.search(r'<div class="station-highlights">(.*?)</div>', card_html, re.DOTALL)
    highlights = []
    if highlights_match:
        highlights = re.findall(r'<span>([^<]+)</span>', highlights_match.group(1))

    # badges
    badges = []
    if badges_html:
        badges = re.findall(r'<span class="badge [^"]+">([^<]+)</span>', badges_html.group(1))

    if len(detail_spans) >= 3:
        station_data = {
            'comment_number': int(num),
            'comment_name': name,
            'classes': classes_match.group(1) if classes_match else '',
            'data_number': int(data_num_match.group(1)) if data_num_match else 0,
            'data_features': data_features_match.group(1) if data_features_match else '',
            'image_src': image_src_match.group(1) if image_src_match else '',
            'image_alt': image_alt_match.group(1) if image_alt_match else '',
            'display_number': int(display_num_match.group(1)) if display_num_match else 0,
            'badges': badges,
            'name': name_h3_match.group(1) if name_h3_match else name,
            'reading': reading_match.group(1) if reading_match else '',
            'description': desc_match.group(1).strip() if desc_match else '',
            'address': detail_spans[0],
            'station_info': detail_spans[1],
            'visit_time': detail_spans[2],
            'highlights': highlights
        }
        stations.append(station_data)
        print(f"{num}宿 {station_data['name']}（{station_data['reading']}）")


print(f"\n抽出完了: {len(stations)}箇所")

# 起点（日本橋）と終点（京都）を抽出
# data-number="0" または "54" のstation-cardを探す
special_stations = []
for data_num in ['0', '54']:
    pattern = rf'(<div\s+class="station-card[^"]*"\s+data-number="{data_num}"[^>]*>.*?<div class="station-info">.*?</div>\s*</div>\s*</div>)'
    match = re.search(pattern, ja_html, re.DOTALL)

    if match:
        full_match = match.group(0)
        card_html = full_match

        # 各要素を抽出
        classes_match = re.search(r'class="station-card ([^"]+)"', full_match)
        data_features_match = re.search(r'data-features="([^"]*)"', full_match)
        image_src_match = re.search(r'<img[^>]+src="([^"]+)"', card_html)
        image_alt_match = re.search(r'<img[^>]+alt="([^"]+)"', card_html)
        display_num_match = re.search(r'<div class="station-number">(.+?)</div>', card_html)
        badges_html = re.search(r'<div class="station-badges">(.*?)</div>', card_html, re.DOTALL)
        name_h3_match = re.search(r'<h3>(.+?)</h3>', card_html)
        reading_match = re.search(r'<div class="station-reading">(.+?)</div>', card_html)
        desc_match = re.search(r'<p class="station-description">\s*(.+?)\s*</p>', card_html, re.DOTALL)

        # 詳細情報
        detail_spans = re.findall(r'<div class="detail-item">.*?<span>([^<]+)</span>', card_html, re.DOTALL)

        # highlights
        highlights_match = re.search(r'<div class="station-highlights">(.*?)</div>', card_html, re.DOTALL)
        highlights = []
        if highlights_match:
            highlights = re.findall(r'<span>([^<]+)</span>', highlights_match.group(1))

        # badges
        badges = []
        if badges_html:
            badges = re.findall(r'<span class="badge [^"]+">([^<]+)</span>', badges_html.group(1))

        if len(detail_spans) >= 3 and name_h3_match:
            special_data = {
                'type': 'special',
                'classes': classes_match.group(1) if classes_match else '',
                'data_number': int(data_num),
                'data_features': data_features_match.group(1) if data_features_match else '',
                'image_src': image_src_match.group(1) if image_src_match else '',
                'image_alt': image_alt_match.group(1) if image_alt_match else '',
                'display_number': display_num_match.group(1) if display_num_match else '',
                'badges': badges,
                'name': name_h3_match.group(1),
                'reading': reading_match.group(1) if reading_match else '',
                'description': desc_match.group(1).strip() if desc_match else '',
                'address': detail_spans[0],
                'station_info': detail_spans[1],
                'visit_time': detail_spans[2],
                'highlights': highlights
            }
            special_stations.append(special_data)
            print(f"特別: {special_data['name']}（{special_data['reading']}）")

# データ保存
output_data = {
    'special_stations': special_stations,
    'regular_stations': stations,
    'total': len(special_stations) + len(stations)
}

output_path = Path(__file__).parent / "tokaido_stations_data.json"
output_path.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding='utf-8')

print("\n" + "=" * 80)
print(f"✅ データ抽出完了")
print(f"   起点・終点: {len(special_stations)}箇所")
print(f"   宿場: {len(stations)}箇所")
print(f"   合計: {len(special_stations) + len(stations)}箇所")
print(f"   保存先: {output_path}")
print("=" * 80)
