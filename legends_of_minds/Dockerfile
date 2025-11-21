# Legends of Minds - Unified Agent Orchestration Platform
# Production-grade container build

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY core/ ./core/
COPY departments/ ./departments/
COPY web/ ./web/

# Create data directories
RUN mkdir -p /var/legends_of_minds && \
    mkdir -p /var/legends_of_minds/artifacts && \
    mkdir -p /var/legends_of_minds/outputs

# Expose ports
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Set entry point
CMD ["python", "-m", "uvicorn", "core.orchestrator:app", "--host", "0.0.0.0", "--port", "8080"]
