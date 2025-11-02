from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api.routes import evaluator_routes
from backend.db.database import Base, engine
from pathlib import Path

# --- Initialize DB ---
Base.metadata.create_all(bind=engine)

# --- App setup ---
app = FastAPI(title="ZenChess API", version="1.0")

# --- Mount frontend ---
frontend_dir = Path(__file__).parent / "../../frontend"
app.mount("/assets", StaticFiles(directory=frontend_dir / "assets"), name="assets")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# --- Include API routes ---
app.include_router(evaluator_routes.router, prefix="/api/v1", tags=["Evaluator"])

# --- Serve frontend index ---
@app.get("/")
def serve_frontend():
    return FileResponse(frontend_dir / "index.html")
