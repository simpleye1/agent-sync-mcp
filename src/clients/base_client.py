#!/usr/bin/env python3
"""
Base client interface for Task Manager clients
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

from src.models import TaskUpdate


class TaskManagerClientBase(ABC):
    """Abstract base class defining the Task Manager client interface"""
    
    @abstractmethod
    def update_task_status(self, task_update: TaskUpdate, id_type: str = "session_id") -> Dict[str, Any]:
        """Update task status
        
        Args:
            task_update: Task update data
            id_type: Identifier type, either "session_id" or "task_id"
            
        Returns:
            Dict with 'success' bool and either 'message' or 'error'
        """
        pass
    
    @abstractmethod
    def get_task_status(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Get current task status
        
        Args:
            identifier: Task identifier (session_id or task_id)
            id_type: Identifier type, either "session_id" or "task_id"
            
        Returns:
            Dict with 'success' bool and either 'data' or 'error'
        """
        pass
    
    @abstractmethod
    def get_task_history(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Get complete task history
        
        Args:
            identifier: Task identifier (session_id or task_id)
            id_type: Identifier type, either "session_id" or "task_id"
            
        Returns:
            Dict with 'success' bool and either 'data' or 'error'
        """
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Check service health
        
        Returns:
            Dict with 'success' bool and health information
        """
        pass
