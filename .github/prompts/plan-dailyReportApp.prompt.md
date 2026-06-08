---
agent: 'agent'
description: 'Azure MCPを活用して日報アプリMVPの仕様駆動実装計画を作成する。'
tools: [vscode, execute, read, agent, edit, search, web, 'microsoftdocs/mcp/*', azure-mcp/search, todo]
---

# 日報アプリ実装計画（Azure MCP活用）

`docs/daily-report-app-meeting.md` と `docs/spec/requirements.md` を一次情報源として、日報アプリMVPの実装計画を日本語で作成してください。

## 必須方針

1. 仕様駆動ワークフロー（分析→設計→実装→検証）に従うこと
2. Azure関連の技術判断は **Azure MCP（`azure-mcp/search`）** を使って根拠を確認すること
3. Microsoft公式情報は `microsoftdocs/mcp/*` を優先して参照すること
4. 出力は他のAIエージェントが実行できる粒度で具体化すること

### Azure MCP利用ルール

- `azure-mcp/search` では「対象技術 + 観点」を含む検索クエリを使用すること
- 例:
  - `Azure OpenAI FastAPI 認証方式 managed identity API key ベストプラクティス`
  - `Azure App Service FastAPI スケーリング 設定 推奨`
  - `Azure OpenAI コスト最適化 レート制限 監視`
- 調査結果は「要点」「採用判断」「根拠」に分けて設計へ反映すること

## 作成対象

- `docs/spec/design.md`
- `docs/spec/tasks.md`

## 実行手順

1. 要件確認: `docs/spec/requirements.md` からMVPの必須要件と制約を抽出
2. Azure調査: Azure OpenAI / FastAPI on Azure App Service について、少なくとも以下を Azure MCP で確認
   - 認証方式（API Key / Managed Identity）
   - スケーリングと可用性設計
   - コスト最適化（レート制限、利用量監視）
   - セキュリティベストプラクティス（秘密情報管理、ネットワーク制御）
3. 設計作成: `docs/spec/design.md` にアーキテクチャ、データフロー、エラーハンドリング、テスト戦略を定義
4. タスク分解: `docs/spec/tasks.md` に依存関係付きの実装タスクを作成
5. 検証: 要件IDとのトレーサビリティ（REQ ↔ TASK）を明示して抜け漏れを確認

## 出力要件

- すべて日本語で記載すること
- 要件ID（例: `REQ-F-001`）を参照して追跡可能にすること
- Azure MCPで確認した内容は、設計上の判断理由として明記すること
