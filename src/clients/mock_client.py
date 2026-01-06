#!/usr/bin/env python3
"""
Mock implementation of Task Manager client for testing
"""

from typing import Dict, Any

from src.models import TaskUpdate
from src.clients.base_client import TaskManagerClientBase


class MockTaskManagerClient(TaskManagerClientBase):
    """Mock implementation for testing"""
    
    def __init__(self):
        self.sessions = {}

    def update_task_status(self, task_update: TaskUpdate, id_type: str = "session_id") -> Dict[str, Any]:
        """Mock update task status"""
        task_data = task_update.to_dict()
        # For mock, we'll use session_id as the key regardless of id_type
        self.sessions[task_update.session_id] = task_data
        
        return {
            "success": True,
            "message": f"Task status updated successfully (mock, id_type: {id_type})"
        }
    
    def get_task_status(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Mock get task status"""
        # For mock, we'll treat identifier as session_id regardless of id_type
        if identifier in self.sessions:
            return {
                "success": True,
                "data": self.sessions[identifier]
            }
        else:
            return {
                "success": False,
                "error": f"Task with {id_type} '{identifier}' not found"
            }
    
    def get_task_history(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Mock get task complete history"""
        # For mock, we'll treat identifier as session_id regardless of id_type
        if identifier in self.sessions:
            # Mock complete history including current status and logs
            history = {
                "task_info": self.sessions[identifier],
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
                        "status": self.sessions[identifier]["status"],
                        "current_action": self.sessions[identifier]["current_action"],
                        "progress_percentage": self.sessions[identifier]["progress_percentage"],
                        "message": self.sessions[identifier]["message"],
                        "created_at": self.sessions[identifier]["timestamp"]
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
                "error": f"Task with {id_type} '{identifier}' not found"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Mock health check"""
        return {
            "success": True,
            "message": "Task Manager service is healthy (mock)",
            "config": {
                "type": "mock",
                "sessions_count": len(self.sessions)
            }
        }