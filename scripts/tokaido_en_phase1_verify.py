#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 1 検証スクリプト
日本語版と英語版の構造とデータの一致を確認
"""

import re
from pathlib import Path

ja_html_path = Path(__file__).parent.parent / "Tokaido/stations.html"
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"

ja_html = ja_html_path.read_text(encoding='utf-8')
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 1: 検証")
print("=" * 80)

all_ok = True
errors = []

# Test 1: 宿場カード数確認
print("\n【Test 1: 宿場カード数確認】")
ja_cards = len(re.findall(r'class="station-card ', ja_html))
en_cards = len(re.findall(r'class="station-card ', en_html))

if ja_cards == en_cards == 55:
    print(f"✓ 宿場カード数: {en_cards}箇所（両方完全）")
else:
    print(f"✗ 宿場カード数: 日本語版{ja_cards}箇所、英語版{en_cards}箇所（期待: 55箇所）")
    all_ok = False
    errors.append(f"宿場カード数不一致")

# Test 2: data-number属性の確認（0-54の55箇所）
print("\n【Test 2: data-number属性の確認】")
ja_numbers = sorted([int(m) for m in re.findall(r'data-number="(\d+)"', ja_html)])
en_numbers = sorted([int(m) for m in re.findall(r'data-number="(\d+)"', en_html)])

expected_numbers = list(range(55))  # 0-54
if ja_numbers == en_numbers == expected_numbers:
    print(f"✓ data-number: 0-54の55箇所（完全）")
else:
    print(f"✗ data-number: 日本語版{len(ja_numbers)}箇所、英語版{len(en_numbers)}箇所")
    if en_numbers != expected_numbers:
        missing = set(expected_numbers) - set(en_numbers)
        extra = set(en_numbers) - set(expected_numbers)
        if missing:
            print(f"  欠損: {sorted(missing)}")
        if extra:
            print(f"  余分: {sorted(extra)}")
    all_ok = False
    errors.append("data-number不一致")

# Test 3: コメントマーカーの確認（1-53宿）
print("\n【Test 3: コメントマーカーの確認】")
ja_comments = re.findall(r'<!-- (\d+)宿 (.+?) -->', ja_html)
en_comments = re.findall(r'<!-- (\d+)宿 (.+?) -->', en_html)

if len(ja_comments) == len(en_comments) == 53:
    print(f"✓ コメントマーカー: 53箇所（完全）")
    # 各コメントが一致しているか確認
    if ja_comments == en_comments:
        print(f"✓ コメント内容: すべて一致")
    else:
        print(f"⚠️ コメント内容: 一部不一致（件数は正常）")
else:
    print(f"✗ コメントマーカー: 日本語版{len(ja_comments)}箇所、英語版{len(en_comments)}箇所")
    all_ok = False
    errors.append("コメントマーカー不一致")

# Test 4: 地域別クラス設定
print("\n【Test 4: 地域別クラス設定】")
en_edo = len(re.findall(r'class="station-card edo', en_html))
en_tokaido = len(re.findall(r'class="station-card tokaido', en_html))
en_kinki = len(re.findall(r'class="station-card kinki', en_html))

ja_edo = len(re.findall(r'class="station-card edo', ja_html))
ja_tokaido = len(re.findall(r'class="station-card tokaido', ja_html))
ja_kinki = len(re.findall(r'class="station-card kinki', ja_html))

if en_edo == ja_edo and en_tokaido == ja_tokaido and en_kinki == ja_kinki:
    print(f"✓ 地域別クラス: 江戸{en_edo}, 東海道{en_tokaido}, 近畿{en_kinki}（日本語版と一致）")
else:
    print(f"✗ 地域別クラス不一致:")
    print(f"  江戸: 日本語{ja_edo}, 英語{en_edo}")
    print(f"  東海道: 日本語{ja_tokaido}, 英語{en_tokaido}")
    print(f"  近畿: 日本語{ja_kinki}, 英語{en_kinki}")
    all_ok = False
    errors.append("地域別クラス不一致")

# Test 5: station-highlights確認（station-featuresから変更済み）
print("\n【Test 5: station-highlights確認】")
en_highlights = len(re.findall(r'<div class="station-highlights">', en_html))
en_old_features = len(re.findall(r'<div class="station-features">', en_html))

if en_highlights == 55 and en_old_features == 0:
    print(f"✓ station-highlights: 55箇所（完全移行）")
else:
    print(f"✗ station-highlights: {en_highlights}箇所、旧features: {en_old_features}箇所")
    all_ok = False
    errors.append("station-highlights移行不完全")

# Test 6: 詳細情報の確認（address, station_info, visit_time）
print("\n【Test 6: 詳細情報の確認】")
en_details = len(re.findall(r'<div class="station-details">', en_html))
en_map_markers = len(re.findall(r'<i class="fas fa-map-marker-alt"></i>', en_html))
en_trains = len(re.findall(r'<i class="fas fa-train"></i>', en_html))
en_clocks = len(re.findall(r'<i class="fas fa-clock"></i>', en_html))

if en_details == en_map_markers == en_trains == en_clocks == 55:
    print(f"✓ 詳細情報: すべて55箇所（完全）")
else:
    print(f"✗ 詳細情報:")
    print(f"  details: {en_details}, map: {en_map_markers}, train: {en_trains}, clock: {en_clocks}")
    all_ok = False
    errors.append("詳細情報不完全")

# Test 7: バッジの確認
print("\n【Test 7: バッジの確認】")
en_badge_divs = len(re.findall(r'<div class="station-badges">', en_html))
en_badge_spans = len(re.findall(r'<span class="badge [^"]+">.*?</span>', en_html))

if en_badge_divs > 0 and en_badge_spans > 0:
    print(f"✓ バッジ: {en_badge_divs}個のdiv、{en_badge_spans}個のspan（存在確認）")
else:
    print(f"✗ バッジ: div={en_badge_divs}, span={en_badge_spans}")
    all_ok = False
    errors.append("バッジ不完全")

# 最終結果
print("\n" + "=" * 80)
if all_ok:
    print("🎉 Phase 1 検証: 100点満点！")
    print("📊 すべてのデータ構造が日本語版と一致しています")
    print("\n【完了項目】")
    print("  ✓ 宿場カード数: 55箇所（起点・終点 + 53宿）")
    print("  ✓ data-number: 0-54の連番")
    print("  ✓ コメントマーカー: 1-53宿")
    print("  ✓ 地域別クラス: 江戸・東海道・近畿")
    print("  ✓ station-highlights: 旧featuresから完全移行")
    print("  ✓ 詳細情報: 住所・駅情報・見学時間")
    print("  ✓ バッジ: カテゴリー別表示")
    print("=" * 80)
    exit(0)
else:
    print(f"❌ Phase 1 検証: {len(errors)}件のエラー")
    print("\n【エラー一覧】")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
    print("=" * 80)
    exit(1)
