#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.5 追加翻訳適用スクリプト
data-features、alt、badges、住所などの翻訳
"""

import re
from pathlib import Path
from tokaido_station_names_en import STATION_NAMES_EN

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.5: 追加翻訳適用")
print("=" * 80)

# 変更カウンター
changes = {
    'data_features': 0,
    'alt': 0,
    'station_number': 0,
    'badges': 0,
    'addresses': 0
}

# 翻訳辞書
FEATURE_TRANS = {
    '起点': 'starting-point',
    '終点': 'endpoint',
    '歴史': 'history',
    '名所': 'scenic',
    '風景': 'scenic',
    'グルメ': 'gourmet',
    '温泉': 'onsen',
    '初心者': 'beginner',
    '特別': 'special',
    '難所': 'difficult'
}

BADGE_TRANS = {
    '起点': 'Starting Point',
    '終点': 'Endpoint',
    '歴史名所': 'Historic Site',
    '風景名所': 'Scenic Spot',
    'グルメ': 'Gourmet',
    '温泉': 'Hot Spring',
    '初心者向け': 'Beginner-Friendly',
    '特別': 'Special',
    '難所': 'Difficult Section'
}

# 1. data-features属性の翻訳
print("\n【1. data-features属性の翻訳】")
feature_pattern = r'data-features="([^"]+)"'
for match in re.finditer(feature_pattern, en_html):
    original = match.group(1)
    # カンマ区切りで翻訳
    features = original.split(',')
    translated = ','.join([FEATURE_TRANS.get(f, f) for f in features])

    if original != translated:
        en_html = en_html.replace(f'data-features="{original}"', f'data-features="{translated}"')
        changes['data_features'] += 1
        print(f"  {original} → {translated}")

# 2. 画像alt属性の翻訳
print("\n【2. 画像alt属性の翻訳】")

# 宿場名の日本語→英語マッピング（長い名前から先に置換）
STATION_JA_TO_EN = {
    '三条大橋': 'Sanjo Ohashi',
    '保土ケ谷': 'Hodogaya',
    '日本橋': 'Nihonbashi',
    '吉原': 'Yoshiwara',
    '蒲原': 'Kambara',
    '白須賀': 'Shirasuka',
    '池鯉鮒': 'Chiryu',
    '四日市': 'Yokkaichi',
    '石薬師': 'Ishiyakushi',
    '品川': 'Shinagawa',
    '川崎': 'Kawasaki',
    '神奈川': 'Kanagawa',
    '戸塚': 'Totsuka',
    '藤沢': 'Fujisawa',
    '平塚': 'Hiratsuka',
    '大磯': 'Oiso',
    '小田原': 'Odawara',
    '箱根': 'Hakone',
    '三島': 'Mishima',
    '沼津': 'Numazu',
    '原': 'Hara',
    '由比': 'Yui',
    '興津': 'Okitsu',
    '江尻': 'Ejiri',
    '府中': 'Fuchu',
    '丸子': 'Mariko',
    '岡部': 'Okabe',
    '藤枝': 'Fujieda',
    '島田': 'Shimada',
    '金谷': 'Kanaya',
    '日坂': 'Nissaka',
    '掛川': 'Kakegawa',
    '袋井': 'Fukuroi',
    '見付': 'Mitsuke',
    '浜松': 'Hamamatsu',
    '舞坂': 'Maisaka',
    '新居': 'Arai',
    '白須賀': 'Shirasuka',
    '二川': 'Futagawa',
    '吉田': 'Yoshida',
    '御油': 'Goyu',
    '赤坂': 'Akasaka',
    '藤川': 'Fujikawa',
    '岡崎': 'Okazaki',
    '池鯉鮒': 'Chiryu',
    '鳴海': 'Narumi',
    '宮': 'Miya',
    '桑名': 'Kuwana',
    '四日市': 'Yokkaichi',
    '石薬師': 'Ishiyakushi',
    '庄野': 'Shono',
    '亀山': 'Kameyama',
    '関': 'Seki',
    '坂下': 'Sakanoshita',
    '土山': 'Tsuchiyama',
    '水口': 'Minakuchi',
    '石部': 'Ishibe',
    '草津': 'Kusatsu',
    '大津': 'Otsu',
    '三条大橋': 'Sanjo Ohashi'
}

alt_pattern = r'alt="([^"]*[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]+[^"]*)"'
for match in re.finditer(alt_pattern, en_html):
    original_alt = match.group(1)
    new_alt = original_alt

    # 宿場名を英語に変換
    for ja_name, en_name in STATION_JA_TO_EN.items():
        new_alt = new_alt.replace(ja_name, en_name)

    # 共通フレーズの翻訳
    new_alt = new_alt.replace(' - 歌川広重浮世絵', ' - Hiroshige Ukiyo-e')
    new_alt = new_alt.replace('歌川広重浮世絵', 'Hiroshige Ukiyo-e')
    new_alt = new_alt.replace('浮世絵', 'Ukiyo-e')

    if original_alt != new_alt:
        en_html = en_html.replace(f'alt="{original_alt}"', f'alt="{new_alt}"')
        changes['alt'] += 1
        print(f"  {original_alt[:40]}... → {new_alt[:40]}...")

# 3. station-numberの翻訳
print("\n【3. station-numberの翻訳】")
NUMBER_TRANS = {
    '起点': 'Start',
    '終点': 'End'
}

number_pattern = r'<div class="station-number">([起終]点)</div>'
for match in re.finditer(number_pattern, en_html):
    original_num = match.group(1)
    translated_num = NUMBER_TRANS.get(original_num, original_num)

    if original_num != translated_num:
        en_html = en_html.replace(
            f'<div class="station-number">{original_num}</div>',
            f'<div class="station-number">{translated_num}</div>'
        )
        changes['station_number'] += 1
        print(f"  {original_num} → {translated_num}")

# 4. バッジの翻訳
print("\n【4. バッジの翻訳】")
badge_pattern = r'<span class="badge [^"]+">([^<]+)</span>'
for match in re.finditer(badge_pattern, en_html):
    original_badge = match.group(1)

    # 日本語が含まれているか確認
    if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', original_badge):
        translated_badge = BADGE_TRANS.get(original_badge, original_badge)

        if original_badge != translated_badge:
            en_html = en_html.replace(match.group(0), match.group(0).replace(original_badge, translated_badge))
            changes['badges'] += 1
            print(f"  {original_badge} → {translated_badge}")

# 5. 住所の翻訳（都道府県名のみ）
print("\n【5. 住所の都道府県名翻訳】")
PREFECTURE_TRANS = {
    '東京都': 'Tokyo',
    '神奈川県': 'Kanagawa',
    '静岡県': 'Shizuoka',
    '愛知県': 'Aichi',
    '三重県': 'Mie',
    '滋賀県': 'Shiga',
    '京都府': 'Kyoto'
}

# 住所部分（detail-item内のspan）で都道府県を翻訳
address_pattern = r'(<div class="detail-item">.*?<i class="fas fa-map-marker-alt"></i>.*?<span>)([^<]+)(</span>)'
for match in re.finditer(address_pattern, en_html, re.DOTALL):
    original_address = match.group(2)
    new_address = original_address

    # 都道府県名を翻訳
    for ja_pref, en_pref in PREFECTURE_TRANS.items():
        if ja_pref in new_address:
            new_address = new_address.replace(ja_pref, en_pref + ', ')
            break

    if original_address != new_address:
        en_html = en_html.replace(match.group(0), match.group(1) + new_address + match.group(3))
        changes['addresses'] += 1

print(f"  {changes['addresses']}箇所の住所を翻訳")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.5 追加翻訳適用完了")
print(f"   data-features: {changes['data_features']}箇所")
print(f"   alt属性: {changes['alt']}箇所")
print(f"   station-number: {changes['station_number']}箇所")
print(f"   badges: {changes['badges']}箇所")
print(f"   addresses: {changes['addresses']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
