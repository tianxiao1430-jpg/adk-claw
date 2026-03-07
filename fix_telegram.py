import re

with open("adk_claw/telegram_handler.py", "r") as f:
    content = f.read()

content = content.replace(
    'async def run_agent(user_id: int, message: str) -> str:',
    'async def run_agent(user_id: int, parts: list) -> str:'
).replace(
    'parts=[types.Part(text=message)]',
    'parts=parts'
)

handle_message_old = """async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"处理普通消息\"\"\"
    user_id = update.effective_user.id
    message = update.message.text

    print(f"[Telegram] {user_id}: {message}")

    # 显示正在输入
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # 运行 Agent
    response = await run_agent(user_id, message)"""

handle_message_new = """async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"处理消息和图片\"\"\"
    user_id = update.effective_user.id

    parts = []
    text = update.message.text or update.message.caption or ""
    
    if text:
        parts.append(types.Part.from_text(text=text))
        
    if update.message.photo:
        photo = update.message.photo[-1]
        photo_file = await photo.get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        parts.append(types.Part.from_bytes(data=bytes(photo_bytes), mime_type="image/jpeg"))

    if not parts:
        return

    print(f"[Telegram] {user_id}: 收到消息 (含图片: {bool(update.message.photo)})")

    # 显示正在输入
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    # 运行 Agent
    response = await run_agent(user_id, parts)"""

content = content.replace(handle_message_old, handle_message_new)

content = content.replace(
    'MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)',
    'MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, handle_message)'
)

with open("adk_claw/telegram_handler.py", "w") as f:
    f.write(content)
