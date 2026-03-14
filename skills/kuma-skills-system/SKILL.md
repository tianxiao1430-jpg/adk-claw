---
name: kuma-skills-system
description: Modular skills system for kuma-claw to extend agent capabilities with custom tools, prompts, and workflows. Use when (1) adding new skills to kuma-claw, (2) managing existing skills (list/info/install), (3) creating custom skill packages, or (4) integrating skills with Google ADK FunctionTool system.
---

# Kuma Skills System

Extend kuma-claw's capabilities with modular, reusable skill packages.

## Overview

Skills are self-contained modules that add specialized tools, prompts, and workflows to kuma-claw. Each skill includes:

- **Metadata** (`skill.json`) - Triggers, dependencies, tool definitions
- **Tools** (`tools.py`) - Google ADK FunctionTool implementations
- **Prompts** (`prompts.py`) - System prompts and examples
- **Resources** (optional) - Scripts, references, assets

## Quick Start

### List Installed Skills

```bash
kuma-claw skills
```

### Get Skill Details

```bash
kuma-claw skill-info <skill-name>
```

### Use a Skill

Skills activate automatically based on trigger keywords:

```
User: "东京今天天气怎么样？"
→ Triggers weather skill → Calls get_current_weather(city="东京")
```

## Core Capabilities

### 1. Skill Discovery

Skills are auto-discovered from:
- `kuma_claw/skills/` - Local skill directory
- Each skill requires `skill.json` in root

### 2. Tool Integration

Skills provide tools via Google ADK FunctionTool:

```python
from google.adk.tools import FunctionTool

def get_current_weather(city: str) -> str:
    """获取指定城市的当前天气"""
    # Implementation
    pass

TOOLS = [
    FunctionTool(func=get_current_weather)
]
```

### 3. Prompt Injection

Skill prompts are automatically added to agent system instruction:

```python
# In skill's prompts.py
SYSTEM_PROMPT = """
## 天气查询能力
你可以通过 get_current_weather 工具获取实时天气信息。
...
"""
```

### 4. Trigger Matching

Skills activate when user message contains trigger keywords:

```json
// skill.json
{
  "triggers": ["天气", "weather", "气温", "预报"]
}
```

## Creating a New Skill

### Step 1: Initialize Skill Structure

```bash
kuma-claw skill-init <skill-name>
```

Creates:
```
skills/<skill-name>/
├── skill.json
├── tools.py
├── prompts.py
└── __init__.py
```

### Step 2: Define Metadata

Edit `skill.json`:

```json
{
  "name": "weather",
  "version": "1.0.0",
  "description": "获取天气和预报信息",
  "triggers": ["天气", "weather", "气温"],
  "author": "your-name",
  "dependencies": ["requests"],
  "tools": [
    {
      "name": "get_current_weather",
      "description": "获取指定城市的当前天气",
      "parameters": {
        "city": {
          "type": "string",
          "description": "城市名称",
          "required": true
        }
      }
    }
  ]
}
```

### Step 3: Implement Tools

Edit `tools.py`:

```python
import requests
from google.adk.tools import FunctionTool

def get_current_weather(city: str) -> str:
    """获取指定城市的当前天气

    Args:
        city: 城市名称（中文或英文）

    Returns:
        天气信息字符串
    """
    try:
        url = f"http://wttr.in/{city}?format=%l:+%t+%C&lang=zh"
        response = requests.get(url, timeout=5)
        return response.text.strip() if response.status_code == 200 else f"❌ 无法获取 {city} 的天气"
    except Exception as e:
        return f"❌ 天气查询失败: {str(e)}"

TOOLS = [
    FunctionTool(func=get_current_weather)
]
```

### Step 4: Add Prompts

Edit `prompts.py`:

```python
SYSTEM_PROMPT = """
## 天气查询能力

你可以通过 `get_current_weather` 工具获取实时天气信息。

使用场景：
- 用户询问"今天天气怎么样"
- 用户询问某城市的气温

调用示例：
get_current_weather(city="东京")
"""

EXAMPLES = [
    {
        "user": "东京今天天气怎么样？",
        "assistant": "让我查一下东京的天气信息。",
        "tool_call": "get_current_weather(city='东京')"
    }
]
```

### Step 5: Test

```bash
# Reload skills
kuma-claw skills-reload

# Test trigger
kuma-claw test "东京今天天气怎么样？"
```

## Skill Manager API

For programmatic access:

```python
from kuma_claw.skills import SkillManager

# Initialize
manager = SkillManager(skills_dir="kuma_claw/skills")

# List skills
skills = manager.list_skills()

# Get skill by trigger
skill = manager.get_skill_by_trigger("天气怎么样")

# Get all tools
tools = manager.get_all_tools()

# Get all prompts
prompts = manager.get_all_prompts()
```

## Best Practices

### Tool Design

- **Single Responsibility**: Each tool should do one thing well
- **Clear Descriptions**: Help the agent understand when to use the tool
- **Error Handling**: Return user-friendly error messages
- **Type Hints**: Use Python type hints for better agent understanding

### Prompt Design

- **Be Specific**: Include concrete examples
- **Show Context**: When and why to use tools
- **Keep It Lean**: Only essential instructions

### Trigger Design

- **Cover Variations**: Include synonyms and common phrases
- **Avoid Overlap**: Don't duplicate triggers across skills
- **Test Coverage**: Verify triggers match user language patterns

## Troubleshooting

### Skill Not Loading

```bash
# Check skill structure
kuma-claw skill-validate <skill-name>

# Check logs
kuma-claw logs --skills
```

### Tool Not Called

- Verify trigger keywords match user message
- Check tool description is clear
- Ensure skill is in `kuma_claw/skills/`

### Import Errors

```bash
# Install dependencies
pip install -r skills/<skill-name>/requirements.txt
```

## Resources

### scripts/

- `skill_manager.py` - Core skill loading and management
- `init_skill.py` - Initialize new skill structure

### references/

- `example_weather_skill/` - Complete weather skill example
- `skill_schema.md` - skill.json schema reference
