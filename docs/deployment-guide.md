# デプロイガイド

堂島フロント企画サイトの本番環境へのデプロイ手順を説明します。

## 前提条件

- Git リポジトリが GitHub に push されていること
- Cloudflare アカウントを持っていること
- Resend アカウントでドメイン認証が完了していること

---

## 1. ローカル開発環境でのテスト

### 1.1 環境変数の設定

`.dev.vars` ファイルを作成し、必要な環境変数を設定：

```bash
# .dev.vars
RESEND_API_KEY=re_your_api_key_here
FROM_EMAIL=noreply@doujimafront.com
RECIPIENT_EMAIL=info@doujimafront.com
TURNSTILE_SECRET_KEY=0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM
```

**注意**: `.dev.vars` は `.gitignore` に追加されているため、Git にコミットされません。

### 1.2 Wrangler のインストール

```bash
npm install -g wrangler
```

### 1.3 ローカルサーバーの起動

```bash
# KV Namespace を使用してローカル実行
wrangler pages dev . --kv RATE_LIMIT

# または npm script がある場合
npm run dev
```

ブラウザで http://localhost:8788 を開いてテスト。

### 1.4 フォーム送信テスト

1. お問い合わせフォームに入力
2. Turnstile チェックを完了
3. 送信ボタンをクリック
4. 成功メッセージが表示されることを確認
5. 受信先メールアドレスにメールが届くことを確認

---

## 2. Cloudflare Pages への初回デプロイ

### 2.1 GitHub リポジトリの準備

```bash
# ブランチを確認
git branch

# feature/resend-integration ブランチを push
git push origin feature/resend-integration

# main ブランチにマージ（レビュー後）
git checkout main
git merge feature/resend-integration
git push origin main
```

### 2.2 Cloudflare Pages プロジェクトの作成

1. Cloudflare Dashboard → 「Workers & Pages」
2. 「Create application」→「Pages」→「Connect to Git」
3. GitHub アカウントを連携
4. リポジトリ「doujima」を選択
5. ビルド設定:
   - **Framework preset**: None
   - **Build command**: (空欄)
   - **Build output directory**: `/`
   - **Root directory**: `/`
6. 「Save and Deploy」をクリック

### 2.3 環境変数の設定

デプロイ完了後、環境変数を設定：

1. プロジェクト「doujima」→「Settings」→「Environment variables」
2. 「Add variable」で以下を追加：

| 変数名 | 値 | 環境 |
|--------|-----|------|
| `RESEND_API_KEY` | `re_xxxxxx...` | Production, Preview |
| `FROM_EMAIL` | `noreply@doujimafront.com` | Production, Preview |
| `RECIPIENT_EMAIL` | `info@doujimafront.com` | Production, Preview |
| `TURNSTILE_SECRET_KEY` | `0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM` | Production, Preview |

3. 「Save」をクリック

### 2.4 KV Namespace のバインディング

1. 「Settings」→「Functions」タブ
2. 「KV namespace bindings」→「Add binding」
3. 設定:
   - **Variable name**: `RATE_LIMIT`
   - **KV namespace**: 作成済みの `RATE_LIMIT` を選択
   - **Environment**: Production と Preview 両方
4. 「Save」をクリック

### 2.5 再デプロイ

環境変数と KV バインディング設定後、再デプロイ：

```bash
# main ブランチに空コミット
git commit --allow-empty -m "Trigger redeploy with env vars"
git push origin main
```

または Cloudflare Dashboard の「Deployments」→「Retry deployment」

---

## 3. カスタムドメインの設定

### 3.1 DNS 設定（お名前.com → Cloudflare）

1. Cloudflare Dashboard → 「Websites」→「Add a site」
2. ドメイン `doujimafront.com` を入力
3. プラン選択（無料プランでOK）
4. DNS レコードの自動スキャン
5. 表示されたネームサーバーをメモ

**お名前.com での設定:**

1. お名前.com にログイン
2. 「ドメイン設定」→「ネームサーバーの設定」→「他のネームサーバーを利用」
3. Cloudflare のネームサーバーを入力：
   - 例: `aaa.ns.cloudflare.com`
   - 例: `bbb.ns.cloudflare.com`
4. 「確認画面へ進む」→「設定する」

**DNS 伝播の確認:**

```bash
# ネームサーバーの確認
nslookup -type=ns doujimafront.com

# A レコードの確認
nslookup doujimafront.com
```

伝播には最大24時間かかる場合があります。

### 3.2 Cloudflare Pages へのカスタムドメイン追加

1. Cloudflare Dashboard → 「Workers & Pages」→ プロジェクト「doujima」
2. 「Custom domains」タブ → 「Set up a custom domain」
3. ドメイン入力:
   - `doujimafront.com`
   - `www.doujimafront.com`（オプション）
4. 「Continue」→「Activate domain」

Cloudflare が自動的に DNS レコードを作成します。

### 3.3 SSL/TLS 設定

1. Cloudflare Dashboard → 「SSL/TLS」
2. 暗号化モード: **Full (strict)** を選択
3. 「Edge Certificates」→「Always Use HTTPS」を有効化

---

## 4. Resend ドメイン認証

### 4.1 SPF/DKIM レコードの追加

1. Resend ダッシュボード → 「Domains」→ `doujimafront.com`
2. 表示される DNS レコードを Cloudflare に追加：

**Cloudflare DNS での設定:**

```
Type: TXT
Name: @
Content: v=spf1 include:resend.com ~all
Proxy: DNS only (グレー)

Type: CNAME
Name: resend._domainkey
Content: resend._domainkey.resend.com
Proxy: DNS only (グレー)
```

3. Resend で「Verify Domain」をクリック
4. 認証完了まで数分〜24時間待つ

### 4.2 認証ステータスの確認

```bash
# SPF レコードの確認
nslookup -type=txt doujimafront.com

# DKIM レコードの確認
nslookup -type=cname resend._domainkey.doujimafront.com
```

Resend ダッシュボードで「Verified」と表示されれば完了。

---

## 5. 本番環境での動作確認

### 5.1 基本動作テスト

1. https://doujimafront.com にアクセス
2. お問い合わせフォームに入力
3. Turnstile チェックを完了
4. 送信ボタンをクリック
5. 成功メッセージが表示されることを確認
6. 受信先メールアドレスにメールが届くことを確認

### 5.2 セキュリティテスト

**Turnstile 検証:**
- Turnstile チェック前に送信できないこと
- Chrome DevTools で Turnstile トークンを削除して送信すると403エラーになること

**ハニーポット:**
- Chrome DevTools で隠しフィールド `website` に値を入力して送信すると403エラーになること

**レート制限:**
- 同一 IP から5分間に4回目の送信で429エラーになること

### 5.3 パフォーマンステスト

**ページ速度:**
```bash
# Lighthouse で計測
npm install -g lighthouse
lighthouse https://doujimafront.com --view
```

**目標値:**
- Performance: 90+
- Accessibility: 90+
- Best Practices: 90+
- SEO: 90+

### 5.4 モバイル動作確認

以下のデバイスでテスト：
- [ ] iPhone (Safari)
- [ ] Android (Chrome)
- [ ] タブレット (iPad, Android)

確認項目：
- [ ] フォーム入力が正常にできる
- [ ] Turnstile が表示・動作する
- [ ] 送信成功メッセージが表示される

---

## 6. 継続的デプロイ（CD）設定

### 6.1 自動デプロイの有効化

Cloudflare Pages は GitHub と連携しているため、`main` ブランチへの push で自動デプロイされます。

**デプロイフロー:**

```
git push origin main
  ↓
GitHub webhook
  ↓
Cloudflare Pages
  ↓
自動ビルド & デプロイ
  ↓
本番環境更新
```

### 6.2 プレビューデプロイ

Pull Request を作成すると、自動的にプレビュー環境がデプロイされます：

```
git checkout -b feature/new-feature
git push origin feature/new-feature
  ↓
GitHub Pull Request 作成
  ↓
Cloudflare Pages プレビューデプロイ
  ↓
https://[hash].doujima.pages.dev
```

プレビュー環境でテスト後、`main` にマージして本番デプロイ。

### 6.3 ロールバック

問題が発生した場合、過去のデプロイにロールバック可能：

1. Cloudflare Dashboard → 「Deployments」
2. ロールバックしたいデプロイを選択
3. 「Rollback to this deployment」をクリック

または Git で revert:

```bash
git revert HEAD
git push origin main
```

---

## 7. モニタリングとログ

### 7.1 デプロイログの確認

```bash
# リアルタイムログ
wrangler pages deployment tail

# または Dashboard の「Logs」セクション
```

### 7.2 エラー監視

**Cloudflare Analytics:**
1. Dashboard → プロジェクト「doujima」→「Analytics」
2. 「Web Analytics」でトラフィックを確認
3. 「Performance」でレスポンスタイムを確認

**Resend Analytics:**
1. Resend ダッシュボード → 「Emails」
2. 送信成功率、エラー率を確認
3. バウンス率、スパム報告を監視

### 7.3 アラート設定（オプション）

**Cloudflare Workers Analytics Engine:**
- 5xx エラー率が閾値を超えたらメール通知
- レスポンスタイムが遅い場合に通知

**Resend Webhooks:**
- メール配信失敗時に通知
- バウンス率が高い場合に通知

---

## 8. トラブルシューティング

### 8.1 デプロイが失敗する

**原因:** ビルドエラー、設定ミス

**対処法:**
```bash
# ローカルで再現確認
wrangler pages dev .

# ログ確認
wrangler pages deployment tail
```

### 8.2 環境変数が反映されない

**原因:** 環境変数設定後に再デプロイされていない

**対処法:**
```bash
# 空コミットで再デプロイ
git commit --allow-empty -m "Trigger redeploy"
git push origin main
```

### 8.3 メール送信が失敗する

**原因1:** Resend ドメイン未認証

**対処法:**
- Resend で DNS レコードを確認
- Cloudflare DNS に正しく追加されているか確認

**原因2:** FROM_EMAIL が認証済みドメインでない

**対処法:**
- `FROM_EMAIL` を `noreply@doujimafront.com` に設定
- Resend で `doujimafront.com` が認証済みか確認

**原因3:** Resend の送信制限超過

**対処法:**
- Resend ダッシュボードで送信数を確認
- 必要に応じて有料プランへアップグレード

### 8.4 Turnstile が動作しない

**原因:** ドメイン設定が不正

**対処法:**
1. Cloudflare Dashboard → 「Turnstile」
2. Site を選択 → 「Settings」
3. 「Domains」に以下を追加：
   - `doujimafront.com`
   - `www.doujimafront.com`
   - `doujima.pages.dev`

---

## 9. デプロイチェックリスト

### 9.1 デプロイ前

- [ ] ローカル環境でテスト完了
- [ ] Git に全変更がコミット済み
- [ ] Resend でドメイン認証完了
- [ ] Cloudflare で環境変数設定完了
- [ ] KV Namespace が作成済み

### 9.2 デプロイ後

- [ ] 本番 URL でサイトにアクセスできる
- [ ] フォーム送信が正常に動作する
- [ ] メールが受信先に届く
- [ ] Turnstile が正常に動作する
- [ ] レート制限が機能する
- [ ] モバイルで正常に動作する
- [ ] SSL/TLS が有効（https://)
- [ ] パフォーマンステスト合格

### 9.3 運用準備

- [ ] クライアントにログイン情報を共有
- [ ] ドキュメントを共有
- [ ] 緊急連絡先を確認
- [ ] バックアッププランを確認
- [ ] モニタリング設定完了

---

## 10. 次のステップ

- [Cloudflare セットアップガイド](./cloudflare-setup.md) - Cloudflare の詳細設定
- [フォーム統合ガイド](./form-integration-guide.md) - フォームの仕様詳細
- [クライアント引き継ぎガイド](./client-meeting-guide.md) - クライアントへの説明資料
