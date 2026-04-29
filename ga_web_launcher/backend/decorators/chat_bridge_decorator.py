"""聊天桥接装饰器：接入 GenericAgent 真实聊天能力"""
import sys, os, threading, time
from pathlib import Path
from core.utils import read_json, write_json
from core.paths import GA_ROOT

# 延迟导入 GeneraticAgent（避免启动时 GA 目录不存在）
_GeneraticAgent = None
def _get_agent_class():
    global _GeneraticAgent
    if _GeneraticAgent is None:
        if str(GA_ROOT) not in sys.path:
            sys.path.insert(0, str(GA_ROOT))
        from agentmain import GeneraticAgent as GA
        _GeneraticAgent = GA
    return _GeneraticAgent

class ChatBridgeDecorator:
    """
    管理多 session 的 GenericAgent 实例池。
    每个 session 独立 agent + 后台线程。
    """
    def __init__(self, data_dir: Path | str):
        self.data_dir = Path(data_dir)
        self.sessions_file = self.data_dir / "chat_sessions.json"
        self._registry = {}  # {session_id: {"agent": GeneraticAgent, "thread": Thread, "last_active": float}}
        self._lock = threading.Lock()

    def get_or_create_agent(self, session_id: str):
        """获取或创建 session 对应的 agent 实例"""
        with self._lock:
            if session_id not in self._registry:
                AgentClass = _get_agent_class()
                agent = AgentClass()
                agent.verbose = False
                thread = threading.Thread(target=agent.run, daemon=True)
                thread.start()
                self._registry[session_id] = {
                    "agent": agent,
                    "thread": thread,
                    "last_active": time.time()
                }
            else:
                self._registry[session_id]["last_active"] = time.time()
            return self._registry[session_id]["agent"]

    def cleanup_inactive(self, timeout_seconds: int = 3600):
        """清理超时未活跃的 session（默认1小时）"""
        with self._lock:
            now = time.time()
            to_remove = [sid for sid, ctx in self._registry.items() 
                        if now - ctx["last_active"] > timeout_seconds]
            for sid in to_remove:
                ctx = self._registry.pop(sid)
                ctx["agent"].abort()  # 停止运行中的任务
            return len(to_remove)

    def cleanup_session(self, session_id: str) -> bool:
        """手动清理指定 session"""
        with self._lock:
            if session_id in self._registry:
                ctx = self._registry.pop(session_id)
                ctx["agent"].abort()
                return True
            return False

    def save_session(self, session_id: str, messages: list[dict]) -> dict:
        data = read_json(self.sessions_file, default={})
        data[session_id] = {"messages": messages, "updated": self._now()}
        write_json(self.sessions_file, data)
        return {"ok": True}

    def load_session(self, session_id: str) -> dict:
        data = read_json(self.sessions_file, default={})
        return data.get(session_id, {"messages": []})

    def list_sessions(self) -> list[dict]:
        data = read_json(self.sessions_file, default={})
        return [{"id": k, **v} for k, v in data.items()]

    def _now(self):
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"

__all__ = ["ChatBridgeDecorator"]
