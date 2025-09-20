# レスポンシブデザイン実装ガイドライン

## 📱 問題と解決策

### 現在の問題

- **特定端末依存**: iPhone 12 Pro Max (428px) と MacBook 13inch (1280px) のみで確認
- **ブレークポイント不統一**: ページごとに異なる設定
- **他端末での崩れ**: 未確認デバイスでの表示問題

## 🎯 解決アプローチ

### 1. 統一ブレークポイントシステム

```css
/* モバイルファーストアプローチ */
:root {
  --bp-xs: 375px; /* iPhone SE, 小型スマホ */
  --bp-sm: 480px; /* 大型スマホ */
  --bp-md: 768px; /* タブレット */
  --bp-lg: 1024px; /* 小型ラップトップ */
  --bp-xl: 1280px; /* デスクトップ */
  --bp-2xl: 1440px; /* 大型デスクトップ */
}
```

### 2. 実装済みファイル

#### 📄 css/base/responsive-system.css

- 統一ブレークポイント定義
- レスポンシブユーティリティクラス
- デバッグ用クラス（現在のブレークポイント表示）

#### 📄 responsive-test.html

- 全デバイスでの表示確認用テストページ
- リアルタイム画面幅表示
- 主要 14 デバイスの対応状況確認

## 🔧 実装手順

### ステップ 1: テストページで確認

```bash
# ライブサーバーで開く
open responsive-test.html
```

### ステップ 2: 既存 CSS の統合

```css
/* 各ページのCSSに追加 */
@import url("base/responsive-system.css");
```

### ステップ 3: メディアクエリの置き換え

#### ❌ 修正前（バラバラな設定）

```css
@media (max-width: 428px) {
  /* iPhone 12 Pro Max専用 */
}
@media (max-width: 1280px) {
  /* MacBook 13inch専用 */
}
```

#### ✅ 修正後（統一システム）

```css
/* モバイル（すべての小型デバイス） */
@media (max-width: 480px) {
}

/* タブレット */
@media (min-width: 481px) and (max-width: 768px) {
}

/* デスクトップ */
@media (min-width: 769px) {
}
```

## 📊 対応デバイスリスト

### スマートフォン（375-428px）

- iPhone SE (375px)
- iPhone 12 Pro (390px)
- iPhone 12 Pro Max (428px) ✅ 確認済み
- iPhone 14 Pro (393px)
- Galaxy S21 (360px)
- Pixel 7 (412px)

### タブレット（768-1024px）

- iPad Mini (768px)
- iPad Air (820px)
- iPad Pro 11" (834px)
- iPad Pro 12.9" (1024px)

### ラップトップ/デスクトップ（1280px+）

- MacBook Air (1280px)
- MacBook Pro 13" (1280px) ✅ 確認済み
- MacBook Pro 14" (1512px)
- Desktop HD (1920px)

## 🚨 重要な修正ポイント

### 1. フレキシブルな単位使用

```css
/* ピクセル固定を避ける */
.container {
  /* ❌ 固定幅 */
  width: 428px;

  /* ✅ フレキシブル */
  width: 100%;
  max-width: 428px;
}
```

### 2. Clamp による可変サイズ

```css
/* フォントサイズの自動調整 */
.heading {
  font-size: clamp(1.5rem, 4vw + 0.5rem, 3rem);
  /* 最小1.5rem、最大3rem、その間は画面幅に応じて可変 */
}
```

### 3. グリッドの段階的変更

```css
.grid {
  /* モバイル: 1カラム */
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid {
    /* タブレット: 2カラム */
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    /* デスクトップ: 3カラム */
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## 🧪 テスト方法

### 1. ブラウザ開発者ツール

```
1. F12キーで開発者ツールを開く
2. デバイスツールバー切り替え（Ctrl+Shift+M）
3. 各デバイスプリセットで確認
```

### 2. 実機テスト推奨デバイス

- **必須**: iPhone SE (最小) / iPhone 14 Pro / iPad / Desktop
- **推奨**: Android (Galaxy/Pixel) / iPad Pro

### 3. デバッグクラスの活用

```html
<!-- HTMLに追加すると画面サイズが表示される -->
<body class="debug-responsive"></body>
```

## 📝 チェックリスト

### 実装前

- [ ] responsive-system.css を読み込み
- [ ] viewport meta タグ確認
- [ ] 既存の固定幅を確認

### 実装中

- [ ] モバイルファーストで記述
- [ ] 統一ブレークポイント使用
- [ ] タッチ要素は最小 44px 確保
- [ ] フレキシブル単位使用

### 実装後

- [ ] responsive-test.html で全デバイス確認
- [ ] 実機での動作確認（最低 3 デバイス）
- [ ] 横向き表示の確認

## 🎯 即効性のある修正

### 優先度 1: コンテナ幅の修正

```css
/* すべてのメインコンテナに適用 */
.container,
.main-content,
section {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  .container,
  .main-content,
  section {
    padding: 0 1.5rem;
  }
}
```

### 優先度 2: 画像の最適化

```css
img {
  max-width: 100%;
  height: auto;
}
```

### 優先度 3: フォントサイズの調整

```css
html {
  font-size: 14px;
}

@media (min-width: 768px) {
  html {
    font-size: 15px;
  }
}

@media (min-width: 1024px) {
  html {
    font-size: 16px;
  }
}
```

## 💡 トラブルシューティング

### Q: 特定の端末でだけ崩れる

A: デバイス固有の幅ではなく、範囲で対応

```css
/* ❌ 特定デバイス */
@media (width: 428px) {
}

/* ✅ 範囲指定 */
@media (max-width: 480px) {
}
```

### Q: 横向きで崩れる

A: orientation メディアクエリ追加

```css
@media (max-width: 768px) and (orientation: landscape) {
  /* 横向き専用スタイル */
}
```

### Q: タッチ操作が効かない

A: タッチターゲットサイズ確認

```css
.button,
.link,
[role="button"] {
  min-height: 44px;
  min-width: 44px;
}
```
