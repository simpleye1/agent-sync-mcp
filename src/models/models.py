#!/usr/bin/env python3
"""
Data models for Agent Status MCP Server
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any


class TaskStatus(Enum):
    """Task status enumeration"""
    RUNNING = "running"
    SUCCESS = "success" 
    FAILED = "failed"


@dataclass
class TaskUpdate:
    """Task update data structure"""
    session_id: str
    jira_ticket: str
    status: TaskStatus
    current_action: str  # Current action description
    progress_percentage: float  # 0-100
    message: str
    details: Dict[str, Any]  # Additional task details
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "session_id": self.session_id,
            "jira_ticket": self.jira_ticket,
            "status": self.status.value,
            "current_action": self.current_action,
            "progress_percentage": self.progress_percentage,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }