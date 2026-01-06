#!/usr/bin/env python3
"""
Mock implementation of Task Manager client for testing
"""

from typing import Dict, Any, Optional

from src.models import TaskUpdate
from src.clients.base_client import TaskManagerClientBase


class MockTaskManagerClient(TaskManagerClientBase):
    """Mock implementation for testing"""
    
    def __init__(self):
        self.tasks = {}  # task_id -> task_data
        self.session_to_task = {}  # session_id -> task_id
        self._task_counter = 0

    def update_task(self, task_id: str, task_update: TaskUpdate) -> Dict[str, Any]:
        """Update task by task_id"""
        task_data = task_update.to_dict()
        task_data['task_id'] = task_id
        self.tasks[task_id] = task_data
        self.session_to_task[task_update.session_id] = task_id
        
        return {
            "success": True,
            "message": "Task updated successfully (mock)",
            "task_id": task_id
        }
    
    def get_task(self, session_id: Optional[str] = None, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get task by session_id or task_id"""
        # Find by task_id first
        if task_id and task_id in self.tasks:
            return {"success": True, "data": self.tasks[task_id]}
        
        # Find by session_id
        if session_id and session_id in self.session_to_task:
            tid = self.session_to_task[session_id]
            if tid in self.tasks:
                return {"success": True, "data": self.tasks[tid]}
        
        return {"success": False, "error": "Task not found"}
    
    def get_task_history(self, task_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get task history by task_id"""
        if task_id not in self.tasks:
            return {"success": False, "error": f"Task '{task_id}' not found"}
        
        task = self.tasks[task_id]
        history = {
            "task_info": task,
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
                    "status": task["status"],
                    "current_action": task["current_action"],
                    "progress_percentage": task["progress_percentage"],
                    "message": task["message"],
                    "created_at": task["timestamp"]
                }
            ],
            "logs": [
                {"id": 1, "log_level": "INFO", "log_message": "Task started", "created_at": "2024-12-30T10:00:00Z"},
                {"id": 2, "log_level": "INFO", "log_message": "Task processing", "created_at": "2024-12-30T10:01:00Z"}
            ]
        }
        
        return {"success": True, "data": history}
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        return {
            "success": True,
            "message": "Task Manager service is healthy (mock)",
            "config": {"type": "mock", "tasks_count": len(self.tasks)}
        }
