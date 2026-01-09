# Use a lightweight Python image
FROM python:3.12-slim

# Install uv directly from the official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL (psycopg2 / asyncpg)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures exact versions from uv.lock
RUN uv sync --frozen --no-cache

# Copy the rest of your application code
COPY . .

# IMPORTANT:
# - Do NOT expose or hardcode ports
# - Render provides $PORT dynamically
CMD ["sh", "-c", "uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
