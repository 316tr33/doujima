#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 2 翻訳検証スクリプト
英語版HTMLの翻訳完了を確認
"""

import re
from pathlib import Path
from tokaido_station_names_en import STATION_NAMES_FULL_EN
from tokaido_descriptions_en import DESCRIPTIONS_EN

en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"
en_html = en_html_path.read_text(encoding='utf-8')

print('=' * 80)
print('東海道英語版 Phase 2 翻訳検証')
print('=' * 80)

all_ok = True
errors = []

# 1. 宿場名の英語化確認
print('\n【1. 宿場名の英語化】')
english_names_found = 0
japanese_names_found = 0

for data_num, english_name in STATION_NAMES_FULL_EN.items():
    pattern = rf'data-number="{data_num}".*?<h3>(.+?)</h3>'
    match = re.search(pattern, en_html, re.DOTALL)

    if match:
        h3_content = match.group(1).strip()
        # 英語名が含まれているか確認
        if english_name in h3_content:
            english_names_found += 1
        else:
            # 日本語文字が残っているか確認（ひらがな、カタカナ、漢字）
            if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', h3_content):
                japanese_names_found += 1
                print(f'✗ {data_num}番: 日本語が残存「{h3_content}」（期待: {english_name}）')
                all_ok = False
                errors.append(f'{data_num}番宿場名未翻訳')

if english_names_found == 55 and japanese_names_found == 0:
    print(f'✓ 55箇所すべて英語化完了')
else:
    print(f'✗ 英語: {english_names_found}箇所, 日本語残存: {japanese_names_found}箇所')
    if english_names_found != 55:
        all_ok = False
        errors.append('宿場名英語化未完了')

# 2. 読み仮名の削除確認
print('\n【2. 読み仮名の削除】')
reading_count = len(re.findall(r'<div class="station-reading">', en_html))
if reading_count == 0:
    print(f'✓ 読み仮名完全削除')
else:
    print(f'✗ {reading_count}箇所の読み仮名が残存')
    all_ok = False
    errors.append('読み仮名削除未完了')

# 3. 説明文の英語化確認
print('\n【3. 説明文の英語化】')
english_desc_found = 0
japanese_desc_found = 0

for data_num in range(55):
    pattern = rf'data-number="{data_num}".*?<p class="station-description">\s*(.+?)\s*</p>'
    match = re.search(pattern, en_html, re.DOTALL)

    if match:
        desc_content = match.group(1).strip()
        # 日本語文字が残っているか確認
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', desc_content):
            japanese_desc_found += 1
            print(f'✗ {data_num}番: 日本語説明文が残存「{desc_content[:50]}...」')
            all_ok = False
            errors.append(f'{data_num}番説明文未翻訳')
        else:
            english_desc_found += 1

if english_desc_found == 55 and japanese_desc_found == 0:
    print(f'✓ 55箇所すべて英語化完了')
else:
    print(f'✗ 英語: {english_desc_found}箇所, 日本語残存: {japanese_desc_found}箇所')
    if english_desc_found != 55:
        all_ok = False
        errors.append('説明文英語化未完了')

# 4. ハイライトの英語化確認
print('\n【4. ハイライトの英語化】')
highlights_sections = re.findall(r'<div class="station-highlights">(.*?)</div>', en_html, re.DOTALL)
total_highlight_spans = 0
japanese_highlight_spans = 0

for section in highlights_sections:
    spans = re.findall(r'<span>([^<]+)</span>', section)
    for span_text in spans:
        total_highlight_spans += 1
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', span_text):
            japanese_highlight_spans += 1

if japanese_highlight_spans == 0:
    print(f'✓ {total_highlight_spans}箇所すべて英語化完了')
else:
    print(f'✗ 合計{total_highlight_spans}箇所中、{japanese_highlight_spans}箇所に日本語が残存')
    all_ok = False
    errors.append('ハイライト英語化未完了')

# 5. 詳細情報ラベルの英語化確認
print('\n【5. 詳細情報ラベルの英語化】')
japanese_labels = ['見学時間：', '最寄り駅：', '住所：', '所在地：', '交通：', 'アクセス：', '営業時間：', '入場料：']
english_labels = ['Visit Time: ', 'Nearest Station: ', 'Address: ', 'Location: ', 'Access: ', 'Hours: ', 'Admission: ']

japanese_label_count = sum(en_html.count(label) for label in japanese_labels)
english_label_count = sum(en_html.count(label) for label in english_labels)

if japanese_label_count == 0 and english_label_count > 0:
    print(f'✓ 日本語ラベル: 0箇所, 英語ラベル: {english_label_count}箇所')
else:
    print(f'✗ 日本語ラベル: {japanese_label_count}箇所, 英語ラベル: {english_label_count}箇所')
    if japanese_label_count > 0:
        for label in japanese_labels:
            count = en_html.count(label)
            if count > 0:
                print(f'  残存: {label} ({count}箇所)')
        all_ok = False
        errors.append('詳細ラベル英語化未完了')

# 6. HTMLタグバランス（Phase 1からの継続チェック）
print('\n【6. HTMLタグバランス】')
for tag in ['div', 'section', 'main']:
    open_count = len(re.findall(rf'<{tag}[^>]*>', en_html))
    close_count = len(re.findall(rf'</{tag}>', en_html))

    if open_count == close_count:
        print(f'✓ <{tag}>: 開{open_count}/閉{close_count}（バランスOK）')
    else:
        print(f'✗ <{tag}>: 開{open_count}/閉{close_count}（不一致）')
        all_ok = False
        errors.append(f'<{tag}>タグ不一致')

# 最終結果
print('\n' + '=' * 80)
if all_ok:
    print('🎉 Phase 2検証: 100点満点！')
    print('📊 英語版の翻訳が完全に完了しています')
    print('\n【検証合格項目】')
    print('  ✓ 宿場名: 55箇所すべて英語化')
    print('  ✓ 読み仮名: 完全削除')
    print('  ✓ 説明文: 55箇所すべて英語化')
    print('  ✓ ハイライト: すべて英語化')
    print('  ✓ 詳細ラベル: すべて英語化')
    print('  ✓ HTMLタグバランス: 維持')
    print('=' * 80)
    exit(0)
else:
    print(f'❌ Phase 2検証: {len(errors)}件のエラー')
    print('\n【エラー一覧】')
    for i, error in enumerate(errors, 1):
        print(f'{i}. {error}')
    print('=' * 80)
    exit(1)
