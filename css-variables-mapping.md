# 📊 CSS変数重複分析・統合マッピング表

## 🚨 重複状況サマリー

**重複ファイル数**: 5ファイル  
**共通変数数**: 5個（基本カラーパレット）  
**統合必要度**: 🔴 Critical

---

## 📋 変数重複マッピング

### 🎨 カラーパレット（全ファイル共通）

| 変数名 | style.css | ohenro.css | tokaido.css | faq.css | guide-simple.css | 統一値 | 
|--------|-----------|------------|-------------|---------|------------------|--------|
| `--primary-gold` | #b8860b | #b8860b | #b8860b | #b8860b | #b8860b | ✅ **#b8860b** |
| `--secondary-gold` | #8b6914 | #8b6914 | #8b6914 | #8b6914 | #8b6914 | ✅ **#8b6914** |
| `--accent-gold` | #d4af37 | #d4af37 | #d4af37 | #d4af37 | #d4af37 | ✅ **#d4af37** |
| `--text-white` | #2c2c2c | #2c2c2c | #2c2c2c | #2c2c2c | #2c2c2c | ✅ **#2c2c2c** |
| `--text-gray` | #555 | #555 | #555 | #555 | #555 | ✅ **#555** |

### 📐 style.css固有変数（28個）

| カテゴリ | 変数数 | 主要変数例 |
|----------|--------|------------|
| カラー拡張 | 8個 | `--text-dark`, `--bg-light`, `--bg-overlay` |
| スペーシング | 6個 | `--spacing-xs` ~ `--spacing-xl`, `--margin-auto` |
| フォント | 8個 | `--font-primary`, `--font-h1` ~ `--font-h4` |
| その他 | 6個 | `--border-gold`, `--shadow-text`, etc. |

### 🎯 ohenro.css固有変数（3個）

| 変数名 | 値 | 用途 |
|--------|-----|------|
| `--border-gold` | `2px solid rgba(212, 175, 55, 0.3)` | お遍路専用境界線 |
| `--margin-auto` | `0 auto` | **重複**: style.cssと同一 |
| `--shadow-text` | `1px 1px 3px rgba(0, 0, 0, 0.2)` | **重複**: style.cssと同一 |
| `--bg-dark` | `linear-gradient(...)` | **値違い**: style.cssと異なる |

### 🚶 tokaido.css, faq.css, guide-simple.css

**固有変数**: なし（基本カラーのみ重複定義）

---

## 🎯 統合計画

### Phase 1: 基本変数統合
```css
:root {
  /* 🎨 カラーパレット（全ファイル共通） */
  --primary-gold: #b8860b;
  --secondary-gold: #8b6914; 
  --accent-gold: #d4af37;
  --text-white: #2c2c2c;
  --text-gray: #555;
  
  /* 📐 カラー拡張（style.css由来） */
  --text-dark: #1a1a1a;
  --bg-light: #faf8f3;
  --bg-light-secondary: #f8f6f0;
  --bg-dark: #f5f3ef; /* style.css版を採用 */
  --bg-overlay: rgba(245, 243, 239, 0.95);
}
```

### Phase 2: スペーシング・フォント統合
```css
:root {
  /* 📏 スペーシング（style.css由来） */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 2rem;
  --spacing-lg: 4rem;
  --spacing-xl: 6rem;
  --margin-auto: 0 auto;
  
  /* 🔤 フォント（style.css由来） */
  --font-primary: "Noto Serif JP", "Yu Mincho", "YuMincho", "Hiragino Mincho Pro", "Times New Roman", serif;
  --font-secondary: "Shippori Mincho", serif;
  --font-h1: 2.5rem;
  --font-h2: 2rem;
  --font-h3: 1.5rem;
  --font-h4: 1.25rem;
  --font-body: 1rem;
  --font-small: 0.9rem;
  --font-xs: 0.8rem;
}
```

### Phase 3: ユーティリティ統合
```css
:root {
  /* 🎨 境界線・影 */
  --border-gold: 1px solid rgba(184, 134, 11, 0.3); /* style.css版を採用 */
  --border-radius: 8px;
  --shadow-text: 1px 1px 3px rgba(0, 0, 0, 0.2);
  --shadow-card: 0 4px 15px rgba(0, 0, 0, 0.1);
}
```

---

## ⚠️ 重複解決ルール

### 🟢 値が同一の場合
→ **そのまま統合**（5個の基本カラーパレット）

### 🟡 値が異なる場合  
→ **style.css版を採用**（理由: 最も包括的で基本となるファイル）

### 🔴 固有機能の場合
→ **ページ固有CSSに移動**（例: お遍路専用の境界線スタイル）

---

## 📊 統合効果予測

### Before（現在）
- **重複変数**: 5ファイル × 5変数 = 25個の重複定義
- **管理コスト**: 色変更時に5ファイル同期が必要

### After（統合後）
- **統一変数**: 1ファイル × 40+変数 = 完全な統一管理
- **管理効率**: 1箇所変更で全サイト反映

### 削減率
- **重複削除**: 25個 → 0個（100%削除）
- **保守コスト**: 5倍 → 1倍（80%削減）

---

## ✅ 次のアクション

1. **css/base/variables.css作成**: 統合変数定義
2. **各ファイルから:root削除**: 重複解消  
3. **import文追加**: 新変数ファイル読み込み
4. **動作確認**: 既存機能の保持確認

**🎯 Task 1.1完了準備OK！**