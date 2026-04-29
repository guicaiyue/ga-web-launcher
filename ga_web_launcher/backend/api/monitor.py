"""Monitor 路由：系统状态 / 日志"""
from fastapi import APIRouter
from services.monitor_service import MonitorService
from pathlib import Path

router = APIRouter(prefix="/api/monitor", tags=["monitor"])
_log_dir = Path(__file__).parent.parent / "logs"

def _svc():
    return MonitorService()

@router.get("/status")
def system_status():
    return _svc().get_system_status()

@router.get("/logs")
def recent_logs(lines: int = 100):
    return _svc().get_recent_logs(_log_dir, lines)
