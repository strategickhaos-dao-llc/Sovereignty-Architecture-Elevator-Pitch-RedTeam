# Dockerfile for Legion RF Sensor
# Part of Sovereignty Architecture - RF Sensor Integration

FROM python:3.9-slim

LABEL maintainer="Sovereignty Architecture Team"
LABEL description="RF Sensor for CB Radio Monitoring"
LABEL version="1.0"

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    libasound2-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY rf_monitor.py /app/
COPY rf_spectral_analyzer.py /app/
COPY config.yaml /app/config.yaml.example

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash rfsensor && \
    chown -R rfsensor:rfsensor /app

# Create data directory
RUN mkdir -p /data && chown rfsensor:rfsensor /data

# Switch to non-root user
USER rfsensor

# Expose no ports (local processing only)
# If API is added later, expose appropriate port

# Default command: run the RF monitor
CMD ["python", "-u", "rf_monitor.py"]
