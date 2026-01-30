FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache-dir -r pyproject.toml

COPY api/ ./api/

EXPOSE 11434

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "11434"]
