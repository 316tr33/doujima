# 納品作業チェックリスト

**所要時間**: 約30-45分
**作業日**: ________
**作業者**: ________

---

## 事前準備（自宅で完了）

- [x] Production環境でフォームテスト完了（`d92d129b.doujima.pages.dev`）
- [x] 全ドキュメント確認
- [ ] クライアントメールアドレス確認（事前にヒアリング）
- [ ] 作業用PC準備（GitHub、Cloudflareアクセス可能）

---

## Phase 1: Resendアカウント設定（15分）

### 1.1 クライアントにResendアカウント作成してもらう

**あなたの指示内容:**
```
1. https://resend.com/ にアクセス
2. 「Sign Up」をクリック
3. メールアドレスとパスワードを入力して登録
4. 認証メールが届くので、リンクをクリックして認証完了
```

### 1.2 API Keyを作成してもらう

**あなたの指示内容:**
```
1. Resendダッシュボードにログイン
2. 左メニューの「API Keys」をクリック
3. 「Create API Key」をクリック
4. Name: "doujima-production"
5. Permission: "Sending access"（デフォルト）
6. 「Create」をクリック
7. 表示されたAPI Keyをコピー（再表示不可なので注意）
```

**あなたがメモ:**
```
RESEND_API_KEY: re_____________________________
```

### 1.3 ドメイン認証設定（あなたが操作）

**Resendダッシュボードで:**
```
1. 左メニュー「Domains」→「Add Domain」
2. Domain: doujimafront.com
3. 表示されるDNSレコードをメモ:
   - TXT _resend.doujimafront.com
   - MX doujimafront.com
   - その他のレコード
```

**メモスペース:**
```
TXT _resend: _________________________
MX Record: __________________________
```

---

## Phase 2: Cloudflare DNS設定（10分）

### 2.1 お名前.comからCloudflareへDNS移管

**クライアントにお名前.comアカウントにログインしてもらう**

**あなたの作業:**
```
1. Cloudflare Dashboardで「Add a Site」
2. doujimafront.com を入力
3. プラン選択: Free
4. Cloudflareが既存のDNSレコードをスキャン
5. 必要なレコードを確認・追加
```

**お名前.comで設定変更（クライアントに指示）:**
```
1. ドメイン管理画面で「ネームサーバーの変更」
2. 「他のネームサーバーを利用」を選択
3. Cloudflareのネームサーバーを入力:
   - ネームサーバー1: ______.ns.cloudflare.com
   - ネームサーバー2: ______.ns.cloudflare.com
4. 保存
```

**待機時間**: DNS伝播（最大24時間、通常15-30分）

### 2.2 ResendのDNSレコード追加

**Cloudflare DNS設定で追加（あなたが操作）:**
```
Type: TXT
Name: _resend
Content: [Phase 1.3でメモした値]
TTL: Auto
Proxy: OFF（DNS only）

Type: MX
Name: @
Content: [Phase 1.3でメモした値]
Priority: 10
TTL: Auto
```

---

## Phase 3: Cloudflare Pages設定（10分）

### 3.1 カスタムドメイン追加

**Cloudflare Pagesダッシュボード（あなたが操作）:**
```
1. プロジェクト「doujima」を開く
2. 「Custom domains」タブ
3. 「Set up a custom domain」
4. Domain: doujimafront.com
5. 「Continue」→「Activate domain」
6. CNAMEレコードが自動追加される（確認のみ）
```

### 3.2 環境変数の更新

**Cloudflare Pages「Settings」→「Environment variables」:**

**Production環境で以下を編集:**
```
RESEND_API_KEY
Value: [Phase 1.2でメモしたAPI Key]
Encrypt: ✓

FROM_EMAIL
Value: noreply@doujimafront.com
（onboarding@resend.dev から変更）

RECIPIENT_EMAIL
Value: [クライアントの受信用メールアドレス]

TURNSTILE_SECRET_KEY
Value: 0x4AAAAAAB_1ya3SKxlzd7HV3dbnIFgKRdM
（変更なし、確認のみ）
```

**「Save」をクリック**

### 3.3 再デプロイ

**環境変数変更後の再デプロイ（あなたが操作）:**
```
1. Cloudflare Pagesの「Deployments」タブ
2. 最新のデプロイメントの右端「...」→「Retry deployment」
3. デプロイ完了を待つ（1-2分）
```

---

## Phase 4: 最終テスト（10分）

### 4.1 ドメインアクセス確認

**ブラウザで確認（あなたとクライアント両方で）:**
```
1. https://doujimafront.com にアクセス
2. サイトが正常に表示されることを確認
3. 各ページ（お遍路、東海道、採用）の表示確認
```

### 4.2 お問い合わせフォームテスト

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
- 差出人: 堂島フロント企画 お問い合わせフォーム <noreply@doujimafront.com>
- 本文: フォーム内容が整形されて表示
```

### 4.3 採用応募フォームテスト

**採用情報ページで（あなたが操作）:**
```
1. お名前: 山田花子
2. フリガナ: ヤマダハナコ
3. メールアドレス: [あなたのテストメール]
4. 電話番号: 090-1234-5678
5. 応募職種: 添乗員、先達（複数選択）
6. 年齢: 30
7. 志望動機: テスト送信です
8. プライバシーポリシーに同意: ✓
9. Turnstile確認
10. 「応募する」をクリック
```

**クライアントの受信メールを確認してもらう:**
```
- 件名: 【採用応募】山田花子 - 添乗員、先達
- 差出人: 堂島フロント企画 採用応募フォーム <noreply@doujimafront.com>
- 本文: 応募内容が整形されて表示
```

---

## Phase 5: クライアントへの説明（5分）

### 5.1 運用説明

**フォーム送信があった場合:**
```
- 設定したメールアドレスに自動で通知が届きます
- メール本文にお客様の連絡先が記載されています
- 返信が必要な場合は、通常のメールソフトで返信してください
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

### 5.2 アカウント情報の整理

**クライアントに渡す情報まとめ:**
```
□ Resendアカウント
  - メールアドレス: _______________________
  - ログインURL: https://resend.com/login
  - 用途: メール送信サービス管理

□ Cloudflareアカウント（既存）
  - ログインURL: https://dash.cloudflare.com/
  - 用途: DNS管理、ホスティング管理

□ GitHubリポジトリ（開発者用）
  - URL: https://github.com/316tr33/doujima
  - 権限: [必要に応じて招待]
```

---

## トラブルシューティング

### メールが届かない場合

**1. Resendドメイン認証を確認:**
```
Resend Dashboard → Domains → doujimafront.com
Status: Verified（緑色）になっているか確認
```

**2. CloudflareのDNSレコードを確認:**
```
TXT _resend.doujimafront.com が存在するか
MX doujimafront.com が存在するか
```

**3. DNS伝播を確認:**
```
https://dnschecker.org/ で doujimafront.com を検索
全世界で伝播しているか確認（最大24時間）
```

### Turnstile検証エラーの場合

**Cloudflare Turnstile設定を確認:**
```
1. Cloudflare Dashboard → Turnstile
2. Site Key: 0x4AAAAAAB_1yaGfdV_epdP4
3. Domains: doujimafront.com が登録されているか確認
4. 登録されていない場合は追加
```

### フォーム送信が403エラーになる場合

**環境変数を確認:**
```
Cloudflare Pages → Settings → Environment variables
- TURNSTILE_SECRET_KEY が正しく設定されているか
- Production環境に設定されているか確認
```

---

## 完了確認

**全てチェックできたら納品完了:**

- [ ] ドメイン https://doujimafront.com でサイトアクセス可能
- [ ] お問い合わせフォーム送信成功（メール受信確認）
- [ ] 採用応募フォーム送信成功（メール受信確認）
- [ ] クライアントがResendダッシュボードにアクセス可能
- [ ] クライアントがCloudflareダッシュボードにアクセス可能
- [ ] クライアントに運用方法を説明済み
- [ ] アカウント情報をクライアントに引き渡し済み

**納品完了日時**: ________ 年 ________ 月 ________ 日 ________ 時

---

## 参考: 現在のテスト環境情報

**テスト済みURL:**
- Production: https://d92d129b.doujima.pages.dev （テスト成功）
- Preview: https://e834a128.doujima.pages.dev （テスト成功）

**テスト用設定（現在）:**
- FROM_EMAIL: onboarding@resend.dev
- RECIPIENT_EMAIL: 316tr33@protonmail.com
- RESEND_API_KEY: re_92TC5R1g_8GSMUrnP1kKWoXvh5SKvkAcX（テスト用）

**本番設定（納品後）:**
- FROM_EMAIL: noreply@doujimafront.com
- RECIPIENT_EMAIL: [クライアント指定のアドレス]
- RESEND_API_KEY: [クライアントのアカウントで生成したキー]
