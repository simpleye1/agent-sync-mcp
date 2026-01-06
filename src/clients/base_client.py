#!/usr/bin/env python3
"""
Base client interface for Task Manager clients
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from src.models import TaskUpdate


class TaskManagerClientBase(ABC):
    """Abstract base class defining the Task Manager client interface"""
    
    @abstractmethod
    def update_task(self, task_id: str, task_update: TaskUpdate) -> Dict[str, Any]:
        """Update task by task_id
        
        Args:
            task_id: Task identifier
            task_update: Task update data
            
        Returns:
            Dict with 'success' bool and either 'message'/'task_id' or 'error'
        """
        pass
    
    @abstractmethod
    def get_task(self, session_id: Optional[str] = None, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get task by session_id or task_id
        
        Args:
            session_id: Session identifier (optional)
            task_id: Task identifier (optional)
            
        Returns:
            Dict with 'success' bool and either 'data' or 'error'
        """
        pass
    
    @abstractmethod
    def get_task_history(self, task_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get task history by task_id
        
        Args:
            task_id: Task identifier
            limit: Maximum number of history entries
            offset: Number of entries to skip
            
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
