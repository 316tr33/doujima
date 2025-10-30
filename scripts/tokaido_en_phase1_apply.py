#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
東海道英語版 Phase 1 データ適用スクリプト
抽出した日本語版データを英語版HTMLに適用
"""

import re
import json
from pathlib import Path

# ファイルパス
json_path = Path(__file__).parent / "tokaido_stations_data.json"
en_html_path = Path(__file__).parent.parent / "Tokaido/en/stations.html"

# JSONデータを読み込み
station_data = json.loads(json_path.read_text(encoding='utf-8'))
en_html = en_html_path.read_text(encoding='utf-8')

print("=" * 80)
print("東海道英語版 Phase 1: データ適用")
print("=" * 80)

# 既存のstations-gridセクションを抽出（削除対象）
# stations-gridの開始から、その終了</div>までを取得
old_cards_pattern = r'(<div class="stations-grid">)(.*?)(</div>)\s*(?=</div>\s*</div>\s*</section>)'
old_cards_match = re.search(old_cards_pattern, en_html, re.DOTALL)

if not old_cards_match:
    print("❌ エラー: stations-gridセクションが見つかりません")
    exit(1)

# 新しいHTMLを生成
def generate_station_card(station):
    """駅カードHTMLを生成"""
    # バッジのHTML生成
    badges_html = ""
    if station['badges']:
        badges_items = "\n      ".join([
            f'<span class="badge {get_badge_class(badge)}">{badge}</span>'
            for badge in station['badges']
        ])
        badges_html = f"""<div class="station-badges">
      {badges_items}
    </div>"""
    
    # ハイライトのHTML生成
    highlights_html = ""
    if station['highlights']:
        highlights_items = "\n      ".join([
            f'<span>{highlight}</span>'
            for highlight in station['highlights']
        ])
        highlights_html = f"""<div class="station-highlights">
      {highlights_items}
    </div>"""
    
    # コメントマーカー（通常の宿場のみ）
    comment = ""
    if 'comment_number' in station:
        comment = f"<!-- {station['comment_number']}宿 {station['comment_name']} -->\n    "
    
    # カードHTML
    card_html = f"""{comment}<div
      class="station-card {station['classes']}"
      data-number="{station['data_number']}"
      data-features="{station['data_features']}"
    >
      <div class="station-image">
        <img
          src="{station['image_src']}"
          alt="{station['image_alt']}"
          loading="lazy"
        />
        <div class="station-number">{station['display_number']}</div>
        {badges_html}
      </div>
      <div class="station-info">
        <h3>{station['name']}</h3>
        <div class="station-reading">{station['reading']}</div>
        <p class="station-description">
          {station['description']}
        </p>
        
        <div class="station-details">

          <div class="detail-item">

            <i class="fas fa-map-marker-alt"></i>

            <span>{station['address']}</span>

          </div>

          <div class="detail-item">

            <i class="fas fa-train"></i>

            <span>{station['station_info']}</span>

          </div>

          <div class="detail-item">

            <i class="fas fa-clock"></i>

            <span>{station['visit_time']}</span>

          </div>

        </div>

        {highlights_html}
      </div>
    </div>"""
    
    return card_html

def get_badge_class(badge_text):
    """バッジのテキストからクラス名を取得"""
    badge_map = {
        '風景名所': 'scenic',
        '歴史名所': 'history',
        'グルメ': 'gourmet',
        '温泉': 'onsen',
        '初心者': 'beginner',
        '特別': 'special'
    }
    return badge_map.get(badge_text, 'history')

# 起点（日本橋）のHTML生成
special_start = [s for s in station_data['special_stations'] if s['data_number'] == 0][0]
start_html = generate_station_card(special_start)

# 通常の宿場のHTML生成（1-53番）
regular_html = "\n\n    ".join([
    generate_station_card(station)
    for station in sorted(station_data['regular_stations'], key=lambda x: x['data_number'])
])

# 終点（三条大橋）のHTML生成
special_end = [s for s in station_data['special_stations'] if s['data_number'] == 54][0]
end_html = generate_station_card(special_end)

# 新しいstations-gridセクション（開始タグを保持、内容を置換、終了タグを保持）
new_content = f"""
            {start_html}

            {regular_html}

            {end_html}
          """

# HTMLを更新（グループ1=開始タグ, グループ2=旧内容, グループ3=終了タグ）
updated_html = en_html.replace(
    old_cards_match.group(0),
    old_cards_match.group(1) + new_content + old_cards_match.group(3)
)

# ファイルに書き込み
en_html_path.write_text(updated_html, encoding='utf-8')

print("\n" + "=" * 80)
print("✅ データ適用完了")
print(f"   起点・終点: {len(station_data['special_stations'])}箇所")
print(f"   宿場: {len(station_data['regular_stations'])}箇所")
print(f"   合計: {station_data['total']}箇所")
print(f"   更新ファイル: {en_html_path}")
print("=" * 80)
