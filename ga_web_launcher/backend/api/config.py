"""Config 路由：mykey / Provider / Mixin / 备份"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.config_service import ConfigService
from pathlib import Path

router = APIRouter(prefix="/api/config", tags=["config"])

_ga_root = Path(__file__).parent.parent.parent   # ga_web_launcher
_key_file = _ga_root / "backend" / "data" / "llm_profiles.json"

def _svc():
    return ConfigService(_ga_root, _key_file)

# ── mykey ──
class WriteMykeyReq(BaseModel):
    content: str

@router.get("/mykey")
def read_mykey():
    return _svc().read_mykey()

@router.post("/mykey")
def write_mykey(req: WriteMykeyReq):
    return _svc().write_mykey(req.content)

@router.post("/mykey/backup")
def backup_mykey():
    return _svc().backup_mykey()

# ── providers ──
@router.get("/providers")
def list_providers():
    return _svc().list_providers()

@router.post("/providers")
def save_provider(cfg: dict):
    return _svc().save_provider(cfg)

@router.post("/providers/test")
def test_connection(cfg: dict):
    return _svc().test_connection(cfg)

# ── mixins ──
@router.get("/mixins")
def list_mixins():
    return _svc().list_mixins()

# ── 备份 ──
@router.get("/backups")
def list_backups(stem: str = ""):
    return _svc().list_backups(stem)
