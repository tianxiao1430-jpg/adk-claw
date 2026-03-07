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
# 可用模型列表
# ============================================

AVAILABLE_MODELS = {
    "Gemini 3.1 (最新)": [
        ("gemini-3.1-pro", "🧠 最强智能，复杂问题，代码生成"),
        ("gemini-3.1-flash", "⚡ 快速高效（推荐）"),
        ("gemini-3.1-flash-lite-preview", "💨 极低成本，高性能"),
    ],
"Gemini 3 (预览版)": [
        ("gemini-3-pro", "🔬 最先进多模态理解"),
        ("gemini-3-flash", "⚡ 极低成本卓越性能"),
    ],
    "Nano Banana (轻量)": [
        ("nano-banana-2", "🍌 高速大容量"),
        ("nano-banana-pro", "🍌 复杂任务支持"),
    ],
    "Gemini 2.0": [
        ("gemini-2.0-flash", "🚀 稳定快速响应"),
        ("gemini-2.0-flash-lite-preview", "💨 轻量版极速响应"),
        ("gemini-2.0-pro-exp", "🔬 实验版前沿功能"),
    ],
    "Gemini 1.5 (经典)": [
        ("gemini-1.5-flash", "📦 稳定可靠"),
        ("gemini-1.5-flash-8b", "📦 经济版成本优化"),
        ("gemini-1.5-pro", "📦 经典强大能力"),
    ],
    "GPT (OpenAI)": [
        ("openai/gpt-4.1", "🆕 最新 GPT-4.1"),
        ("openai/gpt-4.1-mini", "🆕 GPT-4.1 Mini"),
        ("openai/gpt-4.1-nano", "🆕 GPT-4.1 Nano"),
        ("openai/gpt-4o", "🎯 GPT-4 Omni"),
        ("openai/gpt-4o-mini", "⚡ GPT-4 Omni Mini"),
        ("openai/o3-mini", "🧠 O3 Mini 推理模型"),
    ],
    "Claude (Anthropic)": [
        ("anthropic/claude-3.7-sonnet", "🆕 最新 Claude 3.7 Sonnet"),
        ("anthropic/claude-3.5-sonnet", "🎯 Claude 3.5 Sonnet"),
        ("anthropic/claude-3.5-haiku", "⚡ Claude 3.5 Haiku"),
    ],
    "DeepSeek": [
        ("deepseek/deepseek-chat", "💬 DeepSeek Chat"),
        ("deepseek/deepseek-reasoner", "🧠 DeepSeek Reasoner"),
    ],
    "本地模型 (Ollama)": [
        ("ollama/llama3.3", "🦙 Llama 3.3"),
        ("ollama/llama3.2", "🦙 Llama 3.2"),
        ("ollama/qwen2.5", "🌟 Qwen 2.5"),
        ("ollama/deepseek-r1", "🧠 DeepSeek R1"),
        ("ollama/gemma3", "💎 Gemma 3"),
    ],
}


def get_all_models_flat():
    """获取扁平化的模型列表"""
    models = []
    for provider, model_list in AVAILABLE_MODELS.items():
        models.extend(model_list)
    return models


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
    from .config import config as app_config

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
            token = Prompt.ask("Telegram Bot Token")
            if token:
                app_config.set_telegram_token(token)
                console.print("[green]✅ Telegram 已配置[/green]")

        # Slack
        slack_enabled = app_config.is_slack_enabled()
        status = "✅ 已启用" if slack_enabled else "❌ 未配置"
        console.print(f"Slack: {status}")

        if Confirm.ask("配置 Slack？", default=False):
            bot_token = Prompt.ask("Slack Bot Token (xoxb-...)")
            app_token = Prompt.ask("Slack App Token (xapp-...)")
            if bot_token and app_token:
                app_config.set_slack_tokens(bot_token, app_token)
                console.print("[green]✅ Slack 已配置[/green]")

        console.print()

    # Model
    if section in ["model", "all"]:
        run_model_selection(app_config)


def run_model_selection(app_config):
    """运行模型选择向导"""
    console.print("[bold]🤖 模型配置[/bold]")
    console.print("[dim]选择 AI 模型（按数字选择）[/dim]")
    console.print()

    current = app_config.get_model()

    # 显示所有模型
    idx = 1
    model_map = {}

    for provider, models in AVAILABLE_MODELS.items():
        console.print(f"[bold yellow]{provider}[/bold yellow]")
        for model_id, desc in models:
            marker = " ✓" if model_id == current else ""
            console.print(f"  [cyan]{idx:2d}[/cyan]. {model_id:35s} [dim]{desc}[/dim]{marker}")
            model_map[idx] = model_id
            idx += 1
        console.print()

    # 选择
    choice = Prompt.ask(f"选择模型 (当前: {current})", default="1")

    try:
        selected_idx = int(choice)
        if selected_idx in model_map:
            selected_model = model_map[selected_idx]
            app_config.set_model(selected_model)
            console.print(f"[green]✅ 模型已设置为 {selected_model}[/green]")
    except ValueError:
        console.print("[yellow]无效选择，保持当前模型[/yellow]")

    console.print()


@cli.command()
@click.option("--web", is_flag=True, help="启动 Web UI")
@click.option("--slack", is_flag=True, help="启动 Slack Bot")
@click.option("--telegram", is_flag=True, help="启动 Telegram Bot")
@click.option("--all", "all_services", is_flag=True, help="启动所有服务")
@click.option("--port", default=8080, help="Web UI 端口")
def run(web: bool, slack: bool, telegram: bool, all_services: bool, port: int):
    """启动服务"""
    from .main import main as run_main

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

    # 调用 main.py（同步调用，不用 asyncio）
    sys.argv = ["main.py"] + args
    run_main()


@cli.command()
def doctor():
    """健康检查（类似 openclaw doctor）"""
    print_banner()
    console.print()

    from .config import config as app_config

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
    from . import __version__
    console.print(f"[bold cyan]ADK Claw[/bold cyan] v{__version__}")


@cli.command("list-models")
def list_models():
    """列出所有可用模型"""
    console.print(Panel.fit(
        "[bold cyan]🤖 可用模型列表[/bold cyan]",
        border_style="cyan"
    ))
    console.print()

    for provider, models in AVAILABLE_MODELS.items():
        console.print(f"[bold yellow]{provider}[/bold yellow]")
        table = Table(show_header=False, box=None, padding=(0, 2))
        for model_id, desc in models:
            table.add_row(f"[cyan]{model_id}[/cyan]", f"[dim]{desc}[/dim]")
        console.print(table)
        console.print()


# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    cli()
