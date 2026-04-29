"""Chat 业务服务：会话管理、真实聊天接入桥接"""
from decorators.chat_bridge_decorator import ChatBridgeDecorator
from pathlib import Path
import asyncio, json, queue

# 模块级单例，确保所有 ChatService 实例共享同一个 registry
_bridge_singleton = None

class ChatService:
    def __init__(self, data_dir: Path | str):
        global _bridge_singleton
        if _bridge_singleton is None:
            _bridge_singleton = ChatBridgeDecorator(data_dir)
        self.bridge = _bridge_singleton



    async def send_message_stream(self, session_id: str, message: str):
        """流式输出生成器，供 SSE 使用"""
        import asyncio
        agent = self.bridge.get_or_create_agent(session_id)
        display_queue = agent.put_task(message, source="web")
        
        full_response = ""
        try:
            while True:
                try:
                    item = await asyncio.to_thread(display_queue.get, timeout=120)
                except queue.Empty:
                    yield f"data: {json.dumps({'type': 'error', 'content': 'Timeout waiting for response'})}\n\n"
                    break
                
                if "next" in item:
                    # 增量输出
                    full_response = item["next"]
                    yield f"data: {json.dumps({'type': 'partial', 'content': full_response})}\n\n"
                elif "done" in item:
                    # 完整输出
                    full_response = item["done"]
                    yield f"data: {json.dumps({'type': 'done', 'content': full_response})}\n\n"
                    # 保存到会话历史
                    session = self.bridge.load_session(session_id)
                    msgs = session.get("messages", [])
                    msgs.append({"role": "user", "content": message})
                    msgs.append({"role": "assistant", "content": full_response})
                    self.bridge.save_session(session_id, msgs)
                    break
        except Exception as e:
            print(f"[ERROR] send_message_stream: {e}", flush=True)
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
    
    def _call_llm(self, messages: list[dict]) -> str:
        """调用真实 LLM API"""
        import requests
        from core.utils import read_json
        
        # 读取配置
        profiles_file = Path(self.bridge.data_dir) / "llm_profiles.json"
        data = read_json(profiles_file, default={"providers": []})
        providers = data.get("providers", [])
        
        if not providers:
            return "❌ 未配置 AI Provider，请点击右上角 ⚙️ AI配置"
        
        provider = providers[0]
        api_base = provider.get("api_base", "").rstrip("/")
        api_key = provider.get("api_key", "")
        model = provider.get("model", "gpt-4o-mini")
        timeout = provider.get("timeout", 30)
        
        # 构造请求
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"model": model, "messages": [{"role": m["role"], "content": m["content"]} for m in messages if m.get("role") in ["user", "assistant", "system"]]}
        
        # 尝试 /v1/chat/completions，失败则回退 /chat/completions
        for endpoint in [f"{api_base}/v1/chat/completions", f"{api_base}/chat/completions"]:
            try:
                resp = requests.post(endpoint, json=payload, headers=headers, timeout=timeout)
                if resp.status_code == 200:
                    return resp.json()["choices"][0]["message"]["content"]
                elif resp.status_code != 404:
                    return f"❌ API 错误 {resp.status_code}: {resp.text[:200]}"
            except Exception as e:
                if "404" not in str(e):
                    return f"❌ 调用失败: {str(e)[:200]}"
        
        return f"❌ API 端点不可用: {api_base}"

    def create_session(self, title: str = "") -> dict:
        """创建新会话"""
        import time
        session_id = f"sess_{int(time.time() * 1000)}"
        name = title or f"会话 {session_id[-6:]}"
        self.bridge.save_session(session_id, [])
        return {"id": session_id, "name": name, "messages": []}

    def get_history(self, session_id: str):
        session = self.bridge.load_session(session_id)
        return {"messages": session.get("messages", [])}

    def list_sessions(self):
        return self.bridge.list_sessions()

__all__ = ["ChatService"]
