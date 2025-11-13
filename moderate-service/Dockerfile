FROM python:3.11-slim

WORKDIR /app

# Install system certificates and OpenSSL for MongoDB Atlas SSL/TLS connections
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    openssl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

# Expose port (Render will set PORT environment variable if needed)
EXPOSE 8002

# Use PORT environment variable if set (for Render), otherwise default to 8002
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8002}"
