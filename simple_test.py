#!/usr/bin/env python3
"""
简单的功能测试
"""

import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_status_mcp import TaskManagerClient, TaskUpdate, TaskStatus


def test_task_manager_client():
    """测试 Task Manager 客户端"""
    print("🧪 测试 Task Manager 客户端")
    print("="*50)
    
    # 初始化客户端
    client = TaskManagerClient()
    print(f"✅ 客户端初始化完成")
    print(f"   Task Manager URL: {client.base_url}")
    print(f"   超时设置: {client.timeout}s")
    
    # 健康检查
    print("\n🔍 执行健康检查...")
    health_result = client.get_health_check()
    if health_result["success"]:
        print("✅ Task Manager 服务正常")
        print(f"   配置: {health_result['config']}")
    else:
        print("❌ Task Manager 服务异常")
        print(f"   错误: {health_result['error']}")
        print("   这是正常的，因为 Task Manager 服务可能未启动")
    
    # 创建测试任务更新
    print("\n📝 创建测试任务更新...")
    task_update = TaskUpdate(
        session_id="test-session-001",
        task_id="test-task-001",
        jira_ticket="PROJ-123",
        status=TaskStatus.RUNNING,
        current_action="测试 API 调用",
        progress_percentage=50,
        message="正在测试 Task Manager 客户端",
        details={"test": True, "environment": "development"},
        timestamp=datetime.now(timezone.utc).isoformat()
    )
    
    print("✅ 任务更新对象创建成功")
    print(f"   Session ID: {task_update.session_id}")
    print(f"   Task ID: {task_update.task_id}")
    print(f"   Jira Ticket: {task_update.jira_ticket}")
    print(f"   状态: {task_update.status.value}")
    print(f"   进度: {task_update.progress_percentage}%")
    
    # 测试 API 调用（预期会失败，因为服务未启动）
    print("\n🌐 测试 API 调用...")
    result = client.update_task_status(task_update)
    if result["success"]:
        print("✅ API 调用成功")
        print(f"   响应: {result}")
    else:
        print("❌ API 调用失败（预期结果）")
        print(f"   错误: {result['error']}")
    
    # 测试获取任务状态
    print("\n📊 测试获取任务状态...")
    task_result = client.get_task_status("test-task-001")
    if task_result["success"]:
        print("✅ 获取任务状态成功")
        print(f"   数据: {task_result['data']}")
    else:
        print("❌ 获取任务状态失败（预期结果）")
        print(f"   错误: {task_result['error']}")
    
    print("\n🎉 客户端测试完成！")
    print("💡 要完整测试功能，请启动 Task Manager 服务")


def test_environment_variables():
    """测试环境变量配置"""
    print("\n🧪 测试环境变量配置")
    print("="*50)
    
    # 显示当前环境变量
    host = os.getenv('TASK_MANAGER_HOST', 'localhost')
    port = os.getenv('TASK_MANAGER_PORT', '8080')
    timeout = os.getenv('TASK_MANAGER_TIMEOUT', '30')
    
    print(f"✅ 环境变量配置:")
    print(f"   TASK_MANAGER_HOST: {host}")
    print(f"   TASK_MANAGER_PORT: {port}")
    print(f"   TASK_MANAGER_TIMEOUT: {timeout}")
    
    print("\n💡 可以通过以下方式配置:")
    print("   export TASK_MANAGER_HOST=your-host")
    print("   export TASK_MANAGER_PORT=your-port")
    print("   export TASK_MANAGER_TIMEOUT=60")


if __name__ == "__main__":
    test_task_manager_client()
    test_environment_variables()