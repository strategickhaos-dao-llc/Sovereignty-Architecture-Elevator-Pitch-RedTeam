# main.py
from fastapi import FastAPI
from routes import artifacts_router

app = FastAPI(
    title="Sovereignty Architecture API",
    description="API with 206 Partial Content support for redacted artifacts",
    version="1.0.0",
)

app.include_router(artifacts_router)


@app.get("/health")
async def health():
    return {"status": "healthy", "message": "Empire Eternal"}
