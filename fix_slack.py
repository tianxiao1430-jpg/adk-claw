import re

with open("adk_claw/slack_handler.py", "r") as f:
    content = f.read()

content = content.replace(
    'async def run_agent(user_id: str, message: str) -> str:',
    'async def run_agent(user_id: str, parts: list) -> str:'
).replace(
    'parts=[types.Part(text=message)]',
    'parts=parts'
)

# Add import httpx if not present
if "import httpx" not in content:
    content = content.replace("import asyncio", "import asyncio\nimport httpx")

def_mention_old = """    @app.event("app_mention")
    async def handle_mention(event, say):
        \"\"\"处理 @提及\"\"\"
        user = event.get("user", "unknown")
        text = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()

        print(f"[Slack] @{user}: {text}")

        # 运行 Agent
        response = await run_agent(user, text)"""

def_mention_new = """    @app.event("app_mention")
    async def handle_mention(event, say):
        \"\"\"处理 @提及和图片\"\"\"
        user = event.get("user", "unknown")
        text = re.sub(r"<@[^>]+>", "", event.get("text", "")).strip()

        parts = []
        if text:
            parts.append(types.Part.from_text(text=text))

        # 下载图片
        files = event.get("files", [])
        for file in files:
            url = file.get("url_private_download")
            mimetype = file.get("mimetype", "image/jpeg")
            if url and mimetype.startswith("image/"):
                try:
                    import httpx
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, headers={"Authorization": f"Bearer {bot_token}"})
                        if resp.status_code == 200:
                            parts.append(types.Part.from_bytes(data=resp.content, mime_type=mimetype))
                except Exception as e:
                    print(f"下载 Slack 图片失败: {e}")

        if not parts:
            return

        print(f"[Slack] @{user}: 收到消息 (含图片: {len(files) > 0})")

        # 运行 Agent
        response = await run_agent(user, parts)"""

def_msg_old = """    @app.event("message")
    async def handle_message(event, say):
        \"\"\"处理私信\"\"\"
        # 只处理私信
        if event.get("channel_type") != "im":
            return

        user = event.get("user", "unknown")
        text = event.get("text", "")

        print(f"[Slack] DM @{user}: {text}")

        # 运行 Agent
        response = await run_agent(user, text)"""

def_msg_new = """    @app.event("message")
    async def handle_message(event, say):
        \"\"\"处理私信\"\"\"
        # 只处理私信
        if event.get("channel_type") != "im":
            return

        user = event.get("user", "unknown")
        text = event.get("text", "")

        parts = []
        if text:
            parts.append(types.Part.from_text(text=text))

        # 下载图片
        files = event.get("files", [])
        for file in files:
            url = file.get("url_private_download")
            mimetype = file.get("mimetype", "image/jpeg")
            if url and mimetype.startswith("image/"):
                try:
                    import httpx
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, headers={"Authorization": f"Bearer {bot_token}"})
                        if resp.status_code == 200:
                            parts.append(types.Part.from_bytes(data=resp.content, mime_type=mimetype))
                except Exception as e:
                    print(f"下载 Slack 图片失败: {e}")

        if not parts:
            return

        print(f"[Slack] DM @{user}: 收到消息 (含图片: {len(files) > 0})")

        # 运行 Agent
        response = await run_agent(user, parts)"""

content = content.replace(def_mention_old, def_mention_new)
content = content.replace(def_msg_old, def_msg_new)

with open("adk_claw/slack_handler.py", "w") as f:
    f.write(content)
