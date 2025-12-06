FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY core/ ./core/
COPY ai_legion/ ./ai_legion/
COPY synthesis/ ./synthesis/

# Set Python path
ENV PYTHONPATH=/app

# Default command (override in docker-compose)
CMD ["python", "-m", "core.pr_monitor"]
