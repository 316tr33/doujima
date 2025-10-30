#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 4: station-highlights 最適化
- 長すぎるタグを簡潔化（15文字以内目安）
- 起点・終点を特別感のあるタグに
"""

# 修正が必要な宿場のhighlights（番号: [タグ1, タグ2, タグ3]）
updated_highlights = {
    # 起点・終点
    0: ["五街道起点", "日本の道路元標", "江戸・東京中心"],

    # 長すぎるタグを簡潔化
    3: ["神奈川台関門跡", "開港史跡", "本覚寺"],
    4: ["権太坂の急坂", "東海道古道", "宿場の歴史道"],
    5: ["宿場まつり", "鎌倉道分岐点", "本陣・脇本陣跡"],
    6: ["遊行寺", "江島道分岐", "本陣跡"],
    7: ["相模川渡し場跡", "平塚八幡宮", "七夕まつり"],
    8: ["東海道松並木", "日本初海水浴場", "旧伊藤博文邸"],
    9: ["小田原城", "宿場交流館", "かまぼこ博物館"],
    10: ["箱根関所", "芦ノ湖と富士山", "17の温泉地"],

    # 簡潔すぎるタグを具体化
    14: ["富士山麓の宿場", "岳南電車の街", "製紙産業の歴史"],

    # 終点
    54: ["東海道完歩地点", "豊臣秀吉建立", "鴨川の名橋"]
}

if __name__ == "__main__":
    print("Phase 4: 修正対象のstation-highlights")
    print("="*80)

    for num, tags in sorted(updated_highlights.items()):
        if num == 0:
            name = "起点（日本橋）"
        elif num == 54:
            name = "終点（三条大橋）"
        else:
            name = f"{num}番"

        tags_str = ", ".join(tags)
        max_len = max(len(tag) for tag in tags)

        status = "✓" if max_len <= 15 else "⚠"
        print(f"{status} {name:20s}: {tags_str} (最長{max_len}文字)")

    print(f"\n修正対象: {len(updated_highlights)}箇所")
