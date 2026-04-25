# GenericAgent Web Launcher - 开发计划

## 目标
将 GenericAgent Launcher (Qt桌面版) 转换为 Web 版本，部署在NAS上，通过浏览器访问。

## 技术选型
| 层级 | 选型 |
|------|------|
| 前端 | Vue3 + Element Plus |
| 后端 | FastAPI |
| 实时通信 | WebSocket |
| 会话存储 | SQLite/JSON文件 |

## 项目结构
```
ga_web_launcher/
├── backend/
│   ├── main.py              # FastAPI入口
│   ├── api/                 # API路由
│   ├── core/                # 复用launcher_core_parts
│   ├── ws_handler.py        # WebSocket处理器
│   └── static/              # 前端构建输出
├── frontend/                # Vue3源码
├── requirements.txt
└── README.md
```

## 实施步骤

### Phase 1: 项目初始化
- [ ] 创建GitHub公开仓库 `ga-web-launcher`
- [ ] 初始化FastAPI项目结构
- [ ] 迁移 launcher_core_parts 核心逻辑

### Phase 2: 后端核心
- [ ] 迁移 runtime.py - GA进程管理
- [ ] 迁移 sessions.py - 会话管理
- [ ] 迁移 channels.py - 渠道配置
- [ ] 迁移 api/settings 配置接口

### Phase 3: WebSocket聊天
- [ ] 实现WebSocket端点
- [ ] 消息流：前端 → WS → GA后端 → 流式响应 → 前端
- [ ] 会话历史加载

### Phase 4: 前端UI
- [ ] 登录/首页
- [ ] 聊天界面
- [ ] 会话侧边栏
- [ ] 设置面板

### Phase 5: 部署
- [ ] Docker化部署
- [ ] NAS systemd服务配置

## 交付物
1. GitHub公开仓库
2. Docker部署配置
3. NAS部署文档
