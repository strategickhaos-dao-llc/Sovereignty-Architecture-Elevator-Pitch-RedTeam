# Dockerfile for Code-to-Diagram Translator (IDEA_002)
# StrategicKhaos DAO LLC / Valoryield Engine

FROM python:3.11-slim

# Labels for container metadata
LABEL org.opencontainers.image.title="Code-to-Diagram Translator"
LABEL org.opencontainers.image.description="Tool that generates architecture diagrams from source code"
LABEL org.opencontainers.image.vendor="StrategicKhaos DAO LLC"
LABEL org.opencontainers.image.source="https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-"

# Environment variables
ENV IDEA_ID=IDEA_002
ENV NAMESPACE=ns-infra
ENV OUTPUT_FORMAT=mermaid
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Set working directory
WORKDIR /app

# Copy application files
COPY main.py /app/
COPY requirements.txt /app/

# Install dependencies (if any)
RUN pip install --no-cache-dir -r requirements.txt || true

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Default entrypoint
ENTRYPOINT ["python", "main.py"]

# Default command (can be overridden)
CMD ["--help"]
