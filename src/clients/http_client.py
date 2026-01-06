#!/usr/bin/env python3
"""
HTTP implementation using auto-generated client
"""

import os
from typing import Dict, Any, Optional

from src.models import TaskUpdate
from src.clients.base_client import TaskManagerClientBase

# Import generated client
from src.clients.generated._client import Client
from src.clients.generated._client.api.tasks import (
    post_api_tasks,
    get_api_tasks,
    get_api_tasks_history
)
from src.clients.generated._client.api.health import get_api_health
from src.clients.generated._client.models import (
    HttpTaskUpdateRequest,
    HttpTaskUpdateRequestStatus,
    HttpErrorResponse,
    HttpTaskUpdateResponse,
    HttpTaskStatusResponse,
    HttpTaskHistoryResponse
)
from src.clients.generated._client.types import UNSET


class HttpTaskManagerClient(TaskManagerClientBase):
    """HTTP implementation using auto-generated client"""
    
    def __init__(self):
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        timeout_seconds = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
        
        self.client = Client(
            base_url=self.base_url,
            timeout=timeout_seconds
        )
    
    def _convert_task_update_to_request(self, task_update: TaskUpdate) -> HttpTaskUpdateRequest:
        """Convert TaskUpdate to HttpTaskUpdateRequest"""
        status_map = {
            "running": HttpTaskUpdateRequestStatus.RUNNING,
            "success": HttpTaskUpdateRequestStatus.SUCCESS,
            "failed": HttpTaskUpdateRequestStatus.FAILED
        }
        
        details = UNSET
        if task_update.details:
            from src.clients.generated._client.models.http_task_update_request_details import HttpTaskUpdateRequestDetails
            details_obj = HttpTaskUpdateRequestDetails()
            for key, value in task_update.details.items():
                details_obj[key] = value
            details = details_obj
        
        return HttpTaskUpdateRequest(
            session_id=task_update.session_id,
            jira_ticket=task_update.jira_ticket,
            status=status_map[task_update.status.value],
            current_action=task_update.current_action,
            message=task_update.message,
            progress_percentage=task_update.progress_percentage if task_update.progress_percentage is not None else UNSET,
            details=details,
            timestamp=task_update.timestamp if task_update.timestamp else UNSET
        )
    
    def _handle_response_error(self, response) -> Dict[str, Any]:
        """Handle error responses"""
        if isinstance(response, HttpErrorResponse):
            return {
                "success": False,
                "error": response.error,
                "error_code": getattr(response, 'error_code', None),
                "timestamp": getattr(response, 'timestamp', None)
            }
        return {"success": False, "error": "Unknown error response"}
    
    def update_task(self, task_id: str, task_update: TaskUpdate) -> Dict[str, Any]:
        """Update task by task_id"""
        try:
            request = self._convert_task_update_to_request(task_update)
            
            response = post_api_tasks.sync(
                client=self.client,
                body=request,
                task_id=task_id
            )
            
            if response is None:
                return {"success": False, "error": "No response from server"}
            
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            if isinstance(response, HttpTaskUpdateResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "message": response.message,
                    "task_id": getattr(response, 'task_id', None)
                }
            
            return {"success": False, "error": f"Unexpected response type: {type(response)}"}
            
        except Exception as e:
            return {"success": False, "error": f"API call exception: {str(e)}"}
    
    def get_task(self, session_id: Optional[str] = None, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Get task by session_id or task_id"""
        try:
            response = get_api_tasks.sync(
                client=self.client,
                session_id=session_id if session_id else UNSET,
                task_id=task_id if task_id else UNSET
            )
            
            if response is None:
                return {"success": False, "error": "No response from server"}
            
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            if isinstance(response, HttpTaskStatusResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "data": response.data.to_dict() if hasattr(response.data, 'to_dict') else response.data
                }
            
            return {"success": False, "error": f"Unexpected response type: {type(response)}"}
            
        except Exception as e:
            return {"success": False, "error": f"API call exception: {str(e)}"}
    
    def get_task_history(self, task_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """Get task history by task_id"""
        try:
            response = get_api_tasks_history.sync(
                client=self.client,
                task_id=task_id,
                limit=limit,
                offset=offset
            )
            
            if response is None:
                return {"success": False, "error": "No response from server"}
            
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            if isinstance(response, HttpTaskHistoryResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "data": response.data.to_dict() if hasattr(response.data, 'to_dict') else response.data
                }
            
            return {"success": False, "error": f"Unexpected response type: {type(response)}"}
            
        except Exception as e:
            return {"success": False, "error": f"API call exception: {str(e)}"}
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        try:
            response = get_api_health.sync(client=self.client)
            
            if response is None:
                return {"success": False, "error": "No response from server"}
            
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            return {
                "success": True,
                "message": "Task Manager service is healthy",
                "config": {
                    "host": self.host,
                    "port": self.port,
                    "base_url": self.base_url,
                    "status": getattr(response, 'status', 'healthy'),
                    "version": getattr(response, 'version', 'unknown'),
                    "timestamp": getattr(response, 'timestamp', None)
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"Health check exception: {str(e)}"}
