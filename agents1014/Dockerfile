# Dockerfile for TRS Multi-Agent Chess System
# 100% local, sovereign architecture

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    portaudio19-dev \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent_base.py .
COPY mobius_eval.py .
COPY ollama_orchestrator.py .
COPY voice_interface.py .
COPY websocket_bridge.py .
COPY main.py .

# Create directories
RUN mkdir -p /app/logs /app/models

# Expose WebSocket port
EXPOSE 8765

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=ollama:11434
ENV WEBSOCKET_PORT=8765

# Run the application
CMD ["python", "main.py"]
