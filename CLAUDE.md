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
- `recruit.html` - 採用情報ページ
- `docs/` - 開発ドキュメント（継続使用）
- `refactoring-docs/` - 特定リファクタリングプロジェクト用

### CSS モジュラー構造

プロジェクトは完全なモジュラーCSS構造に移行済み：

#### Base層（基盤）
- `css/base/variables.css` - CSS変数定義（カラー、フォント、サイズ）
- `css/base/reset.css` - ブラウザリセット
- `css/base/typography.css` - フォント・テキスト設定
- `css/base/utilities.css` - ユーティリティクラス
- `css/base/gentle-fix.css` - レスポンシブ修正（モバイル対応）

#### Components層（コンポーネント）
- `css/components/navigation.css` - ナビゲーション（固定ヘッダー、サイドナビ）
- `css/components/buttons.css` - ボタンスタイル
- `css/components/cards.css` - カードコンポーネント
- `css/components/slideshow.css` - スライドショー機能
- `css/components/footer.css` - フッター

#### Pages層（ページ別）
- `css/pages/home.css` - トップページ
- `css/pages/ohenro-*.css` - お遍路関連（base, components, layout, responsive）
- `css/pages/tokaido-*.css` - 東海道関連（base, components, layout, responsive）
- `css/pages/b2b.css` - 採用・B2Bページ

#### 統合ファイル
- `css/style.css` - 企業ページ用統合CSS
- `css/ohenro.css` - お遍路事業用統合CSS
- `css/tokaido.css` - 東海道ウォーク事業用統合CSS（@import構造）

### 主要システム

#### お遍路事業
- **STEP学習システム**: 3段階の入門チュートリアル（.compact-original-learning）
- **県別グリッド**: 4県（徳島、高知、愛媛、香川）のカード表示
- **霊場フィルター**: 88ヶ所霊場の検索・フィルター機能（shikoku.html）

#### 東海道ウォーク事業
- **五十三次ガイド**: 東海道の宿場町情報
- **歴史コンテンツ**: 江戸時代の旅人体験
- **ルートマップ**: 東海道コース案内

#### 共通機能
- **スライドショー**: 5枚画像の自動切り替え（6秒間隔）
- **デュアルナビゲーション**: 固定ヘッダー + サイド縦書きナビ
- **レスポンシブ**: 3段階（1024px, 768px, 480px）

### 霊場フィルター機能（重要）

shikoku.htmlの検索・フィルター機能の修正ルール：

- **カードクラス必須**: JavaScript は `card.classList.contains(filter)` でフィルタリング
- **HTMLクラス構造**: `<div class="card tokushima special-temple" data-category="special">`
- **重要霊場設定**: 1番、21番、51番、75番、88番に `special-temple` クラス必須
- **県別クラス**: 必ず番号範囲に応じた県名クラス（data属性ではなくclass属性）
  - 徳島県（1-23番）: `tokushima`
  - 高知県（24-39番）: `kouchi`
  - 愛媛県（40-65番）: `ehime`
  - 香川県（66-88番）: `kagawa`
- **検索コンテナ**: `.temple-search-container` 内に検索ボックスとフィルターボタン配置

### JavaScript 設計

#### 初期化パターン

```javascript
// DOMContentLoaded内での順序
1. initSlideshow()           // スライドショー
2. initializeAnimations()    // アニメーション
3. initSmoothScroll()        // スムーススクロール
4. initHoverNavigation()     // デスクトップナビゲーション
5. initMobileNavigation()    // モバイルナビゲーション
6. initEnhancedNavEffects()  // ナビエフェクト
7. initVideoGallery()        // 動画ギャラリー
8. initNavigationCache()     // ナビキャッシュ
9. initHeaderCache()         // ヘッダーキャッシュ
10. initYoutubeLazyLoading() // YouTube遅延読み込み
11. initTempleFilter()       // 霊場フィルター（重要）
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
  - 企業ページ関連 → `css/style.css` または base/components層
  - お遍路機能関連 → `css/ohenro.css` または pages/ohenro-*
  - 東海道機能関連 → `css/tokaido.css` または pages/tokaido-*
- セクションコメント（`/* */`）で対象エリアを正確に特定
- z-index 階層: ヘッダー(3) > ナビ(99-100) > コンテンツ(1-15)
- レスポンシブは対応するresponsiveファイルに配置

### JavaScript 修正時

- DOM 要素は必ずキャッシュして再利用
- エラーハンドリングは console.log()パターンに統一
- 初期化は必ず DOMContentLoaded イベント内

### 文字エンコーディング注意事項

- **UTF-8厳守**: すべてのファイルはUTF-8エンコーディング
- **日本語コメント**: プロジェクト全体で日本語コメント統一
- **文字化けチェック**: 日本語文字の表示確認必須
- **バイナリ確認**: 文字化け疑いがある場合は `hexdump -C` で確認

### パフォーマンス最適化

- requestAnimationFrame でアニメーション最適化
- IntersectionObserver で視認性監視
- スクロールイベントの頻度制限（30FPS）
- YouTube遅延読み込みでページ速度向上
- DOM要素キャッシュでリピート検索を最小化

### レスポンシブ対応

#### ヒーローセクション高さ修正（重要）
- **企業ページ**: `.hero-section` は `min-height: calc(100vh - 80px)` + `height: auto`
- **お遍路ページ**: `.shikoku-hero` は `min-height: calc(100vh - 80px)` + `height: auto`
- **固定高さ禁止**: 小画面で内容が切れるため、vhやpx固定値は使用しない
- **ヘッダー分調整**: デスクトップ80px、モバイル70px差し引く

#### テストサイズ
レスポンシブテストは `docs/responsive-testing.md` を参照。重要サイズ：
- 360px (Galaxy S8+) - 最終防衛ライン
- 375px (iPhone SE) - CSS設計基準点
- 390px (iPhone 12 Pro) - 最重要サイズ

### デザインテーマ

- **カラーパレット**: 金色（#b8860b, #d4af37）+ 黒背景
- **フォント**: Noto Serif JP（縦書き対応）
- **レスポンシブ**: 3段階（1024px, 768px, 480px）
- **統一感**: 全事業で共通のブランドイメージ維持

## 開発ドキュメント

- **レスポンシブテスト**: `docs/responsive-testing.md` - デバイスサイズ別確認チェックリスト
- **開発ガイド**: `docs/README.md` - ドキュメント構造の説明