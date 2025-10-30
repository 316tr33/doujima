#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2.10 完全英語化スクリプト
ローマ字連結を適切な英語表現に変換
"""

import re
from pathlib import Path
from collections import OrderedDict

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 2.10: ローマ字連結の完全英語化")
print("=" * 80)

changes = {
    'addresses': 0,
    'stations': 0,
    'other': 0
}

# 住所の英語化マッピング（長いパターンから順に処理）
address_fixes = OrderedDict([
    # 最長パターンから順に配置
    ('ToyokawaShiAkasakaMachishuuhen', 'Toyokawa City, Akasaka Town Area'),
    ('FujishiYoshiharaHonchouShuuhen', 'Fuji City, Yoshihara Honcho Area'),
    ('ToyokawaShiGoyuMachishuuhen', 'Toyokawa City, Goyu Town Area'),
    ('ChuukyoukuSanjouOohashiKaiwai', 'Chukyo-ku, Sanjo Ohashi Area'),
    ('HoTsuchiKeTanimachiShuuhen', 'Hodogaya Area'),
    ('MaisakaMachiMaisakaShuuhen', 'Maisaka Town, Maisaka Area'),
    ('ShinkyoMachiShinkyoShuuhen', 'Shinkyo Town, Shinkyo Area'),
    ('AshigarashimoGunHakone', 'Ashigarashimo District, Hakone'),
    ('TsuchiyamaMachiHayamiya', 'Tsuchiyama Town, Hayamiya'),
    ('KanagawaHonchouShuuhen', 'Kanagawa Honcho Area'),
    ('HorinouchiMachishuuhen', 'Horinouchi Town Area'),
    ('OkitsuNakamachiShuuhen', 'Okitsu Nakamachi Area'),
    ('IshiyakushiMachishuuhen', 'Ishiyakushi Town Area'),
    ('KitaTsuchiyamaShuuhen', 'Kita-Tsuchiyama Area'),
    ('KanMachiSakashitaShuuhen', 'Kan Town, Sakashita Area'),
    ('FujikawaMachishuuhen', 'Fujikawa Town Area'),
    ('FutakawaMachishuuhen', 'Futakawa Town Area'),
    ('MizuguchiMachiHonchou', 'Mizuguchi Town, Honcho'),
    ('KonanShiIshibeChuuou', 'Konan City, Ishibe Central'),
    ('MaruyaMachishuuhen', 'Maruyama Town Area'),
    ('MinamishinagawaIttai', 'Minamishinagawa Area'),
    ('NihonbashiMuromachi', 'Nihonbashi Muromachi'),
    ('KawasakikuHonchou', 'Kawasaki-ku Honcho'),
    ('IshibeKuchiShuuhen', 'Ishibe-guchi Area'),
    ('TotsukachouShuuhen', 'Totsuka Town Area'),
    ('KanayaHonchouShuuhen', 'Kanaya Honcho Area'),
    ('BeniyaMachishuuhen', 'Beniya Town Area'),
    ('NishiKoisoShuuhen', 'Nishi-Koiso Area'),
    ('OomiyaMachishuuhen', 'Omiya Town Area'),
    ('OotemachiShuuhen', 'Otemachi Area'),
    ('TounosawaShuuhen', 'Tonosawa Area'),
    ('ShiroyamaShuuhen', 'Shiroyama Area'),
    ('NarumiMachishuuhen', 'Narumi Town Area'),
    ('ShounoMachishuuhen', 'Shono Town Area'),
    ('HigashichouShuuhen', 'Higashicho Area'),
    ('KyoumachiShuuhen', 'Kyomachi Area'),
    ('MotomachiShuuhen', 'Motomachi Area'),
    ('OutemachiShuuhen', 'Otemachi Area'),
    ('TomoechouShuuhen', 'Tomoe Town Area'),
    ('DenmachouShuuhen', 'Denmacho Area'),
    ('NakamachiShuuhen', 'Nakamachi Area'),
    ('TakaoMachishuuhen', 'Takao Town Area'),
    ('NakaizumiShuuhen', 'Nakaizumi Area'),
    ('ShirasukaShuuhen', 'Shirasuka Area'),
    ('UomachiShuuhen', 'Uomachi Area'),
    ('HonchouShuuhen', 'Honcho Area'),
    ('KanbaraShuuhen', 'Kanbara Area'),
    ('NissakaShuuhen', 'Nissaka Area'),
    ('OkabechouOkabe', 'Okabe Town, Okabe'),
    ('NaiTaniShuuhen', 'Naitani Area'),
    ('OoichouShuuhen', 'Oi Town Area'),
    ('MarukoShuuhen', 'Maruko Area'),
    ('AoiKuGofukuchou', 'Aoi-ku, Gofukucho'),
    ('NakaGunOiso', 'Naka District, Oiso'),
    ('HigashiKoiso', 'Higashi-Koiso'),
    ('HaraShuuhen', 'Hara Area'),
    ('YuiShuuhen', 'Yui Area'),
    ('OojiShuuhen', 'Oji Area'),
    ('\\(KyuuNakaku\\)Chuushinbu', 'Central Area (Former Naka Ward)'),
    ('Chuushinbu', 'Central Area'),
    ('KanChoubokuSaki', 'Kan Town, Bokusaki'),
    ('FudakiMachi', 'Fudaki Town'),
    ('YasuoMachi', 'Yasuo Town'),
    ('SenbaMachi', 'Senba Town'),
    ('SuwaSakae', 'Suwa Sakae'),
])

# 駅名の英語化マッピング
station_fixes = OrderedDict([
    ('AtsutaJinguuDenmachou', 'Atsuta Jingu Denmacho'),
    ('MizuguchiIshibashi', 'Mizuguchi-Ishibashi'),
    ('YoshiharaHonchou', 'Yoshiwara-Honcho'),
    ('Izuhakonetetsudou', 'Izu-Hakone Railway'),
    ('KyoutoshiYakushoMae', 'Kyoto City Hall'),
    ('MishimaHirokouji', 'Mishima-Hirokoji'),
    ('FudakiTeiryuujou', 'Fudaki Stop'),
    ('HigashiKanagawa', 'Higashi-Kanagawa'),
    ('KeikyuKawasaki', 'Keikyu Kawasaki'),
    ('HoTsuchiKeTani', 'Hodogaya'),
    ('MeidenAkasaka', 'Meitetsu Akasaka'),
    ('GakunanDensha', 'Gakunan Railway'),
    ('Oumitetsudou', 'Ohmi Railway'),
    ('ShinKanbara', 'Shin-Kanbara'),
    ('ShieiSubway', 'Municipal Subway'),
    ('Romendensha', 'Tram'),
    ('MeidenGoyu', 'Meitetsu Goyu'),
    ('Tennouchou', 'Tennocho'),
    ('TenHamaSen', 'Tenryu Hamanako Railway'),
    ('TaiyuuYama', 'Daiyuzan'),
    ('Jinguumae', 'Jingu-mae'),
    ('KouNoDen', 'Enoden'),
    ('BasuRiyou', 'Bus Available'),
    ('TakushiiNado', 'Taxi etc.'),
    ('BasuNado', 'Bus etc.'),
    ('KasaTou', 'Kasado'),
    ('Sanjou', 'Sanjo'),
])

print("\n【1. 住所の英語化】")

# 住所を修正
for pattern, replacement in address_fixes.items():
    count = en_html.count(pattern)
    if count > 0:
        en_html = en_html.replace(pattern, replacement)
        changes['addresses'] += count
        print(f"  {pattern} → {replacement} ({count}箇所)")

print(f"\n  合計: {changes['addresses']}箇所")

print("\n【2. 駅名の英語化】")

# 駅名を修正
for pattern, replacement in station_fixes.items():
    count = en_html.count(pattern)
    if count > 0:
        en_html = en_html.replace(pattern, replacement)
        changes['stations'] += count
        print(f"  {pattern} → {replacement} ({count}箇所)")

print(f"\n  合計: {changes['stations']}箇所")

print("\n【3. その他の英語化】")

# 全角括弧を半角に
old_count = en_html.count('（') + en_html.count('）')
en_html = en_html.replace('（', '(')
en_html = en_html.replace('）', ')')
changes['other'] += old_count
print(f"  全角括弧を半角に変換: {old_count}箇所")

# ※記号を英語化
old_count = en_html.count('※')
en_html = en_html.replace('※', 'Note: ')
changes['other'] += old_count
print(f"  ※を'Note: 'に変換: {old_count}箇所")

print(f"\n  合計: {changes['other']}箇所")

# ファイルに書き込み
en_html_path.write_text(en_html, encoding='utf-8')

# 最終結果
print("\n" + "=" * 80)
print("✅ Phase 2.10 完全英語化完了")
print(f"   住所: {changes['addresses']}箇所")
print(f"   駅名: {changes['stations']}箇所")
print(f"   その他: {changes['other']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
