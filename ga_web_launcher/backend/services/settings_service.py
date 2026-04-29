"""Settings Service - 系统设置服务"""
from core.utils import read_json, write_json
from core.paths import DATA_DIR

class SettingsService:
    def __init__(self):
        self.settings_file = DATA_DIR / "app_settings.json"
    
    def get_settings(self):
        return read_json(self.settings_file)
    
    def update_settings(self, settings: dict):
        write_json(self.settings_file, settings)
        return settings
