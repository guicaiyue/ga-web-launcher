"""Git 仓库状态与更新装饰器"""
import subprocess
from dataclasses import dataclass
from pathlib import Path
from core.utils import run_cmd

@dataclass
class RepoStatus:
    root: str
    branch: str
    local_commit: str
    remote_commit: str
    behind_count: int
    dirty: bool
    error: str = ""

class RepoDecorator:
    def __init__(self, ga_root: Path | str):
        self.ga_root = Path(ga_root)

    def _fetch(self):
        run_cmd(["git", "fetch", "--all", "--prune"], cwd=self.ga_root, timeout=60)

    def get_status(self) -> RepoStatus:
        try:
            self._fetch()
            b = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.ga_root).stdout.strip()
            lc = run_cmd(["git", "rev-parse", "HEAD"], cwd=self.ga_root).stdout.strip()[:8]
            rc = run_cmd(["git", "rev-parse", "@{u}"], cwd=self.ga_root).stdout.strip()[:8]
            dirty = bool(run_cmd(["git", "status", "--porcelain"], cwd=self.ga_root).stdout.strip())
            counts = run_cmd(["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"],
                             cwd=self.ga_root, timeout=10).stdout.strip().split()
            behind = int(counts[1]) if len(counts) >= 2 else 0
            return RepoStatus(str(self.ga_root), b, lc, rc, behind, dirty)
        except Exception as e:
            return RepoStatus(str(self.ga_root), "?", "?", "?", -1, False, str(e))

    def check_update(self) -> dict:
        s = self.get_status()
        return {"has_update": s.behind_count > 0, "behind_count": s.behind_count,
                "dirty": s.dirty, "branch": s.branch, "error": s.error}

    def get_update_preview(self) -> list[dict]:
        try:
            self._fetch()
            out = run_cmd(["git", "log", "HEAD..@{u}", "--oneline"],
                          cwd=self.ga_root, timeout=15).stdout.strip()
            return [{"message": line} for line in out.splitlines() if line]
        except Exception:
            return []

    def pull_latest(self) -> dict:
        s = self.get_status()
        if s.dirty:
            return {"ok": False, "error": "工作区有未提交改动，请先提交或stash"}
        try:
            out = run_cmd(["git", "pull", "--ff-only"], cwd=self.ga_root, timeout=120)
            return {"ok": out.returncode == 0,
                    "stdout": out.stdout, "stderr": out.stderr}
        except Exception as e:
            return {"ok": False, "error": str(e)}

__all__ = ["RepoDecorator", "RepoStatus"]
