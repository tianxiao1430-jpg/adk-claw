# ADK Claw 🦞

> **Native Google ADK Agent Platform**
> **基于原生 Google ADK 的 AI Agent 平台**
> **ネイティブ Google ADK エージェントプラットフォーム**

[English](#english) | [中文](#中文) | [日本語](#日本語)

---

<a name="english"></a>
## English

### The First Native Google ADK Agent Platform

ADK Claw is the first open-source AI agent platform built on native Google Agent Development Kit (ADK). Designed for seamless integration with Google Workspace and Google Cloud Platform.

### ✨ Key Features

#### 🚀 Native ADK Advantages
- **100% Native ADK** - Built on Google's official Agent Development Kit
- **Google Workspace Integration** - Native support for Gmail, Calendar, Sheets, Docs
- **GCP Optimized** - Seamless deployment on Cloud Run, Vertex AI integration
- **Multi-Model Support** - Gemini / GPT / Claude / DeepSeek / Ollama
- **Multi-Channel** - Slack / Telegram (more coming soon)
- **Zero Configuration** - One-click OAuth for Google Workspace

#### 🔗 Google Ecosystem Integration

**Google Workspace (One-Click Setup)**
```
✅ Gmail          - Send, read, compose emails
✅ Calendar       - Manage events and schedules
✅ Sheets         - Read and write spreadsheets
✅ Docs           - Create and edit documents
✅ Drive          - Access files and folders
```

**Google Cloud Platform**
```
✅ Cloud Run      - One-command deployment
✅ Vertex AI      - Native memory and RAG services
✅ BigQuery       - Data analytics integration
✅ Cloud Storage  - Artifact and file storage
```

#### 💡 Why ADK Claw?

| Feature | ADK Claw | Traditional Frameworks |
|---------|----------|----------------------|
| **Google ADK Native** | ✅ 100% Native | ❌ Custom implementations |
| **Google Workspace** | ✅ One-click OAuth | ⚠️ Manual configuration |
| **GCP Deployment** | ✅ Optimized | ⚠️ Generic |
| **Memory Services** | ✅ Vertex AI RAG | ⚠️ Third-party DBs |
| **Multi-Model** | ✅ 100+ models | ⚠️ Limited |

### 🚀 Quick Start

```bash
# Install
pip install adk-claw

# Initialize
adk-claw init

# Start
adk-claw run --telegram
```

### 📦 Deployment Options

#### Option A: Local Deployment (Free)
```bash
# Local SQLite + FileArtifactService
python3.10 -m adk_claw.cli run --telegram
```
- **Cost**: $0
- **Storage**: SQLite (persistent)
- **Privacy**: Data stays local

#### Option B: Cloud Deployment (GCP Native)
```bash
# Cloud Run + Vertex AI Memory Bank
gcloud run deploy adk-claw --source .
```
- **Cost**: ~$6-15/month
- **Storage**: Vertex AI Memory Bank
- **Features**: Semantic search, auto-scaling

### 🎯 Use Cases

1. **Personal Assistant** - Email, calendar, task management
2. **Team Collaboration** - Shared workspace automation
3. **Data Analysis** - BigQuery + Sheets integration
4. **Customer Support** - Gmail + Calendar scheduling
5. **Content Creation** - Docs + Drive integration

---

<a name="中文"></a>
## 中文

### 第一个原生 Google ADK Agent 平台

ADK Claw 是第一个基于原生 Google Agent Development Kit (ADK) 的开源 AI Agent 平台。专为 Google Workspace 和 Google Cloud Platform 深度集成而设计。

### ✨ 核心优势

#### 🚀 原生 ADK 优势
- **100% 原生 ADK** - 基于 Google 官方 Agent Development Kit
- **Google Workspace 集成** - 原生支持 Gmail、Calendar、Sheets、Docs
- **GCP 优化** - 在 Cloud Run 上无缝部署，Vertex AI 集成
- **多模型支持** - Gemini / GPT / Claude / DeepSeek / Ollama
- **多渠道** - Slack / Telegram（更多即将推出）
- **零配置** - Google Workspace 一键 OAuth

#### 🔗 Google 生态集成

**Google Workspace（一键配置）**
```
✅ Gmail          - 发送、读取、撰写邮件
✅ Calendar       - 管理事件和日程
✅ Sheets         - 读写电子表格
✅ Docs           - 创建和编辑文档
✅ Drive          - 访问文件和文件夹
```

**Google Cloud Platform**
```
✅ Cloud Run      - 一键部署
✅ Vertex AI      - 原生记忆和 RAG 服务
✅ BigQuery       - 数据分析集成
✅ Cloud Storage  - 文件和存储
```

#### 💡 为什么选择 ADK Claw？

| 特性 | ADK Claw | 传统框架 |
|------|----------|---------|
| **原生 Google ADK** | ✅ 100% 原生 | ❌ 自定义实现 |
| **Google Workspace** | ✅ 一键 OAuth | ⚠️ 手动配置 |
| **GCP 部署** | ✅ 优化 | ⚠️ 通用 |
| **记忆服务** | ✅ Vertex AI RAG | ⚠️ 第三方数据库 |
| **多模型** | ✅ 100+ 模型 | ⚠️ 有限 |

### 🚀 快速开始

```bash
# 安装
pip install adk-claw

# 初始化
adk-claw init

# 启动
adk-claw run --telegram
```

### 📦 部署方案

#### 方案 A：本地部署（免费）
```bash
# SQLite + FileArtifactService
python3.10 -m adk_claw.cli run --telegram
```
- **费用**：¥0
- **存储**：SQLite（持久化）
- **隐私**：数据本地保存

#### 方案 B：云端部署（GCP 原生）
```bash
# Cloud Run + Vertex AI Memory Bank
gcloud run deploy adk-claw --source .
```
- **费用**：约 ¥40-100/月
- **存储**：Vertex AI Memory Bank
- **特性**：语义搜索、自动扩容

### 🎯 应用场景

1. **个人助理** - 邮件、日程、任务管理
2. **团队协作** - 共享工作区自动化
3. **数据分析** - BigQuery + Sheets 集成
4. **客户支持** - Gmail + 日程安排
5. **内容创作** - Docs + Drive 集成

---

<a name="日本語"></a>
## 日本語

### 初のネイティブ Google ADK エージェントプラットフォーム

ADK Claw は、ネイティブ Google Agent Development Kit (ADK) で構築された最初のオープンソース AI エージェントプラットフォームです。Google Workspace と Google Cloud Platform とのシームレスな統合を実現。

### ✨ 主な特徴

#### 🚀 ネイティブ ADK の利点
- **100% ネイティブ ADK** - Google公式 Agent Development Kit ベース
- **Google Workspace 統合** - Gmail、Calendar、Sheets、Docs をネイティブサポート
- **GCP 最適化** - Cloud Run でのシームレスなデプロイ、Vertex AI 統合
- **マルチモデル対応** - Gemini / GPT / Claude / DeepSeek / Ollama
- **マルチチャンネル** - Slack / Telegram（今後さらに追加）
- **ゼロ設定** - Google Workspace のワンクリック OAuth

#### 🔗 Google エコシステム統合

**Google Workspace（ワンクリック設定）**
```
✅ Gmail          - メールの送信、読み取り、作成
✅ Calendar       - イベントとスケジュール管理
✅ Sheets         - スプレッドシートの読み書き
✅ Docs           - ドキュメントの作成と編集
✅ Drive          - ファイルとフォルダへのアクセス
```

**Google Cloud Platform**
```
✅ Cloud Run      - ワンコマンドデプロイ
✅ Vertex AI      - ネイティブメモリと RAG サービス
✅ BigQuery       - データ分析統合
✅ Cloud Storage  - アーティファクトとファイルストレージ
```

#### 💡 なぜ ADK Claw？

| 機能 | ADK Claw | 従来のフレームワーク |
|------|----------|-------------------|
| **ネイティブ Google ADK** | ✅ 100% ネイティブ | ❌ カスタム実装 |
| **Google Workspace** | ✅ ワンクリック OAuth | ⚠️ 手動設定 |
| **GCP デプロイ** | ✅ 最適化 | ⚠️ 汎用 |
| **メモリサービス** | ✅ Vertex AI RAG | ⚠️ サードパーティ DB |
| **マルチモデル** | ✅ 100+ モデル | ⚠️ 限定 |

### 🚀 クイックスタート

```bash
# インストール
pip install adk-claw

# 初期化
adk-claw init

# 起動
adk-claw run --telegram
```

### 📦 デプロイオプション

#### オプション A：ローカルデプロイ（無料）
```bash
# SQLite + FileArtifactService
python3.10 -m adk_claw.cli run --telegram
```
- **コスト**：¥0
- **ストレージ**：SQLite（永続化）
- **プライバシー**：データはローカル

#### オプション B：クラウドデプロイ（GCP ネイティブ）
```bash
# Cloud Run + Vertex AI Memory Bank
gcloud run deploy adk-claw --source .
```
- **コスト**：約 $6-15/月
- **ストレージ**：Vertex AI Memory Bank
- **機能**：セマンティック検索、自動スケーリング

### 🎯 ユースケース

1. **パーソナルアシスタント** - メール、カレンダー、タスク管理
2. **チームコラボレーション** - 共有ワークスペース自動化
3. **データ分析** - BigQuery + Sheets 統合
4. **カスタマーサポート** - Gmail + カレンダー予約
5. **コンテンツ作成** - Docs + Drive 統合

---

## CLI Commands / CLI 命令 / CLI コマンド

| Command | Description | 说明 | 説明 |
|---------|-------------|------|------|
| `adk-claw init` | Initialize configuration | 初始化配置 | 初期化 |
| `adk-claw config` | Configuration wizard | 配置向导 | 設定ウィザード |
| `adk-claw doctor` | Health check | 健康检查 | ヘルスチェック |
| `adk-claw run` | Start services | 启动服务 | サービス起動 |
| `adk-claw oauth-status` | Check OAuth status | 查看 OAuth 状态 | OAuth 状態確認 |

## Supported Models / 支持的模型 / 対応モデル

### Gemini 3.1 (Latest)
- `gemini-3.1-pro` - Most intelligent
- `gemini-3.1-flash` - Fast and efficient (Recommended)
- `gemini-3.1-flash-lite-preview` - Ultra-low cost

### Gemini 3 (Preview)
- `gemini-3-pro` - Advanced multimodal understanding
- `gemini-3-flash` - Excellent performance at low cost

### Other Providers
- **OpenAI**: GPT-4.1, GPT-4o, O3-mini
- **Anthropic**: Claude 3.7 Sonnet, Claude 3.5 Sonnet
- **DeepSeek**: DeepSeek Chat, DeepSeek Reasoner
- **Local**: Ollama (Llama 3.3, Qwen 2.5, Gemma 3)

## Architecture / 架构 / アーキテクチャ

```
┌─────────────────────────────────────────────┐
│  CLI (adk-claw init/config/run)             │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│  Web UI (localhost:8080)                    │
│  - OAuth Configuration                      │
│  - Google Workspace Setup                   │
└────────────────┬────────────────────────────┘
                 ↓
┌─────────────────────────────────────────────┐
│  ADK Claw Core (Native ADK)                 │
│  - Google ADK Agent                         │
│  - Multi-Channel Adapters                   │
│  - Google Workspace Tools                   │
└────────┬────────────────────┬───────────────┘
         ↓                    ↓
    Slack (Socket)      Telegram (Polling)
         ↓                    ↓
┌─────────────────────────────────────────────┐
│  Google Services                            │
│  - Gmail / Calendar / Sheets / Docs         │
│  - Vertex AI Memory Bank                    │
│  - Cloud Storage                            │
└─────────────────────────────────────────────┘
```

## Development / 开发 / 開発

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Code formatting
ruff format .

# Type checking
mypy .
```

## Contributing / 贡献 / 貢献

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License / 许可证 / ライセンス

MIT

---

**ADK Claw** - Native Google ADK Agent Platform 🦞
**ADK Claw** - 原生 Google ADK Agent 平台 🦞
**ADK Claw** - ネイティブ Google ADK エージェントプラットフォーム 🦞
