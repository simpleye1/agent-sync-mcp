#!/usr/bin/env python3
"""
HTTP client implementation for Task Manager API
"""

import os
from typing import Dict, Any, Optional
import httpx

from src.clients.base_client import TaskManagerClientBase


class HttpTaskManagerClient(TaskManagerClientBase):
    """HTTP implementation for Task Manager API"""
    
    def __init__(self):
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        self.timeout = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
    
    def _make_request(
        self, 
        method: str, 
        path: str, 
        json_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request and handle response"""
        try:
            with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
                response = client.request(
                    method=method,
                    url=path,
                    json=json_data
                )
                
                if response.status_code >= 400:
                    # 特殊处理常见的 HTTP 错误状态码
                    if response.status_code == 404:
                        return {
                            "success": False,
                            "error": f"API endpoint not found: {method} {path}. The backend service may not have implemented this API yet.",
                            "status_code": 404,
                            "hint": "Please check if the Task Manager backend service has this endpoint implemented."
                        }
                    elif response.status_code == 500:
                        return {
                            "success": False,
                            "error": f"Backend server error (500). The Task Manager service encountered an internal error.",
                            "status_code": 500,
                            "hint": "Please check the Task Manager service logs for details."
                        }
                    
                    # 尝试解析 JSON 错误响应
                    try:
                        error_data = response.json()
                        return {
                            "success": False,
                            "error": error_data.get("error", f"HTTP {response.status_code} error"),
                            "error_code": error_data.get("error_code"),
                            "status_code": response.status_code
                        }
                    except Exception:
                        # 如果无法解析 JSON，返回通用错误信息
                        return {
                            "success": False,
                            "error": f"HTTP {response.status_code} error: {response.text[:200]}",
                            "status_code": response.status_code
                        }
                
                return response.json()
                
        except httpx.TimeoutException:
            return {
                "success": False, 
                "error": f"Request timeout after {self.timeout} seconds",
                "hint": "The Task Manager service may be slow or unresponsive. Try increasing TASK_MANAGER_TIMEOUT."
            }
        except httpx.ConnectError:
            return {
                "success": False, 
                "error": f"Cannot connect to Task Manager service at {self.base_url}",
                "hint": "Please verify that the Task Manager service is running and the host/port are correct."
            }
        except Exception as e:
            return {
                "success": False, 
                "error": f"Request failed: {str(e)}",
                "hint": "An unexpected error occurred. Please check the error message above."
            }
    
    def patch_execution(
        self, 
        execution_id: str, 
        session_id: str
    ) -> Dict[str, Any]:
        """Update execution's session_id"""
        return self._make_request(
            "PATCH",
            f"/api/executions/{execution_id}",
            json_data={"session_id": session_id}
        )
    
    def create_step(
        self, 
        execution_id: str, 
        step_name: str,
        message: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new step for an execution"""
        body = {"step_name": step_name}
        if message is not None:
            body["message"] = message
        if status is not None:
            body["status"] = status
        
        return self._make_request(
            "POST",
            f"/api/executions/{execution_id}/steps",
            json_data=body
        )
    
    def patch_step(
        self, 
        execution_id: str, 
        step_id: str,
        status: Optional[str] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Partially update a step"""
        body = {}
        if status is not None:
            body["status"] = status
        if message is not None:
            body["message"] = message
        
        if not body:
            return {"success": False, "error": "No fields to update"}
        
        return self._make_request(
            "PATCH",
            f"/api/executions/{execution_id}/steps/{step_id}",
            json_data=body
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        result = self._make_request("GET", "/api/health")
        if result.get("success", True) and "error" not in result:
            return {
                "success": True,
                "message": "Task Manager service is healthy",
                "config": {
                    "host": self.host,
                    "port": self.port,
                    "base_url": self.base_url
                },
                **result
            }
        return result
