# 東海道英語版 Phase 2 実装計画

## 概要
日本語テキストを英語に翻訳（55箇所の宿場データ）

## 翻訳対象

### 1. h3タグ：宿場名の英語化
- 現在：`<h3>品川</h3>`
- 変更後：`<h3>Shinagawa Post Town</h3>`
- 対象：55箇所

### 2. 読み仮名の削除または英語化
- 現在：`<div class="station-reading">しながわ</div>`
- オプションA：削除（英語版では不要）
- オプションB：ローマ字表記に変更（Shinagawa）
- 推奨：**削除**（英語版では読み仮名は不要）

### 3. 説明文の英語翻訳
- 現在：`東海道第一の宿場町。江戸時代には遊郭や茶屋が立ち並び、多くの旅人で賑わいました。`
- 変更後：`The first post town on the Tokaido. During the Edo period, it bustled with pleasure quarters and tea houses, attracting many travelers.`
- 対象：55箇所の長文

### 4. 詳細情報ラベル
- 住所：日本語のまま保持（Japanese Address）
- 駅情報：日本語のまま保持（Nearest Station）
- 見学時間：
  - 現在：`見学時間：1–1.5時間`
  - 変更後：`Visit Time: 1–1.5 hours`

### 5. ハイライト（station-highlights）
- 現在：`<span>商業中心</span>`
- 変更後：`<span>Commercial Hub</span>`
- 対象：各宿場3つ前後 × 55箇所 ≈ 165個のキーワード

## 実装アプローチ

### ステップ1: データベース作成
1. 宿場名マッピング（日本語 → ローマ字）
2. 説明文翻訳データベース（55箇所）
3. ハイライトキーワード翻訳辞書

### ステップ2: 適用スクリプト作成
- `tokaido_en_phase2_apply.py`
- JSONデータを読み込み、英語版HTMLに適用

### ステップ3: 検証スクリプト作成
- `tokaido_en_phase2_verify.py`
- 日本語テキストの残存チェック
- 翻訳の完全性確認

## 翻訳品質基準

1. **正確性**: 歴史的事実と地理情報を正確に
2. **簡潔性**: 説明文は2-3文で簡潔に
3. **一貫性**: 用語の統一（post town, Edo period, etc.）
4. **読みやすさ**: 外国人観光客が理解しやすい英語

## 次のステップ

1. 宿場名ローマ字マッピング作成
2. 説明文の翻訳（55箇所）
3. ハイライトキーワード翻訳辞書作成
4. 適用・検証スクリプト実装
