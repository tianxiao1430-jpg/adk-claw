"""
ADK Claw Gateway - Adapters
===========================
"""

from .base import BaseAdapter
from .telegram import TelegramAdapter
from .web import WebAdapter

__all__ = [
    "BaseAdapter",
    "TelegramAdapter",
    "WebAdapter",
]
