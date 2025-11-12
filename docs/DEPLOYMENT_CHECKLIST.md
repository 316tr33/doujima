# 納品作業チェックリスト（Direct Upload版）

**所要時間**: 約 50-60 分（DNS伝播待ち時間含む）
**作業日**: **\_\_\_\_** 年 **\_\_\_\_** 月 **\_\_\_\_** 日
**作業者**: **\_\_\_\_**

**デプロイ方式**: Direct Upload + GitHub Actions

---

## ⚠️ 重要事項

### 絶対に失敗できない Critical Path

🔴 **Phase 1.2**: Resend API Key は再表示不可 → コピー失敗は致命的
🔴 **Phase 2.2**: Cloudflare API Token は再表示不可 → コピー失敗は致命的
🔴 **Phase 3.2**: ネームサーバー変更は破壊的操作 → 必ずメモ確認
🔴 **Phase 3.4→3.5**: "Active" 確認前の DNS レコード追加は Resend 認証失敗の原因
🔴 **Phase 5.2**: 環境変数誤入力は全フォーム機能停止

---

## 事前準備（自宅で完了必須）

### ✅ 完了していること
- [x] GitHub Actions ワークフローファイル作成（`.github/workflows/cloudflare-pages.yml`）
- [x] Git commit & push 完了
- [x] Production 環境でフォームテスト完了（`d92d129b.doujima.pages.dev`）
- [x] このチェックリストの印刷またはタブレット準備

### 📝 ワークフローファイルの確認

**確認URL**: https://github.com/316tr33/doujima/blob/main/.github/workflows/cloudflare-pages.yml

```yaml
# このファイルが存在することを確認
name: Deploy to Cloudflare Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      deployments: write
    steps:
      - uses: actions/checkout@v4
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy . --project-name=doujima
```

**⚠️ このファイルがない場合、Phase 2 に進めません！**

---

## Phase 0: 現地作業前の環境確認（5分）

**現地到着後、作業開始前に必ず実施:**

### 0.1 ネットワーク環境確認
- [ ] クライアント先のWi-Fiに接続完了
- [ ] インターネット接続テスト（`https://cloudflare.com` にアクセス）
- [ ] VPN 使用の場合は接続確認

### 0.2 アカウントアクセス確認
- [ ] GitHub アカウントログイン確認（https://github.com/316tr33/doujima）
- [ ] クライアントメールアドレスの最終確認（Resend用/フォーム受信用）
- [ ] クライアントがお名前.comにログイン可能か確認

### 0.3 クライアント情報確認
- [ ] お名前.com のログイン情報を準備してもらう
- [ ] Resend 用メールアドレスの最終確認
- [ ] 作業時間の最終合意（約60分）

### 0.4 事前準備の最終確認
- [ ] GitHub Actions ワークフローファイルが存在する
- [ ] GitHub リポジトリにアクセス可能
- [ ] GitHub Settings → Secrets → Actions にアクセス可能

**✅ Phase 0 完了確認**: 全項目チェック後、Phase 1へ

---

## Phase 1: Resend アカウント設定（15 分）

### 1.1 クライアントに Resend アカウント作成してもらう

**あなたの指示内容:**

```
1. https://resend.com/ にアクセス
2. 「Sign Up」をクリック
3. [クライアントのメールアドレス] を入力、パスワード設定
4. 認証メールが届くので、リンクをクリックして認証完了
```

### 1.2 API Key を作成してもらう

**🔴 重要**: この手順で失敗するとやり直し不可。慎重に進めてください。

**あなたの指示内容:**

```
1. Resendダッシュボードにログイン
2. 左メニューの「API Keys」をクリック
3. 「Create API Key」をクリック
4. Name: "doujima-production"
5. Permission: "Sending access"（デフォルト）
6. 「Create」をクリック
7. ⚠️ 表示されたAPI Keyを必ずコピー（再表示不可）
```

**あなたがメモ（必須）:**

```
RESEND_API_KEY: re_____________________________
（re_ で始まる32文字のランダム文字列）
```

**確認チェックリスト:**
- [ ] API Key が `re_` で始まっている
- [ ] 32文字程度の長さがある
- [ ] クライアントが「コピーしました」と確認

### 1.3 ドメイン認証設定（あなたが操作）

**🔴 重要**: ルートドメインではなく、**サブドメイン** `send.doujimafront.com` を追加します。
これにより、既存のメール（info@、sato@など）と競合しません。

**Resend ダッシュボードで:**

```
1. 左メニュー「Domains」→「Add Domain」
2. ⚠️ Domain: send.doujimafront.com （サブドメインを指定）
3. 「Add」をクリック
4. 表示される DNS レコード情報を全てメモ
```

**メモスペース（必ず全て記録）:**

```
【必須レコード】
SPF (TXT):
  - Name: _resend.send（または _resend.send.doujimafront.com）
  - Value: _________________________

DKIM (TXT or CNAME):
  - Name: _________________________.send（または完全修飾ドメイン名）
  - Value: _________________________

MX:
  - Name: send（または send.doujimafront.com）
  - Value: feedback-smtp.us-east-1.amazonses.com（または Resend 指定のサーバー）
  - Priority: 10
```

**📸 推奨**: スマートフォンでスクリーンショット撮影

**✅ Phase 1 完了確認:**
- [ ] Resend アカウント作成完了
- [ ] API Key メモ完了（`re_` で始まる）
- [ ] DNS レコード情報全てメモ完了

---

## Phase 2: Cloudflare API Token 発行と GitHub Secrets 登録（15 分）

### 2.1 クライアントの Cloudflare アカウント作成（5分）

**あなたの指示内容:**

```
1. https://dash.cloudflare.com/sign-up にアクセス
2. [クライアントのメールアドレス] を入力、パスワード設定
3. 認証メールのリンクをクリック
4. Cloudflare ダッシュボードにログイン完了を確認
```

**確認事項:**
- [ ] クライアントがダッシュボードにログインできている
- [ ] 「Welcome to Cloudflare」などの初期画面が表示されている

### 2.2 Cloudflare API Token 発行（あなたが指示、クライアントが操作）

**🔴 重要**: このトークンは再表示不可。必ずコピーしてください。

**あなたの指示内容:**

```
1. ダッシュボード右上のアイコン → 「My Profile」
2. 左メニュー「API Tokens」
3. 「Create Token」をクリック
4. 「Custom token」セクションの「Get started」をクリック
5. 以下を設定:

   Token name: GitHub Actions Deploy

   Permissions:
   - Account | Cloudflare Pages | Edit

   Account Resources:
   - Include | All accounts

6. 「Continue to summary」→「Create Token」
7. ⚠️ 表示されたトークンを必ずコピー（再表示不可）
```

**あなたがメモ（必須）:**

```
CLOUDFLARE_API_TOKEN: _________________________________________
（長い英数字の文字列）
```

**確認チェックリスト:**
- [ ] トークンがコピーされている
- [ ] クライアントが「Done」をクリックしてトークン画面を閉じていない

### 2.3 Cloudflare Account ID 取得（あなたが指示、クライアントが操作）

**あなたの指示内容:**

```
1. ダッシュボード左メニュー「Workers & Pages」をクリック
2. 右側の「Account details」セクションを確認
3. 「Account ID」をコピー
```

**あなたがメモ（必須）:**

```
CLOUDFLARE_ACCOUNT_ID: ________________________________
（32文字の英数字）
```

**確認チェックリスト:**
- [ ] Account ID が32文字程度
- [ ] 英数字のみで構成されている

### 2.4 GitHub Secrets 登録（あなたが操作）

**GitHub リポジトリで:**

```
1. https://github.com/316tr33/doujima/settings/secrets/actions を開く
2. 「New repository secret」をクリック

Secret 1:
  - Name: CLOUDFLARE_API_TOKEN
  - Value: [Phase 2.2でメモしたトークン]
  - 「Add secret」をクリック

3. もう一度「New repository secret」をクリック

Secret 2:
  - Name: CLOUDFLARE_ACCOUNT_ID
  - Value: [Phase 2.3でメモしたAccount ID]
  - 「Add secret」をクリック

4. Secrets 一覧に2つ表示されることを確認
```

**確認チェックリスト:**
- [ ] CLOUDFLARE_API_TOKEN が登録されている
- [ ] CLOUDFLARE_ACCOUNT_ID が登録されている
- [ ] 合計2個のSecretsが表示されている

### 2.5 初回デプロイ実行（あなたが操作）

**GitHub Actions で初回デプロイ:**

**方法1: Actions タブから手動実行（推奨）**

```
1. https://github.com/316tr33/doujima/actions を開く
2. 左側「Deploy to Cloudflare Pages」をクリック
3. 右側「Run workflow」ボタン → 「Run workflow」をクリック
4. デプロイ開始を確認（黄色の点が表示）
5. 完了を待つ（1-2分）
6. 緑色のチェックマークが表示されたら成功
```

**方法2: ダミーコミットで自動トリガー**

```bash
cd /Users/macmiller/Desktop/doujima
git commit --allow-empty -m "trigger: 初回デプロイ"
git push origin main
```

**デプロイ確認:**
- [ ] GitHub Actions が緑色のチェックマーク
- [ ] エラーが表示されていない
- [ ] 所要時間: 1-2分程度

### 2.6 Cloudflare でプロジェクト確認（クライアントのダッシュボード）

**クライアントのCloudflareダッシュボードで:**

```
1. 左メニュー「Workers & Pages」
2. 「doujima」プロジェクトが表示されていることを確認
3. プロジェクトをクリック
4. デプロイ履歴が1件表示されている
5. 「Visit site」リンクで *.pages.dev URL を確認
```

**確認チェックリスト:**
- [ ] doujima プロジェクトが存在する
- [ ] デプロイ履歴に1件（Success）
- [ ] *.pages.dev でサイトが表示される

**✅ Phase 2 完了確認:**
- [ ] Cloudflare アカウント作成完了
- [ ] API Token と Account ID メモ完了
- [ ] GitHub Secrets 登録完了（2個）
- [ ] 初回デプロイ成功
- [ ] Cloudflare に doujima プロジェクト表示

---

## Phase 3: ドメイン管理移管（DNS設定）（20-30 分、待機時間含む）

### 3.1 Cloudflareにドメイン追加（クライアントが操作）

**あなたの指示内容:**

```
1. Cloudflare ダッシュボード左メニュー「Websites」
2. 「Add a site」をクリック
3. Domain: doujimafront.com
4. 「Add site」をクリック
5. Plan: Free を選択
6. 「Continue」をクリック
```

### 3.2 Cloudflare ネームサーバー確認（あなたがメモ）

**DNS クイックスキャン後:**

```
Cloudflare が2つのネームサーバーを表示します:

Nameserver 1: __________.ns.cloudflare.com
Nameserver 2: __________.ns.cloudflare.com

⚠️ この2つを必ずメモしてください
```

**あなたがメモ（必須）:**

```
NS1: ________________________.ns.cloudflare.com
NS2: ________________________.ns.cloudflare.com
```

### 3.3 お名前.comでネームサーバー変更（クライアントが操作）

**🔴 重要**: ネームサーバー変更は破壊的操作です。慎重に進めてください。

**変更前の確認（必須）:**
- [ ] 現在のネームサーバーをスクリーンショット保存（バックアップ）
- [ ] Phase 3.2 でメモした NS1/NS2 を再確認

**あなたの指示:**

```
1. トップページ「ドメイン」タブ → 「ドメイン機能一覧」
2. 「ネームサーバーの設定」→「ネームサーバーの変更」
3. doujimafront.com にチェック
4. ⚠️ 現在のネームサーバーをスクリーンショット（念のため）
5. 「他のネームサーバーを利用」タブを選択
6. ネームサーバー1: [Phase 3.2でメモしたNS1]
7. ネームサーバー2: [Phase 3.2でメモしたNS2]
8. 入力内容を再確認（.ns.cloudflare.com で終わるか）
9. 「確認」→「OK」→ 完了確認メッセージ表示
```

**変更後の確認:**
- [ ] 「ネームサーバーの変更が完了しました」メッセージを確認
- [ ] 変更後のネームサーバーがCloudflareのものになっていることを確認

**📌 クライアントへの重要な説明:**

```
【ネームサーバー変更後も安心】
✅ お名前.com管理画面は引き続き使えます:
- ログイン・アクセスは今まで通り可能
- ドメイン更新・請求管理も変わらず利用可能
- ネームサーバー設定の再変更もいつでも可能

【何が変わるのか】
変更するのは「DNSレコード管理の場所」だけです:
- 今まで: お名前.comでDNSレコード管理
- これから: CloudflareでDNSレコード管理
- ドメインの所有権はお名前.comに残ります

【今回の作業は「ドメイン移管」ではありません】
- ドメイン移管（Registrar Transfer）: 登録管理自体を別会社に移す
- ネームサーバー変更: DNS管理だけを別サービスに委託
→ 今回は後者です。お名前.comとの契約は継続します。
```

### 3.4 ドメイン接続確認（重要：Active確認必須）

**🔴 Critical**: ドメインが "Active" になるまで Phase 3.5 に進めません。

**Cloudflare に戻って:**

```
1. 「Done, check nameservers」をクリック
2. 確認中... (数秒待機)
3. ステータスを確認
```

**ケース1: すぐに Active になった（ラッキー）**
```
表示: "Great news! Cloudflare is now protecting your site"
ステータス: Active（緑色）
→ すぐに Phase 3.5 へ進む
```

**ケース2: Pending のまま（通常パターン）**
```
表示: "We're checking your DNS records"
ステータス: Pending（オレンジ色）
→ DNS 伝播を待つ必要あり
```

**待機時間とその間の作業:**

```
【待機時間の目安】
- 通常: 2-6 時間
- 最短: 15-30 分
- 最長: 24-48 時間

【DNS伝播中のサイトアクセスについて】
⚠️ 重要な説明（クライアントに伝える）:

DNS伝播中、サイトは「完全に見れなくなる」わけではありません:
- 一部のユーザー/地域 → 新サーバー（Cloudflare）にアクセス可能
- 一部のユーザー/地域 → 旧サーバー（お名前.com等）にアクセス継続
- 同じ人でも、Wi-Fiとモバイルで違うサーバーに繋がることがある

これは「DNS伝播」の正常な動作です。
世界中のISPが段階的にキャッシュを更新するため、
最大48時間で全世界的に統一されます。

【お名前.com管理画面について】
✅ 安心してください:
- ネームサーバー変更後も、お名前.com Naviにログイン可能です
- ドメイン更新、請求管理、ネームサーバー再変更も可能
- お名前.comはドメイン登録管理を引き続き担当
- Cloudflareに移るのは「DNS管理権限」のみ

【待機中にできること】
1. クライアントとの打ち合わせ
2. 上記の「DNS伝播とは何か」をクライアントに説明
3. 休憩
4. 他の確認事項のレビュー

【確認方法】
- Cloudflare ダッシュボード → doujimafront.com のステータスを確認
- または dnschecker.org で NS レコードの伝播状況を確認
```

**⚠️ 絶対に守ること:**
```
ステータスが "Active" になるまで Phase 3.5 (DNS レコード追加) に進まない
理由: Pending 状態で DNS レコードを追加しても Resend 認証が失敗する
```

**Active 確認チェックリスト:**
- [ ] Cloudflare ダッシュボードで "Active" ステータスを確認
- [ ] サイト名の横に緑色のチェックマークを確認
- [ ] "Your site is active on Cloudflare" メッセージを確認

### 3.5 Resend の DNS レコード追加（サブドメイン用）

**🔴 重要**: サブドメイン `send.doujimafront.com` 用のDNSレコードを追加します。
ルートドメイン `doujimafront.com` のMXレコード（お名前.com）は**絶対に変更しません**。

**前提条件確認:**
- [ ] Phase 3.4 で "Active" ステータス確認済み
- [ ] Phase 1.3 でメモした DNS レコード情報を手元に用意
- [ ] メモした情報が `send.doujimafront.com` 用であることを再確認

**Cloudflare DNS 設定で追加（あなたが操作）:**

**1. SPF レコード (TXT) - サブドメイン用:**
```
Type: TXT
Name: _resend.send（または Phase 1.3 でメモした完全な Name）
Content: [Phase 1.3 でメモした SPF の Value]
TTL: Auto
⚠️ Proxy: DNS only（灰色の雲）← 必ず確認
```

**2. DKIM レコード (TXT または CNAME) - サブドメイン用:**
```
Type: [Resend が指定した Type (TXT or CNAME)]
Name: [Phase 1.3 でメモした DKIM の Name]
     （例: resend._domainkey.send または類似の形式）
Content: [Phase 1.3 でメモした DKIM の Value]
TTL: Auto
⚠️ Proxy: DNS only（灰色の雲）← 必ず確認
```

**3. MX レコード - サブドメイン用:**
```
Type: MX
Name: send（サブドメインを指定）
Content: [Phase 1.3 でメモした MX の Value]
⚠️ Content の末尾にピリオド「.」を追加（例: feedback-smtp.us-east-1.amazonses.com.）
Priority: 10
TTL: Auto
⚠️ Proxy 設定なし（MXレコードにはProxy設定不要）
```

**📌 既存メールの保護確認:**
```
Cloudflare DNS → Records で以下を確認:

✅ ルートドメイン @ のMXレコードは触っていない
   （お名前.comのメールサーバーがそのまま残っている）

✅ サブドメイン send のMXレコードが新規追加されている
   （Resend用）
```

**🔴 Name フィールド: 必ず「send」（サブドメイン）を指定
   「@」（ルートドメイン）にすると既存メールが壊れます**

**確認チェックリスト:**
- [ ] SPF レコード追加完了（_resend.send）
- [ ] DKIM レコード追加完了
- [ ] MX レコード追加完了（send）
- [ ] 全レコードが "DNS only" (灰色の雲)
- [ ] ルートドメイン @ の MX レコードに触れていない

**✅ Phase 3 完了確認:**
- [ ] Cloudflare アカウント作成完了
- [ ] Cloudflare にドメイン追加完了
- [ ] お名前.com でネームサーバー変更完了
- [ ] ドメインステータスが "Active" 確認
- [ ] Resend の DNS レコード 3 つ追加完了（サブドメイン send 用）
- [ ] 全レコードが "DNS only" (灰色) 確認
- [ ] ルートドメイン @ のMXレコードに触れていないことを確認

---

## Phase 4: Cloudflare Pages カスタムドメイン設定（5 分）

### 4.1 カスタムドメイン追加（クライアントが操作、あなたが指示）

**Cloudflare ダッシュボードで:**

```
1. Workers & Pages → doujima プロジェクトをクリック
2. 「Custom domains」タブ
3. 「Set up a domain」をクリック
4. Domain: doujimafront.com （サブドメインなし）
5. 「Continue」をクリック
6. DNS レコードが自動で追加される（CNAMEまたはA）
7. 「Activate domain」をクリック
```

**DNS レコード自動追加の確認:**
```
Cloudflare が自動的に以下を追加:
- Type: CNAME
- Name: doujimafront.com または @
- Target: doujima.pages.dev

または

- Type: A
- Name: doujimafront.com または @
- Target: [CloudflareのIPアドレス]
```

**確認チェックリスト:**
- [ ] カスタムドメインが "Active" ステータス
- [ ] DNS レコードが自動追加されている
- [ ] エラーメッセージが表示されていない

**✅ Phase 4 完了確認:**
- [ ] カスタムドメイン doujimafront.com が Active

---

## Phase 5: Cloudflare Turnstile とCloudflare Pages 環境変数設定（10 分）

### 5.1 Turnstile にドメイン追加（あなたが操作）

**🔴 Critical**: このPhaseを忘れると、本番環境でフォーム送信が100%失敗します。

**Cloudflare Turnstile ダッシュボード:**
```
1. クライアントのCloudflare ダッシュボード → Turnstile
2. 「Add site」をクリック
3. Site name: doujima
4. Domain: doujimafront.com を入力
5. 「Add additional domains」をクリックして以下も追加:
   - localhost
   - 127.0.0.1
6. Widget mode: Managed
7. 「Create」をクリック
8. Site Key と Secret Key をメモ
```

**⚠️ 重要**: 開発環境のSite Keyとは別の新しいキーが発行されます。

**あなたがメモ（必須）:**
```
TURNSTILE_SITE_KEY: 0x4AAAAAAA________________
TURNSTILE_SECRET_KEY: 0x4AAAAAAA________________
```

**確認チェックリスト:**
- [ ] doujimafront.com が登録されている
- [ ] localhost, 127.0.0.1 も登録されている
- [ ] Site Key と Secret Key をメモした

### 5.2 環境変数設定（クライアントが操作、あなたが指示）

**Cloudflare Pages プロジェクトで:**

```
1. Workers & Pages → doujima
2. 「Settings」タブ
3. 「Environment variables」セクション
4. 「Add variables」をクリック
```

**以下4つの環境変数を追加:**

**1. RESEND_API_KEY（重要）**
```
Variable name: RESEND_API_KEY
Value: [Phase 1.2 でメモした API Key]
⚠️ 入力後、もう一度値を確認（re_ で始まる32文字）
Encrypt: ✓（必ずチェック）
```

**2. FROM_EMAIL（変更）**
```
Variable name: FROM_EMAIL
Value: noreply@send.doujimafront.com
⚠️ 重要: サブドメイン send を含める必須
```

**3. RECIPIENT_EMAIL（変更）**
```
Variable name: RECIPIENT_EMAIL
Value: [クライアントの受信用メールアドレス]
⚠️ 入力後、クライアントに読み上げて確認
```

**4. TURNSTILE_SECRET_KEY（新規）**
```
Variable name: TURNSTILE_SECRET_KEY
Value: [Phase 5.1でメモしたSecret Key]
⚠️ この値は Phase 5.1 で取得した新しいキー
```

**保存前の最終確認:**
- [ ] RESEND_API_KEY が `re_` で始まる
- [ ] FROM_EMAIL が `noreply@send.doujimafront.com` になっている（サブドメイン含む）
- [ ] RECIPIENT_EMAIL がクライアントのアドレスになっている
- [ ] TURNSTILE_SECRET_KEY が Phase 5.1 のキーになっている

**「Save」をクリック**

**📌 重要な注意事項：環境変数とデプロイについて**

```
【デプロイ失敗リスクについて】
✅ 安心してください:
- 環境変数の値が間違っていても、デプロイ自体は成功します
- デプロイフェーズでは環境変数の「内容」をチェックしません
- 静的ファイル（HTML/CSS/JS）とFunctions（.js）がアップロードされるだけ

⚠️ ただし注意:
- 環境変数の値が正しいかどうかは「実行時」に初めてわかります
- Phase 6のテストで初めてエラーが判明する可能性があります

【もし Phase 6 でエラーが出たら】
1. どの環境変数が間違っているか特定
2. Phase 5.2 に戻って値を修正
3. Phase 5.3 で再デプロイ
4. Phase 6 のテストを再実行

【よくある間違い】
❌ RESEND_API_KEY: 「re_」で始まらない、32文字でない
❌ FROM_EMAIL: サブドメイン「send」が抜けている
❌ RECIPIENT_EMAIL: タイポ（@の前後が間違っている）
❌ TURNSTILE_SECRET_KEY: 古い開発環境のキーを使っている
```

### 5.3 再デプロイ

**環境変数変更後の再デプロイ（あなたが操作）:**

**方法1: GitHub Actions で再デプロイ（推奨）**

```bash
cd /Users/macmiller/Desktop/doujima
git commit --allow-empty -m "env: 本番環境変数設定完了"
git push origin main
```

**方法2: GitHub Actions タブから手動実行**

```
1. https://github.com/316tr33/doujima/actions
2. 左側「Deploy to Cloudflare Pages」
3. 「Run workflow」→「Run workflow」
```

**デプロイ完了確認:**
- [ ] GitHub Actions が緑色のチェックマーク
- [ ] デプロイ完了時刻が現在時刻になっている
- [ ] Cloudflare Pages に新しいデプロイが表示される

**✅ Phase 5 完了確認:**
- [ ] Turnstile に doujimafront.com 追加完了
- [ ] 環境変数 4 つ全て正しく設定（RESEND_API_KEY/FROM_EMAIL/RECIPIENT_EMAIL/TURNSTILE_SECRET_KEY）
- [ ] 再デプロイ完了（GitHub Actions Success）

---

## Phase 6: 最終テスト（10 分）

### 6.1 ドメインアクセス確認

**前提条件:**
- [ ] Phase 5.3 の再デプロイが Success になっている

**ブラウザで確認（あなたとクライアント両方で）:**

```
1. ブラウザのシークレットモード/プライベートモードで新規ウィンドウを開く
2. https://doujimafront.com にアクセス
3. ⚠️ HTTPSで接続されていることを確認（鍵マーク）
4. トップページが正常に表示されることを確認
5. 各ページの表示確認:
   - お遍路ページ: /Ohenro/index.html
   - 東海道ページ: /Tokaido/index.html
   - 採用ページ: /recruit.html
```

**確認事項:**
- [ ] 全ページが HTTPS で表示される
- [ ] 画像が全て表示される
- [ ] レイアウトが崩れていない
- [ ] モバイル表示も正常（スマートフォンでも確認）

### 6.2 お問い合わせフォームテスト

**トップページの「お問い合わせ」セクションで（あなたが操作）:**

```
1. 会社名: テスト株式会社
2. お名前: 山田太郎
3. メールアドレス: [あなたのテストメール]
4. サービス: 巡礼・先達手配
5. お問い合わせ内容: 納品テストメール
6. プライバシーポリシーに同意: ✓
7. Turnstile（ロボットでない）をクリック
8. 「送信する」をクリック
9. 「送信が完了しました」メッセージを確認
```

**クライアントの受信メールを確認してもらう:**
```
- 件名: 【お問い合わせ】テスト株式会社 - 巡礼・先達手配
- 差出人: 堂島フロント企画 お問い合わせフォーム <noreply@send.doujimafront.com>
  ⚠️ サブドメイン send が含まれていることを確認
- 本文: フォーム内容が整形されて表示
```

**確認事項:**
- [ ] フォーム送信が成功した
- [ ] クライアントがメールを受信した（1分以内）
- [ ] 差出人が `noreply@send.doujimafront.com` になっている（サブドメイン確認）

### 6.3 採用応募フォームテスト

**/recruit.html の「採用応募フォーム」で（あなたが操作）:**

```
1. お名前: 鈴木花子
2. フリガナ: スズキハナコ
3. メールアドレス: [あなたのテストメール]
4. 電話番号: 090-1234-5678
5. 応募職種: 先達・ガイド（チェック）
6. 志望動機: 納品テスト送信
7. プライバシーポリシーに同意: ✓
8. Turnstile（ロボットでない）をクリック
9. 「送信する」をクリック
10. 「送信が完了しました」メッセージを確認
```

**クライアントの受信メールを確認してもらう:**
```
- 件名: 【採用応募】鈴木花子 - 先達・ガイド
- 差出人: 堂島フロント企画 採用応募フォーム <noreply@send.doujimafront.com>
  ⚠️ サブドメイン send が含まれていることを確認
- 本文: 応募内容が整形されて表示
```

**確認事項:**
- [ ] フォーム送信が成功した
- [ ] クライアントがメールを受信した（1分以内）
- [ ] 差出人が `noreply@send.doujimafront.com` になっている（サブドメイン確認）

**✅ Phase 6 完了確認:**
- [ ] ドメイン https://doujimafront.com でサイトアクセス可能
- [ ] お問い合わせフォーム送信成功（メール受信確認）
- [ ] 採用応募フォーム送信成功（メール受信確認）
- [ ] Turnstile ボット対策正常動作
- [ ] 差出人が `noreply@send.doujimafront.com`（サブドメイン確認）

---

## Phase 7: クライアントへの説明（5 分）

### 7.1 運用説明

**📧 メールアドレスの使い分け:**

```
【既存メール（継続使用）】
✅ info@doujimafront.com
✅ sato@doujimafront.com
✅ tanaka@doujimafront.com
→ お名前.comのまま使用継続
→ 今まで通りメール送受信可能
→ 何も変更ありません

【新規メール（フォーム専用）】
🆕 noreply@send.doujimafront.com
→ Resendから自動送信専用
→ フォーム通知のみで使用
→ 受信はできません（noreply = 返信不要）
```

**フォーム送信があった場合:**

```
- 設定したメールアドレス（info@など）に自動で通知が届きます
- 差出人は noreply@send.doujimafront.com
- メール本文にお客様の連絡先が記載されています
- 返信が必要な場合は、info@doujimafront.com から通常のメールで返信してください
```

**月間送信制限:**

```
- 無料プラン: 月3,000通まで
- 現在の使用状況はResendダッシュボードで確認可能
- 超過する場合は有料プランへのアップグレードが必要
```

**セキュリティ機能:**

```
- Cloudflare Turnstile: ボット対策（自動）
- レート制限: 同一IPから5分間に3回まで（自動）
- ハニーポット: スパム対策（自動）
```

### 7.2 アカウント情報の整理

**クライアントに渡す情報まとめ:**

```
□ Resendアカウント
  - メールアドレス: _______________________
  - ログインURL: https://resend.com/login
  - 用途: メール送信サービス管理
  - 注意: API Key は再表示不可（必要な場合は新規作成）

□ Cloudflareアカウント
  - メールアドレス: _______________________
  - ログインURL: https://dash.cloudflare.com/
  - 用途: DNS管理、ホスティング管理
  - プロジェクト: doujima (Cloudflare Pages)
  - 注意: API Token は再表示不可（必要な場合は新規作成）

□ お名前.comアカウント（既存）
  - ログインURL: https://www.onamae.com/
  - 用途: ドメイン登録管理、既存メールサーバー
  - 注意: ネームサーバーは Cloudflare に変更済み
  - 重要: 既存メール（info@、sato@など）は継続使用可能

□ GitHubリポジトリ（開発者用）
  - URL: https://github.com/316tr33/doujima
  - 所有者: 開発者（316tr33）
  - 自動デプロイ: GitHub Actions で自動化済み
  - 注意: コード更新は開発者が実施
```

### 7.3 サイト更新の流れ

**クライアントへの説明:**

```
【通常の運用】
1. サイトの内容更新が必要になったら
   → 開発者（あなた）に連絡
2. 開発者がコードを更新して GitHub に push
   → GitHub Actions が自動的にデプロイ
3. 1-2分後、自動的にサイトが更新される

【環境変数の変更（受信メールアドレスなど）】
1. Cloudflare ダッシュボードにログイン
2. Workers & Pages → doujima → Settings → Environment variables
3. 変更したい変数を編集
4. 開発者に連絡して再デプロイ依頼
```

**✅ Phase 7 完了確認:**
- [ ] クライアントが Resend ダッシュボードにアクセス可能
- [ ] クライアントが Cloudflare ダッシュボードにアクセス可能
- [ ] 運用方法の説明完了
- [ ] アカウント情報を口頭またはドキュメントで引き渡し

---

## トラブルシューティング

### メールが届かない場合

**診断フローチャート:**

**Step 1: Resend ドメイン認証ステータス確認**
```
Resend Dashboard → Domains → send.doujimafront.com
Status: Verified（緑色）になっているか確認

✓ Verified → Step 3 へ
✗ Pending/Failed → Step 2 へ
```

**Step 2: Cloudflare の DNS レコード確認**
```
Cloudflare DNS → Records で以下を確認:

✓ _resend.send の TXT レコードが存在する
✓ [長い文字列].send の TXT/CNAME レコードが存在する
✓ send の MX レコードが存在する
✓ 全レコードが "DNS only"（灰色の雲）

→ 不足があれば Phase 3.5 に戻る
```

**Step 3: Cloudflare Pages 環境変数確認**
```
Workers & Pages → doujima → Settings → Environment variables

✓ RESEND_API_KEY が設定されている
✓ FROM_EMAIL = noreply@send.doujimafront.com
✓ RECIPIENT_EMAIL = [クライアントのアドレス]

→ 不足があれば Phase 5.2 に戻る
```

**Step 4: Cloudflare Pages ログ確認**
```
Workers & Pages → doujima → Logs

エラーメッセージを確認:
- "401 Unauthorized" → RESEND_API_KEY が間違っている
- "Domain not verified" → Resend ドメイン認証が未完了
- "Invalid email" → FROM_EMAIL が間違っている
```

### Turnstile が表示されない場合

**確認事項:**
```
1. Cloudflare Turnstile ダッシュボード
   → doujimafront.com が登録されているか

2. 環境変数 TURNSTILE_SECRET_KEY が正しいか
   → Phase 5.1 で取得した新しいキーを使用

3. ブラウザのコンソールエラー確認
   → F12 → Console タブ
   → Turnstile関連のエラーメッセージを確認
```

### サイトが表示されない場合

**確認事項:**
```
1. DNS 伝播状況確認
   → https://dnschecker.org で doujimafront.com を検索
   → 世界中で Cloudflare の IP に向いているか確認

2. Cloudflare Pages カスタムドメイン確認
   → Workers & Pages → doujima → Custom domains
   → doujimafront.com が "Active" になっているか

3. デプロイステータス確認
   → GitHub Actions が Success になっているか
   → Cloudflare Pages に最新のデプロイが表示されているか
```

---

## 📋 Phase 別チェックリスト（最終確認用）

**Phase 0: 環境確認**
- [ ] ネットワーク接続完了
- [ ] アカウントアクセス確認
- [ ] 事前準備完了（GitHub Actions ワークフローファイル存在）

**Phase 1: Resend**
- [ ] Resend アカウント作成完了
- [ ] RESEND_API_KEY メモ（re_ で始まる）
- [ ] DNS レコード情報メモ（SPF/DKIM/MX）

**Phase 2: Cloudflare + GitHub**
- [ ] Cloudflare アカウント作成完了
- [ ] CLOUDFLARE_API_TOKEN メモ
- [ ] CLOUDFLARE_ACCOUNT_ID メモ
- [ ] GitHub Secrets 登録完了（2個）
- [ ] 初回デプロイ成功

**Phase 3: DNS**
- [ ] Cloudflare にドメイン追加
- [ ] お名前.com でネームサーバー変更
- [ ] ドメインステータス "Active" 確認
- [ ] Resend DNS レコード追加（サブドメイン send）

**Phase 4: カスタムドメイン**
- [ ] doujimafront.com が Active

**Phase 5: Turnstile + 環境変数**
- [ ] Turnstile に doujimafront.com 追加
- [ ] 環境変数 4つ設定完了
- [ ] 再デプロイ成功

**Phase 6: テスト**
- [ ] サイトアクセス可能（HTTPS）
- [ ] お問い合わせフォーム送信成功
- [ ] 採用フォーム送信成功

**Phase 7: 引き渡し**
- [ ] 運用説明完了
- [ ] アカウント情報引き渡し完了

---

### 🎊 納品完了

**全ての項目にチェックが入ったら納品完了です。お疲れ様でした！**

**納品完了日時**: **\_\_\_\_** 年 **\_\_\_\_** 月 **\_\_\_\_** 日 **\_\_\_\_** 時 **\_\_\_\_** 分

**作業時間**: 約 **\_\_\_\_** 分（実測）

**特記事項・トラブル対応記録:**
```
_____________________________________________
_____________________________________________
_____________________________________________
```

---

## 参考: デプロイ方式の説明

**今回採用した方式: Direct Upload + GitHub Actions**

```
【仕組み】
あなたのGitHubリポジトリ（316tr33/doujima）
    ↓ Git push
GitHub Actions（自動実行）
    ↓ Wrangler CLI でデプロイ
クライアントのCloudflare Pages（doujima）
    ↓ カスタムドメイン
https://doujimafront.com
```

**【メリット】**
- ✅ クライアントはGitHubアカウント不要
- ✅ クライアントがCloudflareを完全管理
- ✅ 継続的デプロイ（Git push → 自動デプロイ）
- ✅ Cloudflare Pages Functions 完全対応

**【クライアントができること】**
- Cloudflare ダッシュボードでアクセス統計確認
- 環境変数の変更
- カスタムドメインの管理
- デプロイ履歴の確認

**【開発者（あなた）ができること】**
- コードの更新（Git push）
- 自動デプロイ実行
- GitHub Actions ワークフローの管理

---

## 参考: 環境変数一覧

**本番環境（納品後）:**

- FROM_EMAIL: noreply@send.doujimafront.com（⚠️ サブドメイン send 必須）
- RECIPIENT_EMAIL: [クライアント指定のアドレス]
- RESEND_API_KEY: [クライアントのアカウントで生成したキー]
- TURNSTILE_SECRET_KEY: [Phase 5.1 で取得したキー]

**📌 重要な補足:**

Resendは **send.doujimafront.com** というサブドメインで設定します。
これにより:
- ✅ 既存のメール（info@、sato@など）は影響なし
- ✅ お名前.comのメールサーバーはそのまま使用継続
- ✅ Resendのフォーム送信機能と既存メールが共存可能
