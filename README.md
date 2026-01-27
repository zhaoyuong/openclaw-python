# ClawdBot Python

**个人 AI 助手平台 - Python 完整实现**

这是 [ClawdBot](https://github.com/badlogic/clawdbot) 的完整 Python 克隆版本，从 TypeScript 移植而来。

ClawdBot 是一个本地优先的 AI 助手平台，可以连接多个消息渠道（WhatsApp、Telegram、Discord、Slack 等），通过这些渠道提供 AI 助手服务。

## 🌟 关于本项目

- **原始项目**: [ClawdBot (TypeScript)](https://github.com/badlogic/clawdbot)
- **Python 实现**: 完整功能对等移植
- **创建日期**: 2026-01-27
- **版本**: 0.1.0
- **许可证**: MIT

## Features

- **Multi-Channel Support**: WhatsApp, Telegram, Discord, Slack, WebChat, and more
- **Local-First**: Runs on your hardware, keeps your data private
- **Gateway Architecture**: Single WebSocket control plane for all clients
- **Agent Runtime**: Streaming LLM responses with tool calling
- **58+ Skills**: Pre-built capabilities for common tasks
- **Plugin System**: Extensible architecture for custom channels and tools
- **Web UI**: Control panel and WebChat interface

## Quick Start

### Installation

```bash
# Install with poetry
poetry install

# Or with pip
pip install -e .
```

### Setup

```bash
# Run onboarding wizard
clawdbot onboard

# Start gateway
clawdbot gateway start
```

### Usage

```bash
# Run agent turn
clawdbot agent --message "Hello!"

# Manage channels
clawdbot channels list
clawdbot channels login telegram

# Check status
clawdbot status
```

## Architecture

```
Messaging Channels → Gateway (WebSocket) → Agent Runtime → LLM
                                ↓
                            CLI/Web UI
```

## Development

```bash
# Install dev dependencies
poetry install --with dev

# Run tests
pytest

# Format code
black clawdbot/
ruff check clawdbot/
```

## License

MIT License
