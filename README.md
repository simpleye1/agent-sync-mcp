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

## Quick Start

### Option 1: Direct Python Execution

#### 1. Install Dependencies
```bash
pip install fastmcp requests
```

#### 2. Configure Environment Variables
```bash
export TASK_MANAGER_HOST=localhost
export TASK_MANAGER_PORT=8080
export TASK_MANAGER_TIMEOUT=30
```

#### 3. Start MCP Server
```bash
python3 agent_sync_mcp.py
```

#### 4. Configure in Claude Code CLI
Add to Claude Code CLI configuration file:
```json
{
  "mcpServers": {
    "agent-status": {
      "command": "python3",
      "args": ["/path/to/your/agent_sync_mcp.py"],
      "env": {
        "TASK_MANAGER_HOST": "localhost",
        "TASK_MANAGER_PORT": "8080",
        "TASK_MANAGER_TIMEOUT": "30"
      }
    }
  }
}
```

### Option 2: Docker Container

#### 1. Build Docker Image
```bash
chmod +x build-docker.sh
./build-docker.sh
```

#### 2. Add to Claude Desktop
```bash
claude mcp add agent-sync -s user\
  --env "TASK_MANAGER_HOST=localhost" \
  --env "TASK_MANAGER_PORT=8080" \
  --env "TASK_MANAGER_TIMEOUT=30" \
  --env "USE_MOCK_CLIENT=false" \
  -- docker run -i --rm \
    -e TASK_MANAGER_HOST \
    -e TASK_MANAGER_PORT \
    -e TASK_MANAGER_TIMEOUT \
    -e USE_MOCK_CLIENT \
    agent-sync-mcp:latest
```

#### 3. Add to Claude Desktop (Mock Mode for Testing)
```bash
claude mcp add agent-sync-mock -s user\
  --env "USE_MOCK_CLIENT=true" \
  -- docker run -i --rm \
    -e USE_MOCK_CLIENT \
    agent-sync-mcp:latest
```

#### 4. Manual Docker Run (for testing)
```bash
# Production mode
docker run -i --rm \
  -e TASK_MANAGER_HOST=localhost \
  -e TASK_MANAGER_PORT=8080 \
  -e TASK_MANAGER_TIMEOUT=30 \
  -e USE_MOCK_CLIENT=false \
  agent-sync-mcp:latest

# Mock mode for testing
docker run -i --rm \
  -e USE_MOCK_CLIENT=true \
  agent-sync-mcp:latest
```

## Project Structure

```
├── agent_sync_mcp.py            # Main entry point
├── src/                         # Source code
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── models.py           # TaskStatus, TaskUpdate
│   ├── clients/                 # Client implementations
│   │   ├── __init__.py
│   │   ├── client_interface.py  # Abstract interface
│   │   ├── http_client.py      # HTTP implementation
│   │   ├── mock_client.py      # Mock implementation
│   │   └── client_factory.py   # Factory method
│   └── server/                  # MCP server
│       ├── __init__.py
│       └── mcp_tools.py        # FastMCP tools
├── tests/                       # Test files
│   └── simple_test.py          # Functionality tests
├── docs/                        # Documentation
│   ├── README.md               # Detailed documentation
│   └── MANUAL_TESTING_GUIDE.md # Testing guide
├── Dockerfile                   # Docker configuration
├── .dockerignore               # Docker ignore file
├── build-docker.sh             # Docker build script
├── requirements.txt             # Dependencies
└── mcp-config-example.json     # Configuration example
```

### 4. get_task_history
Get complete task history
```python
get_task_history(task_id="task-001")
```

### 5. health_check
Check Task Manager service health status
```python
health_check()
```

## Testing

### Automated Testing
```bash
python3 tests/simple_test.py
```

### Mock Client Testing
```bash
export USE_MOCK_CLIENT=true
python3 tests/simple_test.py
```

## Documentation

- [Detailed Documentation](docs/README.md)
- [Manual Testing Guide](docs/MANUAL_TESTING_GUIDE.md)

## Environment Variables

| Variable Name | Default Value | Description |
|---------------|---------------|-------------|
| `TASK_MANAGER_HOST` | `localhost` | Task Manager service host |
| `TASK_MANAGER_PORT` | `8080` | Task Manager service port |
| `TASK_MANAGER_TIMEOUT` | `30` | API call timeout (seconds) |
| `USE_MOCK_CLIENT` | `false` | Use mock client for testing |

## License

MIT License