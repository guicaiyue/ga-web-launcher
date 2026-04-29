"""System API - 系统信息接口"""
from fastapi import APIRouter
from datetime import datetime
import sys
from core.paths import GA_ROOT, DATA_DIR

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/health")
async def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@router.get("/info")
async def info():
    return {
        "python_version": sys.version,
        "genericagent_root": str(GA_ROOT),
        "running_agents": 0,
        "data_dir": str(DATA_DIR)
    }

