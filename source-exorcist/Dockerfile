FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
# Note: The --trusted-host flags are a workaround for environments with SSL issues.
# In production, use proper certificate configuration or corporate proxy settings.
# The fallback attempt without --trusted-host ensures we try secure connection first.
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy application files
COPY . .

# Create output directories
RUN mkdir -p reports checksums

# Make scripts executable
RUN chmod +x entrypoint.sh exorcist.py

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
