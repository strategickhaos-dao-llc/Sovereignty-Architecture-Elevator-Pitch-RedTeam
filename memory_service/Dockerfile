FROM python:3.11-slim

WORKDIR /app
COPY memory_service.py /app/memory_service.py
RUN pip install --no-cache-dir fastapi uvicorn chromadb sentence-transformers aiohttp

EXPOSE 8001
CMD ["uvicorn", "memory_service:app", "--host", "0.0.0.0", "--port", "8001"]
