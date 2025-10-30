# Playwright MCP スクリーンショット設定ガイド

## 概要

このプロジェクトでは、Playwright MCPを使用したスクリーンショット撮影時に5MB制限エラーを回避するための設定を実装しています。

## 問題点

- デフォルトのPNG形式では、スクリーンショットが5MBを超える可能性がある
- Claude Codeは5MB以上の画像を処理できず、エラーで中断される

## 解決策

### 1. プロジェクト設定ファイル

`playwright-mcp.config.json` を作成し、以下の最適化を実施：

```json
{
  "browser": {
    "browserName": "chromium",
    "launchOptions": {
      "headless": false
    },
    "contextOptions": {
      "viewport": {
        "width": 1280,
        "height": 720
      },
      "deviceScaleFactor": 1
    }
  },
  "outputDir": ".playwright-mcp",
  "imageResponses": "allow"
}
```

**設定の効果：**
- ビューポートサイズ: 1280x720（720pに制限）
- デバイススケールファクター: 1（Retinaディスプレイの2倍解像度を無効化）
- 出力ディレクトリ: `.playwright-mcp`（自動管理）

### 2. JPEG形式の使用（最重要）

スクリーンショット撮影時は**必ずJPEG形式を指定**してください：

```javascript
// ❌ 悪い例（PNG - 大きいファイルサイズ）
browser_take_screenshot()

// ✅ 良い例（JPEG - 約1/3のファイルサイズ）
browser_take_screenshot({
  "type": "jpeg",
  "filename": "screenshot.jpeg"
})
```

### 3. .gitignore設定

`.playwright-mcp/` ディレクトリは自動生成ファイルのため、Gitから除外されています：

```gitignore
# Playwright MCPスクリーンショット（自動生成）
.playwright-mcp/
playwright-mcp.config.json
```

## 使用方法

### Claude Codeでの実行

Playwright MCPツールを使用する際は、以下のパターンで実行してください：

```
スクリーンショットを撮影してください
→ JPEG形式で、ファイル名は "page-analysis.jpeg" でお願いします
```

### サイズ比較

**同じページの例：**
- PNG形式（デフォルト）: 約5.2MB → エラー発生
- JPEG形式（推奨）: 約1.5MB → 問題なし
- JPEG + 解像度制限: 約800KB → 最適

## トラブルシューティング

### 🚨 エラーループから抜け出せない場合（最重要）

**症状**: 最初のエラー後、どんな指示を出しても同じ5MBエラーが返ってくる

**原因**: 大きなPNG画像がキャッシュに残り、繰り返し読み込まれている

**即座の解決策**:
```bash
# すべてのPNG画像を削除（緊急時）
rm -rf .playwright-mcp/*.png

# または、ディレクトリ全体をクリーンアップ
rm -rf .playwright-mcp/*
```

**その後の対応**:
1. 新しい会話セッションを開始
2. または「スクリーンショットをJPEG形式で再撮影してください」と明示的に指示

### エラーが継続する場合

1. **解像度をさらに下げる**
   ```json
   "viewport": {
     "width": 1024,
     "height": 576
   }
   ```

2. **フルページスクリーンショットを避ける**
   - `fullPage: true` は使用しない
   - 必要な部分のみを撮影

3. **定期的なクリーンアップ（推奨）**
   ```bash
   # 作業終了時に実行
   rm -rf .playwright-mcp/*
   ```

## ファイルサイズの目安

| 設定 | 推定サイズ | 5MB制限 |
|------|------------|---------|
| PNG 1920x1080 | 4-6MB | ⚠️ 危険 |
| PNG 1280x720 | 2-3MB | ✅ 安全 |
| JPEG 1920x1080 | 1.5-2MB | ✅ 安全 |
| JPEG 1280x720 | 0.8-1.2MB | ✅ 最適 |

## 推奨設定

**最も安全で効果的な組み合わせ：**
- ✅ JPEG形式
- ✅ 1280x720解像度
- ✅ deviceScaleFactor: 1
- ✅ fullPage: false

これにより、ほぼ100%の確率で5MB制限内に収まります。
