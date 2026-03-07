"""
Slack 事件处理
==============
处理 Slack @提及 和消息
"""

import os
import re
import asyncio
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from .agent import adk_claw_agent
from .config import config
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# ============================================
# ADK Runner 初始化
# ============================================

session_service = InMemorySessionService()

runner = Runner(
    app_name="adk-claw",
    agent=adk_claw_agent,
    session_service=session_service,
)


# ============================================
# 用户会话管理
# ============================================

user_sessions = {}


async def get_or_create_session(user_id: str):
    """获取或创建用户会话"""
    if user_id not in user_sessions:
        session = session_service.create_session(
            app_name="adk-claw",
            user_id=user_id,
            state={}
        )
        user_sessions[user_id] = session.id
        return session.id
    return user_sessions[user_id]


async def run_agent(user_id: str, message: str) -> str:
    """运行 Agent"""
    session_id = await get_or_create_session(user_id)

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )

    events = runner.run_async(
        session_id=session_id,
        user_id=user_id,
        new_message=content
    )

    response_text = ""
    async for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    return response_text or "抱歉，我没有理解你的意思。"


# ============================================
# Slack App
# ============================================

app = None
handler = None


def init_app():
    """初始化 Slack App"""
    global app, handler

    bot_token = config.get_slack_bot_token()
    app_token = config.get_slack_app_token()

    if not bot_token or not app_token:
        print("❌ 错误：请配置 Slack Bot Token 和 App Token")
        return False

    app = App(token=bot_token)
    handler = SocketModeHandler(app, app_token)

    # 注册事件处理器
    @app.event("app_mention")
    async def handle_mention(event, say):
        """处理 @提及"""
        user = event.get("user", "unknown")
        text = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()

        print(f"[Slack] @{user}: {text}")

        # 运行 Agent
        response = await run_agent(user, text)

        # 回复
        await say(response)

    @app.event("message")
    async def handle_message(event, say):
        """处理私信"""
        # 只处理私信
        if event.get("channel_type") != "im":
            return

        user = event.get("user", "unknown")
        text = event.get("text", "")

        print(f"[Slack] DM @{user}: {text}")

        # 运行 Agent
        response = await run_agent(user, text)

        # 回复
        await say(response)

    return True


def start():
    """启动 Slack Bot"""
    if not init_app():
        return

    print("💬 Slack Bot 启动中...")
    handler.start()
    print("✅ Slack Bot 已启动")


if __name__ == "__main__":
    start()
