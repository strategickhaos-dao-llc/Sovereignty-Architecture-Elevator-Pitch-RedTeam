FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .
COPY config.yaml .

# Create non-root user for security
RUN useradd -m -u 1001 coordinator
USER coordinator

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('nats', 4222)); s.close()" || exit 1

CMD ["python", "main.py"]
