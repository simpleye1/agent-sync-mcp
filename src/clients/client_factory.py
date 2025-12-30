#!/usr/bin/env python3
"""
Factory for creating Task Manager clients
"""

import os

# Import from local modules
import sys
from pathlib import Path
clients_path = Path(__file__).parent.parent / "clients"
sys.path.insert(0, str(clients_path))

from client_interface import TaskManagerClient
from http_client import HttpTaskManagerClient
from mock_client import MockTaskManagerClient


def create_task_manager_client() -> TaskManagerClient:
    """Factory method to create Task Manager client"""
    # Use mock client if in test mode
    if os.getenv('USE_MOCK_CLIENT', 'false').lower() == 'true':
        return MockTaskManagerClient()
    else:
        return HttpTaskManagerClient()