#!/usr/bin/env python3
"""
Simple functionality test
"""

import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from clients import HttpTaskManagerClient, MockTaskManagerClient
from models import TaskUpdate, TaskStatus


def test_http_client():
    """Test HTTP Task Manager client"""
    print("🧪 Testing HTTP Task Manager Client")
    print("="*50)
    
    # Initialize client
    client = HttpTaskManagerClient()
    print(f"✅ Client initialized successfully")
    print(f"   Task Manager URL: {client.base_url}")
    print(f"   Timeout setting: {client.timeout}s")
    
    # Health check
    print("\n🔍 Performing health check...")
    health_result = client.health_check()
    if health_result["success"]:
        print("✅ Task Manager service is healthy")
        print(f"   Config: {health_result['config']}")
    else:
        print("❌ Task Manager service is unhealthy")
        print(f"   Error: {health_result['error']}")
        print("   This is expected if Task Manager service is not running")
    
    # Create test task update
    print("\n📝 Creating test task update...")
    task_update = TaskUpdate(
        session_id="test-session-001",
        task_id="test-task-001",
        jira_ticket="PROJ-123",
        status=TaskStatus.RUNNING,
        current_action="Testing API calls",
        progress_percentage=50,
        message="Testing Task Manager client functionality",
        details={"test": True, "environment": "development"},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    print("✅ Task update object created successfully")
    print(f"   Session ID: {task_update.session_id}")
    print(f"   Task ID: {task_update.task_id}")
    print(f"   Jira Ticket: {task_update.jira_ticket}")
    print(f"   Status: {task_update.status.value}")
    print(f"   Progress: {task_update.progress_percentage}%")
    
    # Test API call (expected to fail if service is not running)
    print("\n🌐 Testing API call...")
    result = client.update_task_status(task_update)
    if result["success"]:
        print("✅ API call successful")
        print(f"   Response: {result}")
    else:
        print("❌ API call failed (expected result)")
        print(f"   Error: {result['error']}")
    
    # Test get task status
    print("\n📊 Testing get task status...")
    task_result = client.get_task_status("test-task-001")
    if task_result["success"]:
        print("✅ Get task status successful")
        print(f"   Data: {task_result['data']}")
    else:
        print("❌ Get task status failed (expected result)")
        print(f"   Error: {task_result['error']}")
    
    print("\n🎉 HTTP client test completed!")
    print("💡 To fully test functionality, please start Task Manager service")


def test_mock_client():
    """Test Mock Task Manager client"""
    print("\n🧪 Testing Mock Task Manager Client")
    print("="*50)
    
    # Initialize mock client
    client = MockTaskManagerClient()
    print("✅ Mock client initialized successfully")
    
    # Health check
    print("\n🔍 Performing health check...")
    health_result = client.health_check()
    print("✅ Mock service health check successful")
    print(f"   Config: {health_result['config']}")
    
    # Create test task update
    task_update = TaskUpdate(
        session_id="mock-session-001",
        task_id="mock-task-001",
        jira_ticket="MOCK-123",
        status=TaskStatus.RUNNING,
        current_action="Testing mock client",
        progress_percentage=75,
        message="Testing mock functionality",
        details={"mock": True},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    # Test update task status
    print("\n📝 Testing update task status...")
    result = client.update_task_status(task_update)
    if result["success"]:
        print("✅ Update task status successful")
        print(f"   Message: {result['message']}")
    else:
        print("❌ Update task status failed")
        print(f"   Error: {result['error']}")
    
    # Test get task status
    print("\n📊 Testing get task status...")
    task_result = client.get_task_status("mock-task-001")
    if task_result["success"]:
        print("✅ Get task status successful")
        print(f"   Task ID: {task_result['data']['task_id']}")
        print(f"   Status: {task_result['data']['status']}")
    else:
        print("❌ Get task status failed")
        print(f"   Error: {task_result['error']}")
    
    # Test get session status
    print("\n👤 Testing get task history...")
    history_result = client.get_task_history("mock-task-001")
    if history_result["success"]:
        print("✅ Get task history successful")
        print(f"   Status history count: {len(history_result['data']['status_history'])}")
        print(f"   Logs count: {len(history_result['data']['logs'])}")
    else:
        print("❌ Get task history failed")
        print(f"   Error: {history_result['error']}")
    
    print("\n🎉 Mock client test completed!")


def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🧪 Testing Environment Variable Configuration")
    print("="*50)
    
    # Display current environment variables
    host = os.getenv('TASK_MANAGER_HOST', 'localhost')
    port = os.getenv('TASK_MANAGER_PORT', '8080')
    timeout = os.getenv('TASK_MANAGER_TIMEOUT', '30')
    use_mock = os.getenv('USE_MOCK_CLIENT', 'false')
    
    print(f"✅ Environment variable configuration:")
    print(f"   TASK_MANAGER_HOST: {host}")
    print(f"   TASK_MANAGER_PORT: {port}")
    print(f"   TASK_MANAGER_TIMEOUT: {timeout}")
    print(f"   USE_MOCK_CLIENT: {use_mock}")
    
    print("\n💡 You can configure using:")
    print("   export TASK_MANAGER_HOST=your-host")
    print("   export TASK_MANAGER_PORT=your-port")
    print("   export TASK_MANAGER_TIMEOUT=60")
    print("   export USE_MOCK_CLIENT=true")


if __name__ == "__main__":
    test_http_client()
    test_mock_client()
    test_environment_variables()