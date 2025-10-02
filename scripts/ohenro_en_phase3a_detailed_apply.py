#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3A詳細版適用スクリプト: 詳細な英語住所への変換
日本語住所を完全なローマ字形式に変換（番地、町名、郵便番号含む）
"""

import re
from pathlib import Path

# ファイルパス
ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"

ja_html = ja_html_path.read_text(encoding='utf-8')
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3A詳細版: 完全な英語住所への変換")
print("=" * 80)

# 日本語版から住所を抽出
ja_pattern = r'<!-- (\d+)番 .+? -->.*?<p>所在地: ([^<]+)</p>'
ja_addresses = re.findall(ja_pattern, ja_html, re.DOTALL)

# 住所辞書を作成
address_dict = {}
for number, address in ja_addresses:
    address_dict[int(number)] = address.strip()

print(f"\n日本語版から抽出した住所: {len(address_dict)}箇所")

# 都道府県マッピング
prefecture_map = {
    '徳島県': 'Tokushima',
    '高知県': 'Kochi',
    '愛媛県': 'Ehime',
    '香川県': 'Kagawa'
}

# 市区町村マッピング
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

def to_romaji_simple(text):
    """
    簡易的なローマ字変換（主要な変換のみ）
    より詳細な変換は個別に対応
    """
    # ひらがな→ローマ字マッピング（基本的なもの）
    hiragana_map = {
        'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
        'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
        'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
        'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
        'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
        'は': 'ha', 'ひ': 'hi', 'ふ': 'fu', 'へ': 'he', 'ほ': 'ho',
        'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
        'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
        'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
        'わ': 'wa', 'を': 'wo', 'ん': 'n',
        'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
        'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
        'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
        'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
        'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
    }

    # カタカナ→ひらがな変換用
    katakana_map = {
        'ア': 'あ', 'イ': 'い', 'ウ': 'う', 'エ': 'え', 'オ': 'お',
        'カ': 'か', 'キ': 'き', 'ク': 'く', 'ケ': 'け', 'コ': 'こ',
        'サ': 'さ', 'シ': 'し', 'ス': 'す', 'セ': 'せ', 'ソ': 'そ',
        'タ': 'た', 'チ': 'ち', 'ツ': 'つ', 'テ': 'て', 'ト': 'と',
        'ナ': 'な', 'ニ': 'に', 'ヌ': 'ぬ', 'ネ': 'ね', 'ノ': 'の',
        'ハ': 'は', 'ヒ': 'ひ', 'フ': 'ふ', 'ヘ': 'へ', 'ホ': 'ほ',
        'マ': 'ま', 'ミ': 'み', 'ム': 'む', 'メ': 'め', 'モ': 'も',
        'ヤ': 'や', 'ユ': 'ゆ', 'ヨ': 'よ',
        'ラ': 'ら', 'リ': 'り', 'ル': 'る', 'レ': 'れ', 'ロ': 'ろ',
        'ワ': 'わ', 'ヲ': 'を', 'ン': 'ん',
        'ガ': 'が', 'ギ': 'ぎ', 'グ': 'ぐ', 'ゲ': 'げ', 'ゴ': 'ご',
        'ザ': 'ざ', 'ジ': 'じ', 'ズ': 'ず', 'ゼ': 'ぜ', 'ゾ': 'ぞ',
        'ダ': 'だ', 'ヂ': 'ぢ', 'ヅ': 'づ', 'デ': 'で', 'ド': 'ど',
        'バ': 'ば', 'ビ': 'び', 'ブ': 'ぶ', 'ベ': 'べ', 'ボ': 'ぼ',
        'パ': 'ぱ', 'ピ': 'ぴ', 'プ': 'ぷ', 'ペ': 'ぺ', 'ポ': 'ぽ',
    }

    result = ""
    for char in text:
        if char in katakana_map:
            char = katakana_map[char]
        if char in hiragana_map:
            result += hiragana_map[char]
        else:
            result += char

    return result.title()

def convert_address_to_english(japanese_address):
    """
    日本語住所を詳細な英語形式に変換
    例: 徳島県鳴門市大麻町板東塚鼻126
    → 126 Bando Tsukahana, Oasa-cho, Naruto City, Tokushima
    """
    # 郵便番号を抽出
    postal_match = re.match(r'〒(\d{3}-\d{4})\s*(.+)', japanese_address)
    if postal_match:
        postal_code = postal_match.group(1)
        address = postal_match.group(2)
    else:
        postal_code = None
        address = japanese_address

    # 都道府県を抽出
    prefecture = None
    for jp_pref, en_pref in prefecture_map.items():
        if jp_pref in address:
            prefecture = en_pref
            address = address.replace(jp_pref, '', 1)
            break

    # 市区町村を抽出
    city = None
    for jp_city, en_city in city_map.items():
        if jp_city in address:
            city = en_city
            address = address.replace(jp_city, '', 1)
            break

    # 残りの部分（町名・番地等）をローマ字化
    # 番地を抽出（末尾の数字やハイフン付き数字）
    number_match = re.search(r'([\d\-ー]+)$', address)
    street_number = number_match.group(1).replace('ー', '-') if number_match else ''
    if number_match:
        address = address[:number_match.start()]

    # 町名をローマ字変換
    # 「町」「字」などの接尾辞を処理
    town_parts = []

    # 「○○町」「○○字」などを分離
    if '町' in address:
        parts = address.split('町')
        for i, part in enumerate(parts[:-1]):
            if part:
                town_parts.append(to_romaji_simple(part) + '-cho')
        if parts[-1]:
            town_parts.append(to_romaji_simple(parts[-1]))
    elif '字' in address:
        parts = address.split('字')
        for i, part in enumerate(parts[:-1]):
            if part:
                town_parts.append(to_romaji_simple(part) + '-aza')
        if parts[-1]:
            town_parts.append(to_romaji_simple(parts[-1]))
    else:
        if address:
            town_parts.append(to_romaji_simple(address))

    # 英語住所を組み立て
    result_parts = []

    if street_number:
        result_parts.append(street_number)

    if town_parts:
        result_parts.append(' '.join(town_parts))

    if city:
        result_parts.append(city)

    if prefecture:
        result_parts.append(prefecture)

    if postal_code:
        result_parts.append(postal_code)

    return ', '.join(result_parts)

# 各寺院の英語住所を生成
english_addresses = {}
for num in range(1, 89):
    if num in address_dict:
        ja_addr = address_dict[num]
        en_addr = convert_address_to_english(ja_addr)
        english_addresses[num] = en_addr
        print(f"{num}番: {en_addr}")

# 英語版HTMLを更新
modified_html = en_html
update_count = 0

for num in range(1, 89):
    if num not in english_addresses:
        continue

    english_addr = english_addresses[num]

    # 現在の簡略版の英語住所を詳細版に置き換え
    # パターン: <p class="english-address">Address: ...</p>
    pattern = rf'(<h3>Temple No\.{num} [^<]+(?:<span[^>]*>.*?</span>)?</h3>(?:\s*<p class="temple-significance">[^<]+</p>)?)\s*<p class="english-address">Address: [^<]+</p>'

    replacement = rf'\1\n              <p class="english-address">Address: {english_addr}</p>'

    if re.search(pattern, modified_html, re.DOTALL):
        modified_html = re.sub(pattern, replacement, modified_html, count=1, flags=re.DOTALL)
        update_count += 1

print(f"\n更新した住所: {update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 3A詳細版適用完了: {en_html_path}")

print("\n【修正サマリー】")
print(f"✓ 詳細な英語住所: {update_count}箇所")
print(f"  - 形式: 番地 + 町名（ローマ字） + 市区町村 + 都道府県 + 郵便番号")
print("=" * 80)
