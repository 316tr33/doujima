#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
お遍路英語版 Phase 3B適用スクリプト: 電話番号の国際形式化
088-xxx-xxxx → +81-88-xxx-xxxx
"""

import re
from pathlib import Path

# ファイルパス
en_html_path = Path(__file__).parent.parent / "Ohenro/en/shikoku.html"
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("お遍路英語版 Phase 3B: 電話番号の国際形式化")
print("=" * 80)

def convert_to_international(phone):
    """
    日本の電話番号を国際形式に変換
    例: 088-689-1111 → +81-88-689-1111
        0883-36-3010 → +81-883-36-3010
    """
    # 先頭の0を削除して+81を追加
    phone = phone.strip()
    if phone.startswith('0'):
        return '+81-' + phone[1:]
    return phone

# 電話番号パターンを検索して国際形式に変換
modified_html = en_html
update_count = 0

# パターン: <p class="card-small-text">電話: 0xx-xxx-xxxx</p>
pattern = r'(<p class="card-small-text">)(電話: )(0\d{1,4}-\d{1,4}-\d{4})(</p>)'

def replace_phone(match):
    global update_count
    update_count += 1

    opening_tag = match.group(1)
    label = match.group(2)
    phone_number = match.group(3)
    closing_tag = match.group(4)

    # 国際形式に変換
    international_phone = convert_to_international(phone_number)

    # 返却
    return f'{opening_tag}Tel: {international_phone}{closing_tag}'

modified_html = re.sub(pattern, replace_phone, modified_html)

print(f"\n更新した電話番号: {update_count}箇所")

# 結果を保存
en_html_path.write_text(modified_html, encoding='utf-8')
print(f"\nPhase 3B適用完了: {en_html_path}")

# 検証用サマリー
print("\n【修正サマリー】")
print(f"✓ 電話番号の国際形式化: {update_count}箇所")
print(f"  - 形式: 「電話: 0xx-xxx-xxxx」→「Tel: +81-xx-xxx-xxxx」")
print("=" * 80)
