with open("adk_claw/agent.py", "r") as f:
    content = f.read()

import re

old_tools_block = """    # 添加工具说明
    tools_prompt = \"\"\"

## 可用工具 (Tools)

你可以使用以下工具：

- **get_current_time**: 获取当前时间
- **remember**: 记住重要信息
  - 用法：remember(content, source)
  - source: "fact" | "preference" | "note"
- **recall**: 回忆相关信息
  - 用法：recall(query, limit=5)
- **forget**: 忘记特定记忆
  - 用法：forget(content_pattern)
- **get_memory_stats**: 获取记忆统计

## 记忆策略"""

new_tools_block = """    # 添加工具说明
    tools_prompt = \"\"\"

## 可用工具 (Tools)

你可以使用以下工具：

- **get_current_time**: 获取当前时间
- **web_search**: 通过 DuckDuckGo 搜索网络获取实时信息（天气、新闻、百科等）
  - 用法：web_search(query, limit=5)
  - 核心指令：当你遇到自己不知道、未训练过、或需要最新数据的提问时（如明天天气、最新新闻），**必须**立即使用此工具。
- **remember**: 记住重要信息
  - 用法：remember(content, source)
  - source: "fact" | "preference" | "note"
- **recall**: 回忆相关信息
  - 用法：recall(query, limit=5)
- **forget**: 忘记特定记忆
  - 用法：forget(content_pattern)
- **get_memory_stats**: 获取记忆统计

## 记忆策略"""

content = content.replace(old_tools_block, new_tools_block)

with open("adk_claw/agent.py", "w") as f:
    f.write(content)
