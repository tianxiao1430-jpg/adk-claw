"""
ADK Claw - 智能 Agent 平台
==========================

基于 Google ADK 的开源 AI Agent 平台。
"""

__version__ = "0.1.0"

from .agent import adk_claw_agent, root_agent
from .config import config
from .prompts import build_system_prompt

__all__ = [
    "adk_claw_agent",
    "root_agent",
    "config",
    "build_system_prompt",
    "__version__",
]
