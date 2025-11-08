# DNS設定手順書

**対象読者:** クライアント、開発者
**最終更新:** 2025-11-06

---

## 目次

1. [DNS移行の概要](#dns移行の概要)
2. [方式A: DNSをCloudflareに移行（推奨）](#方式a-dnsをcloudflareに移行推奨)
3. [方式B: お名前.comのDNSを継続使用](#方式b-お名前comのdnsを継続使用)
4. [トラブルシューティング](#トラブルシューティング)

---

## DNS移行の概要

### DNS移行とドメイン移管の違い

| 項目 | DNS移行（Cloudflare） | ドメイン移管 |
|-----|---------------------|-----------|
| **変更内容** | ネームサーバーのみ変更 | ドメイン管理会社を変更 |
| **お名前.comの契約** | 継続（ドメイン更新は引き続きお名前.comで） | 終了（Cloudflareに移行） |
| **メール設定** | 維持される | 移行作業が必要 |
| **リスク** | 低（MXレコードをコピーすれば安全） | 高（移管ミスでサイトやメールが停止） |
| **費用** | 無料（お名前.comの更新費用は継続） | Cloudflareドメイン管理費用 |
| **推奨度** | ★★★★★ | ★★☆☆☆（不要） |

**結論:** DNS移行（方式A）を推奨します。ドメイン移管は不要です。

### 方式A vs 方式B の比較

| 項目 | 方式A（DNS移行） | 方式B（DNS継続） |
|-----|---------------|----------------|
| **費用** | 完全無料 | 月3,000通まで無料（Resend）<br>超過時：$20/月〜 |
| **メール設定** | MXレコードをコピーするだけ | Resend APIの設定が必要 |
| **速度** | 高速（Cloudflare CDN） | 通常速度 |
| **セキュリティ** | DDoS保護、SSL自動更新 | 標準 |
| **設定難易度** | 中（DNS知識が少し必要） | 低（お名前.comのDNSをそのまま使用） |
| **リスク** | 低（MXレコード設定ミスでメール停止の可能性） | 極低（既存のメール設定を触らない） |
| **推奨度** | ★★★★★（長期的なメリット大） | ★★★☆☆（すぐに運用開始したい場合） |

### メリット・デメリット

#### 方式A: DNSをCloudflareに移行

**メリット:**

- 完全無料（MailChannels APIが無料で使える）
- Cloudflare CDNで高速化
- DDoS攻撃保護
- SSL証明書自動更新
- DNS管理が一箇所に集約

**デメリット:**

- MXレコードのコピーが必要（ミスするとメール停止）
- DNS反映待ち（1〜2時間、最大48時間）
- お名前.comのDNS設定画面は使えなくなる

#### 方式B: お名前.comのDNSを継続使用

**メリット:**

- メール設定を触らない（リスクゼロ）
- 既存のDNS設定をそのまま使用
- お名前.comの管理画面で引き続き操作可能

**デメリット:**

- メール送信API（Resend）が必要（月3,000通超過時は有料）
- Cloudflare CDNの恩恵を受けられない
- 2箇所のサービス管理が必要（お名前.com + Cloudflare）

### リスク評価

| リスク | 方式A | 方式B |
|-------|------|------|
| **メール停止** | 中（MXレコード設定ミス時） | 極低 |
| **サイト停止** | 極低（DNSは即座に元に戻せる） | 極低 |
| **データ損失** | なし | なし |
| **費用増加** | なし | 可能性あり（メール送信量次第） |

**推奨:** クライアントと相談し、リスクを理解した上で方式Aを選択することを推奨します。

---

## 方式A: DNSをCloudflareに移行（推奨）

### 事前準備チェックリスト

- [ ] お名前.comの管理画面にログイン可能
- [ ] 現在のメールサーバーが正常に動作している
- [ ] お名前.comのMXレコード設定を確認できる
- [ ] Cloudflareアカウントを作成済み
- [ ] 作業時間を2〜3時間確保（DNS反映待ち含む）

### ステップ1: お名前.comの現在のDNS設定を確認

#### 1-1. お名前.comの管理画面にログイン

1. https://www.onamae.com/ にアクセス
2. **お名前.com Navi ログイン**
3. お名前ID（会員ID）とパスワードを入力

#### 1-2. DNS設定を確認

1. **ドメイン設定** → **DNS設定/転送設定**
2. `doujimafront.com` を選択
3. **DNSレコード設定を利用する** → **設定する**

#### 1-3. MXレコードを確認（最重要）

以下の情報をメモ帳にコピーしてください:

| タイプ | ホスト名 | VALUE（メールサーバー） | 優先度 | TTL |
|-------|---------|---------------------|-------|-----|
| MX    | @       | mail.example.com    | 10    | 3600 |
| MX    | @       | mail2.example.com   | 20    | 3600 |

**例:**

```
MX @ mail.doujimafront.com 10 3600
MX @ mail2.doujimafront.com 20 3600
```

**注意:** MXレコードが複数ある場合、すべてコピーしてください。

#### 1-4. SPFレコードを確認（推奨）

| タイプ | ホスト名 | VALUE |
|-------|---------|-------|
| TXT   | @       | v=spf1 include:example.com ~all |

**例:**

```
TXT @ v=spf1 include:_spf.google.com ~all
```

#### 1-5. その他のレコードを確認

| タイプ | ホスト名 | VALUE | TTL |
|-------|---------|-------|-----|
| A     | @       | 123.456.789.10 | 3600 |
| CNAME | www     | @              | 3600 |

**すべてのレコードをメモ帳にコピーしてください。**

### ステップ2: Cloudflareにサイトを追加

#### 2-1. Cloudflareダッシュボードにアクセス

1. https://dash.cloudflare.com/ にログイン
2. 左サイドバー → **Websites**
3. **Add a site** ボタンをクリック

#### 2-2. ドメインを入力

1. **Enter your site (example.com):** `doujimafront.com`
2. **Continue** をクリック

#### 2-3. プランを選択

1. **Free $0/month** を選択（推奨）
2. **Continue** をクリック

**無料プランで十分です。有料プランは不要です。**

### ステップ3: DNSレコードをCloudflareにコピー

Cloudflareが自動的に既存のDNSレコードをスキャンしますが、**手動で確認・追加が必要です。**

#### 3-1. MXレコードを追加（最重要）

1. **Add record** をクリック
2. 以下の情報を入力:

| 項目 | 入力値 |
|-----|-------|
| **Type** | `MX` |
| **Name** | `@`（ルートドメイン） |
| **Mail server** | `mail.doujimafront.com`（ステップ1-3でコピーした値） |
| **Priority** | `10`（優先度） |
| **TTL** | `Auto` |

3. **Save** をクリック

**複数のMXレコードがある場合、すべて追加してください。**

#### 3-2. SPFレコードを追加（推奨）

1. **Add record** をクリック
2. 以下の情報を入力:

| 項目 | 入力値 |
|-----|-------|
| **Type** | `TXT` |
| **Name** | `@` |
| **Content** | `v=spf1 include:_spf.google.com ~all`（ステップ1-4でコピーした値） |
| **TTL** | `Auto` |

3. **Save** をクリック

**MailChannels用のSPFレコードも追加（推奨）:**

```
v=spf1 include:_spf.mx.cloudflare.net include:_spf.google.com ~all
```

#### 3-3. Aレコードを追加（Cloudflare Pages用）

1. **Add record** をクリック
2. 以下の情報を入力:

| 項目 | 入力値 |
|-----|-------|
| **Type** | `CNAME` |
| **Name** | `@` |
| **Target** | `doujima.pages.dev`（Cloudflare PagesのURL） |
| **Proxy status** | `Proxied`（オレンジ色） |
| **TTL** | `Auto` |

3. **Save** をクリック

**wwwサブドメインも追加（推奨）:**

| 項目 | 入力値 |
|-----|-------|
| **Type** | `CNAME` |
| **Name** | `www` |
| **Target** | `doujimafront.com` |
| **Proxy status** | `Proxied` |
| **TTL** | `Auto` |

#### 3-4. その他のレコードを追加

お名前.comで確認したすべてのレコードをCloudflareにコピーしてください。

**注意:** Cloudflareが自動スキャンしたレコードは、**すべて正しいか手動で確認してください。**

### ステップ4: ネームサーバーを変更

#### 4-1. Cloudflareのネームサーバーを確認

Cloudflareダッシュボードに以下のように表示されます:

```
Change your nameservers to:

ns1.cloudflare.com
ns2.cloudflare.com
```

**このネームサーバーをメモ帳にコピーしてください。**

#### 4-2. お名前.comでネームサーバーを変更

1. お名前.com Naviにログイン
2. **ドメイン設定** → **ネームサーバーの設定**
3. `doujimafront.com` を選択
4. **他のネームサーバーを利用** を選択
5. Cloudflareのネームサーバーを入力:

   - プライマリネームサーバー: `ns1.cloudflare.com`
   - セカンダリネームサーバー: `ns2.cloudflare.com`

6. **確認画面へ進む** → **設定する** をクリック

**重要:** ネームサーバー変更後、お名前.comのDNS設定画面は使えなくなります。すべての DNS 設定は Cloudflare で行います。

### ステップ5: DNS反映を待つ

#### 5-1. 反映時間

- **通常:** 1〜2時間
- **最大:** 48時間（まれ）

#### 5-2. Cloudflareダッシュボードで確認

1. Cloudflareダッシュボード → **Websites** → `doujimafront.com`
2. ステータスが **Active** になったら完了

**"Pending Nameserver Update" の間は待機してください。**

#### 5-3. 手動で反映を確認（コマンドライン）

**Windowsの場合:**

```cmd
nslookup doujimafront.com
```

**Mac/Linuxの場合:**

```bash
dig doujimafront.com
```

**期待される結果:**

```
;; ANSWER SECTION:
doujimafront.com.  300  IN  A  172.67.xxx.xxx
```

Cloudflare の IP アドレスが返ってくれば成功です。

### ステップ6: メール送信テスト

**重要:** DNS反映後、必ずメール送信テストを行ってください。

#### 6-1. テストメール送信

1. メールクライアント（Outlook、Gmail等）を開く
2. テストメールを `info@doujimafront.com` に送信
3. 受信を確認

#### 6-2. テストメール受信

1. `info@doujimafront.com` からテストメールを送信
2. 別のメールアドレスで受信を確認

#### 6-3. フォームからのメール送信テスト

1. https://doujimafront.com/index.html にアクセス
2. お問い合わせフォームからテスト送信
3. `info@doujimafront.com` でメール受信を確認

**問題があればすぐに次のステップへ進んでください。**

### ステップ7: 問題発生時の緊急対応（ロールバック）

#### メールが届かない場合

**即座にお名前.comのネームサーバーに戻す:**

1. お名前.com Naviにログイン
2. **ドメイン設定** → **ネームサーバーの設定**
3. `doujimafront.com` を選択
4. **お名前.comのネームサーバーを利用** を選択
5. **確認画面へ進む** → **設定する** をクリック

**反映時間:** 30分〜2時間

**その間にCloudflareのMXレコード設定を見直してください。**

---

## 方式B: お名前.comのDNSを継続使用

### 事前準備チェックリスト

- [ ] お名前.comの管理画面にログイン可能
- [ ] Cloudflare Pagesのデプロイが完了している
- [ ] Cloudflare PagesのURL（`doujima.pages.dev`）を確認済み
- [ ] Resendアカウントを作成済み（メール送信API用）

### ステップ1: Cloudflare Pagesにデプロイ

すでに `deployment-guide.md` に従ってデプロイが完了している前提です。

**確認:**

1. https://doujima.pages.dev にアクセス
2. サイトが正常に表示されることを確認

### ステップ2: お名前.comでCNAMEレコード追加

#### 2-1. お名前.comの管理画面にログイン

1. https://www.onamae.com/ にアクセス
2. **お名前.com Navi ログイン**

#### 2-2. DNSレコード設定を開く

1. **ドメイン設定** → **DNS設定/転送設定**
2. `doujimafront.com` を選択
3. **DNSレコード設定を利用する** → **設定する**

#### 2-3. CNAMEレコードを追加

1. **追加** ボタンをクリック
2. 以下の情報を入力:

| 項目 | 入力値 |
|-----|-------|
| **TYPE** | `CNAME` |
| **ホスト名** | `@`（ルートドメイン）または `www` |
| **VALUE** | `doujima.pages.dev` |
| **TTL** | `3600` |

**注意:** お名前.comではルートドメイン（`@`）にCNAMEを設定できない場合があります。その場合、以下のように設定してください:

- **wwwサブドメインのみ:**

  | ホスト名 | VALUE |
  |---------|-------|
  | `www`   | `doujima.pages.dev` |

- **ルートドメインはAレコード:**

  | TYPE | ホスト名 | VALUE |
  |-----|---------|-------|
  | `A` | `@`     | `172.67.xxx.xxx`（Cloudflare PagesのIPアドレス） |

  **Cloudflare PagesのIPアドレス取得方法:**

  ```bash
  nslookup doujima.pages.dev
  ```

3. **追加** をクリック

#### 2-4. DNS反映を待つ

- **通常:** 30分〜1時間
- **最大:** 24時間

**反映確認:**

```bash
nslookup www.doujimafront.com
```

### ステップ3: Cloudflare Pagesにカスタムドメインを追加

#### 3-1. Cloudflare Pagesダッシュボードにアクセス

1. https://dash.cloudflare.com/ にログイン
2. **Workers & Pages** → **doujima** プロジェクト
3. **Custom domains** タブをクリック

#### 3-2. カスタムドメインを追加

1. **Set up a custom domain** をクリック
2. **Domain:** `www.doujimafront.com`（または `doujimafront.com`）
3. **Continue** をクリック
4. DNS設定の確認画面が表示される
5. **Activate domain** をクリック

**Cloudflareが自動的にSSL証明書を発行します（1〜5分）。**

### ステップ4: Resendでメール送信APIを設定

#### 4-1. Resendアカウント作成

1. https://resend.com/ にアクセス
2. **Sign Up** をクリック
3. GitHubアカウントで認証（推奨）

#### 4-2. ドメインを追加

1. Resendダッシュボード → **Domains**
2. **Add Domain** をクリック
3. **Domain:** `doujimafront.com`
4. **Region:** `US-East (us-east-1)`（推奨）
5. **Add** をクリック

#### 4-3. DNS設定を追加

Resendが以下のDNSレコードを表示します:

**SPFレコード:**

```
Type: TXT
Name: @
Value: v=spf1 include:amazonses.com ~all
```

**DKIMレコード（複数）:**

```
Type: TXT
Name: resend._domainkey
Value: p=MIGfMA0GCSqGSIb3DQEBAQUAA4...
```

**お名前.comのDNS設定画面でこれらのレコードを追加してください。**

#### 4-4. ドメイン検証を待つ

- Resendが自動的にDNSレコードを検証します（5〜10分）
- **Status** が **Verified** になったら完了

#### 4-5. APIキーを取得

1. Resendダッシュボード → **API Keys**
2. **Create API Key** をクリック
3. **Name:** `doujima-production`
4. **Permission:** `Sending access`
5. **Domain:** `doujimafront.com`
6. **Create** をクリック
7. APIキーをコピー（例: `re_123456789abcdefghijklmnopqrstuvwxyz`）

**このAPIキーはCloudflare Pagesの環境変数に設定します。**

### ステップ5: Cloudflare Pagesの環境変数を更新

#### 5-1. 環境変数を追加

1. Cloudflare ダッシュボード → **Workers & Pages** → **doujima**
2. **Settings** → **Environment variables**
3. 以下を追加:

| Variable name | Value | Type |
|--------------|-------|------|
| RESEND_API_KEY | `re_123456789...` | Secret |

#### 5-2. コード修正（`functions/submit-contact.js`）

MailChannels APIの代わりにResend APIを使用するようコードを修正します。

**変更前（MailChannels）:**

```javascript
const response = await fetch('https://api.mailchannels.net/tx/v1/send', {
  // ...
});
```

**変更後（Resend）:**

```javascript
const response = await fetch('https://api.resend.com/emails', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    from: 'noreply@doujimafront.com',
    to: env.RECIPIENT_EMAIL,
    subject: subject,
    text: mailBody,
  }),
});
```

**同様の修正を `functions/submit-recruit.js` にも適用してください。**

#### 5-3. GitHubにプッシュして再デプロイ

```bash
git add functions/
git commit -m "feat: Resend APIに切り替え"
git push origin main
```

### ステップ6: テスト

1. https://www.doujimafront.com/ にアクセス
2. お問い合わせフォームからテスト送信
3. メール受信を確認

---

## トラブルシューティング

### 問題1: DNS反映が遅い

**症状:**

- ネームサーバー変更後、24時間経ってもサイトが表示されない
- Cloudflareのステータスが "Pending" のまま

**原因:**

- DNSキャッシュが古い情報を保持している
- ISPのDNSサーバーが反映されていない

**対処法:**

1. **ローカルDNSキャッシュをクリア:**

   **Windows:**
   ```cmd
   ipconfig /flushdns
   ```

   **Mac:**
   ```bash
   sudo dscacheutil -flushcache
   sudo killall -HUP mDNSResponder
   ```

   **Linux:**
   ```bash
   sudo systemd-resolve --flush-caches
   ```

2. **Public DNSサーバーで確認:**

   ```bash
   nslookup doujimafront.com 8.8.8.8
   ```

   Googleの Public DNS（8.8.8.8）で確認すると、最新の情報が取得できます。

3. **別のネットワークで確認:**

   - モバイルデータ通信（Wi-Fiをオフ）
   - 別のWi-Fiネットワーク
   - VPN経由

4. **Cloudflareサポートに問い合わせ:**

   https://support.cloudflare.com/

### 問題2: メールが届かない

**症状:**

- DNS移行後、メールが送受信できない
- メールサーバーエラーが表示される

**原因:**

- MXレコードの設定ミス
- SPFレコードが欠落している
- メールサーバーのIPアドレスが変更された

**対処法:**

1. **MXレコードを確認:**

   ```bash
   nslookup -type=MX doujimafront.com
   ```

   **期待される結果:**

   ```
   doujimafront.com   mail exchanger = 10 mail.doujimafront.com.
   ```

   お名前.comで確認したMXレコードと一致しているか確認してください。

2. **SPFレコードを確認:**

   ```bash
   nslookup -type=TXT doujimafront.com
   ```

   **期待される結果:**

   ```
   doujimafront.com   text = "v=spf1 include:_spf.google.com ~all"
   ```

3. **メールサーバーの動作確認:**

   ```bash
   telnet mail.doujimafront.com 25
   ```

   接続できればメールサーバーは正常です。

4. **Cloudflare DNSで設定を修正:**

   - Cloudflareダッシュボード → **DNS** → **Records**
   - MXレコードを再確認・修正

5. **緊急時: お名前.comに戻す:**

   ステップ7の手順に従ってネームサーバーを元に戻してください。

### 問題3: ネームサーバー変更を元に戻す方法

**手順:**

1. お名前.com Naviにログイン
2. **ドメイン設定** → **ネームサーバーの設定**
3. `doujimafront.com` を選択
4. **お名前.comのネームサーバーを利用** を選択
5. **確認画面へ進む** → **設定する** をクリック

**反映時間:** 30分〜2時間

**注意:** 元に戻した後、Cloudflareで追加したDNSレコード（Aレコード等）は失われます。お名前.comで再度設定してください。

### 問題4: Resendメール送信が失敗する（方式B）

**症状:**

- フォーム送信後、「メール送信に失敗しました」というエラーが表示される
- Resend APIが400エラーを返す

**原因:**

- RESEND_API_KEYが間違っている
- ドメイン検証が完了していない
- APIキーの権限が不足している

**対処法:**

1. **環境変数を確認:**

   Cloudflare ダッシュボード → **Settings** → **Environment variables**

   - `RESEND_API_KEY` が正しく設定されているか確認

2. **Resendダッシュボードで確認:**

   - **Domains** → `doujimafront.com` のステータスが **Verified** か確認
   - **API Keys** → 使用中のキーが有効か確認

3. **APIキーの権限を確認:**

   - **Permission:** `Sending access`
   - **Domain:** `doujimafront.com`

4. **ログを確認:**

   Cloudflare ダッシュボード → **Logs**

   エラーメッセージから原因を特定:

   ```
   Resend API エラー: 400 - Invalid API key
   ```

5. **APIキーを再生成:**

   Resendダッシュボード → **API Keys** → 古いキーを削除 → 新しいキーを作成

---

## 次のステップ

DNS設定が完了したら、以下のドキュメントを参照してください:

- **テスト手順:** `docs/testing-guide.md`
- **クライアント会議:** `docs/client-meeting-guide.md`

---

## サポート情報

### 公式ドキュメント

- **Cloudflare DNS:** https://developers.cloudflare.com/dns/
- **お名前.com ネームサーバー設定:** https://help.onamae.com/
- **Resend API:** https://resend.com/docs

### 問題報告

プロジェクト固有の問題は開発チームに連絡してください。
