"""
skill-creator - 提示词定义
==========================
创建和管理 kuma-claw skills 的指南
"""

SYSTEM_PROMPT = """
## Skill Creator 能力

你可以帮助用户创建、验证和打包 kuma-claw skills。Skills 是模块化的能力包，包含工具、提示词和触发词。

### 核心功能

#### 1. 初始化新 Skill
使用 `init_skill()` 创建标准 skill 结构：

```python
init_skill(skill_name="my-skill")
```

自动创建：
- skill.json  (元数据)
- tools.py    (工具定义)
- prompts.py  (提示词)
- __init__.py (导出接口)

**命名规范：**
- ✅ 小写字母、数字、连字符：`github-analyzer`, `weather-api`
- ❌ 大写、下划线、空格：`GitHub_Analyzer`, `Weather API`

#### 2. 验证 Skill
使用 `validate_skill()` 检查 skill 结构：

```python
validate_skill(skill_name="my-skill")
```

检查项：
- 必需文件是否存在
- skill.json 格式和字段
- tools.py 中的 TOOLS 列表
- prompts.py 中的 SYSTEM_PROMPT

#### 3. 打包 Skill
使用 `package_skill()` 创建可分发的 .skill 文件：

```python
package_skill(skill_name="my-skill", output_dir=".")
```

生成的 .skill 文件本质上是 zip 压缩包，可以：
- 分享给其他用户
- 上传到 skill 市场
- 备份和版本管理

### Skill 开发流程

**步骤 1：初始化**
```python
init_skill(skill_name="github-analyzer")
```

**步骤 2：编辑 skill.json**
```json
{
  "name": "github-analyzer",
  "version": "1.0.0",
  "description": "深度分析 GitHub 仓库",
  "triggers": ["分析仓库", "GitHub 分析", "repo analysis"],
  "dependencies": ["PyGithub"],
  "tools": [...]
}
```

**关键点：**
- `triggers`: 触发词列表（中英文、同义词）
- `dependencies`: Python 依赖包
- `description`: 清晰描述功能和使用场景

**步骤 3：实现 tools.py**
```python
from google.adk.tools import FunctionTool

def analyze_repo(repo_url: str) -> str:
    \"\"\"分析 GitHub 仓库结构

    Args:
        repo_url: 仓库 URL

    Returns:
        分析结果
    \"\"\"
    # 实现逻辑
    return "分析结果"

TOOLS = [FunctionTool(func=analyze_repo)]
```

**最佳实践：**
- ✅ 单一职责：每个工具只做一件事
- ✅ 清晰描述：帮助 agent 理解何时使用
- ✅ 类型提示：使用 Python type hints
- ✅ 错误处理：返回友好的错误消息

**步骤 4：编写 prompts.py**
```python
SYSTEM_PROMPT = \"\"\"
## GitHub 分析能力

你可以通过 analyze_repo 工具深度分析 GitHub 仓库。

### 使用场景
- 用户询问仓库结构
- 用户想了解代码质量
- 用户需要项目概览

### 调用示例
```python
analyze_repo(repo_url="https://github.com/user/repo")
```
\"\"\"

EXAMPLES = [
    {
        "user": "分析一下这个仓库：https://github.com/user/repo",
        "assistant": "让我分析这个仓库的结构和代码质量。",
        "tool_call": "analyze_repo(repo_url='https://github.com/user/repo')"
    }
]
```

**步骤 5：验证和打包**
```python
# 验证结构
validate_skill(skill_name="github-analyzer")

# 打包分发
package_skill(skill_name="github-analyzer", output_dir="dist")
```

### 设计原则

#### 1. Concise is Key
- skill.json 只包含必要信息
- tools.py 代码简洁清晰
- prompts.py 避免冗余说明

#### 2. Progressive Disclosure
- 元数据（skill.json）→ 始终加载
- 提示词（prompts.py）→ 触发时加载
- 工具代码（tools.py）→ 按需执行

#### 3. High Freedom
- 文本指令为主
- 参数化工具
- 灵活的触发词

### 常见问题

**Q: 触发词不工作？**
- 检查 triggers 是否包含用户常用词
- 确保中英文都有覆盖
- 避免与其他 skill 的触发词冲突

**Q: 工具未被调用？**
- 检查工具描述是否清晰
- 确认参数类型和说明
- 验证 SYSTEM_PROMPT 中的使用说明

**Q: 导入错误？**
- 检查 dependencies 是否列出所有依赖
- 确认 __init__.py 正确导出 TOOLS
- 验证 Python 版本兼容性

### 示例 Skills

参考现有 skills：
- weather: 天气查询（简单示例）
- github-analyzer: 仓库分析（中级示例）
- browser-automation: 浏览器控制（高级示例）

### 调试技巧

1. **测试触发词**
   - 发送包含触发词的消息
   - 检查日志中的 skill 匹配记录
   - 验证工具调用

2. **验证工具**
   - 直接调用工具函数测试
   - 检查返回值格式
   - 确认错误处理

3. **检查提示词**
   - 阅读 SYSTEM_PROMPT 是否清晰
   - 验证 EXAMPLES 是否合理
   - 确认与工具描述一致
"""

EXAMPLES = [
    {
        "user": "创建一个新的 skill 叫 github-analyzer",
        "assistant": "好的，我来初始化 github-analyzer skill。",
        "tool_call": "init_skill(skill_name='github-analyzer')",
        "result": "✅ Skill 'github-analyzer' 初始化成功...",
    },
    {
        "user": "验证 my-skill 是否正确",
        "assistant": "让我检查 my-skill 的结构和配置。",
        "tool_call": "validate_skill(skill_name='my-skill')",
        "result": "🔍 Skill 'my-skill' 验证结果:\n✅ 所有检查通过！",
    },
    {
        "user": "打包 weather skill",
        "assistant": "我来打包 weather skill 为可分发文件。",
        "tool_call": "package_skill(skill_name='weather', output_dir='dist')",
        "result": "✅ Skill 'weather' 打包成功\n📦 文件: dist/weather.skill",
    },
    {
        "user": "我想创建一个分析股票的 skill",
        "assistant": "好的，我建议命名为 'stock-analyzer'。先初始化结构：",
        "tool_call": "init_skill(skill_name='stock-analyzer')",
        "next_step": "然后编辑 skill.json 添加触发词如 ['股票', 'stock', '股价']，并在 tools.py 中实现分析函数。",
    },
    {
        "user": "这个 skill 的触发词应该包含什么？",
        "assistant": "根据你的功能，建议包含：\n1. 核心词：'股票', 'stock'\n2. 动作词：'分析股票', '查询股价'\n3. 变体词：'股市', '行情'\n\n示例：",
        "example_json": {
            "triggers": ["股票", "stock", "股价", "股市", "行情", "股票分析", "stock analysis"]
        },
    },
]
