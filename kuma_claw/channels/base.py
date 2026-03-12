"""
Kuma Claw - 渠道基类
==================

所有渠道的公共逻辑（会话管理、Agent 运行）
"""

import logging
from typing import Dict, List, Optional, Tuple
from abc import ABC, abstractmethod

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

logger = logging.getLogger("kuma_claw.channels")


# ============================================
# 会话管理
# ============================================

class SessionManager:
    """统一的会话管理器"""

    def __init__(self, app_name: str = "kuma-claw"):
        self.app_name = app_name
        self.session_service = InMemorySessionService()
        self.user_sessions: Dict[str, str] = {}

    async def get_or_create_session(self, user_id: str) -> str:
        """获取或创建用户会话

        Args:
            user_id: 用户 ID

        Returns:
            会话 ID
        """
        if user_id not in self.user_sessions:
            try:
                session = await self.session_service.create_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    state={}
                )

                # 获取 session id
                session_id = session.id if hasattr(session, 'id') else str(session)
                self.user_sessions[user_id] = session_id
                logger.debug(f"创建新会话: user={user_id}, session={session_id}")

            except Exception as e:
                logger.error(f"创建会话失败: {e}")
                raise

        return self.user_sessions[user_id]

    async def clear_session(self, user_id: str) -> bool:
        """清除用户会话

        Args:
            user_id: 用户 ID

        Returns:
            是否成功
        """
        if user_id in self.user_sessions:
            session_id = self.user_sessions[user_id]
            try:
                await self.session_service.delete_session(
                    app_name=self.app_name,
                    user_id=user_id,
                    session_id=session_id
                )
                del self.user_sessions[user_id]
                logger.debug(f"清除会话: user={user_id}")
                return True
            except Exception as e:
                logger.error(f"清除会话失败: {e}")
                return False
        return False


# ============================================
# Agent 运行器
# ============================================

async def run_agent_with_session(
    runner: Runner,
    session_manager: SessionManager,
    user_id: str,
    parts: List[types.Part],
) -> str:
    """运行 Agent 并返回响应

    Args:
        runner: ADK Runner 实例
        session_manager: 会话管理器
        user_id: 用户 ID
        parts: 消息部分列表

    Returns:
        Agent 响应文本
    """
    try:
        session_id = await session_manager.get_or_create_session(user_id)

        content = types.Content(
            role="user",
            parts=parts
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

    except Exception as e:
        logger.error(f"运行 Agent 失败: {e}")
        return f"处理请求时出错: {str(e)}"


# ============================================
# 渠道基类
# ============================================

class ChannelHandler(ABC):
    """渠道处理器基类"""

    def __init__(self, channel_name: str, agent):
        self.channel_name = channel_name
        self.agent = agent
        self.session_manager = SessionManager()

        # 创建 Runner
        self.runner = Runner(
            app_name="kuma-claw",
            agent=agent,
            session_service=self.session_manager.session_service,
        )

        logger.info(f"{channel_name} 渠道已初始化")

    @abstractmethod
    async def handle_message(self, user_id: str, text: str, **kwargs) -> str:
        """处理消息（子类实现）

        Args:
            user_id: 用户 ID
            text: 消息文本
            **kwargs: 渠道特定参数

        Returns:
            响应文本
        """
        pass

    @abstractmethod
    async def start(self):
        """启动渠道（子类实现）"""
        pass

    @abstractmethod
    async def stop(self):
        """停止渠道（子类实现）"""
        pass

    async def run_agent(
        self,
        user_id: str,
        text: str,
        images: List[Tuple[bytes, str]] = None
    ) -> str:
        """运行 Agent（公共逻辑）

        Args:
            user_id: 用户 ID
            text: 消息文本
            images: 图片列表，格式为 [(bytes, mime_type), ...]
                   例如: [(b'\x89PNG...', 'image/png'), (b'\xff\xd8...', 'image/jpeg')]

        Returns:
            Agent 响应
        """
        parts = [types.Part(text=text)]

        # 添加图片（如果有）
        if images:
            for img_bytes, mime_type in images:
                if not isinstance(img_bytes, bytes):
                    logger.warning(f"图片数据类型错误: {type(img_bytes)}，跳过")
                    continue

                parts.append(types.Part(
                    inline_data=types.Blob(
                        mime_type=mime_type,
                        data=img_bytes
                    )
                ))

        return await run_agent_with_session(
            runner=self.runner,
            session_manager=self.session_manager,
            user_id=user_id,
            parts=parts,
        )
