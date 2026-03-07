"""
ADK Claw - 主入口
================
"""

import os
import sys
import asyncio
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import config


def check_requirements():
    """检查必要配置"""
    missing = []
    
    # 至少需要一个渠道
    has_slack = bool(config.get_slack_bot_token())
    has_telegram = bool(config.get_telegram_token())
    
    if not has_slack and not has_telegram:
        missing.append("至少配置一个渠道（Slack 或 Telegram）")
    
    # 至少需要一个 API Key
    has_google = bool(config.get_google_api_key())
    has_openai = bool(config.get_openai_api_key())
    has_anthropic = bool(config.get_anthropic_api_key())
    
    if not has_google and not has_openai and not has_anthropic:
        missing.append("至少配置一个 API Key（Google/OpenAI/Anthropic）")
    
    return missing


def print_banner():
    """打印 Banner"""
    print("""
╔════════════════════════════════════════════════════════════╗
║          🦞 ADK Claw - 智能 Agent 平台                    ║
║                                                            ║
║  基于 Google ADK | 多模型支持 | 本地部署                  ║
╚════════════════════════════════════════════════════════════╝
    """)


def print_status():
    """打印状态"""
    print("📊 当前状态:")
    print(f"   模型: {config.get_model()}")
    print(f"   Slack: {'✅ 已配置' if config.get_slack_bot_token() else '❌ 未配置'}")
    print(f"   Telegram: {'✅ 已配置' if config.get_telegram_token() else '❌ 未配置'}")
    print()


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ADK Claw")
    parser.add_argument("--web", action="store_true", help="启动 Web UI")
    parser.add_argument("--slack", action="store_true", help="启动 Slack Bot")
    parser.add_argument("--telegram", action="store_true", help="启动 Telegram Bot")
    parser.add_argument("--all", action="store_true", help="启动所有服务")
    parser.add_argument("--port", type=int, default=8080, help="Web UI 端口")
    args = parser.parse_args()
    
    print_banner()
    print_status()
    
    # 如果没有指定任何参数，启动 Web UI
    if not args.web and not args.slack and not args.telegram and not args.all:
        print("💡 使用 --help 查看帮助")
        print("🌐 启动 Web UI 进行配置...")
        args.web = True
    
    # 检查配置
    if args.slack or args.telegram or args.all:
        missing = check_requirements()
        if missing:
            print("❌ 配置不完整：")
            for m in missing:
                print(f"   - {m}")
            print("\n💡 请先通过 Web UI 配置: python main.py --web")
            sys.exit(1)
    
    tasks = []
    
    # Web UI
    if args.web or args.all:
        from web_ui import start_web_ui
        import threading
        web_thread = threading.Thread(
            target=start_web_ui,
            kwargs={"port": args.port},
            daemon=True
        )
        web_thread.start()
        print(f"🌐 Web UI: http://localhost:{args.port}")
    
    # Slack
    if args.slack or args.all:
        if config.get_slack_bot_token():
            from slack_handler import start as start_slack
            import threading
            slack_thread = threading.Thread(target=start_slack, daemon=True)
            slack_thread.start()
            print("💬 Slack Bot 已启动")
        else:
            print("⚠️  Slack 未配置，跳过")
    
    # Telegram
    if args.telegram or args.all:
        token = config.get_telegram_token()
        if token:
            from telegram_handler import start_telegram
            app = start_telegram(token)
            if app:
                print("📱 Telegram Bot 已启动")
                # Telegram 需要在主线程运行
                app.run_polling(allowed_updates=Update.ALL_TYPES)
        else:
            print("⚠️  Telegram 未配置，跳过")
    
    # 如果只启动了 Web，保持运行
    if args.web and not args.slack and not args.telegram:
        print("\n✅ ADK Claw 运行中...")
        print("   按 Ctrl+C 退出")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 再见！")


if __name__ == "__main__":
    from telegram import Update
    asyncio.run(main())
