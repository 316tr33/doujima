# 📋 フェーズ別詳細タスクリスト

**参照**: [MASTER_IMPLEMENTATION_PLAN.md](./MASTER_IMPLEMENTATION_PLAN.md)

---

## 🚀 Phase 1: CSS 構造統一化（Day 1-3）

### Day 1: CSS 変数統一と新構造設計

#### 🎯 Task 1.1: CSS 変数の完全棚卸し

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### 実行手順:

1. **既存変数の抽出**

   ```bash
   # 全CSS変数を抽出
   grep -r ":root" css/ > css-variables-audit.txt
   grep -r "--" css/ >> css-variables-audit.txt
   ```

2. **変数マッピング表作成**

   - [ ] `style.css`の変数一覧
   - [ ] `ohenro.css`の変数一覧
   - [ ] `tokaido.css`の変数一覧
   - [ ] `faq.css`の変数一覧
   - [ ] `guide-simple.css`の変数一覧

3. **重複確認と統合計画**
   - [ ] 同一変数名の値違いチェック
   - [ ] 統一する変数値の決定
   - [ ] 新しい変数命名規則策定

**成果物**: `css-variables-mapping.xlsx`

#### 🎯 Task 1.2: 新 CSS 構造の物理作成

**時間**: 1-2 時間  
**優先度**: 🔴 Critical

##### 実行手順:

```bash
# 新ディレクトリ構造作成
mkdir -p css/base
mkdir -p css/components
mkdir -p css/pages
mkdir -p css/responsive

# 基本ファイル作成
touch css/base/variables.css
touch css/base/reset.css
touch css/base/typography.css
touch css/base/utilities.css
```

**チェックリスト**:

- [ ] `css/base/`ディレクトリ作成
- [ ] `css/components/`ディレクトリ作成
- [ ] `css/pages/`ディレクトリ作成
- [ ] `css/responsive/`ディレクトリ作成
- [ ] 各基本ファイル作成

#### 🎯 Task 1.3: 統一 variables.css 作成

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### 実行手順:

1. **基本 CSS 変数定義**
   ```css
   /* css/base/variables.css */
   :root {
     /* カラーパレット */
     --primary-gold: #b8860b;
     --secondary-gold: #8b6914;
     --accent-gold: #d4af37;

     /* レスポンシブブレークポイント */
     --bp-mobile: 480px;
     --bp-tablet: 768px;
     --bp-desktop: 1024px;

     /* スペーシング */
     --spacing-xs: 0.5rem;
     --spacing-sm: 1rem;
     --spacing-md: 2rem;
     --spacing-lg: 4rem;
   }
   ```

**検証基準**: 全既存変数が新ファイルに含まれている

---

### Day 2: 既存 CSS ファイル分割実装

#### 🎯 Task 2.1: style.css の分割

**時間**: 3-4 時間  
**優先度**: 🔴 Critical

##### 分割対象:

- [ ] **reset 部分** → `css/base/reset.css`
- [ ] **typography 部分** → `css/base/typography.css`
- [ ] **navigation 部分** → `css/components/navigation.css`
- [ ] **home 固有部分** → `css/pages/home.css`
- [ ] **utilities 部分** → `css/base/utilities.css`

##### 実行手順:

1. 各セクションの特定とコピー
2. 新ファイルへの移動
3. 重複コードの除去
4. import 文の追加

**検証**: 元ファイルから該当部分が削除されている

#### 🎯 Task 2.2: ohenro.css の分割

**時間**: 4-5 時間  
**優先度**: 🔴 Critical

##### 分割対象:

- [ ] **お遍路固有スタイル** → `css/pages/ohenro.css`
- [ ] **カードコンポーネント** → `css/components/cards.css`
- [ ] **slideshow 部分** → `css/components/slideshow.css`
- [ ] **レスポンシブ部分** → 適切な`responsive/`ファイル

**検証**: ohenro.css が 1000 行以下になる

#### 🎯 Task 2.3: tokaido.css の分割

**時間**: 4-5 時間  
**優先度**: 🔴 Critical

##### 分割対象（3,706 行を分割）:

- [ ] **東海道固有スタイル** → `css/pages/tokaido.css`
- [ ] **共通コンポーネント** → 適切な`components/`ファイル
- [ ] **フォーム系** → `css/components/forms.css`
- [ ] **ボタン系** → `css/components/buttons.css`

**検証**: tokaido.css が 1500 行以下になる

---

### Day 3: 重複コード除去と統合

#### 🎯 Task 3.1: 重複セレクターの統合

**時間**: 3-4 時間  
**優先度**: 🟡 Important

##### 実行手順:

1. **重複セレクター検出**

   ```bash
   # 重複セレクター検出スクリプト実行
   grep -r "\.prefecture-grid" css/
   grep -r "\.navigation" css/
   ```

2. **統合優先順位**
   - [ ] 高頻度使用セレクター
   - [ ] レイアウト系セレクター
   - [ ] アニメーション系セレクター

**目標**: 重複セレクター 80%削減

#### 🎯 Task 3.2: 未使用 CSS 除去

**時間**: 2-3 時間  
**優先度**: 🟡 Important

##### 実行手順:

1. HTML ファイルで使用されているクラス抽出
2. 未使用クラスの特定
3. 安全な削除の実行

**目標**: CSS 総サイズ 30%削減

#### 🎯 Task 3.3: HTML ファイルの CSS 読み込み更新

**時間**: 1-2 時間  
**優先度**: 🔴 Critical

##### 対象ファイル:

- [ ] `index.html`
- [ ] `Ohenro/index.html`
- [ ] `Ohenro/shikoku.html`
- [ ] `Tokaido/index.html`
- [ ] `recruit.html`

##### 新しい読み込み順序:

```html
<!-- Base CSS -->
<link rel="stylesheet" href="css/base/variables.css" />
<link rel="stylesheet" href="css/base/reset.css" />
<link rel="stylesheet" href="css/base/typography.css" />

<!-- Components CSS -->
<link rel="stylesheet" href="css/components/navigation.css" />
<link rel="stylesheet" href="css/components/slideshow.css" />

<!-- Page-specific CSS -->
<link rel="stylesheet" href="css/pages/home.css" />

<!-- Responsive CSS -->
<link rel="stylesheet" href="css/responsive/mobile.css" />
```

---

## 🚀 Phase 2: モバイル対応完全実装（Day 4-6）

### Day 4: 統一ブレークポイント設定

#### 🎯 Task 4.1: ブレークポイント変数統一

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### variables.css への追加:

```css
:root {
  /* Responsive Breakpoints */
  --bp-mobile-max: 480px;
  --bp-tablet-min: 481px;
  --bp-tablet-max: 768px;
  --bp-desktop-min: 769px;
  --bp-desktop-large: 1200px;

  /* Responsive Utilities */
  --container-mobile: 100%;
  --container-tablet: 90%;
  --container-desktop: 1200px;
}
```

#### 🎯 Task 4.2: 既存メディアクエリの統一化

**時間**: 3-4 時間  
**優先度**: 🔴 Critical

##### 実行手順:

1. **既存メディアクエリの検出**

   ```bash
   grep -r "@media" css/ > existing-media-queries.txt
   ```

2. **統一化作業**
   - [ ] 不統一なブレークポイント修正
   - [ ] 重複メディアクエリの統合
   - [ ] CSS 変数使用への変更

**検証**: 全メディアクエリが統一ブレークポイント使用

---

### Day 5: モバイルファースト実装

#### 🎯 Task 5.1: ベーススタイルのモバイル化

**時間**: 4-5 時間  
**優先度**: 🔴 Critical

##### 対象要素:

- [ ] **フォントサイズ**: fluid typography 導入
- [ ] **スペーシング**: モバイル向け調整
- [ ] **レイアウト**: flexbox/grid 最適化
- [ ] **画像**: responsive images 設定

##### 実装例:

```css
/* Base mobile-first styles */
.container {
  width: var(--container-mobile);
  padding: var(--spacing-sm);
}

/* Desktop enhancement */
@media (min-width: var(--bp-desktop-min)) {
  .container {
    width: var(--container-desktop);
    padding: var(--spacing-lg);
  }
}
```

#### 🎯 Task 5.2: タッチインターフェース最適化

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### 対象要素:

- [ ] **ボタンサイズ**: 最小 44px×44px
- [ ] **タップターゲット**: 適切な間隔確保
- [ ] **スワイプ**: スライドショー対応
- [ ] **ズーム**: 適切な viewport 設定

---

### Day 6: コンポーネント別最適化

#### 🎯 Task 6.1: ナビゲーション最適化

**時間**: 3-4 時間  
**優先度**: 🔴 Critical

##### 実装項目:

- [ ] **ハンバーガーメニュー**: アニメーション改善
- [ ] **メニューオーバーレイ**: スムーズな表示
- [ ] **縦書きナビ**: モバイルでの最適化
- [ ] **タッチ操作**: 操作性向上

#### 🎯 Task 6.2: スライドショー最適化

**時間**: 2-3 時間  
**優先度**: 🟡 Important

##### 実装項目:

- [ ] **スワイプ操作**: タッチ対応
- [ ] **プログレスバー**: モバイル表示調整
- [ ] **画像サイズ**: レスポンシブ対応
- [ ] **パフォーマンス**: 遅延読み込み

#### 🎯 Task 6.3: 県別グリッド最適化

**時間**: 2-3 時間  
**優先度**: 🟡 Important

##### 実装項目:

- [ ] **1 列レイアウト**: モバイル向け
- [ ] **カード間隔**: タッチ操作考慮
- [ ] **画像表示**: アスペクト比維持
- [ ] **テキスト**: 読みやすさ向上

---

## 🚀 Phase 3: 品質保証と最適化（Day 7）

### Day 7: 最終品質検証

#### 🎯 Task 7.1: 全ページ機能テスト

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### テスト項目:

- [ ] **index.html**: 全機能動作確認
- [ ] **Ohenro/index.html**: お遍路機能確認
- [ ] **Ohenro/shikoku.html**: 検索・フィルター確認
- [ ] **Tokaido/index.html**: 東海道機能確認
- [ ] **recruit.html**: 採用ページ確認

#### 🎯 Task 7.2: レスポンシブテスト

**時間**: 2-3 時間  
**優先度**: 🔴 Critical

##### テスト解像度:

- [ ] **320px**: iPhone SE
- [ ] **375px**: iPhone 12 mini
- [ ] **428px**: iPhone 12 Pro Max
- [ ] **768px**: iPad
- [ ] **1024px**: iPad Pro
- [ ] **1440px**: デスクトップ
- [ ] **1920px**: 大型デスクトップ

#### 🎯 Task 7.3: パフォーマンステスト

**時間**: 1-2 時間  
**優先度**: 🟡 Important

##### テスト項目:

- [ ] **PageSpeed Insights**: Mobile 90 点目標
- [ ] **GTmetrix**: Grade A 目標
- [ ] **CSS サイズ**: 50%削減確認
- [ ] **読み込み時間**: 3 秒以下確認

#### 🎯 Task 7.4: 最終ドキュメント整備

**時間**: 1-2 時間  
**優先度**: 🟢 Nice-to-Have

##### 成果物:

- [ ] **CSS 構造ガイド**: 新構造の説明
- [ ] **CLAUDE.md 更新**: 開発コマンド更新
- [ ] **保守ガイド**: 今後の開発ルール
- [ ] **実装レポート**: 改善結果サマリー

---

## ⏱️ 時間管理

### 各タスクの時間配分

| Phase    | 予定時間       | バッファ   | 合計        |
| -------- | -------------- | ---------- | ----------- |
| Phase 1  | 18-24 時間     | 4 時間     | 28 時間     |
| Phase 2  | 14-18 時間     | 3 時間     | 21 時間     |
| Phase 3  | 6-10 時間      | 2 時間     | 12 時間     |
| **総計** | **38-52 時間** | **9 時間** | **61 時間** |

### 1 日あたりの作業時間

- **平日**: 6-8 時間
- **休日**: 8-10 時間
- **推奨ペース**: 7 日間で完了

---

## 🔄 チェックポイント

### 各フェーズ完了時の確認

1. **機能確認**: 既存機能が正常動作
2. **表示確認**: レスポンシブ表示正常
3. **コミット**: git commit でバックアップ
4. **ドキュメント更新**: 進捗記録

### 問題発生時の対応

1. **即座停止**: 問題のあるタスクを停止
2. **原因特定**: 問題の根本原因調査
3. **ロールバック**: 必要に応じて前状態に復旧
4. **計画修正**: スケジュールとタスクの再検討

---

**🎯 各タスクを確実に完了させ、最終的に完璧なモバイル対応サイトを実現しましょう！**
