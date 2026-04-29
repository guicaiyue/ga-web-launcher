"""Key Service - 密钥管理服务"""
from decorators.key_decorator import KeyDecorator
from core.paths import DATA_DIR

class KeyService:
    def __init__(self):
        self.key_dec = KeyDecorator(DATA_DIR / "llm_profiles.json")
    
    def list_keys(self):
        return self.key_dec.load_profiles()
    
    def add_key(self, key_data: dict):
        profiles = self.key_dec.load_profiles()
        profiles.append(key_data)
        self.key_dec.file.write_text(__import__('json').dumps(profiles, indent=2))
        return {"ok": True}
    
    def delete_key(self, key_id: str):
        profiles = [p for p in self.key_dec.load_profiles() if p.get("id") != key_id]
        self.key_dec.file.write_text(__import__('json').dumps(profiles, indent=2))
        return {"ok": True}
