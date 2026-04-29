"""通用工具函数"""
import json, subprocess, shutil, datetime
from pathlib import Path
from typing import Any, Optional

def utc_now() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"

def read_json(path: Path | str, default=None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default

def write_json(path: Path | str, data: Any, indent=2) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")

def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def run_cmd(cmd: list[str], cwd: Path | str | None = None, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)

def copy_file(src: Path | str, dst: Path | str) -> None:
    shutil.copy2(src, dst)

def remove_file(path: Path | str) -> None:
    Path(path).unlink(missing_ok=True)

__all__ = ["utc_now", "read_json", "write_json", "ensure_dir", "run_cmd", "copy_file", "remove_file"]
