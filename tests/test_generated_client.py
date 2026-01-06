#!/usr/bin/env python3
"""
Test generated HTTP client
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.models import TaskUpdate, TaskStatus
from src.clients import create_task_manager_client


def test_generated_client():
    """Test the HTTP client"""
    print("Testing HTTP Client...")
    
    client = create_task_manager_client()
    print(f"Created client: {type(client).__name__}")
    
    # Test health check
    print("\n1. Testing health check...")
    health_result = client.health_check()
    print(f"Health check result: {health_result}")
    
    # Create a test task update
    task_update = TaskUpdate(
        session_id="test_session_123",
        jira_ticket="TEST-456",
        status=TaskStatus.RUNNING,
        current_action="Testing HTTP client",
        progress_percentage=50.0,
        message="Testing the HTTP client",
        details={"test": True, "client_type": "http"},
        timestamp="2024-12-30T15:30:00Z"
    )
    
    # Test update task (by task_id)
    print("\n2. Testing update task...")
    update_result = client.update_task("test_task_789", task_update)
    print(f"Update result: {update_result}")
    
    # Test get task (by session_id)
    print("\n3. Testing get task by session_id...")
    status_result = client.get_task(session_id="test_session_123")
    print(f"Status result: {status_result}")
    
    # Test get task (by task_id)
    print("\n4. Testing get task by task_id...")
    status_result = client.get_task(task_id="test_task_789")
    print(f"Status result: {status_result}")
    
    # Test get task history
    print("\n5. Testing get task history...")
    history_result = client.get_task_history("test_task_789")
    print(f"History result: {history_result}")
    
    print("\nHTTP client test completed!")


def test_factory_selection():
    """Test that factory correctly selects different clients"""
    print("\nTesting Factory Client Selection...")
    
    # Test default client (HTTP client)
    os.environ.pop('USE_MOCK_CLIENT', None)
    client = create_task_manager_client()
    print(f"Default client: {type(client).__name__}")
    
    # Test mock client
    os.environ['USE_MOCK_CLIENT'] = 'true'
    client = create_task_manager_client()
    print(f"Mock client: {type(client).__name__}")
    
    # Reset to default
    os.environ.pop('USE_MOCK_CLIENT', None)
    
    print("Factory selection test completed!")


if __name__ == "__main__":
    test_factory_selection()
    test_generated_client()
