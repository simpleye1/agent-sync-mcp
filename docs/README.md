# Agent Status MCP Server

An MCP (Model Context Protocol) server for tracking Claude agent execution status.

## Features

- 📊 Real-time agent execution status tracking
- 📝 Task progress and status recording
- 🎫 Jira ticket number integration
- 🌐 Data storage via Task Manager service API calls
- 🔍 Health check and error handling
- ⚙️ Environment variable configuration
- 🏗️ Feign-like client interface architecture

## Data Model

### Task Status
- `running`: Currently executing
- `success`: Execution successful
- `failed`: Execution failed

### Data Relationships
- **Session**: Session identifier, one-to-one relationship with task_id
- **Task**: Specific task containing Jira ticket number
- **Action**: Specific execution steps within a task

### Data Structure
```python
@dataclass
class TaskUpdate:
    session_id: str            # Session unique identifier (one-to-one with task_id)
    task_id: str               # Task unique identifier
    jira_ticket: str           # Jira ticket number
    status: TaskStatus         # Task status
    current_action: str        # Current action description
    progress_percentage: float # Progress percentage (0-100)
    message: str               # Status description
    details: Dict[str, Any]    # Additional details
    timestamp: str             # Timestamp
```

## Quick Start

### 1. Install Dependencies
```bash
pip install fastmcp requests
```

### 2. Configure Environment Variables
```bash
export TASK_MANAGER_HOST=localhost
export TASK_MANAGER_PORT=8080
export TASK_MANAGER_TIMEOUT=30
```

### 3. Start MCP Server
```bash
python3 agent_status_mcp.py
```

### 4. Configure in Claude Code CLI
Add to Claude Code CLI configuration file:
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
      }
    }
  }
}
```

### 5. Use in Claude Agent
```python
# In your Claude Agent code
await update_task_status(
    session_id="session-001",
    task_id="task-001",
    jira_ticket="PROJ-123",
    status="running",
    current_action="Writing code",
    message="Writing new feature code",
    progress_percentage=60,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

## MCP Tools

### 1. update_task_status
Update task status
```python
update_task_status(
    session_id="session-001",
    task_id="task-001",
    jira_ticket="PROJ-123",
    status="running",
    current_action="Writing code",
    message="Writing new feature",
    progress_percentage=60.0,
    details={
        "files_modified": ["src/main.py"],
        "lines_added": 45
    }
)
```

### 2. get_task_status
Get task status
```python
get_task_status(task_id="task-001")
```

### 3. get_session_status
Get session status
```python
get_session_status(session_id="session-001")
```

### 4. list_running_tasks
List all running tasks
```python
list_running_tasks()
```

### 5. health_check
Check Task Manager service health status
```python
health_check()
```

## Client Architecture

The system uses a modular Feign-like client interface pattern:

### Module Structure
```
├── models.py              # Data models (TaskStatus, TaskUpdate)
├── client_interface.py    # Abstract client interface
├── http_client.py         # HTTP implementation
├── mock_client.py         # Mock implementation for testing
├── client_factory.py      # Factory for creating clients
├── mcp_tools.py          # MCP tools implementation
└── agent_status_mcp.py   # Main entry point
```

### TaskManagerClient Interface
```python
class TaskManagerClient(ABC):
    @abstractmethod
    def update_task_status(self, task_update: TaskUpdate) -> Dict[str, Any]: pass
    
    @abstractmethod
    def get_task_status(self, task_id: str) -> Dict[str, Any]: pass
    
    @abstractmethod
    def get_session_status(self, session_id: str) -> Dict[str, Any]: pass
    
    @abstractmethod
    def list_running_tasks(self) -> Dict[str, Any]: pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]: pass
```

### Implementations
- **HttpTaskManagerClient**: HTTP implementation for production use
- **MockTaskManagerClient**: Mock implementation for testing
- **Factory method**: `create_task_manager_client()` creates appropriate client based on environment

## Task Manager API

MCP server communicates with Task Manager service through the following API endpoints:

- `POST /api/tasks/status` - Update task status
- `GET /api/tasks/{task_id}` - Get task status
- `GET /api/sessions/{session_id}` - Get session status
- `GET /api/tasks?status=running` - List running tasks
- `GET /api/health` - Health check

## Environment Variable Configuration

| Variable Name | Default Value | Description |
|---------------|---------------|-------------|
| `TASK_MANAGER_HOST` | `localhost` | Task Manager service host |
| `TASK_MANAGER_PORT` | `8080` | Task Manager service port |
| `TASK_MANAGER_TIMEOUT` | `30` | API call timeout (seconds) |
| `USE_MOCK_CLIENT` | `false` | Use mock client for testing |

## Project Files

| File | Description |
|------|-------------|
| `agent_status_mcp.py` | **Main entry point** - MCP server startup script |
| `models.py` | **Data models** - TaskStatus enum and TaskUpdate dataclass |
| `client_interface.py` | **Client interface** - Abstract TaskManagerClient interface |
| `http_client.py` | **HTTP client** - HTTP implementation for production use |
| `mock_client.py` | **Mock client** - Mock implementation for testing |
| `client_factory.py` | **Client factory** - Factory method for creating clients |
| `mcp_tools.py` | **MCP tools** - FastMCP tools implementation |
| `simple_test.py` | **Test script** - Test Task Manager client functionality |
| `requirements.txt` | **Dependencies** - Python package dependencies |
| `mcp-config-example.json` | **Configuration example** - Claude Code CLI MCP configuration template |
| `README.md` | **Project documentation** - Complete usage instructions |
| `MANUAL_TESTING_GUIDE.md` | **Manual testing guide** - Terminal JSON-RPC interaction instructions |

## Testing

### Automated Testing
Run client tests:
```bash
python3 simple_test.py
```

### Mock Client Testing
Use mock client for testing without Task Manager service:
```bash
export USE_MOCK_CLIENT=true
python3 simple_test.py
```

### Manual Terminal Testing
Detailed manual testing guide: [MANUAL_TESTING_GUIDE.md](MANUAL_TESTING_GUIDE.md)

## Future Plans

- [ ] Task Manager service implementation
- [ ] Web interface monitoring dashboard
- [ ] Status change notifications (Webhook, Email)
- [ ] Performance metrics statistics
- [ ] Multi-session collaboration status tracking
- [ ] Real-time status push (WebSocket)

## License

MIT License