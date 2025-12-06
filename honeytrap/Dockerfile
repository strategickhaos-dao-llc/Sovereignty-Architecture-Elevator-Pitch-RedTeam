FROM python:3.11-slim

WORKDIR /app

# Copy application code
COPY app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

ENV PORT=8080

CMD ["python", "app.py"]
