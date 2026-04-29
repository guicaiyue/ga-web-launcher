"""Repo API - 代码仓库管理接口"""
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from services.update_service import UpdateService
from core.paths import GA_ROOT

router = APIRouter(prefix="/api/repo", tags=["repo"])
update_svc = UpdateService(GA_ROOT)
ALLOWED_DOCS = {
    "README.md": GA_ROOT / "README.md",
    "GETTING_STARTED.md": GA_ROOT / "GETTING_STARTED.md",
}

@router.get("/status")
async def status():
    return update_svc.get_status()

@router.post("/check-update")
async def check_update():
    return update_svc.check_update()

@router.post("/pull")
async def pull():
    return update_svc.pull_latest()

@router.get("/docs/{name}", response_class=PlainTextResponse)
async def read_doc(name: str):
    path = ALLOWED_DOCS.get(name)
    if not path:
        raise HTTPException(status_code=404, detail="文档不存在")
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="文档不存在")
    return path.read_text(encoding="utf-8")

