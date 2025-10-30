#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2一括修正スクリプト: CSVデータでHTMLを更新
"""

import csv
import re
from pathlib import Path

# ファイルパス
csv_path = Path("/Users/macmiller/Desktop/doujima/syukubacho.csv")
html_path = Path("/Users/macmiller/Desktop/doujima/Tokaido/stations.html")

# CSVデータを読み込む
stations_data = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        shukuba = row['宿場町']
        if shukuba.startswith('起点') or shukuba.startswith('終点'):
            continue
        parts = shukuba.split('：')
        if len(parts) < 2:
            continue
        try:
            number = int(parts[0])
        except ValueError:
            continue
        stations_data[number] = {
            'address': row['住所'],
            'station': row['最寄駅'],
            'time': row['見学時間目安']
        }

# HTMLを読み込む
html_content = html_path.read_text(encoding='utf-8')

# 各宿場の detail-item セクションを置換
def replace_station_details(match):
    number = int(match.group(1))

    if number not in stations_data:
        return match.group(0)  # 変更なし

    data = stations_data[number]

    # 元のインデントを保持
    indent = match.group(2)

    # 新しいHTMLを生成
    new_details = f'''{indent}<div class="station-details">
{indent}  <div class="detail-item">
{indent}    <i class="fas fa-map-marker-alt"></i>
{indent}    <span>{data['address']}</span>
{indent}  </div>
{indent}  <div class="detail-item">
{indent}    <i class="fas fa-train"></i>
{indent}    <span>{data['station']}</span>
{indent}  </div>
{indent}  <div class="detail-item">
{indent}    <i class="fas fa-clock"></i>
{indent}    <span>見学時間：{data['time']}</span>
{indent}  </div>
{indent}</div>'''

    return new_details

# パターン: <!-- X宿 --> の後の station-details セクションを探す
pattern = r'<!-- (\d+)宿 .+? -->.*?(\s+)<div class="station-details">.*?</div>\s+</div>\s+<div class="station-highlights">'

# 置換実行
modified_html = re.sub(
    pattern,
    lambda m: f'<!-- {m.group(1)}宿 {m.group(0).split("-->")[0].split()[-1]} -->' +
              m.group(0).split('-->')[-1].split('<div class="station-details">')[0] +
              replace_station_details(m) +
              '\n' + m.group(2) + '<div class="station-highlights">',
    html_content,
    flags=re.DOTALL
)

# より単純なアプローチ: 各宿場ごとに個別置換
for number, data in sorted(stations_data.items()):
    # address置換
    addr_pattern = rf'(<!-- {number}宿 .+? -->.*?<i class="fas fa-map-marker-alt"></i>\s*<span>)([^<]+)(</span>)'
    modified_html = re.sub(addr_pattern, rf'\g<1>{data["address"]}\g<3>', modified_html, flags=re.DOTALL)

    # station置換
    station_pattern = rf'(<!-- {number}宿 .+? -->.*?<i class="fas fa-train"></i>\s*<span>)([^<]+)(</span>)'
    modified_html = re.sub(station_pattern, rf'\g<1>{data["station"]}\g<3>', modified_html, flags=re.DOTALL)

    # time置換
    time_pattern = rf'(<!-- {number}宿 .+? -->.*?<i class="fas fa-clock"></i>\s*<span>見学時間：)([^<]+)(</span>)'
    modified_html = re.sub(time_pattern, rf'\g<1>{data["time"]}\g<3>', modified_html, flags=re.DOTALL)

# 結果を保存
html_path.write_text(modified_html, encoding='utf-8')
print(f"Phase 2修正完了: {len(stations_data)}宿場の情報を更新しました")
