"""Chat 路由：会话 CRUD / WebSocket"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from services.chat_service import ChatService
import json, asyncio
from pathlib import Path

router = APIRouter(prefix="/api/chat", tags=["chat"])
_data_dir = Path(__file__).parent.parent / "data"
_sessions_file = _data_dir / "chat_sessions.json"

def _svc():
    return ChatService(_data_dir)

class SendReq(BaseModel):
    session_id: str
    message: str

@router.get("/sessions")
def list_sessions():
    return _svc().list_sessions()

@router.post("/sessions")
def create_session(title: str = ""):
    return _svc().create_session(title)

@router.get("/history/{session_id}")
def get_history(session_id: str):
    return _svc().get_history(session_id)

# ── WebSocket 实时聊天 ──
@router.websocket("/ws/{session_id}")
async def ws_chat(ws: WebSocket, session_id: str):
    await ws.accept()
    svc = _svc()
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "ping":
                await ws.send_text(json.dumps({"type": "pong"}))
            elif msg.get("type") == "message":
                # 流式推送：异步消费生成器
                user_msg = msg.get("message", "")
                async for chunk in svc.send_message_stream(session_id, user_msg):
                    # chunk 格式: "data: {...}\n\n"
                    if chunk.startswith("data: "):
                        payload = json.loads(chunk[6:].strip())
                        await ws.send_text(json.dumps(payload))
                        if payload.get("type") == "done":
                            await asyncio.sleep(0.3)  # 确保 done 帧发出后再关闭连接
                            try:
                                await ws.close()
                            except Exception:
                                pass
                            break
                    await asyncio.sleep(0)  # 让出控制权
    except WebSocketDisconnect:
        pass
