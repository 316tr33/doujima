#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道53宿 + 起点・終点の英語名データベース
"""

# 宿場名: 日本語 → 英語ローマ字表記
STATION_NAMES_EN = {
    # 起点
    0: "Nihonbashi",
    
    # 江戸エリア（1-15宿）
    1: "Shinagawa",
    2: "Kawasaki",
    3: "Kanagawa",
    4: "Hodogaya",
    5: "Totsuka",
    6: "Fujisawa",
    7: "Hiratsuka",
    8: "Oiso",
    9: "Odawara",
    10: "Hakone",
    11: "Mishima",
    12: "Numazu",
    13: "Hara",
    14: "Yoshiwara",
    15: "Kambara",
    
    # 東海道エリア（16-34宿）
    16: "Yui",
    17: "Okitsu",
    18: "Ejiri",
    19: "Fuchu",
    20: "Mariko",
    21: "Okabe",
    22: "Fujieda",
    23: "Shimada",
    24: "Kanaya",
    25: "Nissaka",
    26: "Kakegawa",
    27: "Fukuroi",
    28: "Mitsuke",
    29: "Hamamatsu",
    30: "Maisaka",
    31: "Arai",
    32: "Shirasuka",
    33: "Futagawa",
    34: "Yoshida",
    
    # 近畿エリア（35-53宿）
    35: "Goyu",
    36: "Akasaka",
    37: "Fujikawa",
    38: "Okazaki",
    39: "Chiryu",
    40: "Narumi",
    41: "Miya",
    42: "Kuwana",
    43: "Yokkaichi",
    44: "Ishiyakushi",
    45: "Shono",
    46: "Kameyama",
    47: "Seki",
    48: "Sakanoshita",
    49: "Tsuchiyama",
    50: "Minakuchi",
    51: "Ishibe",
    52: "Kusatsu",
    53: "Otsu",
    
    # 終点
    54: "Sanjo Ohashi"
}

# 宿場の英語表記（Post Town付き）
STATION_NAMES_FULL_EN = {
    0: "Nihonbashi Bridge",  # 起点は橋なのでBridge
    **{i: f"{STATION_NAMES_EN[i]} Post Town" for i in range(1, 54)},
    54: "Sanjo Ohashi Bridge"  # 終点も橋
}

# 読み仮名の表示方針：英語版では削除
# station-reading要素は削除する
