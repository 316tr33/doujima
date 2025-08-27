# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 重要：言語設定

**すべての回答とコミュニケーションは必ず日本語で行ってください。**

## プロジェクト概要

堂島フロント企画の企業サイト。お遍路事業と東海道ウォーク事業を中心とした多事業展開企業の公式ウェブサイト。静的 HTML で構築されたマルチビジネス対応サイトです。

## 開発コマンド

**このプロジェクトは静的 HTML サイトです。**

- **開発環境**: ライブサーバー（VSCode Live Server 推奨）
- **テスト**: ブラウザで直接テスト
- **ビルド**: 不要（静的ファイル）
- **デプロイ**: 静的ホスティングサービスに直接アップロード

## アーキテクチャ

### コアファイル構成

- `index.html` - 企業ホームページ（堂島フロント企画の事業案内）
- `Ohenro/index.html` - お遍路事業メインページ
- `Ohenro/shikoku.html` - 各霊場の詳細ページ
- `Tokaido/index.html` - 東海道ウォーク事業ページ
- `css/style.css` - 共通 CSS（1016 行、企業ページ含む）
- `css/ohenro.css` - お遍路専用 CSS（1966 行）
- `script.js` - JavaScript 機能（518 行）

### 主要システム

#### STEP 学習システム（.compact-original-learning）

3 段階のお遍路入門チュートリアル：

- `.compact-step` - 各 STEP のコンテナ
- `.step-header` + `.step-number` + `.step-title` - STEP 見出し
- `.step-content` - 動画 + 解説エリア（グリッドレイアウト）
- `.step-video` - YouTube 埋め込み
- `.step-description` - 詳細解説（`.quick-points`, `.worship-flow`等の子要素）

#### 県別グリッド（.prefecture-grid）

4 県（徳島、高知、愛媛、香川）のカード表示：

- `.prefecture-block` - Flexbox 縦配置のカードコンテナ
- `.prefecture-header` - 背景画像エリア（aspect-ratio: 1.8/1）
- `.prefecture-simple` - 札所情報エリア（画像下配置）
- 道場名（h4）は`display: none`、県名（p）のみ表示が設計仕様

#### スライドショー（.hero）

- 5 枚画像の自動切り替え（6 秒間隔）
- プログレスバー（.horizontal-progress）とドットナビゲーション
- DOM 要素キャッシュ最適化済み

#### デュアルナビゲーション

- 固定ヘッダー（nav + .nav-links）
- サイド縦書きナビ（.vertical-nav）- 右端からスライドイン

### デザイン・CSS 構造

#### テーマ設計

- **カラーパレット**: 金色（#b8860b, #d4af37）+ 黒背景
- **フォント**: Noto Serif JP（縦書き対応）
- **レスポンシブ**: 3 段階（1024px, 768px, 480px）

#### CSS 分割最適化

- **css/style.css**: 共通スタイル + 企業ページ（1016 行）
- **css/ohenro.css**: お遍路専用スタイル（1966 行）
- 未使用学習レイアウト削除済み（pilgrimage-learning-steps 等）
- 重複メディアクエリ統合済み

### JavaScript 設計

#### 初期化パターン

```javascript
// DOMContentLoaded内での順序
1. initSlideshow()     // スライドショー
2. initAnimations()    // アニメーション
3. initSmoothScroll()  // スムーススクロール
4. initNavigation()    // ナビゲーション
5. initDOMCache()      // DOMキャッシュ
```

#### DOM 最適化

- 要素は初期化時に 1 回取得してキャッシュ
- requestAnimationFrame 使用
- パララックス・パーティクル機能は無効化済み

## 重要な修正ルール

### prefecture-grid 修正時

- `.prefecture-header h4` (道場名) は`display: none`必須
- `.prefecture-header p` (県名) のみ表示、左上配置
- `.prefecture-simple` は画像外の下部に配置
- ホバー時の金色オーバーレイで統一感維持

### CSS 修正時

- **ファイル選択**:
  - 企業ページ関連 → `css/style.css`
  - お遍路機能関連 → `css/ohenro.css`
- セクションコメント（`/* */`）で対象エリアを正確に特定
- z-index 階層: ヘッダー(3) > ナビ(99-100) > コンテンツ(1-15)
- レスポンシブはファイル後半に配置済み

### JavaScript 修正時

- DOM 要素は必ずキャッシュして再利用
- エラーハンドリングは console.log()パターンに統一
- 初期化は必ず DOMContentLoaded イベント内
