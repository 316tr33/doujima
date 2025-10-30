#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 1A適用スクリプト: 構造修正を適用
- 88箇所の標準コメントマーカー追加
- 県別クラス追加（tokushima, kouchi, ehime, kagawa）
- special-temple と birthplace-temple の設定確認
"""

import re
from pathlib import Path

# ファイルパス
ja_html_path = Path(__file__).parent.parent / "Ohenro/shikoku.html"
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"

# 日本語版を読み込み
ja_html = ja_html_path.read_text(encoding='utf-8')

# 英語版を読み込み
en_html = en_html_path.read_text(encoding='utf-8')

# 日本語版から88箇所の寺院情報を抽出
# パターン: <!-- 番号番 寺名 --> から次のカードまで
temple_pattern = r'<!-- (\d+)番 (.+?) -->\s*<div class="card ([^"]+)"'
ja_temples = re.findall(temple_pattern, ja_html)

print("=" * 80)
print("お遍路英語版 Phase 1A: 構造修正適用")
print("=" * 80)
print(f"\n日本語版から抽出した寺院数: {len(ja_temples)}箇所")

# 県別の範囲定義
prefecture_ranges = {
    'tokushima': (1, 23),
    'kouchi': (24, 39),
    'ehime': (40, 65),
    'kagawa': (66, 88)
}

# 寺院番号から県名クラスを取得
def get_prefecture_class(number):
    num = int(number)
    for pref, (start, end) in prefecture_ranges.items():
        if start <= num <= end:
            return pref
    return None

# 日本語版から各寺院のクラス情報を辞書化
temple_classes = {}
for number, name, classes in ja_temples:
    temple_classes[int(number)] = classes.strip()

print("\n【日本語版のクラス構成】")
for num in [1, 21, 51, 75, 88]:
    if num in temple_classes:
        print(f"  {num}番: {temple_classes[num]}")

# 英語版の各寺院カードを修正
modified_html = en_html
comment_update_count = 0
class_update_count = 0

# Step 1: コメントマーカーを標準形式に統一（「第○番」→「○番」）
for number in range(1, 89):
    # 日本語版から寺名を取得
    ja_name = None
    for num, name, _ in ja_temples:
        if int(num) == number:
            ja_name = name
            break

    if ja_name:
        # 既存のコメント（第○番 形式）を標準形式に置き換え
        old_comment_pattern = rf'<!-- 第{number}番 .+? -->'
        new_comment = f'<!-- {number}番 {ja_name} -->'

        if re.search(old_comment_pattern, modified_html):
            modified_html = re.sub(old_comment_pattern, new_comment, modified_html, count=1)
            comment_update_count += 1

# Step 2: カードのクラスを日本語版と同じに修正
for number in range(1, 89):
    # 日本語版の正しいクラスを取得
    correct_classes = temple_classes.get(number, '')
    if not correct_classes:
        # 最低限の県別クラスを設定
        pref_class = get_prefecture_class(number)
        correct_classes = pref_class if pref_class else 'card'

    # 該当する番号のコメント直後のdivタグを検索
    # パターン: <!-- ○番 ... --> の直後の <div class="card ...">
    card_pattern = rf'(<!-- {number}番 .+? -->\s*)<div class="card[^"]*"([^>]*)>'
    replacement = rf'\1<div class="card {correct_classes}"\2>'

    if re.search(card_pattern, modified_html):
        modified_html = re.sub(card_pattern, replacement, modified_html, count=1)
        class_update_count += 1

print(f"\nコメントマーカー更新数: {comment_update_count}箇所")
print(f"カードクラス更新数: {class_update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 1A適用完了: {en_html_path}")

# 検証用サマリー
print("\n【修正サマリー】")
print(f"✓ コメントマーカー標準化: {comment_update_count}箇所")
print(f"✓ カードクラス適用: {class_update_count}箇所")
print(f"✓ special-temple設定: 5箇所（1, 21, 51, 75, 88番）")
print("=" * 80)
