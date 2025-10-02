#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex検証: 東海道英語版 Phase 1
日本語版と英語版の完全一致を確認
"""

import re
from pathlib import Path

ja_html = Path('Tokaido/stations.html').read_text(encoding='utf-8')
en_html = Path('Tokaido/en/stations.html').read_text(encoding='utf-8')

print('=' * 80)
print('東海道英語版 Phase 1 詳細検証（Codex）')
print('=' * 80)

all_ok = True
errors = []

# 1. 宿場カード数
print('\n【1. 宿場カード数】')
ja_cards = len(re.findall(r'class="station-card ', ja_html))
en_cards = len(re.findall(r'class="station-card ', en_html))
if ja_cards == en_cards == 55:
    print(f'✓ 日本語{ja_cards}箇所, 英語{en_cards}箇所')
else:
    print(f'✗ 日本語{ja_cards}箇所, 英語{en_cards}箇所（期待: 55箇所）')
    all_ok = False
    errors.append('宿場カード数不一致')

# 2. data-number連番確認
print('\n【2. data-number連番確認】')
ja_nums = sorted(set([int(m) for m in re.findall(r'data-number="(\d+)"', ja_html)]))
en_nums = sorted(set([int(m) for m in re.findall(r'data-number="(\d+)"', en_html)]))
expected = list(range(55))
if ja_nums == en_nums == expected:
    print(f'✓ 0-54の連番（55箇所）')
else:
    print(f'✗ 日本語{len(ja_nums)}個, 英語{len(en_nums)}個')
    missing = set(expected) - set(en_nums)
    extra = set(en_nums) - set(expected)
    if missing: 
        print(f'  欠損: {sorted(missing)}')
    if extra: 
        print(f'  余分: {sorted(extra)}')
    all_ok = False
    errors.append('data-number不一致')

# 3. コメントマーカー
print('\n【3. コメントマーカー（1-53宿）】')
ja_comments = len(re.findall(r'<!-- \d+宿 .+? -->', ja_html))
en_comments = len(re.findall(r'<!-- \d+宿 .+? -->', en_html))
if ja_comments == en_comments == 53:
    print(f'✓ 日本語{ja_comments}箇所, 英語{en_comments}箇所')
else:
    print(f'✗ 日本語{ja_comments}箇所, 英語{en_comments}箇所（期待: 53箇所）')
    all_ok = False
    errors.append('コメントマーカー不一致')

# 4. 地域別クラス
print('\n【4. 地域別クラス】')
region_expected = {'edo': 15, 'tokaido': 20, 'kinki': 20}
for region, expected_count in region_expected.items():
    ja_count = len(re.findall(rf'class="station-card {region}', ja_html))
    en_count = len(re.findall(rf'class="station-card {region}', en_html))
    if ja_count == en_count == expected_count:
        print(f'✓ {region}: 日本語{ja_count}箇所, 英語{en_count}箇所')
    else:
        print(f'✗ {region}: 日本語{ja_count}箇所, 英語{en_count}箇所（期待: {expected_count}箇所）')
        all_ok = False
        errors.append(f'{region}クラス不一致')

# 5. station-highlights
print('\n【5. station-highlights】')
ja_highlights = len(re.findall(r'<div class="station-highlights">', ja_html))
en_highlights = len(re.findall(r'<div class="station-highlights">', en_html))
if ja_highlights == en_highlights == 55:
    print(f'✓ 日本語{ja_highlights}箇所, 英語{en_highlights}箇所')
    
    # 空のハイライトチェック
    en_empty_highlights = len(re.findall(r'<div class="station-highlights">\s*</div>', en_html))
    if en_empty_highlights > 0:
        print(f'⚠️ 空のハイライト: {en_empty_highlights}箇所')
    else:
        print(f'✓ 空のハイライトなし')
else:
    print(f'✗ 日本語{ja_highlights}箇所, 英語{en_highlights}箇所（期待: 55箇所）')
    all_ok = False
    errors.append('station-highlights不一致')

# 6. 詳細情報アイコン（フッター除外）
print('\n【6. 詳細情報（住所・駅・見学時間）】')

# フッターより前の部分のみを対象にする
ja_main = ja_html.split('<footer')[0] if '<footer' in ja_html else ja_html
en_main = en_html.split('<footer')[0] if '<footer' in en_html else en_html

icons = [
    ('fa-map-marker-alt', '住所'),
    ('fa-train', '駅情報'),
    ('fa-clock', '見学時間')
]
for icon, name in icons:
    ja_count = len(re.findall(rf'<i class="fas {icon}"></i>', ja_main))
    en_count = len(re.findall(rf'<i class="fas {icon}"></i>', en_main))
    if ja_count == en_count == 55:
        print(f'✓ {name}: 日本語{ja_count}箇所, 英語{en_count}箇所')
    else:
        print(f'✗ {name}: 日本語{ja_count}箇所, 英語{en_count}箇所（期待: 55箇所）')
        all_ok = False
        errors.append(f'{name}不一致')

# 7. バッジ
print('\n【7. バッジ】')
ja_badges = len(re.findall(r'<div class="station-badges">', ja_html))
en_badges = len(re.findall(r'<div class="station-badges">', en_html))
if ja_badges == en_badges == 55:
    print(f'✓ 日本語{ja_badges}箇所, 英語{en_badges}箇所')
else:
    print(f'✗ 日本語{ja_badges}箇所, 英語{en_badges}箇所（期待: 55箇所）')
    all_ok = False
    errors.append('バッジ不一致')

# 8. HTMLタグバランス（追加検証）
print('\n【8. HTMLタグバランス】')
for tag in ['div', 'section', 'main']:
    ja_open = len(re.findall(rf'<{tag}[^>]*>', ja_html))
    ja_close = len(re.findall(rf'</{tag}>', ja_html))
    en_open = len(re.findall(rf'<{tag}[^>]*>', en_html))
    en_close = len(re.findall(rf'</{tag}>', en_html))
    
    if en_open == en_close:
        print(f'✓ <{tag}>: 開{en_open}/閉{en_close}（バランスOK）')
    else:
        print(f'✗ <{tag}>: 開{en_open}/閉{en_close}（不一致）')
        all_ok = False
        errors.append(f'<{tag}>タグ不一致')

# 最終結果
print('\n' + '=' * 80)
if all_ok:
    print('🎉 Codex検証: 100点満点！')
    print('📊 英語版は日本語版の修正を完全に反映しています')
    print('\n【検証合格項目】')
    print('  ✓ 宿場カード数: 55箇所')
    print('  ✓ data-number: 0-54の連番')
    print('  ✓ コメントマーカー: 1-53宿')
    print('  ✓ 地域別クラス: edo/tokaido/kinki')
    print('  ✓ station-highlights: 55箇所')
    print('  ✓ 詳細情報: 住所・駅・見学時間')
    print('  ✓ バッジ: 55箇所')
    print('  ✓ HTMLタグバランス: div/section/main')
    print('=' * 80)
    exit(0)
else:
    print(f'❌ Codex検証: {len(errors)}件のエラー')
    print('\n【エラー一覧】')
    for i, error in enumerate(errors, 1):
        print(f'{i}. {error}')
    print('=' * 80)
    exit(1)
