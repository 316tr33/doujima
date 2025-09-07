#!/bin/bash

# WebP変換スクリプト
# 使用方法: ./convert-to-webp.sh

echo "🖼️  画像のWebP変換を開始します..."

# cwebpコマンドの存在確認
if ! command -v cwebp &> /dev/null; then
    echo "❌ cwebpがインストールされていません。"
    echo "インストール方法:"
    echo "  macOS: brew install webp"
    echo "  Ubuntu/Debian: sudo apt-get install webp"
    echo "  CentOS/RHEL: sudo yum install libwebp-tools"
    exit 1
fi

# 変換対象のディレクトリ
IMAGE_DIR="../images"
CONVERTED_COUNT=0
SKIPPED_COUNT=0

# JPEG/PNG画像を検索してWebPに変換
find "$IMAGE_DIR" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | while read -r file; do
    # 出力ファイル名
    webp_file="${file%.*}.webp"
    
    # すでにWebP版が存在する場合はスキップ
    if [ -f "$webp_file" ]; then
        echo "⏭️  スキップ: $(basename "$file") (WebP版が既に存在)"
        ((SKIPPED_COUNT++))
        continue
    fi
    
    # WebPに変換
    echo "🔄 変換中: $(basename "$file") → $(basename "$webp_file")"
    
    # 画質設定（JPEGは85、PNGは可逆圧縮）
    if [[ "$file" == *.png ]]; then
        cwebp -lossless "$file" -o "$webp_file"
    else
        cwebp -q 85 "$file" -o "$webp_file"
    fi
    
    if [ $? -eq 0 ]; then
        # ファイルサイズ比較
        original_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        webp_size=$(stat -f%z "$webp_file" 2>/dev/null || stat -c%s "$webp_file" 2>/dev/null)
        reduction=$((100 - (webp_size * 100 / original_size)))
        
        echo "✅ 成功: $(basename "$webp_file") (サイズ削減: ${reduction}%)"
        ((CONVERTED_COUNT++))
    else
        echo "❌ エラー: $(basename "$file") の変換に失敗"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 変換完了!"
echo "  新規変換: ${CONVERTED_COUNT}枚"
echo "  スキップ: ${SKIPPED_COUNT}枚"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# HTML内の画像参照を更新する提案
echo ""
echo "💡 次のステップ:"
echo "1. HTMLファイル内の画像参照を更新"
echo "2. <picture>要素でWebPとフォールバックを実装"
echo ""
echo "例:"
echo '<picture>'
echo '  <source srcset="image.webp" type="image/webp">'
echo '  <img src="image.jpg" alt="説明">'
echo '</picture>'