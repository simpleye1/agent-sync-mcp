#!/usr/bin/env python3
"""
Task Manager client interface (similar to Java Feign)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

# Import from models package
import sys
from pathlib import Path
models_path = Path(__file__).parent.parent / "models"
sys.path.insert(0, str(models_path))
from models import TaskUpdate


class TaskManagerClient(ABC):
    """Abstract Task Manager client interface (similar to Java Feign)"""
    
    @abstractmethod
    def update_task_status(self, task_update: TaskUpdate) -> Dict[str, Any]:
        """Update task status"""
        pass
    
    @abstractmethod
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        pass
    
    @abstractmethod
    def get_task_history(self, task_id: str) -> Dict[str, Any]:
        """Get task complete history"""
        pass
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        pass