# Contributing to ClawdBot Python

Thank you for your interest in contributing to ClawdBot!

## Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/clawdbot-python.git
cd clawdbot-python
```

2. **Install dependencies**
```bash
make dev
# or
poetry install --with dev
```

3. **Run tests**
```bash
make test
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Format your code before committing:
```bash
make format
make lint
```

## Testing

Write tests for new features:
```bash
# Run all tests
make test

# Run with coverage
make test-cov
```

Tests are located in `tests/` directory.

## Project Structure

```
clawdbot/
├── agents/          # Agent runtime and tools
├── channels/        # Messaging channel implementations
├── cli/             # Command-line interface
├── config/          # Configuration management
├── gateway/         # WebSocket gateway server
├── plugins/         # Plugin system
├── skills/          # Skills loader
└── web/             # Web UI
```

## Adding a New Channel

1. Create channel class in `clawdbot/channels/`
2. Implement `ChannelPlugin` interface
3. Create extension in `extensions/` with `plugin.json`
4. Add tests in `tests/`

## Adding a New Tool

1. Create tool class in `clawdbot/agents/tools/`
2. Inherit from `AgentTool` base class
3. Register in `registry.py`
4. Add tests

## Adding a New Skill

1. Create directory in `skills/`
2. Add `SKILL.md` with frontmatter
3. Document tool usage and examples

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Review

- Code must pass all tests
- Code must pass linting
- Add tests for new features
- Update documentation as needed

## Questions?

Open an issue or discussion on GitHub.
