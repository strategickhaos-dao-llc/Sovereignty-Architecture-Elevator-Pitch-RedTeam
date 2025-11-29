FROM python:3.12-slim

LABEL maintainer="Strategickhaos DAO LLC"
LABEL description="Flask webhook inbox service for GitHub events"

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application code
COPY app.py .

# Create inbox directory (will be mounted as volume)
RUN mkdir -p /inbox

# Set environment variables (override at runtime)
ENV GITHUB_WEBHOOK_SECRET=""
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
