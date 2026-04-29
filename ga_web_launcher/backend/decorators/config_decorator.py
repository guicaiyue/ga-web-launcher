"""配置文件装饰器：读取、备份、写入 mykey.py / bootstrap"""
import shutil, datetime
from pathlib import Path
from core.utils import read_json, write_json
from core.backup import backup_file

class ConfigDecorator:
    def __init__(self, ga_root: Path | str):
        self.ga_root = Path(ga_root)

    def read_mykey(self) -> dict:
        p = self.ga_root / "mykey.py"
        return {"exists": p.exists(), "content": p.read_text("utf-8", errors="replace") if p.exists() else ""}

    def backup_mykey(self) -> dict:
        p = self.ga_root / "mykey.py"
        if not p.exists():
            return {"ok": False, "error": "mykey.py 不存在"}
        bp = backup_file(p)
        return {"ok": True, "backup": str(bp)}

    def write_mykey(self, content: str) -> dict:
        p = self.ga_root / "mykey.py"
        self.backup_mykey()
        p.write_text(content, "utf-8")
        return {"ok": True, "written": str(p)}

    def list_backups(self, stem: str = "") -> list[dict]:
        from core.backup import list_backups as _lb
        return _lb(stem)

__all__ = ["ConfigDecorator"]
