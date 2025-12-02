# Legends of Minds - File Ingest Service

## Overview

The File Ingest Service handles document upload, processing, and metadata management for the Legends of Minds knowledge base.

## Features

- File upload with deduplication (SHA256 hashing)
- Metadata tracking (filename, size, upload time, collection)
- File listing and management
- Integration with Qdrant vector database
- Health monitoring

## Files

- `main.py` - FastAPI application for file ingestion

## Endpoints

### Core Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `GET /docs` - API documentation

### File Management (`/api/`)

- `POST /upload` - Upload a file
  - Form data: `file` (required), `collection` (optional)
  - Returns: file ID, filename, size
  
- `GET /files` - List all uploaded files
  - Returns: array of file metadata
  
- `DELETE /files/{file_id}` - Delete a file
  - Requires: file ID (hash prefix)

## Storage

Files are stored in `/uploads` (mapped to `F:/uploads` on Windows) with:
- Original filename preserved
- SHA256 hash prefix for deduplication
- JSON metadata sidecar files (`.meta.json`)

## Dependencies

```
fastapi
uvicorn
httpx
```

## Running Locally

```bash
cd ingest
pip install fastapi uvicorn httpx
mkdir -p /tmp/uploads  # Create upload directory
UPLOAD_DIR=/tmp/uploads uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

### Upload a File

```bash
curl -X POST http://localhost:8001/api/upload \
  -F "file=@document.pdf" \
  -F "collection=my_notes"
```

### List Files

```bash
curl http://localhost:8001/api/files
```

### Delete a File

```bash
curl -X DELETE http://localhost:8001/api/files/abc12345
```

## Architecture

The Ingest Service:
1. Accepts file uploads via multipart form data
2. Calculates SHA256 hash for deduplication
3. Stores file with hash prefix
4. Saves metadata as JSON
5. (Future) Processes files for vector embedding
6. (Future) Stores vectors in Qdrant

## Security

- Files are stored with safe filenames (no path traversal)
- SHA256 hashing prevents duplicates
- No external API calls
- Localhost-bound by default
