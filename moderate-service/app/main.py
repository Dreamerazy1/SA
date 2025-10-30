from fastapi import FastAPI
from app.adapters.http.auth_router import router as auth_router
from app.adapters.http.moderation_router import router as moderation_router
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Moderation Service")

app.include_router(auth_router)
app.include_router(moderation_router)

# Serve admin UI if present
admin_dir = Path("app/static/admin")
if admin_dir.exists():
    app.mount("/admin", StaticFiles(directory=str(admin_dir), html=True), name="admin")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
