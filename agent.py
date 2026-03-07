"""
ADK Claw - Agent 定义
====================
基于 Google ADK 的 Slack AI Agent
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

try:
    from config import config
    MODEL = config.get_model()
except:
    MODEL = os.environ.get("ADK_MODEL", "gemini-2.5-flash")


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
    from memory import memory_manager
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
    from memory import memory_manager
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
    from memory import memory_manager
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
    from memory import memory_manager
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


# 注册工具
TOOLS = [
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

adk_claw_agent = LlmAgent(
    name="adk_claw",
    model=get_model(),
    instruction="""
你是 ADK Claw，一个智能办公助手。

## 能力
- 回答问题
- 执行简单任务
- 记住和回忆信息
- 获取当前时间

## 工作原则
1. 简洁直接
2. 优先给结果
3. 不确定时主动询问
4. 重要信息主动记住

## 工具
- get_current_time: 获取当前时间
- remember: 记住重要信息
- recall: 回忆相关信息
- forget: 忘记特定记忆

## 记忆策略
- 用户偏好 → 使用 remember(source="preference")
- 重要事实 → 使用 remember(source="fact")
- 临时笔记 → 使用 remember(source="note")
- 需要回忆时 → 使用 recall()
""",
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
