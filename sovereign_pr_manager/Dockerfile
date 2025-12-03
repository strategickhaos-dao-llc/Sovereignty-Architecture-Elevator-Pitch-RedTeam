# SovereignPRManager Dockerfile
# Autonomous PR Orchestration System

FROM python:3.11-slim

LABEL maintainer="StrategicKhaos DAO"
LABEL description="SovereignPRManager - Autonomous PR Review and Merge Orchestration"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Create non-root user
RUN groupadd -r sovereignpr && useradd -r -g sovereignpr sovereignpr

# Create app directory
WORKDIR /app

# Install dependencies
COPY sovereign_pr_manager/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY sovereign_pr_manager/ /app/sovereign_pr_manager/

# Create necessary directories
RUN mkdir -p /app/logs /app/data && \
    chown -R sovereignpr:sovereignpr /app

# Switch to non-root user
USER sovereignpr

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "-m", "sovereign_pr_manager.manager", "--monitor"]
