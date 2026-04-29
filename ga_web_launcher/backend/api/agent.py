"""Agent 路由：仓库状态 / Agent 列表 / 启停"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.agent_service import AgentService

router = APIRouter(prefix="/api/agents", tags=["agents"])

# ── request/response 模型 ──
class StartReq(BaseModel):
    agent_id: str

class StopReq(BaseModel):
    agent_id: str
    pid: int

# ── 依赖注入 (简易，Phase 4 重构为 Depends) ──
_ga_root = Path(__file__).parent.parent / "data"   # 暂用 backend/data
_agents_file = _ga_root / "agents.json"

def _svc():
    return AgentService(_ga_root, _agents_file)

@router.get("/repo/status")
def repo_status():
    return _svc().get_repo_status()

@router.post("/repo/pull")
def repo_pull():
    return _svc().pull_update()

@router.get("/")
def list_agents():
    return _svc().list_agents()

@router.post("/start")
def start_agent(req: StartReq):
    result = _svc().start_agent(req.agent_id)
    if not result.get("ok"):
        raise HTTPException(400, result.get("error", "启动失败"))
    return result

@router.post("/stop")
def stop_agent(req: StopReq):
    return _svc().stop_agent(req.agent_id, req.pid)

@router.get("/{agent_id}")
def get_agent(agent_id: str):
    r = _svc().get_agent_status(agent_id)
    if not r.get("exists"):
        raise HTTPException(404, "Agent not found")
    return r
