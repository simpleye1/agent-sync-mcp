#!/usr/bin/env python3
"""
MCP tools for Nova Agent progress reporting

Tools:
- update_execution_session: Update execution's session_id
- create_step: Create a new step in an execution
- update_step: Update an existing step's status/message
- health_check: Check Task Manager service health
"""

from typing import Dict, Any, Optional
import fastmcp

from src.clients import create_task_manager_client


task_client = create_task_manager_client()
mcp = fastmcp.FastMCP("Nova Task Manager")


@mcp.tool()
def update_execution_session(
    execution_id: str,
    session_id: str
) -> Dict[str, Any]:
    """
    Update execution with session ID. Call this at the start to register your session.
    
    Args:
        execution_id: The execution ID you are working on (get from NOVA_EXECUTION_ID env var)
        session_id: Your agent session ID to associate with this execution (get from skill tool)
    
    Returns:
        Updated execution information
    """
    try:
        result = task_client.patch_execution(
            execution_id=execution_id,
            session_id=session_id
        )
        
        if result.get("success"):
            return {
                "success": True,
                "message": f"Execution {execution_id} updated with session {session_id}",
                "data": result.get("data")
            }
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Failed to update execution: {str(e)}"}


@mcp.tool()
def create_step(
    execution_id: str,
    step_name: str,
    message: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new step in an execution. The step starts with 'running' status by default.
    
    Args:
        execution_id: The execution ID to create the step in (get from NOVA_EXECUTION_ID env var)
        step_name: Name of the step (e.g., "analyzing", "coding", "testing")
        message: Optional description of what this step will do
        status: Optional initial status - "running", "completed", "failed", or "skipped" (default: "running")
    
    Returns:
        Created step information including step_id (save this for updates)
    """
    if status and status not in {"running", "completed", "failed", "skipped"}:
        return {
            "success": False,
            "error": f"Invalid status '{status}'. Must be one of: running, completed, failed, skipped"
        }
    
    try:
        result = task_client.create_step(
            execution_id=execution_id,
            step_name=step_name,
            message=message,
            status=status
        )
        
        if result.get("success"):
            step_data = result.get("data", {})
            return {
                "success": True,
                "message": f"Step '{step_name}' created",
                "step_id": step_data.get("step_id"),
                "data": step_data
            }
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Failed to create step: {str(e)}"}


@mcp.tool()
def update_step(
    execution_id: str,
    step_id: str,
    status: Optional[str] = None,
    message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing step's status and/or message.
    
    Args:
        execution_id: The execution ID containing the step (get from NOVA_EXECUTION_ID env var)
        step_id: The step ID to update (from create_step response)
        status: New status - "running", "completed", "failed", or "skipped"
        message: Updated message describing the outcome
    
    Returns:
        Updated step information
    """
    if not status and not message:
        return {"success": False, "error": "Provide at least status or message to update"}
    
    valid_statuses = {"running", "completed", "failed", "skipped"}
    if status and status not in valid_statuses:
        return {
            "success": False, 
            "error": f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
        }
    
    try:
        result = task_client.patch_step(
            execution_id=execution_id,
            step_id=step_id,
            status=status,
            message=message
        )
        
        if result.get("success"):
            return {
                "success": True,
                "message": f"Step {step_id} updated",
                "data": result.get("data")
            }
        return result
        
    except Exception as e:
        return {"success": False, "error": f"Failed to update step: {str(e)}"}


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    Check Task Manager service health status.
    
    Returns:
        Health check result and configuration information
    """
    return task_client.health_check()
