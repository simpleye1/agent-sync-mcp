#!/usr/bin/env python3
"""
MCP tools implementation - simplified without interface layer
"""

from typing import Dict, Any, Optional
import fastmcp

from src.clients import create_task_manager_client


# Create client instance
task_client = create_task_manager_client()

# Create FastMCP application
mcp = fastmcp.FastMCP("Agent Status Tracker")


@mcp.tool()
def update_task_status(
    session_id: str,
    jira_ticket: str,
    status: str,
    current_action: str,
    message: str,
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Update task status
    
    Args:
        session_id: Session unique identifier
        jira_ticket: Jira ticket number
        status: Task status (running/success/failed)
        current_action: Current action description
        message: Status description message
        progress_percentage: Progress percentage (0-100)
        details: Additional task details (optional)
    
    Returns:
        Operation result
    """
    from datetime import datetime, timezone
    from src.models import TaskUpdate, TaskStatus
    
    try:
        # Validate status value
        task_status = TaskStatus(status)
        
        # Create task update object
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
        
        # Call client directly
        result = task_client.update_task_status(task_update)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"Session {session_id} status updated successfully",
                "task_update": task_update.to_dict(),
                "api_response": result.get("data")
            }
        else:
            return result
            
    except ValueError as e:
        return {
            "success": False,
            "error": f"Invalid status value: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update status: {str(e)}"
        }


@mcp.tool()
def get_task_status(session_id: str, id_type: str = "session_id") -> Dict[str, Any]:
    """
    Get task status
    
    Args:
        session_id: Session unique identifier
        id_type: Type of identifier (session_id or task_id)
    
    Returns:
        Task status information
    """
    return task_client.get_task_status(session_id, id_type=id_type)


@mcp.tool()
def get_task_history(session_id: str, id_type: str = "session_id") -> Dict[str, Any]:
    """
    Get task complete history
    
    Args:
        session_id: Session unique identifier
        id_type: Type of identifier (session_id or task_id)
    
    Returns:
        Complete task history including status changes and logs
    """
    return task_client.get_task_history(session_id, id_type=id_type)


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    Check Task Manager service health status
    
    Returns:
        Health check result and configuration information
    """
    return task_client.health_check()