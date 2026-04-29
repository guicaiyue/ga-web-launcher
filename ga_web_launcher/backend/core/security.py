"""安全相关：脱敏、日志清理"""
import re

def mask_secret(value: str | None, visible: int = 4) -> str:
    """将密钥/密码脱敏，只保留末尾可见字符"""
    if not value:
        return ""
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]

def sanitize_log_text(text: str) -> str:
    """移除日志中的敏感信息（API Key、Token）"""
    # 移除常见的 key=xxx 或 key: xxx 模式
    text = re.sub(r'(api[_-]?key|access[_-]?token|secret|password|apikey)[=:]["\']?([\w\-]{8,})["\']?',
                  r'\1=***MASKED***', text, flags=re.IGNORECASE)
    # 移除完整的 Bearer token
    text = re.sub(r'Bearer\s+[\w\-\.]+', 'Bearer ***MASKED***', text)
    return text

__all__ = ["mask_secret", "sanitize_log_text"]
