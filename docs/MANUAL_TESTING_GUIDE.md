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

   **List available tools**:
   ```json
   {"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
   ```

   **Health check**:
   ```json
   {"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"health_check","arguments":{}}}
   ```

   **Update task status**:
   ```json
   {"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"update_task_status","arguments":{"session_id":"test-session-001","task_id":"test-task-001","jira_ticket":"PROJ-123","status":"running","current_action":"Testing task","message":"Testing MCP functionality","progress_percentage":50}}}
   ```

   **Get task status**:
   ```json
   {"jsonrpc":"2.0","id":5,"method":"tools/call","params":{"name":"get_task_status","arguments":{"task_id":"test-task-001"}}}
   ```

   **Get task history**:
   ```json
   {"jsonrpc":"2.0","id":6,"method":"tools/call","params":{"name":"get_task_history","arguments":{"task_id":"test-task-001"}}}
   ```

## Available Tools

### 1. `update_task_status`
**Description**: Update task status and create history record

**Parameters**:
- `session_id` (string, required): Session unique identifier (one-to-one with task_id)
- `task_id` (string, required): Task unique identifier
- `jira_ticket` (string, required): Jira ticket number
- `status` (string, required): Task status (`running`/`success`/`failed`)
- `current_action` (string, required): Current action description
- `message` (string, required): Status description message
- `progress_percentage` (number, optional, default: 0.0): Progress percentage (0-100)
- `details` (object, optional): Additional task details

**Example**:
```json
{
  "session_id": "session_123",
  "task_id": "task_456",
  "jira_ticket": "PROJ-789",
  "status": "running",
  "current_action": "Processing user request",
  "message": "Started analyzing codebase",
  "progress_percentage": 25.0,
  "details": {"file_count": 15, "complexity": "medium"}
}
```

### 2. `get_task_status`
**Description**: Get current task status

**Parameters**:
- `task_id` (string, required): Task unique identifier

**Example**:
```json
{
  "task_id": "task_456"
}
```

### 3. `get_task_history`
**Description**: Get complete task history including all status changes and logs

**Parameters**:
- `task_id` (string, required): Task unique identifier

**Example**:
```json
{
  "task_id": "task_456"
}
```

### 4. `health_check`
**Description**: Check Task Manager service health status and configuration

**Parameters**: None

**Example**:
```json
{}
```

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