# Use a lightweight Python image
FROM python:3.12-slim

# Install uv directly from the official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL (psycopg2/asyncpg)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact versions in uv.lock
RUN uv sync --frozen --no-cache

# Copy the rest of your application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Use 'uv run' to ensure we use the virtual environment created by uv
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]