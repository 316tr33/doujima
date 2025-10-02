#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スクリプトの絶対パスを相対パスに変換
"""

import re
from pathlib import Path

# scriptsディレクトリ内のすべてのPythonファイル
scripts_dir = Path(__file__).parent
script_files = list(scripts_dir.glob("ohenro_en_*.py")) + \
               [scripts_dir / "verify_main_tags.py",
                scripts_dir / "verify_japanese_text.py",
                scripts_dir / "audit_address_data.py"]

# 絶対パスのパターン
absolute_path_pattern = r'Path\("/Users/macmiller/Desktop/doujima/(.*?)"\)'
# 相対パスへの置換（scriptsディレクトリから見た相対パス）
relative_path_template = r'Path(__file__).parent.parent / "\1"'

print("=" * 80)
print("スクリプトの相対パス化")
print("=" * 80)

total_converted = 0

for script_path in script_files:
    if not script_path.exists():
        continue

    content = script_path.read_text(encoding='utf-8')

    # 絶対パスを検索
    absolute_paths = re.findall(absolute_path_pattern, content)

    if absolute_paths:
        # 相対パスに置換
        new_content = re.sub(absolute_path_pattern, relative_path_template, content)

        # ファイルを更新
        script_path.write_text(new_content, encoding='utf-8')

        print(f"\n✓ {script_path.name}")
        print(f"  変換箇所: {len(absolute_paths)}個")
        for path in set(absolute_paths):
            print(f"    - {path}")

        total_converted += len(absolute_paths)

print("\n" + "=" * 80)
print(f"✅ 相対パス化完了: {total_converted}箇所を変換")
print("=" * 80)
