# クライアント会議用資料

**対象読者:** 開発者（あなた）
**最終更新:** 2025-11-06

---

## 目次

1. [会議の目的](#会議の目的)
2. [会議前の準備](#会議前の準備)
3. [会議アジェンダ（90分）](#会議アジェンダ90分)
4. [会議後のフォローアップ](#会議後のフォローアップ)
5. [想定Q&A](#想定qa)

---

## 会議の目的

### 1. フォーム機能のデモ

- お問い合わせフォームの動作確認
- 採用応募フォームの動作確認
- スパム対策機能の説明
- プライバシーポリシーページの確認

### 2. DNS設定方式の決定

- 方式A（DNSをCloudflareに移行）vs 方式B（お名前.comのDNSを継続）の比較
- メリット・デメリット・リスクの説明
- クライアントの意思決定をサポート

### 3. デプロイ作業の実施

- 選択した方式に基づいてデプロイ作業を実施
- または、デプロイ日程のスケジュール調整

---

## 会議前の準備

### 完了済み項目（確認用）

- [x] Pages Functions実装完了（`functions/submit-contact.js`、`functions/submit-recruit.js`）
- [x] プライバシーポリシーページ作成（`privacy-policy.html`）
- [x] HTML/JavaScript実装完了（フォーム送信処理）
- [x] ローカルテスト完了（wrangler dev）
- [x] ドキュメント作成完了（deployment-guide.md、dns-setup-guide.md、testing-guide.md）

### 会議前日までに準備すること

#### 1. デモ環境の準備

**ローカル開発サーバーを起動:**

```bash
cd /Users/macmiller/Desktop/doujima
wrangler pages dev . --port 8788
```

**確認URL:**

- トップページ: http://localhost:8788/index.html
- 採用ページ: http://localhost:8788/recruit.html
- プライバシーポリシー: http://localhost:8788/privacy-policy.html

**動作確認項目:**

- [ ] お問い合わせフォームが正常に表示される
- [ ] 採用応募フォームが正常に表示される
- [ ] Turnstileウィジェットが表示される（サイトキー設定後）
- [ ] プライバシーポリシーへのリンクが機能する

#### 2. プレゼンテーション資料の準備

**デモシナリオ:**

1. **お問い合わせフォーム**
   - 必須フィールドの未入力エラー
   - メールアドレス形式エラー
   - Turnstile検証（サイトキー設定後）
   - 送信成功メッセージ

2. **採用応募フォーム**
   - 履歴書添付（将来実装予定として説明）
   - 希望職種の複数選択
   - 送信成功メッセージ

3. **スパム対策**
   - Turnstile（Cloudflareのボット検出）
   - ハニーポット（隠しフィールドでスパム判定）
   - レート制限（5分間に3回まで）

#### 3. DNS設定方式の比較表を印刷

**プリントアウト推奨:**

- `docs/dns-setup-guide.md` の「方式A vs 方式Bの比較」セクション

**スクリーンシェア用に準備:**

- Cloudflareダッシュボードのスクリーンショット
- お名前.comのDNS設定画面のスクリーンショット

#### 4. 必要なアカウント情報を確認

**クライアントに事前確認:**

- [ ] お名前.comの管理画面ログイン情報（ID・パスワード）
- [ ] 受信先メールアドレス（例: info@doujimafront.com）
- [ ] メールサーバーの管理者連絡先（DNS移行時に必要）

**自分で準備:**

- [ ] Cloudflareアカウント（サインアップ済み）
- [ ] GitHubリポジトリのアクセス権限

---

## 会議アジェンダ（90分）

### Part 1: デモ（20分）

#### 1. ローカル環境でフォーム機能をデモ

**お問い合わせフォームのデモ:**

1. http://localhost:8788/index.html を開く
2. 「お問い合わせ」ボタンをクリック
3. **必須フィールド未入力エラーのデモ:**
   - 会社名を空欄で送信 → エラーメッセージ表示
4. **メールアドレス形式エラーのデモ:**
   - メールアドレスに「test」と入力 → エラーメッセージ表示
5. **正常送信のデモ:**
   - すべてのフィールドを正しく入力
   - Turnstile検証（チェックボックスをクリック）
   - 送信ボタンをクリック → 成功メッセージ表示

**採用応募フォームのデモ:**

1. http://localhost:8788/recruit.html を開く
2. 「採用応募」ボタンをクリック
3. **希望職種の複数選択:**
   - 複数の職種を選択可能なことを示す
4. **正常送信のデモ:**
   - すべてのフィールドを入力して送信 → 成功メッセージ表示

#### 2. スパム対策の説明

**Turnstile（ボット検出）:**

- Cloudflareの最新ボット検出技術
- reCAPTCHAよりも使いやすく、プライバシーに配慮
- ユーザー体験を損なわない（ワンクリックで完了）

**ハニーポット（隠しフィールド）:**

- 人間には見えない隠しフィールド
- ボットは自動的にすべてのフィールドを埋めるため検出可能
- ユーザー体験への影響ゼロ

**レート制限（DoS攻撃対策）:**

- 同一IPアドレスから5分間に3回までの送信制限
- Workers KVで送信回数を記録
- 制限超過時は429エラーを返す

#### 3. プライバシーポリシーページの確認

1. http://localhost:8788/privacy-policy.html を開く
2. 内容を一緒に確認
3. 修正が必要な箇所があればメモ

---

### Part 2: DNS設定方式の説明と決定（20分）

#### 1. 方式Aの説明（DNSをCloudflareに移行）

**メリット:**

- ✅ 完全無料（MailChannels APIが無料で使える）
- ✅ Cloudflare CDNで高速化（世界275都市以上のデータセンター）
- ✅ DDoS攻撃保護（無料プランでも利用可能）
- ✅ SSL証明書自動更新（Let's Encrypt）
- ✅ DNS管理が一箇所に集約（管理が楽）

**デメリット:**

- ⚠ MXレコードのコピーが必要（ミスするとメール停止）
- ⚠ DNS反映待ち（1〜2時間、最大48時間）
- ⚠ お名前.comのDNS設定画面は使えなくなる（CloudflareのDNS設定画面を使用）

**リスク:**

- 🔴 MXレコード設定ミスでメール停止の可能性（中リスク）
  - **対策:** 現在のMXレコードを正確にコピー、テスト送信で確認
  - **リカバリー:** お名前.comのネームサーバーに戻せば30分〜2時間で復旧

**推奨度:** ⭐⭐⭐⭐⭐（長期的なメリット大）

#### 2. 方式Bの説明（お名前.comのDNSを継続）

**メリット:**

- ✅ メール設定を触らない（リスクゼロ）
- ✅ 既存のDNS設定をそのまま使用
- ✅ お名前.comの管理画面で引き続き操作可能

**デメリット:**

- ⚠ メール送信API（Resend）が必要
  - 月3,000通まで無料
  - 超過時：$20/月〜（約3,000円/月）
- ⚠ Cloudflare CDNの恩恵を受けられない
- ⚠ 2箇所のサービス管理が必要（お名前.com + Cloudflare）

**リスク:**

- 🟢 極低リスク（既存のメール設定を触らない）

**推奨度:** ⭐⭐⭐☆☆（すぐに運用開始したい場合）

#### 3. クライアントの意思決定

**質問リスト:**

1. **メール送信量はどのくらいですか？**
   - 月3,000通以下 → 方式Bでも無料
   - 月3,000通以上 → 方式Aが完全無料でお得

2. **DNS移行のリスクは許容できますか？**
   - MXレコードを正確にコピーすれば問題なし
   - 万が一メールが停止しても30分〜2時間で復旧可能

3. **いつまでにフォーム機能を運用開始したいですか？**
   - すぐに開始したい → 方式B（設定が簡単）
   - 1週間以内でOK → 方式A（長期的にメリット大）

4. **現在のメールサーバーの管理者は誰ですか？**
   - 社内管理 → MXレコード確認が容易
   - 外部業者 → 業者に確認が必要（方式Bも検討）

**推奨:**

- デフォルトで方式Aを推奨
- リスクを理解した上で、クライアントが最終決定

#### 4. 選択理由の確認

**決定事項をメモ:**

- [ ] 選択した方式: 方式A / 方式B
- [ ] 選択理由: ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿
- [ ] デプロイ予定日: ＿＿＿＿年＿＿月＿＿日
- [ ] 作業担当者: ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿

---

### Part 3: デプロイ作業（40分）

#### 方式Aの場合：DNSをCloudflareに移行

**チェックリスト:**

1. **準備（5分）**
   - [ ] Cloudflareアカウント作成（クライアント）
   - [ ] お名前.comの管理画面にログイン（クライアント）

2. **現在のDNS設定を確認（5分）**
   - [ ] お名前.comのMXレコード確認（開発者がサポート）
   - [ ] スクリーンショットを保存
   - [ ] メモ帳にMXレコードをコピー

3. **Cloudflareにサイト追加（5分）**
   - [ ] Cloudflareダッシュボード → Websites → Add a site
   - [ ] ドメイン入力: `doujimafront.com`
   - [ ] プラン選択: Free（無料）

4. **GitHubリポジトリ連携（5分）**
   - [ ] Cloudflareダッシュボード → Workers & Pages → Create application
   - [ ] GitHub認証 → doujimaリポジトリ選択
   - [ ] プロジェクト設定: ビルドコマンド空欄、出力ディレクトリ `/`

5. **DNSレコードコピー（10分）**
   - [ ] MXレコードをCloudflareに追加（最重要）
   - [ ] SPFレコードをCloudflareに追加
   - [ ] Aレコード追加: `@` → `doujima.pages.dev`（CNAME）
   - [ ] WWWレコード追加: `www` → `doujimafront.com`（CNAME）

6. **Turnstile設定（5分）**
   - [ ] Cloudflareダッシュボード → Turnstile → Add site
   - [ ] サイト名: 堂島フロント企画フォーム
   - [ ] ドメイン: `doujimafront.com`, `doujima.pages.dev`
   - [ ] サイトキーとシークレットキーを取得

7. **環境変数設定（5分）**
   - [ ] `RECIPIENT_EMAIL`: `info@doujimafront.com`
   - [ ] `FROM_EMAIL`: `noreply@doujimafront.com`
   - [ ] `TURNSTILE_SECRET_KEY`: （Turnstileから取得）

8. **Workers KV作成・設定（5分）**
   - [ ] Workers & Pages → KV → Create a namespace
   - [ ] Namespace Name: `RATE_LIMIT`
   - [ ] Binding追加: Variable name `RATE_LIMIT`

9. **お名前.comでネームサーバー変更（5分）**
   - [ ] お名前.com Navi → ドメイン設定 → ネームサーバーの設定
   - [ ] `doujimafront.com` を選択
   - [ ] 他のネームサーバーを利用 → Cloudflareのネームサーバーを入力
     - `ns1.cloudflare.com`
     - `ns2.cloudflare.com`
   - [ ] 確認画面へ進む → 設定する

10. **DNS反映を待つ（1〜2時間後）**
    - [ ] Cloudflareダッシュボードでステータス確認
    - [ ] ステータスが "Active" になったら完了

#### 方式Bの場合：お名前.comのDNSを継続

**チェックリスト:**

1. **準備（5分）**
   - [ ] Cloudflareアカウント作成（クライアント）
   - [ ] Resendアカウント作成（開発者）

2. **GitHubリポジトリ連携（5分）**
   - [ ] Cloudflareダッシュボード → Workers & Pages → Create application
   - [ ] GitHub認証 → doujimaリポジトリ選択
   - [ ] プロジェクト設定: ビルドコマンド空欄、出力ディレクトリ `/`

3. **Cloudflare PagesにデプロイComplete（5分）**
   - [ ] 初回デプロイ完了を確認
   - [ ] Cloudflare Pages URL（`doujima.pages.dev`）を確認

4. **お名前.comでCNAMEレコード追加（10分）**
   - [ ] お名前.com Navi → ドメイン設定 → DNS設定/転送設定
   - [ ] `doujimafront.com` を選択
   - [ ] CNAMEレコード追加:
     - ホスト名: `www`
     - VALUE: `doujima.pages.dev`
     - TTL: `3600`

5. **Resendでドメイン追加（10分）**
   - [ ] Resendダッシュボード → Domains → Add Domain
   - [ ] ドメイン入力: `doujimafront.com`
   - [ ] DNSレコード（SPF、DKIM）をお名前.comに追加
   - [ ] ドメイン検証完了を待つ（5〜10分）

6. **Resend APIキー取得（5分）**
   - [ ] Resendダッシュボード → API Keys → Create API Key
   - [ ] Name: `doujima-production`
   - [ ] Permission: `Sending access`
   - [ ] APIキーをコピー

7. **Cloudflare Pagesの環境変数設定（5分）**
   - [ ] `RECIPIENT_EMAIL`: `info@doujimafront.com`
   - [ ] `FROM_EMAIL`: `noreply@doujimafront.com`
   - [ ] `RESEND_API_KEY`: （Resendから取得）
   - [ ] `TURNSTILE_SECRET_KEY`: （Turnstileから取得）

8. **Turnstile設定（5分）**
   - [ ] Cloudflareダッシュボード → Turnstile → Add site
   - [ ] サイト名: 堂島フロント企画フォーム
   - [ ] ドメイン: `doujimafront.com`, `doujima.pages.dev`
   - [ ] サイトキーとシークレットキーを取得

9. **Workers KV作成・設定（5分）**
   - [ ] Workers & Pages → KV → Create a namespace
   - [ ] Namespace Name: `RATE_LIMIT`
   - [ ] Binding追加: Variable name `RATE_LIMIT`

10. **コード修正とデプロイ（5分）**
    - [ ] `functions/submit-contact.js` でMailChannels → Resend APIに変更
    - [ ] `functions/submit-recruit.js` でMailChannels → Resend APIに変更
    - [ ] GitHubにプッシュして再デプロイ

---

### Part 4: テストと確認（10分）

#### DNS反映確認（方式Aの場合）

**コマンドラインで確認:**

```bash
nslookup doujimafront.com
```

**期待される結果:**

```
doujimafront.com    A    172.67.xxx.xxx
```

Cloudflare の IP アドレスが返ってくれば成功。

#### フォーム送信テスト

1. **お問い合わせフォームのテスト:**
   - [ ] https://doujimafront.com/index.html にアクセス
   - [ ] お問い合わせフォームから実際に送信
   - [ ] 成功メッセージが表示される
   - [ ] 受信先メールアドレスでメール受信を確認

2. **採用応募フォームのテスト:**
   - [ ] https://doujimafront.com/recruit.html にアクセス
   - [ ] 採用応募フォームから実際に送信
   - [ ] 成功メッセージが表示される
   - [ ] 受信先メールアドレスでメール受信を確認

#### メール受信確認

**確認項目:**

- [ ] メール件名が正しいか
- [ ] メール本文が正しくフォーマットされているか
- [ ] 日本語が文字化けしていないか
- [ ] 送信元アドレスが `noreply@doujimafront.com` になっているか

#### スマートフォンでの表示確認

**デバイス確認:**

- [ ] iPhone（Safari）
- [ ] Android（Chrome）

**確認項目:**

- [ ] フォームが正常に表示される
- [ ] 入力フィールドが使いやすい
- [ ] Turnstileウィジェットが表示される
- [ ] 送信ボタンが押しやすい

---

## 会議後のフォローアップ

### DNS反映待ち（方式Aの場合：1〜2時間後）

**作業内容:**

1. **DNS反映を定期的に確認:**

   ```bash
   nslookup doujimafront.com
   ```

2. **Cloudflareダッシュボードでステータス確認:**

   - ステータスが "Active" になったら次のステップへ

3. **クライアントにメール送信:**

   ```
   件名: 【堂島フロント企画】DNS反映完了のお知らせ

   お疲れ様です。

   DNS反映が完了しましたので、以下のURLでフォーム機能をご確認ください。

   - トップページ: https://doujimafront.com/index.html
   - 採用ページ: https://doujimafront.com/recruit.html

   お問い合わせフォームと採用応募フォームからテスト送信を行い、
   メール受信を確認してください。

   問題がなければ、本番環境での運用を開始できます。

   よろしくお願いいたします。
   ```

### 本番環境での最終テスト

**テストシナリオ:**

1. **お問い合わせフォーム:**
   - [ ] 必須フィールド未入力エラー
   - [ ] メールアドレス形式エラー
   - [ ] Turnstile検証
   - [ ] 送信成功
   - [ ] メール受信確認

2. **採用応募フォーム:**
   - [ ] 必須フィールド未入力エラー
   - [ ] 希望職種の複数選択
   - [ ] 送信成功
   - [ ] メール受信確認

3. **レート制限テスト:**
   - [ ] 5分間に3回送信 → 成功
   - [ ] 4回目の送信 → 429エラー

4. **スパム対策テスト:**
   - [ ] Turnstile未チェックで送信 → エラー
   - [ ] ハニーポット検出（JavaScriptで隠しフィールドに入力） → エラー

### クライアントへの完了報告

**報告メールテンプレート:**

```
件名: 【堂島フロント企画】フォーム機能デプロイ完了報告

お疲れ様です。

堂島フロント企画のフォーム機能デプロイが完了しましたので、ご報告いたします。

■ デプロイ完了日時
2025年XX月XX日 XX:XX

■ 公開URL
- トップページ: https://doujimafront.com/index.html
- 採用ページ: https://doujimafront.com/recruit.html
- プライバシーポリシー: https://doujimafront.com/privacy-policy.html

■ 実装機能
- お問い合わせフォーム
- 採用応募フォーム
- スパム対策（Turnstile、ハニーポット、レート制限）
- プライバシーポリシーページ

■ 受信先メールアドレス
info@doujimafront.com

■ メール送信方式
【方式A】MailChannels API（無料）
【方式B】Resend API（月3,000通まで無料）

■ テスト結果
- お問い合わせフォーム送信: ✅ 正常
- 採用応募フォーム送信: ✅ 正常
- メール受信: ✅ 正常
- スパム対策: ✅ 正常
- レート制限: ✅ 正常

■ 今後の対応
- 操作マニュアルの作成（次回）
- 問い合わせ内容の管理方法の検討（次回）

ご不明点がございましたら、お気軽にお問い合わせください。

よろしくお願いいたします。
```

### 操作マニュアル提供（次回作成）

**作成予定のマニュアル:**

- フォーム送信データの管理方法
- メール受信設定の確認方法
- トラブル発生時の対応フロー
- Cloudflareダッシュボードの使い方

---

## 想定Q&A

### Q1: DNS移行でメールが使えなくなりませんか？

**A:**

いいえ、MXレコードを正確にコピーすれば100%維持されます。

**理由:**

- DNSのネームサーバーを変更しても、MXレコード（メールサーバーの設定）は引き継がれます
- お名前.comで設定していたMXレコードをCloudflareに正確にコピーすることで、メールサーバーへの接続情報は変わりません
- メールサーバー自体は変更しないため、受信・送信ともに継続されます

**リスク対策:**

- MXレコードのコピー前にスクリーンショットを保存
- DNS反映後、すぐにテストメール送信
- 問題があればお名前.comのネームサーバーに戻す（30分〜2時間で復旧）

---

### Q2: 費用はかかりますか？

**A:**

**方式A（DNSをCloudflareに移行）:** 完全無料

- Cloudflare Pages: 無料
- MailChannels API: 無料（Cloudflare Pages専用）
- Workers KV: 無料枠で十分（月間100,000回の読み取り/書き込み）
- Cloudflare Turnstile: 無料
- お名前.comのドメイン更新費用: 継続（DNS移行しても変わりません）

**方式B（お名前.comのDNSを継続）:** 月3,000通まで無料

- Cloudflare Pages: 無料
- Resend API: 月3,000通まで無料、超過時$20/月〜（約3,000円/月）
- Workers KV: 無料枠で十分
- Cloudflare Turnstile: 無料

**結論:**

- 方式Aは長期的に完全無料
- 方式Bは月間メール送信量が3,000通を超えると有料

---

### Q3: 元に戻せますか？

**A:**

はい、お名前.comのネームサーバーに戻すだけです（5分で設定完了、反映は30分〜2時間）。

**手順:**

1. お名前.com Naviにログイン
2. ドメイン設定 → ネームサーバーの設定
3. `doujimafront.com` を選択
4. **お名前.comのネームサーバーを利用** を選択
5. 確認画面へ進む → 設定する

**反映時間:**

- 通常: 30分〜2時間
- 最大: 24時間（まれ）

**注意点:**

- Cloudflareで追加したDNSレコード（Aレコード、CNAMEレコード等）は失われます
- お名前.comで再度設定する必要があります
- MXレコード（メールサーバー設定）は元に戻ります

---

### Q4: フォーム送信データはどこに保存されますか？

**A:**

現在の実装では、フォーム送信データはメールで送信されるのみで、データベースには保存されません。

**理由:**

- シンプルな実装でコストを抑えるため
- メールで受信したデータは、メールクライアント（Outlook、Gmail等）で管理できます

**将来的な拡張（オプション）:**

- Cloudflare D1（SQLiteデータベース）に保存
- Google Sheetsに自動保存
- Airtableに自動保存

**推奨:**

- 当面はメールでの管理で十分
- 月間100件以上の問い合わせが来るようになったらデータベース導入を検討

---

### Q5: Turnstileを設定しないとどうなりますか？

**A:**

Turnstileを設定しない場合、フォーム送信時にエラーが発生します。

**理由:**

- `functions/submit-contact.js` と `functions/submit-recruit.js` でTurnstile検証が必須になっています
- Turnstileトークンがない場合、400エラー（「セキュリティ検証が完了していません」）が返されます

**対応方法:**

1. **推奨:** Turnstileを設定する（無料、5分で完了）
2. **一時的な回避策:** コードからTurnstile検証を削除する（セキュリティリスクあり、非推奨）

**Turnstile設定のメリット:**

- スパムボット対策
- ブルートフォース攻撃対策
- ユーザー体験を損なわない（reCAPTCHAよりも使いやすい）

---

### Q6: レート制限を変更できますか？

**A:**

はい、`functions/submit-contact.js` と `functions/submit-recruit.js` のコードを修正することで変更できます。

**現在の設定:**

- 5分間に3回まで送信可能
- 超過時は429エラー（「送信回数が制限を超えました」）

**変更方法:**

**ファイル:** `functions/submit-contact.js` と `functions/submit-recruit.js`

**該当箇所:**

```javascript
const maxAttempts = 3;  // ここを変更（例: 5回に変更）
const windowSeconds = 300;  // 5分（例: 600秒=10分に変更）
```

**変更例:**

- 10分間に5回まで: `maxAttempts = 5`, `windowSeconds = 600`
- 1時間に10回まで: `maxAttempts = 10`, `windowSeconds = 3600`

**変更後の手順:**

1. コードを修正
2. GitHubにプッシュ
3. Cloudflare Pagesが自動的に再デプロイ

---

### Q7: メールの送信元アドレスを変更できますか？

**A:**

はい、Cloudflare Pagesの環境変数 `FROM_EMAIL` を変更することで可能です。

**手順:**

1. Cloudflareダッシュボード → **Workers & Pages** → **doujima**
2. **Settings** → **Environment variables**
3. `FROM_EMAIL` の値を変更（例: `contact@doujimafront.com`）
4. **Save** をクリック
5. **Deployments** → **Redeploy** で再デプロイ

**注意点:**

- 送信元アドレスのドメインは、デプロイドメインと一致している必要があります
  - OK: `noreply@doujimafront.com`
  - NG: `noreply@gmail.com`（外部ドメインは不可）

---

### Q8: 採用応募フォームに履歴書添付機能を追加できますか？

**A:**

はい、将来的に追加可能です。ただし、追加の実装が必要です。

**実装方法:**

1. **Cloudflare R2（オブジェクトストレージ）を使用:**
   - 月間10GBまで無料
   - 履歴書ファイル（PDF、Word）を保存

2. **フォーム修正:**
   - `<input type="file">` を追加
   - JavaScriptでファイルアップロード処理を実装

3. **Pages Functions修正:**
   - ファイルをR2にアップロード
   - メールにファイルURLを記載

**費用:**

- 月間10GB、100万回のリクエストまで無料
- 超過時: ストレージ$0.015/GB/月、リクエスト$0.36/100万回

**実装時間:**

- 約2〜3時間

---

### Q9: お問い合わせ内容を自動的にSlackに通知できますか？

**A:**

はい、Slack Webhookを使用することで実装可能です。

**実装方法:**

1. **Slack Webhookを作成:**
   - Slack App設定 → Incoming Webhooks → Webhook URLを取得

2. **環境変数に追加:**
   - Cloudflare Pages → Settings → Environment variables
   - `SLACK_WEBHOOK_URL`: （Slack Webhook URL）

3. **Pages Functions修正:**
   - メール送信後、Slack Webhookにリクエストを送信

**通知内容例:**

```
新しいお問い合わせがありました！

会社名: テスト株式会社
ご担当者名: 山田太郎
メールアドレス: test@example.com
サービス: お遍路事業

詳細はメールをご確認ください。
```

**実装時間:**

- 約1時間

---

## 会議終了後のチェックリスト

- [ ] デモが成功した
- [ ] DNS設定方式が決定した（方式A / 方式B）
- [ ] デプロイ作業が完了した（または日程を決定した）
- [ ] テスト送信が成功した
- [ ] メール受信が確認できた
- [ ] クライアントに完了報告メールを送信した
- [ ] 議事録を作成した
- [ ] 次回の打ち合わせ日程を決定した（必要に応じて）

---

## サポート情報

### 公式ドキュメント

- **Cloudflare Pages:** https://developers.cloudflare.com/pages/
- **MailChannels API:** https://mailchannels.zendesk.com/hc/en-us/articles/4565898358413
- **Resend API:** https://resend.com/docs
- **Cloudflare Turnstile:** https://developers.cloudflare.com/turnstile/

### 問題報告

プロジェクト固有の問題は開発チームに連絡してください。
