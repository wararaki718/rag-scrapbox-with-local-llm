FROM python:3.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 依存関係のインストールをキャッシュするために先にコピー
COPY pyproject.toml uv.lock ./

# システムのPython環境に同期（仮想環境を作らない）
RUN uv sync --frozen --no-dev --no-install-project

COPY api/ ./api/

EXPOSE 11434

# uv run を使用して実行
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "11434"]
