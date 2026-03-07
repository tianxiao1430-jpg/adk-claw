# ADK Claw 🦞

> 第一个基于原生 Google ADK 的开源 AI Agent 平台

## 特点

- ✅ **原生 ADK** - 使用 Google Agent Development Kit
- ✅ **多模型支持** - Gemini / GPT / Claude / DeepSeek / Ollama
- ✅ **多渠道** - Slack / Telegram（更多即将推出）
- ✅ **本地运行** - 零成本，数据不出本地
- ✅ **交互式安装** - 类似 OpenClaw 的配置向导
- ✅ **Web 配置界面** - 无需编辑配置文件
- ✅ **OAuth 支持** - 集成 Google Workspace

## 快速开始

### 方式一：pip 安装（推荐）

```bash
pip install adk-claw
adk-claw init
```

### 方式二：从源码安装

```bash
git clone https://github.com/tianxiao/adk-claw.git
cd adk-claw
pip install -e .
adk-claw init
```

### 初始化向导

运行 `adk-claw init` 后，会进入交互式配置：

```
🦞 ADK Claw - 智能 Agent 平台

📋 检查环境...
✅ Python 3.12.0

📦 检查依赖...
  ✅ google-adk
  ✅ slack-bolt
  ✅ python-telegram-bot
  ✅ fastapi

🔑 API 配置
至少配置一个 API Key

Google API Key [未配置]: ********************************
✅ Google API Key 已保存

📱 渠道配置
至少配置一个渠道

Telegram: ❌ 未配置
配置 Telegram？ [y/N]: y
Telegram Bot Token: ********************************
✅ Telegram 已配置

🤖 模型配置
 1  gemini-3.1-flash   Google Gemini 3.1 Flash (推荐)
 2  gemini-3.1-pro     Google Gemini 3.1 Pro
 3  gpt-4o             OpenAI GPT-4o
 4  claude-3-5-sonnet  Anthropic Claude 3.5 Sonnet

选择模型 (当前: gemini-3.1-flash) [1]: 1
✅ 模型已设置为 gemini-3.1-flash

🎉 安装成功

✅ 初始化完成！

下一步：
  adk-claw run --web      启动 Web UI
  adk-claw run --telegram 启动 Telegram Bot
  adk-claw run --all      启动所有服务
```

## CLI 命令

| 命令 | 说明 | 类似 OpenClaw |
|------|------|--------------|
| `adk-claw init` | 初始化配置 | `openclaw setup` |
| `adk-claw config` | 配置向导 | `openclaw configure` |
| `adk-claw doctor` | 健康检查 | `openclaw doctor` |
| `adk-claw run` | 启动服务 | `openclaw gateway` |
| `adk-claw version` | 显示版本 | `openclaw --version` |

### 详细用法

```bash
# 初始化
adk-claw init                  # 交互式
adk-claw init --non-interactive

# 配置
adk-claw config                # 全部配置
adk-claw config --section api  # 仅 API
adk-claw config --section channels  # 仅渠道
adk-claw config --section model     # 仅模型

# 健康检查
adk-claw doctor

# 运行
adk-claw run --web             # Web UI (localhost:8080)
adk-claw run --telegram        # Telegram Bot
adk-claw run --slack           # Slack Bot
adk-claw run --all             # 所有服务
adk-claw run --web --port 3000 # 自定义端口
```

## 渠道配置

### Telegram

1. Telegram 搜索 @BotFather
2. 发送 `/newbot`
3. 按提示创建
4. 复制 Token

```bash
adk-claw config --section channels
# 选择配置 Telegram，粘贴 Token
```

### Slack

1. 访问 https://api.slack.com/apps
2. Create New App → From scratch
3. **OAuth & Permissions** → 添加：
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
4. **Socket Mode** → Enable → 生成 App Token
5. **Event Subscriptions** → `app_mention`
6. Install to Workspace
7. 复制 Tokens

```bash
adk-claw config --section channels
# 选择配置 Slack，粘贴 Bot Token 和 App Token
```

## 换模型

```bash
adk-claw config --section model
```

或编辑 `~/.adk-claw/config.json`：

```json
{
  "model": "gemini-3.1-flash"
}
```

支持的模型：
- `gemini-3.1-flash`（推荐，免费）
- `gemini-3.1-flash-lite`（极低成本）
- `gemini-3.1-pro`
- `gpt-4o`
- `claude-3-5-sonnet`
- `deepseek-chat`
- `ollama/llama3.1`（本地）

## 添加工具

编辑 `agent.py`：

```python
def my_tool(param: str) -> str:
    """工具描述"""
    return "结果"

TOOLS.append(FunctionTool(func=my_tool))
```

## 架构

```
┌─────────────────────────────────────────────┐
│  CLI (adk-claw init/config/run)             │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│  Web UI (localhost:8080)                    │
│  - 配置 API Keys                            │
│  - OAuth 认证                               │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│  ADK Claw Core                              │
│  - Google ADK Agent                         │
│  - 多渠道适配器                             │
└────────┬────────────────────┬───────────────┘
         ↓                    ↓
    Slack (Socket)      Telegram (Polling)
```

## 与其他方案对比

| 维度 | ADK Claw | OpenClaw | PocketPaw |
|------|----------|----------|-----------|
| 基础技术 | 原生 ADK | Anthropic | 多后端 |
| 多模型 | ✅ 100+ | ❌ 仅 Claude | ✅ |
| Google 生态 | ✅ 深度集成 | ⚠️ 需配置 | ⚠️ 假 ADK |
| 本地部署 | ✅ 完全本地 | ✅ | ✅ |
| 安装体验 | ✅ 交互式 | ✅ 交互式 | ⚠️ 手动 |
| 开源 | ✅ MIT | ✅ | ✅ |

## 路线图

- [x] MVP - Slack/Telegram 支持
- [x] Web 配置界面
- [x] 多模型支持
- [x] 记忆系统（SQLite + FTS）
- [x] CLI 安装向导
- [ ] 向量搜索（嵌入向量）
- [ ] 图片理解
- [ ] 更多工具（Gmail/Calendar/Drive）
- [ ] Cloud Run 部署
- [ ] 更多渠道（Discord/WhatsApp）

## 记忆系统

ADK Claw 内置记忆系统，可以记住和回忆信息：

```
用户：记住我喜欢简洁的回复
Bot：✅ 已记住：你喜欢简洁的回复

用户：我喜欢什么？
Bot：📚 相关记忆：
- 你喜欢简洁的回复
```

### 存储位置

```
~/.adk-claw/
├── config.json      # 配置
├── secrets.json     # 密钥
└── memory.db        # 记忆数据库
```

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
ruff format .

# 类型检查
mypy .
```

## 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT

---

**ADK Claw** - 第一个原生 ADK Agent 平台 🦞
