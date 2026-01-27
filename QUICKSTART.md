# ClawdBot Python - 快速开始

这是 ClawdBot 的完整 Python 实现，从 TypeScript 版本移植而来。

## 功能特性

✅ **已实现的核心功能**：

### 基础架构
- ✅ Gateway WebSocket 服务器（端口 18789）
- ✅ Pydantic 配置管理
- ✅ Typer CLI 命令行工具
- ✅ FastAPI Web UI

### Agent 运行时
- ✅ Anthropic Claude & OpenAI 集成
- ✅ 会话管理（JSONL 持久化）
- ✅ 流式响应
- ✅ 工具调用框架

### 工具系统（6个核心工具）
- ✅ `read_file` - 读取文件
- ✅ `write_file` - 写入文件
- ✅ `edit_file` - 编辑文件
- ✅ `bash` - 执行命令
- ✅ `web_fetch` - 获取网页
- ✅ `web_search` - 网页搜索（占位符）

### 消息渠道（5个）
- ✅ **Telegram** - 完整集成
- ✅ **Discord** - Discord 机器人
- ✅ **Slack** - Slack 机器人
- ✅ **WhatsApp** - 占位符（需要库）
- ✅ **WebChat** - 内置网页聊天

### Skills 系统
- ✅ Skills 加载器
- ✅ 资格检查（OS、二进制、环境变量）
- ✅ 多源加载
- ✅ 4个示例 skills

### 插件系统
- ✅ 插件发现和加载
- ✅ 插件 API
- ✅ 5个扩展插件

### Web UI
- ✅ 控制面板
- ✅ WebChat 界面
- ✅ WebSocket 实时通信

## 快速安装

### 1. 安装依赖

```bash
cd clawdbot-python

# 使用 Poetry（推荐）
poetry install

# 或使用 pip
pip install -e .
```

### 2. 配置

```bash
# 运行向导
clawdbot onboard

# 或手动编辑配置
nano ~/.clawdbot/clawdbot.json
```

示例配置：
```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-5-20250514"
  },
  "gateway": {
    "port": 18789,
    "bind": "loopback"
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

### 3. 设置环境变量

```bash
export ANTHROPIC_API_KEY="your-api-key"
# 或
export OPENAI_API_KEY="your-api-key"
```

### 4. 启动服务

```bash
# 启动 Gateway
clawdbot gateway start

# 或使用 Makefile
make run
```

### 5. 启动 Web UI（可选）

```bash
# 在另一个终端
uvicorn clawdbot.web.app:app --reload --port 8080

# 或
make run-web

# 访问 http://localhost:8080
```

## 使用示例

### CLI 命令

```bash
# 运行 agent
clawdbot agent run "写一个 Python 函数计算斐波那契数列"

# 列出会话
clawdbot sessions list

# 管理渠道
clawdbot channels list
clawdbot channels login telegram

# 系统诊断
clawdbot doctor
```

### Telegram 集成

1. 从 @BotFather 获取 bot token
2. 配置：
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_TOKEN"
    }
  }
}
```
3. 启动 Gateway
4. 在 Telegram 给机器人发消息

### Discord 集成

1. 在 Discord Developer Portal 创建应用
2. 获取 bot token
3. 配置并启动

### WebChat

1. 启动 Web UI：`uvicorn clawdbot.web.app:app --port 8080`
2. 访问：http://localhost:8080/webchat
3. 直接在浏览器聊天

## 项目结构

```
clawdbot-python/
├── clawdbot/              # 主包
│   ├── agents/            # Agent 运行时
│   │   ├── runtime.py     # LLM 集成
│   │   ├── session.py     # 会话管理
│   │   └── tools/         # 工具实现
│   ├── channels/          # 消息渠道
│   │   ├── telegram.py
│   │   ├── discord.py
│   │   └── ...
│   ├── cli/               # CLI 命令
│   ├── config/            # 配置管理
│   ├── gateway/           # WebSocket 服务器
│   ├── plugins/           # 插件系统
│   ├── skills/            # Skills 加载器
│   └── web/               # Web UI
├── extensions/            # 渠道扩展
├── skills/                # 捆绑的 skills
├── tests/                 # 测试套件
└── ui/                    # Web UI 前端
```

## 开发

```bash
# 安装开发依赖
make dev

# 运行测试
make test

# 代码格式化
make format

# Linting
make lint

# 运行诊断
make doctor
```

## 测试

```bash
# 运行所有测试
pytest tests/ -v

# 带覆盖率
pytest tests/ -v --cov=clawdbot --cov-report=html

# 或使用 Makefile
make test
make test-cov
```

## 与 TypeScript 版本对比

| 组件 | TypeScript | Python |
|------|-----------|--------|
| Gateway | ✅ ws | ✅ websockets |
| HTTP | ✅ Express/Hono | ✅ FastAPI |
| 配置 | ✅ Zod | ✅ Pydantic |
| CLI | ✅ Commander | ✅ Typer |
| Agent | ✅ pi-agent-core | ✅ Anthropic/OpenAI SDK |
| 会话 | ✅ JSONL | ✅ JSONL |
| Telegram | ✅ grammY | ✅ python-telegram-bot |
| Discord | ✅ discord.js | ✅ discord.py |
| Skills | ✅ 58+ | ✅ 4（示例）|
| Web UI | ✅ Lit | ✅ Jinja2 + Alpine.js |

## 注意事项

⚠️ **WhatsApp 集成**需要额外的库（whatsapp-web.py 或类似）

⚠️ **Web Search** 需要搜索 API（DuckDuckGo、Google 等）

⚠️ **LanceDB Memory** 是占位符，需要完整实现

⚠️ **Skills** 只包含4个示例，TypeScript 版本有 58+

## 下一步

1. ✅ 添加更多 skills
2. ✅ 实现完整的 WhatsApp 支持
3. ✅ 完善 memory 系统
4. ✅ 添加浏览器自动化工具
5. ✅ 实现 cron jobs
6. ✅ 添加 Canvas/A2UI 工具

## 获取帮助

- 文档：查看 README.md 和 CONTRIBUTING.md
- 问题：运行 `clawdbot doctor` 进行诊断
- 示例：查看 `skills/` 目录的示例 skills

## 许可证

MIT License - 详见 LICENSE 文件
