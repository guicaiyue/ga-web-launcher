# GenericAgent Web Decorator Console - 开发执行计划

## 1. 项目定位

`ga_web_version` 不应被实现为“Web 重写版 GenericAgent”，而应被实现为：

**GenericAgent 的 Web 装饰器控制台（Web Decorator Console）**

即：

- **GenericAgent**：保留为核心执行引擎，负责 agent 推理、工具调用、前端适配、调度等能力
- **ga_web_version**：作为装饰器层，负责 Web 可视化、配置管理、代码更新、多 agent 编排、日志查看与运维控制

### 1.1 设计原则

1. **非侵入优先**：尽量不改动 GenericAgent 核心逻辑
2. **装饰器封装**：对仓库、配置、进程、日志、密钥等能力做包装而非重写
3. **结构化配置优先**：Web 页面维护 JSON/YAML，再生成 `mykey.py`
4. **可回滚**：更新代码、写配置、重启进程前必须具备备份或回退方案
5. **先管理后聊天**：先交付运维控制台价值，再接入真实聊天能力

---

## 2. 当前状态评估

### 2.1 ga_web_version 现状

当前项目已经具备最小 Web 骨架：

- 后端：FastAPI
- 前端：Vue3 + Element Plus（单页）
- 通信：WebSocket
- 功能：会话列表 + 聊天回显（Echo）
- 部署：Docker / GitHub Actions 基础配置

### 2.2 可复用的 GenericAgent 基础能力

已确认可直接借用或封装的核心：

- `launch.pyw`：单实例窗口 + 前端启动逻辑
- `hub.pyw`：多 agent 进程管理、日志读取、状态管理
- `mykey_template.py`：AI key / provider / session / mixin 配置中心

### 2.3 需求落点

本项目重点增强以下三类能力：

1. **Web 页面更好用**
2. **页面按钮可更新 GenericAgent 代码**
3. **支持 GenericAgent 多 agent 管理配置**
4. **支持 AI key 密钥可视化配置**

---

## 3. 总体架构

```text
[Browser]
   ↓
[Vue3 Web Console]
   ↓
[FastAPI Backend]
   ↓
[Decorator Layer]
   ├── RepoDecorator        # Git 更新 / 版本状态
   ├── ProcessDecorator     # 启停 / 重启 / 健康检查
   ├── HubDecorator         # 多 agent 编排
   ├── ConfigDecorator      # 配置读写 / 备份 / 生成
   ├── KeyDecorator         # AI key 可视化 / 测试 / 生成 mykey.py
   └── ChatBridgeDecorator  # WebSocket 与 GenericAgent 聊天桥接
   ↓
[GenericAgent]
```

### 3.1 后端分层建议

```text
ga_web_launcher/backend/
├── main.py
├── api/
│   ├── system.py
│   ├── repo.py
│   ├── agents.py
│   ├── keys.py
│   └── chat.py
├── decorators/
│   ├── repo_decorator.py
│   ├── process_decorator.py
│   ├── hub_decorator.py
│   ├── config_decorator.py
│   ├── key_decorator.py
│   └── chat_bridge_decorator.py
├── services/
│   ├── update_service.py
│   ├── agent_service.py
│   ├── settings_service.py
│   ├── key_service.py
│   └── chat_service.py
├── core/
│   ├── paths.py
│   ├── security.py
│   ├── backup.py
│   ├── schema.py
│   └── utils.py
└── data/
    ├── agents.json
    ├── llm_profiles.json
    ├── app_settings.json
    └── backups/
```

### 3.2 前端分层建议

```text
ga_web_launcher/frontend/
├── index.html
├── src/
│   ├── views/
│   │   ├── Dashboard.vue
│   │   ├── ChatWorkbench.vue
│   │   ├── AgentManager.vue
│   │   ├── KeyManager.vue
│   │   ├── RepoUpdate.vue
│   │   └── SystemSettings.vue
│   ├── components/
│   ├── stores/
│   ├── api/
│   └── router/
```

---

## 4. 功能模块规划

## 4.1 模块 A：代码更新控制台（Repo Decorator）

### 目标
在 Web 页面中完成 GenericAgent 仓库状态查看和一键更新。

### 功能点
- 显示当前分支、当前 commit、最近更新时间
- 检查远程是否有更新
- 预览待更新提交摘要
- 一键 `git pull`
- 更新后可选择自动重启相关 agent
- 输出完整更新日志

### API 草案
- `GET /api/repo/status`
- `POST /api/repo/check-update`
- `POST /api/repo/pull`
- `POST /api/repo/restart-related`

### 风险控制
- 本地工作区有改动时禁止直接 pull
- pull 前展示确认弹窗
- pull 前后记录版本号
- 失败日志落盘
- 必要时支持回滚提示（至少记录旧 commit）

---

## 4.2 模块 B：多 Agent 管理（Hub Decorator）

### 目标
把 `hub.pyw` 的核心思路 Web 化，实现多 agent 统一管理。

### 每个 agent 的建议字段
- `id`
- `name`
- `workdir`
- `startup_cmd`
- `port`
- `llm_profile`
- `frontend_type`
- `env`
- `auto_start`
- `status`
- `pid`
- `last_start_time`
- `health_url`

### 功能点
- 新增 agent
- 编辑 agent
- 启动 / 停止 / 重启
- 查看实时日志
- 健康状态检查
- 批量操作
- 默认 agent 设置

### API 草案
- `GET /api/agents`
- `POST /api/agents`
- `PUT /api/agents/{id}`
- `DELETE /api/agents/{id}`
- `POST /api/agents/{id}/start`
- `POST /api/agents/{id}/stop`
- `POST /api/agents/{id}/restart`
- `GET /api/agents/{id}/logs`
- `GET /api/agents/{id}/status`

### 存储建议
使用 `data/agents.json` 保存结构化配置，不直接把配置散落到前端本地状态。

---

## 4.3 模块 C：AI Key 可视化配置（Key Decorator）

### 目标
将 `mykey_template.py` 中复杂的 Python 配置转为 Web 可视化管理。

### 推荐方案
采用“两层配置模型”：

1. **Web 维护结构化配置**：`data/llm_profiles.json`
2. **后端生成最终运行配置**：输出 `GenericAgent/mykey.py`

### Provider 建议字段
- `name`
- `type`（native_claude / native_oai / mixin / custom）
- `apikey`
- `apibase`
- `model`
- `proxy`
- `thinking_type`
- `reasoning_effort`
- `max_tokens`
- `connect_timeout`
- `read_timeout`
- `enabled`

### Mixin 建议字段
- `name`
- `llm_nos`
- `fallback_order`
- `retry_policy`
- `cooldown`

### 功能点
- 新增 / 编辑 / 删除 provider
- 新增 / 编辑 / 删除 mixin
- 基础模式 / 高级模式切换
- 测试连接
- 保存前校验
- 生成 `mykey.py`
- 备份旧 `mykey.py`
- 脱敏显示 key

### API 草案
- `GET /api/keys/providers`
- `POST /api/keys/providers`
- `PUT /api/keys/providers/{name}`
- `DELETE /api/keys/providers/{name}`
- `GET /api/keys/mixins`
- `POST /api/keys/test`
- `POST /api/keys/generate-mykey`
- `POST /api/keys/backup`

### 安全要求
- 日志中不得打印完整 key
- 前端默认掩码显示
- 导出前必须校验 schema
- 写入前自动备份

---

## 4.4 模块 D：聊天桥接（Chat Bridge）

### 目标
把当前 Echo 聊天升级为真实 GenericAgent 交互入口。

### 分期目标
#### MVP
- 单 agent 单会话
- 文本消息发送
- 返回真实 agent 输出
- 保存基本历史

#### 第二阶段
- 多 agent 切换
- 流式响应
- 工具执行中间状态展示
- 历史会话恢复

### API / WS 草案
- `WS /ws/{session_id}`
- `GET /api/chat/sessions`
- `POST /api/chat/sessions`
- `GET /api/chat/sessions/{id}/messages`

### 设计说明
优先做桥接层，不急于重写 GenericAgent 内部会话机制。

---

## 4.5 模块 E：系统管理与运维

### 功能点
- 显示 GenericAgent 路径
- 显示 Python 环境信息
- 显示运行中的 agent 数量
- 查看系统日志
- 下载日志
- 备份 / 恢复配置
- 重启 Web 后端

### API 草案
- `GET /api/system/info`
- `GET /api/system/health`
- `GET /api/system/logs`
- `POST /api/system/backup`
- `POST /api/system/restore`

---

## 5. 页面信息架构

建议从当前单一聊天页升级为控制台布局。

### 5.1 页面列表
1. **仪表盘**
   - 系统状态
   - 最新版本信息
   - 运行中 agent 数
   - 最近错误日志

2. **聊天工作台**
   - 会话列表
   - 消息区
   - agent 选择
   - 参数面板

3. **多 Agent 管理**
   - agent 表格
   - 状态灯
   - 启停按钮
   - 日志弹窗

4. **AI Key 配置**
   - provider 列表
   - mixin 配置
   - 测试连接
   - 生成配置

5. **代码更新**
   - repo 状态
   - 更新预览
   - pull 操作
   - 重启相关服务

6. **系统设置**
   - 路径配置
   - 默认 agent
   - 备份恢复
   - 安全选项

---

## 6. 数据模型建议

## 6.1 agents.json

```json
[
  {
    "id": "default",
    "name": "默认Agent",
    "workdir": "/path/to/GenericAgent",
    "startup_cmd": "python agentmain.py",
    "port": 8501,
    "llm_profile": "claude_main",
    "frontend_type": "streamlit",
    "env": {},
    "auto_start": false,
    "status": "stopped"
  }
]
```

## 6.2 llm_profiles.json

```json
{
  "providers": [
    {
      "name": "claude_main",
      "type": "native_claude",
      "apikey": "***",
      "apibase": "https://api.anthropic.com",
      "model": "claude-sonnet-4-5",
      "enabled": true
    }
  ],
  "mixins": []
}
```

## 6.3 app_settings.json

```json
{
  "genericagent_root": "/vol1/1000/开发/NAS/GenericAgent",
  "default_agent_id": "default",
  "auto_backup_before_write": true,
  "auto_restart_after_update": false
}
```

---

## 7. 开发阶段与优先级

## Phase 0：项目骨架重构

### 目标
从聊天 Demo 升级为控制台骨架。

### 任务
- [ ] 重构前端为菜单式布局
- [ ] 后端拆分 `api / decorators / services / core`
- [ ] 增加统一数据目录 `data/`
- [ ] 增加基础 schema 校验与日志工具

### 交付物
- 可扩展项目结构
- 控制台基础 UI
- 基础健康检查接口

---

## Phase 1：先交付管理能力（最高优先级）

### 目标
让系统先“能管”。

### 任务
- [ ] 实现 `GET /api/repo/status`
- [ ] 实现检查更新与 pull
- [ ] 实现 agent 列表 / 新增 / 编辑
- [ ] 实现 agent 启停与日志查看
- [ ] 前端完成“代码更新”“多 Agent 管理”页面

### 交付物
- Web 代码更新按钮
- 多 agent 管理页
- 日志查看能力

---

## Phase 2：AI Key 可视化配置

### 目标
让用户不再手改 `mykey.py`。

### 任务
- [ ] 定义 `llm_profiles.json` schema
- [ ] 实现 provider / mixin CRUD
- [ ] 实现 key 脱敏显示
- [ ] 实现测试连接
- [ ] 实现 `mykey.py` 生成器
- [ ] 实现备份恢复

### 交付物
- AI key 管理页
- 自动生成 `mykey.py`
- 配置备份机制

---

## Phase 3：聊天真实接入

### 目标
让系统开始“能用”。

### 任务
- [ ] 替换 Echo 为真实桥接
- [ ] 接入单 agent 聊天
- [ ] 保存会话历史
- [ ] 支持流式展示
- [ ] 增加 agent 切换

### 交付物
- 可用聊天工作台
- 基础会话管理

---

## Phase 4：系统化运维增强

### 目标
适合 NAS 持续运行与发布。

### 任务
- [ ] Docker Compose 完善卷映射
- [ ] 数据目录持久化
- [ ] 增加配置备份下载
- [ ] GitHub Actions 完善镜像发布
- [ ] 增加错误日志与健康检查

### 交付物
- NAS 可持续运行版本
- 稳定部署文档

---

## 8. MVP 建议顺序

如需尽快做出第一个可用版本，建议顺序如下：

1. 控制台布局改造
2. Repo 状态展示
3. 一键更新 GenericAgent
4. 多 agent 配置列表
5. agent 启停 + 日志
6. AI key 可视化配置
7. 生成 `mykey.py`
8. 聊天桥接

---

## 9. 风险与约束

### 9.1 技术风险
- GenericAgent 当前入口较分散，聊天桥接接入点需要进一步确认
- `mykey.py` 为 Python 配置，生成器必须保证语法正确
- 多 agent 并发运行时需处理端口冲突、孤儿进程、日志切分

### 9.2 运维风险
- Git pull 可能受到本地改动影响
- 更新后可能需要重启相关服务才能生效
- NAS 环境下需确认文件权限、路径挂载、Docker 网络

### 9.3 控制措施
- 所有修改型操作先备份
- 所有高风险按钮加确认弹窗
- 所有写操作记录审计日志
- 所有关键路径改为可配置项

---

## 10. 版本里程碑

### v0.2
- 控制台布局完成
- Repo 状态展示
- 更新按钮可用

### v0.3
- 多 agent 管理可用
- agent 启停与日志可用

### v0.4
- AI key 页面可用
- 可生成 `mykey.py`

### v0.5
- 聊天桥接上线
- 基础会话功能可用

### v1.0
- NAS 稳定部署版
- 备份 / 回滚 / 运维能力完善

---

## 11. 本计划的最终结论

本项目的正确方向不是“重写 GenericAgent”，而是：

> **将 ga_web_version 建设为 GenericAgent 的 Web 装饰器控制台。**

优先主线为：

1. **先做管理层**：更新、启停、日志、多 agent
2. **再做配置层**：AI key 可视化、生成 `mykey.py`
3. **最后做使用层**：真实聊天接入、会话管理

该路径能够最大限度复用 GenericAgent 现有能力，同时快速提供 Web 管理价值。
