"""Agent Hub 装饰器：多 Agent 发现、启停、管理"""
from pathlib import Path
from core.utils import read_json, write_json
from core.schema import AgentConfig
from .process_decorator import ProcessDecorator

class HubDecorator:
    def __init__(self, data_file: Path | str):
        self.data_file = Path(data_file)
        self._proc = ProcessDecorator()
        self._agents: list[AgentConfig] = []

    def _load(self):
        self._agents = [AgentConfig(**a) for a in read_json(self.data_file, default=[])]
        return self._agents

    def _save(self):
        write_json(self.data_file, [a.model_dump() for a in self._agents])

    def discover(self) -> list[AgentConfig]:
        return self._load()

    def create(self, cfg: AgentConfig) -> dict:
        try:
            self._load()
            cfg.id = cfg.id or f"agent_{len(self._agents)+1}"
            self._agents.append(cfg)
            self._save()
            return {"ok": True, "agent": cfg.model_dump()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def update(self, id_: str, cfg: AgentConfig) -> dict:
        self._load()
        for i, a in enumerate(self._agents):
            if a.id == id_:
                self._agents[i] = cfg
                self._save()
                return {"ok": True}
        return {"ok": False, "error": "Agent not found"}

    def delete(self, id_: str) -> dict:
        self._load()
        self._agents = [a for a in self._agents if a.id != id_]
        self._save()
        return {"ok": True}

    def start(self, id_: str) -> dict:
        self._load()
        cfg = next((a for a in self._agents if a.id == id_), None)
        if not cfg:
            return {"ok": False, "error": "Agent not found"}
        return self._proc.start_process(cfg.startup_cmd.split(), cwd=cfg.workdir)

    def stop(self, id_: str, pid: int) -> dict:
        return self._proc.stop_process(pid)

    def get_all_status(self) -> list[dict]:
        self._load()
        result = []
        for a in self._agents:
            result.append({"id": a.id, "name": a.name, "enabled": a.enabled})
        return result

__all__ = ["HubDecorator"]
