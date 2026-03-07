import re

with open("adk_claw/agent.py", "r") as f:
    content = f.read()

# Fix the tools_prompt string
target = "- **get_memory_stats**: 获取记忆统计"
replacement = """- **get_memory_stats**: 获取记忆统计
- **web_search**: 通过 DuckDuckGo 搜索网络获取实时信息
  - 用法：web_search(query, limit=5)
  - 必须使用：当用户询问当前事件、天气、新闻或你不知道的信息时，必须主动使用此工具搜索。"""

if target in content and "web_search(query" not in content:
    content = content.replace(target, replacement)

with open("adk_claw/agent.py", "w") as f:
    f.write(content)
