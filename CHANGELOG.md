# Changelog

All notable changes to ClawdBot Python will be documented in this file.

## [0.1.0] - 2026-01-27

### Added

#### Core Infrastructure
- **Gateway Server**: WebSocket server on port 18789 with protocol versioning
- **Configuration System**: Pydantic-based config with JSON5 support
- **CLI**: Typer-based command-line interface with subcommands

#### Agent Runtime
- **LLM Integration**: Anthropic Claude and OpenAI support
- **Session Management**: JSONL-based conversation persistence
- **Streaming**: Real-time streaming responses
- **Tool Execution**: Async tool calling framework

#### Tools (6 Core Tools)
- `read_file` - Read file contents
- `write_file` - Write to files
- `edit_file` - Search and replace in files
- `bash` - Execute shell commands
- `web_fetch` - Fetch web pages
- `web_search` - Web search (placeholder)

#### Channels (5 Channels)
- **Telegram**: Full bot integration with python-telegram-bot
- **Discord**: Discord bot with discord.py
- **Slack**: Slack bot with slack-sdk
- **WhatsApp**: Placeholder (requires library)
- **WebChat**: Built-in web chat interface

#### Skills System
- Skills loader with frontmatter parsing
- Eligibility checking (OS, binaries, env vars)
- Multi-source loading (bundled, managed, workspace)
- 4 Example skills: coding-agent, github, weather, web-search

#### Plugin System
- Plugin discovery and loading
- Plugin API for extensions
- Extension manifests (plugin.json)
- 5 Extension plugins

#### Web UI
- FastAPI-based web server
- Control panel dashboard
- WebChat interface
- Real-time WebSocket communication
- Responsive dark theme

#### Documentation
- Comprehensive README
- Contributing guidelines
- Test suite with pytest
- Makefile for common tasks

### Technical Details
- Python 3.11+ required
- Poetry for dependency management
- Async/await throughout
- Type hints with Pydantic
- Modular architecture

### Known Limitations
- WhatsApp channel needs library integration
- Web search requires API key
- LanceDB memory is placeholder
- Some gateway methods are placeholders

## [Unreleased]

### Planned Features
- Full WhatsApp integration
- Browser automation tool (Playwright)
- Canvas/A2UI tool
- Complete memory system
- Cron jobs
- Voice support
- Native apps (iOS/Android)
- More bundled skills (target: 58+)
