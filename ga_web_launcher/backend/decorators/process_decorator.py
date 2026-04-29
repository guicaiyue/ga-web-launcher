"""进程管理装饰器：精确 PID 管理，不误杀"""
import os, signal, psutil, time
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessStatus:
    pid: int
    name: str
    cmdline: str
    cpu_pct: float
    mem_mb: float
    running: bool

class ProcessDecorator:
    @staticmethod
    def _load(pid: int) -> Optional[psutil.Process]:
        try:
            p = psutil.Process(pid)
            if p.is_running():
                return p
        except psutil.NoSuchProcess:
            pass
        return None

    def start_process(self, cmd: list[str], cwd: str | None = None,
                      env: dict | None = None, wait: float = 0.5) -> dict:
        import subprocess
        try:
            p = subprocess.Popen(cmd, cwd=cwd, env=env)
            time.sleep(wait)
            if self._load(p.pid):
                return {"ok": True, "pid": p.pid}
            return {"ok": False, "error": "进程启动后立即退出"}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def stop_process(self, pid: int, timeout: int = 10) -> dict:
        p = self._load(pid)
        if not p:
            return {"ok": False, "error": f"PID {pid} 不存在或已退出"}
        try:
            p.terminate()
            p.wait(timeout=timeout)
            return {"ok": True}
        except psutil.TimeoutExpired:
            p.kill()
            return {"ok": True, "killed": True}

    def get_status(self, pid: int) -> Optional[ProcessStatus]:
        p = self._load(pid)
        if not p:
            return None
        try:
            with p.oneshot():
                return ProcessStatus(
                    pid=p.pid, name=p.name(),
                    cmdline=" ".join(p.cmdline()),
                    cpu_pct=p.cpu_percent(),
                    mem_mb=p.memory_info().rss / 1024 / 1024,
                    running=p.is_running())
        except Exception:
            return None

    def tail_logs(self, path: str, lines: int = 100) -> str:
        try:
            with open(path, "rb") as f:
                f.seek(0, 2)
                size = f.tell()
                f.seek(max(0, size - lines * 200))
                return f.read().decode("utf-8", errors="replace").splitlines()[-lines:]
        except Exception:
            return ""

__all__ = ["ProcessDecorator", "ProcessStatus"]
