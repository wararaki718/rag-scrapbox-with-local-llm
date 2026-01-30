# Ingestion Batch

Scrapbox のページデータを取得し、SPLADE を用いてスパースベクトル化を行った後、Elasticsearch に格納するためのバッチプログラムです。

## 概要

`architecture.md` の「1. データ蓄積フェーズ（バッチ処理）」を実装しています。

1. **Scrapbox API からデータ取得**: 指定されたプロジェクトの全ページを取得します。
2. **テキスト分割 (Chunking)**: ページ内容を適切なサイズ（デフォルト500文字）に分割します。
3. **SPLADE ベクトル化**: [splade-encoder-api](../splade-encoder-api/) を呼び出し、テキストをスパースベクトルに変換します。
4. **Elasticsearch 登録**: テキスト、メタデータ、ベクトルを `rank_features` 形式で登録します。

## セットアップ

### 1. 依存関係のインストール

Python 3.11 以上が必要です。`uv` を使用してインストールします。

```bash
cd ingestion-batch
uv sync
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、必要な情報を入力してください。

```bash
cp .env.example .env
```

| 変数名 | 説明 | デフォルト |
| :--- | :--- | :--- |
| `SCRAPBOX_PROJECT` | Scrapbox のプロジェクト名 | (必須) |
| `SCRAPBOX_SID` | 非公開プロジェクトの場合の `connect.sid` クッキー | (任意) |
| `ELASTICSEARCH_URL` | Elasticsearch のエンドポイント | `http://localhost:9200` |
| `ELASTICSEARCH_INDEX` | 作成するインデックス名 | `scrapbox-pages` |
| `SPLADE_API_URL` | SPLADE Encoder API のエンドポイント | `http://localhost:8000/encode` |
| `CHUNK_SIZE` | 1チャンクの最大文字数 | `500` |
| `CHUNK_OVERLAP` | チャンク間の重複文字数 | `50` |

## 実行方法

1. **前提条件**:
   - [Elasticsearch](../elasticsearch/docker-compose.yml) が起動していること。
   - [splade-encoder-api](../splade-encoder-api/) が `8000` ポート等で起動していること。

2. **バッチ実行**:

```bash
uv run python -m batch.main
```

格納されたデータのチェック

```bash
curl -X GET "http://localhost:9200/scrapbox-pages/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": { "match_all": {} },
  "size": 5
}'
```

## 開発

### テストの実行

```bash
uv run pytest
```

### Linter (ruff) の実行

```bash
# チェックのみ
uv run ruff check .

# 自動修正
uv run ruff check . --fix
```

## インデックス構成

Elasticsearch には以下のマッピングでデータが作成されます。

- `title`: ページタイトル (kuromoji)
- `text`: 分割されたテキスト (kuromoji)
- `url`: Scrapbox ページの URL
- `updated`: 最終更新日時
- `sparse_vector`: SPLADE によるスパースベクトル (`rank_features`)
