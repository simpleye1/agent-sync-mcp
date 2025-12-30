# Agent Status MCP Server

一个用于跟踪 Claude agent 执行状态的 MCP (Model Context Protocol) 服务器。

## 功能特性

- 📊 实时跟踪 agent 执行状态
- 📝 记录任务进度和状态
- 🎫 支持 Jira 卡号关联
- 🌐 通过 API 调用 Task Manager 服务
- 🔍 健康检查和错误处理
- ⚙️ 环境变量配置

## 数据模型

### 任务状态 (TaskStatus)
- `running`: 正在执行
- `success`: 执行成功
- `failed`: 执行失败

### 数据关系
- **Session**: 会话标识符，与 task_id 一对一关系
- **Task**: 具体任务，包含 Jira 卡号
- **Action**: 任务中的具体执行步骤

### 数据结构
```python
@dataclass
class TaskUpdate:
    session_id: str            # 会话唯一标识 (与 task_id 一对一)
    task_id: str               # 任务唯一标识
    jira_ticket: str           # Jira 卡号
    status: TaskStatus         # 任务状态
    current_action: str        # 当前动作描述
    progress_percentage: float # 进度百分比 (0-100)
    message: str               # 状态描述
    details: Dict[str, Any]    # 额外详情
    timestamp: str             # 时间戳
```

## 快速开始

### 1. 安装依赖
```bash
pip install fastmcp requests
```

### 2. 配置环境变量
```bash
export TASK_MANAGER_HOST=localhost
export TASK_MANAGER_PORT=8080
export TASK_MANAGER_TIMEOUT=30
```

### 3. 启动 MCP 服务器
```bash
python3 agent_status_mcp.py
```

### 4. 在 MCP 客户端中使用
将以下配置添加到你的 MCP 配置文件中：
```json
{
  "mcpServers": {
    "agent-status": {
      "command": "python3",
      "args": ["/path/to/your/agent_status_mcp.py"],
      "env": {
        "TASK_MANAGER_HOST": "localhost",
        "TASK_MANAGER_PORT": "8080",
        "TASK_MANAGER_TIMEOUT": "30"
      },
      "disabled": false,
      "autoApprove": [
        "update_task_status",
        "get_task_status",
        "get_session_status",
        "list_running_tasks",
        "health_check"
      ]
    }
  }
}
```

### 5. 在 Claude Agent 中使用
```python
# 在你的 Claude Agent 代码中
await update_task_status(
    session_id="session-001",
    task_id="task-001",
    jira_ticket="PROJ-123",
    status="running",
    current_action="编写代码",
    message="正在编写新功能代码",
    progress_percentage=60,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

## MCP 工具

### 1. update_task_status
更新任务状态
```python
update_task_status(
    session_id="session-001",
    task_id="task-001",
    jira_ticket="PROJ-123",
    status="running",
    current_action="编写代码",
    message="正在编写新功能",
    progress_percentage=60.0,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

### 2. get_task_status
获取任务状态
```python
get_task_status(task_id="task-001")
```

### 3. get_session_status
获取会话状态
```python
get_session_status(session_id="session-001")
```

### 4. list_running_tasks
列出所有运行中的任务
```python
list_running_tasks()
```

### 5. health_check
检查 Task Manager 服务健康状态
```python
health_check()
```

## Task Manager API

MCP 服务器通过以下 API 端点与 Task Manager 服务通信：

- `POST /api/tasks/status` - 更新任务状态
- `GET /api/tasks/{task_id}` - 获取任务状态
- `GET /api/sessions/{session_id}` - 获取会话状态
- `GET /api/tasks?status=running` - 列出运行中的任务
- `GET /api/health` - 健康检查

## 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `TASK_MANAGER_HOST` | `localhost` | Task Manager 服务主机 |
| `TASK_MANAGER_PORT` | `8080` | Task Manager 服务端口 |
| `TASK_MANAGER_TIMEOUT` | `30` | API 调用超时时间（秒） |
获取存储信息和统计
```python
get_storage_info()
```

## 存储结构

默认存储路径：`~/.task-manager/agent-status/`

可通过环境变量 `AGENT_STATUS_STORAGE_PATH` 配置存储路径：
```bash
export AGENT_STATUS_STORAGE_PATH="/custom/path/to/storage"
python3 start_mcp_server.py
```

新的层次化存储结构（每个 agent 下有自己的 tasks）：
```
~/.task-manager/agent-status/
└── agents/
    ├── claude-coder-001/
    │   ├── current_task.json    # 当前任务信息
    │   └── tasks/               # 该 agent 的所有任务
    │       ├── task-001.json
    │       ├── task-002.json
    │       └── task-003.json
    └── claude-coder-002/
        ├── current_task.json
        └── tasks/
            ├── task-004.json
            └── task-005.json
```

### 任务文件格式 (agents/{agent_id}/tasks/{task_id}.json)
```json
{
  "task_id": "task-001",
  "agent_id": "claude-coder-001",
  "status": "running",
  "current_action": "编写代码",
  "progress_percentage": 60.0,
  "message": "正在编写新功能代码",
  "details": {
    "files_modified": ["src/main.py"],
    "lines_added": 45
  },
  "created_at": "2024-12-29T14:30:22Z",
  "updated_at": "2024-12-29T14:35:22Z"
}
```

### Agent 当前任务文件格式 (agents/{agent_id}/current_task.json)
```json
{
  "agent_id": "claude-coder-001",
  "current_task": {
    // 当前任务的完整信息
  },
  "last_updated": "2024-12-29T14:35:22Z"
}
```

## 项目文件说明

| 文件 | 说明 |
|------|------|
| `agent_status_mcp.py` | **核心文件** - MCP 服务器实现，包含 Task Manager API 客户端 |
| `simple_test.py` | **测试脚本** - 测试 Task Manager 客户端功能 |
| `requirements.txt` | **依赖文件** - Python 包依赖列表 |
| `mcp-config-example.json` | **配置示例** - MCP 配置模板 |
| `README.md` | **项目文档** - 完整的使用说明 |
| `MANUAL_TESTING_GUIDE.md` | **手动测试指南** - 终端 JSON-RPC 交互详细说明 |

## 测试

### 自动化测试
运行客户端测试：
```bash
python3 simple_test.py
```

### 手动终端测试
详细的手动测试指南请参考：[MANUAL_TESTING_GUIDE.md](MANUAL_TESTING_GUIDE.md)

## 扩展计划

- [ ] Task Manager 服务实现
- [ ] Web 界面监控面板
- [ ] 状态变更通知 (Webhook, Email)
- [ ] 性能指标统计
- [ ] 多会话协作状态跟踪
- [ ] 实时状态推送 (WebSocket)

## 许可证

MIT License