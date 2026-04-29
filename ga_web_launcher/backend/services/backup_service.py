"""Backup 业务服务：文件备份、恢复、清理"""
from core.backup import backup_file, restore_file, list_backups as _lb
from core.utils import ensure_dir

class BackupService:
    def backup(self, path: str):
        return {"path": str(backup_file(path))}

    def restore(self, path: str):
        rp = restore_file(path)
        return {"ok": rp is not None, "path": str(rp) if rp else None}

    def list(self, stem: str = ""):
        return _lb(stem)

__all__ = ["BackupService"]
