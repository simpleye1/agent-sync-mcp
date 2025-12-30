#!/usr/bin/env python3
"""
HTTP implementation of Task Manager client
"""

import os
import requests
from typing import Dict, Any, Optional

# Import from local modules
import sys
from pathlib import Path
models_path = Path(__file__).parent.parent / "models"
sys.path.insert(0, str(models_path))
from models import TaskUpdate

# Import from local modules
import sys
from pathlib import Path
clients_path = Path(__file__).parent.parent / "clients"
sys.path.insert(0, str(clients_path))

from client_interface import TaskManagerClient


class HttpTaskManagerClient(TaskManagerClient):
    """HTTP implementation of Task Manager client"""
    
    def __init__(self):
        # Get configuration from environment variables
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        
        # API timeout settings
        self.timeout = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    json=data,
                    timeout=self.timeout,
                    headers={'Content-Type': 'application/json'}
                )
            else:
                return {
                    "success": False,
                    "error": f"Unsupported HTTP method: {method}"
                }
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json() if response.content else None
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": "Resource not found"
                }
            else:
                return {
                    "success": False,
                    "error": f"API call failed: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"API call timeout (>{self.timeout}s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"Cannot connect to Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API call exception: {str(e)}"
            }
    
    def update_task_status(self, task_update: TaskUpdate) -> Dict[str, Any]:
        """Update task status"""
        result = self._make_request('POST', '/api/tasks/status', task_update.to_dict())
        
        if result["success"]:
            return {
                "success": True,
                "message": "Task status updated successfully",
                "data": result.get("data")
            }
        else:
            return result
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        result = self._make_request('GET', f'/api/tasks/{task_id}')
        
        if not result["success"] and "not found" in result.get("error", "").lower():
            return {
                "success": False,
                "error": f"Task {task_id} not found"
            }
        
        return result
    
    def get_task_history(self, task_id: str) -> Dict[str, Any]:
        """Get task complete history"""
        return self._make_request('GET', f'/api/tasks/{task_id}/complete-history')
    
    def health_check(self) -> Dict[str, Any]:
        """Health check"""
        # Use shorter timeout for health check
        original_timeout = self.timeout
        self.timeout = 5
        
        result = self._make_request('GET', '/api/health')
        
        # Restore original timeout
        self.timeout = original_timeout
        
        if result["success"]:
            return {
                "success": True,
                "message": "Task Manager service is healthy",
                "config": {
                    "host": self.host,
                    "port": self.port,
                    "base_url": self.base_url,
                    "timeout": original_timeout
                }
            }
        else:
            return result