"""Config 业务服务：mykey/Provider/Mixin 配置读写"""
from decorators.config_decorator import ConfigDecorator
from decorators.key_decorator import KeyDecorator
from core.schema import ProviderConfig, MixinConfig
from pathlib import Path

class ConfigService:
    def __init__(self, ga_root: Path | str, key_file: Path | str):
        self.ga_root = Path(ga_root)
        self._cfg = ConfigDecorator(ga_root)
        self._key = KeyDecorator(key_file)

    def read_mykey(self):
        return self._cfg.read_mykey()

    def write_mykey(self, content: str):
        return self._cfg.write_mykey(content)

    def backup_mykey(self):
        return self._cfg.backup_mykey()

    def list_providers(self):
        from core.security import mask_secret
        providers = []
        for p in self._key.load_providers():
            data = p.model_dump()
            if "api_key" in data:
                data["api_key"] = mask_secret(data["api_key"])
            providers.append(data)
        return providers

    def save_provider(self, cfg: dict):
        cfg = {"name": "default", **cfg}
        return self._key.save_providers([ProviderConfig(**cfg)])

    def list_mixins(self):
        return [m.model_dump() for m in self._key.load_mixins()]

    def test_connection(self, cfg: dict):
        cfg = {"name": "default", **cfg}
        return self._key.test_connection(ProviderConfig(**cfg))

    def list_backups(self, stem=""):
        return self._cfg.list_backups(stem)

__all__ = ["ConfigService"]
