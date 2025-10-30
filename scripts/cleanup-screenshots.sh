#!/bin/bash

# Playwright MCP スクリーンショットクリーンアップスクリプト
# 5MBエラーループから抜け出すための緊急対応用

echo "🧹 Playwright MCPスクリーンショットをクリーンアップ中..."

# .playwright-mcpディレクトリが存在するか確認
if [ -d ".playwright-mcp" ]; then
    # ファイル数をカウント
    file_count=$(find .playwright-mcp -type f | wc -l)

    if [ "$file_count" -gt 0 ]; then
        echo "📊 削除対象: $file_count 個のファイル"

        # すべてのファイルを削除
        rm -rf .playwright-mcp/*

        echo "✅ クリーンアップ完了"
    else
        echo "✨ クリーンアップ不要（ディレクトリは既に空です）"
    fi
else
    echo "⚠️  .playwright-mcp ディレクトリが見つかりません"
fi

echo ""
echo "💡 次のステップ:"
echo "   1. 新しい会話セッションを開始"
echo "   2. または Claude に「スクリーンショットをJPEG形式で再撮影」と指示"
