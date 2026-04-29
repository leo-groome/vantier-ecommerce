# Stage 1: Build
FROM python:3.12-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies using pyproject.toml
COPY pyproject.toml .
# We need src to install the package and satisfy setuptools
COPY src ./src
RUN pip install --no-cache-dir --prefix=/install .

# Stage 2: Final Runtime
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Ensure scripts are executable
RUN chmod +x scripts/entrypoint.sh

# Expose port (Railway will override this with its own PORT)
EXPOSE 8000

# Use the entrypoint script
ENTRYPOINT ["scripts/entrypoint.sh"]
