#!/usr/bin/env python3
"""
Simple functionality test
"""

import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.clients import HttpTaskManagerClient, MockTaskManagerClient
from src.models import TaskUpdate, TaskStatus


def test_http_client():
    """Test HTTP Task Manager client"""
    print("🧪 Testing HTTP Task Manager Client")
    print("="*50)
    
    client = HttpTaskManagerClient()
    print(f"✅ Client initialized: {client.base_url}")
    
    # Health check
    print("\n🔍 Health check...")
    health_result = client.health_check()
    if health_result["success"]:
        print(f"✅ Healthy: {health_result['config']}")
    else:
        print(f"❌ Unhealthy: {health_result['error']}")
        print("   (Expected if service not running)")
    
    # Create task update
    task_update = TaskUpdate(
        session_id="test-session-001",
        jira_ticket="PROJ-123",
        status=TaskStatus.RUNNING,
        current_action="Testing API",
        progress_percentage=50,
        message="Testing client",
        details={"test": True},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    # Update task
    print("\n📝 Update task...")
    result = client.update_task("task-001", task_update)
    print(f"   Result: {result}")
    
    # Get task
    print("\n📊 Get task by session_id...")
    result = client.get_task(session_id="test-session-001")
    print(f"   Result: {result}")
    
    # Get history
    print("\n📜 Get task history...")
    result = client.get_task_history("task-001")
    print(f"   Result: {result}")
    
    print("\n🎉 HTTP client test completed!")


def test_mock_client():
    """Test Mock Task Manager client"""
    print("\n🧪 Testing Mock Task Manager Client")
    print("="*50)
    
    client = MockTaskManagerClient()
    print("✅ Mock client initialized")
    
    # Health check
    print("\n🔍 Health check...")
    health_result = client.health_check()
    print(f"✅ {health_result['message']}")
    
    # Create task update
    task_update = TaskUpdate(
        session_id="mock-session-001",
        jira_ticket="MOCK-123",
        status=TaskStatus.RUNNING,
        current_action="Testing mock",
        progress_percentage=75,
        message="Mock test",
        details={"mock": True},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    # Update task
    print("\n📝 Update task...")
    result = client.update_task("mock-task-001", task_update)
    print(f"✅ {result['message']}")
    
    # Get task by session_id
    print("\n📊 Get task by session_id...")
    result = client.get_task(session_id="mock-session-001")
    if result["success"]:
        print(f"✅ Found: session={result['data']['session_id']}, status={result['data']['status']}")
    
    # Get task by task_id
    print("\n📊 Get task by task_id...")
    result = client.get_task(task_id="mock-task-001")
    if result["success"]:
        print(f"✅ Found: task_id={result['data']['task_id']}")
    
    # Get history
    print("\n📜 Get task history...")
    result = client.get_task_history("mock-task-001")
    if result["success"]:
        print(f"✅ History entries: {len(result['data']['status_history'])}")
    
    print("\n🎉 Mock client test completed!")


if __name__ == "__main__":
    test_http_client()
    test_mock_client()
