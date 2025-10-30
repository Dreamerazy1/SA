from fastapi import FastAPI
from app.adapters.http.tags_router import router as tags_router

app = FastAPI(title="Tags Service")

app.include_router(tags_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}