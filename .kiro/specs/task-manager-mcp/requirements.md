# 需求文档

## 简介

Nova Task Manager MCP 服务器是一个基于 MCP (Model Context Protocol) 的服务,用于向 Task Manager 服务汇报 Agent 执行进度。该服务提供了一组工具,允许 Agent 注册会话、创建执行步骤、更新步骤状态,并检查服务健康状态。

## 术语表

- **MCP_Server**: 基于 fastmcp 框架实现的 MCP 服务器,提供工具供 Agent 调用
- **Task_Manager**: 后端服务,负责管理任务和执行状态
- **Execution**: 一次任务执行实例,包含多个步骤
- **Step**: 执行过程中的单个步骤,具有状态和消息
- **Session_ID**: Agent 会话的唯一标识符
- **Step_Status**: 步骤状态枚举,包括 running、completed、failed、skipped
- **Client**: 与 Task Manager 通信的客户端实现
- **HTTP_Client**: 通过 HTTP 协议与真实 Task Manager API 通信的客户端
- **Mock_Client**: 用于测试的模拟客户端实现
- **NOVA_EXECUTION_ID**: 环境变量,包含当前执行的 execution_id,Agent 可从此环境变量获取

## 需求

### 需求 1：会话注册

**用户故事：** 作为 Agent,我希望在开始执行时注册我的会话 ID,以便 Task Manager 能够追踪我的执行状态。

#### 验收标准

1. WHEN Agent 调用 update_execution_session 工具并提供 execution_id 和 session_id THEN MCP_Server SHALL 调用 Task Manager API 更新 execution 的 session_id
2. WHEN Task Manager API 返回成功 THEN MCP_Server SHALL 返回包含 success=True 和更新后数据的响应
3. IF Task Manager API 调用失败 THEN MCP_Server SHALL 返回包含 success=False 和错误信息的响应
4. THE update_execution_session 工具 SHALL 要求 execution_id 和 session_id 两个必填参数
5. THE update_execution_session 工具描述 SHALL 告知 Agent 可从环境变量 NOVA_EXECUTION_ID 获取 execution_id
6. THE update_execution_session 工具描述 SHALL 告知 Agent 可通过 skill 工具获取 session_id

### 需求 2：步骤创建

**用户故事：** 作为 Agent,我希望创建执行步骤来记录我的工作进度,以便用户能够了解执行的详细过程。

#### 验收标准

1. WHEN Agent 调用 create_step 工具并提供 execution_id 和 step_name THEN MCP_Server SHALL 创建一个新步骤
2. WHEN 步骤创建成功 THEN MCP_Server SHALL 返回包含 step_id 的响应,供后续更新使用
3. WHEN Agent 提供可选的 message 参数 THEN MCP_Server SHALL 将该消息包含在创建的步骤中
4. WHEN Agent 提供可选的 status 参数 THEN MCP_Server SHALL 使用该状态作为步骤的初始状态
5. WHEN Agent 未提供 status 参数 THEN MCP_Server SHALL 使用 "running" 作为默认初始状态
6. THE MCP_Server SHALL 仅接受以下 status 值：running、completed、failed、skipped
7. IF Agent 提供无效的 status 值 THEN MCP_Server SHALL 返回包含 success=False 和有效状态列表的错误响应
8. IF 步骤创建失败 THEN MCP_Server SHALL 返回包含 success=False 和错误信息的响应
9. THE create_step 工具描述 SHALL 告知 Agent 可从环境变量 NOVA_EXECUTION_ID 获取 execution_id

### 需求 3：步骤更新

**用户故事：** 作为 Agent,我希望更新步骤的状态和消息,以便实时反映执行进度。

#### 验收标准

1. WHEN Agent 调用 update_step 工具并提供有效的 status THEN MCP_Server SHALL 更新步骤状态
2. THE MCP_Server SHALL 仅接受以下状态值：running、completed、failed、skipped
3. IF Agent 提供无效的 status 值 THEN MCP_Server SHALL 返回包含 success=False 和有效状态列表的错误响应
4. IF Agent 未提供 status 和 message 任一参数 THEN MCP_Server SHALL 返回错误提示至少需要提供一个参数
5. WHEN Agent 提供 message 参数 THEN MCP_Server SHALL 更新步骤的消息内容
6. WHEN 步骤更新成功 THEN MCP_Server SHALL 返回包含 success=True 和更新后数据的响应
7. THE update_step 工具描述 SHALL 告知 Agent 可从环境变量 NOVA_EXECUTION_ID 获取 execution_id

### 需求 4：健康检查

**用户故事：** 作为运维人员,我希望检查服务健康状态,以便监控系统运行情况。

#### 验收标准

1. WHEN 用户调用 health_check 工具 THEN MCP_Server SHALL 返回 Task Manager 服务的健康状态
2. WHEN 使用 HTTP_Client 且服务健康 THEN MCP_Server SHALL 返回包含配置信息（host、port、base_url）的响应
3. IF Task Manager 服务不可用 THEN MCP_Server SHALL 返回包含错误信息的响应

### 需求 5：客户端策略模式

**用户故事：** 作为开发者,我希望能够在真实 HTTP 客户端和 Mock 客户端之间切换,以便在不同环境下进行开发和测试。

#### 验收标准

1. THE Client_Factory SHALL 根据 USE_MOCK_CLIENT 环境变量选择客户端实现
2. WHEN USE_MOCK_CLIENT 环境变量为 "true" THEN Client_Factory SHALL 返回 Mock_Client 实例
3. WHEN USE_MOCK_CLIENT 环境变量为 "false" 或未设置 THEN Client_Factory SHALL 返回 HTTP_Client 实例
4. THE HTTP_Client SHALL 从环境变量读取配置：TASK_MANAGER_HOST（默认 localhost）、TASK_MANAGER_PORT（默认 8080）、TASK_MANAGER_TIMEOUT（默认 30 秒）
5. THE Mock_Client SHALL 在内存中维护 execution 和 step 数据,用于测试验证

### 需求 6：HTTP 客户端实现

**用户故事：** 作为系统集成者,我希望 HTTP 客户端能够正确调用 Task Manager API,以便与后端服务通信。

**技术说明：** 项目使用 `openapi-python-client` 从 `docs/swagger.yaml` 自动生成类型化的 API 客户端代码。当 API 定义更新时,运行 `make regenerate` 重新生成客户端。

#### 验收标准

1. WHEN 调用 patch_execution THEN HTTP_Client SHALL 发送 PATCH 请求到 /api/executions/{execution-id}
2. WHEN 调用 create_step THEN HTTP_Client SHALL 发送 POST 请求到 /api/executions/{execution-id}/steps
3. WHEN 调用 patch_step THEN HTTP_Client SHALL 发送 PATCH 请求到 /api/executions/{execution-id}/steps/{step-id}
4. WHEN 调用 health_check THEN HTTP_Client SHALL 发送 GET 请求到 /api/health
5. IF HTTP 请求超时 THEN HTTP_Client SHALL 返回包含 "Request timeout" 错误的响应
6. IF 无法连接到 Task Manager THEN HTTP_Client SHALL 返回包含连接失败信息的响应
7. IF HTTP 响应状态码 >= 400 THEN HTTP_Client SHALL 解析错误响应并返回包含 error 和 error_code 的响应
8. THE 项目 SHALL 提供 Makefile 命令用于从 swagger.yaml 生成客户端代码
9. THE 生成的客户端代码 SHALL 位于 src/clients/generated/ 目录

### 需求 7：数据模型

**用户故事：** 作为开发者,我希望有清晰的数据模型定义,以便理解和使用 API 数据结构。

#### 验收标准

1. THE StepStatus 枚举 SHALL 定义四种状态：running、completed、failed、skipped
2. THE ExecutionPatch 数据类 SHALL 包含可选的 session_id 和 worktree_path 字段
3. THE StepCreate 数据类 SHALL 包含必填的 step_name 和可选的 message、status 字段
4. THE StepPatch 数据类 SHALL 包含可选的 status 和 message 字段
