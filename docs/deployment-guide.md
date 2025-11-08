# フォーム機能デプロイ手順書

**対象読者:** 開発者、クライアントの IT 担当者
**最終更新:** 2025-11-06

---

## 目次

1. [前提条件](#前提条件)
2. [Cloudflare Pages プロジェクト作成](#cloudflare-pages-プロジェクト作成)
3. [環境変数設定](#環境変数設定)
4. [Workers KV Namespace 作成](#workers-kv-namespace作成)
5. [Cloudflare Turnstile 設定](#cloudflare-turnstile設定)
6. [デプロイ実行](#デプロイ実行)
7. [トラブルシューティング](#トラブルシューティング)

---

## 前提条件

### 必須アカウント

- **Cloudflare アカウント**（無料プラン可）

  - サインアップ: https://dash.cloudflare.com/sign-up

- **GitHub アカウント**
  - リポジトリ: doujima（プライベート推奨）

### オプション

- **wrangler CLI**（ローカル開発・手動デプロイ用）
  ```bash
  npm install -g wrangler
  wrangler login
  ```

### 必要情報の準備

- [ ] 受信先メールアドレス（例: info@doujimafront.com）
- [ ] 送信元メールアドレス（例: noreply@doujimafront.com）
- [ ] GitHub リポジトリのアクセス権限

---

## Cloudflare Pages プロジェクト作成

### ステップ 1: Cloudflare ダッシュボードにアクセス

1. https://dash.cloudflare.com/ にログイン
2. 左サイドバーから **Workers & Pages** を選択
3. **Create application** ボタンをクリック
4. **Pages** タブを選択
5. **Connect to Git** を選択

### ステップ 2: GitHub リポジトリ連携

1. **GitHub** を選択
2. GitHub 認証を許可
3. **doujima** リポジトリを選択
4. **Begin setup** をクリック

### ステップ 3: プロジェクト設定

| 項目                       | 設定値                       |
| -------------------------- | ---------------------------- |
| **Project name**           | `doujima`（または任意）      |
| **Production branch**      | `main` または `master`       |
| **Build command**          | 空欄（静的サイトのため不要） |
| **Build output directory** | `/`（ルートディレクトリ）    |

**重要:** ビルドコマンドは不要です。静的 HTML ファイルをそのまま配信します。

4. **Save and Deploy** をクリック

### ステップ 4: 初回デプロイ確認

- デプロイ完了まで 1〜2 分待機
- デプロイ完了後、`https://doujima.pages.dev` のような URL が発行される
- **View project** をクリックして動作確認

---

## 環境変数設定

### ステップ 1: 環境変数設定画面を開く

1. Cloudflare ダッシュボード → **Workers & Pages**
2. **doujima** プロジェクトを選択
3. **Settings** タブをクリック
4. **Environment variables** セクションを開く

### ステップ 2: 本番環境（Production）の環境変数を追加

**Add variable** ボタンを 3 回クリックして、以下を追加:

#### 1. RECIPIENT_EMAIL（必須）

- **Variable name:** `RECIPIENT_EMAIL`
- **Value:** `info@doujimafront.com`（受信先メールアドレス）
- **Environment:** Production
- **Type:** Plain text

#### 2. FROM_EMAIL（必須）

- **Variable name:** `FROM_EMAIL`
- **Value:** `noreply@doujimafront.com`（送信元メールアドレス）
- **Environment:** Production
- **Type:** Plain text

#### 3. TURNSTILE_SECRET_KEY（必須）

- **Variable name:** `TURNSTILE_SECRET_KEY`
- **Value:** `0x4AAxxxxxxxxxxxxxxxxxxxxxxxxxx`（後述の手順で取得）
- **Environment:** Production
- **Type:** **Secret**（セキュリティ向上のため）

### ステップ 3: プレビュー環境（Preview）の環境変数を追加（推奨）

開発・テスト用に別のメールアドレスを設定することを推奨します。

**同じ手順で以下を追加:**

| Variable name        | Value                             | Environment | Type       |
| -------------------- | --------------------------------- | ----------- | ---------- |
| RECIPIENT_EMAIL      | `test@example.com`                | Preview     | Plain text |
| FROM_EMAIL           | `noreply-dev@doujimafront.com`    | Preview     | Plain text |
| TURNSTILE_SECRET_KEY | `0x4AAxxxxxxxxxxxxxxxxxxxxxxxxxx` | Preview     | Secret     |

### ステップ 4: 保存と再デプロイ

1. **Save** ボタンをクリック
2. 環境変数は次回デプロイから反映されます
3. すぐに反映したい場合: **Deployments** → **Redeploy**

---

## Workers KV Namespace 作成

レート制限機能（5 分間に 3 回まで送信）には Workers KV が必要です。

### ステップ 1: KV Namespace を作成

1. Cloudflare ダッシュボード → **Workers & Pages**
2. 左サイドバー → **KV**
3. **Create a namespace** ボタンをクリック
4. **Namespace Name:** `RATE_LIMIT`（正確に入力）
5. **Add** をクリック

### ステップ 2: Namespace ID をコピー

- 作成後、`Namespace ID` が表示されます（例: `a1b2c3d4e5f6...`）
- この ID をメモ帳にコピーしてください

### ステップ 3: プロジェクトに Binding を追加

1. **Workers & Pages** → **doujima** プロジェクト
2. **Settings** → **Functions**
3. **KV namespace bindings** セクション
4. **Add binding** をクリック

| 項目              | 設定値                                 |
| ----------------- | -------------------------------------- |
| **Variable name** | `RATE_LIMIT`                           |
| **KV namespace**  | `RATE_LIMIT`（ドロップダウンから選択） |
| **Environment**   | Production                             |

5. **Save** をクリック

### ステップ 4: プレビュー環境用 Binding を追加（推奨）

**同じ手順で Preview 環境にも追加:**

| 項目              | 設定値                                  |
| ----------------- | --------------------------------------- |
| **Variable name** | `RATE_LIMIT`                            |
| **KV namespace**  | `RATE_LIMIT`（同じ Namespace を使用可） |
| **Environment**   | Preview                                 |

### ステップ 5: wrangler.toml への ID 記入（オプション）

ローカル開発を行う場合、`wrangler.toml` ファイルに KV Namespace ID を記入:

```toml
[[kv_namespaces]]
binding = "RATE_LIMIT"
id = "a1b2c3d4e5f6..."  # ステップ2でコピーしたID
preview_id = "a1b2c3d4e5f6..."  # 同じIDでOK
```

---

## Cloudflare Turnstile 設定

スパムボット対策のため、Cloudflare Turnstile を設定します。

### ステップ 1: Turnstile サイトを追加

1. Cloudflare ダッシュボード → **Turnstile**
2. **Add site** ボタンをクリック

### ステップ 2: サイト情報を入力

| 項目              | 設定値                                                                            |
| ----------------- | --------------------------------------------------------------------------------- |
| **Site name**     | `堂島フロント企画フォーム`                                                        |
| **Domain**        | `doujimafront.com`（本番ドメイン）<br>`doujima.pages.dev`（Cloudflare Pages URL） |
| **Widget Mode**   | `Managed`（推奨）                                                                 |
| **Pre-Clearance** | `Disabled`                                                                        |

**重要:** Domain には本番ドメインと Cloudflare Pages URL の両方を追加してください（カンマ区切り）。

3. **Create** をクリック

### ステップ 3: サイトキーとシークレットキーを取得

作成後、以下の 2 つのキーが表示されます:

- **Site Key（公開鍵）:** `0x4AAAAAAAxxxxxxxxxxxxxxxxxx`
  → HTML に埋め込む（クライアント側）

- **Secret Key（秘密鍵）:** `0x4AAxxxxxxxxxxxxxxxxxxxxxxxxxx`
  → 環境変数 `TURNSTILE_SECRET_KEY` に設定（サーバー側）

**この画面を閉じずに、次のステップに進んでください。**

### ステップ 4: HTML にサイトキーを埋め込む

`index.html` と `recruit.html` の両方に、以下のコードを追加します。

#### 4-1. Turnstile スクリプトを追加（`<head>`タグ内）

```html
<!-- Cloudflare Turnstile -->
<script
  src="https://challenges.cloudflare.com/turnstile/v0/api.js"
  async
  defer
></script>
```

#### 4-2. Turnstile ウィジェットを追加（フォーム内、送信ボタンの直前）

```html
<!-- Turnstile検証 -->
<div
  class="cf-turnstile"
  data-sitekey="0x4AAAAAAAxxxxxxxxxxxxxxxxxx"
  data-callback="onTurnstileSuccess"
  data-error-callback="onTurnstileError"
></div>
```

**`data-sitekey` の値をステップ 3 でコピーした Site Key に置き換えてください。**

#### 4-3. JavaScript コールバック関数を追加（既存の JS ファイル）

```javascript
// Turnstile検証成功時
window.onTurnstileSuccess = function (token) {
  console.log("Turnstile検証成功");
  // 送信ボタンを有効化
  const submitBtn = document.getElementById("submit-btn");
  if (submitBtn) {
    submitBtn.disabled = false;
  }
};

// Turnstile検証エラー時
window.onTurnstileError = function (error) {
  console.error("Turnstile検証失敗:", error);
  alert("セキュリティ検証に失敗しました。ページを再読み込みしてください。");
};
```

### ステップ 5: 環境変数に秘密鍵を設定

1. Cloudflare ダッシュボード → **Workers & Pages** → **doujima**
2. **Settings** → **Environment variables**
3. `TURNSTILE_SECRET_KEY` の値を、ステップ 3 でコピーした Secret Key に更新
4. **Save** をクリック

### ステップ 6: GitHub にプッシュ

```bash
git add index.html recruit.html js/
git commit -m "feat: Cloudflare Turnstileを統合"
git push origin main
```

Cloudflare Pages が自動的に再デプロイします。

---

## デプロイ実行

### 方法 1: 自動デプロイ（推奨）

GitHub へのプッシュで自動的にデプロイされます。

```bash
# コードを修正後
git add .
git commit -m "feat: フォーム機能を追加"
git push origin main
```

**デプロイ進行状況の確認:**

1. Cloudflare ダッシュボード → **Workers & Pages** → **doujima**
2. **Deployments** タブ
3. 最新のデプロイをクリック → ログを確認

**デプロイ完了時間:** 通常 1〜3 分

### 方法 2: 手動デプロイ（wrangler CLI）

ローカルから直接デプロイする場合:

```bash
# プロジェクトルートディレクトリで実行
wrangler pages deploy . --project-name=doujima
```

**認証が必要な場合:**

```bash
wrangler login
```

### デプロイ確認手順

#### 1. Pages Functions が正しくデプロイされたか確認

**ターミナルで確認:**

```bash
curl -X POST https://doujima.pages.dev/submit-contact \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

**期待される応答:**

```json
{
  "success": false,
  "error": "セキュリティ検証が完了していません。"
}
```

これが返ってくれば、Functions は正常に動作しています。

#### 2. 環境変数が設定されているか確認

**Cloudflare ダッシュボード:**

1. **Workers & Pages** → **doujima** → **Settings**
2. **Environment variables** セクション
3. 以下の 3 つが設定されているか確認:
   - `RECIPIENT_EMAIL`
   - `FROM_EMAIL`
   - `TURNSTILE_SECRET_KEY`

#### 3. KV Namespace Binding が設定されているか確認

**Cloudflare ダッシュボード:**

1. **Workers & Pages** → **doujima** → **Settings**
2. **Functions** → **KV namespace bindings**
3. `RATE_LIMIT` binding が存在するか確認

---

## トラブルシューティング

### 問題 1: Pages Functions が動作しない（404 エラー）

**症状:**

- `/submit-contact` にアクセスすると 404 エラー
- フォーム送信ボタンを押してもエラーが表示されない

**原因:**

- `functions/` ディレクトリが正しくデプロイされていない
- ファイル名が間違っている（`submit-contact.js` でなければならない）
- Cloudflare Pages のビルド設定が間違っている

**対処法:**

1. **ファイル構造を確認:**

   ```
   doujima/
   ├── functions/
   │   ├── submit-contact.js  ← 必須
   │   └── submit-recruit.js   ← 必須
   ├── index.html
   └── recruit.html
   ```

2. **Cloudflare Pages の設定を確認:**

   - **Build command:** 空欄
   - **Build output directory:** `/`

3. **再デプロイを実行:**

   ```bash
   git push origin main
   ```

4. **デプロイログを確認:**

   Cloudflare ダッシュボード → **Deployments** → 最新のデプロイ → **View details**

### 問題 2: メール送信エラー（500 エラー）

**症状:**

- フォーム送信後、「メール送信に失敗しました」というエラーが表示される
- ブラウザのコンソールに 500 エラーが表示される

**原因:**

- 環境変数 `RECIPIENT_EMAIL` または `FROM_EMAIL` が設定されていない
- MailChannels API へのリクエストが失敗している
- FROM_EMAIL のドメインがデプロイドメインと一致していない

**対処法:**

1. **環境変数を確認:**

   Cloudflare ダッシュボード → **Settings** → **Environment variables**

   - `RECIPIENT_EMAIL`: `info@doujimafront.com`
   - `FROM_EMAIL`: `noreply@doujimafront.com`

2. **ログを確認:**

   Cloudflare ダッシュボード → **Logs** → Functions のリアルタイムログを表示

   エラーメッセージから原因を特定:

   ```
   [お問い合わせフォーム] メール送信失敗: MailChannels API エラー: 400 - ...
   ```

3. **FROM_EMAIL ドメインを確認:**

   MailChannels API は送信元ドメインの検証を行います。以下のいずれかに設定:

   - `noreply@doujimafront.com`（本番ドメイン）
   - `noreply@doujima.pages.dev`（Cloudflare Pages URL）

4. **SPF レコードを確認（推奨）:**

   DNS に以下の SPF レコードを追加:

   ```
   Type: TXT
   Name: @
   Content: v=spf1 include:_spf.mx.cloudflare.net ~all
   ```

### 問題 3: Turnstile 検証エラー（403 エラー）

**症状:**

- フォーム送信後、「セキュリティ検証に失敗しました」というエラーが表示される
- ブラウザのコンソールに 403 エラーが表示される

**原因:**

- `TURNSTILE_SECRET_KEY` が間違っている
- サイトキーとシークレットキーの不一致
- Turnstile サイトのドメイン設定ミス

**対処法:**

1. **環境変数を確認:**

   Cloudflare ダッシュボード → **Settings** → **Environment variables**

   - `TURNSTILE_SECRET_KEY` の値を再確認

2. **Turnstile サイト設定を確認:**

   Cloudflare ダッシュボード → **Turnstile** → サイトを選択

   - **Domain:** `doujimafront.com` と `doujima.pages.dev` の両方が追加されているか確認

3. **サイトキーとシークレットキーを再取得:**

   - Turnstile ダッシュボードから正しいキーをコピー
   - HTML の `data-sitekey` を更新
   - 環境変数 `TURNSTILE_SECRET_KEY` を更新

4. **ブラウザキャッシュをクリア:**

   - Chrome: `Ctrl+Shift+R`（Windows）/ `Cmd+Shift+R`（Mac）

### 問題 4: レート制限が機能しない（429 エラーが出ない）

**症状:**

- 5 分間に 3 回以上送信できてしまう
- レート制限が動作していない

**原因:**

- KV Namespace Binding が設定されていない
- Binding 名が `RATE_LIMIT` ではない
- KV Namespace へのアクセス権限がない

**対処法:**

1. **KV Namespace Binding を確認:**

   Cloudflare ダッシュボード → **Settings** → **Functions** → **KV namespace bindings**

   - Variable name: `RATE_LIMIT`（正確に）
   - KV namespace: `RATE_LIMIT`（作成済みの Namespace）

2. **KV Namespace が作成されているか確認:**

   Cloudflare ダッシュボード → **Workers & Pages** → **KV**

   - `RATE_LIMIT` Namespace が存在するか確認

3. **ログを確認:**

   ```
   [レート制限] KVエラー: ...
   ```

   というログが出ていれば、KV 接続に問題があります。

4. **Binding を再作成:**

   既存の Binding を削除 → 再度追加 → 再デプロイ

### 問題 5: CORS エラー（ブラウザコンソール）

**症状:**

- ブラウザのコンソールに以下のエラーが表示される:

  ```
  Access to fetch at 'https://doujima.pages.dev/submit-contact'
  from origin 'https://doujimafront.com' has been blocked by CORS policy
  ```

**原因:**

- フォームと API のオリジンが異なる
- CORS ヘッダーが正しく設定されていない

**対処法:**

1. **同一オリジンから送信されているか確認:**

   - HTML ファイルの URL: `https://doujima.pages.dev/index.html`
   - API の URL: `https://doujima.pages.dev/submit-contact`

   **異なるドメインから送信する場合（本番環境）:**

   `functions/submit-contact.js` の CORS ヘッダーを更新:

   ```javascript
   const corsHeaders = {
     "Access-Control-Allow-Origin": "https://doujimafront.com", // 本番ドメイン
     "Access-Control-Allow-Methods": "POST, OPTIONS",
     "Access-Control-Allow-Headers": "Content-Type",
     "Content-Type": "application/json; charset=utf-8",
   };
   ```

2. **プリフライトリクエストの確認:**

   ブラウザの Network タブで `OPTIONS` リクエストが 204 を返しているか確認

### 問題 6: デプロイが完了しない（タイムアウト）

**症状:**

- デプロイが 10 分以上経っても完了しない
- デプロイログに進行状況が表示されない

**原因:**

- Cloudflare Pages のサービス障害
- リポジトリサイズが大きすぎる
- ビルド設定が間違っている

**対処法:**

1. **Cloudflare ステータスページを確認:**

   https://www.cloudflarestatus.com/

2. **デプロイをキャンセル:**

   Cloudflare ダッシュボード → **Deployments** → **Cancel deployment**

3. **再デプロイを実行:**

   ```bash
   git commit --allow-empty -m "chore: trigger redeploy"
   git push origin main
   ```

4. **リポジトリサイズを削減:**

   - `.gitignore` に不要なファイルを追加
   - 大きな画像ファイルを圧縮

---

## 次のステップ

デプロイが完了したら、以下のドキュメントを参照してください:

- **DNS 設定:** `docs/dns-setup-guide.md`
- **テスト手順:** `docs/testing-guide.md`
- **クライアント会議:** `docs/client-meeting-guide.md`

---

## サポート情報

### 公式ドキュメント

- **Cloudflare Pages Functions:** https://developers.cloudflare.com/pages/functions/
- **MailChannels API:** https://mailchannels.zendesk.com/hc/en-us/articles/4565898358413
- **Cloudflare Turnstile:** https://developers.cloudflare.com/turnstile/
- **Workers KV:** https://developers.cloudflare.com/kv/

### 問題報告

プロジェクト固有の問題は開発チームに連絡してください。
