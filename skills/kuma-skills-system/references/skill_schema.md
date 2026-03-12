# skill.json Schema Reference

## 完整 Schema

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "Skill 描述",
  "triggers": ["触发词1", "触发词2"],
  "author": "作者名称",
  "dependencies": ["依赖包1", "依赖包2"],
  "tools": [
    {
      "name": "tool_name",
      "description": "工具描述",
      "parameters": {
        "param_name": {
          "type": "string|integer|boolean|array|object",
          "description": "参数描述",
          "required": true|false,
          "default": "默认值"
        }
      }
    }
  ],
  "prompts": {
    "system": "系统提示词（可选）",
    "examples": []
  }
}
```

## 字段说明

### 必填字段

#### `name` (string)
- **说明**: Skill 唯一标识符
- **格式**: 小写字母、数字、连字符
- **示例**: `"weather"`, `"github-analyzer"`
- **限制**: 最长 64 字符

#### `version` (string)
- **说明**: Skill 版本号
- **格式**: 语义化版本 (semver)
- **示例**: `"1.0.0"`, `"2.1.3"`

#### `description` (string)
- **说明**: Skill 功能描述
- **用途**: 帮助用户和理解 skill 用途
- **示例**: `"获取天气和预报信息"`

#### `triggers` (array of strings)
- **说明**: 触发关键词列表
- **用途**: 匹配用户消息，激活 skill
- **示例**: `["天气", "weather", "气温"]`
- **建议**: 包含中英文、同义词、常见变体

### 可选字段

#### `author` (string)
- **说明**: 作者名称
- **示例**: `"kuma-claw-team"`

#### `dependencies` (array of strings)
- **说明**: Python 依赖包列表
- **用途**: 安装时自动安装依赖
- **示例**: `["requests", "beautifulsoup4"]`

#### `tools` (array of objects)
- **说明**: 工具定义列表（用于文档生成）
- **结构**:
  ```json
  {
    "name": "tool_name",
    "description": "工具描述",
    "parameters": {
      "param_name": {
        "type": "string",
        "description": "参数描述",
        "required": true,
        "default": "默认值"
      }
    }
  }
  ```

#### `prompts` (object)
- **说明**: 提示词配置（可选）
- **字段**:
  - `system`: 系统提示词（通常在 prompts.py 中定义）
  - `examples`: 示例列表（通常在 prompts.py 中定义）

## 最佳实践

### 命名规范
- ✅ 使用描述性名称：`weather`, `github-analyzer`
- ❌ 避免模糊名称：`tool`, `helper`

### 触发词设计
- ✅ 覆盖多种表达方式：`["天气", "weather", "气温"]`
- ✅ 包含用户常用短语：`["查天气", "今天天气"]`
- ❌ 避免过于宽泛：`["信息", "数据"]`

### 依赖管理
- ✅ 只列出必要依赖
- ✅ 指定版本范围：`["requests>=2.28.0"]`
- ❌ 避免与 kuma-claw 核心依赖冲突

### 工具定义
- ✅ 提供清晰的参数说明
- ✅ 标注必填/可选参数
- ✅ 提供默认值（如果适用）

## 示例

### 简单 Skill（无依赖）

```json
{
  "name": "echo",
  "version": "1.0.0",
  "description": "回显用户消息",
  "triggers": ["echo", "回显"],
  "tools": [
    {
      "name": "echo_message",
      "description": "回显消息",
      "parameters": {
        "message": {
          "type": "string",
          "description": "要回显的消息",
          "required": true
        }
      }
    }
  ]
}
```

### 复杂 Skill（多工具+依赖）

```json
{
  "name": "github-analyzer",
  "version": "2.1.0",
  "description": "深度分析 GitHub 仓库",
  "triggers": ["分析仓库", "GitHub 分析", "repo analysis"],
  "author": "kuma-claw-team",
  "dependencies": ["PyGithub>=1.58.0", "requests>=2.28.0"],
  "tools": [
    {
      "name": "analyze_structure",
      "description": "分析项目结构",
      "parameters": {
        "repo_url": {
          "type": "string",
          "description": "仓库 URL",
          "required": true
        }
      }
    },
    {
      "name": "search_code",
      "description": "搜索代码",
      "parameters": {
        "repo_url": {
          "type": "string",
          "description": "仓库 URL",
          "required": true
        },
        "query": {
          "type": "string",
          "description": "搜索关键词",
          "required": true
        }
      }
    }
  ]
}
```

## 验证规则

1. **必填字段检查**: `name`, `version`, `description`, `triggers` 必须存在
2. **类型检查**: 所有字段必须符合 JSON 类型
3. **命名规范**: `name` 必须符合 `[a-z0-9-]+` 正则
4. **版本格式**: `version` 必须符合语义化版本规范
5. **触发词数量**: `triggers` 至少包含 1 个元素
