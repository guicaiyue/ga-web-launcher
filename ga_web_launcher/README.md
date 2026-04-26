# GenericAgent Web Launcher
Web版本Launcher，通过浏览器访问。

## 技术栈
- FastAPI后端
- WebSocket实时通信
- Vue3 + Element Plus前端

## 运行
```bash
pip install -r requirements.txt
cd backend
uvicorn main:app --reload --port 8760
```

## 功能
- 聊天界面
- 会话管理
- 前端选择(Streamlit/Qt DesktopPet等)
