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

from agent import adk_claw_agent
from config import config
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
    """运行 Agent 并返回结果"""
    session_id = await get_or_create_session(user_id)
    
    # 构造消息
    content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )
    
    # 运行 Agent
    events = runner.run_async(
        session_id=session_id,
        user_id=user_id,
        new_message=content
    )
    
    # 收集响应
    response_text = ""
    async for event in events:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    
    return response_text or "抱歉，我没有理解你的意思。"


# ============================================
# Slack App 初始化
# ============================================

def create_slack_app():
    """创建 Slack App"""
    bot_token = config.get_slack_bot_token()
    if not bot_token:
        return None
    
    return App(token=bot_token)


app = create_slack_app()


# ============================================
# 事件处理
# ============================================

def setup_handlers(app: App):
    """设置事件处理器"""
    
    @app.event("app_mention")
    def handle_app_mention(event, say):
        """处理 @提及"""
        user = event.get("user", "unknown")
        text = event.get("text", "")
        channel = event.get("channel", "")
        
        # 移除 @提及 部分
        clean_text = re.sub(r"<@[^>]+>", "", text).strip()
        
        print(f"[Slack:{channel}] {user}: {clean_text}")
        
        # 运行 Agent（同步包装）
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(run_agent(user, clean_text))
        finally:
            loop.close()
        
        # 发送回复
        say(response)
    
    @app.event("message")
    def handle_message(event, say):
        """处理 DM 消息"""
        # 只处理 DM
        if event.get("channel_type") != "im":
            return
        
        user = event.get("user", "unknown")
        text = event.get("text", "")
        
        print(f"[Slack:DM] {user}: {text}")
        
        # 运行 Agent
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(run_agent(user, text))
        finally:
            loop.close()
        
        say(response)


# ============================================
# 启动
# ============================================

def start():
    """启动 Slack Socket Mode"""
    app_token = config.get_slack_app_token()
    
    if not app or not app_token:
        print("❌ 错误：请配置 Slack Tokens")
        print("   运行 python main.py --web 进行配置")
        return
    
    setup_handlers(app)
    
    print("🚀 ADK Claw (Slack) 启动中...")
    print("📡 连接 Slack Socket Mode...")
    
    handler = SocketModeHandler(app, app_token)
    handler.start()


if __name__ == "__main__":
    start()
