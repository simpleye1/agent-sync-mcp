# 实现计划: Task Manager MCP

## 概述

本任务列表基于已实现的代码逆向生成,主要用于记录实现状态和补充测试覆盖。由于核心功能已实现,任务重点在于验证现有实现和补充属性测试。

**重要提示：** 项目使用 `openapi-python-client` 从 `docs/swagger.yaml` 自动生成 API 客户端代码。当修改 API 定义后,运行 `make regenerate` 重新生成客户端代码到 `src/clients/generated/` 目录。

## 任务

- [x] 1. 数据模型实现
  - [x] 1.1 实现 StepStatus 枚举
    - 定义 running、completed、failed、skipped 四种状态
    - _Requirements: 7.1_
  
  - [x] 1.2 实现数据类
    - 实现 ExecutionPatch、StepCreate、StepPatch 数据类
    - _Requirements: 7.2, 7.3, 7.4_

- [x] 2. 客户端抽象层实现
  - [x] 2.1 实现 TaskManagerClientBase 抽象基类
    - 定义 patch_execution、create_step、patch_step、health_check 抽象方法
    - _Requirements: 5.1_
  
  - [x] 2.2 实现 HttpTaskManagerClient
    - 实现 HTTP 请求发送和响应处理
    - 实现环境变量配置读取
    - 注意：项目使用 `make regenerate` 从 swagger.yaml 生成类型化客户端到 src/clients/generated/
    - _Requirements: 5.4, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_
  
  - [x] 2.3 实现 MockTaskManagerClient
    - 实现内存数据存储
    - 实现模拟 API 响应
    - _Requirements: 5.5_
  
  - [x] 2.4 实现 create_task_manager_client 工厂方法
    - 根据 USE_MOCK_CLIENT 环境变量选择客户端
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 3. MCP 工具实现
  - [x] 3.1 实现 update_execution_session 工具
    - 接收 execution_id 和 session_id 参数
    - 调用客户端 patch_execution 方法
    - _Requirements: 1.1, 1.2, 1.3, 1.4_
  
  - [x] 3.2 实现 create_step 工具
    - 接收 execution_id、step_name 和可选 message、status 参数
    - 实现 status 值验证（仅接受 running/completed/failed/skipped）
    - 调用客户端 create_step 方法
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_
  
  - [x] 3.3 实现 update_step 工具
    - 接收 execution_id、step_id、可选 status 和 message 参数
    - 实现状态值验证
    - 调用客户端 patch_step 方法
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  
  - [x] 3.4 实现 health_check 工具
    - 调用客户端 health_check 方法
    - _Requirements: 4.1, 4.2, 4.3_
  
  - [x] 3.5 更新 MCP 工具描述
    - 在 execution_id 参数描述中添加 "可从环境变量 NOVA_EXECUTION_ID 获取" 提示
    - 在 session_id 参数描述中添加 "可通过 skill 工具获取" 提示
    - 更新 update_execution_session、create_step、update_step 三个工具
    - _Requirements: 1.5, 1.6, 2.5, 3.7_

- [ ] 4. 单元测试
  - [ ]* 4.1 编写 MCP 工具单元测试
    - 测试参数验证逻辑
    - 测试错误响应格式
    - _Requirements: 1.4, 3.2, 3.3, 3.4_
  
  - [ ]* 4.2 编写客户端单元测试
    - 测试工厂方法选择逻辑
    - 测试 Mock 客户端数据管理
    - _Requirements: 5.1, 5.2, 5.3, 5.5_
  
  - [ ]* 4.3 编写数据模型单元测试
    - 测试枚举值
    - 测试数据类字段
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 5. 属性测试
  - [ ]* 5.1 编写响应格式一致性属性测试
    - **Property 1: 响应格式一致性**
    - **Validates: Requirements 1.2, 1.3, 2.2, 2.4, 3.6**
  
  - [ ]* 5.2 编写状态值验证属性测试
    - **Property 2: 状态值验证**
    - **Validates: Requirements 3.2, 3.3**
  
  - [ ]* 5.3 编写 Mock 客户端状态一致性属性测试
    - **Property 3: Mock 客户端状态一致性**
    - **Validates: Requirements 5.5**
  
  - [ ]* 5.4 编写工厂方法选择正确性属性测试
    - **Property 4: 工厂方法选择正确性**
    - **Validates: Requirements 5.1, 5.2, 5.3**
  
  - [ ]* 5.5 编写 HTTP 错误响应处理属性测试
    - **Property 5: HTTP 错误响应处理**
    - **Validates: Requirements 6.7**
  
  - [ ]* 5.6 编写步骤创建初始状态属性测试
    - **Property 6: 步骤创建初始状态**
    - **Validates: Requirements 2.1**
  
  - [ ]* 5.7 编写参数传递完整性属性测试
    - **Property 7: 参数传递完整性**
    - **Validates: Requirements 1.1, 2.3, 3.1, 3.5**

- [ ] 6. 检查点 - 确保所有测试通过
  - 运行所有测试,如有问题请咨询用户

## 备注

- 标记为 `[x]` 的任务表示已在现有代码中实现
- 标记为 `*` 的任务为可选任务,可跳过以加快 MVP 进度
- 每个任务都引用了具体的需求以便追溯
- 属性测试验证通用正确性属性
- 单元测试验证具体示例和边界条件
