## Plan: 日報アプリ MVP 実装計画

議事録で確定している方針を前提に、React フロントエンドと FastAPI バックエンドを新規構築し、Azure OpenAI GPT-4.1 を使ってスクリーンショットから日報を生成する MVP を段階的に実装する。先に `docs/spec/requirements.md`、`docs/spec/design.md`、`docs/spec/tasks.md` を日本語で整備し、要件・設計・タスクを固定してから実装に入る。データベースは使わず、セッションベースの一時保持のみで構成する。

**Steps**
1. フェーズ 1: 要件化とスコープ固定
   - 議事録から EARS 形式の要件を抽出し、`docs/spec/requirements.md` にまとめる。
   - 機能対象を「画像アップロード」「日報生成」「編集/コピー/Markdown 出力」「ローディング/エラー表示」「一時データ削除」に限定し、今回対象外を明記する。
   - 受け入れ基準、エラー条件、非機能要件、ブラウザ制約、セキュリティ前提を確定する。
   - 依存関係として Azure OpenAI、FastAPI、React、DevContainer、Azure App Service を整理する。

2. フェーズ 2: 技術設計
   - `docs/spec/design.md` にアーキテクチャ、データフロー、API 契約、セッション管理、画像前処理方針、エラー処理、テスト方針を記述する。
   - 画像受付から生成までのシーケンス、バックエンドの責務分割、フロントエンドの状態管理と画面遷移を固定する。
   - Azure OpenAI への呼び出し方式、リトライ方針、タイムアウト、入力制限、ログ出力方針を決める。
   - MVP では永続化を使わず、画像と生成結果の保持期限と自動削除を設計に含める。

3. フェーズ 3: 実装計画の分解
   - `docs/spec/tasks.md` に、フロントエンド、バックエンド、共通設定、テスト、デプロイ準備の順で追跡可能なタスクを並べる。
   - 依存関係を明示し、並行実行できる作業と順序依存の作業を分ける。
   - 各タスクに期待結果と検証方法を付ける。

4. フェーズ 4: プロジェクト骨格作成
   - 既存コードがない前提で、React アプリと FastAPI アプリの初期構成を作る。
   - DevContainer 前提で開発環境を統一し、環境変数管理、CORS、API ベース URL、Azure OpenAI 設定を整える。
   - フロントエンドの主要 UI を、ドラッグ&ドロップ、貼り付け、プレビュー、生成結果表示、編集、コピー、Markdown 出力まで含めて実装対象にする。
   - バックエンドの主要 API を、画像受信、入力検証、モデル呼び出し、結果整形、エラー応答まで含めて実装対象にする。

5. フェーズ 5: MVP 機能実装
   - 画像アップロードとプレビュー、ローディング表示、エラー表示、生成結果編集をフロントエンドに実装する。
   - FastAPI で生成 API を実装し、Azure OpenAI GPT-4.1 への接続を行う。
   - 画像前処理、サイズ制限、タイムアウト、失敗時のフォールバックメッセージを実装する。
   - Markdown 形式での出力とクリップボードコピーを実装する。

6. フェーズ 6: 検証とデプロイ準備
   - 単体テスト、統合テスト、主要な画像パターンの手動確認を行う。
   - モダンブラウザでの表示確認と、モバイル対象外の前提が崩れていないことを確認する。
   - Azure App Service へのデプロイ手順、環境変数、ログ、監視の前提を整理する。
   - 生成品質、応答時間、API 制限、コスト上限に関するリスクを明文化する。

**Relevant files**
- `/workspaces/github-copilot-workshop/docs/daily-report-app-meeting.md` — 要件抽出の一次情報源。
- `/workspaces/github-copilot-workshop/docs/spec/requirements.md` — EARS 形式の要件定義を作成する。
- `/workspaces/github-copilot-workshop/docs/spec/design.md` — 技術設計、API 契約、シーケンス、エラーマトリクスをまとめる。
- `/workspaces/github-copilot-workshop/docs/spec/tasks.md` — 実装タスク、依存関係、検証手順を追跡する。
- `/workspaces/github-copilot-workshop/.github/instructions/spec-driven-workflow-v1.instructions.md` — 文書化と実行順序の基準。
- `/workspaces/github-copilot-workshop/.github/instructions/reactjs.instructions.md` — フロントエンド実装時の標準。
- `/workspaces/github-copilot-workshop/.github/instructions/python.instructions.md` — バックエンド実装時の標準。
- `/workspaces/github-copilot-workshop/.devcontainer/devcontainer.json` — 開発環境の前提。

**Verification**
1. `docs/spec/requirements.md` に、EARS 形式の要件が漏れなく記載されていることを確認する。
2. `docs/spec/design.md` に、API 契約、データフロー、エラーハンドリング、テスト方針が含まれていることを確認する。
3. `docs/spec/tasks.md` に、実装順序・依存関係・検証手順が含まれていることを確認する。
4. 実装後は、バックエンドの単体テストとフロントエンドの主要コンポーネントテストを実行する前提で計画する。
5. Azure OpenAI への実接続は、少なくとも 1 回の手動疎通確認を検証項目に含める。

**Decisions**
- 初期構成は React + FastAPI + Azure OpenAI GPT-4.1 + Azure App Service とする。
- 永続 DB は導入せず、セッションベースの一時保持のみとする。
- 日報テンプレートは「作業内容」「進捗状況」「課題・問題点」の 3 セクションで固定する。
- 入力は画像スクリーンショットを前提とし、OCR 専用フローは MVP では採用しない。
- モバイル対応は対象外とし、モダンブラウザのみを対象とする。

**Further Considerations**
1. Azure OpenAI の呼び出し上限とコスト制約が厳しい場合は、生成前の画像圧縮とバッチ制御を先に入れる。
2. 生成結果の編集体験を重視する場合は、Markdown エディタを最小のテキストエリア実装から始めるか、拡張エディタを採用するかを後で分岐できるようにする。
3. 2 週間 MVP のため、最初の実装版は単一画面構成に寄せ、ルーティング追加は後続拡張に回す。