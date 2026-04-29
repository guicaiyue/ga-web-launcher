"""Monitor 业务服务：系统资源监控、日志"""
import psutil, datetime
from pathlib import Path

class MonitorService:
    def get_system_status(self):
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "cpu_pct": cpu,
            "mem_total_mb": mem.total / 1024 / 1024,
            "mem_used_mb": mem.used / 1024 / 1024,
            "mem_pct": mem.percent,
            "disk_total_gb": disk.total / 1024 / 1024 / 1024,
            "disk_used_gb": disk.used / 1024 / 1024 / 1024,
            "disk_pct": disk.percent,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        }

    def get_recent_logs(self, log_dir: Path, lines: int = 100):
        logs = []
        for p in sorted(log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            try:
                with open(p, "rb") as f:
                    content = f.read().decode("utf-8", errors="replace").splitlines()[-lines:]
                    logs.append({"file": p.name, "lines": content})
            except Exception:
                pass
        return logs

__all__ = ["MonitorService"]
