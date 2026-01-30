# rag-scrapbox-with-local-llm

Scrapbox のデータを RAG (Retrieval-Augmented Generation) で利用するためのプロジェクトです。

## 構成

- `elasticsearch`: 検索エンジン。SPLADE によるベクトル検索をサポートします。
- `splade-encoder-api`: テキストを SPLADE ベクトルに変換する API。
- `gemma-api`: Gemma 3 4B によるローカル LLM 推論を行う API (OpenAI 互換)。
- `search-api`: 検索および回答生成を行う Web API。
- `web-ui`: ユーザーフレンドリーな検索インターフェースを提供する React (Vite) アプリケーション。
- `ingestion-batch`: Scrapbox のデータを Elasticsearch に取り込むバッチ。

## 実行方法

### 準備

1. `.env` ファイルを作成し、必要に応じて設定を行います。
   ```text
   # デフォルトの設定で動作します
   ```

### サービスの起動

プロジェクト直下にある `compose.yml` を使用して、必要なサービスを一括で起動できます。

```bash
docker compose up -d
```

起動後、以下のポートで各サービスにアクセス可能です。

- Elasticsearch: [http://localhost:9200](http://localhost:9200)
- Kibana: [http://localhost:5601](http://localhost:5601)
- SPLADE Encoder API: [http://localhost:8000](http://localhost:8000)
- Search API: [http://localhost:8001](http://localhost:8001)
- Web UI: [http://localhost:3000](http://localhost:3000)

### 動作確認

`search-api` に対して以下のコマンドで質問を送ることができます。

```bash
curl -X POST "http://localhost:8001/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "Scrapboxの特徴を教えて"}'
```
