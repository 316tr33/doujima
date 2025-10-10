#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.6 住所ハイブリッド化スクリプト
お遍路方式の2行表示（英語住所 + 日本語住所）に変更
"""

import re
from pathlib import Path
import json

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
json_path = Path(__file__).parent / "tokaido_stations_data.json"

en_html = en_html_path.read_text(encoding='utf-8')
station_data = json.loads(json_path.read_text(encoding='utf-8'))

print("=" * 80)
print("東海道英語版 Phase 2.6: 住所ハイブリッド化")
print("=" * 80)

# 全宿場データを統合（起点・終点 + 通常宿場）
all_stations = station_data['special_stations'] + station_data['regular_stations']

# data_numberでソート
all_stations.sort(key=lambda x: x['data_number'])

changes_count = 0

# 各宿場の住所を変換
for station in all_stations:
    data_num = station['data_number']
    original_address = station['address']

    # 現在のHTMLから該当箇所を探す
    pattern = rf'(data-number="{data_num}".*?<i class="fas fa-map-marker-alt"></i>\s*<span>)([^<]+)(</span>)'
    match = re.search(pattern, en_html, re.DOTALL)

    if match:
        current_address = match.group(2).strip()

        # ハイブリッド住所を生成
        # 例: "Tokyo, 中央区日本橋室町～日本橋" →
        #     "<span class=\"english-address\">Tokyo, Chuo-ku, Nihonbashi Muromachi - Nihonbashi</span>\n<span class=\"japanese-address\">Japanese Address: 東京都中央区日本橋室町～日本橋</span>"

        # 英語住所の生成（区名以降をローマ字化）
        english_address = current_address

        # 区名のローマ字化
        english_address = english_address.replace('中央区', 'Chuo-ku, ')
        english_address = english_address.replace('品川区', 'Shinagawa-ku, ')
        english_address = english_address.replace('川崎市', 'Kawasaki City, ')
        english_address = english_address.replace('横浜市', 'Yokohama City, ')
        english_address = english_address.replace('神奈川区', 'Kanagawa-ku, ')
        english_address = english_address.replace('保土ケ谷区', 'Hodogaya-ku, ')
        english_address = english_address.replace('戸塚区', 'Totsuka-ku, ')
        english_address = english_address.replace('藤沢市', 'Fujisawa City, ')
        english_address = english_address.replace('平塚市', 'Hiratsuka City, ')
        english_address = english_address.replace('大磯町', 'Oiso Town, ')
        english_address = english_address.replace('小田原市', 'Odawara City, ')
        english_address = english_address.replace('箱根町', 'Hakone Town, ')
        english_address = english_address.replace('三島市', 'Mishima City, ')
        english_address = english_address.replace('沼津市', 'Numazu City, ')
        english_address = english_address.replace('静岡市', 'Shizuoka City, ')
        english_address = english_address.replace('清水区', 'Shimizu-ku, ')
        english_address = english_address.replace('駿河区', 'Suruga-ku, ')
        english_address = english_address.replace('焼津市', 'Yaizu City, ')
        english_address = english_address.replace('藤枝市', 'Fujieda City, ')
        english_address = english_address.replace('島田市', 'Shimada City, ')
        english_address = english_address.replace('掛川市', 'Kakegawa City, ')
        english_address = english_address.replace('袋井市', 'Fukuroi City, ')
        english_address = english_address.replace('磐田市', 'Iwata City, ')
        english_address = english_address.replace('浜松市', 'Hamamatsu City, ')
        english_address = english_address.replace('西区', 'Nishi-ku, ')
        english_address = english_address.replace('湖西市', 'Kosai City, ')
        english_address = english_address.replace('豊橋市', 'Toyohashi City, ')
        english_address = english_address.replace('岡崎市', 'Okazaki City, ')
        english_address = english_address.replace('知立市', 'Chiryu City, ')
        english_address = english_address.replace('名古屋市', 'Nagoya City, ')
        english_address = english_address.replace('緑区', 'Midori-ku, ')
        english_address = english_address.replace('熱田区', 'Atsuta-ku, ')
        english_address = english_address.replace('桑名市', 'Kuwana City, ')
        english_address = english_address.replace('四日市市', 'Yokkaichi City, ')
        english_address = english_address.replace('鈴鹿市', 'Suzuka City, ')
        english_address = english_address.replace('亀山市', 'Kameyama City, ')
        english_address = english_address.replace('甲賀市', 'Koka City, ')
        english_address = english_address.replace('栗東市', 'Ritto City, ')
        english_address = english_address.replace('草津市', 'Kusatsu City, ')
        english_address = english_address.replace('大津市', 'Otsu City, ')
        english_address = english_address.replace('京都市', 'Kyoto City, ')
        english_address = english_address.replace('東山区', 'Higashiyama-ku, ')

        # 記号の英語化
        english_address = english_address.replace('～', ' - ')
        english_address = english_address.replace('・', ', ')

        # ハイブリッド形式のHTML生成
        hybrid_html = f'<span class="english-address">{english_address}</span><br>\n            <span class="japanese-address">Japanese Address: {original_address}</span>'

        # HTMLを置換
        old_html = match.group(0)
        new_html = match.group(1) + hybrid_html + match.group(3)

        en_html = en_html.replace(old_html, new_html)
        changes_count += 1

        print(f"  {data_num}: ハイブリッド化完了")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.6 住所ハイブリッド化完了")
print(f"   変更箇所: {changes_count}箇所")
print(f"   形式: 英語住所 + 日本語住所（2行表示）")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
