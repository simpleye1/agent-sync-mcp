#!/usr/bin/env python3
"""
Mock implementation of Task Manager client for testing
"""

from typing import Dict, Any

# Import from local modules
import sys
from pathlib import Path
models_path = Path(__file__).parent.parent / "models"
sys.path.insert(0, str(models_path))
from models import TaskUpdate

# Import from local modules
import sys
from pathlib import Path
clients_path = Path(__file__).parent.parent / "clients"
sys.path.insert(0, str(clients_path))

from client_interface import TaskManagerClient


class MockTaskManagerClient(TaskManagerClient):
    """Mock implementation for testing"""
    
    def __init__(self):
        self.tasks = {}
        self.sessions = {}
    
    def update_task_status(self, task_update: TaskUpdate) -> Dict[str, Any]:
        """Mock update task status"""
        task_data = task_update.to_dict()
        self.tasks[task_update.task_id] = task_data
        self.sessions[task_update.session_id] = task_data
        
        return {
            "success": True,
            "message": "Task status updated successfully (mock)",
            "data": task_data
        }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Mock get task status"""
        if task_id in self.tasks:
            return {
                "success": True,
                "data": self.tasks[task_id]
            }
        else:
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
    
    def get_task_history(self, task_id: str) -> Dict[str, Any]:
        """Mock get task complete history"""
        if task_id in self.tasks:
            # Mock complete history including current status and logs
            history = {
                "task_info": self.tasks[task_id],
                "status_history": [
                    {
                        "id": 1,
                        "status": "running",
                        "current_action": "Started task",
                        "progress_percentage": 0,
                        "message": "Task initialized",
                        "created_at": "2024-12-30T10:00:00Z"
                    },
                    {
                        "id": 2,
                        "status": self.tasks[task_id]["status"],
                        "current_action": self.tasks[task_id]["current_action"],
                        "progress_percentage": self.tasks[task_id]["progress_percentage"],
                        "message": self.tasks[task_id]["message"],
                        "created_at": self.tasks[task_id]["timestamp"]
                    }
                ],
                "logs": [
                    {
                        "id": 1,
                        "log_level": "INFO",
                        "log_message": "Task started successfully",
                        "created_at": "2024-12-30T10:00:00Z"
                    },
                    {
                        "id": 2,
                        "log_level": "INFO",
                        "log_message": "Task processing in progress",
                        "created_at": "2024-12-30T10:01:00Z"
                    }
                ]
            }
            
            return {
                "success": True,
                "data": history
            }
        else:
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Mock health check"""
        return {
            "success": True,
            "message": "Task Manager service is healthy (mock)",
            "config": {
                "type": "mock",
                "tasks_count": len(self.tasks),
                "sessions_count": len(self.sessions)
            }
        }