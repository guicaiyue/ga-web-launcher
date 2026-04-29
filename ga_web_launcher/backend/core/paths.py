"""路径配置"""
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
GA_ROOT = BACKEND_ROOT / "GenericAgent"
GA_ROOT_DEFAULT = GA_ROOT
DATA_DIR = BACKEND_ROOT / "data"
BACKUP_DIR = DATA_DIR / "backups"
LOG_DIR = BACKEND_ROOT / "logs"

__all__ = [
    "BACKEND_ROOT",
    "GA_ROOT",
    "GA_ROOT_DEFAULT",
    "DATA_DIR",
    "BACKUP_DIR",
    "LOG_DIR",
]
