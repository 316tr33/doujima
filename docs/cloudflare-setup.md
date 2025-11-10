# Cloudflare セットアップガイド

堂島フロント企画のフォーム機能を動作させるために必要な Cloudflare の設定手順です。

## 前提条件

- Cloudflare アカウントを持っていること
- Resend アカウントを持っていること（無料枠: 3,000通/月）
- プロジェクトが Cloudflare Pages にデプロイされていること

---

## 1. Resend API キーの取得

### 1.1 Resend アカウント作成

1. [Resend](https://resend.com) にアクセス
2. 「Sign Up」からアカウント作成（GitHub/Google アカウントでもOK）
3. 無料プラン（3,000通/月）を選択

### 1.2 ドメイン認証

1. Resend ダッシュボードで「Domains」→「Add Domain」
2. `doujimafront.com` を追加
3. 表示される DNS レコードを Cloudflare DNS に追加：
   - **TXT レコード**: SPF認証用
   - **CNAME レコード**: DKIM認証用

**Cloudflare DNS での設定例:**

```
Type: TXT
Name: @
Content: v=spf1 include:resend.com ~all

Type: CNAME
Name: resend._domainkey
Content: resend._domainkey.resend.com
```

4. DNS 設定後、Resend で「Verify Domain」をクリック
5. 認証完了まで数分〜24時間待つ

### 1.3 API キーの取得

1. Resend ダッシュボードで「API Keys」→「Create API Key」
2. 名前を入力（例: `doujima-production`）
3. 権限: **Sending access** を選択
4. 「Create」をクリックし、API キーをコピー
5. **重要**: API キーは一度しか表示されないため、安全な場所に保存

---

## 2. Cloudflare KV Namespace の作成

レート制限機能に使用する KV Namespace を作成します。

### 2.1 KV Namespace の作成

1. Cloudflare Dashboard → 「Workers & Pages」
2. 「KV」タブ → 「Create namespace」
3. Namespace name: `RATE_LIMIT`
4. 「Add」をクリック
5. 作成された Namespace ID をコピー（例: `b17668227fe14cd28bf6ff52f1f81ba1`）

---

## 3. Cloudflare Pages の環境変数設定

### 3.1 環境変数の設定

1. Cloudflare Dashboard → 「Workers & Pages」
2. プロジェクト「doujima」を選択
3. 「Settings」→「Environment variables」
4. 「Add variable」で以下を追加：

| 変数名 | 値 | 説明 |
|--------|-----|------|
| `RESEND_API_KEY` | `re_xxxxxx...` | Resend API キー |
| `FROM_EMAIL` | `noreply@doujimafront.com` | 送信元メールアドレス |
| `RECIPIENT_EMAIL` | `info@doujimafront.com` | 受信先メールアドレス |
| `TURNSTILE_SECRET_KEY` | `0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM` | Turnstile Secret Key |

**注意事項:**
- 環境は「Production」と「Preview」の両方に設定
- `FROM_EMAIL` は Resend で認証済みのドメインのメールアドレスを使用
- `RECIPIENT_EMAIL` はフォーム送信先のメールアドレス

### 3.2 KV Namespace のバインディング

1. 同じ「Settings」ページで「Functions」タブ
2. 「KV namespace bindings」→「Add binding」
3. Variable name: `RATE_LIMIT`
4. KV namespace: 先ほど作成した `RATE_LIMIT` を選択
5. 「Save」をクリック

---

## 4. Cloudflare Turnstile の設定確認

### 4.1 既存の Turnstile サイト確認

プロジェクトで既に以下の Turnstile キーを使用しています：

- **Site Key**: `0x4AAAAAAB_1yaGfdV_epdP4`
- **Secret Key**: `0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM`

### 4.2 ドメイン設定の確認

1. Cloudflare Dashboard → 「Turnstile」
2. 該当のサイトを選択
3. 「Domains」に以下が含まれていることを確認：
   - `doujimafront.com`
   - `doujima.pages.dev`（Pages のプレビュー用）

追加が必要な場合は「Add」で追加してください。

---

## 5. DNS 設定（お名前.com → Cloudflare 移行）

### 5.1 お名前.com でネームサーバー変更

1. お名前.com にログイン
2. 「ドメイン設定」→「ネームサーバーの設定」
3. Cloudflare が指定するネームサーバーに変更：
   - `aaa.ns.cloudflare.com`
   - `bbb.ns.cloudflare.com`

### 5.2 Cloudflare DNS レコードの設定

1. Cloudflare Dashboard → 「DNS」
2. 必要な DNS レコードを追加：

```
# A レコード（サイト本体）
Type: A
Name: @
Content: [Pages の IP または CNAME]
Proxy: Enabled (オレンジクラウド)

# CNAME レコード（www）
Type: CNAME
Name: www
Content: doujimafront.com
Proxy: Enabled (オレンジクラウド)

# Resend の SPF/DKIM レコード（上記参照）
```

---

## 6. 動作確認

### 6.1 環境変数の確認

```bash
# ローカル開発環境
wrangler pages dev . --kv RATE_LIMIT

# 本番環境
# Cloudflare Dashboard で環境変数を確認
```

### 6.2 フォーム送信テスト

1. サイトにアクセス
2. お問い合わせフォームに入力
3. Turnstile チェックを完了
4. 送信ボタンをクリック
5. 成功メッセージが表示され、指定のメールアドレスにメールが届くことを確認

### 6.3 トラブルシューティング

**エラー: "RESEND_API_KEY が設定されていません"**
→ Cloudflare Pages の環境変数を確認

**エラー: "メール送信に失敗しました"**
→ Resend でドメイン認証が完了しているか確認
→ FROM_EMAIL が認証済みドメインのアドレスか確認

**エラー: "セキュリティ検証に失敗しました"**
→ Turnstile の Secret Key が正しく設定されているか確認
→ Turnstile のドメイン設定を確認

---

## 7. セキュリティのベストプラクティス

1. **API キーの管理**
   - API キーは環境変数に設定し、コードに直接書かない
   - 定期的にローテーション（3〜6ヶ月ごと）

2. **レート制限**
   - KV Namespace を使用した IP ベースのレート制限が有効
   - 5分間に3回まで送信可能

3. **スパム対策**
   - Turnstile によるボット検証
   - ハニーポットフィールドによるスパムボット対策

4. **メール送信**
   - SPF/DKIM 認証でなりすまし防止
   - 送信元ドメインは必ず認証済みドメインを使用

---

## 8. コスト見積もり

| サービス | プラン | 月額コスト |
|----------|--------|------------|
| Cloudflare Pages | 無料プラン | 無料 |
| Cloudflare KV | 無料枠 (100,000 read/day) | 無料 |
| Cloudflare Turnstile | 無料プラン | 無料 |
| Resend | 無料プラン (3,000通/月) | 無料 |

**注意**: フォーム送信が月 3,000 通を超える場合は、Resend の有料プラン（$20/月〜）へのアップグレードが必要です。

---

## 次のステップ

- [フォーム統合ガイド](./form-integration-guide.md) - フォームの詳細仕様
- [デプロイガイド](./deployment-guide.md) - 本番環境へのデプロイ手順
- [クライアント引き継ぎガイド](./client-meeting-guide.md) - クライアントへの説明資料
