#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2検証スクリプト: CSVとHTMLの府県・最寄駅・時間情報を照合
"""

import csv
import re
from pathlib import Path

# CSVファイルを読み込む
csv_path = Path("/Users/macmiller/Desktop/doujima/syukubacho.csv")
html_path = Path("/Users/macmiller/Desktop/doujima/Tokaido/stations.html")

# CSVデータを解析
stations_csv = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        shukuba = row['宿場町']
        # 起点と終点をスキップ
        if shukuba.startswith('起点') or shukuba.startswith('終点'):
            continue
        # 番号を抽出
        parts = shukuba.split('：')
        if len(parts) < 2:
            continue
        try:
            number = int(parts[0])
        except ValueError:
            continue
        name = parts[1].replace('宿', '').replace('（熱田）', '').replace('（鞠子）', '').strip()
        stations_csv[number] = {
            'name': name,
            'address': row['住所'],
            'station': row['最寄駅'],
            'time': row['見学時間目安']
        }

# HTMLから現在の情報を抽出
html_content = html_path.read_text(encoding='utf-8')

# 宿場カードのパターンを検索
pattern = r'<!-- (\d+)宿 (.+?) -->.*?<span>(.+?)</span>.*?<i class="fas fa-train"></i>\s*<span>(.+?)</span>.*?<i class="fas fa-clock"></i>\s*<span>見学時間：(.+?)</span>'
matches = re.findall(pattern, html_content, re.DOTALL)

# 差分を検出
differences = []
for match in matches:
    number = int(match[0])
    html_name = match[1]
    html_address = match[2]
    html_station = match[3]
    html_time = match[4]

    if number in stations_csv:
        csv_data = stations_csv[number]
        errors = []

        if html_address != csv_data['address']:
            errors.append(f"  住所: '{html_address}' → '{csv_data['address']}'")
        if html_station != csv_data['station']:
            errors.append(f"  最寄駅: '{html_station}' → '{csv_data['station']}'")
        if html_time != csv_data['time']:
            errors.append(f"  時間: '{html_time}' → '{csv_data['time']}'")

        if errors:
            differences.append(f"{number}番 {html_name}:")
            differences.extend(errors)

# 結果を出力
if differences:
    print("Phase 2 修正が必要な箇所:")
    print("=" * 60)
    for line in differences:
        print(line)
    print(f"\n合計: {len([d for d in differences if '番' in d])}箇所")
else:
    print("Phase 2: すべてCSVと一致しています ✓")
