"""
ADK Claw - Google Workspace 工具集
==================================

使用 ADK 内置的 GoogleApiToolset。
"""

import os
from typing import List, Optional

from google.adk.tools.base_toolset import BaseToolset

try:
    from google.adk.tools.google_api_tool import (
        CalendarToolset,
        GmailToolset,
        SheetsToolset,
        DocsToolset,
        YoutubeToolset,
        BigQueryToolset,
    )
    ADK_TOOLSETS_AVAILABLE = True
except ImportError:
    ADK_TOOLSETS_AVAILABLE = False

try:
    from ..config import config
except ImportError:
    config = None


def get_oauth_credentials():
    """获取 OAuth 凭证"""
    client_id = None
    client_secret = None
    
    if config:
        client_id = config.get_google_oauth_client_id()
        client_secret = config.get_google_oauth_client_secret()
    
    # 环境变量后备
    if not client_id:
        client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    if not client_secret:
        client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    
    return client_id, client_secret


def create_gmail_toolset(
    tool_filter: Optional[List[str]] = None,
    tool_name_prefix: str = "gmail"
) -> Optional[BaseToolset]:
    """创建 Gmail 工具集
    
    Args:
        tool_filter: 工具过滤器（如 ["messages_send", "messages_list"]）
        tool_name_prefix: 工具名称前缀
        
    Returns:
        GmailToolset 或 None（如果未配置）
    """
    if not ADK_TOOLSETS_AVAILABLE:
        return None
    
    client_id, client_secret = get_oauth_credentials()
    
    if not client_id or not client_secret:
        return None
    
    return GmailToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def create_calendar_toolset(
    tool_filter: Optional[List[str]] = None,
    tool_name_prefix: str = "calendar"
) -> Optional[BaseToolset]:
    """创建 Calendar 工具集"""
    if not ADK_TOOLSETS_AVAILABLE:
        return None
    
    client_id, client_secret = get_oauth_credentials()
    
    if not client_id or not client_secret:
        return None
    
    return CalendarToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def create_sheets_toolset(
    tool_filter: Optional[List[str]] = None,
    tool_name_prefix: str = "sheets"
) -> Optional[BaseToolset]:
    """创建 Sheets 工具集"""
    if not ADK_TOOLSETS_AVAILABLE:
        return None
    
    client_id, client_secret = get_oauth_credentials()
    
    if not client_id or not client_secret:
        return None
    
    return SheetsToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def create_docs_toolset(
    tool_filter: Optional[List[str]] = None,
    tool_name_prefix: str = "docs"
) -> Optional[BaseToolset]:
    """创建 Docs 工具集"""
    if not ADK_TOOLSETS_AVAILABLE:
        return None
    
    client_id, client_secret = get_oauth_credentials()
    
    if not client_id or not client_secret:
        return None
    
    return DocsToolset(
        client_id=client_id,
        client_secret=client_secret,
        tool_filter=tool_filter,
        tool_name_prefix=tool_name_prefix,
    )


def create_all_google_workspace_toolsets() -> List[BaseToolset]:
    """创建所有 Google Workspace 工具集
    
    Returns:
        工具集列表
    """
    toolsets = []
    
    # Gmail - 常用工具
    gmail = create_gmail_toolset(
        tool_filter=[
            "messages_send",
            "messages_list",
            "messages_get",
            "drafts_create",
            "labels_list",
        ]
    )
    if gmail:
        toolsets.append(gmail)
    
    # Calendar - 常用工具
    calendar = create_calendar_toolset(
        tool_filter=[
            "events_list",
            "events_get",
            "events_insert",
            "events_update",
            "events_delete",
            "calendar_list_list",
        ]
    )
    if calendar:
        toolsets.append(calendar)
    
    # Sheets - 常用工具
    sheets = create_sheets_toolset(
        tool_filter=[
            "spreadsheets_get",
            "spreadsheets_create",
            "values_get",
            "values_update",
            "values_append",
            "values_clear",
        ]
    )
    if sheets:
        toolsets.append(sheets)
    
    # Docs - 常用工具
    docs = create_docs_toolset(
        tool_filter=[
            "documents_get",
            "documents_create",
        ]
    )
    if docs:
        toolsets.append(docs)
    
    return toolsets


# 检查状态
def check_google_workspace_status() -> str:
    """检查 Google Workspace 工具集状态"""
    if not ADK_TOOLSETS_AVAILABLE:
        return "❌ ADK GoogleApiToolset 不可用（需要 google-adk >= 0.1.0）"
    
    client_id, client_secret = get_oauth_credentials()
    
    if not client_id or not client_secret:
        return "❌ OAuth 未配置\n\n配置步骤:\n1. 前往 Google Cloud Console\n2. 创建 OAuth 2.0 客户端 ID\n3. 运行: adk-claw config --section oauth\n或设置环境变量:\n  GOOGLE_OAUTH_CLIENT_ID=...\n  GOOGLE_OAUTH_CLIENT_SECRET=..."
    
    return "✅ Google Workspace 工具集可用\n\n可用服务: Gmail, Calendar, Sheets, Docs"
