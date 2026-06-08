# GitHub Copilot ワークショップ

GitHub Copilot を活用したソフトウェア開発を体験するためのテンプレートリポジトリです。

ワークショップ参加者は、このテンプレートリポジトリを **自分の個人 GitHub アカウント** に複製して使用します。リポジトリには、GitHub Copilot のカスタム指示・エージェント・プロンプト・MCP サーバー設定があらかじめ含まれています。

## 前提条件

| ツール | 備考 |
|--------|------|
| [Visual Studio Code](https://code.visualstudio.com/) | 最新版を推奨 |
| [GitHub Copilot 拡張機能](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) | Copilot ライセンスが必要 |
| [Git](https://git-scm.com/) | |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | DevContainer 利用時のみ |

## セットアップ手順

### 1. リポジトリの複製

1. このリポジトリのページで **「Use this template」** → **「Create a new repository」** をクリック
2. Owner を **自分の個人アカウント** に設定し、リポジトリ名を入力して作成
3. 作成したリポジトリをローカルにクローン：

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
code .
```

### 2. VS Code プロキシ設定（Windows 標準 PC 限定）

> **注意:** この設定は社内プロキシ環境下の Windows 標準 PC でのみ必要です。自宅などプロキシが不要な環境では、この手順はスキップしてください。

VS Code のユーザー設定（`settings.json`）に以下を追加してください：

```json
{
  "http.proxy": "http://ユーザー名:パスワード@社内プロキシサーバー:ポート番号",
  "http.proxyStrictSSL": false,
  "http.proxyAuthorization": null
}
```

- `ユーザー名`、`パスワード`、`社内プロキシサーバー`、`ポート番号` は実際の値に置き換えてください
- この設定により、GitHub Copilot や MCP サーバーとの通信がプロキシ経由で行われます

> **⚠️ セキュリティ注意事項 — VS Code 設定同期（Settings Sync）からの除外**
>
> `settings.json` にユーザー名・パスワードを含むプロキシURLを記載した場合、**VS Code の Settings Sync を有効にしていると GitHub アカウント経由でクラウドに同期されてしまいます。** 資格情報の漏えいを防ぐために、以下のいずれかの対策を実施してください。
>
> **方法1: 設定同期の対象から `settings.json` を除外する**
>
> 1. VS Code でコマンドパレット（`Ctrl+Shift+P`）を開く
> 2. **「Settings Sync: Configure」** を実行
> 3. **「Settings」** のチェックを **外す**（または同期対象から除外する）
>
> **方法2: プロキシ設定を環境変数で行う（推奨）**
>
> `settings.json` への直接記載を避け、OS レベルの環境変数としてプロキシを設定する方法です。
> Windows の場合、システムのプロパティ → 環境変数から以下を設定してください：
>
> ```
> HTTP_PROXY=http://ユーザー名:パスワード@社内プロキシサーバー:ポート番号
> HTTPS_PROXY=http://ユーザー名:パスワード@社内プロキシサーバー:ポート番号
> ```
>
> VS Code はこれらの環境変数を自動的に参照するため、`settings.json` への記載は不要になります。
>
> **方法3: ユーザー設定同期の除外キーを指定する**
>
> `settings.json` の同期は続けたいが特定のキーを除外したい場合、`settingsSync.ignoredSettings` に追加してください：
>
> ```json
> {
>   "settingsSync.ignoredSettings": ["http.proxy"]
> }
> ```

### 3. DevContainer での開発（オプション）

Docker Desktop がインストールされている場合、DevContainer を利用して統一された開発環境を構築できます。

1. VS Code でリポジトリを開く
2. コマンドパレット（`Ctrl+Shift+P`）→ **「Dev Containers: Reopen in Container」** を実行
3. Python 3.12 + Node.js 18+ の開発環境が自動的に構築されます

DevContainer には以下の VS Code 拡張機能が自動インストールされます：

- Python / Pylance
- ESLint / Prettier
- REST Client
- GitHub Copilot / GitHub Pull Requests
- Azure GitHub Copilot
- Markdown Mermaid

## リポジトリ構成

```
.
├── .devcontainer/          # DevContainer 設定（Python 3.12 + Node.js 18+）
│   ├── Dockerfile
│   └── devcontainer.json
├── .github/
│   ├── copilot-instructions.md   # Copilot 全体指示（日本語対応）
│   ├── agents/                   # カスタム Copilot エージェント
│   ├── instructions/             # コーディング規約・ワークフロー定義
│   └── prompts/                  # 再利用可能なプロンプト
├── .vscode/
│   ├── mcp.json                  # MCP サーバー設定
│   └── settings.json             # VS Code 設定（コミットメッセージ日本語化）
└── docs/                         # ドキュメント・サンプル資料
```

## GitHub Copilot カスタマイズ

このリポジトリには、GitHub Copilot の動作をカスタマイズする以下の設定が含まれています。

### カスタム指示（Instructions）

Copilot が生成するコードのスタイルや品質基準を定義します。

| ファイル | 対象 | 概要 |
|----------|------|------|
| [python.instructions.md](.github/instructions/python.instructions.md) | `**/*.py` | PEP 8 準拠、型ヒント必須、docstring 規約 |
| [reactjs.instructions.md](.github/instructions/reactjs.instructions.md) | `**/*.jsx, **/*.tsx, **/*.js, **/*.ts, **/*.css, **/*.scss` | React 19+ / TypeScript / アクセシビリティ / パフォーマンス最適化 |
| [spec-driven-workflow-v1.instructions.md](.github/instructions/spec-driven-workflow-v1.instructions.md) | `**` | 仕様駆動開発ワークフロー（分析→設計→実装→検証→振り返り→引き渡しの 6 フェーズ） |

### カスタムエージェント（Agents）

特定の専門領域に特化した Copilot エージェントモードです。

| ファイル | 概要 |
|----------|------|
| [expert-react-frontend-engineer.agent.md](.github/agents/expert-react-frontend-engineer.agent.md) | React / TypeScript / UX / パフォーマンス / アクセシビリティに精通したフロントエンドエンジニア |

### 再利用可能プロンプト（Prompts）

よく使う操作をワンクリックで実行できるプロンプトテンプレートです。

| ファイル | 概要 |
|----------|------|
| [comment-code-generate-a-tutorial.prompt.md](.github/prompts/comment-code-generate-a-tutorial.prompt.md) | コードに日本語コメントを追加し、初心者向けチュートリアルを生成 |
| [create-implementation-plan.prompt.md](.github/prompts/create-implementation-plan.prompt.md) | AI 最適化された実装計画を自動生成 |
| [plan-dailyReportApp.prompt.md](.github/prompts/plan-dailyReportApp.prompt.md) | Azure MCPを活用して日報アプリMVPの仕様駆動実装計画を作成 |
| [create-github-issues-feature-from-implementation-plan.prompt.md](.github/prompts/create-github-issues-feature-from-implementation-plan.prompt.md) | 実装計画から GitHub Issue を自動作成 |

## MCP サーバー設定

[.vscode/mcp.json](.vscode/mcp.json) に以下の MCP（Model Context Protocol）サーバーが事前設定されています：

| サーバー | URL | 用途 |
|----------|-----|------|
| GitHub | `https://api.githubcopilot.com/mcp/` | GitHub リポジトリ操作（Issue 作成、PR 管理など） |
| Microsoft Docs | `https://learn.microsoft.com/api/mcp` | Microsoft 公式ドキュメントの検索・参照 |

> **注意:** MCP サーバーを利用するには、プロキシ環境下では前述のプロキシ設定が必要です。

## サンプルドキュメント

ワークショップの演習で使用するサンプル資料が含まれています。

| ファイル | 概要 |
|----------|------|
| [docs/daily-report-app-meeting.md](docs/daily-report-app-meeting.md) | 日報アプリ開発の会議議事録サンプル |
