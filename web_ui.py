"""
Web UI 启动
===========
"""

import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from config import config

app = FastAPI(title="ADK Claw")

TEMPLATES_DIR = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """主页"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "config": config.config,
        "has_google_key": bool(config.get_google_api_key()),
        "has_openai_key": bool(config.get_openai_api_key()),
        "has_anthropic_key": bool(config.get_anthropic_api_key()),
        "slack_enabled": config.is_slack_enabled(),
        "telegram_enabled": config.is_telegram_enabled(),
    })


@app.post("/api/model")
async def set_model(model: str = Form(...)):
    """设置模型"""
    config.set_model(model)
    return RedirectResponse(url="/?saved=model", status_code=303)


@app.post("/api/google-key")
async def set_google_key(api_key: str = Form(...)):
    """设置 Google API Key"""
    config.set_google_api_key(api_key)
    return RedirectResponse(url="/?saved=google", status_code=303)


@app.post("/api/openai-key")
async def set_openai_key(api_key: str = Form(...)):
    """设置 OpenAI API Key"""
    config.set_openai_api_key(api_key)
    return RedirectResponse(url="/?saved=openai", status_code=303)


@app.post("/api/anthropic-key")
async def set_anthropic_key(api_key: str = Form(...)):
    """设置 Anthropic API Key"""
    config.set_anthropic_api_key(api_key)
    return RedirectResponse(url="/?saved=anthropic", status_code=303)


@app.post("/api/slack")
async def set_slack(bot_token: str = Form(...), app_token: str = Form(...)):
    """设置 Slack"""
    config.set_slack_tokens(bot_token, app_token)
    return RedirectResponse(url="/?saved=slack", status_code=303)


@app.post("/api/telegram")
async def set_telegram(token: str = Form(...)):
    """设置 Telegram"""
    config.set_telegram_token(token)
    return RedirectResponse(url="/?saved=telegram", status_code=303)


@app.post("/api/google-oauth")
async def set_google_oauth(client_id: str = Form(...), client_secret: str = Form(...)):
    """设置 Google OAuth"""
    config.set_google_oauth(client_id, client_secret)
    return RedirectResponse(url="/?saved=oauth", status_code=303)


def start_web_ui(host: str = "localhost", port: int = 8080):
    """启动 Web UI"""
    print(f"🌐 Web UI: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="warning")


if __name__ == "__main__":
    start_web_ui()
