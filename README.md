# ADK Claw 🦞

> 第一个基于原生 Google ADK 的开源 AI Agent 平台

## 特点

- ✅ **原生 ADK** - 使用 Google Agent Development Kit
- ✅ **多模型支持** - Gemini / GPT / Claude / DeepSeek / Ollama
- ✅ **多渠道** - Slack / Telegram（更多即将推出）
- ✅ **本地运行** - 零成本，数据不出本地
- ✅ **Web 配置界面** - 无需编辑配置文件
- ✅ **OAuth 支持** - 集成 Google Workspace

## 快速开始

### 1. 安装

```bash
cd adk-claw
pip install -r requirements.txt
```

### 2. 启动 Web UI

```bash
python main.py --web
```

打开 http://localhost:8080

### 3. 配置

在 Web UI 中配置：

1. **选择模型** - Gemini（免费）/ GPT-4o / Claude
2. **输入 API Key** - 至少配置一个
3. **连接渠道** - Slack 或 Telegram

### 4. 启动 Bot

```bash
# Slack
python main.py --slack

# Telegram
python main.py --telegram

# 全部
python main.py --all
```

## 渠道配置

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
7. 复制 Tokens 到 Web UI

### Telegram

1. Telegram 搜索 @BotFather
2. 发送 `/newbot`
3. 按提示创建
4. 复制 Token 到 Web UI

## 换模型

在 Web UI 选择，或编辑 `~/.adk-claw/config.json`：

```json
{
  "model": "gemini-2.5-flash"
}
```

支持的模型：
- `gemini-2.5-flash`（推荐，免费）
- `openai/gpt-4o`
- `anthropic/claude-3.5-sonnet`
- `deepseek/deepseek-chat`
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
| 开源 | ✅ MIT | ✅ | ✅ |

## 路线图

- [x] MVP - Slack/Telegram 支持
- [x] Web 配置界面
- [x] 多模型支持
- [x] 记忆系统（SQLite + FTS）
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

### 记忆工具

| 工具 | 用途 |
|------|------|
| `remember` | 记住信息 |
| `recall` | 回忆信息 |
| `forget` | 忘记信息 |
| `get_memory_stats` | 查看统计 |

### 存储位置

```
~/.adk-claw/memory.db
```

### 手动管理

可以编辑 `MEMORY.md` 或 `memory/*.md`，然后运行：

```python
from memory import memory_manager
memory_manager.load_memory_files("/path/to/workspace")
```

## 开发

```bash
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
