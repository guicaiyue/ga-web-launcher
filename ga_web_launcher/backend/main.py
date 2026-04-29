"""FastAPI Backend for GA Web Launcher"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 GA Web Launcher starting...")
    from core.bootstrap import ensure_generic_agent
    result = ensure_generic_agent()
    if not result.get("ok"):
        print(f"⚠️ Bootstrap failed: {result.get('error')}")
    yield
    print("🛑 Shutdown...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
from api.system import router as system_router
from api.repo import router as repo_router
from api.agents import router as agents_router
from api.keys import router as keys_router
from api.chat import router as chat_router
from api.config import router as config_router

app.include_router(system_router)
app.include_router(repo_router)
app.include_router(agents_router)
app.include_router(keys_router)
app.include_router(chat_router)
app.include_router(config_router)

# Mount frontend
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/app", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

@app.get("/")
async def root():
    return {"message": "GA Web Launcher API", "version": "0.1.0"}
