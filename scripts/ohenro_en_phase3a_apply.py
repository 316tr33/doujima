#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3A適用スクリプト: 住所の英語化とハイブリッド表示
日本語住所を保持しつつ、英語住所を追加
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3A: 住所の英語化とハイブリッド表示")
print("=" * 80)

# 都道府県名の英語変換マッピング
prefecture_map = {
    '徳島県': 'Tokushima',
    '高知県': 'Kochi',
    '愛媛県': 'Ehime',
    '香川県': 'Kagawa'
}

# 市区町村の英語変換マッピング（主要な市のみ）
city_map = {
    '鳴門市': 'Naruto City',
    '板野郡': 'Itano District',
    '阿波市': 'Awa City',
    '吉野川市': 'Yoshinogawa City',
    '名西郡': 'Myozai District',
    '徳島市': 'Tokushima City',
    '小松島市': 'Komatsushima City',
    '勝浦郡': 'Katsuura District',
    '阿南市': 'Anan City',
    '海部郡': 'Kaifu District',
    '室戸市': 'Muroto City',
    '安芸郡': 'Aki District',
    '香南市': 'Konan City',
    '南国市': 'Nankoku City',
    '高知市': 'Kochi City',
    '土佐市': 'Tosa City',
    '高岡郡': 'Takaoka District',
    '土佐清水市': 'Tosashimizu City',
    '宿毛市': 'Sukumo City',
    '宇和郡': 'Uwa District',
    '宇和島市': 'Uwajima City',
    '西予市': 'Seiyo City',
    '久万高原町': 'Kumakogen Town',
    '松山市': 'Matsuyama City',
    '今治市': 'Imabari City',
    '西条市': 'Saijo City',
    '四国中央市': 'Shikokuchuo City',
    '三豊市': 'Mitoyo City',
    '観音寺市': 'Kanonji City',
    '善通寺市': 'Zentsuji City',
    '仲多度郡': 'Nakatado District',
    '綾歌郡': 'Ayauta District',
    '坂出市': 'Sakaide City',
    '高松市': 'Takamatsu City',
    'さぬき市': 'Sanuki City'
}

def simplify_address(address):
    """
    日本語住所を簡略化した英語住所に変換
    例: 徳島県鳴門市大麻町板東塚鼻126
    → 126 Bando Tsukahana, Oasa-cho, Naruto City, Tokushima
    """
    # 郵便番号を削除
    address = re.sub(r'〒\d{3}-\d{4}\s*', '', address)

    # 都道府県を抽出
    prefecture = None
    for jp_pref, en_pref in prefecture_map.items():
        if jp_pref in address:
            prefecture = en_pref
            address = address.replace(jp_pref, '')
            break

    # 市区町村を抽出
    city = None
    for jp_city, en_city in city_map.items():
        if jp_city in address:
            city = en_city
            address = address.replace(jp_city, '')
            break

    # 残りの住所（町名・番地等）は簡略化表記
    # 詳細な番地は保持、町名等は省略
    # シンプルに「市区町村, 都道府県」形式にする
    if city and prefecture:
        return f"{city}, {prefecture}"
    elif prefecture:
        return prefecture
    else:
        return "Shikoku, Japan"

# 住所パターンを検索して英語住所を追加
modified_html = en_html
update_count = 0

# 各寺院の住所を検索（temple-significanceがある場合も考慮）
pattern = r'(<h3>Temple No\.\d+ [^<]+(?:<span[^>]*>.*?</span>)?</h3>\s*(?:<p class="temple-significance">[^<]+</p>\s*)?)(<p>所在地: )([^<]+)(</p>)'

def replace_address(match):
    global update_count
    update_count += 1

    h3_and_significance = match.group(1)
    address_label = match.group(2)
    japanese_address = match.group(3)
    closing_tag = match.group(4)

    # 英語住所を生成
    english_address = simplify_address(japanese_address)

    # ハイブリッド表示形式で返す
    return (
        f'{h3_and_significance}'
        f'<p class="english-address">Address: {english_address}</p>\n              '
        f'<p class="japanese-address">{address_label.replace("<p>", "")}{japanese_address}{closing_tag}'
    )

modified_html = re.sub(pattern, replace_address, modified_html)

print(f"\n更新した住所: {update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 3A適用完了: {en_html_path}")

# 検証用サマリー
print("\n【修正サマリー】")
print(f"✓ 住所の英語化: {update_count}箇所")
print(f"  - 形式: 英語住所（Address:） + 日本語住所（所在地:）のハイブリッド表示")
print("=" * 80)
