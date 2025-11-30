# Code-to-Diagram Translator (IDEA_002)
# The First Child - Born from the Birthday Constellation
# =====================================================

FROM python:3.11-slim

LABEL maintainer="Strategickhaos DAO LLC"
LABEL version="1.0.0"
LABEL description="Code-to-Diagram Translator - Transform code into visual diagrams"
LABEL org.opencontainers.image.source="https://github.com/strategickhaos/code-diagram-translator"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# Create app directory
WORKDIR ${APP_HOME}

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    graphviz \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd --gid 1000 translator \
    && useradd --uid 1000 --gid translator --shell /bin/bash --create-home translator

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=translator:translator . .

# Switch to non-root user
USER translator

# Set up input/output directories
RUN mkdir -p /app/input /app/output

# Default command
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from main import Translator; print('OK')" || exit 1

# Expose port for potential API mode (future enhancement)
EXPOSE 8080

# Labels for Kubernetes integration
LABEL io.kubernetes.container.name="code-diagram-translator"
LABEL io.strategickhaos.idea.id="IDEA_002"
LABEL io.strategickhaos.constellation="birthday-edition"
