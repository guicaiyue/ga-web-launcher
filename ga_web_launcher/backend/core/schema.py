"""Pydantic 数据模型定义"""
from typing import Optional
from pydantic import BaseModel, Field

class LLMProfile(BaseModel):
    provider: str = ""
    model: str = ""
    thinking_type: Optional[str] = None
    reasoning_effort: Optional[str] = None

class AgentConfig(BaseModel):
    id: str = ""
    name: str = ""
    workdir: str = ""
    startup_cmd: str = ""
    port: int = 0
    llm_profile: LLMProfile = Field(default_factory=LLMProfile)
    auto_start: bool = False
    enabled: bool = True

class ProviderConfig(BaseModel):
    name: str
    type: str = "openai"   # openai | anthropic | ollama | ...
    api_key: str = ""
    api_base: str = ""
    model: str = ""
    thinking_type: Optional[str] = None
    reasoning_effort: Optional[str] = None
    timeout: int = 60
    proxy: str = ""

class MixinConfig(BaseModel):
    name: str
    provider: str
    model: str
    weight: int = 1

class AppSettings(BaseModel):
    genericagent_root: str = ""
    default_agent_id: str = ""
    auto_backup_before_write: bool = True
    auto_restart_after_update: bool = False

__all__ = ["LLMProfile", "AgentConfig", "ProviderConfig", "MixinConfig", "AppSettings"]
