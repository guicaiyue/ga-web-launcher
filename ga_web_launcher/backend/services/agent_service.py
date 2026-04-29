"""Agent 业务服务：封装 Agent 启停、状态查询"""
from decorators.repo_decorator import RepoDecorator
from decorators.hub_decorator import HubDecorator
from decorators.process_decorator import ProcessDecorator
from core.utils import read_json, write_json
from pathlib import Path

class AgentService:
    def __init__(self, ga_root: Path | str, agents_file: Path | str):
        self.ga_root = Path(ga_root)
        self.repo = RepoDecorator(ga_root)
        self.hub = HubDecorator(agents_file)
        self._proc = ProcessDecorator()

    def get_repo_status(self):
        return self.repo.check_update()

    def pull_update(self):
        return self.repo.pull_latest()

    def list_agents(self):
        return self.hub.discover()

    def start_agent(self, id_: str):
        return self.hub.start(id_)

    def stop_agent(self, id_: str, pid: int):
        return self.hub.stop(id_, pid)

    def get_agent_status(self, id_: str) -> dict:
        agents = self.hub.discover()
        cfg = next((a for a in agents if a.id == id_), None)
        if not cfg:
            return {"exists": False}
        return {"exists": True, "config": cfg.model_dump()}

__all__ = ["AgentService"]
