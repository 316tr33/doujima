# 納品前セットアップ手順

**目的:** クライアント訪問前に、GitHub Actions と Cloudflare の連携を完了させる
**所要時間:** 約 20-30 分
**実行場所:** 自宅（開発環境）

---

## 前提条件の確認

### ✅ 必要なもの

- [ ] GitHub アカウント（316tr33）
- [ ] Cloudflare アカウント（開発環境 `d92d129b.doujima.pages.dev` にアクセス可能）
- [ ] インターネット接続
- [ ] このドキュメント（印刷またはタブレットで表示）

---

## Phase 1: Cloudflare 情報の取得（10 分）

### Step 1.1: Cloudflare にログイン

```
1. ブラウザで開く:
   https://dash.cloudflare.com/

2. ログイン情報を入力してログイン
```

**✅ 確認ポイント:** ダッシュボードが表示され、既存のプロジェクト（doujima）が見える

---

### Step 1.2: Account ID の確認とメモ

```
1. ダッシュボード画面を確認
2. 右側のサイドバーに「Account ID」が表示されている
3. 「Click to copy」をクリックしてコピー
```

**📝 ここにメモ（必須）:**

```
CLOUDFLARE_ACCOUNT_ID: 4e09084fbab0ae504a9ee4d0cfc55949
（32文字の英数字）

```

**✅ 確認ポイント:** 32 文字の英数字がコピーされている

---

### Step 1.3: 既存プロジェクト名の確認

```
1. ダッシュボード左メニュー「Workers & Pages」をクリック
2. 既存のプロジェクト一覧を確認
3. doujima関連のプロジェクト名をメモ
```

**📝 ここにメモ（必須）:**

```
既存プロジェクト名: doujima

```

**⚠️ 重要:** この名前を後で使用します

---

### Step 1.4: API Token の作成

```
1. ダッシュボード右上のアイコン（プロフィール画像）をクリック
2. メニューから「My Profile」を選択
3. 左メニュー「API Tokens」をクリック
4. 「Create Token」ボタンをクリック
```

**✅ 確認ポイント:** Token 作成画面が表示される

---

### Step 1.5: Token の設定

```
5. 「Custom token」セクションを探す
6. 「Get started」ボタンをクリック

【設定内容】

Token name:
  GitHub Actions Deploy
  （このままコピー＆ペースト）

Permissions:
  - 「Add」をクリック
  - 1つ目のドロップダウン: Account
  - 2つ目のドロップダウン: Cloudflare Pages
  - 3つ目のドロップダウン: Edit

Account Resources:
  - 1つ目のドロップダウン: Include
  - 2つ目のドロップダウン: All accounts

7. 「Continue to summary」ボタンをクリック
8. 設定内容を確認
9. 「Create Token」ボタンをクリック
```

**✅ 確認ポイント:** Token 作成完了画面が表示される

---

### Step 1.6: Token のコピーとメモ

```
⚠️ 超重要: この画面は二度と表示されません！

1. 表示された長い文字列（Token）を全選択
2. コピー（Cmd+C）
3. 下記にメモ
```

**📝 ここにメモ（必須）:**

```
CLOUDFLARE_API_TOKEN: vFuH7-jJQNZT6wLFcAxKyr4hoFuTtX5ELYswOi6w
```

**✅ 確認ポイント:** Token がコピーされ、メモ完了

```
4. 「View your token」の下の閉じるボタンをクリック
```

---

## Phase 2: GitHub Secrets の登録（5 分）

### Step 2.1: GitHub Secrets 設定画面を開く

```
1. ブラウザで開く:
   https://github.com/316tr33/doujima/settings/secrets/actions

2. GitHubにログイン（必要な場合）
```

**✅ 確認ポイント:** 「Actions secrets and variables」画面が表示される

---

### Step 2.2: API Token を登録

```
1. 「New repository secret」ボタンをクリック

2. 入力:
   Name: CLOUDFLARE_API_TOKEN
   （大文字・アンダースコアに注意）

   Value: [Phase 1.6でメモしたToken]
   （メモから正確にコピー＆ペースト）

3. 「Add secret」ボタンをクリック
```

**✅ 確認ポイント:** Secrets 一覧に「CLOUDFLARE_API_TOKEN」が表示される

---

### Step 2.3: Account ID を登録

```
1. 「New repository secret」ボタンをもう一度クリック

2. 入力:
   Name: CLOUDFLARE_ACCOUNT_ID
   （大文字・アンダースコアに注意）

   Value: [Phase 1.2でメモしたAccount ID]
   （メモから正確にコピー＆ペースト）

3. 「Add secret」ボタンをクリック
```

**✅ 確認ポイント:** Secrets 一覧に 2 つ表示される

- CLOUDFLARE_API_TOKEN
- CLOUDFLARE_ACCOUNT_ID

---

## Phase 3: ワークフローファイルの調整（5 分）

### Step 3.1: プロジェクト名の確認

Phase 1.3 でメモしたプロジェクト名を確認：

```
既存プロジェクト名: ________________________________________
```

---

### Step 3.2: ワークフローファイルのプロジェクト名確認

```
1. ターミナルを開く

2. プロジェクトディレクトリに移動:
   cd /Users/macmiller/Desktop/doujima

3. ワークフローファイルを確認:
   cat .github/workflows/cloudflare-pages.yml
```

**確認箇所:**

```yaml
command: pages deploy . --project-name=doujima
  ^^^^^^^^
  この部分
```

---

### Step 3.3: プロジェクト名の修正（必要な場合のみ）

**Phase 1.3 のプロジェクト名が `doujima` でない場合のみ実行:**

```
1. エディタでファイルを開く:
   code .github/workflows/cloudflare-pages.yml

2. 最終行を修正:
   修正前: command: pages deploy . --project-name=doujima
   修正後: command: pages deploy . --project-name=実際のプロジェクト名

   例: command: pages deploy . --project-name=doujima-pages

3. 保存（Cmd+S）
```

**✅ 確認ポイント:** プロジェクト名が実際の Cloudflare プロジェクト名と一致

---

## Phase 4: Git コミット＆プッシュ（5 分）

### Step 4.1: 現在のブランチを確認

```bash
cd /Users/macmiller/Desktop/doujima
git branch
```

**現在のブランチ:** `* fix/turnstile-debug-logging`

---

### Step 4.2: 変更をステージング

```bash
git add docs/DEPLOYMENT_CHECKLIST.md
git add .github/workflows/cloudflare-pages.yml
```

**✅ 確認ポイント:** エラーが出ない

---

### Step 4.3: ステージング状態を確認

```bash
git status
```

**期待される表示:**

```
Changes to be committed:
  modified:   docs/DEPLOYMENT_CHECKLIST.md
  new file:   .github/workflows/cloudflare-pages.yml
```

**✅ 確認ポイント:** 2 つのファイルが緑色で表示される

---

### Step 4.4: コミット

```bash
git commit -m "feat: Direct Upload方式への移行とGitHub Actions統合

- デプロイ方式をGit IntegrationからDirect Uploadに変更
- GitHub Actionsワークフローファイルを追加
- DEPLOYMENT_CHECKLISTを新方式に全面更新
- クライアントのGitHubアカウント不要に変更

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**✅ 確認ポイント:** コミット成功メッセージが表示される

---

### Step 4.5: プッシュ

```bash
git push origin fix/turnstile-debug-logging
```

**✅ 確認ポイント:** プッシュ成功メッセージが表示される

---

### Step 4.6: main ブランチにマージ

```bash
# mainブランチに切り替え
git checkout main

# リモートの最新状態を取得
git pull origin main

# fix/turnstile-debug-loggingブランチをマージ
git merge fix/turnstile-debug-logging

# mainブランチにプッシュ
git push origin main
```

**✅ 確認ポイント:** main ブランチへのプッシュ成功

---

## Phase 5: GitHub Actions の実行確認（5 分）

### Step 5.1: Actions タブを開く

```
1. ブラウザで開く:
   https://github.com/316tr33/doujima/actions

2. ページを確認
```

**✅ 確認ポイント:** ワークフロー実行の一覧が表示される

---

### Step 5.2: 最新の実行を確認

```
1. 一番上の「Deploy to Cloudflare Pages」をクリック

2. ステータスを確認:
   🟡 黄色の点 → 実行中（1-2分待つ）
   ✅ 緑のチェック → 成功！
   ❌ 赤のバツ → 失敗（次のステップへ）
```

---

### Step 5.3: 成功した場合

```
おめでとうございます！自動デプロイが成功しました。

1. Cloudflareダッシュボードで確認:
   https://dash.cloudflare.com/

2. Workers & Pages → doujima（プロジェクト名）をクリック

3. Deploymentsタブを確認
   → 新しいデプロイが表示される

4. プレビューURLをクリックしてサイト確認
```

**✅ 確認ポイント:** サイトが正常に表示される

**→ Phase 6（最終確認）に進む**

---

### Step 5.4: 失敗した場合

```
1. 失敗したワークフローをクリック

2. 「deploy」ジョブをクリック

3. 「Deploy to Cloudflare Pages」ステップを展開

4. エラーメッセージを確認
```

**よくあるエラーと対処法:**

#### エラー A: "Error: Invalid API Token"

**原因:** API Token が間違っている、または権限不足

**対処:**

```
1. Phase 1.4-1.6 を再実行して新しいTokenを作成
2. 権限が「Account | Cloudflare Pages | Edit」か確認
3. GitHub Secrets を更新:
   https://github.com/316tr33/doujima/settings/secrets/actions
   → CLOUDFLARE_API_TOKEN を削除 → 新しいものを追加
4. 再度プッシュしてワークフロー実行
```

---

#### エラー B: "Error: Project 'doujima' not found"

**原因:** Cloudflare 側のプロジェクト名が `doujima` ではない

**対処:**

```
1. Phase 1.3 で確認した実際のプロジェクト名を確認
2. Phase 3.3 を実行してプロジェクト名を修正
3. 変更をコミット＆プッシュ:
   git add .github/workflows/cloudflare-pages.yml
   git commit -m "fix: Cloudflareプロジェクト名を修正"
   git push origin main
```

---

#### エラー C: "Error: Authentication failed"

**原因:** Account ID が間違っている

**対処:**

```
1. Phase 1.2 を再実行してAccount IDを再確認
2. GitHub Secrets を更新:
   https://github.com/316tr33/doujima/settings/secrets/actions
   → CLOUDFLARE_ACCOUNT_ID を削除 → 正しいものを追加
3. 再度プッシュしてワークフロー実行
```

---

#### エラー D: その他のエラー

**対処:**

```
1. エラーメッセージ全体をコピー
2. Claude Codeに相談
3. または Cloudflare Pagesドキュメントを確認:
   https://developers.cloudflare.com/pages/
```

---

## Phase 6: 最終確認（5 分）

### Step 6.1: デプロイ動作の再確認

```
1. ターミナルで適当な変更を加える:
   cd /Users/macmiller/Desktop/doujima

   # READMEに空行を追加（テスト）
   echo "" >> README.md

   git add README.md
   git commit -m "test: 自動デプロイのテスト"
   git push origin main

2. GitHub Actionsで自動実行を確認:
   https://github.com/316tr33/doujima/actions

3. 1-2分後、Cloudflareで新しいデプロイを確認
```

**✅ 確認ポイント:** 自動デプロイが正常に動作する

---

### Step 6.2: チェックリストの最終確認

納品作業用チェックリストを確認：

```
1. ファイルを開く:
   open docs/DEPLOYMENT_CHECKLIST.md

2. Phase 0「事前準備」を確認:
   すべての項目にチェックが入っているか確認

3. 印刷またはタブレットに転送:
   - 印刷する場合: Cmd+P で印刷
   - タブレットの場合: AirDropまたはクラウド経由で転送
```

**✅ 確認ポイント:** 納品作業用資料の準備完了

---

### Step 6.3: 必要な情報のバックアップ

念のため、重要情報をバックアップ：

```
📝 バックアップメモ（紙またはパスワードマネージャーに保存）

GitHub Repository:
  https://github.com/316tr33/doujima

GitHub Actions:
  https://github.com/316tr33/doujima/actions

GitHub Secrets:
  https://github.com/316tr33/doujima/settings/secrets/actions

Cloudflare Dashboard:
  https://dash.cloudflare.com/

Cloudflare Account ID:
  [Phase 1.2でメモしたID]

Cloudflare Project Name:
  [Phase 1.3でメモしたプロジェクト名]
```

**✅ 確認ポイント:** 情報のバックアップ完了

---

## 完了チェックリスト

すべて完了したか確認：

- [ ] Phase 1: Cloudflare 情報取得完了

  - [ ] Account ID メモ済み
  - [ ] API Token メモ済み
  - [ ] プロジェクト名確認済み

- [ ] Phase 2: GitHub Secrets 登録完了

  - [ ] CLOUDFLARE_API_TOKEN 登録済み
  - [ ] CLOUDFLARE_ACCOUNT_ID 登録済み

- [ ] Phase 3: ワークフローファイル調整完了

  - [ ] プロジェクト名が正しい

- [ ] Phase 4: Git 操作完了

  - [ ] コミット完了
  - [ ] プッシュ完了
  - [ ] main ブランチにマージ完了

- [ ] Phase 5: GitHub Actions 確認完了

  - [ ] ワークフロー実行成功
  - [ ] Cloudflare で新しいデプロイ確認

- [ ] Phase 6: 最終確認完了
  - [ ] 自動デプロイ動作確認
  - [ ] 納品チェックリスト準備完了
  - [ ] バックアップ情報保存完了

---

## 次のステップ

✅ **すべて完了した場合:**

おめでとうございます！納品前の準備が完了しました。

次は「DEPLOYMENT_CHECKLIST.md」を持って、クライアント先での納品作業を進めてください。

---

## トラブルシューティング連絡先

**作業中に問題が発生した場合:**

1. このドキュメントの該当エラー対処法を確認
2. GitHub Actions のログを詳細確認
3. Claude Code に相談（エラーメッセージをコピーして質問）
4. Cloudflare 公式ドキュメント: https://developers.cloudflare.com/pages/

---

**作成日:** 2025 年 11 月 13 日
**バージョン:** 1.0
**対象プロジェクト:** 堂島フロント企画 企業サイト
