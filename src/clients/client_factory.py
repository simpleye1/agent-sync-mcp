#!/usr/bin/env python3
"""
Factory for creating Task Manager clients
"""

import os

from src.clients.base_client import TaskManagerClientBase
from src.clients.mock_client import MockTaskManagerClient
from src.clients.http_client import HttpTaskManagerClient


def create_task_manager_client() -> TaskManagerClientBase:
    """Factory method to create Task Manager client
    
    Returns:
        TaskManagerClientBase: A client instance implementing the TaskManagerClientBase interface
    """
    # Use mock client if in test mode
    if os.getenv('USE_MOCK_CLIENT', 'false').lower() == 'true':
        return MockTaskManagerClient()
    
    # Default to HTTP client
    return HttpTaskManagerClient()