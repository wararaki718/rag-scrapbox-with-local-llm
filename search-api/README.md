# Search API Server

このサービスは、RAG (Retrieval-Augmented Generation) システムの推論フェーズ（リアルタイム処理）を担う Web API サーバーです。
ユーザーの質問に対し、SPLADE によるスパース検索を用いて Elasticsearch から関連情報を取得し、Gemini 2.0 Flash を使用して回答を生成します。

## 主な機能

- **Query Encoding**: ユーザーの質問を `splade-encoder` を介してスパースベクトルに変換。
- **Sparse Retrieval**: Elasticsearch の `rank_features` を利用した高速かつ意味的な検索。
- **Contextual Generation**: 検索結果をコンテキストとして Gemini 2.0 Flash に渡し、根拠に基づいた回答を生成。
- **Resilient Generation**: `tenacity` による指数バックオフを用いたリトライ処理を実装し、LLM API の一時的なエラーに対する耐性を強化。

## 技術スタック

- **Framework**: FastAPI
- **Search**: Elasticsearch (Async / aiohttp)
- **LLM**: Gemini 2.0 Flash (`google-genai`)
- **Resilience**: Tenacity (Exponential backoff retry)
- **JSON Validation**: Pydantic v2
- **Package Manager**: uv

## セットアップと起動

### 環境変数

以下の環境変数を設定する必要があります（`.env` ファイルまたは Docker Compose 経由）。

| 変数名 | 説明 | デフォルト値 |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Gemini API の API キー | (必須) |
| `ELASTICSEARCH_URL` | Elasticsearch の接続先 URL | `http://localhost:9200` |
| `ELASTICSEARCH_INDEX` | 検索対象のインデックス名 | `scrapbox-pages` |
| `SPLADE_API_URL` | SPLADE Encoder API の URL | `http://localhost:8000/encode` |
| `GEMINI_MODEL_NAME` | 使用する Gemini モデル名 | `gemini-2.0-flash-exp` |
| `GEMINI_CONTEXT_CHUNK_SIZE` | LLM に渡すコンテキストのチャンクサイズ | `3` |
| `GEMINI_RPM_DELAY` | チャンク処理間の待機時間（秒） | `1.0` |

### Docker での起動

プロジェクトのルートディレクトリで Docker Compose を使用して起動します。コンテナ内では高速なパッケージマネージャーである `uv` を使用して環境構築が行われます。

```bash
docker compose up -d search-api
```

### ローカルでの開発

`uv` を使用して仮想環境を構築し、開発環境をセットアップできます。

```bash
# 仮想環境の作成と依存関係のインストール
uv sync

# Linter (Ruff) の実行
uv run ruff check api

# テストの実行
uv run pytest
```

## エンドポイント

### `POST /chat`

ユーザーのクエリに基づいて回答を生成します。

**Request Body:**

```json
{
  "query": "Scrapbox について教えて"
}
```

**Response Body:**

```json
{
  "answer": "Scrapbox は...",
  "sources": [
    {
      "text": "...",
      "title": "タイトル",
      "url": "https://scrapbox.io/...",
      "score": 12.34
    }
  ]
}
```

### `GET /health`

サーバーの稼働状態を確認します。
