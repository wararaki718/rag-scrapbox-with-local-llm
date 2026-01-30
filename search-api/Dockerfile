# Use a Python image with uv installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-cache

# Copy the application code
COPY api /app/api
COPY README.md /app/README.md

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8001"]
