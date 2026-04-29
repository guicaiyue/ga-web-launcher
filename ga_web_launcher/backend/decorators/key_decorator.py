"""Key 装饰器：Provider/Mixin 配置、可视化脱敏、连接测试"""
import requests
from core.utils import read_json, write_json
from core.security import mask_secret
from core.schema import ProviderConfig, MixinConfig

class KeyDecorator:
    def __init__(self, llm_profiles_file):
        self.file = llm_profiles_file

    def load_providers(self) -> list[ProviderConfig]:
        data = read_json(self.file, default={"providers": []})
        return [ProviderConfig(**p) for p in data.get("providers", [])]

    def save_providers(self, providers: list[ProviderConfig]) -> dict:
        data = read_json(self.file, default={"providers": [], "mixins": []})
        data["providers"] = [p.model_dump() for p in providers]
        write_json(self.file, data)
        return {"ok": True}

    def load_mixins(self) -> list[MixinConfig]:
        data = read_json(self.file, default={"mixins": []})
        return [MixinConfig(**m) for m in data.get("mixins", [])]

    def save_mixins(self, mixins: list[MixinConfig]) -> dict:
        data = read_json(self.file, default={"providers": [], "mixins": []})
        data["mixins"] = [m.model_dump() for m in mixins]
        write_json(self.file, data)
        return {"ok": True}

    def test_connection(self, provider: ProviderConfig) -> dict:
        try:
            headers = {"Authorization": f"Bearer {provider.api_key}"}
            resp = requests.get(
                f"{provider.api_base.rstrip('/')}/models",
                headers=headers, timeout=provider.timeout or 10)
            return {"ok": resp.status_code < 400, "status": resp.status_code,
                    "body": resp.text[:200]}
        except Exception as e:
            return {"ok": False, "error": str(e)}

__all__ = ["KeyDecorator"]
