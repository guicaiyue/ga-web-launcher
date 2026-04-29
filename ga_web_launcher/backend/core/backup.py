"""文件备份与恢复"""
import shutil, datetime
from pathlib import Path
from .paths import BACKUP_DIR
from .utils import ensure_dir

def backup_file(file_path: Path | str) -> Path | None:
    """备份指定文件，返回备份路径；失败返回 None"""
    src = Path(file_path)
    if not src.exists():
        return None
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = src.name
    ensure_dir(BACKUP_DIR)
    dst = BACKUP_DIR / f"{src.stem}_{ts}{src.suffix}"
    shutil.copy2(src, dst)
    return dst

def restore_file(backup_path: Path | str) -> Path | None:
    """从备份恢复到原位置（需要原始路径元数据）；简化版返回备份内容"""
    bp = Path(backup_path)
    if not bp.exists() or not str(bp).startswith(str(BACKUP_DIR)):
        return None
    return bp  # 调用方自行处理恢复逻辑

def list_backups(stem: str = "") -> list[dict]:
    """列出所有备份，按时间倒序"""
    ensure_dir(BACKUP_DIR)
    backups = []
    for p in sorted(BACKUP_DIR.iterdir(), reverse=True):
        if stem and stem not in p.stem:
            continue
        backups.append({
            "name": p.name,
            "path": str(p),
            "size": p.stat().st_size,
            "created": datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
        })
    return backups

__all__ = ["backup_file", "restore_file", "list_backups"]
