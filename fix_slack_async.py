import re

with open("adk_claw/slack_handler.py", "r") as f:
    content = f.read()

content = content.replace("from slack_bolt import App", "from slack_bolt.async_app import AsyncApp")
content = content.replace("from slack_bolt.adapter.socket_mode import SocketModeHandler", "from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler")

content = content.replace("app = App(token=bot_token)", "app = AsyncApp(token=bot_token)")
content = content.replace("handler = SocketModeHandler(app, app_token)", "handler = AsyncSocketModeHandler(app, app_token)")

start_old = """def start():
    \"\"\"启动 Slack Bot\"\"\"
    if not init_app():
        return

    print("💬 Slack Bot 启动中...")
    handler.start()
    print("✅ Slack Bot 已启动")"""

start_new = """async def start_async():
    if not init_app():
        return
    print("💬 Slack Bot 启动中...")
    await handler.start_async()

def start():
    \"\"\"启动 Slack Bot\"\"\"
    try:
        asyncio.run(start_async())
    except KeyboardInterrupt:
        pass
    print("✅ Slack Bot 已停止")"""

content = content.replace(start_old, start_new)

with open("adk_claw/slack_handler.py", "w") as f:
    f.write(content)
