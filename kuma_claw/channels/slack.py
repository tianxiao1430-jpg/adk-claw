"""
Slack 渠道处理器
==================
"""

import os
import re
import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from .base import ChannelHandler
from .formats import extract_internal_content
from ..service_registry import set_status

logger = logging.getLogger("kuma_claw.channels.slack")


class SlackChannel(ChannelHandler):
    """Slack 渠道处理器"""
    
    def __init__(self, agent, bot_token: str, app_token: str):
        super().__init__("Slack", agent)
        self.bot_token = bot_token
        self.app_token = app_token
        self.app = None
        self.handler = None
    
    async def handle_message(self, user_id: str, text: str, **kwargs) -> str:
        """处理消息"""
        return await self.run_agent(user_id, text)
    
    async def start(self):
        """启动 Slack Bot"""
        self.app = AsyncApp(token=self.bot_token)
        
        @self.app.event("app_mention")
        async def handle_app_mention(body, client, logger_bolt):
            """处理 @ 提及"""
            event = body["event"]
            channel = event["channel"]
            thread_ts = event.get("thread_ts") or event["ts"]
            user_id = event["user"]
            
            # 提取文本
            text = event.get("text", "")
            
            # 移除 bot mention
            text = re.sub(r"<@[^>]+>", "", text)
            
            # 提取图片（如果有）
            files = event.get("files", [])
            image_urls = []
            for f in files:
                if "url_private" in f:
                    image_urls.append(f["url_private"])
            
            # 处理消息
            response = await self.run_agent(
                user_id=user_id,
                text=text,
                images=image_urls,
            )
            
            # 提取内部内容
            _, final_response = extract_internal_content(response)
            
            # 发送响应
            try:
                await client.chat_postMessage(
                    channel=channel,
                    text=final_response,
                    thread_ts=thread_ts
                )
            except Exception as e:
                logger.error(f"发送消息失败: {e}")
                await client.chat_postMessage(
                    channel=channel,
                    text=f"发送失败: {e}",
                    thread_ts=thread_ts
                )
        
        self.handler = AsyncSocketModeHandler(self.app, self.app_token)
        set_status("slack", "starting")
        try:
            await self.handler.start_async()
            set_status("slack", "connected")
            logger.info("Slack Bot 已启动")
        except Exception as e:
            set_status("slack", "error", str(e))
            raise
    
    async def stop(self):
        """停止 Slack Bot"""
        if self.handler:
            await self.handler.stop_async()
        set_status("slack", "disabled")
        logger.info("Slack Bot 已停止")


def create_slack_channel(agent, bot_token: str, app_token: str) -> SlackChannel:
    """创建 Slack 渠道实例"""
    return SlackChannel(agent, bot_token, app_token)
