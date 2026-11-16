from pathlib import Path
from fastapi import FastAPI
from app.restaurants.router import router as restaurants_router

app = FastAPI(
    title="FastAPI + React",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.include_router(restaurants_router, prefix="/api/v1")

@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/api/hello")
def hello(name: str = "World") -> dict[str, str]:
    return {"message": f"Hello, {name}!"}

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend" / "dist"

if FRONTEND_DIR.is_dir():
    app.frontend("/", directory=FRONTEND_DIR)
