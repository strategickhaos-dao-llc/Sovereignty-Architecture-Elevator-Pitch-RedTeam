FROM python:3.11-slim
WORKDIR /app
COPY rag_api.py /app/rag_api.py
RUN pip install --no-cache-dir fastapi uvicorn requests python-dotenv
EXPOSE 8000
CMD ["uvicorn", "rag_api:app", "--host", "0.0.0.0", "--port", "8000"]
