"""
ADK Claw - Agent 定义
====================
基于 Google ADK 的 AI Agent
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

try:
    from .config import config
    MODEL = config.get_model()
except ImportError:
    MODEL = os.environ.get("ADK_MODEL", "gemini-3.1-flash")


# ============================================
# 工具定义
# ============================================

def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def echo_message(message: str) -> str:
    """回显消息（测试用）"""
    return f"收到：{message}"


# ============================================
# 记忆工具
# ============================================

def remember(content: str, source: str = "fact") -> str:
    """记住重要信息

    Args:
        content: 要记住的内容
        source: 来源类型（fact/preference/note）

    Returns:
        确认消息
    """
    from .memory import memory_manager
    entry = memory_manager.remember(content, source=source)
    return f"✅ 已记住：{content}"


def recall(query: str, limit: int = 5) -> str:
    """回忆相关信息

    Args:
        query: 搜索关键词
        limit: 返回数量

    Returns:
        相关记忆
    """
    from .memory import memory_manager
    results = memory_manager.search(query, limit=limit)

    if not results:
        return "没有找到相关记忆"

    lines = ["📚 相关记忆："]
    for r in results:
        lines.append(f"- {r.entry.content}")

    return "\n".join(lines)


def forget(content_pattern: str) -> str:
    """忘记特定记忆

    Args:
        content_pattern: 要忘记的内容模式

    Returns:
        确认消息
    """
    from .memory import memory_manager
    results = memory_manager.search(content_pattern, limit=1)

    if not results:
        return "没有找到匹配的记忆"

    entry = results[0].entry
    memory_manager.forget(entry.id)
    return f"✅ 已忘记：{entry.content}"


def get_memory_stats() -> str:
    """获取记忆统计

    Returns:
        记忆统计信息
    """
    from .memory import memory_manager
    stats = memory_manager.stats()

    lines = [
        f"📊 记忆统计：",
        f"- 总条目：{stats.total_entries}",
    ]

    for source, count in stats.by_source.items():
        lines.append(f"- {source}: {count}")

    if stats.last_sync:
        lines.append(f"- 最后同步：{stats.last_sync}")

    return "\n".join(lines)


# ============================================
# 网络搜索工具
# ============================================

def web_search(query: str, limit: int = 5) -> str:
    """通过 DuckDuckGo 搜索网络获取实时信息
    
    Args:
        query: 搜索关键词
        limit: 返回的结果数量上限
        
    Returns:
        包含标题、摘要和链接的搜索结果文本
    """
    try:
        from ddgs import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=limit):
                results.append(f"标题: {r.get('title')}\n内容: {r.get('body')}\n链接: {r.get('href')}")
        
        if not results:
            return f"没有找到关于 '{query}' 的搜索结果。"
            
        return "\n\n".join(results)
    except Exception as e:
        return f"搜索失败: {str(e)}"

# 注册工具
TOOLS = [
    FunctionTool(func=web_search),
    FunctionTool(func=get_current_time),
    FunctionTool(func=echo_message),
    FunctionTool(func=remember),
    FunctionTool(func=recall),
    FunctionTool(func=forget),
    FunctionTool(func=get_memory_stats),
]


# ============================================
# 模型配置
# ============================================

def get_model():
    """获取模型配置"""
    if MODEL.startswith("openai/"):
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=MODEL)
    elif MODEL.startswith("anthropic/"):
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=MODEL)
    elif MODEL.startswith("deepseek/"):
        from google.adk.models.lite_llm import LiteLlm
        return LiteLlm(model=MODEL)
    else:
        # 默认 Gemini
        return MODEL


# ============================================
# Agent 定义
# ============================================

def get_system_instruction(channel: str = "telegram") -> str:
    """构建系统提示词（支持动态格式注入）

    Args:
        channel: 渠道名称（telegram, slack, discord, web, whatsapp）

    Returns:
        完整的系统提示词
    """
    from .prompts import build_system_prompt
    from .formats import get_format_prompt, inject_format_prompt

    base_prompt = build_system_prompt()

    # 添加工具说明
    tools_prompt = """

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

## 记忆策略

- 用户偏好 → 使用 `remember(source="preference")`
- 重要事实 → 使用 `remember(source="fact")`
- 临时笔记 → 使用 `remember(source="note")`
- 需要回忆时 → 使用 `recall()`
"""

    # 添加内部思考标签说明
    internal_prompt = """

## 内部思考 (Internal Thoughts)

如果部分输出是你的内部推理过程而非给用户的内容，使用 `<internal>` 标签：

```
<internal>
你的内部思考过程...
分析步骤、决策逻辑、调试信息等...
</internal>

给用户的实际回复...
```

`<internal>` 标签内的内容会被记录到日志但**不会发送给用户**。

用途：
- 记录推理过程
- 调试信息
- 中间结果（已通过 send_message 发送的内容）
- 敏感信息（记录但不展示）
"""

    # 组合基础提示词
    import datetime
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_prompt = f"\n\n## 系统信息\n当前时间：{now_str}\n"

    full_prompt = base_prompt + time_prompt + tools_prompt + internal_prompt

    # 动态注入格式规范
    full_prompt = inject_format_prompt(full_prompt, channel)

    return full_prompt


def create_agent(channel: str = "telegram") -> LlmAgent:
    """创建 Agent 实例（支持渠道适配）

    Args:
        channel: 渠道名称

    Returns:
        配置好的 Agent 实例
    """
    return LlmAgent(
        name="adk_claw",
        model=get_model(),
        instruction=get_system_instruction(channel),
        description="ADK Claw - 智能办公助手",
        tools=TOOLS,
    )


# 默认 Agent（向后兼容）
adk_claw_agent = LlmAgent(
    name="adk_claw",
    model=get_model(),
    instruction=get_system_instruction("telegram"),
    description="ADK Claw - 智能办公助手",
    tools=TOOLS,
)


# ============================================
# 导出
# ============================================

root_agent = adk_claw_agent


if __name__ == "__main__":
    print("ADK Claw Agent 已定义")
    print(f"工具数量: {len(TOOLS)}")
    print("\n支持的渠道：telegram, slack, discord, web, whatsapp, console")
    print("\n系统提示词预览（Telegram）：")
    print("=" * 60)
    print(get_system_instruction("telegram")[:800] + "...")
