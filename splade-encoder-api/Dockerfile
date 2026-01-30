# Use a Python image with uv installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Install system dependencies for MeCab and Japanese processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions in uv.lock
# --no-cache helps keep the image size down
RUN uv sync --frozen --no-cache

# Copy the application code
COPY api /app/api
COPY README.md /app/README.md

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Command to run the application
# We use `uv run` to ensure we are using the environment created by uv sync
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
