# Sovereign Banking Integration - Production Container
# StrategicKhaos DAO LLC & ValorYield Engine
# Board Authorization: Resolution 2025-12-004

FROM python:3.11-slim

# Metadata
LABEL maintainer="StrategicKhaos DAO LLC" \
      description="Sovereign Banking Integration - Automated Charitable Distribution" \
      version="1.0" \
      board_resolution="2025-12-004"

# Security: Run as non-root user
RUN groupadd -r banking && useradd -r -g banking banking

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies with security updates
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip check

# Copy application code
COPY scripts/sovereign_banking.py .

# Create audit log directory with proper permissions
RUN mkdir -p /var/log/sovereign-banking && \
    chown -R banking:banking /var/log/sovereign-banking

# Switch to non-root user
USER banking

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Environment variables (defaults, override via Kubernetes)
ENV PYTHONUNBUFFERED=1 \
    AUDIT_LOG_PATH=/var/log/sovereign-banking/audit.jsonl \
    LOG_LEVEL=INFO

# Run the application
CMD ["python", "sovereign_banking.py"]
