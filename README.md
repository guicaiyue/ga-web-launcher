# GenericAgent Web Launcher

Web版本Launcher，通过浏览器访问。

## 快速部署 (Docker)

```bash
# 一键启动
curl -fsSL https://raw.githubusercontent.com/guicaiyue/ga-web-launcher/master/docker-compose.yaml -o docker-compose.yaml
docker-compose up -d
```

访问: http://localhost:8761

| 服务 | 端口 | 说明 |
|-----|------|------|
| Frontend | 8761 | Vue3 + Element Plus |
| Backend | 8760 | FastAPI + WebSocket (端口8000映射) |

## 手动构建

```bash
# 后端
cd ga_web_launcher/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8760

# 前端 (需要先构建)
cd ../frontend
npm install && npm run build
```

## Docker镜像

| 镜像 | 大小 |
|-----|------|
| xirizhi/ga-web-launcher-backend:latest | 171MB |
| xirizhi/ga-web-launcher-frontend:latest | 62MB |

## 技术栈

- **Backend**: FastAPI + uvicorn + WebSocket
- **Frontend**: Vue3 + Element Plus + Vite
- **CI/CD**: GitHub Actions → Docker Hub

## 功能

- 聊天界面
- 会话管理
- 前端选择 (Streamlit / Qt DesktopPet 等)
