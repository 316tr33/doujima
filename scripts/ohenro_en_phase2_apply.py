#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 2適用スクリプト: h3タグの寺院名を英語化
「第○番 寺名」→「Temple No.○ 寺名ローマ字」
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 2: 寺院名の英語化")
print("=" * 80)

# 寺院名の日本語→英語マッピング（ローマ字表記）
temple_names = {
    1: "Ryozen-ji", 2: "Gokuraku-ji", 3: "Konsen-ji", 4: "Dainichi-ji", 5: "Jizo-ji",
    6: "Anraku-ji", 7: "Juraku-ji", 8: "Kumadani-ji", 9: "Horin-ji", 10: "Kirihata-ji",
    11: "Fujii-dera", 12: "Shosan-ji", 13: "Dainichi-ji", 14: "Joraku-ji", 15: "Kokubu-ji",
    16: "Kannon-ji", 17: "Ido-ji", 18: "Onzan-ji", 19: "Tatsue-ji", 20: "Kakurin-ji",
    21: "Tairyu-ji", 22: "Byodo-ji", 23: "Yakuo-ji", 24: "Hotsumisakiji", 25: "Shinshoji",
    26: "Kongochoji", 27: "Konomineji", 28: "Dainichiji", 29: "Kokubunji", 30: "Zenrakuji",
    31: "Chikurinji", 32: "Zenjibuji", 33: "Sekkeiji", 34: "Tanemaji", 35: "Kiyotakiji",
    36: "Shoryuji", 37: "Iwamotoji", 38: "Kongofukuji", 39: "Enkoji", 40: "Kanjizaiji",
    41: "Ryukoji", 42: "Butsumokuji", 43: "Meisekiji", 44: "Daihoji", 45: "Iwayaji",
    46: "Joruriji", 47: "Yasakaji", 48: "Sairinji", 49: "Jodoji", 50: "Hantaji",
    51: "Ishiteji", 52: "Taizanji", 53: "Enmyoji", 54: "Enmeiji", 55: "Nankobo",
    56: "Taisanji", 57: "Eifukuji", 58: "Senyuji", 59: "Kokubunji", 60: "Yokomineji",
    61: "Koonji", 62: "Hojuji", 63: "Kichijoji", 64: "Maegamiji", 65: "Sankakuji",
    66: "Unpenji", 67: "Daikoji", 68: "Jinneiin", 69: "Kannonji", 70: "Motoyamaji",
    71: "Iyadaniji", 72: "Mandaraji", 73: "Shusshakaji", 74: "Koyamaji", 75: "Zentsuji",
    76: "Konzoji", 77: "Doryuji", 78: "Goshoji", 79: "Tennoji", 80: "Kokubunji",
    81: "Shiromineji", 82: "Negoro-ji", 83: "Ichinomiya-ji", 84: "Yashima-ji", 85: "Yakuri-ji",
    86: "Shido-ji", 87: "Nagao-ji", 88: "Okubo-ji"
}

# h3タグの寺院名を英語化
modified_html = en_html
update_count = 0

for number in range(1, 89):
    if number not in temple_names:
        continue

    english_name = temple_names[number]

    # パターン: <h3>第...番 寺名 ...</h3> → <h3>Temple No.○ 英語名 ...</h3>
    # 重要度マーク（★★）や他の要素を保持
    # 漢数字マッピング
    kanji_numbers = {
        1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
        11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五', 16: '十六', 17: '十七', 18: '十八',
        19: '十九', 20: '二十', 21: '二十一', 22: '二十二', 23: '二十三', 24: '二十四', 25: '二十五',
        26: '二十六', 27: '二十七', 28: '二十八', 29: '二十九', 30: '三十', 31: '三十一', 32: '三十二',
        33: '三十三', 34: '三十四', 35: '三十五', 36: '三十六', 37: '三十七', 38: '三十八', 39: '三十九',
        40: '四十', 41: '四十一', 42: '四十二', 43: '四十三', 44: '四十四', 45: '四十五', 46: '四十六',
        47: '四十七', 48: '四十八', 49: '四十九', 50: '五十', 51: '五十一', 52: '五十二', 53: '五十三',
        54: '五十四', 55: '五十五', 56: '五十六', 57: '五十七', 58: '五十八', 59: '五十九', 60: '六十',
        61: '六十一', 62: '六十二', 63: '六十三', 64: '六十四', 65: '六十五', 66: '六十六', 67: '六十七',
        68: '六十八', 69: '六十九', 70: '七十', 71: '七十一', 72: '七十二', 73: '七十三', 74: '七十四',
        75: '七十五', 76: '七十六', 77: '七十七', 78: '七十八', 79: '七十九', 80: '八十', 81: '八十一',
        82: '八十二', 83: '八十三', 84: '八十四', 85: '八十五', 86: '八十六', 87: '八十七', 88: '八十八'
    }
    kanji_num = kanji_numbers[number]
    # 「第」の有無に対応（32番など一部の寺院は「第」なし）
    pattern = rf'<h3>第?{kanji_num}番 [^<]+((?:<span[^>]*>.*?</span>)?)</h3>'

    match = re.search(pattern, modified_html)
    if match:
        update_count += 1
        # マークや追加要素を保持
        extra = match.group(1) if match.group(1) else ''
        replacement = f'<h3>Temple No.{number} {english_name}{extra}</h3>'
        modified_html = re.sub(pattern, replacement, modified_html, count=1)

print(f"\n更新した寺院名: {update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 2適用完了: {en_html_path}")

# 検証用サマリー
print("\n【修正サマリー】")
print(f"✓ 寺院名英語化: {update_count}箇所")
print(f"  - 形式: 「第○番 寺名」→「Temple No.○ ローマ字名」")
print("=" * 80)
