# Task Manager MCP

Nova Agent 进度汇报 MCP 服务器。

## MCP Tools

| Tool | 用途 |
|------|------|
| `update_execution_session` | 更新 execution 的 session_id |
| `create_step` | 创建步骤，返回 step_id |
| `update_step` | 更新步骤状态/消息 |
| `health_check` | 健康检查 |

## 使用示例

```python
# 1. 注册 session
update_execution_session(execution_id="exec-123", session_id="nova-001")

# 2. 创建步骤
result = create_step(execution_id="exec-123", step_name="analyzing")
step_id = result["step_id"]

# 3. 完成步骤
update_step(execution_id="exec-123", step_id=step_id, status="completed")
```

## Step Status

- `running` - 执行中
- `completed` - 完成
- `failed` - 失败
- `skipped` - 跳过

## 配置

```bash
TASK_MANAGER_HOST=localhost
TASK_MANAGER_PORT=8080
TASK_MANAGER_TIMEOUT=30
USE_MOCK_CLIENT=false
```

## 运行

```bash
pip install -r requirements.txt
python task_manager_mcp.py
```
