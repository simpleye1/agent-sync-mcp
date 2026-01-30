---
inclusion: always
---

# Task Manager MCP 项目规范

## 代码生成

**重要：** 本项目的 API 客户端代码是自动生成的，不要手动修改生成的文件。

### 客户端代码生成

- **生成工具**: `openapi-python-client`
- **源文件**: `docs/swagger.yaml`
- **生成目录**: `src/clients/generated/`
- **生成命令**: 
  - `make regenerate` - 清理并重新生成客户端
  - `make generate` - 仅生成客户端
  - `make clean` - 清理生成的代码

### 工作流程

1. 修改 `docs/swagger.yaml` 中的 API 定义
2. 运行 `make regenerate` 重新生成客户端代码
3. 更新手写的包装器代码（如 `src/clients/http_client.py`）以使用新的 API
4. 运行测试验证更改

**注意**: 生成的代码位于 `src/clients/generated/_client/` 目录下，包含：
- `api/` - API 端点函数
- `models/` - 数据模型类
- `client.py` - 客户端基类

## Git Commit 规范

### Pre-commit Hook

项目配置了 pre-commit hook，会在每次 commit 前自动运行测试：

```bash
# Hook 位置
.git/hooks/pre-commit

# 自动执行
make test
```

如果测试失败，commit 会被阻止。修复测试后再次尝试提交。

**跳过 hook（不推荐）**:
```bash
git commit --no-verify -m "your message"
```

### Commit Message 格式

使用简洁的一句话格式，遵循 Conventional Commits 规范：

```
<type>: <description>
```

### Type 类型

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 重构代码
- `test`: 添加或修改测试
- `chore`: 构建工具、依赖更新等

### 示例

```bash
feat: add status parameter to create_step API
fix: handle timeout error in HTTP client
docs: update API usage examples in README
chore: regenerate client from updated swagger spec
refactor: simplify error handling in MCP tools
test: add property tests for step creation
```

### 规则

- 使用英文描述
- 首字母小写
- 不要以句号结尾
- 描述要清晰简洁，说明做了什么改动
- 一个 commit 只做一件事

## 项目结构

```
.
├── docs/
│   └── swagger.yaml          # API 定义（源文件）
├── src/
│   ├── clients/
│   │   ├── generated/        # 自动生成的客户端（不要手动修改）
│   │   ├── base_client.py    # 客户端抽象基类
│   │   ├── http_client.py    # HTTP 客户端实现
│   │   ├── mock_client.py    # Mock 客户端实现
│   │   └── client_factory.py # 客户端工厂
│   ├── models/               # 数据模型
│   └── server/               # MCP 服务器
├── tests/                    # 测试文件
├── Makefile                  # 构建和生成命令
└── .kiro/
    ├── specs/                # 功能规格文档
    └── steering/             # 项目规范和指南
```
