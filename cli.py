"""
ADK Claw - CLI 入口
==================

类似 OpenClaw 的安装体验：
- adk-claw init    # 初始化配置
- adk-claw config  # 配置向导
- adk-claw run     # 启动服务（旧方式）
- adk-claw gateway # 启动网关（新方式）
- adk-claw doctor  # 健康检查
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

console = Console()


def print_banner():
    """打印 Banner"""
    console.print(Panel.fit(
        "[bold cyan]🦞 ADK Claw[/bold cyan] - 智能 Agent 平台\n\n"
        "[dim]基于 Google ADK | 多模型支持 | 本地部署[/dim]",
        border_style="cyan"
    ))


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        console.print("[red]❌ Python 3.10+ required[/red]")
        return False
    console.print(f"[green]✅ Python {version.major}.{version.minor}.{version.micro}[/green]")
    return True


def check_dependencies():
    """检查依赖"""
    deps = {
        "google-adk": "google.genai",
        "slack-bolt": "slack_bolt",
        "python-telegram-bot": "telegram",
        "fastapi": "fastapi",
        "websockets": "websockets",
    }

    missing = []
    for name, module in deps.items():
        try:
            __import__(module.split(".")[0])
            console.print(f"[green]  ✅ {name}[/green]")
        except ImportError:
            console.print(f"[yellow]  ⚠️  {name} (未安装)[/yellow]")
            missing.append(name)

    return missing


# ============================================
# Commands
# ============================================

@click.group()
def cli():
    """ADK Claw - 智能 Agent 平台"""
    pass


@cli.command()
@click.option("--non-interactive", is_flag=True, help="非交互模式")
def init(non_interactive: bool):
    """初始化配置（类似 openclaw setup）"""
    print_banner()
    console.print()

    # 1. 检查 Python 版本
    console.print("[bold]📋 检查环境...[/bold]")
    if not check_python_version():
        sys.exit(1)
    console.print()

    # 2. 检查依赖
    console.print("[bold]📦 检查依赖...[/bold]")
    missing = check_dependencies()
    if missing:
        console.print()
        if non_interactive:
            console.print(f"[yellow]缺少依赖: {', '.join(missing)}[/yellow]")
            console.print("运行: [cyan]pip install -r requirements.txt[/cyan]")
            sys.exit(1)

        if Confirm.ask(f"是否安装缺失的依赖？"):
            console.print("[cyan]安装依赖中...[/cyan]")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    console.print()

    # 3. 配置向导
    if not non_interactive:
        run_config_wizard()

    console.print()
    console.print(Panel.fit(
        "[green]✅ 初始化完成！[/green]\n\n"
        "[cyan]下一步：[/cyan]\n"
        "  [bold]adk-claw gateway[/bold]        启动网关（推荐）\n"
        "  [bold]adk-claw run --web[/bold]      启动 Web UI\n"
        "  [bold]adk-claw run --telegram[/bold] 启动 Telegram Bot",
        title="🎉 安装成功",
        border_style="green"
    ))


@cli.command()
@click.option("--section", type=click.Choice(["api", "channels", "model", "all"]), default="all")
def config(section: str):
    """配置向导（类似 openclaw configure）"""
    print_banner()
    run_config_wizard(section)


def run_config_wizard(section: str = "all"):
    """运行配置向导"""
    from config import config as app_config

    # API Keys
    if section in ["api", "all"]:
        console.print("[bold]🔑 API 配置[/bold]")
        console.print("[dim]至少配置一个 API Key[/dim]")
        console.print()

        # Google
        current = "已配置" if app_config.get_google_api_key() else "未配置"
        google_key = Prompt.ask(
            f"Google API Key [{current}]",
            default="",
            show_default=False
        )
        if google_key:
            app_config.set_google_api_key(google_key)
            console.print("[green]✅ Google API Key 已保存[/green]")

        # OpenAI (可选)
        openai_key = Prompt.ask(
            f"OpenAI API Key (可选)",
            default="",
            show_default=False
        )
        if openai_key:
            app_config.set_openai_api_key(openai_key)
            console.print("[green]✅ OpenAI API Key 已保存[/green]")

        console.print()

    # Channels
    if section in ["channels", "all"]:
        console.print("[bold]📱 渠道配置[/bold]")
        console.print("[dim]至少配置一个渠道[/dim]")
        console.print()

        # Telegram
        telegram_enabled = app_config.is_telegram_enabled()
        status = "✅ 已启用" if telegram_enabled else "❌ 未配置"
        console.print(f"Telegram: {status}")

        if Confirm.ask("配置 Telegram？", default=not telegram_enabled):
            token = Prompt.ask("Telegram Bot Token", password=True)
            if token:
                app_config.set_telegram_token(token)
                console.print("[green]✅ Telegram 已配置[/green]")

        # Slack
        slack_enabled = app_config.is_slack_enabled()
        status = "✅ 已启用" if slack_enabled else "❌ 未配置"
        console.print(f"Slack: {status}")

        if Confirm.ask("配置 Slack？", default=False):
            bot_token = Prompt.ask("Slack Bot Token (xoxb-...)", password=True)
            app_token = Prompt.ask("Slack App Token (xapp-...)", password=True)
            if bot_token and app_token:
                app_config.set_slack_tokens(bot_token, app_token)
                console.print("[green]✅ Slack 已配置[/green]")

        console.print()

    # Model
    if section in ["model", "all"]:
        console.print("[bold]🤖 模型配置[/bold]")

        models = [
            ("gemini-2.5-flash", "Google Gemini 2.5 Flash (推荐)"),
            ("gemini-2.5-pro", "Google Gemini 2.5 Pro"),
            ("gpt-4o", "OpenAI GPT-4o"),
            ("claude-3-5-sonnet", "Anthropic Claude 3.5 Sonnet"),
        ]

        table = Table(show_header=False)
        for i, (model, desc) in enumerate(models, 1):
            table.add_row(f"[cyan]{i}[/cyan]", model, f"[dim]{desc}[/dim]")
        console.print(table)

        current = app_config.get_model()
        choice = Prompt.ask(f"选择模型 (当前: {current})", default="1")

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                app_config.set_model(models[idx][0])
                console.print(f"[green]✅ 模型已设置为 {models[idx][0]}[/green]")
        except ValueError:
            pass

        console.print()


@cli.command()
@click.option("--web", is_flag=True, help="启动 Web UI")
@click.option("--slack", is_flag=True, help="启动 Slack Bot")
@click.option("--telegram", is_flag=True, help="启动 Telegram Bot")
@click.option("--all", "all_services", is_flag=True, help="启动所有服务")
@click.option("--port", default=8080, help="Web UI 端口")
def run(web: bool, slack: bool, telegram: bool, all_services: bool, port: int):
    """启动服务（旧方式，直接启动各渠道）"""
    from main import main as run_main

    # 构建参数
    args = []
    if web or all_services:
        args.append("--web")
        args.extend(["--port", str(port)])
    if slack or all_services:
        args.append("--slack")
    if telegram or all_services:
        args.append("--telegram")
    if all_services:
        args.append("--all")

    if not args:
        args = ["--web"]

    # 调用 main.py
    sys.argv = ["main.py"] + args
    asyncio.run(run_main())


@cli.command()
@click.option("--host", default="0.0.0.0", help="网关监听地址")
@click.option("--port", default=19001, help="网关端口")
@click.option("--web-port", default=8080, help="Web UI 端口")
@click.option("--config", "config_path", help="配置文件路径")
@click.option("--daemon", is_flag=True, help="后台运行")
def gateway(host: str, port: int, web_port: int, config_path: Optional[str], daemon: bool):
    """启动网关（类似 openclaw gateway）"""
    print_banner()
    console.print()

    from config import config as app_config

    # 检查配置
    has_api = bool(app_config.get_google_api_key())
    if not has_api:
        console.print("[red]❌ 请先配置 API Key: adk-claw config[/red]")
        sys.exit(1)

    console.print("[bold]🚀 启动网关...[/bold]")
    console.print(f"   地址: [cyan]{host}:{port}[/cyan]")
    console.print(f"   Web UI: [cyan]http://localhost:{web_port}[/cyan]")
    console.print()

    async def run_gateway():
        from gateway import Gateway, ChannelType
        from gateway.adapters import TelegramAdapter, WebAdapter

        # 创建网关
        gw = Gateway(config_path)

        # 注册适配器
        if app_config.is_telegram_enabled():
            telegram = TelegramAdapter(gw, app_config.get_telegram_token())
            gw.register_adapter(ChannelType.TELEGRAM, telegram)
            console.print("[green]✅ Telegram 已连接[/green]")

        # 注册 Web 适配器
        web = WebAdapter(gw, host=host, port=web_port)
        gw.register_adapter(ChannelType.WEB, web)
        console.print(f"[green]✅ Web UI 已启动: http://localhost:{web_port}[/green]")

        # 启动所有适配器
        for channel, adapter in gw.adapters.items():
            await adapter.start()

        console.print()
        console.print(Panel.fit(
            "[green]✅ 网关运行中[/green]\n\n"
            "[dim]按 Ctrl+C 停止[/dim]",
            border_style="green"
        ))

        # 保持运行
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            console.print("\n[yellow]正在停止...[/yellow]")
            for adapter in gw.adapters.values():
                await adapter.stop()

    try:
        asyncio.run(run_gateway())
    except KeyboardInterrupt:
        console.print("[green]👋 再见！[/green]")


@cli.command()
def doctor():
    """健康检查（类似 openclaw doctor）"""
    print_banner()
    console.print()

    from config import config as app_config

    issues = []

    # Python
    console.print("[bold]📋 环境[/bold]")
    check_python_version()
    console.print()

    # Dependencies
    console.print("[bold]📦 依赖[/bold]")
    missing = check_dependencies()
    if missing:
        issues.append(f"缺少依赖: {', '.join(missing)}")
    console.print()

    # Config
    console.print("[bold]⚙️  配置[/bold]")

    # API Keys
    has_api = bool(app_config.get_google_api_key() or
                   app_config.get_openai_api_key() or
                   app_config.get_anthropic_api_key())
    if has_api:
        console.print("[green]  ✅ API Key 已配置[/green]")
    else:
        console.print("[red]  ❌ API Key 未配置[/red]")
        issues.append("API Key 未配置")

    # Channels
    has_channel = app_config.is_telegram_enabled() or app_config.is_slack_enabled()
    if has_channel:
        console.print("[green]  ✅ 渠道已配置[/green]")
    else:
        console.print("[yellow]  ⚠️  渠道未配置[/yellow]")
        issues.append("渠道未配置（仅 Web UI 可用）")

    console.print()

    # Summary
    if issues:
        console.print(Panel.fit(
            "[yellow]⚠️  发现问题：[/yellow]\n" + "\n".join(f"  • {i}" for i in issues),
            title="诊断结果",
            border_style="yellow"
        ))
        console.print()
        console.print("[cyan]修复建议：[/cyan]")
        console.print("  [bold]adk-claw config[/bold]  运行配置向导")
    else:
        console.print(Panel.fit(
            "[green]✅ 所有检查通过！[/green]",
            title="诊断结果",
            border_style="green"
        ))


@cli.command()
def version():
    """显示版本"""
    console.print("[bold cyan]ADK Claw[/bold cyan] v0.1.0")


# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    cli()
