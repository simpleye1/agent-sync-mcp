# 🧪 Manual Testing Guide

## Quick Test

### Automated Testing
```bash
python3 simple_test.py
```

### Manual Terminal Interaction

1. **Start server**:
   ```bash
   python3 agent_status_mcp.py
   ```

2. **Input in new terminal in sequence**:

   **Initialize**:
   ```json
   {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
   ```

   **Send initialization complete**:
   ```json
   {"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
   ```

   **Health check**:
   ```json
   {"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"health_check","arguments":{}}}
   ```

   **Update task status**:
   ```json
   {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"update_task_status","arguments":{"session_id":"test-session-001","task_id":"test-task-001","jira_ticket":"PROJ-123","status":"running","current_action":"Testing task","message":"Testing MCP functionality","progress_percentage":50}}}
   ```

   **Get task status**:
   ```json
   {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"get_task_status","arguments":{"task_id":"test-task-001"}}}
   ```

   **Get session status**:
   ```json
   {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_session_status","arguments":{"session_id":"test-session-001"}}}
   ```

## Available Tools

- `update_task_status` - Update task status
- `get_task_status` - Get task status
- `get_session_status` - Get session status
- `list_running_tasks` - List running tasks
- `health_check` - Health check

## Architecture Description

- **New architecture**: Data storage via API calls to Task Manager service, no local storage
- **Task status**: `running`, `success`, `failed`
- **Data relationship**: session_id and task_id have one-to-one relationship
- **Jira integration**: Each task is associated with a Jira ticket number

## Environment Variable Configuration

| Variable Name | Default Value | Description |
|---------------|---------------|-------------|
| `TASK_MANAGER_HOST` | `localhost` | Task Manager service host |
| `TASK_MANAGER_PORT` | `8080` | Task Manager service port |
| `TASK_MANAGER_TIMEOUT` | `30` | API call timeout (seconds) |
| `USE_MOCK_CLIENT` | `false` | Use mock client for testing |

## Client Architecture

The system uses a Feign-like client interface pattern:

- **TaskManagerClient**: Abstract interface defining all API operations
- **HttpTaskManagerClient**: HTTP implementation for production use
- **MockTaskManagerClient**: Mock implementation for testing
- **Factory method**: `create_task_manager_client()` creates appropriate client based on environment