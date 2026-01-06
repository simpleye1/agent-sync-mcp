#!/usr/bin/env python3
"""
MCP tools implementation
"""

from typing import Dict, Any, Optional
import fastmcp

from src.clients import create_task_manager_client


# Create client instance
task_client = create_task_manager_client()

# Create FastMCP application
mcp = fastmcp.FastMCP("Agent Status Tracker")


@mcp.tool()
def update_task(
    session_id: str,
    jira_ticket: str,
    status: str,
    current_action: str,
    message: str,
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update task status for the current agent session
    
    Args:
        session_id: Your agent session ID (use your own session identifier)
        jira_ticket: Jira ticket number you are working on
        status: Sub-task status - "running" while in progress, "success" when completed, "failed" on error
        current_action: Sub-task name in one word (e.g. analyzing, coding, testing, reviewing, deploying)
        message: Detailed description of what you accomplished or encountered
        progress_percentage: Your estimated overall progress (0-100)
        details: Additional context as key-value pairs (optional)
    
    Returns:
        Operation result
    """
    from datetime import datetime, timezone
    from src.models import TaskUpdate, TaskStatus
    
    try:
        # First get task_id by session_id
        get_result = task_client.get_task(session_id=session_id)
        if not get_result["success"]:
            return {"success": False, "error": f"Failed to get task: {get_result.get('error')}"}
        
        task_id = get_result["data"].get("task_id")
        if not task_id:
            return {"success": False, "error": "Task not found for session_id"}
        
        # Build task update
        task_status = TaskStatus(status)
        task_update = TaskUpdate(
            session_id=session_id,
            jira_ticket=jira_ticket,
            status=task_status,
            current_action=current_action,
            progress_percentage=max(0, min(100, progress_percentage)),
            message=message,
            details=details or {},
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        # Update task by task_id
        result = task_client.update_task(task_id, task_update)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Task {task_id} updated successfully",
                "task_id": task_id,
                "task_update": task_update.to_dict(),
                "api_response": result
            }
        else:
            return result
            
    except ValueError as e:
        return {"success": False, "error": f"Invalid status value: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}


@mcp.tool()
def get_task(session_id: str) -> Dict[str, Any]:
    """
    Get current task information for your agent session
    
    Args:
        session_id: Your agent session ID (use your own session identifier)
    
    Returns:
        Task information including status, progress, and details
    """
    return task_client.get_task(session_id=session_id)


@mcp.tool()
def get_task_history(session_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    Get complete history of your agent session's task
    
    Args:
        session_id: Your agent session ID (use your own session identifier)
        limit: Maximum number of history entries to return (default 100)
        offset: Number of entries to skip for pagination (default 0)
    
    Returns:
        Complete task history including all status changes and logs
    """
    # First get task_id by session_id
    get_result = task_client.get_task(session_id=session_id)
    if not get_result["success"]:
        return {"success": False, "error": f"Failed to get task: {get_result.get('error')}"}
    
    task_id = get_result["data"].get("task_id")
    if not task_id:
        return {"success": False, "error": "Task not found for session_id"}
    
    return task_client.get_task_history(task_id, limit=limit, offset=offset)


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    Check Task Manager service health status
    
    Returns:
        Health check result and configuration information
    """
    return task_client.health_check()
