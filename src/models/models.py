#!/usr/bin/env python3
"""
Data models for Task Manager MCP Server
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class StepStatus(Enum):
    """Step status enumeration"""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ExecutionPatch:
    """Execution patch data structure"""
    session_id: Optional[str] = None
    worktree_path: Optional[str] = None


@dataclass
class StepCreate:
    """Step creation data structure"""
    step_name: str
    message: Optional[str] = None
    status: Optional[str] = None


@dataclass
class StepPatch:
    """Step patch data structure"""
    status: Optional[StepStatus] = None
    message: Optional[str] = None
