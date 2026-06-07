---
agent: 'agent'
description: 'feature_request.ymlまたはchore_request.ymlテンプレートを使用して、実装計画からGitHub Issueを作成する。'
tools:[agent, 'microsoftdocs/mcp/*', github/add_issue_comment, github/issue_read, github/issue_write, github/list_issues, github/search_issues, github/sub_issue_write, github.vscode-pull-request-github/issue_fetch, github.vscode-pull-request-github/suggest-fix, github.vscode-pull-request-github/renderIssues]
---
# 実装計画からGitHub Issueを作成

`${file}`の実装計画からGitHub Issueを作成します。

## プロセス

1. 計画ファイルを分析してフェーズを特定
2. `search_issues`を使用して既存のissueを確認
3. フェーズごとに`create_issue`を使用して新しいissueを作成するか、`update_issue`で既存のものを更新
4. `feature_request.yml`または`chore_request.yml`テンプレートを使用（代替としてデフォルト）

## 要件

- 実装フェーズごとに1つのissue
- 明確で構造化されたタイトルと説明
- 計画で必要とされる変更のみを含める
- 作成前に既存のissueと照合して確認

## Issueの内容

- タイトル: 実装計画のフェーズ名（日本語）
- 説明: フェーズの詳細、要件、およびコンテキスト（日本語）
- ラベル: issueタイプに適したもの（feature/chore）
- すべてのissueコンテンツに日本語を使用
