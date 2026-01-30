# Gemma 3 4B API (Ollama Python Client)

このサービスは、Python の `ollama` ライブラリを使用して LLM 推論を行う FastAPI サーバーです。ホストマシン等で動作している Ollama サーバーと通信して推論を実行します。

## 主な機能

- **Ollama Python SDK**: 公式の `ollama` ライブラリを使用した安定した通信。
- **OpenAI 互換エンドポイント**: `search-api` から利用可能な `/v1/chat/completions` を提供。
- **モダンな開発環境**: `uv` による高速なパッケージ管理と `ruff` による高速な Lint を導入。

## セットアップと起動

### 準備

1. ホストマシンに [Ollama](https://ollama.com/) がインストールされ、実行されている必要があります。
2. 使用するモデルをあらかじめプルしておいてください。

```bash
ollama pull gemma3:4b
```

### 起動方法（Docker）

プロジェクトのルートディレクトリで Docker Compose を使用して起動します。

```bash
docker compose up -d gemma-api
```

### 開発用セットアップ（ローカル）

[uv](https://docs.astral.sh/uv/) がインストールされている場合、以下のコマンドで環境構築と実行が可能です。

```bash
# 依存関係のインストール
uv sync

# API サーバーの起動
uv run uvicorn api.main:app --host 0.0.0.0 --port 11434 --reload
```

## 開発ツール

### Lint の実行

```bash
uv run ruff check .
```

## 環境変数

| 変数名 | 説明 | デフォルト値 |
| :--- | :--- | :--- |
| `MODEL_NAME` | 使用するモデル名 | `gemma3:4b` |
| `OLLAMA_HOST` | Ollama サーバーの URL | `http://host.docker.internal:11434` |

## API の使用例

### チャット・コンプリーション

```bash
curl -X POST "http://localhost:11434/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gemma3:4b",
       "messages": [
         {"role": "user", "content": "こんにちは、自己紹介をしてください。"}
       ]
     }'
```
