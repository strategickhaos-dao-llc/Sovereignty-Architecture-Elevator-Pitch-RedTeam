# Code-to-Diagram Translator
# IDEA_002 - StrategicKhaos DAO LLC

FROM python:3.11-slim

LABEL maintainer="StrategicKhaos DAO LLC"
LABEL idea_id="IDEA_002"
LABEL service_name="svc-code-diagram"
LABEL department="infra_cloud"
LABEL description="Tool that generates living architecture diagrams from source code"

# Set working directory
WORKDIR /app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV IDEA_ID=IDEA_002
ENV RUN_MODE=prototype
ENV OUTPUT_FORMAT=mermaid

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Expose port for potential web interface
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
