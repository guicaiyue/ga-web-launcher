"""FastAPI Backend for GA Web Launcher"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json, asyncio
from typing import Dict

# In-memory session store
sessions: Dict[str, dict] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 GA Web Launcher starting...")
    yield
    print("🛑 Shutdown...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "GA Web Launcher API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# WebSocket endpoint for chat
@app.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    session_id = None
    try:
        while True:
            data = await ws.receive_text()
            msg = json.loads(data)
            msg_type = msg.get("type")
            
            if msg_type == "init":
                session_id = msg.get("session_id", "default")
                sessions[session_id] = {"history": [], "config": {}}
                await ws.send_text(json.dumps({
                    "type": "init_ok", "session_id": session_id
                }))
            elif msg_type == "chat":
                user_msg = msg.get("message", "")
                # Echo for now - will integrate GA later
                await ws.send_text(json.dumps({
                    "type": "response", "message": f"Echo: {user_msg}"
                }))
    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")
