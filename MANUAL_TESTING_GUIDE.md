# 🧪 手动测试指南

## 快速测试

### 自动化测试
```bash
python3 simple_test.py
```

### 手动终端交互

1. **启动服务器**：
   ```bash
   python3 mcp_server_clean.py
   ```

2. **在新终端中按顺序输入**：

   **初始化**：
   ```json
   {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
   ```

   **发送初始化完成**：
   ```json
   {"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
   ```

   **健康检查**：
   ```json
   {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"health_check","arguments":{}}}
   ```

   **更新任务状态**：
   ```json
   {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"update_task_status","arguments":{"session_id":"test-session-001","task_id":"test-task-001","jira_ticket":"PROJ-123","status":"running","current_action":"测试任务","message":"正在测试 MCP 功能","progress_percentage":50}}}
   ```

   **获取任务状态**：
   ```json
   {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_task_status","arguments":{"task_id":"test-task-001"}}}
   ```

   **获取会话状态**：
   ```json
   {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_session_status","arguments":{"session_id":"test-session-001"}}}
   ```

## 可用工具

- `update_task_status` - 更新任务状态
- `get_task_status` - 获取任务状态
- `get_session_status` - 获取会话状态
- `list_running_tasks` - 列出运行中的任务
- `health_check` - 健康检查

## 存储结构说明

- **新架构**: 通过 API 调用 Task Manager 服务，不再使用本地存储
- **任务状态**: `running`, `success`, `failed`
- **数据关系**: session_id 和 task_id 一对一关系
- **Jira 集成**: 每个任务关联一个 Jira 卡号

## 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `TASK_MANAGER_HOST` | `localhost` | Task Manager 服务主机 |
| `TASK_MANAGER_PORT` | `8080` | Task Manager 服务端口 |
| `TASK_MANAGER_TIMEOUT` | `30` | API 调用超时时间（秒） |