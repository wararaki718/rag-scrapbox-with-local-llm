# Use a Python image with uv installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --no-dev: Skip development dependencies
# --frozen: Use the exact versions from uv.lock
# --no-cache: Keep the image small
RUN uv sync --frozen --no-dev --no-cache

# Copy the application code
COPY batch /app/batch
COPY README.md /app/README.md

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application (batch processing)
CMD ["uv", "run", "python", "-m", "batch.main"]
