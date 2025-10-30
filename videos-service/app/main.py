from fastapi import FastAPI
from app.adapters.http.videos_router import router as videos_router


app = FastAPI(title="Videos Service")

app.include_router(videos_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


