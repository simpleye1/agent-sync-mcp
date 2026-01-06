#!/usr/bin/env python3
"""
HTTP implementation using auto-generated client
"""

import os
from typing import Dict, Any

from src.models import TaskUpdate
from src.clients.base_client import TaskManagerClientBase

# Import generated client
from src.clients.generated._client import Client
from src.clients.generated._client.api.tasks import (
    put_api_tasks_identifier_status,
    get_api_tasks_identifier,
    get_api_tasks_identifier_history
)
from src.clients.generated._client.api.health import get_api_health
from src.clients.generated._client.models import (
    HttpTaskUpdateRequest,
    HttpTaskUpdateRequestStatus,
    PutApiTasksIdentifierStatusIdType,
    GetApiTasksIdentifierIdType,
    GetApiTasksIdentifierHistoryIdType,
    HttpErrorResponse,
    HttpTaskUpdateResponse,
    HttpTaskStatusResponse,
    HttpTaskHistoryResponse
)
from src.clients.generated._client.types import UNSET


class HttpTaskManagerClient(TaskManagerClientBase):
    """HTTP implementation using auto-generated client"""
    
    def __init__(self):
        # Get configuration from environment variables
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        
        # API timeout settings
        timeout_seconds = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
        
        # Create the generated client
        self.client = Client(
            base_url=self.base_url,
            timeout=timeout_seconds
        )
    
    def _convert_task_update_to_request(self, task_update: TaskUpdate) -> HttpTaskUpdateRequest:
        """Convert our TaskUpdate to generated HttpTaskUpdateRequest"""
        # Convert status enum
        status_map = {
            "running": HttpTaskUpdateRequestStatus.RUNNING,
            "success": HttpTaskUpdateRequestStatus.SUCCESS,
            "failed": HttpTaskUpdateRequestStatus.FAILED
        }
        
        # Handle details conversion
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
    
    def _convert_id_type_to_put_enum(self, id_type: str) -> PutApiTasksIdentifierStatusIdType:
        """Convert string id_type to PutApiTasksIdentifierStatusIdType enum"""
        if id_type == "task_id":
            return PutApiTasksIdentifierStatusIdType.TASK_ID
        return PutApiTasksIdentifierStatusIdType.SESSION_ID
    
    def _convert_id_type_to_get_enum(self, id_type: str) -> GetApiTasksIdentifierIdType:
        """Convert string id_type to GetApiTasksIdentifierIdType enum"""
        if id_type == "task_id":
            return GetApiTasksIdentifierIdType.TASK_ID
        return GetApiTasksIdentifierIdType.SESSION_ID
    
    def _convert_id_type_to_history_enum(self, id_type: str) -> GetApiTasksIdentifierHistoryIdType:
        """Convert string id_type to GetApiTasksIdentifierHistoryIdType enum"""
        if id_type == "task_id":
            return GetApiTasksIdentifierHistoryIdType.TASK_ID
        return GetApiTasksIdentifierHistoryIdType.SESSION_ID
    
    def _handle_response_error(self, response) -> Dict[str, Any]:
        """Handle error responses from generated client"""
        if isinstance(response, HttpErrorResponse):
            return {
                "success": False,
                "error": response.error,
                "error_code": getattr(response, 'error_code', None),
                "timestamp": getattr(response, 'timestamp', None)
            }
        return {
            "success": False,
            "error": "Unknown error response"
        }
    
    def update_task_status(self, task_update: TaskUpdate, id_type: str = "session_id") -> Dict[str, Any]:
        """Update task status using generated client"""
        try:
            # Convert to generated request format
            request = self._convert_task_update_to_request(task_update)
            id_type_enum = self._convert_id_type_to_put_enum(id_type)
            
            # Call generated API
            response = put_api_tasks_identifier_status.sync(
                identifier=task_update.session_id,
                client=self.client,
                body=request,
                id_type=id_type_enum
            )
            
            if response is None:
                return {
                    "success": False,
                    "error": "No response from server"
                }
            
            # Handle error response
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            # Handle success response
            if isinstance(response, HttpTaskUpdateResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "message": response.message,
                    "task_id": getattr(response, 'task_id', None)
                }
            
            return {
                "success": False,
                "error": f"Unexpected response type: {type(response)}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"API call exception: {str(e)}"
            }
    
    def get_task_status(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Get current task status using generated client"""
        try:
            id_type_enum = self._convert_id_type_to_get_enum(id_type)
            
            response = get_api_tasks_identifier.sync(
                identifier=identifier,
                client=self.client,
                id_type=id_type_enum
            )
            
            if response is None:
                return {
                    "success": False,
                    "error": "No response from server"
                }
            
            # Handle error response
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            # Handle success response
            if isinstance(response, HttpTaskStatusResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "data": response.data.to_dict() if hasattr(response.data, 'to_dict') else response.data
                }
            
            return {
                "success": False,
                "error": f"Unexpected response type: {type(response)}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"API call exception: {str(e)}"
            }
    
    def get_task_history(self, identifier: str, id_type: str = "session_id") -> Dict[str, Any]:
        """Get complete task history using generated client"""
        try:
            id_type_enum = self._convert_id_type_to_history_enum(id_type)
            
            response = get_api_tasks_identifier_history.sync(
                identifier=identifier,
                client=self.client,
                id_type=id_type_enum
            )
            
            if response is None:
                return {
                    "success": False,
                    "error": "No response from server"
                }
            
            # Handle error response
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            # Handle success response
            if isinstance(response, HttpTaskHistoryResponse):
                return {
                    "success": response.success if hasattr(response, 'success') else True,
                    "data": response.data.to_dict() if hasattr(response.data, 'to_dict') else response.data
                }
            
            return {
                "success": False,
                "error": f"Unexpected response type: {type(response)}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"API call exception: {str(e)}"
            }
    
    def health_check(self) -> Dict[str, Any]:
        """Health check using generated client"""
        try:
            response = get_api_health.sync(client=self.client)
            
            if response is None:
                return {
                    "success": False,
                    "error": "No response from server"
                }
            
            # Handle error response
            if isinstance(response, HttpErrorResponse):
                return self._handle_response_error(response)
            
            # Handle success response (assuming it's a health response)
            return {
                "success": True,
                "message": "Task Manager service is healthy (generated client)",
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
            return {
                "success": False,
                "error": f"Health check exception: {str(e)}"
            }