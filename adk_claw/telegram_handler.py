"""
Telegram 事件处理
=================
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from .agent import create_agent
from .formats import extract_internal_content
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# ============================================
# ADK Runner
# ============================================

session_service = InMemorySessionService()

# 为 Telegram 创建专用的 Agent
telegram_agent = create_agent(channel="telegram")

runner = Runner(
    app_name="adk-claw",
    agent=telegram_agent,
    session_service=session_service,
)

user_sessions = {}


async def get_or_create_session(user_id: str) -> str:
    """获取或创建用户会话"""
    if user_id not in user_sessions:
        # create_session 是 async 方法，需要 await
        session = await session_service.create_session(
            app_name="adk-claw",
            user_id=str(user_id),
            state={}
        )

        # 获取 session id
        if hasattr(session, 'id'):
            session_id = session.id
        else:
            session_id = str(session)

        user_sessions[user_id] = session_id
        return session_id

    return user_sessions[user_id]


async def run_agent(user_id: int, message: str) -> str:
    """运行 Agent"""
    session_id = await get_or_create_session(str(user_id))

    content = types.Content(
        role="user",
        parts=[types.Part(text=message)]
    )

    events = runner.run_async(
        session_id=session_id,
        user_id=str(user_id),
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
# Telegram Handlers
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /start 命令"""
    await update.message.reply_text(
        "🦞 你好！我是 ADK Claw。\n\n"
        "直接发消息给我，我会帮你处理。"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理 /help 命令"""
    await update.message.reply_text(
        "🦞 ADK Claw 帮助\n\n"
        "直接发消息给我，我会：\n"
        "- 回答问题\n"
        "- 执行任务\n"
        "- 获取信息\n\n"
        "示例：\n"
        "- 现在几点？\n"
        "- 帮我总结这段文字\n"
        "- 分析这个链接..."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理普通消息"""
    user_id = update.effective_user.id
    message = update.message.text

    print(f"[Telegram] {user_id}: {message}")

    # 显示正在输入
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # 运行 Agent
    response = await run_agent(user_id, message)

    # 提取 internal 内容和可见内容
    internal_content, visible_content = extract_internal_content(response)

    # 记录 internal 内容到日志
    if internal_content:
        print(f"[Internal] {internal_content}")

    # 发送可见内容给用户
    if visible_content:
        await update.message.reply_text(visible_content)
    else:
        # 如果没有可见内容，发送默认回复
        await update.message.reply_text("任务已完成。")


# ============================================
# 启动
# ============================================

def start_telegram(token: str):
    """启动 Telegram Bot"""
    if not token:
        print("❌ 错误：请设置 TELEGRAM_BOT_TOKEN")
        return None

    print("📱 Telegram Bot 启动中...")

    app = Application.builder().token(token).build()

    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Telegram Bot 已启动")

    return app


if __name__ == "__main__":
    import os
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if token:
        app = start_telegram(token)
        app.run_polling()
    else:
        print("请设置 TELEGRAM_BOT_TOKEN")
