#!/usr/bin/env python3
"""
Agent Status MCP Server
用于跟踪 Claude agent 执行状态的 MCP 服务器

数据模型说明：
- Session: 一个会话对应一个任务 (session_id 和 task_id 一对一)
- Task: 具体的任务，包含 jira 卡号
- Action: 任务中的具体执行步骤

通过 API 调用 task-manager 服务进行数据存储
"""

import json
import os
import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

import fastmcp


class TaskStatus(Enum):
    """任务状态枚举"""
    RUNNING = "running"
    SUCCESS = "success" 
    FAILED = "failed"


@dataclass
class TaskUpdate:
    """任务更新数据结构"""
    task_id: str
    session_id: str
    jira_ticket: str
    status: TaskStatus
    current_action: str  # 当前执行的动作描述
    progress_percentage: float  # 0-100
    message: str
    details: Dict[str, Any]  # 额外的任务详情
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "session_id": self.session_id,
            "task_id": self.task_id,
            "jira_ticket": self.jira_ticket,
            "status": self.status.value,
            "current_action": self.current_action,
            "progress_percentage": self.progress_percentage,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class TaskManagerClient:
    """Task Manager API 客户端"""
    
    def __init__(self):
        # 从环境变量获取配置
        self.host = os.getenv('TASK_MANAGER_HOST', 'localhost')
        self.port = os.getenv('TASK_MANAGER_PORT', '8080')
        self.base_url = f"http://{self.host}:{self.port}"
        
        # API 超时设置
        self.timeout = int(os.getenv('TASK_MANAGER_TIMEOUT', '30'))
    
    def update_task_status(self, task_update: TaskUpdate) -> Dict[str, Any]:
        """更新任务状态"""
        try:
            url = f"{self.base_url}/api/tasks/status"
            response = requests.post(
                url,
                json=task_update.to_dict(),
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "任务状态更新成功",
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"API 调用失败: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"API 调用超时 (>{self.timeout}s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"无法连接到 Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API 调用异常: {str(e)}"
            }
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        try:
            url = f"{self.base_url}/api/tasks/{task_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": f"未找到任务 {task_id}"
                }
            else:
                return {
                    "success": False,
                    "error": f"API 调用失败: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"API 调用超时 (>{self.timeout}s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"无法连接到 Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API 调用异常: {str(e)}"
            }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """获取会话状态"""
        try:
            url = f"{self.base_url}/api/sessions/{session_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            elif response.status_code == 404:
                return {
                    "success": False,
                    "error": f"未找到会话 {session_id}"
                }
            else:
                return {
                    "success": False,
                    "error": f"API 调用失败: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"API 调用超时 (>{self.timeout}s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"无法连接到 Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API 调用异常: {str(e)}"
            }
    
    def list_running_tasks(self) -> Dict[str, Any]:
        """列出所有运行中的任务"""
        try:
            url = f"{self.base_url}/api/tasks?status=running"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"API 调用失败: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"API 调用超时 (>{self.timeout}s)"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"无法连接到 Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"API 调用异常: {str(e)}"
            }
    
    def get_health_check(self) -> Dict[str, Any]:
        """健康检查"""
        try:
            url = f"{self.base_url}/api/health"
            response = requests.get(url, timeout=5)  # 健康检查用较短超时
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": "Task Manager 服务正常",
                    "config": {
                        "host": self.host,
                        "port": self.port,
                        "base_url": self.base_url,
                        "timeout": self.timeout
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"健康检查失败: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "健康检查超时"
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": f"无法连接到 Task Manager ({self.base_url})"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"健康检查异常: {str(e)}"
            }


# 初始化 Task Manager 客户端
task_manager = TaskManagerClient()

# 创建 FastMCP 应用
mcp = fastmcp.FastMCP("Agent Status Tracker")


@mcp.tool()
def update_task_status(
    session_id: str,
    task_id: str,
    jira_ticket: str,
    status: str,
    current_action: str,
    message: str,
    progress_percentage: float = 0.0,
    details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    更新任务状态
    
    Args:
        session_id: 会话唯一标识符 (与 task_id 一对一)
        task_id: 任务唯一标识符
        jira_ticket: Jira 卡号
        status: 任务状态 (running/success/failed)
        current_action: 当前执行的动作描述
        message: 状态描述信息
        progress_percentage: 进度百分比 (0-100)
        details: 额外的任务详情 (可选)
    
    Returns:
        操作结果
    """
    try:
        # 验证状态值
        task_status = TaskStatus(status)
        
        # 创建任务更新对象
        task_update = TaskUpdate(
            session_id=session_id,
            task_id=task_id,
            jira_ticket=jira_ticket,
            status=task_status,
            current_action=current_action,
            progress_percentage=max(0, min(100, progress_percentage)),
            message=message,
            details=details or {},
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        # 调用 Task Manager API
        result = task_manager.update_task_status(task_update)
        
        if result["success"]:
            return {
                "success": True,
                "message": f"任务 {task_id} 状态已更新",
                "task_update": task_update.to_dict(),
                "api_response": result.get("data")
            }
        else:
            return result
        
    except ValueError as e:
        return {
            "success": False,
            "error": f"无效的状态值: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"更新状态失败: {str(e)}"
        }


@mcp.tool()
def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    获取任务状态
    
    Args:
        task_id: 任务唯一标识符
    
    Returns:
        任务状态信息
    """
    return task_manager.get_task_status(task_id)


@mcp.tool()
def get_session_status(session_id: str) -> Dict[str, Any]:
    """
    获取会话状态
    
    Args:
        session_id: 会话唯一标识符
    
    Returns:
        会话状态信息
    """
    return task_manager.get_session_status(session_id)


@mcp.tool()
def list_running_tasks() -> Dict[str, Any]:
    """
    列出所有运行中的任务
    
    Returns:
        运行中的任务列表
    """
    return task_manager.list_running_tasks()


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    检查 Task Manager 服务健康状态
    
    Returns:
        健康检查结果和配置信息
    """
    return task_manager.get_health_check()


if __name__ == "__main__":
    mcp.run()