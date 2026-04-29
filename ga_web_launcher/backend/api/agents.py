"""Agents API - Agent管理接口"""
from fastapi import APIRouter
from services.agent_service import AgentService
from core.paths import GA_ROOT, DATA_DIR

router = APIRouter(prefix="/api/agents", tags=["agents"])
agent_svc = AgentService(GA_ROOT, DATA_DIR / "agents.json")

@router.get("")
async def list_agents():
    return agent_svc.list_agents()

@router.post("/start/{agent_id}")
async def start_agent(agent_id: str):
    return agent_svc.start_agent(agent_id)

@router.post("/stop/{agent_id}")
async def stop_agent(agent_id: str, pid: int):
    return agent_svc.stop_agent(agent_id, pid)
